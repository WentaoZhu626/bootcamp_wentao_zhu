# Homework 05: Data Storage

This homework demonstrates environment-driven data storage using CSV and Parquet formats, reusable read/write utility functions, and validation after reloading stored data.

## Data Storage

### Folder Structure

- `data/raw/` stores CSV files representing the original data.
- `data/processed/` stores Parquet files for analytical use.

### Storage Formats

CSV is used for raw data because it is human-readable, portable, and easy to inspect. Parquet is used for processed data because it preserves data types more reliably and provides an efficient columnar format for analytics.

### Environment Variables

The storage paths are configured in the local `.env` file:

- `DATA_DIR_RAW=data/raw`
- `DATA_DIR_PROCESSED=data/processed`

The Notebook loads these variables with `python-dotenv` and creates missing directories automatically. `.env` is excluded from Git, while `.env.example` documents the required configuration.

### Validation

The Notebook reloads both CSV and Parquet files and checks that their shapes match the original DataFrame. It also verifies that the `date` column remains datetime-compatible and that the `price` column remains numeric.

### Assumptions and Limitations

Parquet storage requires `pyarrow` or `fastparquet`. CSV files may require explicit date parsing when they are reloaded.