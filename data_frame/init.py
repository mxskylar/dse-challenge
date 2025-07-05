import dataclasses
import pandas as pd

from data_frame.dtype import get_dtype_for_type
from data_frame.initial_data_frame import InitialDataFrameName, get_api_object_class_for_table
from mobilize.api_object import get_atomic_type
from mobilize.attendance import Attendance


def get_columns_and_dtypes() -> dict[InitialDataFrameName, tuple[list[str], dict[str, str]]]:
  """
  Returns column names and dtypes for the Pandas dataframes of all tables
  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame
  """
  # These data class fields will NOT become columns in the final tables.
  # They were only included in the data classes before their nested data was normalized.
  # Now that it is fully normalize, the columns are no longer needed.
  FIELD_DENY_LISTS = {
    InitialDataFrameName.ATTENDANCES: [
        "person",
        "event",
        "timeslot",
        "sponsor",
        "custom_signup_field_values"
    ],
    InitialDataFrameName.EVENTS: [
        "timeslots",
        "tags",
        "event_campaign",
        "sponsor"
    ]
  }
  # Get column and dtypes for all data frames
  dtypes = {}
  for df_name in InitialDataFrameName:
    cls = get_api_object_class_for_table(df_name)
    fields = dataclasses.fields(cls)
    field_deny_list = FIELD_DENY_LISTS[df_name] if df_name in FIELD_DENY_LISTS else []
    columns = []
    column_dtypes = {}
    for field in fields:
      # Add columns and dtypes that are not in the field deny list
      if field.name not in field_deny_list:
        columns.append(field.name)
        atomic_type = get_atomic_type(field.type)
        dtype = get_dtype_for_type(atomic_type)
        column_dtypes[field.name] = dtype.value
    dtypes[df_name] = (columns, column_dtypes)
  return dtypes

def get_data_frames(attendances: list[Attendance]) -> dict[InitialDataFrameName, pd.DataFrame]:
  """
  Returns Pandas data frames for each table.
  Loads data froms from lists of classes serialized from JSON API data and drops unnecessary columns.
  Casts column data to expected Pandas dtypes.
  """
  data = {df_name:[] for df_name in InitialDataFrameName}
  for attendance in attendances:
    data[InitialDataFrameName.ATTENDANCES].append(attendance)
    # Custom signup field values
    if attendance.custom_signup_field_values:
      data[InitialDataFrameName.CUSTOM_SIGNUP_FIELD_VALUES] = [
        *data[InitialDataFrameName.CUSTOM_SIGNUP_FIELD_VALUES],
        *attendance.custom_signup_field_values
      ]
    # Timeslot
    data[InitialDataFrameName.TIMESLOTS].append(attendance.timeslot)
    # Event
    data[InitialDataFrameName.EVENTS].append(attendance.event)
    # Event timeslots
    if attendance.event.timeslots:
      data[InitialDataFrameName.TIMESLOTS] = [
        *data[InitialDataFrameName.TIMESLOTS],
        *attendance.event.timeslots
      ]
    # Event campaign
    if attendance.event.event_campaign:
      data[InitialDataFrameName.EVENT_CAMPAIGNS].append(attendance.event.event_campaign)
    # Event tags
    if attendance.event.tags:
      data[InitialDataFrameName.TAGS] = [
        *data[InitialDataFrameName.TAGS],
        *attendance.event.tags
      ]
    # Sponsor
    if attendance.sponsor:
      data[InitialDataFrameName.ORGANIZATIONS].append(attendance.sponsor)
    # People
    data[InitialDataFrameName.PEOPLE].append(attendance.person)
  
  # Load data frames for lists of classes
  columns_and_dtypes = get_columns_and_dtypes()
  data_frames = {}
  for df_name, rows in data.items():
    columns, dtypes = columns_and_dtypes[df_name]
    # Types must be converted with astype because otherwise,
    # Pandas will incorrectly cast some integers as floats
    data_frames[df_name] = pd.DataFrame(rows, columns=columns).astype(dtypes)
  return data_frames