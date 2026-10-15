"""lab13 Task 4: inference tool for the acidic/non-acidic classifier.

Reads a FASTA file, scores every sequence with the trained MLP, and writes a new
FASTA whose headers are decorated with the predicted label and probability:

    >protein 1 | acidic 0.729
    LDNAVMENFFGHLKEE...

Usage:
    python acidic_protein_dl_predictor.py -i test.fasta -o test_acidic_pred.fasta
"""

import argparse
import os
import sys

import joblib
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lab11", "scripts"))
import fasta_utils as fu  # noqa: E402

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "acidic_mlp.joblib")
THRESHOLD = 0.5   # balanced dataset -> 0.5 is a reasonable operating point


def read_records(path):
    """Yield (header, sequence) pairs, skipping comment lines."""
    header, seq = None, []
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(seq)
                header, seq = line[1:], []
            else:
                seq.append(line.strip())
    if header is not None:
        yield header, "".join(seq)


def main():
    ap = argparse.ArgumentParser(description="Acidic protein/peptide predictor")
    ap.add_argument("-i", "--input", required=True, help="input FASTA")
    ap.add_argument("-o", "--output", required=True, help="output FASTA with predictions")
    args = ap.parse_args()

    bundle = joblib.load(MODEL_PATH)
    pipe, feats = bundle["pipeline"], bundle["features"]

    records = list(read_records(args.input))
    X = pd.DataFrame([fu.features(seq) for _, seq in records])[feats]
    proba = pipe.predict_proba(X)[:, 1]   # P(acidic)

    with open(args.output, "w") as out:
        for (header, seq), p in zip(records, proba):
            label = "acidic" if p >= THRESHOLD else "non-acidic"
            score = p if label == "acidic" else 1 - p
            out.write(f">{header} | {label} {score:.6f}\n{seq}\n")

    print(f"wrote {len(records)} predictions to {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
