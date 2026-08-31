"""Reusable cleaning helpers for Stage 06."""

from collections.abc import Iterable

import pandas as pd


def fill_missing_median(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """Return a copy with missing numeric values filled by column medians."""
    result = dataframe.copy()
    for column in columns:
        if column not in result.columns:
            raise KeyError(f"Column not found: {column}")
        if not pd.api.types.is_numeric_dtype(result[column]):
            raise TypeError(f"Median fill requires a numeric column: {column}")
        result[column] = result[column].fillna(result[column].median())
    return result


def drop_missing(dataframe: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """Drop columns whose missing-value fraction is greater than threshold."""
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    keep = dataframe.isna().mean() <= threshold
    return dataframe.loc[:, keep].copy()


def normalize_data(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """Return a copy with selected numeric columns min-max normalized."""
    result = dataframe.copy()
    for column in columns:
        if column not in result.columns:
            raise KeyError(f"Column not found: {column}")
        if not pd.api.types.is_numeric_dtype(result[column]):
            raise TypeError(f"Normalization requires a numeric column: {column}")
        minimum = result[column].min()
        span = result[column].max() - minimum
        result[column] = 0.0 if span == 0 else (result[column] - minimum) / span
    return result
