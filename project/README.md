# CSI 300 Hidden-State Risk Allocation

## Project Summary

Institutional investors need a repeatable way to decide whether broad China equity exposure should remain fully invested or be reduced when the market environment changes. Fixed calendar rules and unconditional historical averages can miss shifts in return, volatility, and trading activity. This project studies whether a Gaussian Hidden Markov Model (HMM) can identify recurring CSI 300 market regimes from information available at each rebalance date and turn those regimes into a transparent 20-trading-day risk-allocation signal.

The output is a research decision-support signal: `risk_on` recommends full benchmark exposure and `risk_off` recommends cash exposure until the next rebalance. It does not short, use leverage, place orders, or replace portfolio limits and human review. The primary comparison is a chronological out-of-sample backtest against CSI 300 buy-and-hold, with transaction costs and sensitivity analysis included.

## Stakeholder Context

- **Primary stakeholder:** the chair of a tactical asset-allocation committee.
- **End users:** quantitative analysts, portfolio managers, and portfolio-risk staff.
- **Decision:** whether to maintain or reduce CSI 300 exposure for the next 20 trading days.
- **What they care about:** drawdown control, risk-adjusted return, signal stability, transparent assumptions, and operational reproducibility.
- **Use boundary:** the signal triggers review; it is not an automated investment instruction.

See [`docs/stakeholder_memo.md`](docs/stakeholder_memo.md) for the stakeholder brief and [`reports/final_report.md`](reports/final_report.md) for the decision-ready results.

## Scope, Assumptions, and Success Criteria

### In scope

- CSI 300 daily open, high, low, close, and volume data from 2005-01-04 through 2026-08-31.
- Four trailing features sampled every 20 trading days.
- A five-state Gaussian HMM with a rolling 100-observation training window.
- Chronological walk-forward signals beginning in September 2011.
- Full-index or cash exposure, with 5 basis points charged when exposure changes.
- Model-state, outlier-treatment, and uncertainty sensitivity analysis.

### Out of scope

- Individual-security selection, leverage, short selling, derivatives, and portfolio optimization.
- Intraday decisions, market-impact modeling, taxes, dividends, and cash interest.
- Claims that latent states are permanent economic truths.
- Live trading or production approval.

### Decision criteria

The research candidate is useful only if it improves risk-adjusted performance or drawdown behavior relative to buy-and-hold without relying on future information. Directional accuracy, MAE, turnover, exposure, and bootstrap uncertainty are supporting diagnostics. A result is not considered conclusive when its active-return confidence interval includes zero.

## Current Findings

The five-state candidate was evaluated over 182 non-overlapping 20-day periods from 2011-09-01 through 2026-08-31. After the stated transaction-cost assumption, it produced a 6.68% annualized return, 0.48 Sharpe ratio, and -39.98% maximum drawdown. Buy-and-hold produced 3.45%, 0.26, and -42.64%, respectively. Direction accuracy was 54.95%, and the strategy was invested 62.09% of periods.

The result is sensitive to modeling choices. Three- and four-state alternatives had Sharpe ratios of 0.29 and 0.20, while removing training-only feature clipping reduced the Sharpe ratio to 0.23. The bootstrap 95% interval for mean active 20-day return was -0.41% to 0.74%, so the apparent improvement is not statistically decisive. The recommended action is continued shadow monitoring, not immediate deployment.

## Goals -> Lifecycle -> Deliverables

| Goal | Lifecycle stage | Deliverable |
|---|---|---|
| Define a stakeholder decision and project boundary | 01 Problem Framing & Scoping | `README.md`, `docs/stakeholder_memo.md` |
| Make the work reproducible | 02 Tooling Setup | `.env.example`, `.gitignore`, `requirements.txt`, project scaffold |
| Establish reusable Python patterns | 03 Python Fundamentals | `notebooks/python_fundamentals_summary.ipynb`, `src/utils.py` |
| Acquire traceable market data | 04 Data Acquisition | `src/ingest.py`, `data/raw/hs300_daily.csv`, source metadata |
| Preserve reproducible data states | 05 Data Storage | CSV raw data, CSV/Parquet processed data, storage documentation |
| Build an analysis-ready table | 06 Data Preprocessing | `src/cleaning.py`, cleaning audit, processed daily data |
| Make extreme observations explicit | 07 Outlier Analysis | `src/outliers.py`, flags, clipped/unclipped sensitivity |
| Understand distributions and relationships | 08 EDA | `notebooks/eda_analysis.ipynb`, `src/eda.py`, saved figures |
| Create domain-relevant predictors | 09 Feature Engineering | `src/features.py`, `data/processed/period_features.csv` |
| Fit a time-aware model | 10 Modeling | `src/modeling.py`, walk-forward predictions, model artifact |
| Quantify performance and uncertainty | 11 Evaluation & Risk | `src/evaluation.py`, scenario metrics, bootstrap interval |
| Communicate a decision-ready result | 12 Delivery Design | `reports/final_report.md`, `reports/images/` |
| Package the analysis for reuse | 13 Productization | `app.py`, `model/regime_model.joblib`, API evidence in pipeline notebook |
| Define operational controls | 14 Deployment & Monitoring | `docs/monitoring_plan.md`, `docs/handoff_plan.md` |
| Describe execution dependencies | 15 Orchestration | `docs/orchestration_plan.md`, `src/run_step.py` |
| Make the full lifecycle legible | 16 Lifecycle Review | `docs/lifecycle_framework_guide.md`, `docs/project_summary.md` |

## Repository Structure

```text
project/
├── data/
│   ├── raw/                 # Immutable downloaded market data and provenance
│   └── processed/           # Reproducible cleaned, feature, prediction, and metric files
├── notebooks/
│   ├── python_fundamentals_summary.ipynb
│   ├── eda_analysis.ipynb
│   └── project_pipeline.ipynb
├── src/                     # Ingestion, cleaning, features, HMM, evaluation, reporting, CLI
├── docs/                    # Design decisions, risks, monitoring, handoff, lifecycle summary
├── reports/
│   ├── final_report.md
│   └── images/
├── model/regime_model.joblib
├── tests/
├── app.py
├── requirements.txt
└── README.md
```

## Setup from a Fresh Clone

From the repository root:

```bash
cd project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

No API key is required. The committed raw file makes the default workflow offline-reproducible.

## Run the Full Analysis

The final, cumulative notebook is `notebooks/project_pipeline.ipynb`. It begins by changing to the project root, so it can be launched from either `project/` or `project/notebooks/`.

```bash
jupyter lab notebooks/project_pipeline.ipynb
```

Use **Run All**. The notebook reads the committed raw file, recreates processed tables, runs the walk-forward scenarios, overwrites the model artifact, saves report figures, and tests the API. The same pipeline can run without Jupyter:

```bash
python -c "from src.pipeline import run_full_pipeline; run_full_pipeline(refresh_data=False)"
```

To attempt a live refresh, use `refresh_data=True`. Acquisition tries yfinance first and falls back to AkShare if Yahoo is unavailable or rate-limited.

## Run One CLI Pipeline Step

Stage 15 exposes the idempotent cleaning task as a command-line step. From `project/`:

```bash
python -m src.run_step \
  --input data/raw/hs300_daily.csv \
  --output data/processed/hs300_clean_cli.csv \
  --log logs/pipeline.log
```

Re-running the command safely replaces the same processed output. It logs start time, paths, row count, completion, and failures.

## Data Storage and Provenance

- `data/raw/hs300_daily.csv` is the unchanged source snapshot used for grading.
- `data/raw/hs300_daily_metadata.json` records source, retrieval time, requested and actual dates, row count, fallback errors, and SHA-256 checksum.
- `data/processed/hs300_clean.csv` and `.parquet` contain the validated daily table.
- `data/processed/period_features.csv` contains one leakage-safe record per rebalance date.
- Predictions, metrics, and uncertainty summaries are generated, never hand-edited.
- `DATA_DIR` may be overridden in `.env`; relative paths resolve from `project/`.

The live acquisition used AkShare's public Sina index endpoint after yfinance returned a rate-limit error. This source outcome is documented in the committed metadata rather than hidden.

## Feature Definitions

| Feature | Definition | Decision rationale |
|---|---|---|
| `period_return` | Return over the previous 20 trading days | Captures medium-horizon market direction |
| `return_sharpe` | Mean daily return divided by daily volatility, scaled to the 20-day window | Separates stable advances from noisy moves |
| `volume_ratio` | Recent half-window average volume divided by full-window average volume, minus one | Captures changes in participation |
| `half_return` | Return over the previous 10 trading days | Detects acceleration or reversal within the full window |

Every feature uses observations available on or before the signal date. Scaling and clipping bounds are fitted only on the active training window.

## API Usage

Start the saved-model API:

```bash
python app.py
```

It serves on `http://127.0.0.1:5060`.

Health and latest cached decision:

```bash
curl http://127.0.0.1:5060/health
curl http://127.0.0.1:5060/latest
```

Score an explicit feature record:

```bash
curl -X POST http://127.0.0.1:5060/predict \
  -H "Content-Type: application/json" \
  -d '{"features":{"period_return":0.03,"return_sharpe":0.8,"volume_ratio":0.1,"half_return":0.01}}'
```

The response includes hidden state, `risk_on`/`risk_off`, recommended exposure, expected 20-day return, model version, and training date. Missing, extra, or nonnumeric feature values return HTTP 400 with a JSON error.

## Assumptions, Risks, and Handoff

- Latent state numbers have no stable economic meaning across refits; only their training-window return mapping drives exposure.
- Index history is not a total-return series, and cash earns zero in this analysis.
- A five-state diagonal-Gaussian HMM is a simplifying approximation, not proof of five true regimes.
- Repeated scenario review creates model-selection risk.
- The out-of-sample active-return interval includes zero.
- Public-source schema, timing, and availability can change.
- The API is local demonstration software without authentication or production hardening.

The full controls and ownership path are documented in [`docs/model_card.md`](docs/model_card.md), [`docs/monitoring_plan.md`](docs/monitoring_plan.md), and [`docs/handoff_plan.md`](docs/handoff_plan.md). The stakeholder recommendation is to run the signal in shadow mode, review it monthly, and require independent data and cost validation before any capital decision.
