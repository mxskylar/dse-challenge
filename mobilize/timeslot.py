from dataclasses import dataclass
from mobilize.api_object import ApiObject


@dataclass
class Timeslot(ApiObject):
    """
    Timeslot of a Mobilize event
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#timeslot
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    id: int
    event_id: int
    start_date: int
    end_date: int
    is_full: bool
    # Although instructions is not marked as optional in the API docs,
    # it is often excluded from data returned by the API
    instructions: str | None = None
    max_attendees: int | None = None