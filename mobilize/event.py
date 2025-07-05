from dataclasses import dataclass
from enum import Enum
from mobilize.api_object import ApiObject
from mobilize.event_campaign import EventCampaign
from mobilize.organization import Organization
from mobilize.timeslot import Timeslot
from mobilize.tag import Tag


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
        # Contact (most nested data is normalized)
        contact_args = {}
        if "contact" in kwargs and kwargs["contact"]:
            contact =  kwargs["contact"]
            contact_args = {f"contact_{key}":value for key, value in contact.items() if key != "owner_user_id"}
            if "owner_user_id" in contact:
                contact_args["owner_user_id"] = contact["owner_user_id"]
        
        # Location (most nested data is normalized)
        location_args = {}
        if "location" in kwargs and kwargs["location"]:
            location = kwargs["location"]
            key_deny_list = ["address_lines", "location"]
            location_args = {key:value for key, value in location.items() if key not in key_deny_list}
            if "address_lines" in location:
                # Join address by escaped new line character,
                # which allows the string value to fit on a single line in a CSV file
                location_args["address"] = "\\n".join(location["address_lines"])
            if "location" in location:
                nested_location = location["location"]
                if "latitude" in nested_location:
                    location_args["location_latitude"] = nested_location["latitude"]
                if "longitude" in nested_location:
                    location_args["location_longitude"] = nested_location["longitude"]

        # Timeslots
        timeslot_args = {}
        if "timeslots" in kwargs and kwargs["timeslots"] and "id" in kwargs and kwargs["id"]:
            timeslots = []
            for timeslot in kwargs["timeslots"]:
                # Enables the event and timeslot tables to be joined
                timeslots.append({**timeslot, "event_id": kwargs["id"]})
            timeslot_args = {"timeslots": timeslots}
        
        # Tags
        tag_args = {}
        if "tags" in kwargs and kwargs["tags"] and "id" in kwargs:
            tags = []
            for tag in kwargs["tags"]:
                # Enables the event and tag tables to be joined
                tags.append({**tag, "event_id": kwargs["id"]})
            timeslot_args = {"timeslots": timeslots}
        
        # Event Campaign & Sponsor (nested IDs are normalized so they can join to other tables)
        other_args = {}
        if "event_campaign" in kwargs and kwargs["event_campaign"] and "id" in kwargs["event_campaign"]:
            other_args["event_campaign_id"] = kwargs["event_campaign"]["id"]
        if "sponsor" in kwargs and kwargs["sponsor"] and "id" in kwargs["sponsor"]:
            other_args["sponsor_id"] = kwargs["sponsor"]["id"]
        
        args = {
            **kwargs,
            **contact_args,
            **location_args,
            **timeslot_args,
            **tag_args,
            **other_args
        }
        super().__init__(**args)
    
    # Defining event_type as a string rather than an enum because
    # new values may be added to the enum by the API
    event_type: str
    
    # If the requesting organization is independent
    # and the event’s organization is coordinated, all but event_type is omitted.
    id: int | None = None
    event_campaign_id: int | None = None
    title: str | None = None
    description: str | None = None
    featured_image_url: str | None = None
    high_priority: bool | None = None
    timezone: str | None = None
    browser_url: str | None = None
    created_date: int | None = None
    modified_date: int | None = None
    visibility: EventDataVisibility | None = None
    address_visibility: EventDataVisibility | None = None
    created_by_volunteer_host: bool | None = None
    is_virtual: bool | None = None
    virtual_action_url: str | None = None
    accessibility_status: EventAccessbilityStatus | None = None
    accessbility_notes: str | None = None
    approval_status: EventApprovalStatus | None = None
    instructions: str | None = None
    contact_name: str | None = None
    contact_email_adddress: str | None = None
    contact_phone_number: str | None = None
    owner_user_id: int | None = None
    venue: str | None = None
    address: str | None = None
    locality: str | None = None
    region: str | None = None
    country: str | None = None
    postal_code: str | None = None
    location_latitude: float | None = None
    location_longitude: float | None = None
    congressional_district: str | None = None
    state_leg_district: str | None = None
    state_senate_district: str | None = None

    # Original nested data for timeslots is initially preserved
    # because it will be decoupled into a separate table
    timeslots: list[Timeslot] | None = None
    tags: list[Tag] | None = None
    event_campaign: EventCampaign | None = None
    sponsor: Organization | None = None