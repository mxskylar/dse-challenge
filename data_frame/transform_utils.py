import pandas as pd


def filter_out_null(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Filters out rows with null value in sepcified column
    """
    return df[df[column_name].notnull()]