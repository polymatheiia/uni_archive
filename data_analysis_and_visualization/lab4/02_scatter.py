import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("temperatures_clean.csv")

plt.figure(figsize=(10, 6))
plt.scatter(data['year'], data['AverageTemperatureCelsius'])
plt.xlabel("year")
plt.ylabel("AverageTemperatureCelsius")
plt.tight_layout()
plt.savefig("fig1.png", dpi=150)
plt.show()
