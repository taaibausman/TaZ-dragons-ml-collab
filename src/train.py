"""Model training stage: loads processed train split, fits classifier, and saves model."""

import argparse
import os
import sys

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from src.utils import load_params, set_seed


def train_model(
    train_path: str = "data/processed/train.csv",
    model_dir: str = "models",
    config_path: str = "params.yaml",
) -> None:
    """Train machine learning model using parameters and save model artifact."""
    params = load_params(config_path)
    seed = params.get("seed", 42)
    train_cfg = params.get("train", {})
    model_type = train_cfg.get("model_type", "random_forest")
    target_col = params.get("prepare", {}).get("target", "2urvived")

    set_seed(seed)

    if not os.path.exists(train_path):
        # If processed data doesn't exist yet, run prepare first
        from src.prepare import prepare_data

        prepare_data(config_path=config_path)

    train_df = pd.read_csv(train_path)
    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]

    if model_type == "random_forest":
        model = RandomForestClassifier(
            n_estimators=int(train_cfg.get("n_estimators", 100)),
            max_depth=int(train_cfg.get("max_depth", 6)) if train_cfg.get("max_depth") else None,
            min_samples_split=int(train_cfg.get("min_samples_split", 2)),
            criterion=train_cfg.get("criterion", "gini"),
            random_state=seed,
        )
    elif model_type == "gradient_boosting":
        model = GradientBoostingClassifier(
            n_estimators=int(train_cfg.get("n_estimators", 100)),
            max_depth=int(train_cfg.get("max_depth", 4)),
            random_state=seed,
        )
    elif model_type == "logistic_regression":
        model = LogisticRegression(
            max_iter=1000,
            random_state=seed,
        )
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    model.fit(X_train, y_train)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")
    joblib.dump(model, model_path)
    print(f"[train] Model ({model_type}) trained and saved to: {model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train ML model.")
    parser.add_argument(
        "--train-data", default="data/processed/train.csv", help="Path to train data"
    )
    parser.add_argument("--model-dir", default="models", help="Directory to save model")
    parser.add_argument("--config", default="params.yaml", help="Path to params.yaml")
    args = parser.parse_args()

    train_model(train_path=args.train_data, model_dir=args.model_dir, config_path=args.config)
