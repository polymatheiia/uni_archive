"""mpld3 interactive-legend line plot of five random walks with confidence bands.

Each series can be toggled by clicking its legend entry. Synthetic random-walk
data is used purely to demonstrate mpld3's InteractiveLegendPlugin + fill_between.

Usage:
    python mpld3_data_randomwalk.py 0   # show interactively
    python mpld3_data_randomwalk.py 1   # save HTML and print its path
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins


def build_figure():
    rng = np.random.default_rng(9615)
    n = 100
    df = pd.DataFrame(
        (0.1 * (rng.random((n, 5)) - 0.5)).cumsum(0),
        columns=["a", "b", "c", "d", "e"],
    )

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.grid(True, alpha=0.3)
    for key, val in df.items():
        line, = ax.plot(val.index, val.values, label=key, linewidth=2)
        ax.fill_between(
            val.index, val.values - 0.3, val.values + 0.3,
            color=line.get_color(), alpha=0.25,
        )

    handles, labels = ax.get_legend_handles_labels()
    legend = plugins.InteractiveLegendPlugin(
        zip(handles, ax.collections), labels,
        alpha_unsel=0.1, alpha_over=1.5, start_visible=True,
    )
    plugins.connect(fig, legend)

    ax.set_xlabel("step")
    ax.set_ylabel("value")
    ax.set_title("Five random walks with confidence bands (click legend to toggle)",
                 fontsize=13)
    return fig


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["0", "1"]:
        print("Usage: python mpld3_data_randomwalk.py [0|1]")
        sys.exit(1)

    fig = build_figure()
    if sys.argv[1] == "0":
        mpld3.show()
    else:
        out_file = "mpld3_data_randomwalk.html"
        mpld3.save_html(fig, out_file)
        print(os.path.abspath(out_file))


if __name__ == "__main__":
    main()
