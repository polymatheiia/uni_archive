"""Animated bubble plots for groups a, b, c.

x = year, y = population, bubble size = population density (people / km2). Each
frame shows the current-year bubble for every country plus a faded trail of its
past positions; the country code labels the bubble. Produces bubble_a/b/c.gif.

Usage: python 04_bubble.py
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


def density_frame(codes):
    dens = ac.load_density()
    sub = dens[dens["Country Code"].isin(codes)]
    pop_w = sub.pivot_table(index="Year", columns="Country Code", values="Population")[codes]
    den_w = sub.pivot_table(index="Year", columns="Country Code", values="Density")[codes]
    common = pop_w.dropna(how="any").index.intersection(den_w.dropna(how="any").index)
    return pop_w.loc[common], den_w.loc[common], list(common)


def make_bubble_gif(codes, title, filename):
    pop_w, den_w, years = density_frame(codes)
    ymax = np.nanmax(pop_w.values) * 1.15
    dmax = np.nanmax(den_w.values)

    def size(d):
        return 80 + 3000 * (d / dmax)

    fig, ax = plt.subplots(figsize=(8, 5))

    def draw(i):
        ax.clear()
        cur = years[i]
        upto = years[: i + 1]
        for k, code in enumerate(codes):
            color = ac.GROUP_COLORS[k]
            # faded trail
            ax.plot(upto, pop_w.loc[upto, code], color=color, alpha=0.25, lw=1)
            d = den_w.loc[cur, code]
            p = pop_w.loc[cur, code]
            ax.scatter([cur], [p], s=size(d), color=color, alpha=0.6, edgecolor="k", linewidth=0.5)
            ax.text(cur, p, " " + code, color=color, fontsize=11, fontweight="bold", va="center")
        ax.set_xlim(years[0], years[-1])
        ax.set_ylim(0, ymax)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: ac.human(v)))
        ax.set_xlabel("Year", fontsize=13)
        ax.set_ylabel("Population (bubble size = density)", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.text(0.05, 0.92, str(int(cur)), transform=ax.transAxes,
                ha="left", va="top", fontsize=30, fontweight="bold", color="0.3")
        ax.grid(alpha=0.3)
        fig.tight_layout()

    anim = FuncAnimation(fig, draw, frames=len(years), interval=1000 / FPS)
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
    make_bubble_gif(a, "Five most populated - population & density", "bubble_a.gif")
    make_bubble_gif(b, f"Random group (around {nm[pivot]}, {byear})", "bubble_b.gif")
    make_bubble_gif(c, "Poland and its population neighbours", "bubble_c.gif")


if __name__ == "__main__":
    main()
