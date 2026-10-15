"""Shared data loading for the lab12/lab13 ML scripts.

Loads the feature CSVs produced in lab11. The feature matrix deliberately EXCLUDES
uid, data_type and pI: the label is defined as (pI < 5), so keeping pI would leak
the target. Only sequence-derived features are used.
"""

import os

import pandas as pd

LAB11_DATA = os.path.join(os.path.dirname(__file__), "..", "..", "lab11", "data")
DROP = ["uid", "data_type", "pI", "label"]


def feature_columns(df):
    return [c for c in df.columns if c not in DROP]


def load_split(name):
    df = pd.read_csv(os.path.join(LAB11_DATA, f"IPC_features_{name}.csv"))
    X = df[feature_columns(df)]
    y = df["label"]
    return X, y, df


def load_all():
    return pd.read_csv(os.path.join(LAB11_DATA, "IPC_features.csv"))
