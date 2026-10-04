"""Feature engineering, data cleaning, and preprocessing functions."""

from typing import List, Optional

import pandas as pd


def compute_family_size(df: pd.DataFrame) -> pd.Series:
    """Compute FamilySize from sibsp and Parch."""
    sibsp = df["sibsp"] if "sibsp" in df.columns else 0
    parch = df["Parch"] if "Parch" in df.columns else 0
    return sibsp + parch + 1


def clean_dataset(
    df: pd.DataFrame,
    feature_cols: Optional[List[str]] = None,
    target_col: str = "2urvived",
) -> pd.DataFrame:
    """Perform structural cleaning and select requested features.

    Missing-value imputation is intentionally handled after the train/test
    split so that statistics are learned from the training data only.
    """
    df_clean = df.copy()

    # Drop zero-padding columns if present.
    zero_cols = [c for c in df_clean.columns if c.startswith("zero")]
    if zero_cols:
        df_clean = df_clean.drop(columns=zero_cols)

    # Select specified features and target.
    if feature_cols:
        selected_cols = [c for c in feature_cols if c in df_clean.columns]

        if target_col in df_clean.columns and target_col not in selected_cols:
            selected_cols.append(target_col)

        df_clean = df_clean[selected_cols]

    return df_clean


def fit_imputation_values(df: pd.DataFrame) -> dict:
    """Learn imputation values from the training data only."""
    imputation_values = {}

    if "Embarked" in df.columns:
        non_null = df["Embarked"].dropna()
        imputation_values["Embarked"] = non_null.mode()[0] if not non_null.empty else 2.0

    if "Age" in df.columns:
        imputation_values["Age"] = df["Age"].median()

    if "Fare" in df.columns:
        imputation_values["Fare"] = df["Fare"].median()

    return imputation_values


def apply_imputation(df: pd.DataFrame, imputation_values: dict) -> pd.DataFrame:
    """Apply training-derived imputation values to a dataset."""
    df_imputed = df.copy()

    for column, value in imputation_values.items():
        if column in df_imputed.columns:
            df_imputed[column] = df_imputed[column].fillna(value)

    return df_imputed
