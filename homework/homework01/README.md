# Next-Day Market Volatility Forecasting for Portfolio Risk Management

**Stage:** Problem Framing & Scoping (Stage 01)

## Problem Statement

Portfolio risk managers must decide whether to maintain, reduce, or hedge market exposure before the next trading session, but the size of the next day's market move is unknown when that decision is made. Relying only on a fixed risk limit or a long historical average can understate risk when market conditions change quickly. The project will investigate whether recent SPY returns, trading ranges, volume, and the VIX can provide a more responsive estimate of next-day market volatility.

The initial predictive target will be the next trading day's absolute close-to-close SPY log return, used as a transparent daily volatility proxy. The forecast will be produced after the current market close using only information available at that time. It will support a review decision rather than automate a trade. The primary success criterion is at least a 5% reduction in mean absolute error relative to a 20-day rolling historical-volatility baseline on a chronological holdout period. A secondary goal is to identify high-volatility days with at least 60% recall while maintaining at least 40% precision.

## Stakeholder & User

- **Primary stakeholder:** The Head of Portfolio Risk, who owns the risk limits and decides when portfolio exposure requires review.
- **End users:** A daily risk analyst and portfolio managers who consume the forecast and decide whether to maintain exposure, reduce position sizes, or add hedges.
- **Timing:** The result must be available after the U.S. market close and before the next trading session begins.
- **Workflow context:** The forecast supplements the existing daily risk report. It does not replace judgment, position-level analysis, or formal risk limits.
- **What users care about:** Timeliness, stability, interpretable drivers, clear uncertainty, and reliable warnings during unusually volatile periods.

## Useful Answer & Decision

This is a **predictive** problem. The main output will be a next-day volatility estimate and a Low / Normal / High risk label. A High label will trigger a review of exposure, concentration, and hedge coverage; it will not automatically execute a trade. The stakeholder-facing artifact will be a compact daily risk summary containing the forecast, the baseline forecast, the risk label, recent market context, and the assumptions behind the signal.

Model quality will be evaluated with time-ordered data. Mean absolute error (MAE) is the primary regression metric because it is easy to interpret and less dominated by a few extreme observations than squared-error metrics. Root mean squared error (RMSE), precision, recall, and precision-recall area under the curve for high-volatility alerts will be reported as secondary diagnostics.

## Assumptions & Constraints

- Daily adjusted SPY market data and a VIX series are available for research and can be aligned by trading date.
- Only information available by the current market close may be used to forecast the next trading day.
- The first version will use daily public data; intraday, proprietary, position-level, and options-surface data are out of scope.
- The workflow must run reproducibly on a personal laptop with open-source Python tools.
- Raw data will remain unchanged; all cleaning and feature creation must be reproducible from code.
- Evaluation must use chronological splits or walk-forward validation rather than random train/test splits.
- The output is a decision-support signal for an academic project, not investment advice or an automated trading instruction.

## Known Unknowns / Risks

- **Market regime change:** Relationships may weaken after structural breaks. Use walk-forward tests and compare performance across calm and stressed periods.
- **Rare extreme events:** Average metrics can hide poor crisis behavior. Report tail-period errors and alert recall separately.
- **Data leakage:** Rolling features or thresholds can accidentally use future observations. Lag predictors and fit all transformations on training data only.
- **Data quality:** Missing dates, corporate-action adjustments, or time-zone mismatches can distort returns. Add validation checks and retain data provenance.
- **Weak incremental signal:** A complex model may not beat a simple rolling baseline. Treat an honest negative result as a valid finding and prefer the simplest reliable model.
- **Alert fatigue:** Too many High labels reduce trust. Evaluate both precision and recall and document the threshold tradeoff.

## Lifecycle Mapping

| Goal | Lifecycle stage | Deliverable |
| --- | --- | --- |
| Define the risk decision and project boundary | Problem Framing & Scoping (Stage 01) | This README and the stakeholder memo |
| Identify the stakeholder, end users, and decision timing | Problem Framing & Scoping (Stage 01) | Stakeholder context and decision workflow |
| Establish measurable success criteria | Problem Framing & Scoping (Stage 01) | Baseline, MAE target, and alert metrics |
| Acquire reproducible market inputs | Data Acquisition & Ingestion | Raw SPY and VIX data with provenance notes |
| Create leakage-safe predictors | Data Cleaning & Feature Engineering | Processed feature table and reusable source code |
| Compare candidate forecasts with a simple baseline | Modeling & Evaluation | Time-ordered evaluation notebook and metrics report |
| Communicate an actionable risk signal | Reporting & Communication | Daily risk summary, figures, and final report |

## Repo Plan

- `homework/homework01/` contains the self-contained Stage 01 exercise.
- `project/data/raw/` will hold source data exactly as acquired.
- `project/data/processed/` will hold reproducible cleaned data and feature tables.
- `project/notebooks/` will hold the cumulative project notebook and focused analyses.
- `project/src/` will hold reusable acquisition, cleaning, feature, and evaluation functions.
- `project/docs/` will hold stakeholder notes, assumptions, and design decisions.
- `project/reports/images/` will hold generated figures; `project/model/` will hold saved model objects when introduced.
- The project README and risk log will be reviewed at every lifecycle stage. Changes will be committed after each meaningful, reproducible milestone.

## Stage 01 Deliverables

- [Completed starter notebook](homework01_problem-framing-and-scoping_submission.ipynb)
- [Stakeholder memo](docs/stakeholder_memo.md)
- Repository: [WentaoZhu626/bootcamp_wentao_zhu](https://github.com/WentaoZhu626/bootcamp_wentao_zhu)
