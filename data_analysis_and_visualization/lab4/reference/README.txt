================================================
    Exploring global temperatures since 1750
                  (part 1)
================================================
Source: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab4/
(continues in ../../lab5/reference/README.txt, part 2)

Exercise 4


During this exercise we will plot some data about the temperatures. 
We will move from the simplest to more complicated plots.


The data: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab4/temperature.csv

================================================

Task 1: Data cleaning and preparing for plotting
a) there are missing values for City and Country in some records, remove those
b) there are NA's in AverageTemperatureFahr and AverageTemperatureUncertaintyFahr, 
remove rows with missing values in those fields
c) remove empty 'City' and 'Country' fields
d) 'day' field has no other values besides 1, thus you can remove it from the data
e) convert AverageTemperatureFahr and AverageTemperatureUncertaintyFahr into 
AverageTemperatureCelsius and AverageTemperatureUncertaintyCelsius 
(you can drop '*Fahr' columns)
f) save new csv file with cleaned data (e.g. temperatures_clean.csv)

================================================

Task 2: Scatter plot
a) first plot all AverageTemperatureCelsius vs. year
The result should look like:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab4/fig1.png

Summary: the plot is quite unreadable (we used to big 'circles' for data point)

b) recreate the plot using 'points' instead 'circles', add grid
The result should look like:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab4/fig2.png

Summary: better, but still not very informative

c) add transparency
The result should look like:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab4/fig3.png

Summary: you start to see anything

d) add color
The result should look like:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab4/fig4.png

Summary: this did not help to much, we move to another plot type and look more deeply 

================================================

Task 3: Box plots
a) visualising the distribution of temperatures within each country

The result should look like:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab4/fig5.png

Summary: we start to see some interesting facts

b) add jitter to boxplot

You will need to play with the parameters e.g. transparency
https://stackoverflow.com/questions/29779079/adding-a-scatter-of-points-to-a-boxplot-using-matplotlib

The result should look like:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab4/fig6.png

c) change boxplot to violin plot (sometimes known as a beanplot)
Boxplots are useful summaries, but they hide the shape of the distribution. 
For instance, if there is a bimodal distribution, this would not be observed
with a boxplot. An alternative is a violin plot, where the shape 
(of the density of points) is drawn.

================================================
================================================

After the exercise you should have:
- temperatures_clean.csv
- 7 python scripts
- (at least) 7 plots in png files produced by python scripts

Note: you need to use python, but you do not need limit yourself to matplotlib

