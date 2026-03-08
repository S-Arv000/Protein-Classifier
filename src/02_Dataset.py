import os
import argparse
import pandas as pd

from FASTA_Reader import read_fasta
from Feature_quantifier import FeatureQuantifier, quantify_features, feature_columns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--positive_fasta", default="data/raw/uniprot/positive.fasta")
    parser.add_argument("--negative_fasta", default="data/raw/uniprot/negative.fasta")
    parser.add_argument("--output_csv", default="data/processed/data.csv")
    parser.add_argument("--window", default=15, type=int)
    args = parser.parse_args()

    cfg = FeatureQuantifier(window=args.window)

    rows = []
    keep_positive = 0
    keep_negative = 0
    skips = 0

    # Process +ve sequences (1)
    for seq_id, seq in read_fasta(args.positive_fasta):
        feat = quantify_features(seq, cfg)
        if feat["length"] < cfg.min_length:
            skips += 1
            continue
        row = {"id": seq_id, "label": 1}
        row.update(feat)
        rows.append(row)
        keep_positive += 1

    # Process -ve sequences (0)
    for seq_id, seq in read_fasta(args.negative_fasta):
        feat = quantify_features(seq, cfg)
        if feat["length"] < cfg.min_length:
            skips += 1
            continue
        row = {"id": seq_id, "label": 0}
        row.update(feat)
        rows.append(row)
        keep_negative += 1

    cols = feature_columns(cfg)
    df = pd.DataFrame(rows, columns=["id", "label"] + cols)
    os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)
    df.to_csv(args.output_csv, index=False)

    # Summary
    print(
        f"\n Dataset Summary:"
        f"\nSaved to:          {args.output_csv}"
        f"\nKept positives:    {keep_positive}"
        f"\nKept negatives:    {keep_negative}"
        f"\nSkipped (too short): {skips}"
        f"\nLabel counts:\n{df['label'].value_counts().to_string()}"
    )

if __name__ == "__main__":
    main()