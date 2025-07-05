import pytest

from mobilize.utils import EmptyOrNullObjectException, generate_uuid_from_obj


def test_generates_unique_uuids():
    hash1 = generate_uuid_from_obj({"foo": "bar"})
    hash2 = generate_uuid_from_obj({"key": "val"})
    assert hash1 != hash2, "UUIDs generated from hash of different payloads should be unique"

def test_generate_uuid_from_empty_object():
    # Generating UUIDs from the hash of empty objects is not allowed
    with pytest.raises(EmptyOrNullObjectException) as e_info:
        generate_uuid_from_obj({})

def test_generate_uuid_from_null_object():
    # Generating UUIDs from the hash of null objects is not allowed
    with pytest.raises(EmptyOrNullObjectException) as e_info:
        generate_uuid_from_obj(None)