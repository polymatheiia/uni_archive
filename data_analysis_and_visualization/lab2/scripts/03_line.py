"""Animated line plots of population over time for groups a, b, c.

Each series starts as a dot and grows into a line as the years advance. The
three-letter country code rides at the leading end of each line, and a large year
counter sits inside the plot. Produces line_a.gif, line_b.gif, line_c.gif.

Usage: python 03_line.py
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


def make_line_gif(codes, title, filename):
    pop = ac.load_population()
    frame = ac.group_frame(pop, codes).dropna(how="any")
    years = list(frame.index)
    ymax = np.nanmax(frame.values) * 1.1

    fig, ax = plt.subplots(figsize=(8, 5))

    def draw(i):
        ax.clear()
        upto = years[: i + 1]
        cur = years[i]
        for k, code in enumerate(codes):
            color = ac.GROUP_COLORS[k]
            ys = frame.loc[upto, code].values
            ax.plot(upto, ys, color=color, linewidth=2)
            ax.scatter([cur], [ys[-1]], color=color, s=40, zorder=3)
            ax.text(cur, ys[-1], " " + code, color=color, fontsize=12,
                    fontweight="bold", va="center")
        ax.set_xlim(years[0], years[-1])
        ax.set_ylim(0, ymax)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: ac.human(v)))
        ax.set_xlabel("Year", fontsize=13)
        ax.set_ylabel("Population", fontsize=13)
        ax.set_title(title, fontsize=15, fontweight="bold")
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
    make_line_gif(a, "Five most populated countries - population over time", "line_a.gif")
    make_line_gif(b, f"Random group (around {nm[pivot]}, {byear})", "line_b.gif")
    make_line_gif(c, "Poland and its population neighbours", "line_c.gif")


if __name__ == "__main__":
    main()
