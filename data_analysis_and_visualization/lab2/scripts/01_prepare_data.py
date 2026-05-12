import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("../data")
POP_CSV = DATA_DIR / "API_SP.POP.TOTL_DS2_en_csv_v2.csv"
AREA_CSV = DATA_DIR / "API_AG.LND.TOTL.K2_DS2_en_csv_v2.csv"

YEAR_START = 1960
YEAR_END = 2024

NON_COUNTRY_KEYWORDS = [
    "income", "world", "europe", "asia", "africa", "america", "caribbean",
    "arab", "union", "oecd", "ida", "ibrd", "least developed", "fragile",
    "small states", "euro area", "middle east", "north america", "south asia",
    "sub-saharan", "latin america", "pacific", "dividend"
]

NON_COUNTRY_NAMES = {
    "World", "High income", "Low income", "Middle income", "Euro area",
    "European Union", "OECD members", "Arab World", "Sub-Saharan Africa",
    "South Asia", "North America", "East Asia & Pacific",
    "Latin America & Caribbean", "IBRD only", "IDA only", "IDA total"
}


def is_country_like(name: str) -> bool:
    if pd.isna(name):
        return False
    name = str(name).strip()
    if name in NON_COUNTRY_NAMES:
        return False
    low = name.lower()
    return not any(word in low for word in NON_COUNTRY_KEYWORDS)


def load_indicator(csv_path):
    df = pd.read_csv(csv_path, skiprows=4)
    years = [str(y) for y in range(YEAR_START, YEAR_END + 1)]
    df = df[["Country Name", "Country Code"] + years]
    df = df[df["Country Name"].apply(is_country_like)].copy()

    long_df = df.melt(
        id_vars=["Country Name", "Country Code"],
        value_vars=years,
        var_name="Year",
        value_name="Value"
    )
    long_df["Year"] = long_df["Year"].astype(int)
    long_df["Value"] = pd.to_numeric(long_df["Value"], errors="coerce")
    long_df = long_df.dropna(subset=["Value"])
    return long_df


pop = load_indicator(POP_CSV).rename(columns={"Value": "Population"})
area = load_indicator(AREA_CSV).rename(columns={"Value": "Area_km2"})

density = pop.merge(area, on=["Country Name", "Country Code", "Year"], how="inner")
density["Density"] = density["Population"] / density["Area_km2"]

DATA_DIR.mkdir(exist_ok=True)

pop.to_csv(DATA_DIR / "population_clean.csv", index=False)
area.to_csv(DATA_DIR / "area_clean.csv", index=False)
density.to_csv(DATA_DIR / "density_clean.csv", index=False)

print("Saved:")
print(DATA_DIR / "population_clean.csv")
print(DATA_DIR / "area_clean.csv")
print(DATA_DIR / "density_clean.csv")
