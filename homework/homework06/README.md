# Homework 06: Data Preprocessing

This homework applies reusable cleaning functions to the starter dataset and saves a cleaned copy to `data/processed/sample_data_cleaned.csv`.

## Cleaning Strategy

- `drop_missing()` removes columns with a missing fraction above 50%; this removes `extra_data` while retaining useful columns.
- `fill_missing_median()` fills missing numeric values in `age`, `income`, and `score` with their column medians.
- `normalize_data()` applies min-max scaling to those numeric columns.
- `zipcode` remains text and the city labels remain unchanged.

The reusable functions live in `src/cleaning.py`. The notebook compares missingness and summary statistics before and after cleaning. Median imputation assumes the observed values are representative; dropping a highly incomplete column may discard information if its missingness is meaningful.
