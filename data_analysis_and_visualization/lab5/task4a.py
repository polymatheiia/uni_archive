import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("temperatures_clean.csv")
avg_df = df.groupby(["year", "Country"], as_index=False)["AverageTemperatureCelsius"].mean()
avg_df = avg_df.sort_values("year")

plt.figure(figsize=(10, 6))
plt.plot(avg_df["year"], avg_df["AverageTemperatureCelsius"], color="black", linewidth=1)
plt.xlabel("year")
plt.ylabel("countryAverage")
plt.grid(True)
plt.tight_layout()
plt.savefig("fig7.png", dpi=150)
plt.show()
