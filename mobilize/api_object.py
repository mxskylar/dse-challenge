import dataclasses
import json
import hashlib
from types import NoneType, UnionType
from typing import get_args, get_origin
import uuid

class NestedJsonEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that returns dictionary of all nested class objects within an object
    https://docs.python.org/3/library/json.html
    """
    def default(self, obj):
        # If value has attribute __dict__, it's a class object.
        # Return dictionary of object values.
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)

def get_class(data_type):
    """
    Gets class embedded in data type

    Supports data types that are:
    - A single class
    - A union of None and a SINGLE class
    - A list of classes, including lists of lists & lists of supported union types
    """
    origin_type = get_origin(data_type)
    if origin_type is UnionType:
        # Get types in union that are not None
        types = list(filter(lambda data_type: data_type is not NoneType, get_args(data_type)))
        if len(types) > 1:
            raise Exception(
                f"Failed find class in type '{data_type}' " +
                "Union contains more than one non-None type. " +
                "This is not supported."
            )
        return types[0]
    elif origin_type is list:
        return get_class(origin_type)
    return data_type
        

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
            # Get key with same name as the key for the argument
            def get_matching_field():
                for field in fields:
                    if k == field.name:
                        return field
                return None
            field = get_matching_field()
            if field:
                value = v
                if type(v) is dict:
                    cls = get_class(field.type)
                    value = cls(**value)
                setattr(self, k, value)
    
    def __get_hash_id__(self) -> str:
        """
        Generates a UUID seeded from an MD5 hash of the object's data.
        MD5 hashes use 128 bits and have a low chance of collision (1 in 2^128).

        Generating UUIDs is necessary because some object's IDs are ommitted
        due to campaign finance restrictions. From the Mobilize API docs:

        "If the requesting organization is independent and the event's organization is coordinated, id is omitted."
        https://github.com/mobilizeamerica/api?tab=readme-ov-file#attendance-object

        Additionally, generating UUIDs from a hash of a row's data ensures that
        duplicate rows can easily be dropped from a Pandas DataFrame
        while still preserving a unique ID that can still join to another table as expected.
        """
        data = json.dumps(self.__dict__, cls=NestedJsonEncoder)
        hash = hashlib.md5(data.encode()).hexdigest()
        return uuid.UUID(hash).hex
