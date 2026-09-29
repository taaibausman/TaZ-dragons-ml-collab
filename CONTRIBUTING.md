# Contributing Guide

Welcome to the **TaZ-dragons** ML Project collaboration repository.

## 1. Branching Model

We follow a strict unidirectional promotion model:
- **`main`**: Production branch. Only contains tagged, reproducible release models (`model-v1.0`). Direct pushes and force-pushes are blocked.
- **`staging`**: Release candidate branch. Used for full end-to-end reproducibility testing (`dvc repro` and metric checks) before promoting to `main`.
- **`dev`**: Main integration branch. All feature, data, and pipeline branches merge into `dev` via Pull Requests.

### Short-lived Branches
- **`feat/<name>`**: New features, code refactoring, pipeline steps. Created from `dev`, merged into `dev`, deleted after merge.
- **`data/<name>`**: Dataset modifications (updates, cleaning changes) tracked via DVC. Created from `dev`, merged into `dev`.
- **`exp/<member>-<idea>`**: Personal exploratory branches (e.g., `exp/taaiba-rf-depth`, `exp/zaneeha-lr-features`). Never merged directly into `dev`. Winning experiments are cherry-picked or applied into a `feat/` branch.
- **`fix/<name>`**: Urgent fixes to production. Created from `main`, merged to `main`, and back-merged into `dev`.

## 2. Commit Message Conventions

We adhere to the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat:` New features or pipeline enhancements
- `data:` Changes to dataset tracking, versions, or data preparation
- `exp:` Experiment runs and parameter tuning
- `fix:` Bug fixes
- `ci:` CI workflow and automated test changes
- `docs:` Documentation and report updates
- `refactor:` Code restructuring without behavioral change

Example:
```bash
git commit -m "feat: add feature scaling step in data preparation"
git commit -m "data: track raw titanic dataset with DVC"
git commit -m "exp: test random forest max_depth=10"
```

## 3. Merge Strategy (PR Decision)

- **PRs into `dev`**: **Squash and Merge** (to maintain clean, atomic commits per feature while preserving PR discussion).
- **Promotion to `staging` & `main`**: **Merge Commit** (to preserve full release history and exact commit SHAs).

## 4. Pull Request Workflow & Checklist

Every PR must use the checklist template `.github/pull_request_template.md`:
1. Open PR targeting `dev`.
2. Assign teammate as reviewer.
3. Ensure all CI checks pass (linting with `ruff`, tests with `pytest`, data checks, smoke train).
4. Reviewer verifies checklist items and approves before merging.
