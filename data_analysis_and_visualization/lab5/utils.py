"""Shared helpers for the lab5 temperature plotting scripts.

Every task script takes a single positional parameter:
    python taskNx.py 0   -> show the plot interactively (plt.show())
    python taskNx.py 1   -> save the plot to its PNG file and print the path
"""

import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "temperatures_clean.csv"


def parse_mode():
    """Return "0" (show) or "1" (save); exit with usage on anything else."""
    if len(sys.argv) != 2 or sys.argv[1] not in ("0", "1"):
        script = os.path.basename(sys.argv[0])
        print(f"Usage: python {script} [0|1]   (0 = show, 1 = save)")
        sys.exit(1)
    return sys.argv[1]


def load_data(path=DATA_FILE):
    return pd.read_csv(path)


def yearly_country_means(df):
    """Average temperature per (year, country)."""
    return (
        df.groupby(["year", "Country"], as_index=False)["AverageTemperatureCelsius"]
        .mean()
        .sort_values("year")
    )


def yearly_city_means(df, country):
    """Average temperature per (year, city) for one country."""
    sub = df[df["Country"] == country]
    return (
        sub.groupby(["year", "City"], as_index=False)["AverageTemperatureCelsius"]
        .mean()
        .sort_values("year")
    )


def finish(outfile, mode):
    """Show or save the current figure depending on the run mode."""
    if mode == "0":
        plt.show()
    else:
        plt.savefig(outfile, dpi=150, bbox_inches="tight")
        print(os.path.abspath(outfile))
        plt.close()
