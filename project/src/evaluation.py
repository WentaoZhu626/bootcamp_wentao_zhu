"""Performance, uncertainty, and scenario evaluation helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error


def max_drawdown(nav: pd.Series) -> float:
    drawdown = nav / nav.cummax() - 1
    return float(drawdown.min())


def performance_metrics(backtest: pd.DataFrame, periods_per_year: float = 252 / 20) -> dict:
    """Compute risk-aware strategy and benchmark metrics."""
    strategy = backtest["strategy_return"]
    benchmark = backtest["benchmark_return"]
    years = len(backtest) / periods_per_year

    def annual_return(values: pd.Series) -> float:
        total = float((1 + values).prod())
        return total ** (1 / years) - 1 if years > 0 and total > 0 else np.nan

    def sharpe(values: pd.Series) -> float:
        volatility = values.std(ddof=1)
        return float(values.mean() / volatility * np.sqrt(periods_per_year)) if volatility > 0 else np.nan

    return {
        "n_periods": int(len(backtest)),
        "strategy_annual_return": annual_return(strategy),
        "strategy_annual_volatility": float(strategy.std(ddof=1) * np.sqrt(periods_per_year)),
        "strategy_sharpe": sharpe(strategy),
        "strategy_max_drawdown": max_drawdown(backtest["strategy_nav"]),
        "benchmark_annual_return": annual_return(benchmark),
        "benchmark_annual_volatility": float(benchmark.std(ddof=1) * np.sqrt(periods_per_year)),
        "benchmark_sharpe": sharpe(benchmark),
        "benchmark_max_drawdown": max_drawdown(backtest["benchmark_nav"]),
        "prediction_mae": float(mean_absolute_error(backtest["future_return"], backtest["predicted_return"])),
        "prediction_rmse": float(mean_squared_error(backtest["future_return"], backtest["predicted_return"]) ** 0.5),
        "direction_accuracy": float(
            accuracy_score(backtest["future_return"] > 0, backtest["predicted_return"] > 0)
        ),
        "exposure_rate": float(backtest["position"].mean()),
        "turnover_events": int((backtest["turnover"] > 0).sum()),
    }


def bootstrap_mean_active_return(
    backtest: pd.DataFrame,
    n_bootstrap: int = 2000,
    confidence: float = 0.95,
    seed: int = 42,
) -> dict:
    """Bootstrap a confidence interval for mean strategy-minus-benchmark return."""
    active = (backtest["strategy_return"] - backtest["benchmark_return"]).to_numpy()
    rng = np.random.default_rng(seed)
    estimates = np.array([rng.choice(active, len(active), replace=True).mean() for _ in range(n_bootstrap)])
    alpha = 1 - confidence
    low, high = np.quantile(estimates, [alpha / 2, 1 - alpha / 2])
    return {"mean": float(active.mean()), "ci_low": float(low), "ci_high": float(high)}
