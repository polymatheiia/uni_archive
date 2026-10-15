"""Build raport.html for the animated-plots project (labs 1-3).

References the rendered GIFs/PNGs by relative path (report lives in lab2/, images
in lab2/images and lab3/images). Run after 02-05_*.py and the lab3 scripts.
"""

import os

OUT = "raport.html"


def fig(src, caption):
    return (f'<figure><img src="{src}" loading="lazy" style="max-width:100%;border:1px solid #ddd;border-radius:6px;">'
            f'<figcaption>{caption}</figcaption></figure>')


def row(*figs):
    return f'<div class="row">{"".join(figs)}</div>'


HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Animated plots - World Bank population (labs 1-3)</title>
<style>
 body {{ font-family: system-ui, sans-serif; max-width: 1150px; margin: 0 auto; padding: 1.5rem; color:#1a1a1a; }}
 h1 {{ border-bottom:3px solid #333; padding-bottom:.3rem; }}
 h2 {{ color:#2c3e50; margin-top:2.2rem; }}
 .row {{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; }}
 figure {{ margin:0; }} figcaption {{ font-weight:600; margin:.3rem 0 .6rem; }}
 code {{ background:#f2f2f2; padding:.1rem .3rem; border-radius:3px; }}
</style></head><body>
<h1>Animated plots — World Bank population</h1>
<p>Project spanning labs 1–3. Population data from the World Bank indicator
<code>SP.POP.TOTL</code> (1960–2024) and land area <code>AG.LND.TOTL.K2</code>.
Aggregate rows (World, OECD, income groups, …) are filtered out using the World
Bank country metadata (real countries have a non-empty Region). All animations
use <code>matplotlib.animation</code>; every script re-derives its own data.</p>

<h3>Three country groups</h3>
<ul>
 <li><b>(a) Five most populated</b> in 2023: India, China, USA, Indonesia, Pakistan.</li>
 <li><b>(b) Random group</b>: a random country &amp; year (seed-fixed) plus the four
     closest by population that year.</li>
 <li><b>(c) Poland as centroid</b>: Poland plus the four countries closest to it by
     population in 2023.</li>
</ul>

<h2>1. Bar plots — colour &amp; black-and-white</h2>
<p>Fixed population axis (bars grow, ranking is not rescaled), three-letter country
codes tracking each bar, a large year counter and short <code>150M</code>-style
labels. The b&amp;w versions use hatches instead of colour.</p>
{row(fig("images/bar_a_color.gif","(a) most populated — colour"), fig("images/bar_a_bw.gif","(a) most populated — b&w"))}
{row(fig("images/bar_b_color.gif","(b) random group — colour"), fig("images/bar_b_bw.gif","(b) random group — b&w"))}
{row(fig("images/bar_c_color.gif","(c) Poland centroid — colour"), fig("images/bar_c_bw.gif","(c) Poland centroid — b&w"))}

<h2>2. Line plots</h2>
<p>Each series starts as a dot and grows into a line; the country code rides the
leading end.</p>
{row(fig("images/line_a.gif","(a)"), fig("images/line_b.gif","(b)"))}
{row(fig("images/line_c.gif","(c)"), "")}

<h2>3. Bubble plots</h2>
<p>x = year, y = population, bubble size = population density (people/km²), with a
faded trajectory trail.</p>
{row(fig("images/bubble_a.gif","(a)"), fig("images/bubble_b.gif","(b)"))}
{row(fig("images/bubble_c.gif","(c)"), "")}

<h2>4. Other representation — ranking race</h2>
<p>Horizontal bars re-sorted every year, so countries visibly overtake each other
in rank (unlike the fixed vertical bars above).</p>
{row(fig("images/other_a.gif","(a)"), fig("images/other_b.gif","(b)"))}
{row(fig("images/other_c.gif","(c)"), "")}

<h2>5. Event highlight (lab 3, part III)</h2>
<p>Rwanda and four neighbours. The animation freezes for ~4 seconds on 1994 with an
explanatory label to emphasise the population collapse caused by the genocide
(Rwanda fell from ~8.0M in 1993 to ~5.7M in 1995 before recovering).</p>
{row(fig("../lab3/images/event_rwanda.gif","Rwanda genocide, 1994"), "")}

<h2>6. Gantt chart (lab 3, part IV)</h2>
<p>Organisation of the University of Warsaw 2026/2027 academic year for the Faculty
of Mathematics, Computer Science and Mechanics, transcribed from the Rector's
resolution M.2026.30.Post.1 (Appendix 1). Full-page A4 PDFs:
<a href="../lab3/images/gantt_color.pdf">colour</a> /
<a href="../lab3/images/gantt_bw.pdf">black-and-white</a>.</p>
{row(fig("../lab3/images/gantt_color.png","Gantt — colour"), fig("../lab3/images/gantt_bw.png","Gantt — b&w"))}
</body></html>"""


def main():
    with open(OUT, "w") as f:
        f.write(HTML)
    print(os.path.abspath(OUT))


if __name__ == "__main__":
    main()
