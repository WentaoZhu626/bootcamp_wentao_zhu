"""Reusable exploratory summaries for market data."""

from __future__ import annotations

import pandas as pd


def eda_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Return type, completeness, and distribution diagnostics by column."""
    rows = []
    for column in frame.columns:
        series = frame[column]
        numeric = pd.api.types.is_numeric_dtype(series)
        rows.append(
            {
                "column": column,
                "dtype": str(series.dtype),
                "count": int(series.notna().sum()),
                "missing": int(series.isna().sum()),
                "unique": int(series.nunique(dropna=True)),
                "mean": float(series.mean()) if numeric else None,
                "std": float(series.std()) if numeric else None,
                "min": float(series.min()) if numeric else None,
                "max": float(series.max()) if numeric else None,
                "skew": float(series.skew()) if numeric else None,
            }
        )
    return pd.DataFrame(rows)
