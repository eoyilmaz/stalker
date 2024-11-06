# -*- coding: utf-8 -*-
"""Tests for the Status class."""

import pytest

from stalker import Entity, Status


@pytest.fixture(scope="function")
def setup_status_tests():
    """Set up tests for the stalker.models.status.Status class."""
    data = dict()
    data["kwargs"] = {
        "name": "Complete",
        "description": "use this if the object is complete",
        "code": "CMPLT",
    }

    # create an entity object with same kwargs for __eq__ and __ne__ tests
    # (it should return False for __eq__ and True for __ne__ for same
    # kwargs)
    data["entity1"] = Entity(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Status class."""
    assert Status.__auto_name__ is False


def test_equality(setup_status_tests):
    """equality of two statuses."""
    data = setup_status_tests
    status1 = Status(**data["kwargs"])
    status2 = Status(**data["kwargs"])

    data["kwargs"]["name"] = "Work In Progress"
    data["kwargs"]["description"] = "use this if the object is still in progress"
    data["kwargs"]["code"] = "WIP"

    status3 = Status(**data["kwargs"])

    assert status1 == status2
    assert not status1 == status3
    assert not status1 == data["entity1"]


def test_status_and_string_equality_in_status_name(setup_status_tests):
    """status can be compared with a string matching the Status.name."""
    data = setup_status_tests
    a_status = Status(**data["kwargs"])
    assert a_status == data["kwargs"]["name"]
    assert a_status == data["kwargs"]["name"].lower()
    assert a_status == data["kwargs"]["name"].upper()
    assert a_status != "another name"


def test_status_and_string_equality_in_status_code(setup_status_tests):
    """status can be compared with a string matching the Status.code."""
    data = setup_status_tests
    a_status = Status(**data["kwargs"])
    assert a_status == data["kwargs"]["code"]
    assert a_status == data["kwargs"]["code"].lower()
    assert a_status == data["kwargs"]["code"].upper()


def test_inequality(setup_status_tests):
    """inequality of two statuses."""
    data = setup_status_tests
    status1 = Status(**data["kwargs"])
    status2 = Status(**data["kwargs"])
    data["kwargs"]["name"] = "Work In Progress"
    data["kwargs"]["description"] = "use this if the object is still in progress"
    data["kwargs"]["code"] = "WIP"

    status3 = Status(**data["kwargs"])

    assert not status1 != status2
    assert status1 != status3
    assert status1 != data["entity1"]


def test_status_and_string_inequality_in_status_name(setup_status_tests):
    """status can be compared with a string."""
    data = setup_status_tests
    a_status = Status(**data["kwargs"])
    assert not a_status != data["kwargs"]["name"]
    assert not a_status != data["kwargs"]["name"].lower()
    assert not a_status != data["kwargs"]["name"].upper()
    assert a_status != "another name"


def test_status_and_string_inequality_in_status_code(setup_status_tests):
    """status can be compared with a string."""
    data = setup_status_tests
    a_status = Status(**data["kwargs"])
    assert not a_status != data["kwargs"]["code"]
    assert not a_status != data["kwargs"]["code"].lower()
    assert not a_status != data["kwargs"]["code"].upper()


def test__hash__is_working_as_expected(setup_status_tests):
    """__hash__ is working as expected."""
    data = setup_status_tests
    data["test_status"] = Status(**data["kwargs"])
    result = hash(data["test_status"])
    assert isinstance(result, int)
    assert result == data["test_status"].__hash__()
