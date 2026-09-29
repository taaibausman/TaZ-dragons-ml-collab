"""Smoke and integration tests for model training and evaluation."""

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.evaluate import evaluate_model
from src.train import train_model


def test_smoke_train_end_to_end(tmp_path):
    """Smoke train test: verify model training on small dataset sample."""
    sample_df = pd.DataFrame(
        {
            "Age": np.random.uniform(18, 70, size=50),
            "Fare": np.random.uniform(5, 200, size=50),
            "Sex": np.random.choice([0, 1], size=50),
            "sibsp": np.random.choice([0, 1, 2], size=50),
            "Parch": np.random.choice([0, 1, 2], size=50),
            "Pclass": np.random.choice([1, 2, 3], size=50),
            "Embarked": np.random.choice([0, 1, 2], size=50),
            "2urvived": np.random.choice([0, 1], size=50),
        }
    )

    train_file = tmp_path / "train.csv"
    sample_df.to_csv(train_file, index=False)

    model_dir = tmp_path / "models"
    model_dir.mkdir()

    train_model(train_path=str(train_file), model_dir=str(model_dir))

    model_path = model_dir / "model.joblib"
    assert model_path.exists(), "Model file was not created"

    model = joblib.load(model_path)
    assert isinstance(model, RandomForestClassifier)

    # Test evaluation output
    metrics_file = tmp_path / "metrics.json"
    metrics = evaluate_model(
        model_path=str(model_path), test_path=str(train_file), metrics_path=str(metrics_file)
    )
    assert "accuracy" in metrics
    assert "f1" in metrics
    assert 0.0 <= metrics["accuracy"] <= 1.0
