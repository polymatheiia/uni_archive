"""lab13 Task 4: train a dense neural-network classifier (scikit MLPClassifier).

A two-hidden-layer dense network (relu, adam, L2 regularisation + early stopping as
the dropout-style regulariser). Prints the layer structure, evaluates on the test
split, and saves the model three ways:
  acidic_mlp.joblib   - full fitted pipeline (used by the predictor)
  acidic_mlp.json     - architecture/summary (model.to_json() equivalent)
  acidic_mlp_weights.npz - layer weights + biases (hdf5-style binary artifact)

Run: python 06_train_mlp.py
"""

import json
import os
import sys

import numpy as np
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lab12", "scripts"))
import common  # noqa: E402

MODELS = os.path.join(os.path.dirname(__file__), "..", "models")
HIDDEN = (64, 32)
SEED = 42


def main():
    Xtr, ytr, _ = common.load_split("train")
    Xte, yte, _ = common.load_split("test")
    feats = list(Xtr.columns)

    pipe = make_pipeline(
        StandardScaler(),
        MLPClassifier(hidden_layer_sizes=HIDDEN, activation="relu", solver="adam",
                      alpha=1e-3, early_stopping=True, max_iter=500, random_state=SEED),
    )
    pipe.fit(Xtr, ytr)
    mlp = pipe.named_steps["mlpclassifier"]

    # print a keras-style summary
    sizes = [len(feats)] + list(HIDDEN) + [1]
    print("Dense MLP architecture:")
    total = 0
    for i in range(len(sizes) - 1):
        params = sizes[i] * sizes[i + 1] + sizes[i + 1]
        total += params
        kind = "output" if i == len(sizes) - 2 else "hidden"
        print(f"  layer {i + 1} ({kind}): {sizes[i]:3d} -> {sizes[i + 1]:3d}   params={params}")
    print(f"  total trainable params: {total}   (converged in {mlp.n_iter_} iterations)")

    acc = accuracy_score(yte, pipe.predict(Xte))
    print(f"\nTest accuracy: {acc:.4f}\n")
    print(classification_report(yte, pipe.predict(Xte), target_names=["non-acidic", "acidic"]))

    os.makedirs(MODELS, exist_ok=True)
    joblib.dump({"pipeline": pipe, "features": feats}, os.path.join(MODELS, "acidic_mlp.joblib"))

    arch = {
        "type": "MLPClassifier", "hidden_layer_sizes": list(HIDDEN),
        "activation": "relu", "solver": "adam", "alpha": 1e-3,
        "n_features": len(feats), "features": feats, "classes": [0, 1],
        "n_iter": int(mlp.n_iter_), "test_accuracy": round(float(acc), 4),
        "layer_shapes": [list(c.shape) for c in mlp.coefs_],
    }
    with open(os.path.join(MODELS, "acidic_mlp.json"), "w") as f:
        json.dump(arch, f, indent=2)

    weights = {}
    for i, (c, b) in enumerate(zip(mlp.coefs_, mlp.intercepts_)):
        weights[f"W{i}"] = c
        weights[f"b{i}"] = b
    np.savez(os.path.join(MODELS, "acidic_mlp_weights.npz"), **weights)

    print("saved acidic_mlp.joblib, acidic_mlp.json, acidic_mlp_weights.npz")


if __name__ == "__main__":
    main()
