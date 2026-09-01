"""Small reusable utilities used across lifecycle stages."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd


def parse_dates(frame: pd.DataFrame, column: str = "date") -> pd.DataFrame:
    """Return a copy with a validated, timezone-naive datetime column."""
    result = frame.copy()
    result[column] = pd.to_datetime(result[column], errors="coerce").dt.tz_localize(None)
    if result[column].isna().any():
        raise ValueError(f"{column} contains invalid dates")
    return result


def file_sha256(path: str | Path) -> str:
    """Calculate a stable checksum for provenance and monitoring."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
