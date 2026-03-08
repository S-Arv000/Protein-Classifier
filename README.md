# Protein Classifier

Small, personal binary classification model, built to evaluate membrane vs. non-membrane proteins

## Overview

Contains scripts to train an develop a model to classify membrane vs. non-membrane proteins.
Scripts pull data from uniprot, builds dataset train and evaluate a model, then generate predictions on sequences. All protein data in FASTA format

^^ Currently trained on 100 Seqs 

## Repos

Data: Stores raw input files (sequences, positive/negative sequences)
Models: saved models and checkpoints
src: core scripts
    01_Uniprot_Data: Fetch Uniprot data and sequences
    02_Dataset: Preprocessing and constructs dataset 
    03_train_Eval: model training and evaluations to base predictions
    04_Predictions: generate predictions from inputs (see "Data")
    FASTA_Reader, Feature_quantifier: Helper modules


## Startup

1.Create environment and install packages, dependencies, etc.  
    skikit-learn, numpy, pandas

2.Run Pipeline in order:  
    01_Uniprot_Data  
    02_Dataset  
    03_Train_Eval  
    04_Predictions  


## Outputs

Saved model joblib  
Metrics JSON  
Report & plots: ROC, PR, confusion matrix  
Output CSV: sequence id, probability, predicted label +ve(1) or -ve(0)


## Data

Extract data directly from Uniprot, changing seq_limit for amount of data  
OR  
Place input files in data/raw as positve/negative.fasta for training  
  
Include input file wanting to predict, save as "input_fasta" and add realtiveb path to 04, get Output CSV of predictions


## Things to do maybe

Better split, baseline, feature expansion, model upgrades  

If im feeling it; Structure prediction, functino prediction, 
identify localization  

will see





