import argparse
import pandas as pd
import joblib

from FASTA_Reader import read_fasta
from Feature_quantifier import FeatureQuantifier, quantify_features


def main():
    ''' Predict protein properties, return id with P(transmembrane) and predicion'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_path", default="models/logistic_model.joblib")
     
    # Adjust input path as needed
    parser.add_argument("--input_fasta", default = "data/Input/input_fasta.txt")
    parser.add_argument("--out_csv", default="reports/predictions.csv")
    args = parser.parse_args()

    bundle = joblib.load(args.model_path)
    model = bundle["model"]
    feature_columns = bundle["features"]
    threshold = float(bundle.get("best_threshold", 0.5))

    cfg = FeatureQuantifier()
    rows = []
    for seq_id, seq in read_fasta(args.input_fasta):
        feat = quantify_features(seq, cfg)
        x = [feat.get(col, 0.0) for col in feature_columns]

        probability = float(model.predict_proba([x])[0][1])
        prediction = 1 if probability >= threshold else 0
        rows.append({"id": seq_id, "probability": probability, "prediction": prediction})

    pd.DataFrame(rows).to_csv(args.out_csv, index=False)
    print(f"Predictions saved to: {args.out_csv}")


if __name__ == "__main__":
    main()