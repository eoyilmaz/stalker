# -*- coding: utf-8 -*-
"""AuthenticationLog class related tests."""
import datetime

import pytest

import pytz

from stalker import AuthenticationLog, User
from stalker.models.auth import LOGIN, LOGOUT


@pytest.fixture(scope="function")
def setup_authentication_log_tests():
    """Set up tests for the AuthenticationLog class.

    Returns:
        dict: Test data.
    """
    data = dict()
    data["test_user1"] = User(
        name="Test User 1",
        login="tuser1",
        email="tuser1@users.com",
        password="secret",
    )
    data["test_user2"] = User(
        name="Test User 2",
        login="tuser2",
        email="tuser2@users.com",
        password="secret",
    )
    return data


def test_user_argument_is_skipped(setup_authentication_log_tests):
    """TypeError is raised if the user arg is skipped."""
    with pytest.raises(TypeError) as cm:
        AuthenticationLog(action=LOGIN, date=datetime.datetime.now(pytz.utc))
    assert str(cm.value) == (
        "AuthenticationLog.user should be a User instance, not NoneType: 'None'"
    )


def test_user_argument_is_none(setup_authentication_log_tests):
    """TypeError is raised if the user arg is None."""
    with pytest.raises(TypeError) as cm:
        AuthenticationLog(user=None, action=LOGIN, date=datetime.datetime.now(pytz.utc))
    assert str(cm.value) == (
        "AuthenticationLog.user should be a User instance, not NoneType: 'None'"
    )


def test_user_argument_is_not_a_user_instance(setup_authentication_log_tests):
    """TypeError is raised if user arg is not User."""
    with pytest.raises(TypeError) as cm:
        AuthenticationLog(
            user="not a user instance",
            action=LOGIN,
            date=datetime.datetime.now(pytz.utc),
        )
    assert str(cm.value) == (
        "AuthenticationLog.user should be a User instance, "
        "not str: 'not a user instance'"
    )


def test_user_attribute_is_not_a_user_instance(setup_authentication_log_tests):
    """TypeError is raised if user attr is not User."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"], action=LOGIN, date=datetime.datetime.now(pytz.utc)
    )
    with pytest.raises(TypeError) as cm:
        uli.user = "not a user instance"

    assert str(cm.value) == (
        "AuthenticationLog.user should be a User instance, "
        "not str: 'not a user instance'"
    )


def test_user_argument_is_working_properly(setup_authentication_log_tests):
    """user arg value is correctly passed to the user attribute."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"], action=LOGOUT, date=datetime.datetime.now(pytz.utc)
    )
    assert uli.user == data["test_user1"]


def test_user_attribute_is_working_properly(setup_authentication_log_tests):
    """user attr is working properly."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"], action=LOGOUT, date=datetime.datetime.now(pytz.utc)
    )
    assert uli.user != data["test_user2"]
    uli.user = data["test_user2"]
    assert uli.user == data["test_user2"]


def test_action_argument_is_skipped(setup_authentication_log_tests):
    """action attr is "login" if the action argument is skipped."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"], date=datetime.datetime.now(pytz.utc)
    )
    assert uli.action == LOGIN


def test_action_argument_is_none(setup_authentication_log_tests):
    """action attr is "login" when action arg is None."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"], action=None, date=datetime.datetime.now(pytz.utc)
    )
    assert uli.action == LOGIN


def test_action_argument_value_is_not_login_or_logout(setup_authentication_log_tests):
    """ValueError is raised if the action attr is not one of "login" or "login"."""
    data = setup_authentication_log_tests
    with pytest.raises(ValueError) as cm:
        AuthenticationLog(
            user=data["test_user1"],
            action="not login",
            date=datetime.datetime.now(pytz.utc),
        )
    assert (
        str(cm.value)
        == 'AuthenticationLog.action should be one of "login" or "logout", '
        'not "not login"'
    )


def test_action_attribute_value_is_not_login_or_logout(setup_authentication_log_tests):
    """ValueError is raised if the action attr is not LOGIN/LOGOUT."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"], action=LOGIN, date=datetime.datetime.now(pytz.utc)
    )
    with pytest.raises(ValueError) as cm:
        uli.action = "not login"
    assert (
        str(cm.value)
        == 'AuthenticationLog.action should be one of "login" or "logout", '
        'not "not login"'
    )


def test_action_argument_is_working_properly(setup_authentication_log_tests):
    """action arg value is passed to the action attr."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"], action=LOGIN, date=datetime.datetime.now(pytz.utc)
    )
    assert uli.action == LOGIN
    uli = AuthenticationLog(
        user=data["test_user1"], action=LOGOUT, date=datetime.datetime.now(pytz.utc)
    )
    assert uli.action == LOGOUT


def test_action_attribute_is_working_properly(setup_authentication_log_tests):
    """action attr is working properly."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"], action=LOGIN, date=datetime.datetime.now(pytz.utc)
    )
    assert uli.action != LOGOUT
    uli.action = LOGOUT
    assert uli.action == LOGOUT


def test_date_argument_is_skipped(setup_authentication_log_tests):
    """date attr datetime.datetime.now(pytz.utc) if date arg is skipped."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(user=data["test_user1"], action=LOGIN)
    diff = datetime.datetime.now(pytz.utc) - uli.date
    assert diff.microseconds < 5000


def test_date_argument_is_none(setup_authentication_log_tests):
    """date attr datetime.datetime.now(pytz.utc) if date argument is None."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(user=data["test_user1"], action=LOGIN, date=None)
    diff = datetime.datetime.now(pytz.utc) - uli.date
    assert diff < datetime.timedelta(seconds=1)


def test_date_attribute_is_none(setup_authentication_log_tests):
    """date attr is set to datetime.datetime.now(pytz.utc) if is set to None."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"],
        action=LOGIN,
        date=datetime.datetime.now(pytz.utc) - datetime.timedelta(days=10),
    )
    diff = datetime.datetime.now(pytz.utc) - uli.date
    one_second = datetime.timedelta(seconds=1)
    assert diff > one_second
    uli.date = None
    diff = datetime.datetime.now(pytz.utc) - uli.date
    assert diff < one_second


def test_date_argument_is_not_a_datetime_instance(setup_authentication_log_tests):
    """TypeError is raised if date argument is not a datetime.datetime instance."""
    data = setup_authentication_log_tests
    with pytest.raises(TypeError) as cm:
        AuthenticationLog(
            user=data["test_user1"], action=LOGIN, date="not a datetime instance"
        )
    assert str(cm.value) == (
        'AuthenticationLog.date should be a datetime.datetime instance, '
        "not str: 'not a datetime instance'"
    )


def test_date_attribute_is_not_a_datetime_instance(setup_authentication_log_tests):
    """TypeError is raised if date attr is not datetime.datetime instance."""
    data = setup_authentication_log_tests
    uli = AuthenticationLog(
        user=data["test_user1"], action=LOGIN, date=datetime.datetime.now(pytz.utc)
    )
    with pytest.raises(TypeError) as cm:
        uli.date = "not a datetime instance"

    assert str(cm.value) == (
        'AuthenticationLog.date should be a datetime.datetime instance, '
        "not str: 'not a datetime instance'"
    )


def test_date_argument_is_working_properly(setup_authentication_log_tests):
    """date argument value is properly passed to the date attribute."""
    data = setup_authentication_log_tests
    date = datetime.datetime(2016, 11, 14, 16, 30, tzinfo=pytz.utc)
    uli = AuthenticationLog(user=data["test_user1"], action=LOGIN, date=date)

    assert uli.date == date


def test_date_attribute_is_working_properly(setup_authentication_log_tests):
    """date attribute value can be properly changed."""
    data = setup_authentication_log_tests
    date1 = datetime.datetime(2016, 11, 4, 6, 30, tzinfo=pytz.utc)
    date2 = datetime.datetime(2016, 11, 14, 16, 30, tzinfo=pytz.utc)
    uli = AuthenticationLog(user=data["test_user1"], action=LOGIN, date=date1)
    assert uli.date != date2
    uli.date = date2
    assert uli.date == date2


def test_date_argument_is_working_properly2(setup_authentication_log_tests):
    """date argument value is properly passed to the date attribute."""
    data = setup_authentication_log_tests
    date1 = datetime.datetime(2016, 11, 4, 6, 30, tzinfo=pytz.utc)
    uli = AuthenticationLog(user=data["test_user1"], action=LOGIN, date=date1)
    assert uli.date == date1
