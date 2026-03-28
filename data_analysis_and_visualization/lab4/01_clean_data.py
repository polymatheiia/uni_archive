import pandas as pd

def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9

data = pd.read_csv("https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab4/temperature.csv")
data = data.dropna(subset=[
    'City',
    'Country',
    'AverageTemperatureFahr',
    'AverageTemperatureUncertaintyFahr'
])
data = data[
    (data['City'].astype(str).str.strip() != '') &
    (data['Country'].astype(str).str.strip() != '')
]
data = data.drop(columns=['day'])
data['AverageTemperatureCelsius'] = fahrenheit_to_celsius(data['AverageTemperatureFahr'])
data['AverageTemperatureUncertaintyCelsius'] = fahrenheit_to_celsius(data['AverageTemperatureUncertaintyFahr'])
data = data.drop(columns=[
    'AverageTemperatureFahr',
    'AverageTemperatureUncertaintyFahr'
])
data.to_csv("./temperatures_clean.csv", index=False)
