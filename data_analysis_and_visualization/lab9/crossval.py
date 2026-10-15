"""Task 4: time-series cross-validation of the three forecasting methods.

Uses sklearn's TimeSeriesSplit (n_splits=5) on each country's yearly-average
series. For every split we fit AR, ARMA and HWES on the training window and
measure the Mean Absolute Error (MAE) of the forecast over the held-out window,
then average the MAE across splits.

Writes crossval_mae.csv and prints the table. Run: python crossval.py
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings

warnings.filterwarnings("ignore")

COUNTRIES = ["Poland", "Ukraine"]
N_SPLITS = 5
AR_LAGS = 10
ARMA_ORDER = (5, 0, 2)


def load_series(country):
    ya = pd.read_csv("yearly_averages.csv")
    s = ya[ya["Country"] == country].sort_values("year")
    return s["YearlyAvgTemp"].to_numpy()


def fit_forecast(method, train, h):
    if method == "ar":
        lags = min(AR_LAGS, len(train) // 2)
        res = AutoReg(train, lags=lags, old_names=False).fit()
        return res.get_prediction(start=len(train), end=len(train) + h - 1).predicted_mean
    if method == "arma":
        res = ARIMA(train, order=ARMA_ORDER).fit()
        return np.asarray(res.get_forecast(steps=h).predicted_mean)
    if method == "hwes":
        res = ExponentialSmoothing(train, trend="add", seasonal=None).fit()
        return np.asarray(res.forecast(h))
    raise ValueError(method)


def cross_val(country):
    y = load_series(country)
    tscv = TimeSeriesSplit(n_splits=N_SPLITS)
    scores = {m: [] for m in ("ar", "arma", "hwes")}
    for train_idx, test_idx in tscv.split(y):
        train, test = y[train_idx], y[test_idx]
        for m in scores:
            try:
                pred = fit_forecast(m, train, len(test))
                scores[m].append(mean_absolute_error(test, pred))
            except Exception:
                scores[m].append(np.nan)
    return {m: np.nanmean(v) for m, v in scores.items()}


def main():
    rows = {c: cross_val(c) for c in COUNTRIES}
    table = pd.DataFrame(rows).T[["ar", "arma", "hwes"]].round(3)
    table.index.name = "country"
    table.to_csv("crossval_mae.csv")
    print("Mean Absolute Error (averaged over 5 TimeSeriesSplit folds)\n")
    print(table.to_string())
    print("\nsaved crossval_mae.csv")


if __name__ == "__main__":
    main()
