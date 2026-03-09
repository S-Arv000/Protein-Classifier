import os
import json
import argparse
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    roc_curve,
    average_precision_score,
    precision_recall_curve,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


def f1_threshold(y_true, y_probs):
    """Return (threshold, f1) that maximises F1"""
    thresholds = np.linspace(0.0, 1.0, 101)
    best_threshold = 0.5
    best_f1 = -1.0

    for thresh in thresholds:
        preds = (y_probs >= thresh).astype(int)
        score = f1_score(y_true, preds)
        if score > best_f1:
            best_f1 = score
            best_threshold = thresh

    return best_threshold, best_f1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_csv", default="data/processed/data.csv")
    parser.add_argument(
        "--model_output", default="models/logistic_model.joblib"
    ) 
    parser.add_argument(
        "--model_metrics", default="models/model_metrics.json"
    )
    parser.add_argument(
        "--classification_report",
        default="reports/classification_report.txt",
    )
    parser.add_argument(
        "--reports_dir",
        default="reports",
    )
    parser.add_argument("--test_size", default=0.2, type=float)
    parser.add_argument("--random_state", default=42, type=int)
    args = parser.parse_args()

    #   training
    df = pd.read_csv(args.data_csv)
    X = df.drop(columns=["id", "label"])
    y = df["label"]
    ids = df["id"]
    feature_columns = list(X.columns)

    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        X, y, ids, test_size=args.test_size, random_state=args.random_state, stratify=y
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(random_state=args.random_state, max_iter=5000),
                ),
        ]
    )

    parameter_grid = {"classifier__C": [0.01, 0.1, 1, 10, 100]}
    grid_search = GridSearchCV(pipeline, parameter_grid, n_jobs=2, scoring="f1")
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    y_probs = best_model.predict_proba(X_test)[:, 1]
    preds_05 = (y_probs >= 0.5).astype(int)

    best_threshold, best_f1 = f1_threshold(y_test, y_probs)
    preds = (y_probs >= best_threshold).astype(int)

    metrics = {
        "best_parameters": grid_search.best_params_,
        "roc_auc": roc_auc_score(y_test, y_probs),
        "pr_auc": average_precision_score(y_test, y_probs),
        "best_f1": best_f1,
        "best_threshold": best_threshold,
        "n_training": len(y_train),
        "n_test": len(y_test),
        "positive_rate_train": np.mean(y_train),
        "positive_rate_test": np.mean(y_test),
        "test_id": id_test.tolist(),
        "feature_columns": feature_columns,
    }

    print("Model Metrics:")
    print(json.dumps(metrics, indent=4))

    print("\nClassification Report (0.5 threshold)")
    print(classification_report(y_test, preds_05, digits=5))
    print(f"\nClassification Report (best F1 threshold = {best_threshold})")
    print(classification_report(y_test, preds, digits=5))

    # Metrics
    os.makedirs(os.path.dirname(args.model_output), exist_ok=True)
    joblib.dump(
        {
            "model": best_model,
            "features": feature_columns,
            "best_threshold": best_threshold,
        },
        args.model_output,
    )
    os.makedirs(os.path.dirname(args.model_metrics), exist_ok=True)
    with open(args.model_metrics, "w") as f:
        json.dump(metrics, f, indent=4)

    # Classification report text
    os.makedirs(os.path.dirname(args.classification_report), exist_ok=True)
    with open(args.classification_report, "w") as f:
        f.write("Threshold=0.5\n")
        f.write(classification_report(y_test, preds_05, digits=5))
        f.write("\n")
        f.write(f"Threshold={best_threshold}\n")
        f.write(classification_report(y_test, preds, digits=5))

    # plots belwo
    os.makedirs(args.reports_dir, exist_ok=True)

    # ROC
    fpr, tpr, _ = roc_curve(y_test, y_probs)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.xlabel("False Positive")
    plt.ylabel("True Positive")
    plt.title("ROC Curve")
    plt.savefig(os.path.join(args.reports_dir, "ROC.png"))
    plt.close()

    # PR curve
    precision, recall, _ = precision_recall_curve(y_test, y_probs)
    plt.figure()
    plt.plot(recall, precision)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.savefig(os.path.join(args.reports_dir, "PRC.png"))
    plt.close()

    # confusion matrix using best F1 threshold
    cm = confusion_matrix(y_test, preds)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    plt.figure()
    disp.plot()
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title(f"Confusion Matrix (Best F1 thresh = {best_threshold})")
    plt.savefig(os.path.join(args.reports_dir, "cfm.png"))
    plt.close()

    print(f"Saved Model: {args.model_output}")
    print(f"Saved Metrics: {args.model_metrics}")
    print(f"Saved Report text: {args.classification_report}")
    print(f"Saved plot images in: {args.reports_dir}")


if __name__ == "__main__":
    main()