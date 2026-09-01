"""Leakage-safe features sampled at fixed rebalancing dates."""

from __future__ import annotations

import numpy as np
import pandas as pd


FEATURE_COLUMNS = ["period_return", "return_sharpe", "volume_ratio", "half_return"]


def build_period_observations(daily: pd.DataFrame, holding_period: int = 20) -> pd.DataFrame:
    """Create trailing features at each rebalance and the next-period target."""
    frame = daily.sort_values("date").reset_index(drop=True)
    half = max(1, holding_period // 2)
    daily_returns = frame["close"].pct_change()
    rows = []
    for index in range(holding_period, len(frame) - holding_period, holding_period):
        period_returns = daily_returns.iloc[index - holding_period + 1 : index + 1].dropna()
        volatility = period_returns.std(ddof=1)
        full_volume = frame["volume"].iloc[index - holding_period + 1 : index + 1].mean()
        recent_volume = frame["volume"].iloc[index - half + 1 : index + 1].mean()
        rows.append(
            {
                "date": frame.loc[index, "date"],
                "next_date": frame.loc[index + holding_period, "date"],
                "close": frame.loc[index, "close"],
                "period_return": frame.loc[index, "close"] / frame.loc[index - holding_period, "close"] - 1,
                "return_sharpe": (
                    period_returns.mean() / volatility * np.sqrt(holding_period)
                    if pd.notna(volatility) and volatility > 0
                    else 0.0
                ),
                "volume_ratio": recent_volume / full_volume - 1 if full_volume > 0 else 0.0,
                "half_return": frame.loc[index, "close"] / frame.loc[index - half, "close"] - 1,
                "future_return": frame.loc[index + holding_period, "close"] / frame.loc[index, "close"] - 1,
            }
        )
    result = pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan)
    return result.dropna(subset=[*FEATURE_COLUMNS, "future_return"]).reset_index(drop=True)


def build_latest_features(daily: pd.DataFrame, holding_period: int = 20) -> dict[str, float]:
    """Build the four trailing features at the most recent available date."""
    frame = daily.sort_values("date").reset_index(drop=True)
    if len(frame) <= holding_period:
        raise ValueError("not enough daily rows for latest features")
    index = len(frame) - 1
    half = max(1, holding_period // 2)
    daily_returns = frame["close"].pct_change()
    period_returns = daily_returns.iloc[index - holding_period + 1 : index + 1].dropna()
    volatility = period_returns.std(ddof=1)
    full_volume = frame["volume"].iloc[index - holding_period + 1 : index + 1].mean()
    recent_volume = frame["volume"].iloc[index - half + 1 : index + 1].mean()
    return {
        "period_return": float(frame.loc[index, "close"] / frame.loc[index - holding_period, "close"] - 1),
        "return_sharpe": float(
            period_returns.mean() / volatility * np.sqrt(holding_period)
            if pd.notna(volatility) and volatility > 0
            else 0.0
        ),
        "volume_ratio": float(recent_volume / full_volume - 1 if full_volume > 0 else 0.0),
        "half_return": float(frame.loc[index, "close"] / frame.loc[index - half, "close"] - 1),
    }
