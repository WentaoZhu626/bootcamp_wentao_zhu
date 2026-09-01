# Data Dictionary

## Raw daily table

| Column | Type | Meaning |
|---|---|---|
| `date` | date | Trading date |
| `open` | float | Index open level |
| `high` | float | Index daily high |
| `low` | float | Index daily low |
| `close` | float | Index close level |
| `volume` | float | Provider-reported index volume proxy |

## Processed daily additions

| Column | Type | Meaning |
|---|---|---|
| `daily_return` | float | Close-to-close percentage return |
| `log_return` | float | Difference in log closing level |
| `return_outlier` | boolean | Broad 3-IQR extreme-return flag; observations are retained |

## Period feature table

| Column | Type | Meaning |
|---|---|---|
| `date` | date | Signal/rebalance date |
| `next_date` | date | End of the next 20-trading-day holding period |
| `close` | float | Closing level on the signal date |
| `period_return` | float | Trailing 20-day return |
| `return_sharpe` | float | Trailing return-to-volatility statistic |
| `volume_ratio` | float | Recent 10-day mean volume / 20-day mean volume - 1 |
| `half_return` | float | Trailing 10-day return |
| `future_return` | float | Next 20-day return; used only as the evaluation target |

## Prediction table

`walk_forward_predictions.csv` adds predicted return, hidden state, binary position, turnover, net strategy return, benchmark return, cumulative NAV, and direction-correct indicator. `future_return` is never used to form the same row's signal.
