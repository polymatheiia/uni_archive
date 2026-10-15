"""Assemble one self-contained report.html with all lab7 interactive plots.

Three libraries (mpld3, Bokeh, Plotly), each on two datasets (tech stocks +
sklearn wine), plus a bonus mpld3 random-walk plot. Every JavaScript dependency
(Plotly, Bokeh, d3, mpld3) is inlined, so report.html has NO external
dependencies and works offline. Run: python make_report.py
"""

import os
import html

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine

import mpld3
import mpld3.urls
from mpld3 import plugins

import plotly.graph_objects as go
import plotly.offline as po

from bokeh.plotting import figure as bfigure
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10_5, Category10_3
from bokeh.embed import components
from bokeh.resources import INLINE

STOCK_CSV = "stock_data.csv"
STOCK_COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
WINE_IDX = [0, 1, 5, 6]  # alcohol, malic_acid, flavanoids, nonflavanoid_phenols


# ----------------------------------------------------------------------------- mpld3
def mpld3_stocks_fig():
    df = pd.read_csv(STOCK_CSV, index_col="Date", parse_dates=True)
    fig, ax = plt.subplots(figsize=(11, 5.5))
    lines, labels = [], []
    for col, color in zip(df.columns, STOCK_COLORS):
        line, = ax.plot(df.index, df[col], label=col, color=color, lw=2, alpha=0.85)
        lines.append(line); labels.append(col)
    ax.set_xlabel("Date"); ax.set_ylabel("Stock price ($)")
    ax.set_title("Tech stocks (2023) - click legend to toggle")
    ax.grid(True, alpha=0.3); fig.autofmt_xdate()
    plugins.connect(fig, plugins.InteractiveLegendPlugin(lines, labels, alpha_unsel=0.1))
    return fig


def mpld3_wine_fig():
    wine = load_wine()
    X = wine.data + 0.1 * np.random.random(wine.data.shape)
    y = wine.target
    names = [wine.feature_names[i] for i in WINE_IDX]
    fig, ax = plt.subplots(4, 4, sharex="col", sharey="row", figsize=(8, 8))
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    for i in range(4):
        for j in range(4):
            ax[3 - i, j].scatter(X[:, WINE_IDX[j]], X[:, WINE_IDX[i]], c=y, s=25, alpha=0.6)
    for a in ax.flat:
        a.xaxis.set_major_formatter(plt.NullFormatter())
        a.yaxis.set_major_formatter(plt.NullFormatter())
    for i in range(4):
        ax[3 - i, i].text(0.5, 0.5, names[i], transform=ax[3 - i, i].transAxes,
                          ha="center", va="center", fontsize=9)
    fig.suptitle("Wine scatter matrix - drag to brush (linked)", fontsize=12)
    plugins.connect(fig, plugins.LinkedBrush(ax[0, 0].collections[0]))
    return fig


def mpld3_randomwalk_fig():
    from mpld3_data_randomwalk import build_figure
    return build_figure()


def mpld3_div(fig, figid):
    spec = mpld3.fig_to_dict(fig)
    plt.close(fig)
    import json
    return (f'<div id="{figid}"></div>\n'
            f'<script>mpld3.draw_figure("{figid}", {json.dumps(spec)});</script>')


# ----------------------------------------------------------------------------- plotly
def plotly_stocks_html(div_id):
    df = pd.read_csv(STOCK_CSV, index_col="Date", parse_dates=True)
    fig = go.Figure()
    for col, color in zip(df.columns, STOCK_COLORS):
        fig.add_trace(go.Scatter(
            x=df.index, y=df[col], mode="lines", name=col,
            line=dict(color=color, width=2),
            hovertemplate="<b>%{fullData.name}</b><br>%{x|%Y-%m-%d}<br>$%{y:.2f}<extra></extra>"))
    fig.update_layout(title="Tech stocks (2023) - hover unified, click legend to toggle",
                      xaxis_title="Date", yaxis_title="Stock price ($)",
                      hovermode="x unified", template="plotly_white", height=480,
                      legend=dict(itemclick="toggle", itemdoubleclick="toggleothers"))
    return fig.to_html(full_html=False, include_plotlyjs=False, div_id=div_id)


def plotly_wine_html(div_id):
    wine = load_wine()
    X = wine.data + 0.1 * np.random.random(wine.data.shape)
    y = wine.target
    names = [wine.feature_names[i] for i in WINE_IDX]
    colors = ["#e41a1c", "#377eb8", "#4daf4a"]
    fig = go.Figure()
    for cls, cname in enumerate(wine.target_names):
        m = y == cls
        fig.add_trace(go.Scatter(
            x=X[m, WINE_IDX[0]], y=X[m, WINE_IDX[2]], mode="markers", name=str(cname),
            marker=dict(color=colors[cls], size=7, opacity=0.7),
            hovertemplate=f"{names[0]}: %{{x:.2f}}<br>{names[2]}: %{{y:.2f}}<extra>{cname}</extra>"))
    fig.update_layout(title="Wine: alcohol vs flavanoids by class",
                      xaxis_title=names[0], yaxis_title=names[2],
                      template="plotly_white", height=480)
    return fig.to_html(full_html=False, include_plotlyjs=False, div_id=div_id)


# ----------------------------------------------------------------------------- bokeh
def bokeh_stocks_model():
    df = pd.read_csv(STOCK_CSV, index_col="Date", parse_dates=True)
    p = bfigure(title="Tech stocks (2023) - click legend to hide",
                x_axis_type="datetime", x_axis_label="Date",
                y_axis_label="Stock price ($)", height=430, sizing_mode="stretch_width")
    for col, color in zip(df.columns, Category10_5):
        p.line(df.index, df[col], legend_label=col, color=color, line_width=2, name=col)
    p.add_tools(HoverTool(tooltips=[("Stock", "$name"), ("Price", "$@y{0.00}")], mode="vline"))
    p.legend.location = "top_left"; p.legend.click_policy = "hide"
    return p


def bokeh_wine_model():
    wine = load_wine()
    X = wine.data + 0.1 * np.random.random(wine.data.shape)
    y = wine.target
    names = [wine.feature_names[i] for i in WINE_IDX]
    src = ColumnDataSource(dict(
        alcohol=X[:, WINE_IDX[0]], malic=X[:, WINE_IDX[1]],
        flav=X[:, WINE_IDX[2]], nonflav=X[:, WINE_IDX[3]],
        color=[Category10_3[t] for t in y],
        cls=[wine.target_names[t] for t in y]))
    keys = ["alcohol", "malic", "flav", "nonflav"]
    grid = []
    for i in range(4):
        row = []
        for j in range(4):
            p = bfigure(width=190, height=190, tools="pan,box_select,lasso_select,reset,wheel_zoom",
                        toolbar_location=None)
            if i == j:
                p.text(x=[0], y=[0], text=[names[i]], text_align="center", text_font_size="9pt")
                p.axis.visible = False; p.grid.visible = False
            else:
                p.scatter(x=keys[j], y=keys[i], source=src, size=6, color="color", alpha=0.6,
                          nonselection_fill_alpha=0.15)
                p.add_tools(HoverTool(tooltips=[("class", "@cls")]))
            p.xaxis.major_label_text_font_size = "0pt"
            p.yaxis.major_label_text_font_size = "0pt"
            row.append(p)
        grid.append(row)
    return gridplot(grid[::-1], toolbar_location="right")


# ----------------------------------------------------------------------------- assemble
def main():
    # mpld3 JS (bundled with the package -> fully offline)
    with open(mpld3.urls.D3_LOCAL) as f:
        d3_js = f.read()
    with open(mpld3.urls.MPLD3_LOCAL) as f:
        mpld3_js = f.read()

    plotly_js = po.get_plotlyjs()
    bokeh_res = INLINE.render()

    mp_stocks = mpld3_div(mpld3_stocks_fig(), "mpld3-stocks")
    mp_wine = mpld3_div(mpld3_wine_fig(), "mpld3-wine")
    mp_walk = mpld3_div(mpld3_randomwalk_fig(), "mpld3-walk")

    pl_stocks = plotly_stocks_html("plotly-stocks")
    pl_wine = plotly_wine_html("plotly-wine")

    bk_script, bk_divs = components({"bokeh-stocks": bokeh_stocks_model(),
                                     "bokeh-wine": bokeh_wine_model()})

    def section(title, desc, body):
        return (f'<section><h2>{html.escape(title)}</h2>'
                f'<p class="desc">{desc}</p>{body}</section>')

    parts = [
        section("Plotly - tech stocks", "Time series with unified hover and toggleable legend.", pl_stocks),
        section("Plotly - wine", "Scatter of two chemical features coloured by wine class; hover for details.", pl_wine),
        section("Bokeh - tech stocks", "Same stocks; click a legend entry to hide a line, hover shows price.", bk_divs["bokeh-stocks"]),
        section("Bokeh - wine", "4x4 scatter matrix with linked box/lasso selection across panels.", bk_divs["bokeh-wine"]),
        section("mpld3 - tech stocks", "Matplotlib figure made interactive; click legend to toggle series.", mp_stocks),
        section("mpld3 - wine", "Scatter matrix with linked brushing (drag to select in one panel).", mp_wine),
        section("mpld3 - random walks (bonus)", "Interactive legend plus shaded confidence bands.", mp_walk),
    ]

    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Lab 7 - Interactive plots report</title>
<style>
 body {{ font-family: system-ui, sans-serif; max-width: 1100px; margin: 0 auto; padding: 1.5rem; color:#1a1a1a; }}
 h1 {{ border-bottom: 3px solid #333; padding-bottom: .3rem; }}
 section {{ margin: 2.5rem 0; padding-top: .5rem; border-top: 1px solid #ddd; }}
 h2 {{ color:#2c3e50; }} .desc {{ color:#555; margin-top:-.3rem; }}
</style>
<script type="text/javascript">{d3_js}</script>
<script type="text/javascript">{mpld3_js}</script>
<script type="text/javascript">{plotly_js}</script>
{bokeh_res}
</head><body>
<h1>Lab 7 - Interactive plots</h1>
<p>Six required interactive plots (three libraries x two datasets) plus one bonus,
all embedded in this single self-contained file - no internet connection needed.
Datasets: synthetic tech-stock prices (<code>stock_data.csv</code>) and the
scikit-learn wine dataset.</p>
{''.join(parts)}
{bk_script}
</body></html>"""

    with open("report.html", "w") as f:
        f.write(doc)
    print(os.path.abspath("report.html"), f"({len(doc)//1024} KB)")


if __name__ == "__main__":
    main()
