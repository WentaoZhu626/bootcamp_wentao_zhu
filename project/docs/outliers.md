# Outlier Assumptions and Sensitivity

Extreme index returns may be data errors, genuine crises, or precisely the events a regime model must learn. Automatically deleting them would create an unrealistically calm training history, so the primary data table retains all valid price movements.

`src/outliers.py` provides two reusable controls:

- `iqr_outlier_flags()` identifies daily returns outside broad three-IQR fences for audit and EDA. It flags 71 daily observations in the current dataset.
- `clip_to_training_bounds()` clips model features at the 1st and 99th percentiles calculated only from the current training window. It applies the same historical bounds to the current feature row, avoiding future-data leakage.

The five-state candidate uses training-only clipping for numerical stability. The sensitivity scenario `no_feature_clipping` keeps the same model structure but disables clipping. Its Sharpe ratio falls from 0.48 to 0.23, while maximum drawdown changes from -39.98% to -36.21%. This disagreement is a material model-risk finding: apparent performance depends on how extreme feature values are handled.

The flags are not labels of "bad data." Source validation, OHLC consistency, and duplicate checks determine whether a record is invalid. Valid extremes remain available in processed files and are visible to reviewers.
