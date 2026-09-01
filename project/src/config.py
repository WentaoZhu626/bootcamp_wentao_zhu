"""Environment-aware project configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_env() -> None:
    """Load local environment variables without overriding shell values."""
    load_dotenv(PROJECT_ROOT / ".env", override=False)


def project_path(env_name: str, default: str) -> Path:
    """Resolve an environment-driven path relative to the project root."""
    load_env()
    value = Path(os.getenv(env_name, default))
    return value if value.is_absolute() else (PROJECT_ROOT / value).resolve()


@dataclass(frozen=True)
class Settings:
    """Parameters used by the reproducible analysis pipeline."""

    symbol: str = "000300"
    yfinance_symbol: str = "000300.SS"
    start_date: str = "2005-01-01"
    end_date: str = "2026-09-01"
    holding_period: int = 20
    n_states: int = 5
    initial_train_periods: int = 80
    training_window_periods: int = 100
    refit_every: int = 5
    n_iter: int = 100
    random_state: int = 42
    transaction_cost_bps: float = 5.0

    @property
    def data_dir(self) -> Path:
        return project_path("DATA_DIR", "data")

    @property
    def raw_path(self) -> Path:
        return self.data_dir / "raw" / "hs300_daily.csv"

    @property
    def processed_dir(self) -> Path:
        return self.data_dir / "processed"
