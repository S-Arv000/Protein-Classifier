# Protein Classifier

Small, personal binary classification, basically first project.  
It works so im happy
## Overview

Contains scripts to train an develop a model to classify transmembrane vs. non-transmembrane proteins
Scripts pull data from uniprot, build a dataset, train, then generate predictions on sequences. All protein data in FASTA format  
  
+(ve) = transmemebrane 

## Repos

data: Stores raw input files (sequences, positive/negative sequences)
models: saved models and checkpoints
src:
    1_uniprot: Fetch Uniprot data and sequences
    2_dataset: Preprocessing and constructs dataset 
    3_training: model training and evaluations
    4_predict: generate predictions
    FASTA_Reader, Feature_quantifier: Helper modules


## Startup

1.Create environment and install packages, dependencies, etc.  
    skikit-learn, numpy, pandas

2.Run Pipeline in order:  
    1_uniprot  
    2_dataset  
    3_Training  
    4_predict  


## Outputs

model joblib  
metrics JSON  
plots: ROC, PR, cfm  
predictions csv: sequence id, probability, predicted label +ve(1) or -ve(0)


## Results
Trained on 500 proteins

Threshold: 0.51  
  
weighted avgs:  
Precision: 0.91148    
Recall: 0.91000  
F1: 0.90992
  
![Confusion Matrix]("reports\cfm.png)  

![Precision Recall]("reports\PRC.png)  

Predictions on input data in reports, 373 proteins








