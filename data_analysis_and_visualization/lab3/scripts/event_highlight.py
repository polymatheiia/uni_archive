"""lab3 III: animated bar plot that highlights a demographic event.

Rwanda and four neighbours (Burundi, Uganda, Tanzania, DR Congo). The 1994
Rwandan genocide caused a sharp, visible drop in Rwanda's population. When the
animation reaches 1994 it freezes for ~4 seconds and shows an explanatory label,
then continues.

Produces event_rwanda.gif. Usage: python event_highlight.py
"""

import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import FuncFormatter

DATA = os.path.join(os.path.dirname(__file__), "..", "..", "lab2", "data", "population_clean.csv")
CODES = ["RWA", "BDI", "UGA", "TZA", "COD"]
COLORS = ["#d62728", "#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd"]
EVENT_YEARS = (1992, 1995)   # label shown while inside this range
FREEZE_AT = 1994             # freeze the animation on this year
FREEZE_FRAMES = 48           # ~4 s at 12 fps
FPS = 12


def human(n):
    for div, suf in [(1e9, "B"), (1e6, "M"), (1e3, "k")]:
        if abs(n) >= div:
            return f"{n / div:.1f}{suf}"
    return f"{n:.0f}"


def main():
    pop = pd.read_csv(DATA)
    sub = pop[pop["Country Code"].isin(CODES)]
    wide = sub.pivot_table(index="Year", columns="Country Code", values="Population")[CODES].dropna()
    years = list(wide.index)
    ymax = np.nanmax(wide.values) * 1.15

    # build the frame sequence, repeating 1994 to create the freeze
    seq = []
    for y in years:
        seq.append(y)
        if y == FREEZE_AT:
            seq.extend([FREEZE_AT] * FREEZE_FRAMES)

    x = np.arange(len(CODES))
    fig, ax = plt.subplots(figsize=(8, 5))

    def draw(year):
        ax.clear()
        vals = wide.loc[year].values
        ax.bar(x, vals, color=COLORS)
        for xi, (code, v) in enumerate(zip(CODES, vals)):
            ax.text(xi, v + ymax * 0.01, code, ha="center", va="bottom",
                    fontsize=14, fontweight="bold")
        ax.set_ylim(0, ymax)
        ax.set_xticks(x); ax.set_xticklabels(CODES, fontsize=12)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: human(v)))
        ax.set_ylabel("Population", fontsize=13)
        ax.set_title("Rwanda and neighbours - the 1994 genocide", fontsize=14, fontweight="bold")
        ax.text(0.97, 0.92, str(int(year)), transform=ax.transAxes,
                ha="right", va="top", fontsize=32, fontweight="bold", color="0.3")
        if EVENT_YEARS[0] <= year <= EVENT_YEARS[1]:
            ax.text(0.5, 0.55, "RWANDAN GENOCIDE\n1994",
                    transform=ax.transAxes, ha="center", va="center",
                    fontsize=22, fontweight="bold", color="darkred",
                    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.85))
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()

    anim = FuncAnimation(fig, draw, frames=seq, interval=1000 / FPS)
    out = os.path.join(os.path.dirname(__file__), "..", "images", "event_rwanda.gif")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    anim.save(out, writer=PillowWriter(fps=FPS))
    plt.close(fig)
    print(os.path.abspath(out))


if __name__ == "__main__":
    main()
