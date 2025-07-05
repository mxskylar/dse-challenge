import pandas as pd


def filter_out_null_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    return df[df[column_name].notnull()]