"""lab1 exercise 1: scrape a plotting video and turn it into an animated GIF.

Downloads a video with yt-dlp (preferring a small format) and converts a chosen
segment to a GIF with ffmpeg, mirroring the workflow in the lab README
(yt-dlp -> ffmpeg frames -> gif).

Examples:
    # from the course's example video, 6 s starting at 20 s, 8 fps, 520 px wide
    python youtube_to_gif.py "https://www.youtube.com/watch?v=7DemM7UGmIg" \
        --start 20 --dur 6 --fps 8 --width 520 -o ../images/tv_series.gif

The rendered ../images/tv_series_demo.gif in this project was produced with the
same ffmpeg step directly from the course-hosted copy of that video.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def have(tool):
    return shutil.which(tool) is not None


def download(url, workdir):
    """Download the video with yt-dlp; return the path to the file."""
    out = str(Path(workdir) / "video.%(ext)s")
    # -S "+size" prefers the smallest format; merge to mp4 when possible.
    cmd = ["yt-dlp", "-S", "+size,+res", "-o", out, url]
    subprocess.run(cmd, check=True)
    files = list(Path(workdir).glob("video.*"))
    if not files:
        raise RuntimeError("yt-dlp produced no file")
    return str(files[0])


def to_gif(src, start, dur, fps, width, out_path):
    vf = f"fps={fps},scale={width}:-1:flags=lanczos"
    cmd = ["ffmpeg", "-y", "-ss", str(start), "-t", str(dur),
           "-i", src, "-vf", vf, "-loop", "0", out_path]
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", help="YouTube (or direct) video URL")
    ap.add_argument("--start", type=float, default=0.0, help="segment start (s)")
    ap.add_argument("--dur", type=float, default=6.0, help="segment duration (s)")
    ap.add_argument("--fps", type=int, default=8)
    ap.add_argument("--width", type=int, default=520)
    ap.add_argument("-o", "--out", default="../images/out.gif")
    args = ap.parse_args()

    if not have("ffmpeg"):
        sys.exit("ffmpeg is required")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    # A direct video URL can be fed straight to ffmpeg (it streams only the
    # requested segment); otherwise download first with yt-dlp.
    if args.url.lower().endswith((".mp4", ".webm", ".mkv")):
        to_gif(args.url, args.start, args.dur, args.fps, args.width, args.out)
    else:
        if not have("yt-dlp"):
            sys.exit("yt-dlp is required for non-direct URLs")
        with tempfile.TemporaryDirectory() as tmp:
            video = download(args.url, tmp)
            to_gif(video, args.start, args.dur, args.fps, args.width, args.out)

    print(Path(args.out).resolve())


if __name__ == "__main__":
    main()
