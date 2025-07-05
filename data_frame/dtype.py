from datetime import datetime, date
from enum import Enum


class DType(Enum):
    """
    Emum for the names of Pandas dtypes
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dtypes.html
    """
    INT = "Int64"
    FLOAT = "Float64"
    DATETIME = "Datetime64"
    BOOL = "bool"
    OBJECT = "object"

def get_dtype_for_type(t) -> DType:
    """
    Returns Pandas dtype that corresponds to native Python type
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dtypes.html
    """
    if t is int:
        return DType.INT
    elif t is float:
        return DType.FLOAT
    elif t is datetime or t is date:
        return DType.DATETIME
    elif t is bool:
        return DType.BOOL
    # Pandas considers strings, nested objects, and nested lists to all be objects
    # From the Pandas docs: "Columns with mixed types are stored with the object dtype."
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dtypes.html
    return DType.OBJECT