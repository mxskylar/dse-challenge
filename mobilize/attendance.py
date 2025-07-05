from dataclasses import dataclass
from enum import Enum
from mobilize.api_object import ApiObject
from mobilize.person import Person
from mobilize.event import Event
from mobilize.organization import Organization
from mobilize.timeslot import Timeslot
from mobilize.custom_signup_field_value import CustomSignupFieldValue


class AttendanceStatus(Enum):
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"
    CONFIRMED = "CONFIRMED"

@dataclass
class Attendance(ApiObject):
    """
    Attendance to a Mobilize event
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#attendance-object
    """
    def __init__(self, **kwargs):
        # Referrer (nested data is normalized)
        referrer_args = {}
        if "referrer" in kwargs and kwargs["referrer"]:
            referrer_args = {f"referrer_{key}":value for key, value in kwargs["referrer"].items()}
        
        # Timeslot (most nested data is normalized)
        timeslot_args = {}
        if "timeslot" in kwargs and kwargs["timeslot"]:
            timeslot_args = {f"timeslot_{key}":value for key, value in kwargs["timeslot"].items() if key != "id"}
        
        # Event (some nested data is normalized)
        event_args = {}
        if "event" in kwargs and kwargs["event"]:
            event = kwargs["event"]
            if "id" in event:
                # This ID can join to the events table
                event_id = event["id"]
                event_args["event_id"] = event_id
                if "timeslot" in kwargs and kwargs["timeslot"]:
                    kwargs["timeslot"]["event_id"] = event_id
            if "event_type" in event:
                event_args["event_type"] = event["event_type"]
        
        # Person & Sponsor (nested IDs are normalized so they can join to other tables)
        other_args = {}
        if "person" in kwargs and kwargs["person"] and "id" in kwargs["person"]:
            other_args["person_id"] = kwargs["person"]["id"]
        if "sponsor" in kwargs and kwargs["sponsor"] and "id" in kwargs["sponsor"]:
            other_args["sponsor_id"] = kwargs["sponsor"]["id"]
        
        # Custom signup field values
        custom_signup_field_value_args = {}
        # If custom_signup_field_values is set, there should always be a non-null ID.
        # From the API docs on custom_signup_field_values:
        # "If the requesting organization is not the event owner or co-owner, this is omitted."
        # From the API docs on id:
        # "If the requesting organization is independent and the event’s organization is coordinated, this is omitted."
        # https://github.com/mobilizeamerica/api?tab=readme-ov-file#attendance-object
        # This is verified in tests/test_get_tables.py:test_attendance_join_custom_signup_field_values
        if "custom_signup_field_values" in kwargs and "id" in kwargs:
            values = []
            for value in kwargs["custom_signup_field_values"]:
                # Enables the attendance and custom_signup_field_value tables to be joined
                values.append({**value, "attendance_id": kwargs["id"]})
            custom_signup_field_value_args = {"custom_signup_field_values": values}
        
        args = {
            **kwargs,
            **referrer_args,
            **timeslot_args,
            **event_args,
            **other_args,
            **custom_signup_field_value_args
        }
        super().__init__(**args)

    created_date: int
    modified_date: int
    status: AttendanceStatus
    attended: bool
    person_id: int
    event_type: str
    referrer_utm_source: str	
    referrer_utm_medium: str	
    referrer_utm_campaign: str	
    referrer_utm_term: str	
    referrer_utm_content: str	
    referrer_url: str
    timeslot_start_date: int
    timeslot_end_date: int
    timeslot_is_full: bool

    # Original nested data for these attributes is initially preserved
    # because they will be decoupled into separate tables
    person: Person
    event: Event
    timeslot: Timeslot
    sponsor: Organization | None = None
    custom_signup_field_values: list[CustomSignupFieldValue] | None = None

    # If the requesting organization is independent
    # and the event’s organization is coordinated, the ID omitted.
    id: int | None = None
    event_id: int | None = None
    sponsor_id: int | None = None
    # Although instructions is not marked as optional in the API docs,
    # it is often excluded from data returned by the API
    timeslot_instructions: str | None = None
    timeslot_max_attendees: int | None = None