import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("temperatures_clean.csv")

plt.figure(figsize=(10, 6))
plt.scatter(
    data['year'],
    data['AverageTemperatureCelsius'],
    marker='.',
    s=20,
    alpha=0.1,
    color='blue'
)
plt.xlabel("year")
plt.ylabel("AverageTemperatureCelsius")
plt.grid(True)
plt.tight_layout()
plt.savefig("fig4.png", dpi=150)
plt.show()
