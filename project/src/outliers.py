"""Documented outlier detection and clipping helpers."""

from __future__ import annotations

import pandas as pd


def iqr_outlier_flags(series: pd.Series, multiplier: float = 3.0) -> pd.Series:
    """Flag observations outside broad IQR fences without deleting them."""
    clean = series.dropna()
    q1, q3 = clean.quantile([0.25, 0.75])
    spread = q3 - q1
    lower, upper = q1 - multiplier * spread, q3 + multiplier * spread
    return (series < lower) | (series > upper)


def clip_to_training_bounds(
    train: pd.DataFrame,
    current: pd.DataFrame,
    columns: list[str],
    lower: float = 0.01,
    upper: float = 0.99,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clip train/current features using bounds learned only from training data."""
    train_out, current_out = train.copy(), current.copy()
    for column in columns:
        low, high = train[column].quantile([lower, upper])
        train_out[column] = train[column].clip(low, high)
        current_out[column] = current[column].clip(low, high)
    return train_out, current_out
