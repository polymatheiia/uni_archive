"""lab12 Tasks 2-3: train and compare classifiers for the acidic/non-acidic task.

Models: DecisionTree (scanning max_depth), RandomForest, K-Nearest Neighbors and
SVM (RBF kernel, tuned with GridSearchCV). Reports accuracy on the held-out test
set, saves a scores table, a depth-vs-accuracy curve, and a decision-tree
visualisation. Run: python 05_ml_models.py
"""

import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

import common

IMG = os.path.join(os.path.dirname(__file__), "..", "images")
DATA_OUT = os.path.join(os.path.dirname(__file__), "..", "images")
SEED = 42


def depth_scan(Xtr, ytr, Xte, yte):
    depths = range(1, 16)
    tr, te = [], []
    for d in depths:
        clf = DecisionTreeClassifier(max_depth=d, random_state=SEED).fit(Xtr, ytr)
        tr.append(clf.score(Xtr, ytr))
        te.append(clf.score(Xte, yte))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(list(depths), tr, "o-", label="train")
    ax.plot(list(depths), te, "s-", label="test")
    ax.set_xlabel("max_depth"); ax.set_ylabel("accuracy")
    ax.set_title("Decision tree accuracy vs. depth"); ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout()
    os.makedirs(IMG, exist_ok=True)
    fig.savefig(os.path.join(IMG, "tree_depth_accuracy.png"), dpi=130)
    plt.close(fig)
    best_d = int(list(depths)[int(np.argmax(te))])
    return best_d, te[int(np.argmax(te))]


def viz_tree(Xtr, ytr, feats):
    clf = DecisionTreeClassifier(max_depth=4, random_state=SEED).fit(Xtr, ytr)
    fig, ax = plt.subplots(figsize=(20, 10))
    plot_tree(clf, feature_names=feats, class_names=["non-acidic", "acidic"],
              filled=True, rounded=True, fontsize=8, ax=ax, impurity=False)
    ax.set_title("Decision tree (max_depth=4)", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, "decision_tree.png"), dpi=120)
    plt.close(fig)


def main():
    Xtr, ytr, _ = common.load_split("train")
    Xte, yte, _ = common.load_split("test")
    feats = list(Xtr.columns)
    rows = []

    # Decision tree (depth scan)
    best_d, dt_acc = depth_scan(Xtr, ytr, Xte, yte)
    rows.append(("DecisionTree", f"max_depth={best_d}", dt_acc))
    viz_tree(Xtr, ytr, feats)

    # Random forest (grid search)
    rf = GridSearchCV(
        RandomForestClassifier(random_state=SEED),
        {"n_estimators": [100, 300], "max_depth": [None, 10, 20]},
        cv=5, n_jobs=-1).fit(Xtr, ytr)
    rows.append(("RandomForest", str(rf.best_params_), accuracy_score(yte, rf.predict(Xte))))

    # KNN (scan k) - needs scaling
    knn = GridSearchCV(
        make_pipeline(StandardScaler(), KNeighborsClassifier()),
        {"kneighborsclassifier__n_neighbors": [3, 5, 9, 15, 25]},
        cv=5, n_jobs=-1).fit(Xtr, ytr)
    rows.append(("KNN", str(knn.best_params_), accuracy_score(yte, knn.predict(Xte))))

    # SVM RBF (grid search) - needs scaling
    svm = GridSearchCV(
        make_pipeline(StandardScaler(), SVC(kernel="rbf")),
        {"svc__C": [1, 10, 100], "svc__gamma": ["scale", 0.01, 0.1]},
        cv=5, n_jobs=-1).fit(Xtr, ytr)
    rows.append(("SVM (RBF)", str(svm.best_params_), accuracy_score(yte, svm.predict(Xte))))

    table = pd.DataFrame(rows, columns=["model", "best_params", "test_accuracy"])
    table["test_accuracy"] = table["test_accuracy"].round(4)
    table.to_csv(os.path.join(IMG, "model_scores.csv"), index=False)
    print(table.to_string(index=False))
    print("\nsaved model_scores.csv, tree_depth_accuracy.png, decision_tree.png")


if __name__ == "__main__":
    main()
