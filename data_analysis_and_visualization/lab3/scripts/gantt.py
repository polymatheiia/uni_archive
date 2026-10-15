"""lab3 IV: Gantt chart of the UW 2026/2027 academic year (MIM faculty).

Dates transcribed from the Rector's resolution M.2026.30.Post.1 (Appendix 1, the
schedule for the Faculty of Mathematics, Computer Science and Mechanics - pages
3-4 of the PDF). Produces A4 colour and black-and-white single-page PDFs plus PNG
copies for the report.

Usage: python gantt.py
"""

import os
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch

# (label, start, end, category)
# Categories: W = winter classes, S = summer classes, E = exam session, B = break
TASKS = [
    ("Winter classes - block I",        date(2026, 10, 2),  date(2026, 11, 1),  "W"),
    ("Winter classes - block II",       date(2026, 11, 2),  date(2026, 12, 6),  "W"),
    ("Winter classes - block III",      date(2026, 12, 7),  date(2026, 12, 20), "W"),
    ("Winter holidays",                 date(2026, 12, 21), date(2027, 1, 6),   "B"),
    ("Winter classes - block III cont", date(2027, 1, 7),   date(2027, 1, 24),  "W"),
    ("Winter exam session",             date(2027, 1, 25),  date(2027, 2, 7),   "E"),
    ("Inter-semester break",            date(2027, 2, 8),   date(2027, 2, 14),  "B"),
    ("Summer classes - block I",        date(2027, 2, 22),  date(2027, 3, 21),  "S"),
    ("Summer classes - block II",       date(2027, 3, 22),  date(2027, 5, 2),   "S"),
    ("Spring holidays",                 date(2027, 3, 25),  date(2027, 3, 30),  "B"),
    ("Summer classes - block III",      date(2027, 5, 3),   date(2027, 6, 6),   "S"),
    ("Summer exam session",             date(2027, 6, 7),   date(2027, 6, 27),  "E"),
    ("Summer holidays",                 date(2027, 6, 28),  date(2027, 9, 30),  "B"),
    ("Winter-semester re-sit session",  date(2027, 2, 15),  date(2027, 2, 21),  "E"),
    ("Summer-semester re-sit session",  date(2027, 8, 30),  date(2027, 9, 12),  "E"),
]

CAT_NAME = {"W": "Winter classes", "S": "Summer classes",
            "E": "Examination session", "B": "Break / holidays"}
CAT_COLOR = {"W": "#1f77b4", "S": "#2ca02c", "E": "#d62728", "B": "#ff7f0e"}
# black-and-white: greyscale fills + hatches
CAT_GREY = {"W": "0.35", "S": "0.6", "E": "0.15", "B": "0.85"}
CAT_HATCH = {"W": "//", "S": "\\\\", "E": "xx", "B": ".."}


def draw_gantt(bw, out_pdf, out_png):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 portrait
    ypos = range(len(TASKS))
    for y, (label, start, end, cat) in zip(ypos, TASKS):
        left = mdates.date2num(start)
        width = mdates.date2num(end) - left
        if bw:
            ax.barh(y, width, left=left, height=0.6,
                    color=CAT_GREY[cat], edgecolor="black",
                    hatch=CAT_HATCH[cat], linewidth=1)
        else:
            ax.barh(y, width, left=left, height=0.6,
                    color=CAT_COLOR[cat], edgecolor="black", linewidth=0.5)

    ax.set_yticks(list(ypos))
    ax.set_yticklabels([t[0] for t in TASKS], fontsize=10)
    ax.invert_yaxis()
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
    ax.set_xlim(mdates.date2num(date(2026, 9, 20)), mdates.date2num(date(2027, 10, 10)))
    ax.set_xlabel("Date", fontsize=12)
    ax.set_title("University of Warsaw - academic year 2026/2027\n"
                 "Faculty of Mathematics, Computer Science and Mechanics",
                 fontsize=13, fontweight="bold")
    ax.grid(axis="x", alpha=0.4)

    if bw:
        handles = [Patch(facecolor=CAT_GREY[c], edgecolor="black", hatch=CAT_HATCH[c],
                         label=CAT_NAME[c]) for c in CAT_NAME]
    else:
        handles = [Patch(facecolor=CAT_COLOR[c], edgecolor="black", label=CAT_NAME[c])
                   for c in CAT_NAME]
    ax.legend(handles=handles, loc="lower right", fontsize=9, title="Phase")
    fig.text(0.5, 0.02,
             "Source: Rector's resolution M.2026.30.Post.1, Appendix 1 (MIM faculty).",
             ha="center", fontsize=7, color="0.4")

    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(out_pdf, format="pdf")       # full A4 page
    fig.savefig(out_png, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(os.path.abspath(out_pdf))
    print(os.path.abspath(out_png))


def main():
    img = os.path.join(os.path.dirname(__file__), "..", "images")
    os.makedirs(img, exist_ok=True)
    draw_gantt(False, os.path.join(img, "gantt_color.pdf"), os.path.join(img, "gantt_color.png"))
    draw_gantt(True, os.path.join(img, "gantt_bw.pdf"), os.path.join(img, "gantt_bw.png"))


if __name__ == "__main__":
    main()
