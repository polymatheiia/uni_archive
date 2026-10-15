# reconstruct_geometryA_bragg.py
"""
Approach B — Bragg-informed midpoint & endpoint estimation using geometry A.

Usage:
    python reconstruct_geometryA_bragg.py
"""

import numpy as np
from numpy.linalg import lstsq, svd

try:
    import testing
except Exception:
    raise RuntimeError("This script requires testing.py in same folder")

from reconstruct_geometryA_uvwt import (
    PHIS, fit_2d_line_from_hist, strip_bin_to_mm,
    solve_xy_from_s, fit_line_pca
)

def bragg_midpoint_refine(hist_list_or_raw, phis=PHIS, n_samples=600, verbose=True):
    if isinstance(hist_list_or_raw, tuple):
        hist_list = hist_list_or_raw[0]
        raw = hist_list_or_raw
    else:
        hist_list = hist_list_or_raw
        raw = None

    if not isinstance(hist_list, (list, tuple)):
        raise ValueError("hist_list required")

    hU, hV, hW = [np.asarray(h, float) for h in hist_list]
    H, W = hU.shape

    # Fit lines
    a_u, b_u = fit_2d_line_from_hist(hU)
    a_v, b_v = fit_2d_line_from_hist(hV)
    a_w, b_w = fit_2d_line_from_hist(hW)

    t_vals = np.linspace(0, H - 1, n_samples)
    u_bins = a_u * t_vals + b_u
    v_bins = a_v * t_vals + b_v
    w_bins = a_w * t_vals + b_w

    center_bin = W / 2.0
    s_u_mm = strip_bin_to_mm(u_bins, center_bin)
    s_v_mm = strip_bin_to_mm(v_bins, center_bin)
    s_w_mm = strip_bin_to_mm(w_bins, center_bin)

    xs = np.empty_like(s_u_mm); ys = np.empty_like(s_u_mm)
    for i in range(n_samples):
        x_mm, y_mm = solve_xy_from_s([s_u_mm[i], s_v_mm[i], s_w_mm[i]], phis)
        xs[i] = x_mm; ys[i] = y_mm
    zs = (t_vals - T_OFFSET_CONST - TRIGGER_DELAY) * MM_PER_TBIN
    pts = np.vstack([xs, ys, zs]).T

    # density proxy: sample histogram intensities near predicted bins
    densities = np.zeros(n_samples, dtype=float)
    for i in range(n_samples):
        t_idx = int(np.clip(round(t_vals[i]), 0, H-1))
        iu = int(np.clip(round(u_bins[i]), 0, W-1))
        iv = int(np.clip(round(v_bins[i]), 0, W-1))
        iw = int(np.clip(round(w_bins[i]), 0, W-1))
        densities[i] = (hU[t_idx, iu] + hV[t_idx, iv] + hW[t_idx, iw]) / 3.0

    mid_idx = int(np.argmax(densities))
    mid_pt = pts[mid_idx]

    # local PCA to estimate tangent
    win = max(5, int(0.02 * len(t_vals)))
    low = max(0, mid_idx - win); high = min(len(t_vals), mid_idx + win + 1)
    center_local, dir_local = fit_line_pca(pts[low:high])

    # find indices where density >= 10% of peak
    thr = densities[mid_idx] * 0.10
    mask = densities >= thr
    if mask.any():
        idxs = np.where(mask)[0]
        ep0 = pts[idxs.min()]
        ep1 = pts[idxs.max()]
    else:
        # fallback ±L mm
        L = 50.0
        ep0 = center_local - dir_local * L
        ep1 = center_local + dir_local * L

    out = {'mid_pt': mid_pt, 'ep0_mm': ep0, 'ep1_mm': ep1, 'pts': pts, 'center_local': center_local, 'dir_local': dir_local}
    if raw is not None:
        try:
            gt0, gt1 = raw[3], raw[4]
            out['err0'] = np.linalg.norm(ep0 - gt0); out['err1'] = np.linalg.norm(ep1 - gt1)
        except Exception:
            pass

    if verbose:
        print("Approach B (Bragg midpoint) results:")
        print("mid:", mid_pt)
        print("ep0:", ep0)
        print("ep1:", ep1)
        if 'err0' in out:
            print("errs:", out['err0'], out['err1'])

    return out

if __name__ == "__main__":
    raw = testing.getTestData('middle')
    res = bragg_midpoint_refine(raw, phis=PHIS, n_samples=800)
    if 'err0' in res:
        print("Errors:", res['err0'], res['err1'])
