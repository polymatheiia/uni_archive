================================================
    Exploring global temperatures since 1750
                  (part 2)
================================================
Source: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab5/
(continues from ../../lab4/reference/README.txt, part 1)

The continuation of temperature plots. Thus you should already have
the dataset, scripts and plots from Tasks 1-3

The data: ../lab4/temperatures.csv

================================================

Task 4: Time series
a) calculate average temperature per year per each country 
- in this part, you need to group data by year and country 
- then calculate mean for each group
- do line plot with years on x axis and temperature on y axis

The result should look like: fig7.png

Summary: the plot is quite unreadable

b) to avoid too much of information split graphed data by Country

The result should look like: fig8.png

Summary: better

c) and add color

The result should look like: fig9.png

Summary: you start to see anything

================================================

Task 5: Grouping multiple subplots
a) make one (!) plot containing multiple subplots

The result should look like: fig10.png


b) split line in each subplot by city of each country

The result should look like: fig11.png

c) clean background 

Frequently, plotting libraries by default adds a grey grid. While
it may look nice at first glance, but, for print and better 
clarity, it is wise to reverse the grid coloring

The result should look like: fig12.png


d) divide into cities

As we gain some space by dividing the data into subplots, we can
use it to show more data. For each subplot/country add lines for 
individual data. You can have one legend or multiple legends 
(separate for each subplot). Mark the cities in different colors.

The result should look like: fig13.png

e) change labels, add title, customize fonts, rotate elements, etc.

The result should look like: fig14.png, fig15.png

Note: you need to use python, but you do not need limit yourself to 
matplotlib (seabonr is nice alternative plotting library)

================================================
================================================

Prepare the homework as a project directory with lab4 & lab5 exercises. 

It should contain:
- the main report file in PDF (with all the plots embedded)* 
- the python scripts generating plots (one script per one plot)**
- the separate plots as image files

*  no python code in the report file
** plain python plots (*.py)- thus no jupyter notebooks

For instance: task2a.py, task2b.py, ...
Additionally, the script should one parameter [0/1] for showing or saving the plot.
For instance typing in the terminal: 
python task2a.py 0      [will show the plot in interactive mode, plt.show()]
python task2a.py 1      [will store the plot in the file and print the path to the file]

Requred scripts/plots: 
task2a, task2b, task2c, task2d, 
task3a, task3b, task3c,
task4a, task4b, task4c,
task5a, task5b, task5c, task5d, task5e (one final plot)

As you can see there will be (at least) 15 scripts and 15 plots. Many scripts will 
share code, thus it might be worth moving some redundant code to separate *.py 
module (e.g. utils.py).

As usual, organise the project directory into subdirectories
e.g. ./images ./scripts ./data, etc.

All files should be sent until 12.04.2026 via Email
'DAV26_lab5_hw_Surname_Name.7z' (ASCII letters only) attachment.

Using non-English labels, legends, descriptions, etc. will be scored -10%

Additionally, all problems with the structure of the plot e.g. the plot size,  
labels font size, etc. will also affect the grading. You need to follow advice 
included in the lectures or/and learned during the exercises.

