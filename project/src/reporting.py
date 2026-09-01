"""Create consistent stakeholder-facing figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def create_eda_figures(daily: pd.DataFrame, observations: pd.DataFrame, output_dir: str | Path) -> None:
    output = Path(output_dir)
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(9, 4.8))
    sns.histplot(daily["daily_return"].dropna(), bins=80, kde=True, ax=ax, color="#3266a8")
    ax.set(title="CSI 300 Daily Return Distribution", xlabel="Daily return", ylabel="Observations")
    _save(fig, output / "daily_return_distribution.png")

    fig, ax = plt.subplots(figsize=(7, 5.5))
    correlation = observations[["period_return", "return_sharpe", "volume_ratio", "half_return", "future_return"]].corr()
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
    ax.set_title("Feature Correlation Matrix")
    _save(fig, output / "feature_correlation.png")


def create_evaluation_figures(
    backtest: pd.DataFrame,
    scenarios: pd.DataFrame,
    output_dir: str | Path,
) -> None:
    output = Path(output_dir)
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(backtest["next_date"], backtest["strategy_nav"], label="HMM risk allocation", linewidth=2)
    ax.plot(backtest["next_date"], backtest["benchmark_nav"], label="CSI 300 buy and hold", linewidth=1.7)
    ax.set(title="Out-of-Sample Cumulative Growth", xlabel="Date", ylabel="Growth of 1.0")
    ax.legend()
    _save(fig, output / "cumulative_performance.png")

    fig, ax = plt.subplots(figsize=(10, 4.6))
    strategy_dd = backtest["strategy_nav"] / backtest["strategy_nav"].cummax() - 1
    benchmark_dd = backtest["benchmark_nav"] / backtest["benchmark_nav"].cummax() - 1
    ax.fill_between(backtest["next_date"], strategy_dd, 0, alpha=0.45, label="HMM allocation")
    ax.plot(backtest["next_date"], benchmark_dd, color="#bf4b4b", linewidth=1.2, label="Buy and hold")
    ax.set(title="Drawdown Comparison", xlabel="Date", ylabel="Drawdown")
    ax.legend()
    _save(fig, output / "drawdown_comparison.png")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    sns.barplot(data=scenarios, x="scenario", y="strategy_sharpe", ax=axes[0], color="#3266a8")
    axes[0].axhline(float(scenarios["benchmark_sharpe"].iloc[0]), color="#bf4b4b", linestyle="--", label="benchmark")
    axes[0].set(title="Sharpe Ratio by Assumption", xlabel="", ylabel="Sharpe ratio")
    axes[0].tick_params(axis="x", rotation=25)
    axes[0].legend()
    sns.barplot(data=scenarios, x="scenario", y="strategy_max_drawdown", ax=axes[1], color="#d9943d")
    axes[1].axhline(float(scenarios["benchmark_max_drawdown"].iloc[0]), color="#bf4b4b", linestyle="--", label="benchmark")
    axes[1].set(title="Maximum Drawdown by Assumption", xlabel="", ylabel="Drawdown")
    axes[1].tick_params(axis="x", rotation=25)
    axes[1].legend()
    _save(fig, output / "scenario_comparison.png")

    fig, ax = plt.subplots(figsize=(10, 5.3))
    for state, group in backtest.groupby("state"):
        ax.scatter(group["date"], group["future_return"], s=24, alpha=0.75, label=f"State {state}")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set(title="Out-of-Sample Hidden States and Next-Period Returns", xlabel="Signal date", ylabel="Next-period return")
    ax.legend(ncol=2)
    _save(fig, output / "hidden_states.png")
