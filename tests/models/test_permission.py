# -*- coding: utf-8 -*-
"""Permission class tests."""

import sys

import pytest

from stalker.models.auth import Permission


@pytest.fixture(scope="function")
def setup_permission_tests():
    """Set up the tests for the Permission class."""
    data = dict()
    data["kwargs"] = {"access": "Allow", "action": "Create", "class_name": "Project"}
    data["test_permission"] = Permission(**data["kwargs"])
    return data


def test_access_argument_is_skipped(setup_permission_tests):
    """TypeError is raised if the access argument is skipped."""
    data = setup_permission_tests
    data["kwargs"].pop("access")
    with pytest.raises(TypeError) as cm:
        Permission(**data["kwargs"])

    if sys.version_info[0] >= 3:
        assert (
            str(cm.value)
            == "__init__() missing 1 required positional argument: 'access'"
        )
    else:
        assert str(cm.value) == "__init__() takes exactly 4 arguments (3 given)"


def test_access_argument_is_none(setup_permission_tests):
    """TypeError is raised if the access argument is None."""
    data = setup_permission_tests
    data["kwargs"]["access"] = None
    with pytest.raises(TypeError) as cm:
        Permission(**data["kwargs"])

    assert (
        str(cm.value) == "Permission.access should be an instance of str not NoneType"
    )


def test_access_argument_accepts_only_allow_or_deny_as_value(setup_permission_tests):
    """ValueError is raised if access is something other than 'Allow' or 'Deny'."""
    data = setup_permission_tests
    data["kwargs"]["access"] = "Allowed"
    with pytest.raises(ValueError) as cm:
        Permission(**data["kwargs"])
    assert str(cm.value) == 'Permission.access should be "Allow" or "Deny" not Allowed'


def test_access_argument_is_setting_access_attribute_value(setup_permission_tests):
    """access argument is setting the access attribute value correctly."""
    data = setup_permission_tests
    assert data["kwargs"]["access"] == data["test_permission"].access


def test_access_attribute_is_read_only(setup_permission_tests):
    """access attribute is read only."""
    data = setup_permission_tests
    with pytest.raises(AttributeError) as cm:
        data["test_permission"].access = "Deny"

    error_message = (
        "can't set attribute"
        if sys.version_info.minor < 11
        else "property '_access_getter' of 'Permission' object has no setter"
    )

    assert str(cm.value) == error_message


def test_action_argument_is_skipped_will_raise_a_type_error(setup_permission_tests):
    """TypeError is raised if the action argument is skipped."""
    data = setup_permission_tests
    data["kwargs"].pop("action")
    with pytest.raises(TypeError) as cm:
        Permission(**data["kwargs"])

    if sys.version_info[0] >= 3:
        assert (
            str(cm.value)
            == "__init__() missing 1 required positional argument: 'action'"
        )
    else:
        # Python 2.7
        assert str(cm.value) == "__init__() takes exactly 4 arguments (3 given)"


def test_action_argument_is_none(setup_permission_tests):
    """TypeError is raised if the action argument is set to None."""
    data = setup_permission_tests
    data["kwargs"]["action"] = None
    with pytest.raises(TypeError) as cm:
        Permission(**data["kwargs"])

    assert (
        str(cm.value) == "Permission.action should be an instance of str not NoneType"
    )


def test_action_argument_accepts_default_values_only(setup_permission_tests):
    """ValueError is raised if the action arg is not in the defaults.DEFAULT_ACTIONS."""
    data = setup_permission_tests
    data["kwargs"]["action"] = "Add"
    with pytest.raises(ValueError) as cm:
        Permission(**data["kwargs"])

    assert (
        str(cm.value) == "Permission.action should be one of the values of ['Create', "
        "'Read', 'Update', 'Delete', 'List'] not 'Add'"
    )


def test_action_argument_is_setting_the_argument_attribute(setup_permission_tests):
    """action argument is setting the argument attribute value."""
    data = setup_permission_tests
    assert data["kwargs"]["action"] == data["test_permission"].action


def test_action_attribute_is_read_only(setup_permission_tests):
    """action attribute is read only."""
    data = setup_permission_tests
    with pytest.raises(AttributeError) as cm:
        data["test_permission"].action = "Add"

    error_message = (
        "can't set attribute"
        if sys.version_info.minor < 11
        else "property '_action_getter' of 'Permission' object has no setter"
    )

    assert str(cm.value) == error_message


def test_class_name_argument_skipped(setup_permission_tests):
    """TypeError is raised if the class_name argument is skipped."""
    data = setup_permission_tests
    data["kwargs"].pop("class_name")
    with pytest.raises(TypeError) as cm:
        Permission(**data["kwargs"])

    if sys.version_info[0] >= 3:
        assert (
            str(cm.value) == "__init__() missing 1 required positional argument: "
            "'class_name'"
        )
    else:
        # Python 2.7
        assert str(cm.value) == "__init__() takes exactly 4 arguments (3 given)"


def test_class_name_argument_is_none(setup_permission_tests):
    """TypeError is raised if the class_name argument is None."""
    data = setup_permission_tests
    data["kwargs"]["class_name"] = None
    with pytest.raises(TypeError) as cm:
        Permission(**data["kwargs"])

    assert (
        str(cm.value)
        == "Permission.class_name should be an instance of str not NoneType"
    )


def test_class_name_argument_is_not_a_string(setup_permission_tests):
    """TypeError is raised if the class_name argument is not a string instance."""
    data = setup_permission_tests
    data["kwargs"]["class_name"] = 10
    with pytest.raises(TypeError) as cm:
        Permission(**data["kwargs"])

    assert str(cm.value) == "Permission.class_name should be an instance of str not int"


def test_class_name_argument_is_setting_the_class_name_attribute_value(
    setup_permission_tests,
):
    """class_name argument value is correctly passed to the class_name attribute."""
    data = setup_permission_tests
    assert data["test_permission"].class_name == data["kwargs"]["class_name"]


def test_class_name_attribute_is_read_only(setup_permission_tests):
    """class_name attribute is read only."""
    data = setup_permission_tests
    with pytest.raises(AttributeError) as cm:
        data["test_permission"].class_name = "Asset"

    error_message = (
        "can't set attribute"
        if sys.version_info.minor < 11
        else "property '_class_name_getter' of 'Permission' object has no setter"
    )

    assert str(cm.value) == error_message
