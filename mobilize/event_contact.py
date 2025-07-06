from dataclasses import dataclass
from mobilize.api_object import ApiObject


@dataclass
class EventContact(ApiObject):
    """
    A contact for a Mobilize event
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#contact
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    event_id: int
    # Generating a UUID because, for some reason, owner_user_id is not unique in data/attendances.json
    uuid: str
    name: str
    phone_number: str
    owner_user_id: int
    email_adddress: str | None = None