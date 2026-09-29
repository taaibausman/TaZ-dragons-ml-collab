"""Unit tests for feature engineering and cleaning functions."""

import pandas as pd

from src.features import clean_dataset, compute_family_size


def test_compute_family_size():
    """Test family size calculation (sibsp + Parch + 1)."""
    df = pd.DataFrame(
        {
            "sibsp": [0, 1, 2],
            "Parch": [0, 2, 1],
        }
    )
    family_size = compute_family_size(df)
    assert list(family_size) == [1, 4, 4]


def test_clean_dataset_removes_zero_columns():
    """Test that zero-padded columns are dropped."""
    df = pd.DataFrame(
        {
            "Age": [22.0, 38.0, None],
            "Fare": [7.25, 71.28, 8.05],
            "Embarked": [2.0, None, 2.0],
            "zero": [0, 0, 0],
            "zero.1": [0, 0, 0],
            "2urvived": [0, 1, 1],
        }
    )
    cleaned = clean_dataset(df, feature_cols=["Age", "Fare", "Embarked"], target_col="2urvived")
    assert "zero" not in cleaned.columns
    assert "zero.1" not in cleaned.columns
    assert "Age" in cleaned.columns
    assert "Fare" in cleaned.columns
    assert "Embarked" in cleaned.columns
    assert "2urvived" in cleaned.columns
    assert cleaned["Age"].isnull().sum() == 0
    assert cleaned["Embarked"].isnull().sum() == 0
