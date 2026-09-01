# Lifecycle Framework Guide

| Stage | Where the work lives | Project decision |
|---|---|---|
| 01 Problem Framing & Scoping | `README.md`, `docs/stakeholder_memo.md` | Frame the output as an advisory 20-day full-index/cash decision for an allocation committee, not an automated trade |
| 02 Tooling Setup | `.gitignore`, `.env.example`, `requirements.txt`, standard folders | Use a reproducible Python environment and keep local settings outside version control |
| 03 Python Fundamentals | `notebooks/python_fundamentals_summary.ipynb`, `src/utils.py` | Formalize date parsing and checksums as reusable utilities |
| 04 Data Acquisition & Ingestion | `src/ingest.py`, `data/raw/` | Try yfinance, fall back to AkShare, and preserve the successful raw snapshot plus provenance |
| 05 Data Storage | `data/raw/`, `data/processed/`, README Data Storage section | Keep immutable raw CSV and reproducible processed CSV/Parquet outputs |
| 06 Data Preprocessing | `src/cleaning.py`, `cleaning_audit.csv`, pipeline notebook | Validate dates, OHLC relationships, prices, volume, missingness, and duplicates |
| 07 Outliers & Risk Assumptions | `src/outliers.py`, `docs/outliers.md` | Retain valid extremes; flag them and compare training-only clipping with no clipping |
| 08 Exploratory Data Analysis | `notebooks/eda_analysis.ipynb`, `src/eda.py`, report images | Examine return tails, missingness, feature relationships, and time coverage |
| 09 Feature Engineering | `src/features.py`, `period_features.csv` | Use four trailing return, risk-adjusted return, volume, and acceleration features with no same-row target leakage |
| 10 Modeling | `src/modeling.py`, `walk_forward_predictions.csv` | Use a five-state rolling Gaussian HMM and chronological walk-forward evaluation |
| 11 Evaluation & Risk Communication | `src/evaluation.py`, `scenario_metrics.csv`, uncertainty JSON | Compare metrics, state-count scenarios, outlier treatment, and a bootstrap active-return interval |
| 12 Results & Delivery Design | `reports/final_report.md`, `reports/images/` | Deliver a plain-language written report with decisions, alternate scenarios, and risks |
| 13 Productization | `model/regime_model.joblib`, `app.py`, pipeline API tests | Save the complete inference bundle and expose health, explicit-feature, and latest-signal routes |
| 14 Deployment & Monitoring | `docs/monitoring_plan.md`, `docs/handoff_plan.md` | Monitor Data/Model/System/Business layers with named owners and rollback rules |
| 15 Orchestration & System Design | `docs/orchestration_plan.md`, `src/run_step.py` | Decompose six tasks and make cleaning an idempotent logged CLI step |
| 16 Lifecycle Review | this guide, `docs/project_summary.md`, final README | Keep the full chain readable and runnable for a new analyst |
