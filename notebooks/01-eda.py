# %%
# 01-eda.py - Exploratory Data Analysis for Titanic Survival Dataset
# Paired with notebooks/01-eda.ipynb via Jupytext (percent format)

# %%
import os
import sys

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.features import clean_dataset, compute_family_size

# %%
# Load raw Titanic dataset
data_path = os.path.join("..", "data", "raw", "titanic.csv")
if not os.path.exists(data_path):
    data_path = os.path.join("data", "raw", "titanic.csv")

df_raw = pd.read_csv(data_path)
print("Raw Dataset Shape:", df_raw.shape)

# %%
# Clean dataset using reusable function from src/features.py
df_clean = clean_dataset(df_raw, feature_cols=["Age", "Fare", "Sex", "sibsp", "Parch", "Pclass", "Embarked"], target_col="2urvived")
print("Cleaned Dataset Shape:", df_clean.shape)
print("Cleaned Dataset Head:")
print(df_clean.head())

# %%
# Compute FamilySize using reusable function from src/features.py
df_clean["FamilySize"] = compute_family_size(df_clean)
print("Family Size Distribution:")
print(df_clean["FamilySize"].value_counts().sort_index())

# %%
# Survival rate by Sex
print("Survival Rate by Sex (1=Female, 0=Male):")
print(df_clean.groupby("Sex")["2urvived"].mean())

# %%
# Survival rate by Pclass
print("Survival Rate by Pclass:")
print(df_clean.groupby("Pclass")["2urvived"].mean())
