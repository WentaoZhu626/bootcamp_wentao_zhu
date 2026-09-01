# Deployment and Monitoring Plan

The candidate would run in shadow mode after each 20-trading-day rebalance. Monitoring begins with these thresholds:

| Layer / failure mode | Metric and starting threshold | Alert and first runbook step |
|---|---|---|
| Data: stale/incomplete history | latest date older than two expected business days; required-column null rate above 0.5% | Data analyst; stop scoring and compare source metadata with the last successful snapshot |
| Data: feature/schema drift | schema hash mismatch or feature PSI above 0.20 versus the trailing two-year reference | Quant analyst; validate provider changes before rebuilding |
| Model: deteriorating decisions | trailing 12-signal accuracy below 45% or Sharpe below 0 | Model owner and risk chair; suspend use and run all state-count scenarios |
| System: unreliable service | success below 95% over 20 runs or API p95 latency above 500 ms | Platform on-call; inspect `logs/pipeline.log`, keep the last good artifact, and retry once |
| Business: unusable allocation | exposure below 20% or above 90%, or more than six switches, over 12 signals | Committee chair; review turnover, costs, and state mapping |

Quantitative research reviews the dashboard monthly and logs repository issues. The data analyst owns source checks; platform on-call owns recovery and API availability. The risk chair approves rollback or renewed decision use.

Routine refitting occurs every five signals. Full review is annual, or earlier after a schema alert, PSI breach, two failed scoring cycles, or performance breach. Retraining cannot overwrite the approved artifact until data validation, chronological backtesting, scenario comparison, and risk-chair approval finish. Roll back to the prior `model/regime_model.joblib`; unresolved incidents keep the system in shadow mode.
