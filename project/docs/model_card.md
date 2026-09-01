# Model Card: CSI 300 Hidden-State Risk Allocation

## Intended Use

The model supports a 20-trading-day review of broad CSI 300 exposure. It returns a hidden state, expected period return, and binary full-index/cash recommendation. It is intended for research and shadow monitoring by a tactical asset-allocation team.

## Model and Features

- Gaussian Hidden Markov Model with five states and diagonal covariance.
- Four trailing features: 20-day return, return-to-volatility statistic, volume ratio, and 10-day return.
- Rolling 100-observation training window, refitted every five rebalance observations.
- Training-window standardization and 1st/99th percentile clipping.
- State numbers are arbitrary; state-level historical forward returns determine `risk_on` or `risk_off`.

## Evaluation Design

Walk-forward evaluation uses non-overlapping 20-day observations. The first 80 observations initialize the process; every later prediction is generated from prior information. Exposure changes pay 5 basis points. Buy-and-hold is the benchmark. Sensitivity cases change state count and outlier clipping.

## Performance Snapshot

For 182 out-of-sample periods ending 2026-08-31, the candidate has 6.68% annualized return, 0.48 Sharpe ratio, -39.98% maximum drawdown, 54.95% direction accuracy, and 62.09% exposure. Buy-and-hold has 3.45% annualized return, 0.26 Sharpe, and -42.64% maximum drawdown.

## Limitations

- The bootstrap 95% interval for mean active period return includes zero.
- State-count and clipping choices materially affect results.
- The price index omits dividends; cash earns zero; cost and liquidity assumptions are simplified.
- Regime relationships can change, and state identities can permute after retraining.
- Public source availability and schema can change.

## Approval Status

Research candidate only. Recommended next step: shadow run, independent data/cost validation, and pre-registered forward evaluation before any live allocation use.
