import json
import csv
import pandas as pd

from data_frame.init import get_data_frames
from data_frame.initial_data_frame import InitialDataFrameName
from data_frame.transform_utils import filter_out_null_column
from mobilize.attendance import Attendance


ATTENDANCES_DATA_FILE = "data/attendances.json"

def get_tables() -> dict[str, pd.DataFrame]:
  attendances: list[Attendance] = []
  # Serialize attendance data into classes, normalize columns, and associate joinable IDs
  with open(ATTENDANCES_DATA_FILE) as f:
    attendances = [Attendance(**attendance) for attendance in json.loads(f.read())]
  # Load data frames from lists of classes
  data_frames = get_data_frames(attendances)

  # 1. Filter out timeslots whose id is excluded for campaign finance reasons.
  #    The other columns for these timeslots were normalized and will be included in the attendances table.
  # 2. All remaining timeslots are associated with both an Attendance and an Event,
  #    so duplicate rows need to be dropped.
  raw_timeslots = data_frames[InitialDataFrameName.TIMESLOTS]
  timeslots = filter_out_null_column(raw_timeslots, "id").drop_duplicates()

  # 1. Filter out events whose id is excluded for campaign finance reasons.
  #    According to the API:
  #    "If the requesting organization is independent and the event’s organization is coordinated, all but event_type is omitted."
  #    https://github.com/mobilizeamerica/api?tab=readme-ov-file#attendance-object
  #    The event_type column was normalized and will be included in the attendances table.
  # 2. Split events and contacts into separate tables. The same event is returned more than once by the API,
  #    resulting in a duplicate event for each contact.
  # 3. The same Event may be associated with multiple attendances, so duplicate rows need to be dropped
  #    from both the events and contacts data frames.
  filtered_events = filter_out_null_column(data_frames[InitialDataFrameName.EVENTS], "id")
  contact_columns = ["contact_name", "contact_email_adddress", "contact_phone_number", "owner_user_id"]
  event_contacts = filtered_events[[*contact_columns, "id"]].rename(columns={"id": "event_id"}).drop_duplicates()
  events = filtered_events.drop(columns=contact_columns).drop_duplicates()

  # More than one event may be associated with the same event campaign,
  # so duplicate rows need to be dropped.
  event_campaigns = data_frames[InitialDataFrameName.EVENT_CAMPAIGNS].drop_duplicates()

  # 1. More than one Tag may be associated with one Event,
  #    so a separate relational table / flat file must map event_id to tag_id.
  #    Split the data frame into two: One data frame for the mapping and another for the remaining columns.
  # 2. Multiple events may be associated with the same Tags,
  #    so duplicate rows need to be dropped.
  raw_tags = data_frames[InitialDataFrameName.TAGS]
  event_tag_mapping = raw_tags[["event_id", "id"]].rename(columns={"id": "tag_id"})
  tags = raw_tags.drop(columns=["event_id"]).drop_duplicates()

  # More than one attendance or event may be associated with the same sponsor organization,
  # so duplicate rows need to be dropped.
  organizations = data_frames[InitialDataFrameName.ORGANIZATIONS].drop_duplicates()

  # More than one attendance may be associated with the same person
  # because they may have attendend multiple events,
  # so duplicate rows need to be dropped.
  people = data_frames[InitialDataFrameName.PEOPLE].drop_duplicates()

  return {
    "attendances": data_frames[InitialDataFrameName.ATTENDANCES],
    "custom_signup_field_values": data_frames[InitialDataFrameName.CUSTOM_SIGNUP_FIELD_VALUES],
    "timeslots": timeslots,
    "events": events,
    "event_contacts": event_contacts,
    "event_campaigns": event_campaigns,
    "event_tags": event_tag_mapping,
    "tags": tags,
    "organizations": organizations,
    "people": people
  }

if __name__ =="__main__":
  data_frames = get_tables()
  for table_name, df in data_frames.items():
    df.to_csv(f"data/{table_name}.csv", index=False, quoting=csv.QUOTE_STRINGS)