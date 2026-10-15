"""Task 3: 250-year temperature forecasts for Poland and Ukraine.

For each country we fit three forecasting methods to the yearly-average series and
extrapolate 250 years ahead, drawing a 95% confidence band:

  AR    - Autoregression                     (statsmodels AutoReg)
  ARMA  - Autoregressive Moving Average      (statsmodels ARIMA, d=0)
  HWES  - Holt-Winters Exponential Smoothing (additive trend)

Produces six PNGs: pol_ar.png, pol_arma.png, pol_hwes.png and the ukr_* equivalents.

Usage:
    python forecast.py 0   # show the six plots
    python forecast.py 1   # save the six PNGs and print their paths
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings

warnings.filterwarnings("ignore")

COUNTRIES = {"Poland": "pol", "Ukraine": "ukr"}
HORIZON = 250
AR_LAGS = 10
ARMA_ORDER = (5, 0, 2)


def load_series(country):
    ya = pd.read_csv("yearly_averages.csv")
    s = ya[ya["Country"] == country].sort_values("year")
    return s["year"].to_numpy(), s["YearlyAvgTemp"].to_numpy()


def forecast_ar(y):
    res = AutoReg(y, lags=AR_LAGS, old_names=False).fit()
    pred = res.get_prediction(start=len(y), end=len(y) + HORIZON - 1)
    mean = pred.predicted_mean
    ci = pred.conf_int(alpha=0.05)
    return mean, ci[:, 0], ci[:, 1]


def forecast_arma(y):
    res = ARIMA(y, order=ARMA_ORDER).fit()
    fc = res.get_forecast(steps=HORIZON)
    mean = fc.predicted_mean
    ci = fc.conf_int(alpha=0.05)
    return mean, ci[:, 0], ci[:, 1]


def forecast_hwes(y):
    res = ExponentialSmoothing(y, trend="add", seasonal=None).fit()
    mean = np.asarray(res.forecast(HORIZON))
    # ExponentialSmoothing has no closed-form interval; approximate a growing
    # 95% band from the in-sample residual std, widening with the horizon.
    resid_std = np.std(y - res.fittedvalues, ddof=1)
    step = np.sqrt(np.arange(1, HORIZON + 1))
    half = 1.96 * resid_std * step
    return mean, mean - half, mean + half


METHODS = {"ar": forecast_ar, "arma": forecast_arma, "hwes": forecast_hwes}
METHOD_TITLES = {"ar": "AR (autoregression)",
                 "arma": "ARMA", "hwes": "Holt-Winters exp. smoothing"}


def make_plot(country, code, method, mode):
    years, y = load_series(country)
    mean, lo, hi = METHODS[method](y)
    future_years = np.arange(years[-1] + 1, years[-1] + 1 + HORIZON)

    plt.figure(figsize=(12, 6))
    plt.plot(years, y, color="black", lw=1, label="Observed yearly average")
    plt.plot(future_years, mean, color="tab:red", lw=1.8, label="Forecast")
    plt.fill_between(future_years, lo, hi, color="tab:red", alpha=0.2,
                     label="95% confidence interval")
    plt.axvline(years[-1], color="gray", ls="--", lw=0.8)
    plt.xlabel("Year")
    plt.ylabel("Average temperature (Celsius)")
    plt.title(f"{country}: {METHOD_TITLES[method]} forecast to {future_years[-1]}")
    plt.legend(loc="upper left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if mode == "0":
        plt.show()
    else:
        out = f"{code}_{method}.png"
        plt.savefig(out, dpi=150, bbox_inches="tight")
        plt.close()
        print(os.path.abspath(out))


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("0", "1"):
        print("Usage: python forecast.py [0|1]")
        sys.exit(1)
    mode = sys.argv[1]
    for country, code in COUNTRIES.items():
        for method in METHODS:
            make_plot(country, code, method, mode)


if __name__ == "__main__":
    main()
