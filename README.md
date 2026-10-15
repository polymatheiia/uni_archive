# uni_archive

Archive of my university coursework projects and homework submissions
(University of Warsaw, Faculty of Mathematics, Informatics and Mechanics).

Course names are given in English; the original Polish names are in parentheses.
Most assignment texts and comments in the code are in Polish or English depending on the course.

## Overview

| Folder | Course / subject | Level | Languages & tools | Contents |
|---|---|---|---|---|
| [`intro_to_c/`](intro_to_c) | Introduction to Computer Science (*Wstęp do informatyki*) | BSc, year 1 | C | Exercise and homework solutions: sorting, sieve of Eratosthenes, factorisation, text-file I/O, pointers and lists, a cheat-sheet program |
| [`oop_cpp/`](oop_cpp) | Object-Oriented Programming (*Programowanie obiektowe*) | BSc, year 2 | C++, CMake | Pass-assignment project (shop/city simulation with classes), lab exercises, exam |
| [`numerical_methods/`](numerical_methods) | Ordinary Differential Equations: computational labs (*Równania różniczkowe zwyczajne*) | BSc, year 2 | Python (Jupyter, SymPy) | Lab assignments LP2.1–LP3.1 and Project 1 |
| [`multivariate_statistics/`](multivariate_statistics) | Statistical Computing / Multivariate Statistics | MSc | R (R Markdown) | Two project assignments (PCA, covariance and correlation, scree plots) |
| [`time_series/`](time_series) | Time Series (*Szeregi czasowe*) | MSc | R (R Markdown) | Two projects |
| [`data_analysis_and_visualization/`](data_analysis_and_visualization) | Data Analysis and Visualization | MSc | Python (pandas, matplotlib, plotly, bokeh, mpld3, scikit-learn, PyTorch) | Labs 1–13, see below |
| [`mu_flu_timeseries/`](mu_flu_timeseries) | Applied Mathematics (*Matematyka użytkowa*), project 3 | MSc | Python | Time-series analysis of influenza incidence in Poland, 2010–2023 |
| [`mu_reconstruction_scratch/`](mu_reconstruction_scratch) | Applied Mathematics (*Matematyka użytkowa*), project 1 (my scratch work) | MSc | Python, NumPy | Experiments for a particle-track reconstruction task |

## Details

### `intro_to_c/`
- `ćwiczenia/` — weekly exercises `cwiczenia_1.c` … `cwiczenia_12.c`
- `moodle/` — assignments and examples from the course page (sorting algorithms, counting sort, primes, factorisation, text files)
- `poprawa/` — resubmitted (corrected) homework `Zadanie1–3`
- `1/` — first-week tasks
- `Sciaga/` — cheat-sheet program
- `trening*.c` — practice programs

Student ID lines were removed from the file headers.

### `oop_cpp/`
- `Projekt_zal/` — credit project: classes for a city with shop chains, stores, trade objects and customers (`miasto.h`, `funkcje.cpp`, `main.cpp`)
- `lab-cwiczenia-podstawy/` — basic class exercises (fractions, rectangles, dice, students, animals, expressions, …)
- `lab-mini-cwiczenie/` — small lab exercise
- `egzamin/` — exam solution

Build each folder with CMake: `cmake -S . -B build && cmake --build build`.

### `numerical_methods/`
Jupyter notebooks `LP2.1`, `LP2.2`, `LP2.3`, `LP3.1` and `Projekt 1` (lab assignments LP 1.1–1.2 and onward).
They install their own pinned SymPy at the top, so they are best run in a fresh environment.

### `multivariate_statistics/` and `time_series/`
`project1.Rmd` / `project2.Rmd` (multivariate statistics) and `project 1.Rmd` / `project 2.Rmd` (time series),
each with its knitted `.html`.

### `data_analysis_and_visualization/`
| Lab | Topic |
|---|---|
| `lab1`–`lab3` | Animated plots: video to GIF, animated bar, line and bubble charts of population data, event highlighting, Gantt chart |
| `lab4`–`lab5` | Static plots of global temperatures since 1750: scatter, transparency and colour, box/jitter/violin plots, report |
| `lab6` | The importance of plotting: Anscombe's quartet and the Datasaurus |
| `lab7` | Interactive plots in Bokeh, Plotly and mpld3 (stocks and wine data), HTML report |
| `lab9` | Time-series forecasting: AR/MA, exponential smoothing, cross-validated MAE, HTML report |
| `lab11`–`lab13` | Isoelectric-point project: dataset building (pI < 5 classification), classical ML, deep learning and inference, PDF report |

Each lab folder contains a `README.md` or report where available. `lab*/reference/` holds the instructor's
task material and reference output, not my work.

### `mu_flu_timeseries/`
Scripts for downloading and extracting regional influenza data (`flu_get_data.py`, `extract_flu_data_2022_2023.py`),
a Google Trends comparison (`multiTimeline.csv`, `geoMap.csv`), and the analysis notebook `analiza_szeregu_grypa.ipynb`.
The source Excel report from the national health authority is not included.

### `mu_reconstruction_scratch/`
Scratch scripts and a demo notebook for track reconstruction (geometry variants, peak position interpolation,
diagnostics). The finished group project lives in a separate repository (`MU-p1`).

## Not included
- Instructor-authored lab templates and lecture material
- Other students' work
- Raw third-party data files, virtual environments and IDE files (see `.gitignore`)
