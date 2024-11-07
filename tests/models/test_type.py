# -*- coding: utf-8 -*-
"""Tests for the Type class."""

import sys
import pytest

from stalker import Asset, Entity, Type


@pytest.fixture(scope="function")
def setup_type_tests():
    """Set up tests for the Type class."""
    data = dict()
    data["kwargs"] = {
        "name": "test type",
        "code": "test",
        "description": "this is a test type",
        "target_entity_type": "SimpleEntity",
    }

    data["test_type"] = Type(**data["kwargs"])

    # create another Entity with the same name of the
    # test_type for __eq__ and __ne__ tests
    data["entity1"] = Entity(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Ticket class."""
    assert Type.__auto_name__ is False


def test_equality(setup_type_tests):
    """equality operator."""
    data = setup_type_tests
    new_type2 = Type(**data["kwargs"])

    data["kwargs"]["target_entity_type"] = "Asset"
    new_type3 = Type(**data["kwargs"])

    data["kwargs"]["name"] = "a different type"
    data["kwargs"]["description"] = "this is a different type"
    new_type4 = Type(**data["kwargs"])

    assert data["test_type"] == new_type2
    assert not data["test_type"] == new_type3
    assert not data["test_type"] == new_type4
    assert not data["test_type"] == data["entity1"]


def test_inequality(setup_type_tests):
    """inequality operator."""
    data = setup_type_tests
    new_type2 = Type(**data["kwargs"])

    data["kwargs"]["target_entity_type"] = "Asset"
    new_type3 = Type(**data["kwargs"])

    data["kwargs"]["name"] = "a different type"
    data["kwargs"]["description"] = "this is a different type"
    new_type4 = Type(**data["kwargs"])

    assert not data["test_type"] != new_type2
    assert data["test_type"] != new_type3
    assert data["test_type"] != new_type4
    assert data["test_type"] != data["entity1"]


def test_plural_class_name(setup_type_tests):
    """plural name of Type class."""
    data = setup_type_tests
    assert data["test_type"].plural_class_name == "Types"


def test_target_entity_type_argument_cannot_be_skipped(setup_type_tests):
    """TypeError raised if the created Type doesn't have any target_entity_type."""
    data = setup_type_tests
    data["kwargs"].pop("target_entity_type")
    with pytest.raises(TypeError) as cm:
        Type(**data["kwargs"])
    assert str(cm.value) == "Type.target_entity_type cannot be None"


def test_target_entity_type_argument_cannot_be_none(setup_type_tests):
    """TypeError raised if the target_entity_type argument is None."""
    data = setup_type_tests
    data["kwargs"]["target_entity_type"] = None
    with pytest.raises(TypeError) as cm:
        Type(**data["kwargs"])
    assert str(cm.value) == "Type.target_entity_type cannot be None"


def test_target_entity_type_argument_cannot_be_empty_string(setup_type_tests):
    """ValueError raised if the target_entity_type argument is an empty string."""
    data = setup_type_tests
    data["kwargs"]["target_entity_type"] = ""
    with pytest.raises(ValueError) as cm:
        Type(**data["kwargs"])
    assert str(cm.value) == "Type.target_entity_type cannot be empty"


def test_target_entity_type_argument_accepts_strings(setup_type_tests):
    """target_entity_type argument accepts strings."""
    data = setup_type_tests
    data["kwargs"]["target_entity_type"] = "Asset"
    # no error should be raised
    Type(**data["kwargs"])


def test_target_entity_type_argument_accepts_python_classes(setup_type_tests):
    """target_entity_type argument is given as a Python class converted to a string."""
    data = setup_type_tests
    data["kwargs"]["target_entity_type"] = Asset
    new_type = Type(**data["kwargs"])
    assert new_type.target_entity_type == "Asset"


def test_target_entity_type_attribute_is_read_only(setup_type_tests):
    """target_entity_type attribute is read-only."""
    data = setup_type_tests
    with pytest.raises(AttributeError) as cm:
        data["test_type"].target_entity_type = "Asset"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute",
        11: "property of 'Type' object has no setter",
        12: "property of 'Type' object has no setter",
    }.get(
        sys.version_info.minor,
        "property '_target_entity_type_getter' of 'Type' object has no setter",
    )

    assert str(cm.value) == error_message


def test_target_entity_type_attribute_is_working_as_expected(setup_type_tests):
    """target_entity_type attribute is working as expected."""
    data = setup_type_tests
    assert data["test_type"].target_entity_type == data["kwargs"]["target_entity_type"]


def test__hash__is_working_as_expected(setup_type_tests):
    """__hash__ is working as expected."""
    data = setup_type_tests
    result = hash(data["test_type"])
    assert isinstance(result, int)
    assert result == data["test_type"].__hash__()
