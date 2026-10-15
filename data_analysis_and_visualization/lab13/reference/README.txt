====================================================================
              ISOELECTRIC POINT & pH OPTIMA
                         PART 3
====================================================================
Source: https://www.mimuw.edu.pl/~lukaskoz/teaching/dav/labs/lab13/
(part 3 of 3; follows ../../lab11/reference/README.txt and
../../lab12/reference/README.txt)

4) ML models building (deep learning)
- install tensorflow & keras (pytorch is also a nice alternative for the backend)
https://keras.io/getting_started/
https://pypi.org/project/keras/
etc.

- train dense model (at least two dense layers, adam, relu/softsign, dropout layers)*

- print the model structure and save in text or image file (screenshot), model.summary()

- calculate scores and save models in json&hdf5 format, model.to_json()

- make prediction/inference script (command-line tool that as an input will take the fasta file and 
extend/decorate the header with non-acidic <score>* / acidic label <score>)

*MLPClassifier & MLPRegressor (for simple, dense models you can even use scikit)
https://scikit-learn.org/stable/api/sklearn.neural_network.html


for instance:
python acidic_protein_dl_predictor.py -i test.fasta -o test_acidic_pred.fasta
python pH_OPTIMA_protein_dl_predictor.py -i test.fasta -o test_optima_pred.fasta

where test.fasta is for instance
>protein 1
LDNAVMENFFGHLKEEDDMYYRRDYRNVEELENAVNEYITYWNQDDEKRIKLSLGGHVEYDRTEEYQQKAG
>UPI00028EB81A status=active
MTGVWQPSPDFRQRAAVWGMALPEPEFTKPAELAAFRDRRRRRR
>AF-A0A782FH33
MWRVRIFFGKRQTCAFWLCVTGTCASTMPISERHRAMKGDSIDVVNGRRLPGYGLCIKNKPV
...

and the test_acidic_pred.fasta is:
>protein 1 | acidic 0.72905566
LDNAVMENFFGHLKEEDDMYYRRDYRNVEELENAVNEYITYWNQDDEKRIKLSLGGHVEYDRTEEYQQKAG
>UPI00028EB81A status=active | non-acidic 0.04302571 
MTGVWQPSPDFRQRAAVWGMALPEPEFTKPAELAAFRDRRRRRR
>AF-A0A782FH33 | non-acidic 0.13989039
MWRVRIFFGKRQTCAFWLCVTGTCASTMPISERHRAMKGDSIDVVNGRRLPGYGLCIKNKPV
...

* as we tried to make balanced dataset 0.5 threshold is a good starting point,
but for real case scenari you set this by ROC

====================================================================

GPU vs CPU
For our exercises, it is sufficient to use only CPU, but in real-life scenarios
deep learning training frequently requires a lot of the computing power. 
Thus, the GPU are frequently used, but this is also the tricky part. 

First of all, you need quite powerful GPU cards like:
H100 $300k for a node (8xGPU): https://smicro.pl/nvidia-hgx-h100-640gb-935-24287-0001-000-3
A100 $150k for a node (8xGPU): https://smicro.pl/nvidia-hgx-a100-640gb-935-23587-0000-204-3 

Next, you need to install special (nVidia) drivers supporting deep learning 
(it seems easy to install, but frequently it may lead to serious problems 
including miss-configuration, "dependency hell" or even complete system failure).

====================================================================

Homework:

Make pdf report with all plots and the tables summarizing the parts 1-4 (three last weeks).
If possible, make some conclusions.

Additionally provide all datasets, scripts, separate plot image files like:
    - initial data exploration plots
    - the decision trees visualizations
    - for deep learning provide also json&hdf models
    
All files should be sent until 08.06.2026
via email to lukaskoz@mimuw.edu.pl with the email subject:

'DAV26_labML_hw_Surname_Name' without email text body and with 
'DAV26_labML_hw_Surname_Name.7z' (ASCII letters only) attachment.



