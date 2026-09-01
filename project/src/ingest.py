"""Acquire and persist CSI 300 daily market data."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.utils import file_sha256


REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def normalize_market_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize AkShare or yfinance output to one lowercase schema."""
    result = frame.copy()
    if isinstance(result.columns, pd.MultiIndex):
        result.columns = result.columns.get_level_values(0)
    result = result.reset_index()
    aliases = {
        "Date": "date",
        "日期": "date",
        "Open": "open",
        "开盘": "open",
        "High": "high",
        "最高": "high",
        "Low": "low",
        "最低": "low",
        "Close": "close",
        "收盘": "close",
        "Volume": "volume",
        "成交量": "volume",
    }
    result = result.rename(columns=aliases)
    missing = set(REQUIRED_COLUMNS) - set(result.columns)
    if missing:
        raise ValueError(f"market source missing columns: {sorted(missing)}")
    result = result[REQUIRED_COLUMNS].copy()
    result["date"] = pd.to_datetime(result["date"], errors="coerce").dt.tz_localize(None)
    for column in REQUIRED_COLUMNS[1:]:
        result[column] = pd.to_numeric(result[column], errors="coerce")
    return result.sort_values("date").dropna(subset=["date", "close"]).reset_index(drop=True)


def download_yfinance(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Download prices with yfinance; raises when Yahoo returns no rows."""
    import yfinance as yf

    frame = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        timeout=30,
    )
    if frame.empty:
        raise RuntimeError("yfinance returned no rows")
    return normalize_market_columns(frame)


def download_akshare(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Download CSI index prices from AkShare's public Sina endpoint."""
    import akshare as ak

    frame = normalize_market_columns(ak.stock_zh_index_daily(symbol=f"sh{symbol}"))
    mask = frame["date"].between(pd.Timestamp(start), pd.Timestamp(end))
    result = frame.loc[mask].reset_index(drop=True)
    if result.empty:
        raise RuntimeError("AkShare returned no rows in the requested date range")
    return result


def validate_raw_market_data(frame: pd.DataFrame) -> None:
    """Fail fast on schema, duplicate-date, ordering, and price defects."""
    missing = set(REQUIRED_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"raw data missing columns: {sorted(missing)}")
    if frame["date"].duplicated().any():
        raise ValueError("raw data contains duplicate dates")
    if not frame["date"].is_monotonic_increasing:
        raise ValueError("raw data is not ordered by date")
    if (frame[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("raw data contains non-positive prices")
    if len(frame) < 1000:
        raise ValueError("raw history is too short for the configured HMM window")


def acquire_hs300(
    raw_path: str | Path,
    start: str,
    end: str,
    symbol: str = "000300",
    yfinance_symbol: str = "000300.SS",
    refresh: bool = False,
) -> tuple[pd.DataFrame, dict]:
    """Load a cached raw file or refresh it, trying Yahoo then AkShare."""
    path = Path(raw_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path = path.with_name("hs300_daily_metadata.json")

    if path.exists() and not refresh:
        frame = normalize_market_columns(pd.read_csv(path))
        validate_raw_market_data(frame)
        metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
        metadata.update({"source_used": "committed cache", "sha256": file_sha256(path)})
        return frame, metadata

    errors: dict[str, str] = {}
    try:
        frame = download_yfinance(yfinance_symbol, start, end)
        source = "yfinance"
    except Exception as error:
        errors["yfinance"] = f"{type(error).__name__}: {error}"
        frame = download_akshare(symbol, start, end)
        source = "AkShare Sina index endpoint"

    validate_raw_market_data(frame)
    frame.to_csv(path, index=False)
    metadata = {
        "symbol": symbol,
        "requested_start": start,
        "requested_end": end,
        "actual_start": str(frame["date"].min().date()),
        "actual_end": str(frame["date"].max().date()),
        "rows": int(len(frame)),
        "source_used": source,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "fallback_errors": errors,
        "sha256": file_sha256(path),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
    return frame, metadata
