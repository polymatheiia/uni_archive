# Lab 9/10 — Time Series Forecast

Deliverable report: **`report.html`** (self-contained, 14 plots + MAE table).

| Step | Script | Output |
|------|--------|--------|
| 1–2. Yearly averages + 8 country scatter plots (with seasonal zoom) | `lab9.py [0/1]` | `yearly_averages.csv`, `bra.png` … `ukr.png` |
| 3. 250-year forecasts, 2 countries × 3 methods (AR, ARMA, HWES) + 95% CI | `forecast.py [0/1]` | `pol_ar.png`, `pol_arma.png`, `pol_hwes.png`, `ukr_*` |
| 4. TimeSeriesSplit (n=5) MAE cross-validation | `crossval.py` | `crossval_mae.csv` |
| Report | `make_report.py` | `report.html` |

Supplementary (extra methods, not required): `ar_and_ma.py`, `sarima_model.py`,
`ses_model.py`, `var_model.py`.

## Findings

- **Trend & seasonality:** every country shows a gentle long-term warming trend;
  the 5-year zoom panels expose a strong annual seasonal cycle in the monthly data.
- **Forecasts:** AR/ARMA revert to the mean with bounded intervals; Holt-Winters
  extrapolates the additive trend, so its central line keeps climbing and the band
  widens with the horizon.
- **Cross-validation MAE** (lower = better):

  | country | ar | arma | hwes |
  |---------|----|------|------|
  | Poland | 0.769 | 0.795 | 0.864 |
  | Ukraine | 0.731 | 0.773 | 0.893 |

  The simpler AR model generalises best on held-out folds; HWES pays for its
  aggressive trend extrapolation.

```bash
# with the project venv active, from lab9/
python lab9.py 1 && python forecast.py 1 && python crossval.py && python make_report.py
```
