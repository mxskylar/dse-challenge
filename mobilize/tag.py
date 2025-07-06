from dataclasses import dataclass
from mobilize.api_object import ApiObject


@dataclass
class Tag(ApiObject):
    """
    A tag for a Mobilize event
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#tag
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    id: int
    event_id: int
    name: str