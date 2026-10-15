import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("temperatures_clean.csv")
avg_df = df.groupby(["year", "Country"], as_index=False)["AverageTemperatureCelsius"].mean()


plt.figure(figsize=(10, 6))
for country in avg_df["Country"].unique():
    subset = avg_df[avg_df["Country"] == country]
    plt.plot(subset["year"], subset["AverageTemperatureCelsius"], color="black", linewidth=1)

plt.xlabel("year")
plt.ylabel("countryAverage")
plt.title("Average Temperature per Year by Country")
plt.grid(True)
plt.tight_layout()
plt.savefig("fig8.png", dpi=150)
plt.show()
