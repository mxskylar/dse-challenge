from dataclasses import dataclass
from enum import Enum
from mobilize.api_object import ApiObject

class SmsOptInStatus(Enum):
    UNSPECIFIED = "UNSPECIFIED"
    OPT_IN = "OPT_IN"
    OPT_OUT = "OPT_OUT"

@dataclass
class Person(ApiObject):
    """
    Person attending a Mobilize event
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#person-object
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id: int
    # Ignoring person_id because it will eventually be deprecated
    user_id: int
    created_date: int
    modified_date: int
    given_name: str
    family_name: str
    sms_opt_in_status: SmsOptInStatus
    blocked_date: int

    # Original nested data for timeslots is initially preserved
    # because it will be decoupled into a separate table
    #email_addresses: list[Email] = []
    #phone_numbers: list[Phone] = []
    #postal_addresses: list[Address] = []