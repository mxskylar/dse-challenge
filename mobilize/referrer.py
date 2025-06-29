from dataclasses import dataclass
from mobilize.api_object import ApiObject

@dataclass
class Referrer(ApiObject):
    """TBD"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)