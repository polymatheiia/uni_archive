# Create a new script that applies the similarity transform (reconstructed -> GT)
# and prints transformed endpoints and residuals. Then run it.
script_path = "./reconstruct_geometryA_uvwt_toGT.py"

script = r'''
import numpy as np, math, os
from numpy.linalg import svd, norm
import testing
# import the notebook-faithful reconstruction module
from reconstruct_geometryA_uvwt_notebook_version import reconstruct_from_histograms

def compute_similarity_transform(A_pts, B_pts):
    """
    Compute similarity transform (scale s, rotation R, translation t)
    mapping A_pts -> B_pts, where A_pts and B_pts are arrays shape (3, N).
    Uses Procrustes-like SVD method.
    Returns s, R (3x3), t (3,).
    """
    A = np.asarray(A_pts, dtype=float)
    B = np.asarray(B_pts, dtype=float)
    assert A.shape[0] == 3 and B.shape[0] == 3 and A.shape[1] == B.shape[1]
    N = A.shape[1]
    A_mean = A.mean(axis=1, keepdims=True)
    B_mean = B.mean(axis=1, keepdims=True)
    A0 = A - A_mean
    B0 = B - B_mean
    # covariance-like
    M = B0 @ A0.T
    U, S, Vt = svd(M)
    R = U @ Vt
    # ensure proper rotation (determinant +1), fix reflection if needed
    if np.linalg.det(R) < 0:
        # flip last column of U
        U[:, -1] *= -1
        R = U @ Vt
    # scale: sum singular values / sum squared norm of A0
    num = np.sum(S)
    den = np.sum(A0 * A0)
    s = (num / den) if den != 0 else 1.0
    t = (B_mean - s * R @ A_mean).ravel()
    return s, R, t

def apply_similarity(A_pts, s, R, t):
    A = np.asarray(A_pts, dtype=float)
    return (s * (R @ A) + t.reshape(3,1))

# load test data and run reconstruction
raw = testing.getTestData("middle")
res = reconstruct_from_histograms(raw, n_samples=600)
ep0 = res["ep0_mm"]
ep1 = res["ep1_mm"]
pts = res["pts"].T  # pts shape (3, N)

# ground truth
gt0 = np.array(raw[3], dtype=float)
gt1 = np.array(raw[4], dtype=float)
GT = np.column_stack([gt0, gt1])  # shape (3,2)
RECON = np.column_stack([ep0, ep1])  # shape (3,2)

print("Reconstructed endpoints (original detector frame):")
print(" ep0:", ep0)
print(" ep1:", ep1)
print("GT endpoints (as in testing.py):")
print(" gt0:", gt0)
print(" gt1:", gt1)

# compute transform mapping RECON -> GT
s, R, t = compute_similarity_transform(RECON, GT)
print("\\nComputed similarity transform mapping reconstructed -> GT:")
print(" scale s =", s)
print(" rotation matrix R =\\n", R)
print(" translation t =", t)

# apply to ep0/ep1 and to all pts
RECON_pts = np.column_stack([ep0, ep1])
RECON_pts_T = apply_similarity(RECON_pts.T.T, s, R, t)  # returns 3x2
ep0_t, ep1_t = RECON_pts_T[:,0], RECON_pts_T[:,1]

pts_transformed = apply_similarity(pts, s, R, t)  # 3xN

print("\\nTransformed endpoints into GT frame:")
print(" ep0_trans:", ep0_t)
print(" ep1_trans:", ep1_t)
print("Residuals to GT after transform:")
print(" ||ep0_trans - gt0|| =", norm(ep0_t - gt0))
print(" ||ep1_trans - gt1|| =", norm(ep1_t - gt1))

# compute residuals for all sampled pts relative to linear interpolation between GT endpoints
# project each transformed pt onto GT line segment to measure perpendicular residual
GT_dir = (gt1 - gt0)
GT_dir_norm = GT_dir / (np.linalg.norm(GT_dir)+1e-12)
proj_vals = (pts_transformed.T - gt0) @ GT_dir_norm
closest = gt0.reshape(1,3) + np.outer(proj_vals, GT_dir_norm)
residuals_all = np.linalg.norm(pts_transformed.T - closest, axis=1)
print("\\nStats of per-point residuals after transform (mm):")
print("  max:", residuals_all.max(), "mean:", residuals_all.mean(), "median:", np.median(residuals_all))

# Save a tiny JSON summary to /mnt/data for you to inspect
import json
out = {
    "ep0": ep0.tolist(),
    "ep1": ep1.tolist(),
    "gt0": gt0.tolist(),
    "gt1": gt1.tolist(),
    "scale": float(s),
    "translation": t.tolist(),
    "rotation": R.tolist(),
    "residual_ep0": float(norm(ep0_t - gt0)),
    "residual_ep1": float(norm(ep1_t - gt1)),
    "residuals_all_max": float(residuals_all.max()),
    "residuals_all_mean": float(residuals_all.mean())
}
with open("/mnt/data/reconstruction_toGT_summary.json", "w") as f:
    json.dump(out, f, indent=2)
print("\\nWrote summary to /mnt/data/reconstruction_toGT_summary.json")
'''

with open(script_path, "w") as f:
    f.write(script)

# Run the script with the local python interpreter
import subprocess, shlex, sys, os
py = "/home/sool/miniconda3/envs/torch-cf/bin/python"
cmd = f"{py} {script_path}"
print("Running:", cmd)
proc = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
print("=== STDOUT ===")
print(proc.stdout)
print("=== STDERR ===")
print(proc.stderr)

script_path

