# Lab 7/8 — Interactive plots

Three libraries × two datasets = six interactive plots (plus one bonus mpld3 plot),
each as its own script taking `[0/1]` (`0` = show, `1` = save HTML + print path).

| Library | Stocks | Wine |
|---------|--------|------|
| mpld3   | `mpld3_data_stocks.py` | `mpld3_data_wine.py` |
| Bokeh   | `bokeh_data_stocks.py` | `bokeh_data_wine.py` |
| Plotly  | `plotly_data_stocks.py` | `plotly_data_wine.py` |

Bonus: `mpld3_data_randomwalk.py` (interactive legend + confidence bands).

Datasets: `stock_data.csv` (synthetic tech-stock prices) and the scikit-learn wine
dataset (loaded in-script).

## Combined report

`make_report.py` builds **`report.html`** — a single, fully self-contained file with
**all** interactive plots and **every** JS dependency (Plotly, Bokeh, d3, mpld3)
inlined, so it renders offline with no external requests.

```bash
# with the project venv active, from lab7/
python make_report.py            # -> report.html
python plotly_data_stocks.py 1   # or run any single plot
```
