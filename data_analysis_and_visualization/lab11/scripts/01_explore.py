"""lab11 Task 1a: explore the protein and peptide datasets.

Parses both FASTA files, saves the parsed (sequence, pI, length) tables, draws pI
and length histograms for each dataset, and reports the interquartile range (IQR)
of pI and length.

Usage:
    python 01_explore.py 0   # show the histograms
    python 01_explore.py 1   # save histogram PNGs + parsed CSVs and print paths
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import fasta_utils as fu

REF = os.path.join(os.path.dirname(__file__), "..", "reference")
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
IMG = os.path.join(os.path.dirname(__file__), "..", "images")
PROT = os.path.join(REF, "pip_ch2d19_2_1st_isoform_outliers_3units_cleaned_0.99.fasta")
PEP = os.path.join(REF, "Gauci_PHENYX_SEQUEST_0.99_duplicates_out.fasta")


def parse_to_df(path, kind):
    rows = [{"sequence": s, "pI": pi, "length": len(fu.clean_seq(s)), "data_type": kind}
            for s, pi in fu.parse_fasta(path, kind)]
    return pd.DataFrame(rows)


def iqr(x):
    q1, q3 = np.percentile(x, [25, 75])
    return q1, q3, q3 - q1


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("0", "1"):
        print("Usage: python 01_explore.py [0|1]")
        sys.exit(1)
    mode = sys.argv[1]

    prot = parse_to_df(PROT, "protein")
    pep = parse_to_df(PEP, "peptide")

    if mode == "1":
        os.makedirs(DATA, exist_ok=True)
        prot.to_csv(os.path.join(DATA, "protein_parsed.csv"), index=False)
        pep.to_csv(os.path.join(DATA, "peptide_parsed.csv"), index=False)

    print("Dataset sizes:  proteins =", len(prot), " peptides =", len(pep))
    for name, df in [("IPC_protein", prot), ("IPC_peptide", pep)]:
        for col in ("pI", "length"):
            q1, q3, r = iqr(df[col])
            print(f"  {name:12s} {col:7s} IQR: Q1={q1:.2f} Q3={q3:.2f} IQR={r:.2f}")

    os.makedirs(IMG, exist_ok=True)
    specs = [("IPC_protein", prot, "pI"), ("IPC_protein", prot, "length"),
             ("IPC_peptide", pep, "pI"), ("IPC_peptide", pep, "length")]
    for name, df, col in specs:
        plt.figure(figsize=(7, 4.5))
        plt.hist(df[col], bins=40, color="#4477aa", edgecolor="white")
        q1, q3, r = iqr(df[col])
        plt.axvline(q1, color="red", ls="--", lw=1, label=f"Q1={q1:.1f}")
        plt.axvline(q3, color="red", ls="--", lw=1, label=f"Q3={q3:.1f} (IQR={r:.1f})")
        plt.xlabel(col + (" (isoelectric point)" if col == "pI" else " (residues)"))
        plt.ylabel("count")
        plt.title(f"{name} — {col} distribution")
        plt.legend()
        plt.tight_layout()
        if mode == "0":
            plt.show()
        else:
            out = os.path.join(IMG, f"{name}_{col}_histogram.png")
            plt.savefig(out, dpi=130)
            plt.close()
            print(os.path.abspath(out))


if __name__ == "__main__":
    main()
