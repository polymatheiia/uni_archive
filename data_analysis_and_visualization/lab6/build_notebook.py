"""Build, execute, and export the lab6 report.

Creates lab6.ipynb (Anscombe's quartet + Datasaurus dozen analysis), executes it
so the tables and plots are embedded, and exports a self-contained report.html.

Run: python build_notebook.py
"""

import nbformat as nbf
from nbclient import NotebookClient
from nbconvert import HTMLExporter

nb = nbf.v4.new_notebook()
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))


def code(text):
    cells.append(nbf.v4.new_code_cell(text))


md(
    "# Lab 6 — The importance of plotting\n\n"
    "Two datasets whose **summary statistics are (almost) identical** but whose "
    "**shapes are completely different**: Anscombe's quartet (`ans.csv`) and the "
    "Datasaurus dozen (`ans2.tsv`). The tables below are computed from the data and "
    "the scatter plots show why the numbers alone are misleading."
)

code(
    "import numpy as np\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "from scipy import stats\n"
    "\n"
    "plt.rcParams['figure.dpi'] = 110\n"
    "pd.set_option('display.float_format', lambda v: f'{v:.3f}')"
)

# ---- Task 1: Anscombe ----
md(
    "## Task 1 — Anscombe's quartet (`ans.csv`)\n\n"
    "Four (x, y) datasets. For each we compute the mean and **sample** variance of x "
    "and y, the correlation, the least-squares line `y = a + b·x`, and its "
    "coefficient of determination R²."
)

code(
    "ans = pd.read_csv('reference/ans.csv', index_col=0)\n"
    "rows = []\n"
    "for i in [1, 2, 3, 4]:\n"
    "    x = ans[f'x{i}'].to_numpy(); y = ans[f'y{i}'].to_numpy()\n"
    "    b, a, r, p, se = stats.linregress(x, y)\n"
    "    rows.append({\n"
    "        'dataset': f'set {i}',\n"
    "        'mean x': x.mean(),\n"
    "        'sample var x': x.var(ddof=1),\n"
    "        'mean y': y.mean(),\n"
    "        'sample var y': y.var(ddof=1),\n"
    "        'corr(x,y)': r,\n"
    "        'reg a (intercept)': a,\n"
    "        'reg b (slope)': b,\n"
    "        'R^2': r**2,\n"
    "    })\n"
    "anscombe_stats = pd.DataFrame(rows).set_index('dataset')\n"
    "anscombe_stats.round(3)"
)

md(
    "The filled table (values rounded to ~2-3 places):\n\n"
    "| Property | Value | Accuracy |\n"
    "| --- | --- | --- |\n"
    "| Mean of x | 9.0 | exact for all four sets |\n"
    "| Sample variance of x | 11.0 | exact for all four sets |\n"
    "| Mean of y | 7.50 | to 2 places (7.50, 7.50, 7.50, 7.50) |\n"
    "| Sample variance of y | 4.13 | to 2 places (4.127 each) |\n"
    "| Correlation between x and y | 0.816 | to 3 places |\n"
    "| Linear regression line | y = 3.00 + 0.500·x | to 2-3 places |\n"
    "| R² of the regression | 0.667 | to 3 places |\n\n"
    "All four datasets share the same statistics — yet they look nothing alike:"
)

code(
    "fig, axes = plt.subplots(2, 2, figsize=(9, 7), sharex=True, sharey=True)\n"
    "xs = np.linspace(3, 20, 100)\n"
    "for i, ax in zip([1, 2, 3, 4], axes.flat):\n"
    "    x = ans[f'x{i}']; y = ans[f'y{i}']\n"
    "    b, a, r, p, se = stats.linregress(x, y)\n"
    "    ax.scatter(x, y, color='tab:blue', s=40, zorder=3)\n"
    "    ax.plot(xs, a + b*xs, color='tab:red', lw=1.5)\n"
    "    ax.set_title(f'Set {i}: y = {a:.2f} + {b:.2f}x,  r = {r:.3f}')\n"
    "    ax.grid(True, alpha=0.3)\n"
    "fig.suptitle(\"Anscombe's quartet — identical stats, different shapes\", fontsize=14, fontweight='bold')\n"
    "fig.supxlabel('x'); fig.supylabel('y')\n"
    "plt.tight_layout(); plt.show()"
)

md(
    "**Reading:** set 1 is a genuine linear relationship; set 2 is a clean parabola "
    "(a line is the wrong model); set 3 is perfectly linear except for one outlier "
    "that drags the slope; set 4 is a vertical stack plus a single high-leverage "
    "point that alone defines the fitted line."
)

# ---- Task 2: Datasaurus ----
md(
    "## Task 2 — Datasaurus dozen (`ans2.tsv`)\n\n"
    "Thirteen datasets of 142 points each. For every dataset we compute mean x, "
    "mean y, SD x, SD y and the correlation, rounded to 3 places."
)

code(
    "dino = pd.read_csv('reference/ans2.tsv', sep='\\t')\n"
    "g = dino.groupby('dataset')\n"
    "summary = pd.DataFrame({\n"
    "    'mean x': g['x'].mean(),\n"
    "    'mean y': g['y'].mean(),\n"
    "    'sd x': g['x'].std(ddof=1),\n"
    "    'sd y': g['y'].std(ddof=1),\n"
    "    'corr': g.apply(lambda d: d['x'].corr(d['y']), include_groups=False),\n"
    "}).round(3)\n"
    "summary"
)

md(
    "Every dataset has essentially the same mean x ≈ 54.3, mean y ≈ 47.8, "
    "SD x ≈ 16.8, SD y ≈ 26.9 and corr ≈ −0.06. Now the scatter plots, one subplot "
    "per dataset (same panel idea as Task 5 in Lab 5):"
)

code(
    "names = sorted(dino['dataset'].unique())\n"
    "fig, axes = plt.subplots(3, 5, figsize=(15, 9), sharex=True, sharey=True)\n"
    "for name, ax in zip(names, axes.flat):\n"
    "    d = dino[dino['dataset'] == name]\n"
    "    ax.scatter(d['x'], d['y'], s=8, color='tab:green')\n"
    "    ax.set_title(name)\n"
    "    ax.grid(True, alpha=0.3)\n"
    "for ax in axes.flat[len(names):]:\n"
    "    ax.axis('off')\n"
    "fig.suptitle('Datasaurus dozen — same summary statistics, wildly different shapes', fontsize=14, fontweight='bold')\n"
    "fig.supxlabel('x'); fig.supylabel('y')\n"
    "plt.tight_layout(); plt.show()"
)

md(
    "### What do \"d\" and \"s\" stand for?\n\n"
    "The 13 datasets are the **Datasaurus dozen**. The short labels are shape names:\n\n"
    "- **`d` = *dino*** — the points draw a **dinosaur** (the original *Datasaurus*).\n"
    "- **`s` = *star*** — the points draw a **five-pointed star**.\n\n"
    "(The rest follow the same convention: `a`=away, `h`=h_lines, `v`=v_lines, "
    "`x`=x_shape, `high`=high_lines, plus dots, circle, bullseye, slant_up, "
    "slant_down, wide_lines.)\n\n"
    "**Conclusion:** identical means, standard deviations and correlations tell you "
    "almost nothing about the data — you must plot it. See "
    "[*Same Stats, Different Graphs*](https://www.autodeskresearch.com/publications/samestats) "
    "and [Anscombe's quartet](https://en.wikipedia.org/wiki/Anscombe%27s_quartet)."
)

nb["cells"] = cells
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}

# Execute in the lab6 directory so the relative data paths resolve.
client = NotebookClient(nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": "."}})
client.execute()

with open("lab6.ipynb", "w") as f:
    nbf.write(nb, f)

html_exporter = HTMLExporter()
html_exporter.embed_images = True
body, _ = html_exporter.from_notebook_node(nb)
with open("report.html", "w") as f:
    f.write(body)

print("wrote lab6.ipynb and report.html")
