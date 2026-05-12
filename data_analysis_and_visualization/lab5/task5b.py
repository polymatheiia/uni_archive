import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("temperatures_clean.csv")
avg_df = df.groupby(["year", "Country"], as_index=False)["AverageTemperatureCelsius"].mean()
countries = avg_df["Country"].unique()

fig, axes = plt.subplots(3, 3, figsize=(14, 10), sharex=True, sharey=True)
axes = axes.flatten()

for i, country in enumerate(countries):
    ax = axes[i]
    country_df = df[df["Country"] == country]

    for city in country_df["City"].unique():
        city_df = country_df[country_df["City"] == city].groupby("year", as_index=False)["AverageTemperatureCelsius"].mean()
        ax.plot(city_df["year"], city_df["AverageTemperatureCelsius"], linewidth=1)

    ax.set_title(country)
    ax.grid(True)

for j in range(len(countries), len(axes)):
    axes[j].axis("off")

fig.suptitle("Average temperature", fontsize=18)
plt.tight_layout()
plt.savefig("fig10.png", dpi=150)
plt.show()
