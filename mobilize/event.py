from dataclasses import dataclass
from enum import Enum
from mobilize.api_object import ApiObject
from mobilize.organization import Organization
from mobilize.timeslot import Timeslot

class EventDataVisibility(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

class EventAccessbilityStatus(Enum):
    ACCESSIBLE = "ACCESSIBLE"
    NOT_ACCESSIBLE = "NOT_ACCESSIBLE"
    NOT_SURE = "NOT_SURE"

class EventApprovalStatus(Enum):
    APPROVED = "APPROVED"
    NEEDS_APPROVAL = "NEEDS_APPROVAL"
    REJECTED = "REJECTED"
    NEEDS_HOST_VERIFICATION = "NEEDS_HOST_VERIFICATION"

@dataclass
class Event(ApiObject):
    """
    An event managed in the Mobilize platform
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#event-object
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    # Defining event_type as a string rather than an enum because
    # new values may be added to the enum by the API
    event_type: str
    
    # If the requesting organization is independent
    # and the event’s organization is coordinated, all but event_type is omitted.
    id: int | None = None
    title: str | None = None
    description: str | None = None
    featured_image_url: str | None = None
    high_priority: bool | None = None
    sponsor: Organization | None = None
    #location: Location | None = None
    timezone: str | None = None
    browser_url: str | None = None
    created_date: int | None = None
    modified_date: int | None = None
    visibility: EventDataVisibility | None = None
    address_visibility: EventDataVisibility | None = None
    created_by_volunteer_host: bool | None = None
    is_virtual: bool | None = None
    virtual_action_url: str | None = None
    #contact: Contact | None = None
    accessibility_status: EventAccessbilityStatus | None = None

    # Original nested data for timeslots is initially preserved
    # because it will be decoupled into a separate table
    timeslots: list[Timeslot] | None = None