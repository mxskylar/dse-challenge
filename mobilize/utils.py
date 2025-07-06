import hashlib
import json
import uuid


class EmptyOrNullObjectException(Exception):
    """
    Raised when attempting to generate a UUID from the hash of an empty or null object,
    which will likely lead to UUID collisions for any rows with the same empty or null values.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

def generate_uuid_from_obj(obj: dict) -> str:
    """
    Generates a UUID seeded from an MD5 hash of the object's data.
    MD5 hashes use 128 bits and have a low chance of collision (1 in 2^128).

    This can be used to generate an ID for a row of data that
    does not already have a unique ID returned by the Mobilize API.
    """
    # Do not hash empty or null objects
    # because this will likely lead to UUID collisions for any rows with the same empty or null values
    if not obj:
        raise EmptyOrNullObjectException(
            "Attempting to hash an empty or null object! This will likely lead to UUID collisions."
        )
    hash = hashlib.md5(json.dumps(obj).encode()).hexdigest()
    return uuid.UUID(hash).hex