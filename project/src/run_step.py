"""CLI wrapper for the idempotent cleaning step."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

from src.cleaning import clean_market_data


def run_clean_step(input_path: str | Path, output_path: str | Path) -> Path:
    """Read raw CSV, clean it, and atomically replace the requested output."""
    source, destination = Path(input_path), Path(output_path)
    if not source.exists():
        raise FileNotFoundError(source)
    logging.info("clean step start input=%s output=%s", source, destination)
    cleaned = clean_market_data(pd.read_csv(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    cleaned.to_csv(temporary, index=False)
    temporary.replace(destination)
    logging.info("clean step complete rows=%d", len(cleaned))
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CSI 300 cleaning task")
    parser.add_argument("--input", default="data/raw/hs300_daily.csv")
    parser.add_argument("--output", default="data/processed/hs300_clean_cli.csv")
    parser.add_argument("--log", default="logs/pipeline.log")
    args = parser.parse_args()
    Path(args.log).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(args.log), logging.StreamHandler()],
    )
    run_clean_step(args.input, args.output)


if __name__ == "__main__":
    main()
