#!/usr/bin/env python3
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import svd, norm
from PIL import Image

# ------------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------------
RECON_MODULE = "reconstruct_geometryA_uvwt"
EVENT = "middle"
OUTDIR = "./reconstruction_visuals"
os.makedirs(OUTDIR, exist_ok=True)

# ------------------------------------------------------------------
# IMPORT PROJECT MODULES
# ------------------------------------------------------------------
if "." not in sys.path:
    sys.path.insert(0, ".")

import importlib
reconmod = importlib.import_module(RECON_MODULE)
testing = importlib.import_module("testing")  # ensures testing is available
reconmod.testing = testing                    # attach if needed

# ------------------------------------------------------------------
# LOAD RAW + RUN RECONSTRUCTION
# ------------------------------------------------------------------
raw = testing.getTestData(EVENT)
recon = reconmod.reconstruct_from_histograms_notebook(raw, n_samples=600)

histU, histV, histW = raw[0]
(a_u, b_u), (a_v, b_v), (a_w, b_w) = recon["fits"]
t_min, t_max = recon.get("t_range", (0, histU.shape[0]-1))
t_vals = np.linspace(t_min, t_max, 600)
W = histU.shape[1]

# ------------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------------
def save_plot(fig, name):
    path = os.path.join(OUTDIR, name)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path

def compute_centroids(hist):
    H, Wloc = hist.shape
    cent = np.full(H, np.nan)
    for t in range(H):
        row = hist[t,:]
        S = row.sum()
        if S > 0:
            cent[t] = float((np.arange(Wloc)*row).sum()/(S + 1e-12))
    return cent

def plot_hist_fit(hist, a, b, centroids, title, fname):
    H, Wloc = hist.shape
    vmin, vmax = np.percentile(hist, 1), np.percentile(hist, 99)
    fig, ax = plt.subplots(figsize=(7,4), dpi=150)
    im = ax.imshow(hist, origin='lower', aspect='auto',
                   interpolation='nearest',
                   extent=[0,Wloc-1,0,H-1],
                   vmin=vmin, vmax=vmax, cmap='viridis')
    fig.colorbar(im, ax=ax, label="Intensity")

    # centroids
    valid = ~np.isnan(centroids)
    if valid.sum() > 0:
        ax.scatter(centroids[valid],
                   np.where(valid)[0],
                   c="white", s=10, edgecolors="black",
                   label="centroids")

    # LS fit
    t_plot = np.linspace(t_min, t_max, 600)
    strip_plot = np.clip(a*t_plot + b, 0, Wloc-1)
    ax.plot(strip_plot, t_plot, color="red", lw=2,
            label="LS fit")

    ax.set_title(title)
    ax.set_xlabel("Strip index")
    ax.set_ylabel("Time bin")
    ax.legend(loc="upper left")
    return save_plot(fig, fname)

def plot_samples(hist, samples, tvals, title, fname):
    H, Wloc = hist.shape
    vmin, vmax = np.percentile(hist, 1), np.percentile(hist, 99)
    fig, ax = plt.subplots(figsize=(7,4), dpi=150)

    im = ax.imshow(hist, origin='lower', aspect='auto',
                   interpolation='nearest',
                   extent=[0,Wloc-1,0,H-1],
                   vmin=vmin, vmax=vmax, cmap='viridis')
    fig.colorbar(im, ax=ax, label="Intensity")

    ax.plot(samples, tvals,
            color="yellow", lw=1.2, alpha=0.95, label="sampled")
    ax.scatter(samples[::max(1,len(samples)//40)],
               tvals[::max(1,len(samples)//40)],
               color="yellow", s=20)

    ax.set_title(title)
    ax.set_xlabel("Strip index")
    ax.set_ylabel("Time bin")
    ax.legend(loc="upper left")
    return save_plot(fig, fname)

def plot_3d_cloud(pts, ep0, ep1, fname, pts_size=40, residuals=True):
    fig = plt.figure(figsize=(9,7), dpi=150)
    ax = fig.add_subplot(111, projection="3d")

    N = pts.shape[0]
    times = np.linspace(0,1,N)

    sc = ax.scatter(pts[:,0], pts[:,1], pts[:,2],
                    c=times, cmap="plasma",
                    s=pts_size, edgecolors="k", linewidths=0.2)

    # PCA line
    ax.plot([ep0[0],ep1[0]],[ep0[1],ep1[1]],[ep0[2],ep1[2]],
            color="red", lw=2.5, label="PCA segment")

    ax.scatter([ep0[0]],[ep0[1]],[ep0[2]],
               color="lime", edgecolors="k", s=100)
    ax.scatter([ep1[0]],[ep1[1]],[ep1[2]],
               color="magenta", edgecolors="k", s=100)

    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.set_zlabel("Z [mm]")

    fig.colorbar(sc, ax=ax, pad=0.08)
    ax.legend(loc="upper left")
    return save_plot(fig, fname)

# ------------------------------------------------------------------
# PRODUCE ALL PLOTS
# ------------------------------------------------------------------
centU = compute_centroids(histU)
centV = compute_centroids(histV)
centW = compute_centroids(histW)

# Histogram fits
plot_hist_fit(histU, a_u, b_u, centU, "U-plane: centroids + LS fit",
              "histU_fit.png")
plot_hist_fit(histV, a_v, b_v, centV, "V-plane: centroids + LS fit",
              "histV_fit.png")
plot_hist_fit(histW, a_w, b_w, centW, "W-plane: centroids + LS fit",
              "histW_fit.png")

# Sampled overlays
u_samples = np.clip(a_u*t_vals + b_u, 0, W-1)
v_samples = np.clip(a_v*t_vals + b_v, 0, W-1)
w_samples = np.clip(a_w*t_vals + b_w, 0, W-1)

plot_samples(histU, u_samples, t_vals, "U-plane: sampled positions",
             "samplesU.png")
plot_samples(histV, v_samples, t_vals, "V-plane: sampled positions",
             "samplesV.png")
plot_samples(histW, w_samples, t_vals, "W-plane: sampled positions",
             "samplesW.png")

# 3D cloud + PCA line
pts = recon["pts"]
ep0 = recon["ep0_mm"]
ep1 = recon["ep1_mm"]

plot_3d_cloud(pts, ep0, ep1, "3dcloud.png")

# Zoom-in
N = pts.shape[0]
mid = N//2
halfw = max(3, N//40)
mask = np.arange(mid-halfw, mid+halfw)

fig = plt.figure(figsize=(6,5), dpi=150)
ax = fig.add_subplot(111, projection="3d")
ax.scatter(pts[mask,0], pts[mask,1], pts[mask,2],
           s=80, c="tab:blue", edgecolors="k")

ax.set_title("Zoom-in: middle segment of 3D cloud")
ax.set_xlabel("X [mm]"); ax.set_ylabel("Y [mm]"); ax.set_zlabel("Z [mm]")
save_plot(fig, "zoom_real.png")

# ------------------------------------------------------------------
# NEW: 50× MAGNIFIED DEVIATIONS
# ------------------------------------------------------------------
center = pts.mean(axis=0)
U, S, Vt = svd((pts-center).T, full_matrices=False)
direction = U[:,0]

proj = (pts-center) @ direction
closest = center + np.outer(proj, direction)

deviations = pts - closest
magnified = closest + deviations * 3000.0

# Plot magnified cloud
fig = plt.figure(figsize=(9,7), dpi=150)
ax = fig.add_subplot(111, projection="3d")

times = np.linspace(0,1,N)
sc = ax.scatter(magnified[:,0], magnified[:,1], magnified[:,2],
                c=times, cmap="viridis",
                s=40, edgecolors="k", linewidths=0.3)

ax.plot([ep0[0],ep1[0]],[ep0[1],ep1[1]],[ep0[2],ep1[2]],
        color="red", lw=2.5, label="PCA segment")

ax.set_title("Magnified Deviations (3000×)", fontsize=14)
ax.set_xlabel("X [mm]"); ax.set_ylabel("Y [mm]"); ax.set_zlabel("Z [mm]")

fig.colorbar(sc, ax=ax, pad=0.08)
save_plot(fig, "magnified_3000x.png")

print("\nAll images saved to", OUTDIR)
