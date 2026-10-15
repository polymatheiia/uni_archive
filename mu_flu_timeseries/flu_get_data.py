import pandas as pd
import requests
from datetime import datetime, timedelta

### problem data settings

REGION = "śląskie"
YEAR = 2026
WEEK = 4

### helpers

folder = 'Data/'
folder = ''

wojewodztwa = {
    "dolnośląskie": "Wrocław",
    "kujawsko-pomorskie": "Toruń",
    "lubelskie": "Lublin",
    "lubuskie": "Zielona Góra",
    "łódzkie": "Łódź",
    "małopolskie": "Kraków",
    "mazowieckie": "Warszawa",
    "opolskie": "Opole",
    "pomorskie": "Gdańsk",
    "śląskie": "Katowice",
    "świętokrzyskie": "Kielce",
    "warmińsko-mazurskie": "Olsztyn",
    "wielkopolskie": "Poznań",
    "zachodniopomorskie": "Szczecin",
}

def city_lon_lat(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=pl&format=json"
    response = requests.get(url).json()
    lat = response['results'][0]['latitude']
    lon = response['results'][0]['longitude']
    return lat, lon

def find_weeks(year, week, nofweeks=4):
    first_monday = datetime.strptime(f'{year}-W{week}-1', "%G-W%V-%u")
    mondays = [first_monday + timedelta(days=7 * i) for i in range(nofweeks)]
    last_sunday = (mondays[-1] + timedelta(days=6))
    return [m.isocalendar()[0:2] for m in mondays], first_monday, last_sunday

def find_months(dt, nofmonths=4):
    y, m, _ = dt.year, dt.month, dt.day
    months = [(y,m)]
    for _ in range(nofmonths-1):
        m = m-1
        if m == 0:
            m = 12
            y = y-1
        months.insert(0,(y,m))
    return months

### set up historical data

weeks, start, end = find_weeks(YEAR, WEEK, nofweeks=4)
months = find_months(start, nofmonths=4)

### set up ground truth data for forecast validation

weeks_tmp, _ , _  = find_weeks(YEAR, WEEK, nofweeks=6)
weeks_forecast, start_forecast, _  = find_weeks(weeks_tmp[-1][0], weeks_tmp[-1][1], nofweeks=4)
months_forecast = find_months(start_forecast, nofmonths=4)

print('='*24)
print(f'Problem statement: {REGION = }, {YEAR = }, {WEEK = }\n')
print(f'\tTimespan for e-zdrowie historical data infected:\n\t\t{weeks = }')
print(f'\tTimespan for e-zdrowie historical data vaccinated:\n\t\t{months = }')
print(f'\tTimespan for open-meteo historical data:\n\t\t{start.strftime('%Y-%m-%d')} {end.strftime('%Y-%m-%d')}')
print(f'\tCity for open-meteo historical data:\n\t\t{wojewodztwa[REGION]}')
print(f'\n\tTimespan for e-zdrowie infected forecast data\n\t\t{weeks_forecast = }')
print('='*24)

def get_weather_data(region, start, end):
    city = wojewodztwa[region]
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    filename = f'{folder}weather-hourly'
    lat, lon = city_lon_lat(city)
    OPENMETEO = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}"
    url_hourly = f"{OPENMETEO}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code&timezone=auto&format=csv"
    print(f'Downloading open-meteo data for {region}')
    print(f'\t{city} ({lon=} {lat=}) | {start_date} - {end_date}')
    df_hourly = pd.read_csv(url_hourly, skiprows=3)
    print(f'\tSaving to {filename}')
    df_hourly.to_csv(f'{filename}.csv', index=False, encoding='utf-8')
    print('Done.')
    return df_hourly

df_hourly = get_weather_data(REGION, start, end)

print('Downloading e-zdrowie data...')
url = 'https://ezdrowie.gov.pl/pobierz/14553'
sheets  = pd.read_excel(url, sheet_name=["Tabela 3", "Tabela 5"], skiprows=5)

def get_flu_data(sheets, REGION, weeks, months, filename):
    print('Selecting e-zdrowie data to work with...')
    df_infected, df_vaccinated = sheets.values()
    
    #
    # select from infected table
    #
    df_infected =  df_infected[ (df_infected["Województwo"]==REGION.upper()) & (df_infected["Choroba"] == "Grypa") ]
    df_vaccinated =  df_vaccinated[ (df_vaccinated["Województwo"]==REGION.upper()) & (df_vaccinated["Choroba"] == "Grypa") ]
    
    select_time = (df_infected["Rok"]==weeks[0][0]) & (df_infected["Numer tygodnia"] == weeks[0][1])
    for (y, w) in weeks:
        select_time = select_time | ((df_infected["Rok"]==y) & (df_infected["Numer tygodnia"] == w))
    df_infected =  df_infected[ select_time ]
    
    #
    # select from vaccinated table
    #
    start_month =  f"{months[0][0]}-{months[0][1]:02d}-01"
    end_month =  f"{months[-1][0]}-{months[-1][1]:02d}-01"
    select_time = (df_vaccinated["Miesiąc"] >= start_month) & (df_vaccinated["Miesiąc"] <= end_month)
    df_vaccinated =  df_vaccinated[ select_time ]
    
    #
    # save both dataframes to Excel and CSV formats
    #
    print(f'\tSaving to {filename}')
    df_infected.to_csv(f'{filename}-infected.csv', index=False, encoding='utf-8')
    df_vaccinated.to_csv(f'{filename}-vaccinated.csv', index=False, encoding='utf-8')
    print('Done.')
    
    return df_infected, df_vaccinated

filename = f'{folder}ezdrowie-flu'
df_infected, df_vaccinated = get_flu_data(sheets, REGION, weeks, months, filename)
df_infected_forecast, df_vaccinated_forecast = get_flu_data(sheets, REGION, weeks_forecast, months_forecast, f'{filename}-forecast')

print(df_infected.head())
