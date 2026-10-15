# diagnostics_snippet.py
import numpy as np
from numpy.linalg import svd, norm
import matplotlib.pyplot as plt
import os


# paste or import your res and raw (here we assume they are available)
# If you run this standalone, import JSON summary and images and testing.getTestData
# For quick use, run inside same Python process after tomographic reconstruction.

def print_top_voxels_uvwt(res, raw, top_n=20):
    density = res['density']; grid = res['grid']
    ny,nx,nz = density.shape
    flat = density.ravel()
    idx_sorted = np.argsort(flat)[::-1]
    top = idx_sorted[:min(top_n, flat.size)]
    print("Top voxel forward projections (uvwt) and density:")
    for k in top:
        iy = (k // (nx*nz)) % ny
        rest = k % (nx*nz)
        ix = rest // nz
        iz = rest % nz
        x = grid['x_centers'][ix]; y = grid['y_centers'][iy]; z = grid['z_centers'][iz]
        # forward map from your pipeline (ensure function xyz_to_uvwt available)
        u = -(y - 99.75) / 1.5
        Vphi = np.deg2rad(30.0)
        Wphi = np.deg2rad(-30.0)
        v_mm = (x - (-138.9971)) * np.cos(Vphi) - (y - 98.25) * np.sin(Vphi) + 98.75
        v = v_mm / 1.5
        w_mm = (x - (-138.9971)) * np.cos(-Wphi) - (y - 98.25) * np.sin(-Wphi) + 98.75
        w = w_mm / 1.5
        f = 6.46 / 25.0
        t = z / f + 256 + 5
        print(f" voxel idx({ix},{iy},{iz}) xyz=({x:.2f},{y:.2f},{z:.2f}) -> u={u:.2f}, v={v:.2f}, w={w:.2f}, t={t:.2f}, density={flat[k]:.6f}")

def procrustes_similarity(A, B):
    # A,B are 3xN matrices of corresponding points (N>=1). Returns s,R,t such that B ≈ s R A + t
    A = np.asarray(A, float); B = np.asarray(B, float)
    assert A.shape[0] == 3 and B.shape[0] == 3
    A_mean = A.mean(axis=1, keepdims=True)
    B_mean = B.mean(axis=1, keepdims=True)
    A0 = A - A_mean; B0 = B - B_mean
    M = B0 @ A0.T
    U,S,Vt = svd(M)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        U[:,-1] *= -1
        R = U @ Vt
    s = S.sum() / (np.sum(A0*A0) + 1e-12)
    t = (B_mean - s * R @ A_mean).ravel()
    return s, R, t

# assume res and raw exist:
best = res.get('best_cluster')
if best is None:
    print("No best cluster to analyze")
else:
    print("Cluster center:", best['center'])
    print("Cluster direction:", best['direction'])
    print_top_voxels_uvwt(res, raw, top_n=30)

    # Compare endpoints to GT
    ep0 = np.asarray(best['ep0']); ep1 = np.asarray(best['ep1'])
    if raw and len(raw) >= 5:
        gt0 = np.asarray(raw[3]); gt1 = np.asarray(raw[4])
        # try both pairings
        d_direct = np.linalg.norm(ep0-gt0) + np.linalg.norm(ep1-gt1)
        d_swapped = np.linalg.norm(ep0-gt1) + np.linalg.norm(ep1-gt0)
        print("direct distances:", np.linalg.norm(ep0-gt0), np.linalg.norm(ep1-gt1), "total=", d_direct)
        print("swapped distances:", np.linalg.norm(ep0-gt1), np.linalg.norm(ep1-gt0), "total=", d_swapped)

        # Procrustes: are these the same shape up to similarity?
        A = np.column_stack([ep0, ep1])  # 3x2
        B = np.column_stack([gt0, gt1])
        s,R,t = procrustes_similarity(A, B)
        Atrans = s * (R @ A) + t.reshape(3,1)
        resids = np.linalg.norm(Atrans - B, axis=0)
        print("Procrustes scale, residuals:", s, resids)

    # plot XY slice at cluster Z
    grid = res['grid']; density = res['density']
    # find nearest z index to cluster center
    zc = best['center'][2]
    iz = int(np.argmin(np.abs(grid['z_centers'] - zc)))
    print("Plotting XY slice at cluster z idx", iz, "z=", grid['z_centers'][iz])
    fig, ax = plt.subplots(figsize=(6,5))
    im = ax.imshow(density[:,:,iz].T, origin='lower', aspect='auto',
                   extent=[grid['x_centers'][0], grid['x_centers'][-1], grid['y_centers'][0], grid['y_centers'][-1]])
    ax.set_title(f"Density XY slice at cluster z={grid['z_centers'][iz]:.2f}")
    fig.colorbar(im, ax=ax)
    path = os.path.join("tomo_output", "density_xy_at_cluster_z.png")
    fig.savefig(path, dpi=200, bbox_inches='tight'); plt.close(fig)
    print("Saved:", path)
