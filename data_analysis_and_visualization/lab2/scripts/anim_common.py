"""Shared helpers for the World Bank population animations (labs 1-3).

Loads the cleaned population/area/density tables, defines the three country
selections used throughout the project (a: most populated, b: a random group,
c: Poland as centroid) and provides small formatting helpers.
"""

import glob
import os

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "images")
REF_YEAR = 2023
RANDOM_SEED = 42

# stable colour per position in the group of five
GROUP_COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
# hatches for the black-and-white versions
GROUP_HATCHES = ["////", "....", "xxxx", "\\\\\\\\", "++++"]


def _load(name):
    return pd.read_csv(os.path.join(DATA_DIR, name))


def load_population():
    return _load("population_clean.csv")


def load_density():
    return _load("density_clean.csv")


def _codes_to_names(pop):
    return dict(pop.drop_duplicates("Country Code")
               .set_index("Country Code")["Country Name"])


def select_most_populated(pop, n=5, year=REF_YEAR):
    """(a) The n most populated countries in `year`."""
    snap = pop[pop["Year"] == year].nlargest(n, "Population")
    return list(snap["Country Code"])


def select_random_group(pop, n=5, seed=RANDOM_SEED):
    """(b) A random country and year, plus the n-1 closest by population."""
    rng = np.random.default_rng(seed)
    years = sorted(pop["Year"].unique())
    year = int(rng.choice(years))
    snap = pop[pop["Year"] == year].dropna(subset=["Population"])
    pivot = snap.sample(1, random_state=seed).iloc[0]
    snap = snap.assign(dist=(snap["Population"] - pivot["Population"]).abs())
    group = snap.nsmallest(n, "dist")
    return list(group["Country Code"]), pivot["Country Code"], year


def select_poland_centroid(pop, n=5, year=REF_YEAR):
    """(c) Poland plus the n-1 countries closest to it by population in `year`."""
    snap = pop[pop["Year"] == year].dropna(subset=["Population"])
    pol = snap[snap["Country Code"] == "POL"]["Population"].iloc[0]
    snap = snap.assign(dist=(snap["Population"] - pol).abs())
    group = snap.nsmallest(n, "dist")
    return list(group["Country Code"])


def group_frame(pop, codes):
    """Wide frame indexed by Year, one column per country code (population)."""
    sub = pop[pop["Country Code"].isin(codes)]
    wide = sub.pivot_table(index="Year", columns="Country Code", values="Population")
    return wide[codes]  # preserve requested order


def human(n):
    """Short population label: 1.4B, 150M, 900k."""
    for div, suf in [(1e9, "B"), (1e6, "M"), (1e3, "k")]:
        if abs(n) >= div:
            return f"{n / div:.1f}{suf}"
    return f"{n:.0f}"


def ensure_img_dir():
    os.makedirs(IMG_DIR, exist_ok=True)
    return IMG_DIR


# Names used for titles/legends
def names(pop):
    return _codes_to_names(pop)
