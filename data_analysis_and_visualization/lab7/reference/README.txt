====================================================================
                            Interactive plots
                              (continuation)
====================================================================

Aggregated statement: this project ran across lab7 and lab8. The lab8 version
below is the most extensive (adds the extra task, homework spec, and extra
links), so it's kept as the single statement for both.
Sources:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab7/
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab8/

====================================================================

In previous exercises we focused on static and animated plots.
We now move to so-called interactive plots.

====================================================================

We will focus on a few python libraries:
- mpld3     http://mpld3.github.io
- pygal     http://www.pygal.org/en/stable/
- plotly    https://plotly.com/python
- Bokeh     https://docs.bokeh.org
- HoloViews http://holoviews.org
- Altair    https://altair-viz.github.io/gallery/index.html#interactive-charts

* you can use also one other extra library (if you find it as useful as those above)
* for installing libraries ue can use Virtual Environment
https://docs.python.org/3/tutorial/venv.html

====================================================================

The task:

From the six libraries above choose three.
Next using each library generate two, separate, interactive plots 

For instance:

mpld3_plot1_data1.py
mpld3_plot2_data2.py

pygal_plot1_data1.py
pygal_plot2_data2.py

bokeh_plot1_data1.py
bokeh_plot2_data2.py

So let's say you use temperature dataset (data1) and plot type: lineplot (plot1).
Thus you should have interactive lineplots from mpld3, pygal, bokeh.

(Six plots in total)

You can use the data from previous exercises, but you do not need to.
You are not allowed to use examples from libraries tutorials/galleries 
(obviously, you can use them for learning purposes).

Hint: frequently the data used for making animated plots can be easily 
transformed into the interactive plot, but it may require to move to 
different plot type e.g. bar plot with time (the dimension upon we 
updated plot for population) can be scatter plot with tooltips

====================================================================

Additionally, the scripts should have one positional parameter [0/1] for showing or 
saving the plot.

For instance typing in the terminal: 
python plot1.py 0      [will show the plot in interactive mode, plt.show()]
python plot1.py 1      [will store the plot in the file and print the path to the file]

====================================================================

Extra task:

You can earn up to an extra 50% if you generate each plot using each 
library on the same data from the main task (18 plots).

For instance: 

mpld3_data1.py      mpld3_data2.py      mpld3_data3.py
pygal_data1.py      pygal_data2.py      pygal_data3.py
bokeh_data1.py      bokeh_data2.py      bokeh_data3.py

mpld3_data4.py      mpld3_data5.py      mpld3_data6.py
pygal_data4.py      pygal_data5.py      pygal_data6.py
bokeh_data4.py      bokeh_data5.py      bokeh_data6.py

====================================================================

Prepare the homework as a project directory with the above plots. 

It should contain:
- the main report file in HTML form (with all the plots embedded)* 
- the data for plots
- the python scripts generating plots (one script per one plot)**
- the separate plots

*  static HTML file without external dependencies; all plots in one(!) HTML file
** plain python plots (*.py)- thus no jupyter notebooks, the script 
should use one parameter [0/1] for showing or saving the plot.

All files should be sent until 04.05.2026 - Monday (!)

via email to lukaskoz@mimuw.edu.pl with the email subject:
'DAV26_lab08_hw_Surname_Name' without email text body and with 
'DAV26_lab08_hw_Surname_Name.7z' (ASCII letters only) attachment.

====================================================================
EXTRAS

For Data visualization:
https://python-graph-gallery.com/  Great site, many examples (focus on matplotlib or seaborn)
https://github.com/microsoft/data-formulator
https://github.com/rgerum/pylustrator

For speed:
https://github.com/cupy/cupy CuPy: NumPy & SciPy for GPU
https://github.com/fireducks-dev/fireducks Replacement of Pandas
https://pola.rs/ Replacement of Pandas
https://pypy.org/ about 3 times faster than CPython (which also worth to try among similar like Numba, Cython, GraalPy)

Varia:
https://github.com/yobibyte/report Alternative to jupiter notebooks

