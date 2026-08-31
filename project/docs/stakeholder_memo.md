# Stakeholder Brief: Next-Day Market Volatility Forecast

**Audience:** Head of Portfolio Risk and portfolio managers

**Cadence:** Daily, after the U.S. market close and before the next session

**Decision supported:** Review, reduce, or hedge broad U.S. equity exposure

## Persona and Business Context

Maya Chen is a composite Head of Portfolio Risk at a diversified investment firm. She owns the portfolio's escalation standards and must balance two costs: reacting too slowly to genuine market stress and reacting too often to noisy warnings. Her team already knows the portfolio's current exposure, but it lacks a concise, benchmarked estimate of whether tomorrow's broad-market volatility is likely to be unusual.

A useful forecast must arrive before the next session, distinguish a model signal from a transparent baseline, and explain its limitations. Maya does not want a black-box trading recommendation. She wants a review trigger that helps the team decide whether current exposure, concentrated positions, and hedge coverage deserve attention.

## Proposed Deliverable

The project will provide:

- A next-day SPY volatility forecast using only information available by the latest market close.
- A 20-day rolling historical-volatility baseline for comparison.
- A Low / Normal / High risk label.
- A short summary of recent return, trading-range, volume, and VIX conditions.
- Visible data-quality, model-drift, and uncertainty warnings.

## Decision Workflow

1. The daily risk analyst checks data freshness and reviews the forecast after the close.
2. A High label triggers review of portfolio exposure, concentrations, and hedge coverage.
3. The Head of Portfolio Risk and portfolio managers decide whether to maintain exposure, reduce risk, or add a hedge.
4. The system records the forecast and decision context for later monitoring.
5. No trade is executed automatically.

## Acceptance Criteria

- At least 5% lower chronological-holdout MAE than the 20-day rolling baseline.
- At least 60% recall and 40% precision for high-volatility alerts.
- No future information in features, transformations, or alert thresholds.
- A reproducible run on a personal laptop before the next trading session.
- A concise report that separates facts, forecasts, assumptions, and limitations.

## Constraints and Controls

- The initial scope uses public daily SPY and VIX data only.
- Intraday feeds, proprietary positions, options surfaces, and automated execution are excluded.
- Walk-forward validation and regime-level reporting will address nonstationarity.
- Tail-period error and alert recall will supplement average-error metrics.
- Data provenance, missing-date checks, and feature lags will be documented.

## Stage 01 Decision Request

Approve the project boundary, the stakeholder workflow, and the proposed success criteria before data acquisition begins. The central design choice is intentional: the forecast is a human review trigger, not an automated trading strategy.
