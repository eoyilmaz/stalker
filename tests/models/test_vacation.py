# -*- coding: utf-8 -*-
"""Tests for the Vacation class."""
import datetime
import sys

import pytest
import pytz

from stalker import Type
from stalker import User
from stalker import Vacation


@pytest.fixture(scope="function")
def setup_vacation_tests():
    """Set up test for the Vacation class."""
    data = dict()
    # create a user
    data["test_user"] = User(
        name="Test User",
        login="testuser",
        email="testuser@test.com",
        password="secret",
    )

    # vacation type
    data["personal_vacation"] = Type(
        name="Personal", code="PERS", target_entity_type="Vacation"
    )

    data["studio_vacation"] = Type(
        name="Studio Wide", code="STD", target_entity_type="Vacation"
    )

    data["kwargs"] = {
        "user": data["test_user"],
        "type": data["personal_vacation"],
        "start": datetime.datetime(2013, 6, 6, 10, 0, tzinfo=pytz.utc),
        "end": datetime.datetime(2013, 6, 10, 19, 0, tzinfo=pytz.utc),
    }

    data["test_vacation"] = Vacation(**data["kwargs"])
    return data


def test_strictly_typed_is_false():
    """__strictly_typed_ attribute is False for Vacation class."""
    assert Vacation.__strictly_typed__ is False


def test_user_argument_is_skipped(setup_vacation_tests):
    """user argument can be skipped skipped."""
    data = setup_vacation_tests
    data["kwargs"].pop("user")
    Vacation(**data["kwargs"])


def test_user_argument_is_none(setup_vacation_tests):
    """user argument can be set to None."""
    data = setup_vacation_tests
    data["kwargs"]["user"] = None
    Vacation(**data["kwargs"])


def test_user_attribute_is_none(setup_vacation_tests):
    """user attribute cat be set to None."""
    data = setup_vacation_tests
    data["test_vacation"].user = None


def test_user_argument_is_not_a_user_instance(setup_vacation_tests):
    """TypeError raised if the user arg is not a User instance."""
    data = setup_vacation_tests
    data["kwargs"]["user"] = "not a user instance"
    with pytest.raises(TypeError) as cm:
        Vacation(**data["kwargs"])

    assert str(cm.value) == (
        "Vacation.user should be an instance of stalker.models.auth.User, "
        "not str: 'not a user instance'"
    )


def test_user_attribute_is_not_a_user_instance(setup_vacation_tests):
    """TypeError raised if the user attr is not a User instance."""
    data = setup_vacation_tests
    with pytest.raises(TypeError) as cm:
        data["test_vacation"].user = "not a user instance"

    assert str(cm.value) == (
        "Vacation.user should be an instance of stalker.models.auth.User, "
        "not str: 'not a user instance'"
    )


def test_user_argument_is_working_properly(setup_vacation_tests):
    """user argument value is correctly passed to the user attribute."""
    data = setup_vacation_tests
    assert data["test_vacation"].user == data["kwargs"]["user"]


def test_user_attribute_is_working_properly(setup_vacation_tests):
    """user attribute is working properly."""
    data = setup_vacation_tests
    new_user = User(
        name="test user 2", login="testuser2", email="test@user.com", password="secret"
    )

    assert data["test_vacation"].user != new_user
    data["test_vacation"].user = new_user
    assert data["test_vacation"].user == new_user


def test_user_argument_back_populates_vacations_attribute(setup_vacation_tests):
    """user argument back populates vacations attribute of the User instance."""
    data = setup_vacation_tests
    assert data["test_vacation"] in data["kwargs"]["user"].vacations


def test_user_attribute_back_populates_vacations_attribute(setup_vacation_tests):
    """user attribute back populates vacations attribute of the User instance."""
    data = setup_vacation_tests
    new_user = User(
        name="test user 2", login="testuser2", email="test@user.com", password="secret"
    )
    data["test_vacation"].user = new_user
    assert data["test_vacation"] in new_user.vacations


def test_to_tjp_attribute_is_a_read_only_property(setup_vacation_tests):
    """to_tjp is a read-only attribute."""
    data = setup_vacation_tests
    with pytest.raises(AttributeError) as cm:
        data["test_vacation"].to_tjp = "some value"

    error_message = (
        "can't set attribute 'to_tjp'"
        if sys.version_info.minor < 11
        else "property 'to_tjp' of 'Vacation' object has no setter"
    )

    assert str(cm.value) == error_message


def test_to_tjp_attribute_is_working_properly(setup_vacation_tests):
    """to_tjp attribute is working properly."""
    data = setup_vacation_tests
    # TODO: Vacation should also use time zone info
    expected_tjp = "vacation 2013-06-06-10:00:00 - 2013-06-10-19:00:00"
    assert data["test_vacation"].to_tjp == expected_tjp
