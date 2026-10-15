# Lab 11 — Isoelectric point, part 1 (dataset)

Build a balanced dataset for classifying proteins/peptides as **acidic (pI < 5)**.

| Step | Script | Output |
|------|--------|--------|
| 1a. Parse FASTA, pI/length histograms + IQR | `01_explore.py [0/1]` | `data/{protein,peptide}_parsed.csv`, `images/IPC_*_histogram.png` |
| 1b. Build balanced 2200-item dataset + 60/20/20 splits | `02_build_dataset.py` | `data/IPC_classification_dataset*.fasta`, train/test/val splits |
| 1b. Feature CSVs (uid, type, pI, length, MW, aa counts, hydrophobicity, charge, label) | `03_features.py` | `data/IPC_features*.csv` |

`fasta_utils.py` holds the FASTA parsers (protein `pI/mw` brackets, peptide
`mean exp pI:`), the MD5 UID, and the feature encoder.

Dataset: 1100 acidic / 1100 non-acidic = 550 protein positives (pI<5) + 550 most
basic proteins + 550 random peptides pI<5 + 550 random peptides pI>10. The
stratified split keeps proteins/peptides balanced (660/660 train, 220/220 test/val).

```bash
python 01_explore.py 1 && python 02_build_dataset.py && python 03_features.py
```
