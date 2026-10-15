"""lab11 Task 1b: build a balanced acidic-classification dataset (2200 items).

Composition (label 1 = acidic, pI < 5.0):
  550 protein  positives : proteins with pI < 5
  550 protein  negatives : the 550 most basic proteins (few exceed pI 10)
  550 peptide  positives : random peptides with pI < 5
  550 peptide  negatives : random peptides with pI > 10

Writes IPC_classification_dataset.fasta with headers  >UID|type|pI|label  where
UID is the MD5 of the sequence, then splits 60/20/20 two ways (plain random and
stratified by source type) and reports how each split is composed.

Usage: python 02_build_dataset.py
"""

import os

import numpy as np
import pandas as pd

import fasta_utils as fu

REF = os.path.join(os.path.dirname(__file__), "..", "reference")
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
PROT = os.path.join(REF, "pip_ch2d19_2_1st_isoform_outliers_3units_cleaned_0.99.fasta")
PEP = os.path.join(REF, "Gauci_PHENYX_SEQUEST_0.99_duplicates_out.fasta")
N_PER_GROUP = 550
SEED = 42


def load(path, kind):
    return pd.DataFrame([{"sequence": fu.clean_seq(s), "pI": pi, "data_type": kind}
                         for s, pi in fu.parse_fasta(path, kind)])


def build():
    rng = np.random.default_rng(SEED)
    prot = load(PROT, "protein")
    pep = load(PEP, "peptide")

    prot_pos = prot[prot["pI"] < 5.0].nsmallest(N_PER_GROUP, "pI")
    prot_neg = prot.nlargest(N_PER_GROUP, "pI")            # 550 most basic
    pep_pos = pep[pep["pI"] < 5.0].sample(N_PER_GROUP, random_state=SEED)
    pep_neg = pep[pep["pI"] > 10.0].sample(N_PER_GROUP, random_state=SEED)

    df = pd.concat([prot_pos, prot_neg, pep_pos, pep_neg], ignore_index=True)
    df["label"] = (df["pI"] < 5.0).astype(int)
    df["uid"] = df["sequence"].map(fu.md5_uid)
    df = df.drop_duplicates("uid").reset_index(drop=True)
    return df


def write_fasta(df, path):
    with open(path, "w") as fh:
        for _, r in df.iterrows():
            fh.write(f">{r.uid}|{r.data_type}|{r.pI}|{r.label}\n{r.sequence}\n")


def split_random(df, seed):
    idx = df.sample(frac=1, random_state=seed).index
    n = len(df)
    a, b = int(0.6 * n), int(0.8 * n)
    return df.loc[idx[:a]], df.loc[idx[a:b]], df.loc[idx[b:]]


def split_stratified(df, seed):
    """Split proteins and peptides separately, then merge, for balanced sources."""
    trains, tests, vals = [], [], []
    for _, grp in df.groupby("data_type"):
        tr, te, va = split_random(grp, seed)
        trains.append(tr); tests.append(te); vals.append(va)
    return (pd.concat(trains).sample(frac=1, random_state=seed),
            pd.concat(tests).sample(frac=1, random_state=seed),
            pd.concat(vals).sample(frac=1, random_state=seed))


def describe(name, parts):
    print(f"\n{name} split composition:")
    for label, part in zip(("train", "test", "val"), parts):
        pos = int((part["label"] == 1).sum())
        prot = int((part["data_type"] == "protein").sum())
        print(f"  {label:5s} n={len(part):4d}  positives={pos:4d}  "
              f"proteins={prot:4d}  peptides={len(part) - prot:4d}")


def main():
    os.makedirs(DATA, exist_ok=True)
    df = build()
    print("Built dataset:", len(df), "items;",
          int(df["label"].sum()), "acidic /", int((df.label == 0).sum()), "non-acidic")
    write_fasta(df, os.path.join(DATA, "IPC_classification_dataset.fasta"))
    df.to_csv(os.path.join(DATA, "IPC_classification_dataset.csv"), index=False)

    # Iteration 1: plain random split
    r = split_random(df, SEED)
    describe("Random (iteration 1)", r)

    # Iteration 2: stratified by source, saved as the canonical splits
    s_train, s_test, s_val = split_stratified(df, SEED)
    describe("Stratified by source (iteration 2)", (s_train, s_test, s_val))
    for name, part in [("train", s_train), ("test", s_test), ("val", s_val)]:
        write_fasta(part, os.path.join(DATA, f"IPC_classification_dataset_{name}.fasta"))
        part.to_csv(os.path.join(DATA, f"IPC_classification_dataset_{name}.csv"), index=False)
    print("\nsaved IPC_classification_dataset.fasta and train/test/val splits in ../data/")


if __name__ == "__main__":
    main()
