===============================================================================================================
=====================     Animated plots (World Bank population project) - aggregated  =======================
===============================================================================================================

Sources (aggregated, most extensive statement of each part kept, repeated recaps removed):
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab1/  (introduces the exercise)
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab2/  (parts I & II)
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab3/  (part III + final combined homework)

This project ran across three labs. Each lab's page recapped the previous selection
(a/b/c below) before adding new requirements - that recap is collapsed here into one
copy. The standalone "youtube video -> gif" exercise from lab1 is unrelated and kept
separately in ../../lab1/reference/. The Gantt chart task that was appended to lab3's
page is also unrelated and kept separately in ../../lab3/reference/.

===============================================================================================================
Exercise 2 (lab1): initial data selection
===============================================================================================================

Given the data from The World Bank:
https://data.worldbank.org/indicator/SP.POP.TOTL?end=2024&start=1960&view=chart
do animated bar plots (gif file) for all years for:

a) 5 most populated countries (filter out groups like South Asia, OECD, etc.)

b) pick one country and year at random and then find 4 other countries that are the closest by
population size (either + or -) in given year and do similar plot (e.g., Chile at 1985 and 4 other countries)

c) the same as (b) but this time use Poland as "the centroid"
(*you can use a different country - your homeland - if applicable)

Expected result: 3 animated bar plots (gif)
Example (task a, showing why a floating x-axis is bad practice):
- bad: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab1/task_a_bad_population_floating_x-axis.gif
       (kept here as task_a_bad_population_floating_x-axis.gif)
- good: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab1/task_a_good.gif
        (kept here as task_a_good.gif)

IMPORTANT: For animation plots use as much as possible "matplotlib.animation"
https://matplotlib.org/stable/api/animation_api.html
Remember, we use English. All text used in the plots should be in English.

===============================================================================================================
Part I (lab2): Playing with colors and labels
===============================================================================================================

For all plots from exercise 2 (a-c) do bar plots:
a) color version (most likely you already have a good starting point)
b) black & white version

Requirements:
- on top of each bar put three letters "Country Code" e.g. CHN for China
- "Country Code" position is updated with respect to the bar size
- for the black-and-white version use shapes and/or textures to indicate the classification
- the axis indicating the population should be fixed
  (the bar should show the increase, not the leadership)
- there is a year counter inside of the plot (make it big enough)
- the font for all elements should be visible (from a large distance)
- increase the readability of the plot as much as possible
  (e.g. do not use 150.000.000, 150e6 on the scale; 150M is much shorter and easy to read)

Expected result: 6 animated bar plots (gif; 3 b&w and 3 colors)

===============================================================================================================
Part II (lab2): Play with a different representation of the data
===============================================================================================================

All of the plots so far had been "bar plots". Now, the task is to present
the data using different plot representations. For each a-c from the previous lab do similar
animated plots, but as:
A) line plot (so the plots start as a dot and the line moves while time progress)
B) bubble plot (x is time, y is the population, z (bubble) is a population density)
C) any other representation

- find the data about the area related to the countries of interest and calculate
population density (population/area).

Requirements:
- on top of each bar, line or bubble put a three-letter "Country Code" e.g. CHN for China
- "Country Code" position is updated with the respect to the line or bubble location
- there is a year counter inside of the plot (make it big enough)
- the font for all elements should be visible (from a large distance)

Expected result: three animated, color plots (gif) with line plots, three bubble plots,
and three more plots (other)

===============================================================================================================
Part III (lab3): Exploration of the data
===============================================================================================================

Select a group of 4-8 countries that:
- at least one shows some strange behavior e.g. strong increase, decrease or
stability of the population size in some particular period of time
(thus it is up to you to find those in the data)
- mark this event on the plot

For instance, you could pick one or a few countries in some war zone and few
other outside of it (e.g. Rwanda in the 90s) and show how the population changed
(to highlight the difference try to use neighbors or/and countries with similar
population size). To mark the event stop/freeze (or decrease speed)
the animation for ~4s in order to allow people to read the information
(imagine that you are having a speech and you want to emphasize the fact)
- thus you need to put some additional text for those ~4s in some part
of the plot (e.g. "WAR") explaining the observed fact. If the selected
event is related to a given period e.g. 5 years, than you show the text
on all related years (e.g. 1992-1995).

Expected result: 1 animated, bar plot (gif)
Example plot: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab3/lab3_1.gif
(kept here as lab3_1.gif)

===============================================================================================================
Homework (final, combined across lab1 + lab2 + lab3)
===============================================================================================================

The report regarding the whole project should be made in HTML.

The project folder should include:
1) raport.html (do not overuse jupyter and similar tools - the idea is to have
   plots embedded in one place in nice and clean form; the report is not a place
   for the code, use separate *.py files for that)
2) the data (cleaned version)
3) the plots (gifs from parts I, II, III as separate files)
4) the python scripts

There should be 15 plots in total (parts I & II):
a) two plots for 5 most populated countries (b&w and color version)
b) two plots for 5 randomly picked (b&w and color version)
c) two plots for 5 with Poland as the centroid (b&w and color version)
A) three animated, color plots (gif) with line plots (rendered from a-c data)
B) three bubble plots (rendered from a-c data)
C) three other plots (rendered from a-c data)
plus 1 additional animated bar plot for Part III (event highlighting).

Remember, all plots should be good quality, and contain labels for axes, legends,
titles, proper font size, etc. Use English for all labels/legends/descriptions.

(Original deadlines, for reference: lab1&2 homework was due 07.03.2026, extended
through lab3 to 14.03.2026, both via email to lukaskoz@mimuw.edu.pl.)
