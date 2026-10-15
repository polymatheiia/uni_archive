#!/usr/bin/env python3
"""
reconstruct_geometryA_tomo_with_gt.py

Standalone tomographic reconstruction runner with GT comparison.
Run: python reconstruct_geometryA_tomo_with_gt.py

Outputs:
 - PNG visuals in ./tomo_output/
 - JSON summary ./tomo_output/tomo_summary_with_gt.json
 - verbose stdout diagnostics including raw endpoint errors vs GT
"""

import os
import json
import math
from collections import deque
import numpy as np
from numpy.linalg import svd, norm
import matplotlib.pyplot as plt

# ---------------------------
# Detector geometry constants (must match main pipeline)
# ---------------------------
REF_X = -138.9971
REF_Y = 98.25
STRIP_PITCH = 1.5
SAMPLING_FREQUENCY = 25.0
DRIFT_VELOCITY = 6.46
F_TBIN_TO_MM = DRIFT_VELOCITY / SAMPLING_FREQUENCY
T_OFFSET_CONST = 256.0
TRIGGER_DELAY = 5.0
PHIS = {"U": 0.0, "V": np.deg2rad(30.0), "W": np.deg2rad(-30.0)}

# ---------------------------
# Forward mapping helper (xyz -> u,v,w,t fractional)
# ---------------------------
def xyz_to_uvwt(xs, ys, zs):
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    zs = np.asarray(zs, dtype=float)
    Vphi = float(PHIS["V"])
    Wphi = float(PHIS["W"])
    u = -(ys - 99.75) / STRIP_PITCH
    v_mm = (xs - REF_X) * math.cos(Vphi) - (ys - REF_Y) * math.sin(Vphi) + 98.75
    v = v_mm / STRIP_PITCH
    cosW = math.cos(-Wphi)
    w_mm = (xs - REF_X) * cosW - (ys - REF_Y) * math.sin(-Wphi) + 98.75
    w = w_mm / STRIP_PITCH
    f = F_TBIN_TO_MM
    t = zs / f + T_OFFSET_CONST + TRIGGER_DELAY
    return u, v, w, t

# ---------------------------
# Small helpers
# ---------------------------
def _find_3d_components(binary):
    ny, nx, nz = binary.shape
    visited = np.zeros(binary.shape, dtype=bool)
    comps = []
    neighbors = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
    for iy in range(ny):
        for ix in range(nx):
            for iz in range(nz):
                if binary[iy,ix,iz] and not visited[iy,ix,iz]:
                    q = deque()
                    q.append((iy,ix,iz))
                    visited[iy,ix,iz] = True
                    comp = []
                    while q:
                        cy,cx,cz = q.popleft()
                        comp.append((cy,cx,cz))
                        for dy,dx,dz in neighbors:
                            nyi, nxi, nzi = cy+dy, cx+dx, cz+dz
                            if 0 <= nyi < ny and 0 <= nxi < nx and 0 <= nzi < nz:
                                if binary[nyi,nxi,nzi] and not visited[nyi,nxi,nzi]:
                                    visited[nyi,nxi,nzi] = True
                                    q.append((nyi,nxi,nzi))
                    comps.append(comp)
    comps.sort(key=lambda c: len(c), reverse=True)
    return comps

# ---------------------------
# Simple tomographic backprojection (product or sum), non-soft (fast)
# ---------------------------
def tomographic_reconstruct(raw, voxel_params, vote_method="sum", threshold_frac=0.05, min_cluster_size=6):
    """
    Fast tomographic reconstruction (integer-bin mapping).
    raw[0] must be (histU, histV, histW).
    """
    histU, histV, histW = raw[0]
    histU = np.asarray(histU, dtype=float)
    histV = np.asarray(histV, dtype=float)
    histW = np.asarray(histW, dtype=float)
    T, W = histU.shape

    # normalize to avoid scale issues for product
    hU = histU / (histU.max() if histU.max() > 0 else 1.0)
    hV = histV / (histV.max() if histV.max() > 0 else 1.0)
    hW = histW / (histW.max() if histW.max() > 0 else 1.0)

    x_centers = np.linspace(voxel_params['x_min'], voxel_params['x_max'], voxel_params['nx'])
    y_centers = np.linspace(voxel_params['y_min'], voxel_params['y_max'], voxel_params['ny'])
    z_centers = np.linspace(voxel_params['z_min'], voxel_params['z_max'], voxel_params['nz'])
    nx = voxel_params['nx']; ny = voxel_params['ny']; nz = voxel_params['nz']

    Xc, Yc, Zc = np.meshgrid(x_centers, y_centers, z_centers, indexing='xy')
    flat_x = Xc.ravel(); flat_y = Yc.ravel(); flat_z = Zc.ravel()
    Nvox = flat_x.size

    u_pred, v_pred, w_pred, t_pred = xyz_to_uvwt(flat_x, flat_y, flat_z)
    u_idx = np.round(u_pred).astype(int)
    v_idx = np.round(v_pred).astype(int)
    w_idx = np.round(w_pred).astype(int)
    t_idx = np.round(t_pred).astype(int)

    mask = (t_idx >= 0) & (t_idx < T) & (u_idx >= 0) & (u_idx < W) & (v_idx >= 0) & (v_idx < W) & (w_idx >= 0) & (w_idx < W)
    density_flat = np.zeros(Nvox, dtype=float)
    valid_idx = np.nonzero(mask)[0]

    if valid_idx.size > 0:
        if vote_method == "product":
            eps = 1e-12
            tu = t_idx[valid_idx]; uu = u_idx[valid_idx]
            tv = t_idx[valid_idx]; vv = v_idx[valid_idx]
            tw = t_idx[valid_idx]; ww = w_idx[valid_idx]
            density_flat[valid_idx] = (hU[tu, uu] + eps) * (hV[tv, vv] + eps) * (hW[tw, ww] + eps)
        else:
            tu = t_idx[valid_idx]; uu = u_idx[valid_idx]
            tv = t_idx[valid_idx]; vv = v_idx[valid_idx]
            tw = t_idx[valid_idx]; ww = w_idx[valid_idx]
            density_flat[valid_idx] = hU[tu, uu] + hV[tv, vv] + hW[tw, ww]

    density = density_flat.reshape((ny, nx, nz))
    max_d = float(density.max()) if density.size>0 else 0.0
    nonzero = int(np.count_nonzero(density))
    thr = threshold_frac * max_d if max_d>0 else 0.0
    occupied = density > thr
    components = _find_3d_components(occupied)

    clusters = []
    for comp in components:
        coords = np.array(comp, dtype=int)
        ys_idx = coords[:,0]; xs_idx = coords[:,1]; zs_idx = coords[:,2]
        x_vals = x_centers[xs_idx]; y_vals = y_centers[ys_idx]; z_vals = z_centers[zs_idx]
        weights = density[ys_idx, xs_idx, zs_idx]
        clusters.append({'coords_idx': coords, 'xyz': np.vstack([x_vals,y_vals,z_vals]).T, 'weights': weights})

    best_cluster = None
    if len(clusters) > 0:
        clusters_sorted = sorted(clusters, key=lambda c: (len(c['weights']), np.sum(c['weights'])), reverse=True)
        cand = clusters_sorted[0]
        if len(cand['weights']) >= min_cluster_size:
            xyz = cand['xyz']; w = cand['weights']
            Wsum = np.sum(w) if np.sum(w)>0 else w.size
            center = np.sum(xyz * w.reshape(-1,1), axis=0) / Wsum
            X = (xyz - center) * np.sqrt(w.reshape(-1,1))
            U, S, Vt = svd(X, full_matrices=False)
            direction = Vt[0, :]
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            proj = (xyz - center) @ direction
            smin, smax = float(np.min(proj)), float(np.max(proj))
            ep0 = center + direction * smin
            ep1 = center + direction * smax
            best_cluster = dict(center=center, direction=direction, ep0=ep0, ep1=ep1, xyz=xyz, weights=w)

    result = {
        "density": density,
        "grid": {"x_centers": x_centers, "y_centers": y_centers, "z_centers": z_centers},
        "max_density": max_d,
        "nonzero_voxels": nonzero,
        "components": len(components),
        "clusters": len(clusters),
        "best_cluster": best_cluster
    }
    return result

# ---------------------------
# Adaptive wrapper (coarse -> refine)
# ---------------------------
def adaptive_tomography(raw):
    coarse_params = dict(x_min=-200, x_max=200, nx=80, y_min=-100, y_max=200, ny=80, z_min=-300, z_max=100, nz=60)
    methods = [('product', 0.12), ('product', 0.05), ('sum', 0.12), ('sum', 0.05), ('sum', 0.02)]
    print("[adaptive] trying coarse methods")
    for vote, thr in methods:
        print(f"  try vote={vote} thr={thr}")
        res = tomographic_reconstruct(raw, voxel_params=coarse_params, vote_method=vote, threshold_frac=thr, min_cluster_size=8)
        print(f"    max_density={res['max_density']:.6f} nonzero_voxels={res['nonzero_voxels']} comps={res['components']} clusters={res['clusters']}")
        if res['best_cluster'] is not None:
            print("    -> found cluster on coarse grid")
            return res, {"stage": "coarse", "vote": vote, "threshold_frac": thr, "voxel_params": coarse_params}
    # coarse failed -> linear-based bbox
    print("[adaptive] coarse failed, attempting linear-based bbox")
    try:
        import importlib
        linmod = importlib.import_module("reconstruct_geometryA_uvwt")
        linres = linmod.reconstruct_from_histograms_notebook(raw, n_samples=600)
        bbox = _voxel_params_from_linear_bbox(linres, half_length_along=150.0, orth_margin=40.0, nx=140, ny=140, nz=100)
        print("  bbox from linear:", bbox)
    except Exception as e:
        print("  linear-based bbox failed:", e)
        bbox = dict(x_min=-200, x_max=200, nx=120, y_min=-100, y_max=200, ny=120, z_min=-300, z_max=100, nz=80)
    # refined tries
    for vote, thr in [('sum', 0.02), ('sum', 0.01), ('sum', 0.005)]:
        print(f"  refined try vote={vote} thr={thr}")
        res = tomographic_reconstruct(raw, voxel_params=bbox, vote_method=vote, threshold_frac=thr, min_cluster_size=6)
        print(f"    max_density={res['max_density']:.6f} nonzero_voxels={res['nonzero_voxels']} comps={res['components']} clusters={res['clusters']}")
        if res['best_cluster'] is not None:
            print("    -> found cluster on refined bbox")
            return res, {"stage": "refined", "vote": vote, "threshold_frac": thr, "voxel_params": bbox}
    print("[adaptive] all attempts failed")
    return None, None

# helper to build bbox from linear result
def _voxel_params_from_linear_bbox(linres, half_length_along=200.0, orth_margin=80.0, nx=120, ny=120, nz=80):
    center = np.asarray(linres['center'], dtype=float)
    direction = np.asarray(linres['direction'], dtype=float)
    direction = direction / (np.linalg.norm(direction) + 1e-12)
    ref = np.array([1.0,0.0,0.0])
    if abs(np.dot(ref, direction)) > 0.9:
        ref = np.array([0.0,1.0,0.0])
    u1 = np.cross(direction, ref); u1 /= (np.linalg.norm(u1) + 1e-12)
    u2 = np.cross(direction, u1); u2 /= (np.linalg.norm(u2) + 1e-12)
    corners = []
    for sx in [-1,1]:
        for sy in [-1,1]:
            for sz in [-1,1]:
                p = center + sx*direction*half_length_along + sy*u1*orth_margin + sz*u2*orth_margin
                corners.append(p)
    corners = np.array(corners)
    mins = corners.min(axis=0) - 1.0
    maxs = corners.max(axis=0) + 1.0
    return dict(x_min=float(mins[0]), x_max=float(maxs[0]), nx=int(nx),
                y_min=float(mins[1]), y_max=float(maxs[1]), ny=int(ny),
                z_min=float(mins[2]), z_max=float(maxs[2]), nz=int(nz))

# ---------------------------
# GT comparison (raw error only)
# ---------------------------
def compare_to_gt_if_present(raw, ep0, ep1, verbose=True):
    ep0 = np.asarray(ep0, dtype=float)
    ep1 = np.asarray(ep1, dtype=float)
    if raw is None or not isinstance(raw, (tuple,list)) or len(raw) < 5:
        if verbose:
            print("[GT compare] No GT endpoints found in raw (expected raw[3], raw[4]).")
        return None
    try:
        gt0 = np.asarray(raw[3], dtype=float)
        gt1 = np.asarray(raw[4], dtype=float)
    except Exception:
        if verbose:
            print("[GT compare] raw[3]/raw[4] exist but could not be parsed as numeric arrays.")
        return None

    d00 = float(np.linalg.norm(ep0 - gt0))
    d11 = float(np.linalg.norm(ep1 - gt1))
    total_direct = d00 + d11
    d01 = float(np.linalg.norm(ep0 - gt1))
    d10 = float(np.linalg.norm(ep1 - gt0))
    total_swapped = d01 + d10

    if total_direct <= total_swapped:
        pairing = "direct"
        distances = {"ep0->gt0": d00, "ep1->gt1": d11}
    else:
        pairing = "swapped"
        distances = {"ep0->gt1": d01, "ep1->gt0": d10}

    if verbose:
        print("[GT compare] best pairing:", pairing)
        for k,v in distances.items():
            print(f"   {k} distance = {v:.6f} mm")
        print(f"   total_direct = {total_direct:.6f} mm, total_swapped = {total_swapped:.6f} mm")
    return {"pairing": pairing, "distances": distances, "total_direct": total_direct, "total_swapped": total_swapped}

# ---------------------------
# Visualization utilities
# ---------------------------
def save_png(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close(fig)

def plot_density_slices(density, grid, outdir):
    ny, nx, nz = density.shape
    x_centers = grid['x_centers']; y_centers = grid['y_centers']; z_centers = grid['z_centers']
    maxd = density.max() if density.size>0 else 1.0
    mid_z = nz // 2
    fig, ax = plt.subplots(figsize=(6,5))
    im = ax.imshow(density[:,:,mid_z].T, origin='lower', aspect='auto',
                   extent=[x_centers[0], x_centers[-1], y_centers[0], y_centers[-1]],
                   vmin=0, vmax=maxd, cmap='inferno')
    ax.set_title("Density XY slice (mid z)")
    ax.set_xlabel("X [mm]"); ax.set_ylabel("Y [mm]")
    fig.colorbar(im, ax=ax, label='density')
    save_png(fig, os.path.join(outdir, "density_xy_midz.png"))

    fig, ax = plt.subplots(figsize=(6,5))
    proj_xz = density.sum(axis=0)
    im = ax.imshow(proj_xz.T, origin='lower', aspect='auto',
                   extent=[x_centers[0], x_centers[-1], z_centers[0], z_centers[-1]],
                   vmin=0, vmax=proj_xz.max() if proj_xz.max()>0 else 1, cmap='magma')
    ax.set_title("Density XZ projection (sum over Y)")
    ax.set_xlabel("X [mm]"); ax.set_ylabel("Z [mm]")
    fig.colorbar(im, ax=ax)
    save_png(fig, os.path.join(outdir, "density_xz_proj.png"))

    fig, ax = plt.subplots(figsize=(6,5))
    proj_yz = density.sum(axis=1)
    im = ax.imshow(proj_yz.T, origin='lower', aspect='auto',
                   extent=[y_centers[0], y_centers[-1], z_centers[0], z_centers[-1]],
                   vmin=0, vmax=proj_yz.max() if proj_yz.max()>0 else 1, cmap='magma')
    ax.set_title("Density YZ projection (sum over X)")
    ax.set_xlabel("Y [mm]"); ax.set_ylabel("Z [mm]")
    fig.colorbar(im, ax=ax)
    save_png(fig, os.path.join(outdir, "density_yz_proj.png"))

def plot_top_voxel_scatter(res, outdir, top_n=500):
    density = res['density']; grid = res['grid']
    ny,nx,nz = density.shape
    flat = density.ravel()
    idx_sorted = np.argsort(flat)[::-1]
    top = idx_sorted[:min(top_n, flat.size)]
    xs=[]; ys=[]; zs=[]; ds=[]
    for k in top:
        iy = (k // (nx*nz)) % ny
        rest = k % (nx*nz)
        ix = rest // nz
        iz = rest % nz
        xs.append(grid['x_centers'][ix]); ys.append(grid['y_centers'][iy]); zs.append(grid['z_centers'][iz]); ds.append(flat[k])
    fig = plt.figure(figsize=(8,6)); ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(xs, ys, zs, c=ds, cmap='plasma', s=14)
    ax.set_title("Top voxel centers (by density)")
    ax.set_xlabel("X [mm]"); ax.set_ylabel("Y [mm]"); ax.set_zlabel("Z [mm]")
    fig.colorbar(sc, ax=ax, pad=0.08, label='voxel density')
    save_png(fig, os.path.join(outdir, "top_voxels_scatter.png"))

def plot_best_cluster_3d(best, outdir, linear_res=None):
    xyz = best['xyz']; w = best['weights']; center = best['center']; d = best['direction']; ep0 = best['ep0']; ep1 = best['ep1']
    fig = plt.figure(figsize=(8,6)); ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(xyz[:,0], xyz[:,1], xyz[:,2], c=w, cmap='viridis', s=40)
    ax.plot([ep0[0], ep1[0]], [ep0[1], ep1[1]], [ep0[2], ep1[2]], color='red', lw=2.5, label='Tomo PCA')
    ax.scatter([center[0]], [center[1]], [center[2]], color='lime', s=80, label='cluster center')
    if linear_res is not None:
        try:
            le0 = linear_res['ep0_mm']; le1 = linear_res['ep1_mm']
            ax.plot([le0[0], le1[0]], [le0[1], le1[1]], [le0[2], le1[2]], color='magenta', lw=2.0, linestyle='--', label='Linear recon')
        except Exception:
            pass
    ax.set_title("Best cluster voxel centers and PCA line")
    ax.set_xlabel("X [mm]"); ax.set_ylabel("Y [mm]"); ax.set_zlabel("Z [mm]")
    ax.legend()
    save_png(fig, os.path.join(outdir, "best_cluster_3d.png"))

# ---------------------------
# Main
# ---------------------------
def main():
    outdir = os.path.abspath("./tomo_output")
    os.makedirs(outdir, exist_ok=True)

    # import project modules
    try:
        import importlib
        testing = importlib.import_module("testing")
        linmod = importlib.import_module("reconstruct_geometryA_uvwt")
        print("[main] imported testing and reconstruct_geometryA_uvwt OK")
    except Exception as e:
        print("[main] ERROR importing modules:", e)
        return

    raw = testing.getTestData("middle")
    print("[main] got raw test data")

    # adaptive tomography
    res, info = adaptive_tomography(raw)
    if res is None:
        print("[main] tomography failed to find cluster. Exiting.")
        return
    print("[main] tomography success:", info)

    # visualizations
    plot_density_slices(res['density'], res['grid'], outdir)
    plot_top_voxel_scatter(res, outdir, top_n=800)
    best = res.get('best_cluster')
    linres = None
    try:
        linres = linmod.reconstruct_from_histograms_notebook(raw, n_samples=600)
    except Exception:
        pass
    if best is not None:
        plot_best_cluster_3d(best, outdir, linear_res=linres)

    # compare best endpoints to GT (raw error)
    if best is not None:
        ep0_t = best['ep0']; ep1_t = best['ep1']
        gt_comp = compare_to_gt_if_present(raw, ep0_t, ep1_t, verbose=True)
    else:
        gt_comp = None
        print("[main] no best cluster to compare to GT")

    # simple metric: distance between tomo endpoints and linear endpoints (if linear exists)
    ep_lin_dist = None
    if linres is not None and best is not None:
        try:
            ep0_lin = linres['ep0_mm']; ep1_lin = linres['ep1_mm']
            d0 = float(np.linalg.norm(np.asarray(ep0_t) - np.asarray(ep0_lin)))
            d1 = float(np.linalg.norm(np.asarray(ep1_t) - np.asarray(ep1_lin)))
            ep_lin_dist = {"ep0_to_linear_ep0": d0, "ep1_to_linear_ep1": d1}
            print("[main] tomo <-> linear endpoint distances:", ep_lin_dist)
        except Exception:
            ep_lin_dist = None

    # summary
    summary = {
        "adaptive_info": info,
        "voxels_grid": {"nx": res['grid']['x_centers'].size, "ny": res['grid']['y_centers'].size, "nz": res['grid']['z_centers'].size},
        "mask_count_estimate": int(res['nonzero_voxels']),
        "max_density": float(res['max_density']),
        "best_cluster_present": bool(best is not None),
        "gt_comparison": gt_comp,
        "tomo_vs_linear_endpoint_distance": ep_lin_dist
    }
    with open(os.path.join(outdir, "tomo_summary_with_gt.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("[main] outputs written to", outdir)
    print("  - tomo_summary_with_gt.json")
    print("  - density_xy_midz.png, density_xz_proj.png, density_yz_proj.png")
    print("  - top_voxels_scatter.png")
    if best is not None:
        print("  - best_cluster_3d.png")

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

if __name__ == "__main__":
    main()
