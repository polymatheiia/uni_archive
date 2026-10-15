"""Build the final ISOELECTRIC POINT report (labs 11-13) as report.pdf.

Aggregates parts 1-4: dataset construction & exploration (lab11), feature analysis
and classical ML models (lab12), and the dense neural network + inference (lab13).
Uses matplotlib PdfPages (no extra dependencies). Run: python make_report.py
"""

import json
import os
import textwrap

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

HERE = os.path.dirname(__file__)
L11_IMG = os.path.join(HERE, "..", "lab11", "images")
L11_DATA = os.path.join(HERE, "..", "lab11", "data")
L12_IMG = os.path.join(HERE, "..", "lab12", "images")
MODELS = os.path.join(HERE, "models")
OUT = os.path.join(HERE, "report.pdf")


def iqr_table():
    lines = []
    for name, f in [("IPC_protein", "protein_parsed.csv"),
                    ("IPC_peptide", "peptide_parsed.csv")]:
        df = pd.read_csv(os.path.join(L11_DATA, f))
        for col in ("pI", "length"):
            q1, q3 = np.percentile(df[col], [25, 75])
            lines.append(f"{name:12s} {col:7s} Q1={q1:8.2f}  Q3={q3:8.2f}  IQR={q3 - q1:8.2f}")
    return "\n".join(lines)


def text_page(pdf, title, body, subtitle=None, mono=False):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.text(0.5, 0.93, title, ha="center", fontsize=20, fontweight="bold")
    if subtitle:
        fig.text(0.5, 0.88, subtitle, ha="center", fontsize=12, style="italic")
    family = "monospace" if mono else None
    fig.text(0.08, 0.83, body, ha="left", va="top", fontsize=9.5, family=family)
    plt.axis("off")
    pdf.savefig(fig)
    plt.close(fig)


def image_page(pdf, title, images, captions):
    n = len(images)
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.text(0.5, 0.96, title, ha="center", fontsize=15, fontweight="bold")
    for k, (img, cap) in enumerate(zip(images, captions)):
        ax = fig.add_subplot(n, 1, k + 1)
        if os.path.exists(img):
            ax.imshow(mpimg.imread(img))
        ax.axis("off")
        ax.set_title(cap, fontsize=9)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    pdf.savefig(fig)
    plt.close(fig)


def main():
    scores = pd.read_csv(os.path.join(L12_IMG, "model_scores.csv"))
    arch = json.load(open(os.path.join(MODELS, "acidic_mlp.json")))

    with PdfPages(OUT) as pdf:
        text_page(
            pdf, "Isoelectric Point — is a protein acidic?",
            textwrap.fill(
                "Binary classification of proteins and peptides into acidic (pI < 5, "
                "label 1) and non-acidic (label 0). This report covers the four parts "
                "of the project: building a balanced dataset from the IPC protein and "
                "peptide FASTA files, engineering sequence features, exploring them, "
                "training classical ML models, and finally a dense neural network with "
                "a command-line inference tool.", 92),
            subtitle="Data Analysis & Visualization — labs 11-13")

        # Part 1
        text_page(
            pdf, "Part 1 — Dataset & exploration",
            "Parsed sources:  proteins = 2183,  peptides = 16882\n\n"
            "Balanced classification dataset (2200 items, 1100 acidic / 1100 non-acidic):\n"
            "  550 protein positives  (pI < 5)\n"
            "  550 protein negatives  (the 550 most basic proteins)\n"
            "  550 peptide positives  (random, pI < 5)\n"
            "  550 peptide negatives  (random, pI > 10)\n\n"
            "UID = MD5(sequence). Header format:  >UID|type|pI|label\n"
            "Split 60/20/20 two ways: plain random, and stratified by source type.\n"
            "The stratified split keeps proteins/peptides balanced across train/test/val.\n\n"
            "Interquartile ranges:\n" + iqr_table(),
            mono=True)
        image_page(pdf, "Part 1 — pI & length distributions",
                   [os.path.join(L11_IMG, "IPC_protein_pI_histogram.png"),
                    os.path.join(L11_IMG, "IPC_peptide_pI_histogram.png")],
                   ["Protein pI (Q1/Q3 marked)", "Peptide pI (Q1/Q3 marked)"])
        image_page(pdf, "Part 1 — sequence length distributions",
                   [os.path.join(L11_IMG, "IPC_protein_length_histogram.png"),
                    os.path.join(L11_IMG, "IPC_peptide_length_histogram.png")],
                   ["Protein length", "Peptide length"])

        # Part 2
        model_txt = scores.to_string(index=False)
        text_page(
            pdf, "Part 2 — Features & classical models",
            "Features (sequence-derived only; pI is excluded to avoid label leakage):\n"
            "  length, molecular_weight, 20 amino-acid counts, hydrophobicity\n"
            "  (Kyte-Doolittle total & mean), net charge.\n\n"
            "The strongest single predictor is net charge (Pearson r = -0.50 with the\n"
            "acidic label): acidic sequences carry more D/E and fewer K/R. The acidic\n"
            "residue counts aa_D and aa_E are the next most informative.\n\n"
            "Held-out test accuracy:\n\n" + model_txt,
            mono=True)
        image_page(pdf, "Part 2 — feature correlations & tree tuning",
                   [os.path.join(L12_IMG, "correlation_heatmap.png"),
                    os.path.join(L12_IMG, "tree_depth_accuracy.png")],
                   ["Feature correlation matrix", "Decision-tree accuracy vs depth"])
        image_page(pdf, "Part 2 — decision tree (max_depth = 4)",
                   [os.path.join(L12_IMG, "decision_tree.png")],
                   ["Charge and the acidic-residue counts dominate the top splits"])

        # Parts 3-4
        layer_txt = "\n".join(
            f"  layer {i+1}: {s[0]} -> {s[1]}" for i, s in enumerate(arch["layer_shapes"]))
        text_page(
            pdf, "Parts 3-4 — Dense neural network & inference",
            "Model: scikit-learn MLPClassifier (dense), relu + adam, L2 alpha=1e-3,\n"
            "early stopping (dropout-style regularisation).\n\n"
            f"Architecture (in -> hidden -> hidden -> out):\n{layer_txt}\n\n"
            f"Converged in {arch['n_iter']} iterations.\n"
            f"Test accuracy: {arch['test_accuracy']}\n\n"
            "Saved in three formats: acidic_mlp.joblib (full pipeline),\n"
            "acidic_mlp.json (architecture summary), acidic_mlp_weights.npz (weights).\n\n"
            "Inference tool (acidic_protein_dl_predictor.py) decorates FASTA headers:\n"
            "  >protein 1 | acidic 0.917\n"
            "  >UPI00028EB81A status=active | non-acidic 0.909\n"
            "  >AF-A0A782FH33 | non-acidic 0.944\n\n"
            "Conclusion: all models reach ~92-95% accuracy on this balanced task;\n"
            "the SVM (RBF) and decision tree lead marginally. Net charge and acidic\n"
            "residue composition carry most of the signal, which matches the biochemistry\n"
            "of the isoelectric point.",
            mono=True)

    print(os.path.abspath(OUT))


if __name__ == "__main__":
    main()
