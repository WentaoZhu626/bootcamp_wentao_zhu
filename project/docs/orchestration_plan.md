# Orchestration and System Design Plan

## Task Decomposition

| Task | Inputs | Outputs | Depends on | Idempotent? |
|---|---|---|---|---|
| 1. Acquire | yfinance/AkShare, `.env`, existing `data/raw/hs300_daily.csv` | `data/raw/hs300_daily.csv`, `data/raw/hs300_daily_metadata.json` | None | Conditional: cache reads are idempotent; an explicit live refresh may change with provider revisions |
| 2. Clean and validate | `data/raw/hs300_daily.csv` | `data/processed/hs300_clean.csv`, `.parquet`, `cleaning_audit.csv` | Acquire | Yes: deterministic code atomically replaces the same paths |
| 3. Build features | `data/processed/hs300_clean.csv` | `data/processed/period_features.csv` | Clean | Yes: fixed inputs and holding period produce the same table |
| 4. Walk-forward model | period features and scenario specifications | predictions, scenario metrics, uncertainty JSON, `model/regime_model.joblib` | Features | Yes with fixed seed and package versions |
| 5. Create report assets | cleaned data, predictions, metrics | `reports/images/*.png`, `reports/final_report.md` | Features and model | Yes: figures overwrite stable filenames |
| 6. Serve and verify | saved model artifact | `/health`, `/predict`, `/latest` responses and notebook test evidence | Model | Yes for identical model and request inputs |

## Dependencies and Parallel Work

```text
Acquire -> Clean -> Features -> Walk-forward model -> Serve/verify
                         |              |
                         +-> EDA plots  +-> Evaluation plots/report
```

EDA figures can run after features while model scenarios run. API verification and final reporting wait for a successfully saved model. The cumulative notebook executes serially for clarity, but the boundaries support later scheduling.

## Logging and Checkpoints

Each task logs start/end time, input path or source, row counts, selected parameters, output path, and exception details to `logs/pipeline.log`. Raw CSV plus metadata form the acquisition checkpoint. Cleaned Parquet, period features, predictions, scenario metrics, and the versioned model artifact are downstream checkpoints. A task should read only the latest validated upstream checkpoint and write to a temporary filename before atomic replacement.

## Failure and Retry Policy

- Network acquisition: two attempts with short backoff per provider, then retain the committed cache and record the failure.
- Schema or validation failure: no retry; stop because repeating malformed data is unsafe.
- HMM non-convergence: retry once with the same specification and a documented alternate seed; if still unstable, fail that scenario rather than silently selecting a result.
- File-write failure: retry once after verifying directory permissions and free space.
- API test failure: keep the prior model artifact and stop handoff.

Retries must not hide changes to data, parameters, or model version.

## Automation Boundary

Automate deterministic ingestion validation, cleaning, feature creation, walk-forward scoring, saved figures, and API smoke tests. Keep interpretation, model approval, alert-threshold changes, and live-refresh acceptance manual because these actions require risk judgment. Airflow or Prefect would add operational weight without improving the course-scale pipeline; Python functions, a CLI wrapper, logging, and stable checkpoints are sufficient.

`src/run_step.py` implements Task 2 as a reusable function and CLI. Its default command reads `data/raw/hs300_daily.csv`, writes `data/processed/hs300_clean_cli.csv`, and logs to `logs/pipeline.log`.
