#!/usr/bin/env python3
"""
reconstruction_tests.py
UPDATED: Now computes BOTH raw (pre-alignment) and aligned (post-Transform)
endpoint errors and ensures JSON serializable output.
"""

import os, json, csv, copy, math, time
import numpy as np
from numpy.linalg import norm

import testing
import reconstruct_geometryA_uvwt as reconmod

OUTDIR = os.path.abspath(os.path.dirname(__file__))
SUMMARY_PATH = os.path.join(OUTDIR, "reconstruction_test_summary.json")
CSV_PATH = os.path.join(OUTDIR, "reconstruction_test_runs.csv")

# ===============================================================
# Utilities
# ===============================================================

def make_json_serializable(obj):
    """Recursively convert numpy types to Python built-ins for json.dump."""
    if isinstance(obj, dict):
        return {make_json_serializable(k): make_json_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(make_json_serializable(v) for v in obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        # numpy scalar
        py = obj.item()
        # convert numpy.int64 -> int, numpy.float64 -> float
        return make_json_serializable(py)
    # primitive python types are left as-is
    return obj

# ===============================================================
# Utility for computing both errors (raw and aligned)
# ===============================================================

def compute_errors(raw, detector_result, aligned_result):
    """
    Input:
        detector_result: output of reconstruct_from_histograms_notebook
        aligned_result:  output of reconstruct_aligned

    Returns dict with:
        - raw errors (detector frame)
        - aligned errors (GT frame)
    """
    gt0 = np.array(raw[3], float)
    gt1 = np.array(raw[4], float)

    # Detector frame endpoints
    ep0_raw = np.array(detector_result["ep0_mm"], float)
    ep1_raw = np.array(detector_result["ep1_mm"], float)

    # Aligned endpoints
    ep0_gt = np.array(aligned_result["ep0_gt"], float)
    ep1_gt = np.array(aligned_result["ep1_gt"], float)

    return {
        "err0_raw": float(norm(ep0_raw - gt0)),
        "err1_raw": float(norm(ep1_raw - gt1)),
        "err0_aligned": float(norm(ep0_gt - gt0)),
        "err1_aligned": float(norm(ep1_gt - gt1)),
    }

# ===============================================================
# Canonical run
# ===============================================================

def run_canonical(raw, n_samples=600):
    det = reconmod.reconstruct_from_histograms_notebook(raw, n_samples=n_samples)
    aligned = reconmod.reconstruct_aligned(raw, n_samples=n_samples, verbose=False)
    errs = compute_errors(raw, det, aligned)
    return {"detector": det, "aligned": aligned, **errs}

# ===============================================================
# Test 1: roundtrip algebra sanity
# ===============================================================

def test_forward_inverse_roundtrip(raw):
    gt0 = np.array(raw[3], float)
    gt1 = np.array(raw[4], float)

    errs = {}
    for i, gt in enumerate([gt0, gt1]):
        uvwt = testing.getXYZtoUVWT(gt.reshape(1,3))[0]
        u,v,w,t = [float(x) for x in uvwt]
        x,y,z = reconmod.invert_uvwt_point(u,v,w,t)
        errs[f"gt{i}_roundtrip_err_xyz"] = float(norm(np.array([x,y,z]) - gt))
    return errs

# ===============================================================
# Helper to reconstruct from UVWT arrays → hist
# ===============================================================

def build_histograms_from_uvwt(uvwt):
    Hbins = 512
    Cbins = 256
    uvals = uvwt[:,0]; vvals = uvwt[:,1]; wvals = uvwt[:,2]; tvals = uvwt[:,3]
    HU,_,_ = np.histogram2d(tvals, uvals, bins=(Hbins, Cbins))
    HV,_,_ = np.histogram2d(tvals, vvals, bins=(Hbins, Cbins))
    HW,_,_ = np.histogram2d(tvals, wvals, bins=(Hbins, Cbins))
    return [np.clip(HU,0,None), np.clip(HV,0,None), np.clip(HW,0,None)]

# ===============================================================
# Test 2: noise in XYZ
# ===============================================================

def test_noise_on_xyz(raw, sigma_xyz=1.0, n_trials=10, n_samples=600):
    gt0 = np.array(raw[3],float)
    gt1 = np.array(raw[4],float)

    Npts = 200
    alphas = np.linspace(0,1,Npts)
    base_pts = np.array([gt0 + a*(gt1-gt0) for a in alphas])

    results = []

    for k in range(n_trials):
        noisy_xyz = base_pts + np.random.normal(scale=sigma_xyz, size=base_pts.shape)
        uvwt = testing.getXYZtoUVWT(noisy_xyz)

        HU,HV,HW = build_histograms_from_uvwt(uvwt)
        new_raw = ([HU,HV,HW], raw[1], raw[2], raw[3], raw[4])

        det = reconmod.reconstruct_from_histograms_notebook(new_raw, n_samples=n_samples)
        aligned = reconmod.reconstruct_aligned(new_raw, n_samples=n_samples, verbose=False)
        errs = compute_errors(new_raw, det, aligned)

        results.append(errs)

    return results

# ===============================================================
# Test 3: noise on histogram
# ===============================================================

def test_noise_on_hist(raw, sigma_hist=5.0, n_trials=10, n_samples=600):
    histU, histV, histW = raw[0]
    results = []

    for k in range(n_trials):
        HU = np.clip(histU + np.random.normal(scale=sigma_hist, size=histU.shape), 0, None)
        HV = np.clip(histV + np.random.normal(scale=sigma_hist, size=histV.shape), 0, None)
        HW = np.clip(histW + np.random.normal(scale=sigma_hist, size=histW.shape), 0, None)
        new_raw = ([HU,HV,HW], raw[1], raw[2], raw[3], raw[4])

        det = reconmod.reconstruct_from_histograms_notebook(new_raw, n_samples=n_samples)
        aligned = reconmod.reconstruct_aligned(new_raw, n_samples=n_samples, verbose=False)
        errs = compute_errors(new_raw, det, aligned)

        results.append(errs)

    return results

# ===============================================================
# Test 4: missing strips
# ===============================================================

def test_missing_strips(raw, missing_fraction=0.05, n_trials=10, n_samples=600):
    histU, histV, histW = raw[0]
    W = histU.shape[1]
    results = []

    for k in range(n_trials):
        HU,HV,HW = histU.copy(), histV.copy(), histW.copy()
        missing_cols = np.random.choice(W, size=max(1,int(W*missing_fraction)), replace=False)
        HU[:,missing_cols] = 0
        HV[:,missing_cols] = 0
        HW[:,missing_cols] = 0

        new_raw = ([HU,HV,HW], raw[1], raw[2], raw[3], raw[4])
        det = reconmod.reconstruct_from_histograms_notebook(new_raw, n_samples=n_samples)
        aligned = reconmod.reconstruct_aligned(new_raw, n_samples=n_samples, verbose=False)
        errs = compute_errors(new_raw, det, aligned)

        results.append(errs)

    return results

# ===============================================================
# Test 5: calibration perturbations
# ===============================================================

def test_calibration_perturbations(raw, n_trials=20, n_samples=600,
                                   dx_sigma=2.0, dphi_sigma_deg=0.3, dpitch_sigma=0.01):
    orig_REF_X = reconmod.REF_X
    orig_REF_Y = reconmod.REF_Y
    orig_PHIS = reconmod.PHIS.copy()
    orig_STRIP = reconmod.STRIP_PITCH

    results = []

    for k in range(n_trials):
        # perturb
        reconmod.REF_X = orig_REF_X + np.random.normal(scale=dx_sigma)
        reconmod.REF_Y = orig_REF_Y + np.random.normal(scale=dx_sigma)
        dphi = np.deg2rad(np.random.normal(scale=dphi_sigma_deg))
        reconmod.PHIS = {"U":0.0, "V":orig_PHIS["V"]+dphi, "W":orig_PHIS["W"]+dphi}
        reconmod.STRIP_PITCH = orig_STRIP + np.random.normal(scale=dpitch_sigma)

        det = reconmod.reconstruct_from_histograms_notebook(raw, n_samples=n_samples)
        aligned = reconmod.reconstruct_aligned(raw, n_samples=n_samples, verbose=False)
        errs = compute_errors(raw, det, aligned)
        results.append(errs)

        # restore
        reconmod.REF_X = orig_REF_X
        reconmod.REF_Y = orig_REF_Y
        reconmod.PHIS = orig_PHIS.copy()
        reconmod.STRIP_PITCH = orig_STRIP

    return results

# ===============================================================
# Test 6: bootstrap fits
# ===============================================================

def test_bootstrap_linefit(raw, n_boot=40, n_samples=600):
    histU, histV, histW = raw[0]

    def bootstrap_plane(H):
        H_flat = H.ravel()
        total = float(H_flat.sum()) if H_flat.sum() != 0 else 1.0
        prob = H_flat / total
        # avoid NaNs
        idx = np.random.choice(len(H_flat), size=len(H_flat), replace=True, p=np.maximum(prob, 0))
        resampled = np.zeros_like(H)
        t_idx = np.unravel_index(idx, H.shape)[0]
        c_idx = np.unravel_index(idx, H.shape)[1]
        for tt,cc in zip(t_idx,c_idx):
            resampled[tt,cc] += 1.0
        return resampled

    results = []

    for k in range(n_boot):
        HU = bootstrap_plane(histU)
        HV = bootstrap_plane(histV)
        HW = bootstrap_plane(histW)
        new_raw = ([HU,HV,HW], raw[1], raw[2], raw[3], raw[4])

        det = reconmod.reconstruct_from_histograms_notebook(new_raw, n_samples=n_samples)
        aligned = reconmod.reconstruct_aligned(new_raw, n_samples=n_samples, verbose=False)
        errs = compute_errors(new_raw, det, aligned)
        results.append(errs)

    return results

# ===============================================================
# RUN ALL TESTS
# ===============================================================

def run_all_tests():
    raw = testing.getTestData("middle")

    summary = {"timestamp": time.time(), "tests": {}}
    rows = []

    # 1. algebra sanity
    summary["tests"]["roundtrip"] = test_forward_inverse_roundtrip(raw)
    rows.append(["roundtrip","gt0_roundtrip_err_xyz",summary["tests"]["roundtrip"]["gt0_roundtrip_err_xyz"]])
    rows.append(["roundtrip","gt1_roundtrip_err_xyz",summary["tests"]["roundtrip"]["gt1_roundtrip_err_xyz"]])

    # 2. canonical
    canonical = run_canonical(raw)
    summary["tests"]["canonical"] = canonical
    rows.append(["canonical","err0_raw",canonical["err0_raw"]])
    rows.append(["canonical","err1_raw",canonical["err1_raw"]])
    rows.append(["canonical","err0_aligned",canonical["err0_aligned"]])
    rows.append(["canonical","err1_aligned",canonical["err1_aligned"]])

    # 3. XYZ noise
    print("Running noise_on_xyz...")
    noise_xyz = test_noise_on_xyz(raw)
    summary["tests"]["noise_xyz"] = noise_xyz
    for i,e in enumerate(noise_xyz):
        rows.append(["noise_xyz", i, e["err0_raw"], e["err1_raw"], e["err0_aligned"], e["err1_aligned"]])

    # 4. HIST noise
    print("Running noise_on_hist...")
    noise_hist = test_noise_on_hist(raw)
    summary["tests"]["noise_hist"] = noise_hist
    for i,e in enumerate(noise_hist):
        rows.append(["noise_hist", i, e["err0_raw"], e["err1_raw"], e["err0_aligned"], e["err1_aligned"]])

    # 5. missing strips
    print("Running missing_strips...")
    missing = test_missing_strips(raw)
    summary["tests"]["missing_strips"] = missing
    for i,e in enumerate(missing):
        rows.append(["missing_strips", i, e["err0_raw"], e["err1_raw"], e["err0_aligned"], e["err1_aligned"]])

    # 6. calibration perturbations
    print("Running calibration perturbations...")
    calib = test_calibration_perturbations(raw)
    summary["tests"]["calibration_perturbations"] = calib
    for i,e in enumerate(calib):
        rows.append(["calibration_pert", i, e["err0_raw"], e["err1_raw"], e["err0_aligned"], e["err1_aligned"]])

    # 7. bootstrap
    print("Running bootstrap...")
    bootstrap = test_bootstrap_linefit(raw)
    summary["tests"]["bootstrap"] = bootstrap
    for i,e in enumerate(bootstrap):
        rows.append(["bootstrap", i, e["err0_raw"], e["err1_raw"], e["err0_aligned"], e["err1_aligned"]])

    # Make summary JSON-serializable
    summary_clean = make_json_serializable(summary)

    # Save summary JSON
    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary_clean, f, indent=2)
    print("Wrote summary:", SUMMARY_PATH)

    # Save CSV
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["test","idx","err0_raw","err1_raw","err0_aligned","err1_aligned"])
        for r in rows:
            # ensure each entry is native type
            row_clean = []
            for v in r:
                if isinstance(v, (np.generic, np.ndarray)):
                    v = make_json_serializable(v)
                row_clean.append(v)
            writer.writerow(row_clean)

    print("Wrote CSV:", CSV_PATH)
    return summary_clean

# ===============================================================
# MAIN
# ===============================================================

if __name__ == "__main__":
    print("Running ALL tests with raw + aligned errors...")
    summary = run_all_tests()
    print("Done.")
