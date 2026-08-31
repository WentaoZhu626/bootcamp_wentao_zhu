import pandas as pd


def get_summary_stats(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for numeric columns."""
    return dataframe.describe(include="number")