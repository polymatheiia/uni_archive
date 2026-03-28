import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("temperatures_clean.csv")

order = sorted(data['country_id'].unique())
grouped = [data.loc[data['country_id'] == c, 'AverageTemperatureCelsius'] for c in order]

plt.figure(figsize=(10, 6))
parts = plt.violinplot(grouped, showmeans=False, showmedians=True, showextrema=True)

plt.xticks(range(1, len(order) + 1), order)
plt.xlabel("country_id")
plt.ylabel("AverageTemperatureCelsius")
plt.tight_layout()
plt.savefig("fig7.png", dpi=150)
plt.show()
