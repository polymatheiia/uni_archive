====================================================================
                    Time Series Forecast
                    (two weeks exercise)
====================================================================

Aggregated statement: this project ran across lab9 and lab10 with near-identical
pages. The lab10 version below is the most extensive (adds the homework spec),
so it's kept as the single statement for both.
Sources:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab9/
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab10/

====================================================================

We will re-use the temperature file from Lab 4:
The data: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab9/temperature.csv

====================================================================

The task: We will do some visualization and some forecasting of country temperature and 
global warming.

1) for each country (there are 8 countries) calculate the average temperature in given 
year in Celsius (note that for some time series models month data are also useful)

2) make scatter plots for all countries (one plot per one country)
Do you see any trend already? Does the data contain seasonal compound? 
(Hint: zoom the main plot to few years)

Expected result: 8 scatter plots (plus scripts and data files) 
e.g. bra.png, fra.png, jap.png, etc.

3) Make some forecasting. 
Our data are limited to 2024. Let's make some predictions for the next 250 years. 

Task: Using Simple Time Series Forecasting Methods (for a complete list see below). 
Make forecasting for 2 selected countries using 3 (out of 12) forecasting methods.
Apart from the main trend, you should also include uncertainty of the forecasting 
(e.g. by adding 95% confidence interval). 

Expected result: 6 plots (2 countries * 3 methods) e.g. 
bra_ar.png, bra_ma.png, bra_arma.png
fra_ar.png, fra_ma.png, fra_arma.png

Important: the more complicated model is the more parameters you can choose or tune. 
Therefore, focus on reading the documentation and understanding what you are doing, 
rather than on using default parameters.

You can earn extra points (up to 50%) for making a prediction using more than 
3 methods or/and 2 countries or adding analysing seasonal trends.

See also:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/lectures/lecture10/DAV_Lecture_10.pdf

4) Time series cross-validation

Do you see any difference between Time Series Forecasting Methods in the quality of 
the forecasts? 

If not, maybe try to extend the time span of forecasting.
Or maybe there is a better way to say which model/parameters are better?

Explore TimeSeriesSplit ("from sklearn.model_selection import TimeSeriesSplit")

Using some forecast quality metrics (e.g. Mean Absolute Error or any other) and 
TimeSeriesSplit (e.g. n_splits=5) calculate the model fitness. 
Take the two countries from part (3) and do a table with statistics. 

Expected result: the table with statistics
_____________________________

        ar    arma    hwes
_____________________________

bra    MAE     MAE     MAE     

fra    MAE     MAE     MAE     
_____________________________

====================================================================
Simple Time Series Forecasting Methods

 1. Autoregression (AR)
 2. Moving Average (MA)
 3. Autoregressive Moving Average (ARMA)
 4. Autoregressive Integrated Moving Average (ARIMA)
 5. Seasonal Autoregressive Integrated Moving-Average (SARIMA)
 6. Seasonal Autoregressive Integrated Moving-Average with Exogenous Regressors (SARIMAX)
 7. Vector Autoregression (VAR)
 8. Vector Autoregression Moving-Average (VARMA)
 9. Vector Autoregression Moving-Average with Exogenous Regressors (VARMAX)
10. Simple Exponential Smoothing (SES)
11. Holt Winter's Exponential Smoothing (HWES)
12. prophet (by itself this is only simple linear model, but it is worth to know the api 
and the library)
====================================================================

Useful links:

https://towardsdatascience.com/time-series-analysis-in-python-an-introduction-70d5a5b1d52a
https://stackoverflow.com/questions/49712037/trend-predictor-in-python
https://machinelearningmastery.com/make-predictions-time-series-forecasting-python/
https://machinelearningmastery.com/multi-step-time-series-forecasting/
https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/
https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/
https://www.datacamp.com/courses/introduction-to-time-series-analysis-in-python

Alternative libraries:
https://skforecast.org 
https://github.com/Nixtla/statsforecast
https://github.com/MBrouns/timeseers (based on Prophet)
https://business-science.github.io/pytimetk/

Varia:
https://www.kaggle.com/code/konradb/ts-0-the-basics
https://pyoflife.com/introduction-to-time-series-with-python/
https://github.com/cleanlab/cleanlab


====================================================================

Prepare the homework as a project directory with the mentioned plots and table. 

It should contain:
- the main report file in HTML form* (with 14 plots and the table) 
- the data for plots
- the python scripts generating plots (one script per one plot)**
- the separate plots (*.png)
- the script for generating the table

*  static HTML without external dependencies
** plain python plots (*.py)- thus no jupyter notebooks

Additionally, the plotting scripts should have one parameter [0/1] for showing or 
saving the plot.

For instance typing in the terminal: 
python plot1.py 0      [will show the plot in interactive mode, plt.show()]
python plot1.py 1      [will store the plot in the file and print the path to the file]

All files should be sent until Saturday 16.05.2026
via email to lukaskoz@mimuw.edu.pl with the email subject:
'DAV26_lab10_hw_Surname_Name' without email text body and with 
'DAV26_lab10_hw_Surname_Name.7z' (ASCII letters only) attachment.

Using non-English labels, legends, descriptions, etc. will be scored -10%

Additionally, all problems with the structure of the plot e.g.
the plot size, labels font size, etc. will also affect the grading. 
You need to follow the advice included in the lectures and in the instruction.
