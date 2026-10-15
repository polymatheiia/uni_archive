"""Parsing + feature helpers shared across labs 11-13.

Handles the two source FASTA formats:
  protein: >ID|['4.55/26669', ...]   or   >id|ACC 8.7 8.7   (pI/mw or bare pI)
  peptide: >... mean exp pI: 4.37
and computes the sequence features used for the ML datasets.
"""

import hashlib
import re

# --- amino-acid constants (from the lab11 README) ---
AA = list("ACDEFGHIKLMNPQRSTVWY")

KD_SCALE = {  # Kyte-Doolittle hydrophobicity
    'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8, 'G': -0.4, 'H': -3.2,
    'I': 4.5, 'K': -3.9, 'L': 3.8, 'M': 1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5,
    'R': -4.5, 'S': -0.8, 'T': -0.7, 'V': 4.2, 'W': -0.9, 'Y': -1.3,
}
MASS = {  # monoisotopic-ish residue masses (Da)
    'D': 115.0886, 'E': 129.1155, 'C': 103.1388, 'Y': 163.1760, 'H': 137.1411,
    'K': 128.1741, 'R': 156.1875, 'M': 131.1926, 'F': 147.1766, 'L': 113.1594,
    'V': 99.1326, 'A': 71.0788, 'G': 57.0519, 'Q': 128.1307, 'N': 114.1038,
    'I': 113.1594, 'W': 186.2132, 'S': 87.0782, 'P': 97.1167, 'T': 101.1051,
}
WATER = 18.01524
POSITIVE = ("K", "R")
NEGATIVE = ("D", "E")

_PIMW = re.compile(r"(\d+\.\d+)\s*/\s*\d+")      # 4.55/26669
_FLOAT = re.compile(r"\d+\.\d+")
_PEP_PI = re.compile(r"mean exp pI:\s*([0-9.]+)")


def _valid_pi(vals):
    return [v for v in vals if 0.0 < v <= 14.0]


def protein_pi(header):
    """Mean pI from a protein header (handles pI/mw brackets and bare floats)."""
    pis = [float(x) for x in _PIMW.findall(header)]
    if not pis:
        pis = _valid_pi(float(x) for x in _FLOAT.findall(header))
    return sum(pis) / len(pis) if pis else None


def peptide_pi(header):
    m = _PEP_PI.search(header)
    return float(m.group(1)) if m else None


def parse_fasta(path, kind):
    """Yield (sequence, pI) for kind in {'protein','peptide'}, skipping comments."""
    pi_of = protein_pi if kind == "protein" else peptide_pi
    header, seq = None, []
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("#") or not line.strip():
                continue
            if line.startswith(">"):
                if header is not None and seq:
                    pi = pi_of(header)
                    if pi is not None:
                        yield "".join(seq), pi
                header, seq = line[1:], []
            else:
                seq.append(line.strip())
    if header is not None and seq:
        pi = pi_of(header)
        if pi is not None:
            yield "".join(seq), pi


def clean_seq(seq):
    return "".join(c for c in seq.upper() if c.isalpha())


def md5_uid(seq):
    return hashlib.md5(seq.encode()).hexdigest()


def features(seq):
    """Return a dict of engineered features for one sequence."""
    seq = clean_seq(seq)
    n = len(seq)
    counts = {f"aa_{a}": seq.count(a) for a in AA}
    mw = sum(MASS.get(c, 0.0) for c in seq) + (WATER if n else 0.0)
    hydro_total = sum(KD_SCALE.get(c, 0.0) for c in seq)
    charge = sum(seq.count(a) for a in POSITIVE) - sum(seq.count(a) for a in NEGATIVE)
    row = {"length": n, "molecular_weight": round(mw, 2)}
    row.update(counts)
    row["hydro_total"] = round(hydro_total, 3)
    row["hydro_mean"] = round(hydro_total / n, 3) if n else 0.0
    row["charge"] = float(charge)
    return row
