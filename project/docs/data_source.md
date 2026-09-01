# Data Source and Acquisition Notes

## Source

The project uses CSI 300 index daily OHLCV data for symbol `000300`. The acquisition module tries:

1. yfinance ticker `000300.SS`;
2. AkShare's public Sina index endpoint for `sh000300`.

On 2026-09-01, Yahoo returned a rate-limit response, so the committed snapshot was acquired through AkShare. No API key is required. Exact retrieval details and the source-file checksum are stored in `data/raw/hs300_daily_metadata.json`.

## Validation

`src/ingest.py` checks required columns, chronological ordering, duplicate dates, positive prices, and minimum history. `src/cleaning.py` applies stricter OHLC consistency checks and records a before/after audit. The downloaded raw CSV is not manually edited.

## Reproducibility Policy

The default pipeline reads the committed snapshot and therefore works without network access. A user must explicitly pass `refresh_data=True` to replace it. Live-source results may differ because providers revise history or change schemas; any refresh should be reviewed through the metadata, checksum, row count, date range, and cleaning audit before modeling.
