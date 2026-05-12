import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("temperatures_clean.csv")
avg_df = df.groupby(["year", "Country"], as_index=False)["AverageTemperatureCelsius"].mean()

plt.figure(figsize=(10, 6))

countries = avg_df["Country"].unique()
colors = plt.cm.tab10.colors

for i, country in enumerate(countries):
    subset = avg_df[avg_df["Country"] == country]
    plt.plot(
        subset["year"],
        subset["AverageTemperatureCelsius"],
        color=colors[i % len(colors)],
        linewidth=1,
        label=country
    )

plt.xlabel("year")
plt.ylabel("countryAverage")
plt.title("Average Temperature per Year by Country")
plt.grid(True)
plt.legend(title="Country")
plt.tight_layout()
plt.savefig("fig9.png", dpi=150)
plt.show()
