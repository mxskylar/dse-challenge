from dataclasses import dataclass
from mobilize.api_object import ApiObject


@dataclass
class CustomSignupFieldValue(ApiObject):
    """
    Custom data about the signup for an attendance to a Mobilize event
    https://github.com/mobilizeamerica/api?tab=readme-ov-file#customsignupfieldvalue
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    # This should never be null because, according to the API docs:
    # "If the requesting organization is not the event owner or co-owner, custom_signup_field_values is omitted."
    # https://github.com/mobilizeamerica/api?tab=readme-ov-file#attendance-object
    attendance_id: int
    custom_field_id: int
    custom_field_name: str
    # From the API docs: "Exactly one of text_value and boolean_value will be non-null"
    text_value: str | None = None
    boolean_value: str | None = None