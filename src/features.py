"""Feature engineering, data cleaning, and preprocessing functions."""

from typing import List, Optional

import pandas as pd


def compute_family_size(df: pd.DataFrame) -> pd.Series:
    """Compute FamilySize feature from sibsp (siblings/spouse) and Parch (parents/children)."""
    sibsp = df["sibsp"] if "sibsp" in df.columns else 0
    parch = df["Parch"] if "Parch" in df.columns else 0
    return sibsp + parch + 1


def clean_dataset(
    df: pd.DataFrame, feature_cols: Optional[List[str]] = None, target_col: str = "2urvived"
) -> pd.DataFrame:
    """Clean raw dataset, drop redundant zero-padded columns, and impute missing values."""
    df_clean = df.copy()

    # Drop zero padding columns if present
    zero_cols = [c for c in df_clean.columns if c.startswith("zero")]
    if zero_cols:
        df_clean = df_clean.drop(columns=zero_cols)

    # Impute missing values
    if "Embarked" in df_clean.columns:
        embarked_mode = (
            df_clean["Embarked"].mode()[0] if not df_clean["Embarked"].dropna().empty else 2.0
        )
        df_clean["Embarked"] = df_clean["Embarked"].fillna(embarked_mode)

    if "Age" in df_clean.columns:
        age_median = df_clean["Age"].median()
        df_clean["Age"] = df_clean["Age"].fillna(age_median)

    if "Fare" in df_clean.columns:
        fare_median = df_clean["Fare"].median()
        df_clean["Fare"] = df_clean["Fare"].fillna(fare_median)

    # Select specified features and target
    if feature_cols:
        selected_cols = [c for c in feature_cols if c in df_clean.columns]
        if target_col in df_clean.columns and target_col not in selected_cols:
            selected_cols.append(target_col)
        df_clean = df_clean[selected_cols]

    return df_clean
