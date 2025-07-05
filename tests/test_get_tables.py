import json
import pytest
import pandas as pd

from data_frame.transform_utils import filter_out_null
from process_data import ATTENDANCES_DATA_FILE, get_tables


@pytest.fixture(scope='session', autouse=True)
def data_frames():
    return get_tables()

@pytest.fixture(scope='session', autouse=True)
def raw_json() -> list[dict]:
    with open(ATTENDANCES_DATA_FILE) as f:
        return json.loads(f.read())

def count_rows(df: pd.DataFrame) -> int:
    """
    Returns the number of rows in a Pandas data frame
    """
    return len(df.index)

def assert_column_is_unique_and_not_null(df: pd.DataFrame, column_name: str):
    """
    Asserts that:
        1. None of a column's values are null
        2. Column values are unique
    """
    assert 0 == count_rows(df[df[column_name].isnull()]), \
        f"No values in column {column_name} should be null"
    assert df[column_name].is_unique is True, \
        f"Values in column {column_name} should be unique"

def assert_not_unique(df: pd.DataFrame, column_name: str):
    """
    Asserts that a column's values are NOT unqiue in a Pandas data frame
    """
    assert df[column_name].is_unique is False, \
        f"Values in column {column_name} should NOT be unique"

def assert_joins_to_single_row(
    left_df: pd.DataFrame,
    left_column_name: str,
    right_df: pd.DataFrame,  
    right_column_name: str,
    assert_left: bool
):
    """
    When assert_left:
        - TRUE: Asserts that each non-null row in the left data frame joins to a single row in the right data frame
        - FALSE: Asserts that each non-null row in the right data frame joins to a single row in the left data frame
    """
    joined_df = pd.merge(
        left_df,
        right_df,
        how="inner",
        left_on=left_column_name,
        right_on=right_column_name
    )
    single_match_df = left_df if assert_left else right_df
    single_match_column_name = left_column_name if assert_left else right_column_name
    non_null_rows = count_rows(filter_out_null(single_match_df, single_match_column_name))
    assert_direction = "left" if assert_left else "right"
    assert non_null_rows == count_rows(joined_df), (
        f"Number of non-null rows returned by {left_column_name} INNER JOIN {right_column_name} " +
        f"does not match number of rows on the {assert_direction} table"
    )

def test_attendances(data_frames):
    attendances = data_frames["attendances"]
    non_null_ids = attendances[attendances["id"].notnull()]["id"]
    assert non_null_ids.is_unique is True, "Non-null values in the column id should be unique"

    # Joins to events
    # Events may only contain one non-null value, event_type, for campagin finance reasons
    # In these cases, the key "event.id" will be null but the key "event" will have a non-null value
    assert_joins_to_single_row(
        attendances,
        "event_id",
        data_frames["events"],
        "id",
        assert_left=True
    )

    # Joins to sponsors / organizations
    assert_joins_to_single_row(
        attendances,
        "sponsor_id",
        data_frames["organizations"],
        "id",
        assert_left=True
    )

    # Joins to people
    assert_joins_to_single_row(
        attendances,
        "person_uuid",
        data_frames["people"],
        "uuid",
        assert_left=True
    )

    # Joins to custom_signup_field_values
    assert_joins_to_single_row(
        attendances,
        "id",
        data_frames["custom_signup_field_values"],
        "attendance_id",
        assert_left=False
    )

def test_organizations(data_frames):
    organizations = data_frames["organizations"]
    assert_column_is_unique_and_not_null(organizations, "id")

def test_people(data_frames):
    people = data_frames["people"]
    assert_column_is_unique_and_not_null(people, "uuid")

    # For some reason, these IDs are not unique in data/attendances.json
    # This is IDs are re-used for different people with different email addresses & names
    assert_not_unique(people, "id")
    assert_not_unique(people, "user_id")

def test_events(data_frames):
    events = data_frames["events"]
    assert_column_is_unique_and_not_null(events, "id")

    # Joins to event_campaigns
    assert_joins_to_single_row(
        events,
        "event_campaign_id",
        data_frames["event_campaigns"],
        "id",
        assert_left=True
    )

    # Joins to event_contacts
    assert_joins_to_single_row(
        events,
        "id",
        data_frames["event_contacts"],
        "event_id",
        assert_left=False
    )

    # Joins to sponsors / organizations
    assert_joins_to_single_row(
        events,
        "sponsor_id",
        data_frames["organizations"],
        "id",
        assert_left=True
    )

    # Joins to timeslots
    assert_joins_to_single_row(
        events,
        "id",
        data_frames["timeslots"],
        "event_id",
        assert_left=False
    )

    # Joins to tags
    assert_joins_to_single_row(
        events,
        "id",
        data_frames["event_tags"],
        "event_id",
        assert_left=False
    )

def test_event_campaigns(data_frames):
    event_campaigns = data_frames["event_campaigns"]
    assert_column_is_unique_and_not_null(event_campaigns, "id")

def test_contacts(data_frames):
    contacts = data_frames["contacts"]
    assert_column_is_unique_and_not_null(contacts, "uuid")

    assert_joins_to_single_row(
        contacts,
        "uuid",
        data_frames["event_contacts"],
        "event_contact_uuid",
        assert_left=False
    )

def test_timeslots(data_frames):
    timeslots = data_frames["timeslots"]
    assert_column_is_unique_and_not_null(timeslots, "id")

def test_tags(data_frames):
    tags = data_frames["tags"]
    assert_column_is_unique_and_not_null(tags, "id")

    assert_joins_to_single_row(
        tags,
        "id",
        data_frames["event_tags"],
        "tag_id",
        assert_left=False
    )