import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("temperatures_clean.csv")
avg_df = df.groupby(["year", "Country"], as_index=False)["AverageTemperatureCelsius"].mean()
countries = avg_df["Country"].unique()

fig, axes = plt.subplots(3, 3, figsize=(16, 11), sharex=True, sharey=True)
axes = axes.flatten()

all_handles = []
all_labels = []

for i, country in enumerate(countries):
    ax = axes[i]
    country_df = df[df["Country"] == country].copy()

    cities = sorted(country_df["City"].dropna().unique())
    cmap = plt.cm.tab20

    for j, city in enumerate(cities):
        city_df = country_df[country_df["City"] == city].copy()

        city_avg = (
            city_df.groupby("year", as_index=False)["AverageTemperatureCelsius"]
            .mean()
            .sort_values("year")
        )

        line, = ax.plot(
            city_avg["year"],
            city_avg["AverageTemperatureCelsius"],
            color=cmap(j % 20),
            linewidth=1
        )

        if i == 0:
            all_handles.append(line)
            all_labels.append(city)

    ax.set_title(country, fontsize=13)
    ax.grid(True, alpha=0.4)

for k in range(len(countries), len(axes)):
    axes[k].axis("off")

fig.legend(all_handles, all_labels, title="City", loc="center right")
fig.suptitle("Average temperature", fontsize=18)
fig.supxlabel("year", fontsize=14)
fig.supylabel("Average temperature", fontsize=14)

plt.tight_layout(rect=[0.03, 0.03, 0.85, 0.95])
plt.show()
