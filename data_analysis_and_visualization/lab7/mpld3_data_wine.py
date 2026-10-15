import sys
import os
import numpy as np
import matplotlib.pyplot as plt

import mpld3
from mpld3 import plugins
from sklearn.datasets import load_wine

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["0", "1"]:
        print("Usage: python mpld3_data_wine.py [0|1]")
        sys.exit(1)

    wine = load_wine()
    X = wine.data
    y = wine.target
    feature_names = wine.feature_names

    X = X + 0.1 * np.random.random(X.shape)

    # we use 4 selected features for a 4x4 scatter matrix
    feature_idx = [0, 1, 5, 6]
    # 0 = alcohol
    # 1 = malic_acid
    # 5 = flavanoids
    # 6 = nonflavanoid_phenols

    fig, ax = plt.subplots(4, 4, sharex="col", sharey="row", figsize=(8, 8))
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95,
                        hspace=0.1, wspace=0.1)

    for i in range(4):
        for j in range(4):
            ax[3 - i, j].scatter(
                X[:, feature_idx[j]],
                X[:, feature_idx[i]],
                c=y,
                s=40,
                alpha=0.6
            )

    # Remove tick labels
    for axi in ax.flat:
        for axis in [axi.xaxis, axi.yaxis]:
            axis.set_major_formatter(plt.NullFormatter())

    # Add feature names on diagonal
    for i in range(4):
        ax[3 - i, i].text(
            0.5, 0.5, feature_names[feature_idx[i]],
            transform=ax[3 - i, i].transAxes,
            ha="center", va="center", fontsize=10
        )

    
    plugins.connect(fig, plugins.LinkedBrush(ax[0, 0].collections[0]))

    if sys.argv[1] == "0":
        mpld3.show()
    else:
        out_file = "mpld3_data_wine.html"
        mpld3.save_html(fig, out_file)
        print(os.path.abspath(out_file))

if __name__ == "__main__":
    main()