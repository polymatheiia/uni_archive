# Lab 3 — Animated plots, part 3

Two parts on this lab's page. Part III (data exploration / event highlight) continues
the population project; part IV (Gantt) is standalone.

- `scripts/event_highlight.py` → `images/event_rwanda.gif` — animated bar plot of
  Rwanda + four neighbours that **freezes for ~4 s on 1994** with a "RWANDAN
  GENOCIDE" label (Rwanda fell from ~8.0M in 1993 to ~5.7M in 1995).
- `scripts/gantt.py` → `images/gantt_color.pdf`, `images/gantt_bw.pdf` (full-page
  A4) plus PNG copies — Gantt of the University of Warsaw 2026/2027 academic year
  (MIM faculty), transcribed from the Rector's resolution
  `reference/M.2026.30.Post.1.EN.pdf` (Appendix 1, pages 3–4).

Both are embedded in the combined project report **`../lab2/raport.html`**.

```bash
python scripts/event_highlight.py
python scripts/gantt.py
```
