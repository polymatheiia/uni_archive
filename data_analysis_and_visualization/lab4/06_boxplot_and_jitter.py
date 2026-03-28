import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("temperatures_clean.csv")

order = sorted(data['country_id'].unique())
grouped = [data.loc[data['country_id'] == c, 'AverageTemperatureCelsius'] for c in order]

plt.figure(figsize=(10, 6))
plt.boxplot(grouped, tick_labels=order)
plt.xlabel("country_id")
plt.ylabel("AverageTemperatureCelsius")
plt.tight_layout()
plt.savefig("fig5.png", dpi=150)
plt.show()

plt.figure(figsize=(10, 6))
plt.boxplot(grouped, tick_labels=order)

for i, c in enumerate(order, start=1):
    y = data.loc[data['country_id'] == c, 'AverageTemperatureCelsius'].values
    x = np.random.normal(i, 0.08, size=len(y))
    plt.scatter(x, y, alpha=0.1, s=20, color='tomato')

plt.xlabel("country_id")
plt.ylabel("AverageTemperatureCelsius")
plt.tight_layout()
plt.savefig("fig6.png", dpi=150)
plt.show()
