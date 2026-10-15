"""lab11 Task 1b (features): encode each dataset split as a feature CSV.

Columns match the course sample (IPC_classification_dataset_sample.csv):
  uid, data_type, pI, length, molecular_weight, aa_A..aa_Y (counts),
  hydro_total, hydro_mean, charge, label

Reads the FASTA splits written by 02_build_dataset.py and writes one CSV per split
plus a combined IPC_features.csv. Run: python 03_features.py
"""

import os

import pandas as pd

import fasta_utils as fu

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


def read_split_fasta(path):
    """Read >UID|type|pI|label headers written by the builder."""
    rows = []
    header, seq = None, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header:
                    rows.append((header, "".join(seq)))
                header, seq = line[1:], []
            else:
                seq.append(line)
    if header:
        rows.append((header, "".join(seq)))
    out = []
    for h, s in rows:
        uid, dtype, pi, label = h.split("|")
        out.append((uid, dtype, float(pi), int(label), s))
    return out


def encode(entries):
    rows = []
    for uid, dtype, pi, label, seq in entries:
        row = {"uid": uid, "data_type": dtype, "pI": pi}
        row.update(fu.features(seq))
        row["label"] = label
        rows.append(row)
    cols = (["uid", "data_type", "pI", "length", "molecular_weight"]
            + [f"aa_{a}" for a in fu.AA]
            + ["hydro_total", "hydro_mean", "charge", "label"])
    return pd.DataFrame(rows)[cols]


def main():
    combined = []
    for name in ("train", "test", "val"):
        fasta = os.path.join(DATA, f"IPC_classification_dataset_{name}.fasta")
        df = encode(read_split_fasta(fasta))
        df.to_csv(os.path.join(DATA, f"IPC_features_{name}.csv"), index=False)
        combined.append(df)
        print(f"{name}: {len(df)} rows -> IPC_features_{name}.csv")
    alldf = pd.concat(combined, ignore_index=True)
    alldf.to_csv(os.path.join(DATA, "IPC_features.csv"), index=False)
    print(f"combined: {len(alldf)} rows -> IPC_features.csv")


if __name__ == "__main__":
    main()
