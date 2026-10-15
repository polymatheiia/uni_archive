# Lab 13 — Isoelectric point, part 3 (deep learning + inference)

Final part of the ML project. Report: **`report.pdf`** (parts 1–4).

| Step | Script | Output |
|------|--------|--------|
| Train dense MLP (2 hidden layers, relu/adam, early stopping) | `scripts/06_train_mlp.py` | `models/acidic_mlp.joblib`, `acidic_mlp.json`, `acidic_mlp_weights.npz` |
| FASTA inference tool (decorates headers with acidic/non-acidic + score) | `scripts/acidic_protein_dl_predictor.py -i in.fasta -o out.fasta` | decorated FASTA |
| Final PDF report (parts 1–4) | `make_report.py` | `report.pdf` |

MLP: 25 → 64 → 32 → 1, 3777 params, **test accuracy 0.934**. Saved three ways
(joblib pipeline, JSON architecture summary, NPZ weights — the `model.to_json()` /
hdf5-style artifacts). Threshold 0.5 (dataset is balanced).

Example (`acidic_protein_dl_predictor.py`):

```
>protein 1 | acidic 0.917
>UPI00028EB81A status=active | non-acidic 0.909
>AF-A0A782FH33 | non-acidic 0.944
```

```bash
python scripts/06_train_mlp.py
python scripts/acidic_protein_dl_predictor.py -i some.fasta -o some_pred.fasta
python make_report.py
```

Note: the homework's optional pH-optima regression track (downloading UniProt
sequences) is not included; the core acidic-classification pipeline is complete.
