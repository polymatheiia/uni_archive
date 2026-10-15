# Lab 1 — Animated plots, part 1

Two exercises on this lab's page:

## Exercise 1 — video → animated GIF

Learn the GIF-making workflow (yt-dlp → ffmpeg → gif).

- `scripts/youtube_to_gif.py` — downloads a video with yt-dlp (smallest format) and
  converts a chosen segment to a GIF with ffmpeg.
- `images/tv_series_demo.gif` — a real 6-second, 8-fps clip rendered directly from
  the course's example video ("Most Popular TV Series 1986–2019"), produced with the
  same ffmpeg step.

```bash
python scripts/youtube_to_gif.py "https://www.youtube.com/watch?v=7DemM7UGmIg" \
    --start 20 --dur 6 --fps 8 --width 520 -o images/tv_series.gif
```

## Exercise 2 — World Bank population animations

This is the start of the population-animation project that continues through labs 2
and 3. The full solution (data prep, the three country groups, and all animated
plots) lives in **[`../lab2/`](../lab2/)** with the combined report at
`../lab2/raport.html`. See `../lab2/scripts/`.
