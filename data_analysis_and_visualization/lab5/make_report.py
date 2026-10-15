"""Build the combined lab4 + lab5 report as report.pdf.

Embeds every figure produced by the lab4 and lab5 scripts, each with a short
caption, plus a title page and section intros. Uses matplotlib's PdfPages so it
needs no extra dependencies. Run: python make_report.py
"""

import os
import textwrap

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

LAB4 = "../lab4"
LAB5 = "."
OUT = "report.pdf"

TITLE = "Exploring Global Temperatures Since 1750"
SUBTITLE = "Data Analysis & Visualization - Labs 4 & 5 (temperature project)"

# (image_path, heading, caption)
FIGURES = [
    (f"{LAB4}/fig1.png", "Task 2a - scatter with default markers",
     "Every monthly average temperature against year. Large filled circles "
     "overlap so heavily that the plot is essentially a solid block: unreadable."),
    (f"{LAB4}/fig2.png", "Task 2b - point markers and a grid",
     "Switching to small point markers and adding a grid already reveals the "
     "vertical banding of the seasonal cycle, but the mass of points is still dense."),
    (f"{LAB4}/fig3.png", "Task 2c - transparency",
     "Adding alpha transparency lets density show through: darker regions are where "
     "most observations fall, so the bulk of the distribution becomes visible."),
    (f"{LAB4}/fig4.png", "Task 2d - colour",
     "Colouring the points adds a third channel, but for this data it does not add "
     "much insight - a scatter plot is simply not the right tool here."),
    (f"{LAB4}/fig5.png", "Task 3a - box plot per country",
     "Distribution of temperatures within each country. Medians, spread and outliers "
     "are now readable at a glance, and hot vs. cold / stable vs. variable climates stand out."),
    (f"{LAB4}/fig6.png", "Task 3b - box plot with jitter",
     "Overlaying a transparent jittered scatter shows how many observations sit behind "
     "each box, so sample size and density are not hidden by the summary."),
    (f"{LAB4}/fig7.png", "Task 3c - violin plot",
     "Violin plots draw the estimated density, exposing multi-modal shapes (e.g. strong "
     "seasonal double peaks) that a box plot would hide."),
    (f"{LAB5}/fig7.png", "Task 4a - one continuous line",
     "Yearly average per (year, country) plotted as a single line. The curve jumps "
     "between countries within each year, producing a jagged, unreadable trace."),
    (f"{LAB5}/fig8.png", "Task 4b - split by country",
     "Drawing one black line per country removes the jumps; the individual climate "
     "levels separate, but without colour the lines are hard to tell apart."),
    (f"{LAB5}/fig9.png", "Task 4c - colour per country",
     "Assigning a colour and a legend entry to each country finally makes the yearly "
     "trends comparable; a gentle warming drift is visible in most series."),
    (f"{LAB5}/fig10.png", "Task 5a - one subplot per country",
     "Faceting into a 3x3 panel gives each country its own axes, removing overlap and "
     "letting shape and trend be read country by country on a shared scale."),
    (f"{LAB5}/fig11.png", "Task 5b - split each subplot by city",
     "Each country panel is split into its cities. More detail is visible, but the "
     "default dark grid competes with the data."),
    (f"{LAB5}/fig12.png", "Task 5c - clean reversed grid",
     "Reversing the grid (light panel, white grid lines) reduces visual noise and "
     "prints cleanly, while keeping the per-city structure."),
    (f"{LAB5}/fig13.png", "Task 5d - cities in colour with legends",
     "Colouring the cities and adding per-subplot legends uses the space gained by "
     "faceting to show which city each line is."),
    (f"{LAB5}/fig14.png", "Task 5e - final panel (shared legend)",
     "Presentation-ready version: bold titles, larger fonts, rotated year ticks and a "
     "single shared city legend on the right."),
    (f"{LAB5}/fig15.png", "Task 5e - final panel (per-country legends)",
     "Alternative final layout with a legend inside every country panel, useful when "
     "the figure is printed and read one panel at a time."),
]

INTRO = (
    "This report walks through the temperature-exploration project from the simplest "
    "to progressively more informative plots. Task 1 cleaned the raw data "
    "(temperatures_clean.csv): rows with missing City/Country or missing Fahrenheit "
    "temperature/uncertainty were dropped, the constant 'day' column was removed, and "
    "temperatures were converted from Fahrenheit to Celsius. Tasks 2-3 (lab 4) build "
    "scatter, box and violin plots of the raw monthly data; tasks 4-5 (lab 5) move to "
    "yearly time series and small-multiple panels. Each figure below is annotated with "
    "what it shows and why the next step improves on it."
)


def text_page(pdf, title, subtitle=None, body=None):
    fig = plt.figure(figsize=(8.27, 11.69))  # A4 portrait
    fig.text(0.5, 0.80, title, ha="center", va="center",
             fontsize=24, fontweight="bold", wrap=True)
    if subtitle:
        fig.text(0.5, 0.72, subtitle, ha="center", va="center", fontsize=13)
    if body:
        wrapped = "\n".join(textwrap.wrap(body, width=78))
        fig.text(0.1, 0.60, wrapped, ha="left", va="top", fontsize=11)
    plt.axis("off")
    pdf.savefig(fig)
    plt.close(fig)


def figure_page(pdf, img_path, heading, caption):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.text(0.5, 0.95, heading, ha="center", va="top", fontsize=15, fontweight="bold")
    ax = fig.add_axes([0.05, 0.22, 0.90, 0.68])
    ax.imshow(mpimg.imread(img_path))
    ax.axis("off")
    wrapped = "\n".join(textwrap.wrap(caption, width=90))
    fig.text(0.08, 0.16, wrapped, ha="left", va="top", fontsize=10)
    pdf.savefig(fig)
    plt.close(fig)


def main():
    with PdfPages(OUT) as pdf:
        text_page(pdf, TITLE, SUBTITLE, INTRO)
        for img, heading, caption in FIGURES:
            if not os.path.exists(img):
                print(f"WARNING missing figure: {img}")
                continue
            figure_page(pdf, img, heading, caption)
    print(os.path.abspath(OUT))


if __name__ == "__main__":
    main()
