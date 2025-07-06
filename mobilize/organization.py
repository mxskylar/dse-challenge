from dataclasses import dataclass
from mobilize.api_object import ApiObject


@dataclass
class Organization(ApiObject):
    """
    Organization sponsoring or requesting a Mobilize event
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#organization-object
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    id: int
    name: str
    slug: str
    is_coordinated: bool
    is_independent: bool
    is_primary_campaign: bool
    state: str
    district: str
    candidate_name: str
    event_feed_url: str
    created_date: int
    modified_date: int
    # Using string org_type instead of an enum because new values may be added
    org_type: str
    # Using string race_type instead of an enum because new values may be added
    # From the API docs: "null if not a campaign"
    race_type: str | None