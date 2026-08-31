# Next-Day Market Volatility Forecasting for Portfolio Risk Management

**Current lifecycle stage:** Problem Framing & Scoping (Stage 01)

## Project Summary

Portfolio risk managers must decide whether to maintain, reduce, or hedge market exposure before the next trading session, yet the size of the next day's market move is unknown when that decision is made. A risk process based only on fixed limits or long historical averages may react too slowly when conditions change. This project will test whether recent SPY returns, trading ranges, volume, and the VIX can provide a timely and interpretable estimate of next-day broad-market volatility.

The first version will forecast the next trading day's absolute close-to-close SPY log return as a transparent daily volatility proxy. It will use only information available by the current market close and will produce both a continuous forecast and a Low / Normal / High risk label. The result is intended to trigger a human review of exposure and hedge coverage; it will not execute trades. Success requires an out-of-sample improvement over a simple historical-volatility baseline while retaining useful recall and precision for unusually volatile days.

## Stakeholder Persona and Context

- **Primary stakeholder:** Head of Portfolio Risk, accountable for limits, escalation standards, and the cost of unnecessary risk reductions.
- **End users:** Daily risk analysts and portfolio managers who interpret the signal and decide whether exposure or hedging should change.
- **Decision timing:** After the U.S. market close and before the next trading session.
- **Core pain point:** Existing reports explain current exposure, but a late warning is not actionable and frequent false alarms erode trust.
- **Required qualities:** Timely, reproducible, interpretable, benchmarked, and explicit about uncertainty.

The full stakeholder brief is available in [`docs/stakeholder_memo.md`](docs/stakeholder_memo.md).

## Useful Answer and Decision

This is a predictive problem. The primary output is a next-day volatility estimate; the secondary output is a high-volatility review alert. A High label asks the risk team to examine exposure, concentration, and hedge coverage. Existing limits, position-level information, and human judgment remain authoritative.

The primary metric is mean absolute error (MAE) on a chronological holdout period. The first success target is at least a 5% MAE reduction relative to a 20-day rolling historical-volatility baseline. Secondary diagnostics include RMSE and, for High alerts, precision, recall, and precision-recall area under the curve. The initial alert target is at least 60% recall with at least 40% precision.

## Scope

### In Scope

- Daily SPY prices, returns, trading ranges, and volume.
- Daily VIX information and leakage-safe rolling market features.
- A next-day absolute-return volatility proxy.
- Time-ordered or walk-forward evaluation against simple baselines.
- A compact stakeholder-facing daily risk summary.

### Out of Scope

- Intraday or high-frequency forecasting.
- Proprietary position data and full portfolio optimization.
- Direct prediction of market direction or guaranteed profitability.
- Automated order execution.
- Production deployment during the initial course stages.

## Assumptions and Constraints

- Public SPY and VIX data can be acquired with sufficient history and aligned by trading date.
- Every predictor must be known by the current market close.
- The workflow must run on a personal laptop with open-source Python tools.
- Raw data remains unchanged; processed outputs are reproducible from source code.
- Chronological validation is required because random splitting would leak temporal information.
- The output is an academic decision-support artifact, not investment advice.

## Known Unknowns and Risk Controls

| Risk or unknown | Planned control |
| --- | --- |
| Market relationships change across regimes | Walk-forward evaluation and regime-level reporting |
| Extreme volatility observations are rare | Tail-period error analysis and alert recall |
| Rolling features can leak future data | Explicit feature lags and training-only transformations |
| Sources may contain gaps or timestamp mismatches | Schema, date, and missing-data validation with provenance notes |
| A complex model may not beat a naive baseline | Baseline-first evaluation and preference for simpler reliable models |
| Frequent alerts may create fatigue | Precision-recall analysis and stakeholder-approved threshold review |

## Goals, Lifecycle, and Deliverables

| Goal | Lifecycle stage | Deliverable |
| --- | --- | --- |
| Define the decision, stakeholder, and project boundary | Problem Framing & Scoping (Stage 01) | Project README and stakeholder memo |
| Establish measurable success criteria | Problem Framing & Scoping (Stage 01) | Baseline definition, MAE target, and alert metrics |
| Acquire traceable market data | Data Acquisition & Ingestion | Immutable raw files and provenance documentation |
| Produce an analysis-ready dataset | Data Cleaning & Feature Engineering | Validated processed table and reusable functions |
| Understand signal behavior and limitations | Exploratory Analysis | Project notebook and saved figures |
| Compare forecasts without temporal leakage | Modeling & Evaluation | Walk-forward results, baseline comparison, and model artifact |
| Support a daily risk-review decision | Reporting & Communication | Risk summary, assumptions, limitations, and final report |

## Repository Plan

```text
project/
├── data/
│   ├── raw/          # Direct, unedited source data
│   └── processed/    # Reproducible cleaned data and features
├── notebooks/        # Cumulative pipeline and focused analysis notebooks
├── src/              # Reusable acquisition, cleaning, feature, and evaluation code
├── docs/             # Stakeholder notes, assumptions, and design decisions
├── reports/
│   └── images/       # Generated stakeholder-facing figures
├── model/            # Saved model objects when introduced
├── requirements.txt
└── README.md
```

Raw data will never be edited manually. Processed data and figures must be reproducible from code. The README, assumptions, and risk controls will be reviewed at every lifecycle stage, and each meaningful reproducible milestone will be committed to GitHub.

## Current Deliverables

- [Stage 01 stakeholder memo](docs/stakeholder_memo.md)
- [Stage 01 homework framing package](../homework/homework01/README.md)
