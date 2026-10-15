"""Animated horizontal bar-chart race (the "other" representation) for a, b, c.

Unlike the fixed vertical bars of 02_bar.py, here the bars are horizontal and are
re-sorted every year, so countries visibly overtake each other in rank. The
country code and short population label sit at the end of each bar, with a large
year counter. Produces other_a.gif, other_b.gif, other_c.gif.

Usage: python 05_other.py
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


def make_race_gif(codes, title, filename):
    pop = ac.load_population()
    frame = ac.group_frame(pop, codes).dropna(how="any")
    years = list(frame.index)
    xmax = np.nanmax(frame.values) * 1.18
    color_of = {code: ac.GROUP_COLORS[k] for k, code in enumerate(codes)}

    fig, ax = plt.subplots(figsize=(8, 5))

    def draw(i):
        ax.clear()
        cur = years[i]
        row = frame.loc[cur].sort_values()  # ascending -> largest on top
        ranked = list(row.index)
        vals = row.values
        ypos = np.arange(len(ranked))
        ax.barh(ypos, vals, color=[color_of[c] for c in ranked])
        for y, code, v in zip(ypos, ranked, vals):
            ax.text(v + xmax * 0.01, y, f"{code}  {ac.human(v)}",
                    va="center", ha="left", fontsize=12, fontweight="bold")
        ax.set_yticks(ypos)
        ax.set_yticklabels(ranked, fontsize=11)
        ax.set_xlim(0, xmax)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: ac.human(v)))
        ax.set_xlabel("Population", fontsize=13)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.text(0.95, 0.10, str(int(cur)), transform=ax.transAxes,
                ha="right", va="bottom", fontsize=34, fontweight="bold", color="0.3")
        ax.grid(axis="x", alpha=0.3)
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
    make_race_gif(a, "Five most populated - ranking race", "other_a.gif")
    make_race_gif(b, f"Random group (around {nm[pivot]}, {byear})", "other_b.gif")
    make_race_gif(c, "Poland and its population neighbours", "other_c.gif")


if __name__ == "__main__":
    main()
