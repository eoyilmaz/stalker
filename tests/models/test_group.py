# -*- coding: utf-8 -*-
"""Tests for the Group class."""

import pytest

from stalker import Group, Permission, User


@pytest.fixture(scope="function")
def set_group_tests():
    """Set up the test for the Group class."""
    data = dict()
    # create a couple of Users
    data["test_user1"] = User(
        name="User1",
        login="user1",
        password="1234",
        email="user1@test.com",
    )

    data["test_user2"] = User(
        name="User2",
        login="user2",
        password="1234",
        email="user1@test.com",
    )

    data["test_user3"] = User(
        name="User3",
        login="user3",
        password="1234",
        email="user3@test.com",
    )

    # create a test group
    data["kwargs"] = {
        "name": "Test Group",
        "users": [data["test_user1"], data["test_user2"], data["test_user3"]],
    }

    data["test_group"] = Group(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Group class."""
    assert Group.__auto_name__ is False


def test_users_argument_is_skipped(set_group_tests):
    """users argument is skipped the users attribute is an empty list."""
    data = set_group_tests
    data["kwargs"].pop("users")
    new_group = Group(**data["kwargs"])
    assert new_group.users == []


def test_users_argument_is_not_a_list_of_user_instances(set_group_tests):
    """TypeError is raised if the users argument is not a list of User instances."""
    data = set_group_tests
    data["kwargs"]["users"] = [12, "not a user"]
    with pytest.raises(TypeError) as cm:
        Group(**data["kwargs"])

    assert str(cm.value) == (
        "Group.users attribute must all be stalker.models.auth.User instances, "
        "not int: '12'"
    )


def test_users_attribute_is_not_a_list_of_user_instances(set_group_tests):
    """TypeError is raised if the users attribute is not a list of User instances."""
    data = set_group_tests
    with pytest.raises(TypeError) as cm:
        data["test_group"].users = [12, "not a user"]

    assert str(cm.value) == (
        "Group.users attribute must all be stalker.models.auth.User instances, "
        "not int: '12'"
    )


def test_users_argument_updates_the_groups_attribute_in_the_given_user_instances(
    set_group_tests,
):
    """users arg will have the current Group instance in their groups attribute."""
    data = set_group_tests
    data["kwargs"]["name"] = "New Group"
    new_group = Group(**data["kwargs"])

    assert all(new_group in user.groups for user in data["kwargs"]["users"])


def test_users_attribute_updates_the_groups_attribute_in_the_given_user_instances(
    set_group_tests,
):
    """users attr will have the current Group instance in their groups attribute."""
    data = set_group_tests
    test_users = data["kwargs"].pop("users")
    new_group = Group(**data["kwargs"])
    new_group.users = test_users
    assert all(new_group in user.groups for user in test_users)


def test_permissions_argument_is_working_properly(set_group_tests):
    """permissions can be added to the Group on __init__()."""
    data = set_group_tests
    # create a couple of permissions
    perm1 = Permission("Allow", "Create", "User")
    perm2 = Permission("Allow", "Read", "User")
    perm3 = Permission("Deny", "Delete", "User")

    new_group = Group(
        name="Test Group",
        users=[data["test_user1"], data["test_user2"]],
        permissions=[perm1, perm2, perm3],
    )

    assert new_group.permissions == [perm1, perm2, perm3]
