"""Animated bar plots of population for the three country groups (a, b, c).

Produces 6 GIFs: colour and black-and-white versions of each group.
  bar_a_color.gif / bar_a_bw.gif   (5 most populated)
  bar_b_color.gif / bar_b_bw.gif   (random group)
  bar_c_color.gif / bar_c_bw.gif   (Poland as centroid)

Requirements met: three-letter country codes on top of each bar (position tracks
the bar height), a fixed population axis (bars grow, ranking is not re-scaled), a
large year counter, short 150M-style tick labels, and a black-and-white variant
that uses hatches instead of colour.

Usage: python 02_bar.py            (renders all six)
"""

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import FuncFormatter

import anim_common as ac

FPS = 12


def common_years(frame):
    valid = frame.dropna(how="any")
    return list(valid.index)


def make_bar_gif(codes, title, filename, bw=False):
    pop = ac.load_population()
    frame = ac.group_frame(pop, codes)
    years = common_years(frame)
    ymax = np.nanmax(frame.loc[years].values) * 1.15

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(codes))

    def draw(year):
        ax.clear()
        vals = frame.loc[year].values
        if bw:
            bars = ax.bar(x, vals, color="white", edgecolor="black", linewidth=1.3)
            for b, h in zip(bars, ac.GROUP_HATCHES):
                b.set_hatch(h)
        else:
            bars = ax.bar(x, vals, color=ac.GROUP_COLORS[:len(codes)])
        # country code + value on top of each bar
        for xi, (code, v) in enumerate(zip(codes, vals)):
            ax.text(xi, v + ymax * 0.01, code, ha="center", va="bottom",
                    fontsize=15, fontweight="bold")
            ax.text(xi, v * 0.5, ac.human(v), ha="center", va="center",
                    fontsize=11, color="black" if bw else "white", fontweight="bold")
        ax.set_ylim(0, ymax)
        ax.set_xticks(x)
        ax.set_xticklabels(codes, fontsize=12)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: ac.human(v)))
        ax.set_ylabel("Population", fontsize=13)
        ax.set_title(title, fontsize=15, fontweight="bold")
        ax.text(0.97, 0.92, str(int(year)), transform=ax.transAxes,
                ha="right", va="top", fontsize=34, fontweight="bold",
                color="0.3")
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()

    anim = FuncAnimation(fig, draw, frames=years, interval=1000 / FPS)
    out = os.path.join(ac.ensure_img_dir(), filename)
    anim.save(out, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    print(os.path.abspath(out))


def main():
    pop = ac.load_population()
    nm = ac.names(pop)
    a = ac.select_most_populated(pop)
    b, pivot, byear = ac.select_random_group(pop)
    c = ac.select_poland_centroid(pop)

    jobs = [
        (a, "Five most populated countries", "bar_a"),
        (b, f"Random group (around {nm[pivot]}, {byear})", "bar_b"),
        (c, "Poland and its population neighbours", "bar_c"),
    ]
    for codes, title, stem in jobs:
        make_bar_gif(codes, title + " - colour", f"{stem}_color.gif", bw=False)
        make_bar_gif(codes, title + " - b&w", f"{stem}_bw.gif", bw=True)


if __name__ == "__main__":
    main()
