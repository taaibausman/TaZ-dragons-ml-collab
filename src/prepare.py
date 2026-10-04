"""Data preparation stage: load raw data, clean, split, and save processed splits."""

import argparse
import os
import sys

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sklearn.model_selection import train_test_split

from src.features import apply_imputation, clean_dataset, fit_imputation_values
from src.utils import load_params, set_seed


def prepare_data(
    input_path: str = "data/raw/titanic.csv",
    output_dir: str = "data/processed",
    config_path: str = "params.yaml",
) -> None:
    """Load raw dataset, clean features, perform deterministic train/test split, and save."""
    params = load_params(config_path)
    seed = params.get("seed", 42)
    split_cfg = params.get("split", {})
    test_size = split_cfg.get("test_size", 0.2)
    stratify_flag = split_cfg.get("stratify", True)
    prep_cfg = params.get("prepare", {})
    feature_cols = prep_cfg.get("features", None)
    target_col = prep_cfg.get("target", "2urvived")

    set_seed(seed)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input dataset not found at: {input_path}")

    df_raw = pd.read_csv(input_path)

    # Perform structural cleaning and feature selection first.
    df_cleaned = clean_dataset(
        df_raw,
        feature_cols=feature_cols,
        target_col=target_col,
    )

    stratify_target = (
        df_cleaned[target_col] if stratify_flag and target_col in df_cleaned.columns else None
    )

    # Split BEFORE learning imputation values to prevent data leakage.
    train_df, test_df = train_test_split(
        df_cleaned,
        test_size=test_size,
        random_state=seed,
        stratify=stratify_target,
    )

    # Learn preprocessing statistics ONLY from the training data.
    imputation_values = fit_imputation_values(train_df)

    # Apply the training-derived values to both splits.
    train_df = apply_imputation(train_df, imputation_values)
    test_df = apply_imputation(test_df, imputation_values)

    os.makedirs(output_dir, exist_ok=True)
    train_path = os.path.join(output_dir, "train.csv")
    test_path = os.path.join(output_dir, "test.csv")

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    print(f"[prepare] Successfully saved {len(train_df)} train rows -> {train_path}")
    print(f"[prepare] Successfully saved {len(test_df)} test rows -> {test_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare and split raw data.")
    parser.add_argument("--input", default="data/raw/titanic.csv", help="Path to raw dataset")
    parser.add_argument(
        "--output-dir", default="data/processed", help="Output directory for splits"
    )
    parser.add_argument("--config", default="params.yaml", help="Path to params.yaml")
    args = parser.parse_args()

    prepare_data(input_path=args.input, output_dir=args.output_dir, config_path=args.config)
