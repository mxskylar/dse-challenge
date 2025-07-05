from dataclasses import dataclass
from enum import Enum
from mobilize.api_object import ApiObject


class MultipleContactsException(Exception):
    """
    Raised when there is more than one form of contact for a person
    (e.g. email address, phone number, or postal code).

    According to the API, this should not be possible.
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#person-object
    """
    def __init__(self, api_key):
        self.message = f"Mobilize API returned more than one contact under '{api_key}'. Only one is expected."
        super().__init__(self.message)

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
        # Contacts
        # According to the API docs, these lists will never contain more than one item
        # and they will always be the primary contact for the person
        contact_types = [
            ("email_addresses", "address", "email_address"),
            ("phone_numbers", "number", "phone_number"),
            ("postal_addresses", "postal_code", "postal_code")
        ]
        contact_args = {}
        for api_key, nested_key, column_name in contact_types:
            if api_key in kwargs and kwargs[api_key]:
                contacts = kwargs[api_key]
                if len(contacts) > 1:
                    raise MultipleContactsException(api_key)
                if len(contacts) > 0:
                    # According to the API docs, only this column will have useful data
                    # because primary is always true
                    # https://github.com/mobilizeamerica/api?tab=readme-ov-file#email
                    contact_args[column_name] = contacts[0][nested_key]
        
        args = {
            **kwargs,
            **contact_args
        }
        super().__init__(**args)

    # Generating a UUID because, for some reason, neither id nor user_id are unique in data/attendances.json
    uuid: str
    id: int
    # Ignoring person_id because it will eventually be deprecated
    user_id: int
    created_date: int
    modified_date: int
    given_name: str
    family_name: str
    sms_opt_in_status: SmsOptInStatus
    blocked_date: int
    phone_number: str
    postal_code: str
    # From the API docs:
    # "The email_addresses list may be empty however if the Person is not affiliated with the requesting Organization,
    # and the Person's affiliated Organization has restrictions on what volunteer data may be shared."
    email_address: str | None = None