"""Feature helpers for Stage 09."""

import pandas as pd


def add_spend_income_ratio(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result['spend_income_ratio'] = result['monthly_spend'] / result['income']
    return result


def add_spend_credit_ratio(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    result['spend_credit_ratio'] = result['monthly_spend'] / result['credit_score']
    return result


def add_region_frequency(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.copy()
    frequencies = result['region'].value_counts(normalize=True)
    result['region_frequency'] = result['region'].map(frequencies)
    return result
