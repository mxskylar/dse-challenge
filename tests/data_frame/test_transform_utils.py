import pandas as pd

from data_frame.transform_utils import filter_out_null


def test_filter_out_null():
    non_null_id_row = {"id": 1}
    df_with_null_value = pd.DataFrame([non_null_id_row, {"id": None}])
    df = filter_out_null(df_with_null_value, "id")
    assert df.to_dict("records") == [non_null_id_row], \
        "Only the row with a non-null value in the column id should remain in the data frame"