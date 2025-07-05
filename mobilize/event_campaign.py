from dataclasses import dataclass
from mobilize.api_object import ApiObject


@dataclass
class EventCampaign(ApiObject):
    """
    The campaign of a Mobilize event
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#eventcampaign
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    id: int
    slug: str
    event_create_page_url: str