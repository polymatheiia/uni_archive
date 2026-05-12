import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 16,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

df = pd.read_csv("temperatures_clean.csv")
avg_df = df.groupby(["year", "Country"], as_index=False)["AverageTemperatureCelsius"].mean()
countries = avg_df["Country"].unique()

fig, axes = plt.subplots(3, 3, figsize=(14, 10), sharex=True, sharey=True)
axes = axes.flatten()

for i, country in enumerate(countries):
    ax = axes[i]
    country_df = df[df["Country"] == country]

    cities = country_df["City"].unique()
    colors = plt.cm.tab20.colors

    for j, city in enumerate(cities):
        city_df = country_df[country_df["City"] == city].groupby("year", as_index=False)["AverageTemperatureCelsius"].mean()
        ax.plot(
            city_df["year"],
            city_df["AverageTemperatureCelsius"],
            linewidth=1,
            color=colors[j % len(colors)],
            label=city
        )

    ax.set_title(country, fontsize=13, fontweight="bold")
    ax.grid(True, color="lightgray", linewidth=0.5)
    ax.tick_params(axis="x", rotation=45)

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, title="City", loc="center right", fontsize=10)

fig.suptitle("Average temperature", fontsize=20, fontweight="bold")
fig.supxlabel("Year of observation", fontsize=16)
fig.supylabel("Average temperature", fontsize=16)

for j in range(len(countries), len(axes)):
    axes[j].axis("off")

plt.tight_layout(rect=[0.03, 0.03, 0.85, 0.95])
plt.show()
