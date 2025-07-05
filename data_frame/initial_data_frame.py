from enum import Enum
from mobilize.attendance import Attendance
from mobilize.custom_signup_field_value import CustomSignupFieldValue
from mobilize.event_campaign import EventCampaign
from mobilize.event_contact import EventContact
from mobilize.organization import Organization
from mobilize.person import Person
from mobilize.tag import Tag
from mobilize.timeslot import Timeslot
from mobilize.event import Event


class InitialDataFrameName(Enum):
    """
    Enum for tables to insert data into
    """
    ATTENDANCES = "attendances"
    CUSTOM_SIGNUP_FIELD_VALUES = "custom_signup_field_values"
    TIMESLOTS = "timeslots"
    EVENTS = "events"
    EVENT_CONTACTS = "event_contacts"
    EVENT_CAMPAIGNS = "event_campaigns"
    TAGS = "tags"
    ORGANIZATIONS = "organizations"
    PEOPLE = "people"

def get_api_object_class_for_table(df_name: InitialDataFrameName):
    """
    Returns the class for an ApiObject that corresponds to a Table
    """
    match df_name:
        case InitialDataFrameName.ATTENDANCES:
            return Attendance
        case InitialDataFrameName.CUSTOM_SIGNUP_FIELD_VALUES:
            return CustomSignupFieldValue
        case InitialDataFrameName.TIMESLOTS:
            return Timeslot
        case InitialDataFrameName.EVENTS:
            return Event
        case InitialDataFrameName.EVENT_CONTACTS:
            return EventContact
        case InitialDataFrameName.EVENT_CAMPAIGNS:
            return EventCampaign
        case InitialDataFrameName.TAGS:
            return Tag
        case InitialDataFrameName.ORGANIZATIONS:
            return Organization
        case InitialDataFrameName.PEOPLE:
            return Person
        case _:
            return None