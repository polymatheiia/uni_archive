====================================================================
              ISOELECTRIC POINT & pH OPTIMA
                         PART 2
====================================================================
Source: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab12/
(part 2 of 3; datasets are shared with ../../lab11/reference/, continues in
../../lab13/reference/README.txt)

Having some features like:
Feature Name        Type        Description
seq_length          Integer     Total number of amino acids
mw                  Float       Molecular weight (Da)
avg_hydrophobicity  Float       Mean hydrophobicity (e.g., Kyte-Doolittle)
fraction_A, ..., fraction_Y Float Fraction of each of the 20 amino acids
num_acidic          Intege      Count of D and E residues
num_basic           Integer     Count of K, R, H residues
aromaticity         Float       Proportion of F, Y, W residues
aliphatic_index     Float       Relative volume occupied by aliphatic side chains (A, V, I, L)
instability_index   Float       Predicted stability (lower = more stable)
charge              Float       Charge
...
label_acidic        0/1         Classification label: 1 if pI < 5.0, else 0 (for binary classification task)

Output Format (CSV Example)
uid,seq_length,mw,avg_hydrophobicity,fraction_A,...,charge,label_acidic
ec22b6bb,23,2400.1,0.12,0.13,...,-1.25,1
abcd1234,95,10840.3,-0.05,0.06,...,+0.75,0

Runs the same script for extraction of features for our regression task

Task 2: 
1) Explore the data:
- make plots regarding each feature 
(e.g. scatter plots, histograms, box plots, heat map, etc.
minimum two types of plots for each feature)
- decide which columns should be used for the prediction 
- calculate the correlation of each feature*

2) We will start with decision trees as the most intuitive 
a) train DecisionTreeClassifier (test the depth parameter)
- calculate the accuracy for different tree structures (e.g. depth, number of features)**
- visualise the trees (use meaningful labels)
b) do the training again using RandomForestClassifier

3) ML models building
a) train Nearest Neighbors
b) train Support Vector Machine (RBF & GridSearchCV)***

In all cases make some scripts and summaries in the form of tables 
(e.g. with scores from different setups)

* Actually before making any ML model when you have your features you should do proper
'feature selection' step to avoid non-informative or/and highly correlated features:
- https://scikit-learn.org/stable/modules/feature_selection.html
- https://scikit-learn.org/stable/modules/unsupervised_reduction.html

** you can use here GridSearchCV 
https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
https://scikit-learn.org/stable/auto_examples/model_selection/plot_randomized_search.html
https://scikit-learn.org/stable/auto_examples/model_selection/plot_successive_halving_heatmap.html

*** Decision trees are not necessary good for regression task, but SVM can be easily moved to SVR
https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html

Thus, make SVR model for our regression task (skip DecisionTrees, NN here)


