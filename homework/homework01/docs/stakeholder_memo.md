# Stakeholder Brief: Next-Day Market Volatility Forecast

**Audience:** Head of Portfolio Risk and portfolio managers

**Cadence:** Daily, after the U.S. market close and before the next session

**Decision supported:** Review, reduce, or hedge broad U.S. equity exposure

## Persona and Context

Maya Chen is a composite Head of Portfolio Risk at a diversified investment firm. She is accountable for keeping portfolio exposure within approved limits while avoiding unnecessary turnover and hedging costs. Her team already receives position and exposure reports, but those reports describe the portfolio more clearly than they describe how unusual tomorrow's market conditions may be.

Maya's recurring pain point is timing. A warning that arrives after volatility has already risen is too late, while a system that produces frequent false alarms will be ignored. She needs a concise pre-session signal that explains how tomorrow's expected volatility compares with a transparent historical baseline, how confident the team should be, and what changed in the recent market data.

## What the Team Will Receive

- A next-day SPY volatility forecast based only on information available by the latest market close.
- A 20-day rolling historical-volatility baseline shown beside the model forecast.
- A Low / Normal / High risk label, with the threshold estimated from training data rather than future observations.
- A brief explanation of recent return, trading-range, volume, and VIX conditions.
- A record of missing data, model limitations, and any monitoring warnings.

## Decision Workflow

1. The daily risk analyst reviews the forecast and validation checks after the close.
2. A High risk label triggers a review of portfolio exposure, concentrated positions, and hedge coverage.
3. The Head of Portfolio Risk and portfolio managers decide whether to maintain exposure, reduce risk, or add a hedge.
4. No trade is executed automatically. Existing risk limits and human judgment remain authoritative.

## Success Criteria

- Reduce holdout MAE by at least 5% relative to a 20-day rolling baseline.
- Achieve at least 60% recall and 40% precision for high-volatility alerts.
- Produce the signal before the next trading session with no future information in the feature set.
- Keep the report short enough to interpret during the daily risk-review workflow.

## Assumptions and Constraints

- Public daily SPY and VIX data are sufficient for the first version.
- The project runs on a personal laptop and uses open-source Python tools.
- Intraday feeds, proprietary positions, options surfaces, and automated execution are outside the initial scope.
- Results are for academic decision support and are not investment advice.

## Principal Risks and Controls

- **Regime change:** Use walk-forward evaluation and report results by market regime.
- **Rare shocks:** Report tail-period errors and alert recall, not only average accuracy.
- **Leakage:** Lag inputs and fit transformations and thresholds only on training windows.
- **False alarms:** Show precision-recall tradeoffs and allow the stakeholder to review the alert threshold.
- **Missing or stale data:** Validate timestamps and fail visibly instead of silently producing a forecast.

## Decision Requested at Stage 01

Approve the problem framing, the daily decision workflow, and the proposed success criteria before data acquisition begins. In particular, confirm that a review trigger - rather than an automated trade - is the appropriate first operational use of the forecast.
