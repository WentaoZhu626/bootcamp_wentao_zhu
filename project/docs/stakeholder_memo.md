# Stakeholder Memo: CSI 300 Regime Signal

**To:** Tactical Asset-Allocation Committee Chair\
**From:** Quantitative Research\
**Decision horizon:** Next 20 trading days

## Decision Problem

The committee must decide whether to maintain full CSI 300 benchmark exposure or temporarily reduce exposure when market conditions appear unfavorable. The current process benefits from a systematic signal that reacts to changing return, volatility, and participation patterns while remaining understandable enough to challenge in committee review.

## Proposed Answer

This project uses a five-state Gaussian Hidden Markov Model to group recurring market conditions. At each rebalance date, the model uses only trailing information, estimates the current hidden state, and maps that state to the forward returns observed in its rolling training window. A positive estimate produces `risk_on`; otherwise it produces `risk_off`. The signal is a review input, not an order.

## What Success Means

Success means better out-of-sample risk-adjusted performance or drawdown behavior than CSI 300 buy-and-hold after 5 basis points per exposure change. Direction accuracy, turnover, scenario stability, and bootstrap uncertainty must also be acceptable. A strong point estimate is insufficient when plausible assumptions reverse the conclusion.

## Guardrails

- No shorting, leverage, or security selection.
- No information dated after the signal date.
- Human review remains mandatory.
- Results are based on a price index, zero cash yield, and simplified costs.
- Deployment should remain in shadow mode until independently validated.

The current five-state result is encouraging but assumption-sensitive, and the active-return confidence interval includes zero. Continue monitoring; do not treat this research result as production approval.
