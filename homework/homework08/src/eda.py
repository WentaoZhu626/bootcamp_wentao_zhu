"""Reusable exploratory-data-analysis helpers."""

import pandas as pd


def eda_summary(dataframe: pd.DataFrame) -> dict:
    """Print and return a compact data-quality and profiling summary."""
    numeric = dataframe.select_dtypes(include='number')
    categorical = dataframe.select_dtypes(include=['object', 'category', 'string'])
    result = {
        'shape': dataframe.shape,
        'missing': dataframe.isna().sum().to_dict(),
        'numeric_summary': numeric.describe().T,
        'categorical_summary': {
            column: categorical[column].value_counts(dropna=False).to_dict()
            for column in categorical.columns
        },
    }
    print('Shape:', result['shape'])
    print()
    print('Missing values:')
    print(pd.Series(result['missing']))
    print()
    print('Numeric summary:')
    print(result['numeric_summary'])
    print()
    print('Categorical counts:')
    for column, counts in result['categorical_summary'].items():
        print(column, counts)
    return result
