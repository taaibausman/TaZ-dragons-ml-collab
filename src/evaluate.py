"""Evaluation stage: loads model and test split, computes metrics, logs commit SHA, and writes metrics.json."""

import argparse
import json
import os
import sys

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

from src.utils import get_git_commit_sha, load_params


def evaluate_model(
    model_path: str = "models/model.joblib",
    test_path: str = "data/processed/test.csv",
    metrics_path: str = "metrics.json",
    config_path: str = "params.yaml",
) -> dict:
    """Evaluate model performance on test set and write metrics.json."""
    params = load_params(config_path)
    target_col = params.get("prepare", {}).get("target", "2urvived")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Test data file not found at: {test_path}")

    model = joblib.load(model_path)
    test_df = pd.read_csv(test_path)

    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    accuracy = float(accuracy_score(y_test, y_pred))
    precision = float(precision_score(y_test, y_pred, zero_division=0))
    recall = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_proba)) if y_proba is not None else 0.0

    commit_sha = get_git_commit_sha()

    metrics = {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "commit_sha": commit_sha,
        "model_type": params.get("train", {}).get("model_type", "unknown"),
        "seed": params.get("seed", 42),
    }

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"[evaluate] Metrics saved to {metrics_path}:")
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate model.")
    parser.add_argument("--model-path", default="models/model.joblib", help="Path to trained model")
    parser.add_argument("--test-data", default="data/processed/test.csv", help="Path to test data")
    parser.add_argument(
        "--metrics-path", default="metrics.json", help="Path to output metrics.json"
    )
    parser.add_argument("--config", default="params.yaml", help="Path to params.yaml")
    args = parser.parse_args()

    evaluate_model(
        model_path=args.model_path,
        test_path=args.test_data,
        metrics_path=args.metrics_path,
        config_path=args.config,
    )
