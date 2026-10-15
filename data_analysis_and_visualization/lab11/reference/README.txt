====================================================================
                    ISOELECTRIC POINT
====================================================================
Source: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab11/
(part 1 of 3; continues in ../../lab12/reference/README.txt and
../../lab13/reference/README.txt. Dataset files below (fasta/csv/png) are
shared by parts 1 & 2, so they are not duplicated in lab12/reference/.)

General info: https://en.wikipedia.org/wiki/Isoelectric_point

Isoelectric point is the pH at which a molecule carries no net electrical charge or is electrically neutral on average.

TASK 1:
Is the protein acidic (pI below 5)?

Our task is to classify proteins/peptides into acidic (pI < 5) and non-acidic (pI >= 5).

PREPARATION OF THE DATASET
To build an ML model, we need a dataset. Let's use the one used for IPC package construction:
http://isoelectric.org/datasets.html
More info: http://dx.doi.org/10.1186/s13062-016-0159-9

There are two main datasets:
- IPC_peptide (16,882 items)
- IPC_protein (2,324 items)

Download:
- http://isoelectric.org/datasets/Gauci_PHENYX_SEQUEST_0.99_duplicates_out.fasta
- http://isoelectric.org/datasets/pip_ch2d19_2_1st_isoform_outliers_3units_cleaned_0.99.fasta

These datasets were preprocessed and cleaned, but we will need to prepare them further.

Since we aim for binary classification, we will label data based on a threshold of pI = 5.0:
- pI < 5 --> acidic (label: 1)
- pI >= 5 --> non-acidic (label: 0)

a) First, analyze the dataset contents:
- Open both files and check their format.
- Create histograms based on average pI and sequence length.
- Calculate IQR (interquartile range) for both.

See example plots:
- IPC_protein: pI and length
- IPC_peptide: pI and length

https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab11/IPC_protein_pI_histogram.png
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab11/IPC_protein_len_histogram.png
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab11/IPC_peptide_pI_histogram.png
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab11/IPC_peptide_len_histogram.png

Note: The datasets differ in size and sequence length distribution.

b) Count how many proteins/peptides have pI < 5.0.

Let's create a dataset of acidic proteins and peptides:
- From the protein dataset, take all proteins with pI < 5.0 (e.g. 550 items --> positives, label 1).
- Then, take up to 550 most basic peptides with pI > 10* (negatives, label 0), for proteins sort and take 550 the most basic ones

*adjust untill you have enough cases

For the larger peptide dataset:
- Extract all peptides with pI < 5.0 and those with pI > 10.
- Randomly select 550 from each group (550 positives and 550 negatives).

Finally, merge the protein and peptide records into one dataset of 2200 items.

Format:
>UID|peptide/protein|pI|1/0
sequence

Use MD5 hash of the sequence as UID:

python
import hashlib
sequence = "YDNSLTVVSNASCTTNCLAPLAK"
res = hashlib.md5(sequence.encode())
MD5_hash_uid = res.hexdigest()
print(MD5_hash_uid)
# Output: ec22b6bb20f548f06b81a1a0760d78d6

Save as: IPC_classification_dataset_100.fasta

Now split the data into training, testing, and validation sets (60/20/20):

First iteration:
- Randomly split the data. Count how many items in each split come from proteins/peptides and how many are positives/negatives.

Due to dataset size, proportions may slightly vary.

Second iteration:
- To ensure balanced source types, split proteins and peptides separately, then randomly divide and merge the splits.

Compare the distributions between the two methods.

Save the splits:
    IPC_classification_dataset_60_train.fasta
    IPC_classification_dataset_20_test.fasta
    IPC_classification_dataset_20_val.fasta

Now, having these files, we can think about some features that can be engineered from the sequences for our task. Some obvious ones include:
- the protein/peptide sequence itself
- the number of amino acids of a given type
- overall charge at neutral pH

Additional useful features might be:
- sequence length
- amino acid composition (relative frequency or raw count of each residue)
- fraction of acidic residues (e.g., D, E)
- fraction of basic residues (e.g., K, R, H)
- hydrophobicity score (e.g., using Kyte-Doolittle scale)
- aromaticity (presence of F, Y, W)
- molecular weight
- charge
- aliphatic index
- instability index
- presence of specific motifs (e.g., dipeptides or tripeptides)
- sequence entropy or complexity

Make csv files for IPC_classification_dataset that will have some of those features included.

Recommended Features:
Feature Name        Type        Description
seq_length          Integer     Total number of amino acids
mw                  Float       Molecular weight (Da)
avg_hydrophobicity  Float       Mean hydrophobicity (e.g., Kyte-Doolittle)
count_A,            Float       Count/Fraction of Ala
...,                Float       Count/Fraction of other amino acids
count_Y             Float       Count/Fraction of Tyr
num_acidic          Intege      Count of D and E residues
num_basic           Integer     Count of K, R, H residues
aromaticity         Float       Proportion of F, Y, W residues
aliphatic_index     Float       Relative volume occupied by aliphatic side chains (A, V, I, L)
instability_index   Float       Predicted stability (lower = more stable)
charge              Float       Charge
label_acidic        0/1         Classification label: 1 if pI < 5.0, else 0 (for binary classification task)

Output Format (CSV Example)
uid,seq_length,mw,avg_hydrophobicity,fraction_A,...,charge_at_pH7,charge,label_acidic
ec22b6bb,23,2400.1,0.12,0.13,...,-1.25,4.82,1
abcd1234,95,10840.3,-0.05,0.06,...,+0.75,9.71,0

Example:
https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab11/IPC_classification_dataset_sample.csv

========================================================================================================

Some usefull information:

aa_letters = ['A', 'C', 'D', 'E', 'F', 
              'G', 'H', 'I', 'K', 'L', 
              'M', 'N', 'P', 'Q', 'R', 
              'S', 'T', 'V', 'W', 'Y', 'X', '0']
#X - unknown 0-padding


'''Hydrophobicity: Kyte-Doolittle scale'''
kd_scale = {
        'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8,
        'G': -0.4, 'H': -3.2, 'I': 4.5, 'K': -3.9, 'L': 3.8,
        'M': 1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5, 'R': -4.5,
        'S': -0.8, 'T': -0.7, 'V': 4.2, 'W': -0.9, 'Y': -1.3
    }
    
    
"""molecular weight"""
massDict = {'D':115.0886, 'E': 129.1155, 'C': 103.1388, 'Y':163.1760, 'H':137.1411, 
           'K':128.1741, 'R': 156.1875,  'M': 131.1926, 'F':147.1766, 'L':113.1594,
           'V':99.1326,  'A':  71.0788,  'G':  57.0519, 'Q':128.1307, 'N':114.1038, 
           'I':113.1594, 'W': 186.2132,  'S':  87.0782, 'P': 97.1167, 'T':101.1051, 
           'U':141.05,   'h2o':18.01524, 'X':        0, 'Z':128.6231, 'O':255.31, 
           'B':114.5962, 'J': 113.1594,}
           
positive_aa = ['K', 'R']    #1
negative_aa = ['D', 'E']    #-1
aromatic_aa = ['F', 'W', 'H', 'Y']

volume =  {'A': 88.6,  'R': 173.4, 'N': 114.1, 'D': 111.1, 
        'C': 108.5, 'E': 138.4, 'Q': 143.8, 'G': 60.1, 
        'H': 153.2, 'I': 166.7, 'L': 166.7, 'K': 168.6, 
        'M': 162.9, 'F': 189.9, 'P': 112.7, 'S': 89.0, 
        'T': 116.1, 'W': 227.8, 'Y': 193.6, 'V': 140.0, 'X':141.26}

vdWalls = {'A':  67.0, 'R': 148.0, 'N':  96.0, 'D':  91.0, 'C': 86.0, 
           'E': 109.0, 'Q': 114.0, 'G':  48.0, 'H': 118.0, 'I': 124.0, 
           'L': 124.0, 'K': 135.0, 'M': 124.0, 'F': 135.0, 'P': 90.0, 
           'S':  73.0, 'T':  93.0, 'W': 163.0, 'Y': 141.0, 'V': 105.0, 'X': 109.2}
           
pKa = {'Cterm': 2.2, 'D': 3.453,  'E': 4.16, 
             'C': 8.3, 'Y': 10.09, 'H': 6.576, 
             'Nterm': 9.2, 'K': 10.66, 'R':  13.231}
             
volume =  {'A': 88.6,  'R': 173.4, 'N': 114.1, 'D': 111.1, 
        'C': 108.5, 'E': 138.4, 'Q': 143.8, 'G': 60.1, 
        'H': 153.2, 'I': 166.7, 'L': 166.7, 'K': 168.6, 
        'M': 162.9, 'F': 189.9, 'P': 112.7, 'S': 89.0, 
        'T': 116.1, 'W': 227.8, 'Y': 193.6, 'V': 140.0, 'X':141.26}

normalized_volume = {'A': 0.1699, 'C': 0.2886, 'D': 0.3041, 'E': 0.4669,
                     'F': 0.774,  'G': 0.0,    'H': 0.5552, 'I': 0.6357,
                     'K': 0.647,  'L': 0.6357, 'M': 0.613,  'N': 0.322,
                     'P': 0.3137, 'Q': 0.4991, 'R': 0.6756, 'S': 0.1723,
                     'T': 0.3339, 'V': 0.4764, 'W': 1.0, 'X': 0.484,  'Y': 0.7961}    
                     

More features: 
https://www.genome.jp/aaindex/       


#HOMEWORK
Today, we started to create the dataset for the classification task. Let's make another dataset for regression task.

We will work on the problem of predicting enzyme pH optima and the dataset we use will be:
"Predicting Enzyme pH Optima from Structure Using Equivariant Graph Neural Networks"
 https://doi.org/10.64898/2026.01.18.700076
 
 The task for the homework is to download protein sequences (not structures) for train set (9168 items) and test set (2284 items).
 
 Hints: 
 - find in the preprint the datasets location
 - download datasets (at this point you should notice that the are no sequences there, only UIDs from UniProt)
 - write script that will download the sequences based on UIDs 
       (e.g. https://rest.uniprot.org/uniprotkb/A0A0H3AFW5.fasta)
 
 As we will work again with similar problem ("pH bound"), you can use previous script to make CSV encoding features.
