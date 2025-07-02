import dataclasses
from dataclasses import dataclass
import json
from mobilize.api_object import UnsupportedTypeException, get_atomic_type, get_field_with_name
from mobilize.attendance import Attendance
from mobilize.event import Event
from mobilize.person import Person
from process_data import ATTENDANCES_DATA_FILE
import pytest

def get_attendance():
    with open(ATTENDANCES_DATA_FILE) as f:
        attendances = json.loads(f.read())
        return Attendance(**attendances[0])

@dataclass
class DataClass:
    """
    Data class with a field for each use case to test
    """
    def __init__(self, **kwargs: dict):
        self.single_class = get_attendance()
        self.list_of_classes = []
        self.list_of_unions = []
        self.list_of_lists = []
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    single_class: Attendance
    valid_union: Attendance | None
    invalid_union: Attendance | str | None
    list_of_classes: list[Attendance]
    list_of_unions: list[Attendance | None]
    list_of_lists: list[list[Attendance]]

def get_field_type(field_name: str, value=None):
    """
    Returns the type of a data class's field to test with
    """
    kwargs = {} if value is None else {field_name: value}
    test_class = DataClass(**kwargs)
    fields = dataclasses.fields(test_class)
    print(fields)
    field = get_field_with_name(fields, field_name)
    return field.type

def test_single_class():
    single_class_type = get_field_type("single_class")
    assert get_atomic_type(single_class_type) is Attendance, "Atomic type should be Attendance class"

def test_valid_union():
    # Valid union with a class value
    valid_union_type_class_value = get_field_type("valid_union", get_attendance())
    assert get_atomic_type(valid_union_type_class_value) is Attendance, "Atomic type should be Attendance class"
    # Valid union with a None value
    valid_union_type_none_value = get_field_type("valid_union", None)
    assert get_atomic_type(valid_union_type_none_value) is Attendance, "Atomic type should be Attendance class"

def test_invalid_union():
    invalid_union_type = get_field_type("invalid_union", get_attendance())
    with pytest.raises(UnsupportedTypeException) as e_info:
        get_atomic_type(invalid_union_type)

def test_list_of_classes():
    list_of_classes_type = get_field_type("list_of_classes", [get_attendance()])
    assert get_atomic_type(list_of_classes_type) is Attendance, "Atomic type should be Attendance class"

def test_list_of_unions():
    # List of unions with class values
    list_of_unions_type_class_value = get_field_type("list_of_unions", [get_attendance()])
    assert get_atomic_type(list_of_unions_type_class_value) is Attendance, "Atomic type should be Attendance class"
    # List of unions with None values
    list_of_unions_type_none_value = get_field_type("list_of_unions", [None])
    assert get_atomic_type(list_of_unions_type_none_value) is Attendance, "Atomic type should be Attendance class"

def test_list_of_lists():
    list_of_lists_type = get_field_type("list_of_lists", [[get_attendance()]])
    assert get_atomic_type(list_of_lists_type) is Attendance, "Atomic type should be Attendance class"