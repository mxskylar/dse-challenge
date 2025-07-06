import dataclasses
import os

from types import NoneType, UnionType
from typing import get_args, get_origin


def get_field_with_name(fields, name: str):
    """
    Get field with a matching name
    """
    for field in fields:
        if name == field.name:
            return field
    return None

class UnsupportedTypeException(Exception):
    """
    Raised when a data class's field has a type that is not supported
    because its specific / atomic type is not determinable
    (e.g. union types with more than one non-None types)
    """
    def __init__(self, field_type, reason: str):
        self.message = f"Unsupported type '{field_type}': Unable to determine atomic type because {reason}"
        super().__init__(self.message)

def get_atomic_type(field_type):
    """
    Gets the specific / atomic type (e.g. int) embedded in
    a data class field's overall type (e.g. union type: int | None)

    This supports the types of fields in data classes,
    NOT the types on individual variables or fields from non-data classes.

    Supports data types that are:
    - A single type
    - A union of None and a SINGLE non-None type
    - A list of types, including lists of lists and lists of supported union types
    """
    origin_type = get_origin(field_type)
    if origin_type is UnionType:
        # Get types in union that are not None
        sub_type = get_args(field_type)
        non_none_sub_types = list(filter(lambda t: t is not NoneType, sub_type))
        if len(non_none_sub_types) > 1:
            raise UnsupportedTypeException(field_type, "union contains more than one non-None type")
        return non_none_sub_types[0]
    elif origin_type is list:
        sub_type = get_args(field_type)[0]
        return get_atomic_type(sub_type)
    return field_type

class ApiObject:
    """
    Mobilize API object
    https://github.com/mobilizeamerica/api
    """
    def __init__(self, **kwargs: dict):
        # Assign attributes defined in the data class
        # Attributes not defined will be ignored, even when returned by the API
        fields = dataclasses.fields(self)
        for k, v in kwargs.items():
            field = get_field_with_name(fields, k)
            if field:
                value = v
                # Cast value to class if the raw value is a dictionary
                if type(v) is dict:
                    cls = get_atomic_type(field.type)
                    value = cls(**value)
                # Escape new line characters in strings so that they fit on one line in a CSV file
                elif type(v) is str:
                    value = v.replace(os.linesep, "\\n")
                setattr(self, k, value)