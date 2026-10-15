# recon_diagnostics.py
import numpy as np, math, os
from numpy.linalg import svd, norm

# Paths (local files used by previous code)
print("Local file paths (for reference):")
print(" - testing.py path (in project):", os.path.abspath("testing.py"))
print(" - patched notebook recon (if present):", os.path.abspath("reconstruct_geometryA_uvwt_notebook_version.py"))
print(" - patched project recon (if present):", os.path.abspath("reconstruct_geometryA_uvwt_patched.py"))
print()

# Import testing and our notebook reconstruction implementations
import testing  # must be importable in your project env

# Import functions from the notebook-faithful module if you have it in the same folder.
# If not, fall back to in-file redefinitions.
try:
    from reconstruct_geometryA_uvwt_notebook_version import invert_uvwt_point, fit_2d_line_from_hist, reconstruct_from_histograms, PHIS
except Exception:
    # If you don't have that file, we define the exact notebook inverse here.
    PHIS = {"U": 0.0, "V": np.deg2rad(30.0), "W": np.deg2rad(-30.0)}
    STRIP_PITCH = 1.5
    REF_X = -138.9971
    REF_Y = 98.25
    SAMPLING_FREQUENCY = 25.0
    DRIFT_VELOCITY = 6.46
    F_TBIN_TO_MM = DRIFT_VELOCITY / SAMPLING_FREQUENCY
    T_OFFSET_CONST = 256.0
    TRIGGER_DELAY = 5.0

    def invert_uvwt_point(u_bin, v_bin, w_bin, t_bin, phis=PHIS):
        y_mm = 99.75 - STRIP_PITCH * float(u_bin)
        U_mm = STRIP_PITCH * float(v_bin) - 98.75
        W_mm = STRIP_PITCH * float(w_bin) - 98.75
        Vphi = float(phis["V"]); Wphi = float(phis["W"])
        cosV = math.cos(Vphi); sinV = math.sin(Vphi)
        cosW = math.cos(-Wphi); sinW = math.sin(-Wphi)
        rhs_v = U_mm + (y_mm - REF_Y) * sinV
        rhs_w = W_mm + (y_mm - REF_Y) * sinW
        denom = cosV*cosV + cosW*cosW
        denom = denom if abs(denom) > 1e-12 else 1e-12
        x_minus_ref = (cosV*rhs_v + cosW*rhs_w) / denom
        x_mm = REF_X + x_minus_ref
        z_mm = (float(t_bin) - T_OFFSET_CONST - TRIGGER_DELAY) * F_TBIN_TO_MM
        return x_mm, y_mm, z_mm

    def fit_2d_line_from_hist(hist, keep_percentile=90.0):
        H, W = hist.shape
        T, C = np.meshgrid(np.arange(H), np.arange(W), indexing='ij')
        Tf = T.ravel(); Cf = C.ravel(); If = hist.ravel()
        thr = np.percentile(If, keep_percentile)
        sel = If >= thr
        if sel.sum() < 50:
            sel = If > 0
        weights = np.sqrt(np.maximum(If[sel], 1e-12))
        A = np.vstack([Tf[sel], np.ones(sel.sum())]).T
        Aw = A * weights[:, None]
        bw = Cf[sel] * weights
        p, *_ = np.linalg.lstsq(Aw, bw, rcond=None)
        return float(p[0]), float(p[1])

    def reconstruct_from_histograms(raw, n_samples=400):
        histU, histV, histW = raw[0]
        a_u, b_u = fit_2d_line_from_hist(histU)
        a_v, b_v = fit_2d_line_from_hist(histV)
        a_w, b_w = fit_2d_line_from_hist(histW)
        H, W = histU.shape
        t_vals = np.linspace(0, H-1, n_samples)
        u_bins = a_u * t_vals + b_u
        v_bins = a_v * t_vals + b_v
        w_bins = a_w * t_vals + b_w
        xs = np.empty(n_samples); ys = np.empty(n_samples); zs = np.empty(n_samples)
        for i in range(n_samples):
            xs[i], ys[i], zs[i] = invert_uvwt_point(u_bins[i], v_bins[i], w_bins[i], t_vals[i])
        pts = np.column_stack((xs, ys, zs))
        center = pts.mean(axis=0)
        U, S, Vt = np.linalg.svd((pts - center).T, full_matrices=False)
        dirv = U[:,0]; dirv = dirv / (np.linalg.norm(dirv)+1e-12)
        proj = (pts - center) @ dirv
        ep0 = center + dirv * proj.min()
        ep1 = center + dirv * proj.max()
        return {"ep0_mm": ep0, "ep1_mm": ep1, "center": center, "direction": dirv, "fits": ((a_u,b_u),(a_v,b_v),(a_w,b_w)), "pts": pts}

print("Imported testing.py from:", testing.__file__)

# Pull test data
raw = testing.getTestData("middle")
hist_list = raw[0]
gt0 = np.array(raw[3], float)
gt1 = np.array(raw[4], float)
print("\nGT endpoints:\n GT0:", gt0, "\n GT1:", gt1)

# Forward function
def forward_point(xyz):
    xyz = np.asarray(xyz, float).reshape(1,3)
    uvwt = testing.getXYZtoUVWT(xyz)[0]
    return uvwt

# 1) forward->inverse on GT endpoints
print("\n1) Forward->Inverse on GT endpoints")
for i,pt in enumerate((gt0, gt1)):
    u,v,w,t = forward_point(pt)
    inv = invert_uvwt_point(u,v,w,t)
    print(f" GT{i}: {pt} -> UVWT: {(u,v,w,t)} -> inv: {inv}  err={norm(np.array(inv)-pt)}")

# 2) forward->inverse on samples along the GT line
print("\n2) Round-trip on samples along the GT line")
samples = [gt0 + (gt1-gt0)*alpha for alpha in np.linspace(0,1,11)]
errs = []
for s,pt in enumerate(samples):
    u,v,w,t = forward_point(pt)
    inv = invert_uvwt_point(u,v,w,t)
    e = norm(np.array(inv)-pt)
    errs.append(e)
    print(f"  s={s:2d} err={e:.6f}")
print("  max,mean:", max(errs), np.mean(errs))

# 3) Fit 2D lines on histograms
hU, hV, hW = hist_list
print("\n3) hist shapes:", hU.shape, hV.shape, hW.shape)
fits = (fit_2d_line_from_hist(hU), fit_2d_line_from_hist(hV), fit_2d_line_from_hist(hW))
print("  fits (a,b) U,V,W:", fits)

# 4) Run full reconstruction and compare to GT
print("\n4) Full reconstruction via notebook method:")
res = reconstruct_from_histograms(raw, n_samples=600)
ep0 = res["ep0_mm"]; ep1 = res["ep1_mm"]
print("  ep0:", ep0)
print("  ep1:", ep1)
print("  GT0:", gt0)
print("  GT1:", gt1)
print("  errs:", norm(ep0-gt0), norm(ep1-gt1))

# 5) Check whether mismatch is a rigid transform (translation+rotation+scale)
#    Compute Procrustes (similarity) transform from reconstructed pair -> GT pair
A = np.vstack([ep0, ep1]).T  # 3x2
B = np.vstack([gt0, gt1]).T  # 3x2
# centralize
Am = A.mean(axis=1, keepdims=True); Bm = B.mean(axis=1, keepdims=True)
A0 = A - Am; B0 = B - Bm
# find scale and rotation using SVD on 3x2 matrices mapped via 2 point sets
# treat columns as points; compute best-fit linear map R*s such that R*s @ A0 ≈ B0
U, svals, Vt = svd(B0 @ A0.T)
R = U @ Vt
scale = np.trace(np.diag(svals))/np.trace(A0 @ A0.T) if np.trace(A0 @ A0.T)!=0 else 1.0
# transform A -> Atrans
Atrans = (scale * R @ (A - Am)) + Bm
errs_after = [norm(Atrans[:,i]-B[:,i]) for i in range(A.shape[1])]
print("\n5) Procrustes-like transform diagnostic:")
print("  rotation matrix R:\n", R)
print("  scale:", scale)
print("  transformed ep0/ep1:", Atrans[:,0], Atrans[:,1])
print("  residuals after transform:", errs_after)

print("\nIf residuals after transform are small but raw errs are large, the mismatch is mainly a rigid-frame scaling/rotation/translation issue.")
print("If residuals after transform are still large, the inverse algebra or constants are wrong.")
