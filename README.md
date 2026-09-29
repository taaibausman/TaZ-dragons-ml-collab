# TaZ-dragons ML Collaboration Project

[![CI](https://github.com/taaibausman/TaZ-dragons-ml-collab/actions/workflows/ci.yml/badge.svg)](https://github.com/taaibausman/TaZ-dragons-ml-collab/actions/workflows/ci.yml)

## 📌 Overview
This repository contains a collaborative, reproducible Machine Learning workflow for Titanic Survival Prediction built for **Assignment 01: Git-Based Collaboration for an ML Project**.

## 👥 Team Members & Roles
- **Zaneeha Afzal** (`@zaneehaafzal`) — **Data & Platform Co-Owner**
  - Responsibilities: DVC setup, data versioning, dataset updates, pre-commit hygiene, schema validation.
- **Taaiba Usman** (`@taaibausman`) — **Model & Platform Co-Owner**
  - Responsibilities: Model training pipeline, hyperparameter configs, CI workflow, release management.

## 📂 Project Structure
```text
.
├── configs/
│   └── params.yaml            # Hyperparameters and pipeline configuration
├── data/
│   ├── raw/                   # Raw dataset (tracked by DVC)
│   └── processed/             # Cleaned train/test splits (tracked by DVC)
├── models/                    # Serialized model artifacts (tracked by DVC)
├── notebooks/                 # Exploratory data analysis (paired with Jupytext)
├── src/                       # Reusable and tested source code
│   ├── __init__.py
│   ├── utils.py               # Utilities (seeds, IO, commit SHA logging)
│   ├── features.py            # Feature engineering and cleaning
│   ├── prepare.py             # Data preparation stage
│   ├── train.py               # Model training stage
│   └── evaluate.py            # Evaluation & metrics generation stage
├── tests/                     # Unit, data, and model tests
├── .github/
│   ├── workflows/ci.yml       # GitHub Actions CI workflow
│   └── pull_request_template.md
├── .gitignore
├── .pre-commit-config.yaml    # Pre-commit hook configuration
├── CONTRIBUTING.md            # Git branching and review guidelines
├── dvc.yaml                   # DVC pipeline DAG definition
├── params.yaml                # Parameters symlink/definition
├── pyproject.toml             # Project build configuration
└── requirements.txt           # Pinned dependencies
```

## 🚀 Quickstart

### 1. Setup Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
pre-commit install
```

### 2. Pull Data and Reproduce Pipeline
```bash
dvc pull
dvc repro
```

### 3. Run Tests and Linting
```bash
pytest tests/
ruff check .
```
