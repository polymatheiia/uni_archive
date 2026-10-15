"""Build a self-contained report.html for the lab9/10 time-series project.

Embeds (as base64) the 8 per-country scatter plots and the 6 forecast plots, and
renders the TimeSeriesSplit MAE table, with no external dependencies.
Run: python make_report.py   (after lab9.py 1, forecast.py 1, crossval.py)
"""

import base64
import os

import pandas as pd

SCATTERS = [("bra", "Brazil"), ("fra", "France"), ("jap", "Japan"),
            ("nzl", "New Zealand"), ("pol", "Poland"), ("zaf", "South Africa"),
            ("swe", "Sweden"), ("ukr", "Ukraine")]
FORECASTS = [("pol_ar", "Poland - AR"), ("pol_arma", "Poland - ARMA"),
             ("pol_hwes", "Poland - HWES"), ("ukr_ar", "Ukraine - AR"),
             ("ukr_arma", "Ukraine - ARMA"), ("ukr_hwes", "Ukraine - HWES")]


def img(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/png;base64,{b64}" style="max-width:100%;height:auto;">'


def grid(items, cols=2):
    cells = "".join(
        f'<figure><figcaption>{cap}</figcaption>{img(code + ".png")}</figure>'
        for code, cap in items if os.path.exists(code + ".png"))
    return f'<div class="grid grid{cols}">{cells}</div>'


def mae_table():
    t = pd.read_csv("crossval_mae.csv", index_col=0)
    head = "".join(f"<th>{c}</th>" for c in t.columns)
    rows = ""
    for country, row in t.iterrows():
        rows += "<tr><th>" + country + "</th>" + \
            "".join(f"<td>{v:.3f}</td>" for v in row) + "</tr>"
    return (f'<table class="mae"><thead><tr><th>country</th>{head}</tr></thead>'
            f'<tbody>{rows}</tbody></table>')


def main():
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Lab 9/10 - Time series forecast</title>
<style>
 body {{ font-family: system-ui, sans-serif; max-width: 1150px; margin: 0 auto; padding: 1.5rem; color:#1a1a1a; }}
 h1 {{ border-bottom: 3px solid #333; padding-bottom:.3rem; }}
 h2 {{ color:#2c3e50; margin-top:2rem; }}
 .grid {{ display:grid; gap:1rem; }} .grid2 {{ grid-template-columns:1fr 1fr; }}
 figure {{ margin:0; border:1px solid #ddd; border-radius:6px; padding:.4rem; }}
 figcaption {{ font-weight:600; margin-bottom:.3rem; }}
 table.mae {{ border-collapse:collapse; margin:1rem 0; }}
 table.mae th, table.mae td {{ border:1px solid #bbb; padding:.4rem .9rem; text-align:center; }}
 table.mae thead th {{ background:#f0f0f0; }}
</style></head><body>
<h1>Time Series Forecast — global temperatures</h1>
<p>Yearly-average temperatures for eight countries (1750s–2013). We inspect trend
and seasonality, forecast 250 years ahead for Poland and Ukraine with three methods
(AR, ARMA, Holt-Winters), each with a 95% confidence band, and cross-validate the
methods with <code>TimeSeriesSplit</code>.</p>

<h2>1–2. Trend &amp; seasonality — one scatter per country</h2>
<p>Each panel shows the monthly observations (light) with the yearly average (red)
and a fitted linear trend; the lower sub-panel zooms to the last five years, where
the seasonal cycle is clearly visible. A gentle long-term warming trend is present
in every country.</p>
{grid(SCATTERS)}

<h2>3. Forecasts to 2263 (95% confidence intervals)</h2>
<p>AR and ARMA revert to the series mean with a bounded, quickly-saturating interval,
whereas Holt-Winters extrapolates the additive trend, so its central line keeps
rising and its band widens with the horizon.</p>
{grid(FORECASTS)}

<h2>4. Cross-validation — mean absolute error</h2>
<p>MAE of each method averaged over 5 <code>TimeSeriesSplit</code> folds (lower is
better). On this data the simpler AR model generalises best; ARMA is close, and
Holt-Winters pays for its aggressive trend extrapolation on the held-out folds.</p>
{mae_table()}
</body></html>"""
    with open("report.html", "w") as f:
        f.write(doc)
    print(os.path.abspath("report.html"))


if __name__ == "__main__":
    main()
