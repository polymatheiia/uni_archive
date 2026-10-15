===============================================================================================================
=========================================     Animated plots part 1  ==========================================
===============================================================================================================

Source: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab1/

Note: This lab's page also introduced the World Bank population animation exercise
(exercise 2, a/b/c). That part is cumulative with labs 2 and 3, so its aggregated,
most extensive task statement lives in ../../lab2/reference/README.txt instead of
being repeated here. This file only covers the standalone exercise 1 below.

===============================================================================================================

1) Scrap some youtube video with plots e.g. https://www.youtube.com/watch?v=7DemM7UGmIg
and convert it into animated gif.

Hints:
- use web browser plugins, youtube-dl or similar tools

Prefered setup:
https://github.com/yt-dlp/yt-dlp
https://pypi.org/project/yt-dlp/
Inspect formats with option -F & dowload rather smaller than bigger (-f option)

Install yt-dlp using venv:
a) https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
b) https://docs.python.org/3/tutorial/venv.html

- convert mp4 into gif using ffpmeg and convert (ImageMagic)
https://askubuntu.com/questions/648603/how-to-create-an-animated-gif-from-mp4-video-via-command-line
ffmpeg -i video.mp4  -r 5 'frames/frame-%03d.jpg'
cd frames
convert -delay 20 -loop 0 *.jpg myimage.gif

As you learned how to make animated gif by joining the image files ('convert' command
from ImageMagic), now it is time for PYTHON scripting and do some serious plotting.

===============================================================================================================

Reference assets for this exercise (not downloaded here due to size - fetch if needed):
- source video: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab1/Most%20Popular%20TV%20Series%201986%20-%202019-7DemM7UGmIg.mp4 (147M)
- extracted frames: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab1/frames.tar.gz (46M)

Useful libraries:
1) matplotlib https://matplotlib.org/stable/api/animation_api.html
2) bar-chart-race https://pypi.org/project/bar-chart-race/
