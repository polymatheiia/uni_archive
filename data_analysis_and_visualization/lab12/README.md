# Lab 12 — Isoelectric point, part 2 (classical ML)

Uses the feature CSVs from lab11 (`common.py` loads them and **drops `pI`** to avoid
label leakage, since label = pI<5).

| Step | Script | Output |
|------|--------|--------|
| EDA: per-feature histograms + box plots, correlation heatmap, feature/label correlations | `04_eda.py [0/1]` | `images/feature_histograms.png`, `feature_boxplots.png`, `correlation_heatmap.png` |
| Train DecisionTree (depth scan), RandomForest, KNN, SVM-RBF (GridSearchCV) + tree viz | `05_ml_models.py` | `images/model_scores.csv`, `tree_depth_accuracy.png`, `decision_tree.png` |

## Results

Net **charge** is the dominant predictor (r = −0.50 with the acidic label); acidic
residue counts `aa_D`/`aa_E` follow. Held-out test accuracy:

| model | best params | test acc |
|-------|-------------|----------|
| DecisionTree | max_depth=4 | 0.943 |
| RandomForest | 300 trees | 0.939 |
| KNN | k=5 | 0.921 |
| SVM (RBF) | C=10, γ=0.01 | 0.948 |

```bash
python 04_eda.py 1 && python 05_ml_models.py
```
