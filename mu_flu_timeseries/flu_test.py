import pandas as pd
from datetime import datetime, timedelta

import numpy as np

np.random.seed(2026) # obligatory fixed random seed for replicability

### problem data settings

REGION = "śląskie"
YEAR = 2026
WEEK = 4

folder = 'Data/'
folder = ''

print('='*24)
print(f'Problem statement: {REGION = }, {YEAR = }, {WEEK = }')
print('='*24)

def find_weeks(year, week, nofweeks=4):
    first_monday = datetime.strptime(f'{year}-W{week}-1', "%G-W%V-%u")
    mondays = [first_monday + timedelta(days=7 * i) for i in range(nofweeks)]
    last_sunday = (mondays[-1] + timedelta(days=6))
    return [m.isocalendar()[0:2] for m in mondays], first_monday, last_sunday

def flu_predict(region, year, week, infected, vaccinated, weather, trends):
    
    df_hourly = pd.read_csv(weather)
    df_infected = pd.read_csv(infected)
    df_vaccinated = pd.read_csv(vaccinated)
    df_trends = pd.read_csv(trends, skiprows=2)
    
    for df in (df_hourly, df_infected, df_vaccinated, df_trends):
        print(df.head())
        print('-'*20)
    
    weeks_tmp, _ , _  = find_weeks(year, week, nofweeks=6)
    weeks_forecast, _ , _  = find_weeks(weeks_tmp[-1][0], weeks_tmp[-1][1], nofweeks=4)
    
    forecast = []
    for (y,w) in weeks_forecast:
        infected = 100*np.random.rand() # THIS IS A PLACEHOLDER. Put here the prediction from your model instead!
        forecast.append(infected)
        print(f'Forecast for week {w:02d} of year {y}: {infected: 10.5f} per 100 000')
    
    return forecast

#
# Model assessment procedure
# 
try:
    forecast = flu_predict(REGION, YEAR, WEEK, f'{folder}ezdrowie-flu-infected.csv', f'{folder}ezdrowie-flu-vaccinated.csv', f'{folder}weather-hourly.csv', 'multiTimeline.csv')
except:
    print('Error while running flu_predict')
    forecast = [0.0]*4
    
df_infected_forecast = pd.read_csv(f'{folder}ezdrowie-flu-forecast-infected.csv')
ground_truth = df_infected_forecast['Liczba przypadków na 100 tys.'].tolist()
years = df_infected_forecast['Rok'].tolist()
weeks = df_infected_forecast['Numer tygodnia'].tolist()

def flu_predict_error(forecast, ground_truth, years, weeks):
    error = 0.0
    for w in range(4):
        e = forecast[w] - ground_truth[w]
        print(f'Forecast for week {weeks[w]:02d} of year {years[w]} error = {e}')
        error = error + abs(e)
    return error

print(f'\nTotal l1 error: {flu_predict_error(forecast, ground_truth, years, weeks)}')


