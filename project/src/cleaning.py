"""Reusable market-data cleaning functions."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.utils import parse_dates


PRICE_COLUMNS = ["open", "high", "low", "close"]


def clean_market_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Clean market data while preserving genuine extreme price movements."""
    result = parse_dates(frame)
    result = result.sort_values("date").drop_duplicates("date", keep="last").reset_index(drop=True)
    for column in [*PRICE_COLUMNS, "volume"]:
        result[column] = pd.to_numeric(result[column], errors="coerce")
    result.loc[result["volume"] < 0, "volume"] = np.nan
    result["volume"] = result["volume"].replace(0, np.nan).ffill().bfill()
    result = result.dropna(subset=PRICE_COLUMNS)
    result = result[(result[PRICE_COLUMNS] > 0).all(axis=1)]
    result = result[result["high"] >= result[["open", "close", "low"]].max(axis=1)]
    result = result[result["low"] <= result[["open", "close", "high"]].min(axis=1)]
    result["daily_return"] = result["close"].pct_change()
    result["log_return"] = np.log(result["close"]).diff()
    return result.reset_index(drop=True)


def cleaning_audit(raw: pd.DataFrame, cleaned: pd.DataFrame) -> pd.DataFrame:
    """Return a compact before/after quality table."""
    return pd.DataFrame(
        {
            "check": ["rows", "duplicate_dates", "missing_prices", "nonpositive_volume"],
            "raw": [
                len(raw),
                int(pd.to_datetime(raw["date"]).duplicated().sum()),
                int(raw[PRICE_COLUMNS].isna().sum().sum()),
                int((pd.to_numeric(raw["volume"], errors="coerce") <= 0).sum()),
            ],
            "cleaned": [
                len(cleaned),
                int(cleaned["date"].duplicated().sum()),
                int(cleaned[PRICE_COLUMNS].isna().sum().sum()),
                int((cleaned["volume"] <= 0).sum()),
            ],
        }
    )
