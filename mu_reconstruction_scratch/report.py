# Recreate visualizations comparing centroid vs argmax vs parabolic interpolation (retry).
import numpy as np
import matplotlib.pyplot as plt
import os

def parabolic_peak_position(y, idx):
    W = len(y)
    if idx <= 0 or idx >= W-1:
        return float(idx)
    ym1, y0, yp1 = y[idx-1], y[idx], y[idx+1]
    denom = (ym1 - 2*y0 + yp1)
    if abs(denom) < 1e-12:
        return float(idx)
    delta = 0.5 * (ym1 - yp1) / denom
    return float(idx) + delta

def make_gaussian_profile(center, sigma, amplitude, W=256, noise=0.0, missing=None):
    x = np.arange(W)
    y = amplitude * np.exp(-0.5 * ((x - center)/sigma)**2)
    if missing is not None:
        y[missing] = 0.0
    if noise > 0:
        y = y + np.random.normal(scale=noise, size=W)
        y = np.clip(y, 0, None)
    return x, y

def make_bimodal_profile(c1, s1, a1, c2, s2, a2, W=256, noise=0.0):
    x = np.arange(W)
    y = a1 * np.exp(-0.5 * ((x - c1)/s1)**2) + a2 * np.exp(-0.5 * ((x - c2)/s2)**2)
    if noise > 0:
        y = y + np.random.normal(scale=noise, size=W)
        y = np.clip(y, 0, None)
    return x, y

def compute_estimators(x, y):
    idx_max = int(np.argmax(y))
    argmax_val = float(idx_max)
    par_pos = parabolic_peak_position(y, idx_max)
    total = np.sum(y)
    centroid = float(np.sum(x * y) / total) if total > 0 else float('nan')
    return {"argmax": argmax_val, "parabolic": par_pos, "centroid": centroid}

# scenarios
W = 256
scenarios = []
x1, y1 = make_gaussian_profile(center=120.3, sigma=3.2, amplitude=100.0, W=W, noise=0.0)
scenarios.append(("Clean Gaussian", x1, y1))
x2, y2 = make_gaussian_profile(center=110.7, sigma=3.8, amplitude=80.0, W=W, noise=1.5)
scenarios.append(("Noisy Gaussian", x2, y2))
x3a, y3a = make_gaussian_profile(center=130.0, sigma=3.0, amplitude=70.0, W=W, noise=0.0)
x3b, y3b = make_gaussian_profile(center=135.5, sigma=7.0, amplitude=10.0, W=W, noise=0.0)
y3 = y3a + y3b + np.random.normal(scale=0.6, size=W)
y3 = np.clip(y3, 0, None)
scenarios.append(("Skewed / Asymmetric", x3a, y3))
x4, y4 = make_bimodal_profile(c1=80.5, s1=3.0, a1=50.0, c2=92.2, s2=3.0, a2=45.0, W=W, noise=0.8)
scenarios.append(("Bimodal (two peaks)", x4, y4))
x5, y5 = make_gaussian_profile(center=150.3, sigma=4.0, amplitude=90.0, W=W, noise=0.8)
missing_idx = np.arange(148,152)
y5[missing_idx] = 0.0
scenarios.append(("Missing strips (dead channels)", x5, y5))

# Plot and save images
out_dir = './reconstruction_visuals'
os.makedirs(out_dir, exist_ok=True)
saved_files = []

for i, (title, x, y) in enumerate(scenarios, start=1):
    est = compute_estimators(x, y)
    fig, ax = plt.subplots(figsize=(7,3.2), dpi=150)
    ax.plot(x, y, drawstyle='steps-mid', lw=1.2, color='tab:blue', label='strip charges')
    ax.set_title(title)
    ax.set_xlabel('Strip index')
    ax.set_ylabel('Signal amplitude')
    ax.axvline(est["argmax"], color='orange', ls='--', label=f'argmax = {est["argmax"]:.2f}')
    ax.scatter([est["parabolic"]], [np.interp(est["parabolic"], x, y)], color='darkorange', s=40, marker='o', label=f'parabolic = {est["parabolic"]:.3f}')
    ax.axvline(est["centroid"], color='green', ls=':', label=f'centroid = {est["centroid"]:.3f}')
    ax.text(0.02, 0.75, f'centroid={est["centroid"]:.3f}\nparabolic={est["parabolic"]:.3f}\nargmax={est["argmax"]:.3f}', transform=ax.transAxes, fontsize=9, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    ax.legend(loc='upper right', fontsize=8)
    plt.tight_layout()
    fname = os.path.join(out_dir, f'method_compare_{i}.png')
    fig.savefig(fname, dpi=300, bbox_inches='tight')
    saved_files.append(fname)
    plt.close(fig)

# statistical comparison for many noisy Gaussians
rng = np.random.RandomState(42)
N=400
centroid_offsets = []
parabolic_offsets = []
true_centers = []
for _ in range(N):
    c = 120 + rng.normal(scale=15)
    sigma = 2.5 + rng.uniform(0,2)
    amp = 50 + rng.uniform(0,100)
    x, y = make_gaussian_profile(center=c, sigma=sigma, amplitude=amp, W=W, noise=rng.normal(scale=1.2), missing=None)
    est = compute_estimators(x, y)
    centroid_offsets.append(est["centroid"] - c)
    parabolic_offsets.append(est["parabolic"] - c)
    true_centers.append(c)

fig_stat, axs = plt.subplots(1,2, figsize=(10,3.5), dpi=150)
axs[0].hist(centroid_offsets, bins=40, color='green', alpha=0.8)
axs[0].set_title('Centroid bias distribution (est - true center)')
axs[0].set_xlabel('offset (strip units)')
axs[1].hist(parabolic_offsets, bins=40, color='orange', alpha=0.8)
axs[1].set_title('Parabolic interpolation bias distribution (est - true center)')
axs[1].set_xlabel('offset (strip units)')
plt.tight_layout()
stat_fname = os.path.join(out_dir, 'method_compare_stats.png')
fig_stat.savefig(stat_fname, dpi=300, bbox_inches='tight')
saved_files.append(stat_fname)
plt.close(fig_stat)

print("Saved images:")
for f in saved_files:
    print(f)

# Print a small numeric summary for the specific scenarios
for title, x, y in scenarios:
    est = compute_estimators(x, y)
    print(f"{title}: centroid={est['centroid']:.4f}, parabolic={est['parabolic']:.4f}, argmax={est['argmax']:.4f}")

