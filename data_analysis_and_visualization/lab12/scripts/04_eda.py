"""lab12 Task 1: exploratory data analysis of the engineered features.

Produces (at least two plot types per feature): a grid of histograms split by
class, a grid of box plots by class, and a correlation heatmap. Also prints each
feature's Pearson correlation with the acidic label. Run: python 04_eda.py [0|1]
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common

IMG = os.path.join(os.path.dirname(__file__), "..", "images")


def grid_shape(n):
    cols = 5
    rows = int(np.ceil(n / cols))
    return rows, cols


def hist_grid(df, feats, mode):
    rows, cols = grid_shape(len(feats))
    fig, axes = plt.subplots(rows, cols, figsize=(3 * cols, 2.4 * rows))
    for ax, f in zip(axes.flat, feats):
        for lab, color in [(0, "#4477aa"), (1, "#cc6677")]:
            ax.hist(df[df.label == lab][f], bins=25, alpha=0.6, color=color,
                    label=("acidic" if lab else "non-acidic"))
        ax.set_title(f, fontsize=8)
        ax.tick_params(labelsize=6)
    for ax in axes.flat[len(feats):]:
        ax.axis("off")
    axes.flat[0].legend(fontsize=6)
    fig.suptitle("Feature histograms by class", fontsize=13, fontweight="bold")
    fig.tight_layout()
    _finish(fig, "feature_histograms.png", mode)


def box_grid(df, feats, mode):
    rows, cols = grid_shape(len(feats))
    fig, axes = plt.subplots(rows, cols, figsize=(3 * cols, 2.4 * rows))
    for ax, f in zip(axes.flat, feats):
        ax.boxplot([df[df.label == 0][f], df[df.label == 1][f]],
                   tick_labels=["non", "acid"], showfliers=False)
        ax.set_title(f, fontsize=8)
        ax.tick_params(labelsize=6)
    for ax in axes.flat[len(feats):]:
        ax.axis("off")
    fig.suptitle("Feature box plots by class", fontsize=13, fontweight="bold")
    fig.tight_layout()
    _finish(fig, "feature_boxplots.png", mode)


def corr_heatmap(df, feats, mode):
    corr = df[feats + ["label"]].corr()
    fig, ax = plt.subplots(figsize=(10, 9))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr))); ax.set_xticklabels(corr.columns, rotation=90, fontsize=7)
    ax.set_yticks(range(len(corr))); ax.set_yticklabels(corr.columns, fontsize=7)
    fig.colorbar(im, fraction=0.046, pad=0.04)
    ax.set_title("Feature correlation matrix", fontsize=13, fontweight="bold")
    fig.tight_layout()
    _finish(fig, "correlation_heatmap.png", mode)


def _finish(fig, name, mode):
    if mode == "0":
        plt.show()
    else:
        os.makedirs(IMG, exist_ok=True)
        out = os.path.join(IMG, name)
        fig.savefig(out, dpi=130)
        plt.close(fig)
        print(os.path.abspath(out))


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("0", "1"):
        print("Usage: python 04_eda.py [0|1]")
        sys.exit(1)
    mode = sys.argv[1]
    df = common.load_all()
    feats = common.feature_columns(df)

    print("Pearson correlation of each feature with the acidic label:")
    corr_label = df[feats + ["label"]].corr()["label"].drop("label").sort_values()
    for f, v in corr_label.items():
        print(f"  {f:18s} {v:+.3f}")

    hist_grid(df, feats, mode)
    box_grid(df, feats, mode)
    corr_heatmap(df, feats, mode)


if __name__ == "__main__":
    main()
