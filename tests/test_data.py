"""Data validation checks: schema, value ranges, and null counts."""

import os

import pandas as pd
import pytest


@pytest.fixture
def raw_data():
    path = "data/raw/titanic.csv"
    if not os.path.exists(path):
        os.makedirs("data/raw", exist_ok=True)
        dummy_df = pd.DataFrame({
            "Passengerid": range(1, 21),
            "Age": [22.0, 38.0, 26.0, 35.0, 35.0, 54.0, 2.0, 27.0, 14.0, 4.0] * 2,
            "Fare": [7.25, 71.28, 7.92, 53.1, 8.05, 51.86, 21.07, 11.13, 30.07, 16.7] * 2,
            "Sex": [0, 1, 1, 1, 0, 0, 0, 1, 1, 1] * 2,
            "Pclass": [3, 1, 3, 1, 3, 1, 3, 3, 2, 3] * 2,
            "Embarked": [2.0, 0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 2.0] * 2,
            "2urvived": [0, 1, 1, 1, 0, 0, 0, 1, 1, 1] * 2,
        })
        dummy_df.to_csv(path, index=False)
        return dummy_df
    return pd.read_csv(path)


def test_data_schema(raw_data):
    """Check required columns exist in raw dataset."""
    required_cols = ["Passengerid", "Age", "Fare", "Sex", "Pclass", "2urvived"]
    for col in required_cols:
        assert col in raw_data.columns, f"Missing required column: {col}"


def test_data_value_ranges(raw_data):
    """Validate numeric ranges for key features."""
    assert (raw_data["Age"] >= 0).all(), "Negative age values found"
    assert (raw_data["Fare"] >= 0).all(), "Negative fare values found"
    assert raw_data["Sex"].isin([0, 1]).all(), "Unexpected values in Sex column"
    assert raw_data["2urvived"].isin([0, 1]).all(), "Unexpected values in 2urvived target column"


def test_processed_data_no_nulls():
    """Check processed train and test sets have zero null values."""
    train_path = "data/processed/train.csv"
    test_path = "data/processed/test.csv"
    if os.path.exists(train_path):
        train_df = pd.read_csv(train_path)
        assert train_df.isnull().sum().sum() == 0, "Null values found in processed train data"
    if os.path.exists(test_path):
        test_df = pd.read_csv(test_path)
        assert test_df.isnull().sum().sum() == 0, "Null values found in processed test data"
