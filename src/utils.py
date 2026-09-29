"""Utility functions for reproducibility, configuration, and logging."""

import os
import random
import subprocess

import numpy as np
import yaml


def load_params(config_path: str = "params.yaml") -> dict:
    """Load configuration parameters from YAML file."""
    if not os.path.exists(config_path):
        alt_path = os.path.join("configs", "params.yaml")
        if os.path.exists(alt_path):
            config_path = alt_path
        else:
            raise FileNotFoundError(f"Configuration file not found at {config_path} or {alt_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def set_seed(seed: int = 42) -> None:
    """Set random seed across standard libraries for deterministic execution."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def get_git_commit_sha() -> str:
    """Retrieve current Git commit SHA, fallback to 'uncommitted' if unavailable."""
    try:
        sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
            .decode("ascii")
            .strip()
        )
        return sha
    except Exception:
        return "uncommitted"
