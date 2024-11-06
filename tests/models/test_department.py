# -*- coding: utf-8 -*-
"""Tests for the Department class."""

import datetime

import pytest

import pytz

from stalker import Department, DepartmentUser, Entity, User
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_department_tests():
    """Set up the tests foe the Department class."""
    data = dict()
    data["test_admin"] = User(
        name="admin",
        login="admin",
        email="admin@admins.com",
        password="12345",
    )

    # create a couple of test users
    data["test_user1"] = User(
        name="User1",
        login="user1",
        email="user1@test.com",
        password="123456",
    )

    data["test_user2"] = User(
        name="User2",
        login="user2",
        email="user2@test.com",
        password="123456",
    )

    data["test_user3"] = User(
        name="User3",
        login="user3",
        email="user3@test.com",
        password="123456",
    )

    data["test_user4"] = User(
        name="User4",
        login="user4",
        email="user4@test.com",
        password="123456",
    )

    data["test_user5"] = User(
        name="User5",
        login="user5",
        email="user5@test.com",
        password="123456",
    )

    data["users_list"] = [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
        data["test_user4"],
    ]

    data["date_created"] = data["date_updated"] = datetime.datetime.now(pytz.utc)

    data["kwargs"] = {
        "name": "Test Department",
        "description": "This is a department for testing purposes",
        "created_by": data["test_admin"],
        "updated_by": data["test_admin"],
        "date_created": data["date_created"],
        "date_updated": data["date_updated"],
        "users": data["users_list"],
    }

    # create a default department object
    data["test_department"] = Department(**data["kwargs"])

    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Department class."""
    assert Department.__auto_name__ is False


def test___hash___value_is_correctly_calculated(setup_department_tests):
    """__hash__ value is correctly calculated."""
    data = setup_department_tests
    assert data["test_department"].__hash__() == hash(
        "{}:{}:{}".format(
            data["test_department"].id,
            data["test_department"].name,
            data["test_department"].entity_type
        )
    )


def test_users_argument_accepts_an_empty_list(setup_department_tests):
    """users argument accepts an empty list."""
    data = setup_department_tests
    # this should work without raising any error
    data["kwargs"]["users"] = []
    new_dep = Department(**data["kwargs"])
    assert isinstance(new_dep, Department)


def test_users_attribute_accepts_an_empty_list(setup_department_tests):
    """users attribute accepts an empty list."""
    data = setup_department_tests
    # this should work without raising any error
    data["test_department"].users = []


def test_users_argument_accepts_only_a_list_of_user_objects(setup_department_tests):
    """users argument accepts only a list of user objects."""
    data = setup_department_tests
    test_value = [1, 2.3, [], {}]
    data["kwargs"]["users"] = test_value
    # this should raise a TypeError
    with pytest.raises(TypeError) as cm:
        Department(**data["kwargs"])

    assert str(cm.value) == (
        "DepartmentUser.user should be a stalker.models.auth.User instance, "
        "not int: '1'"
    )


def test_users_attribute_accepts_only_a_list_of_user_objects(setup_department_tests):
    """users attribute accepts only a list of user objects."""
    data = setup_department_tests
    test_value = [1, 2.3, [], {}]
    # this should raise a TypeError
    with pytest.raises(TypeError) as cm:
        data["test_department"].users = test_value

    assert str(cm.value) == (
        "DepartmentUser.user should be a stalker.models.auth.User instance, "
        "not int: '1'"
    )


def test_users_attribute_elements_accepts_user_only_1(setup_department_tests):
    """TypeError is raised if append non-User to the users attr."""
    data = setup_department_tests
    # append
    with pytest.raises(TypeError) as cm:
        data["test_department"].users.append(0)

    assert str(cm.value) == (
        "DepartmentUser.user should be a stalker.models.auth.User instance, "
        "not int: '0'"
    )


def test_users_attribute_elements_accepts_user_only_2(setup_department_tests):
    """TypeError is raised if non list assigned to the users attr."""
    data = setup_department_tests
    # __setitem__
    with pytest.raises(TypeError) as cm:
        data["test_department"].users[0] = 0

    assert str(cm.value) == (
        "DepartmentUser.user should be a stalker.models.auth.User instance, "
        "not int: '0'"
    )


def test_users_argument_is_not_iterable(setup_department_tests):
    """TypeError is raised if the given users argument is not an instance of list."""
    data = setup_department_tests
    data["kwargs"]["users"] = "a user"
    with pytest.raises(TypeError) as cm:
        Department(**data["kwargs"])

    assert str(cm.value) == (
        "DepartmentUser.user should be a stalker.models.auth.User instance, "
        "not str: 'a'"
    )


def test_users_attribute_is_not_iterable(setup_department_tests):
    """TypeError is raised if the users attr is not iterable value."""
    data = setup_department_tests
    with pytest.raises(TypeError) as cm:
        data["test_department"].users = "a user"

    assert str(cm.value) == (
        "DepartmentUser.user should be a stalker.models.auth.User instance, "
        "not str: 'a'"
    )


def test_users_attribute_defaults_to_empty_list(setup_department_tests):
    """users attribute defaults to an empty list if the users argument is skipped."""
    data = setup_department_tests
    data["kwargs"].pop("users")
    new_department = Department(**data["kwargs"])
    assert new_department.users == []


def test_users_attribute_set_to_none(setup_department_tests):
    """TypeError is raised if the users attribute is set to None."""
    data = setup_department_tests
    with pytest.raises(TypeError) as cm:
        data["test_department"].users = None

    assert str(cm.value) == "'NoneType' object is not iterable"


def test_equality(setup_department_tests):
    """equality of two Department objects."""
    data = setup_department_tests
    dep1 = Department(**data["kwargs"])
    dep2 = Department(**data["kwargs"])

    entity_kwargs = data["kwargs"].copy()
    entity_kwargs.pop("users")
    entity1 = Entity(**entity_kwargs)

    data["kwargs"]["name"] = "Animation"
    dep3 = Department(**data["kwargs"])

    assert dep1 == dep2
    assert not dep1 == dep3
    assert not dep1 == entity1


def test_inequality(setup_department_tests):
    """inequality of two Department objects."""
    data = setup_department_tests
    dep1 = Department(**data["kwargs"])
    dep2 = Department(**data["kwargs"])

    entity_kwargs = data["kwargs"].copy()
    entity_kwargs.pop("users")
    entity1 = Entity(**entity_kwargs)

    data["kwargs"]["name"] = "Animation"
    dep3 = Department(**data["kwargs"])

    assert not dep1 != dep2
    assert dep1 != dep3
    assert dep1 != entity1


@pytest.fixture(scope="function")
def setup_department_db_tests(setup_postgresql_db):
    """set up Database tests for Department class."""
    data = dict()
    data["test_admin"] = User.query.filter_by(login="admin").first()

    # create a couple of test users
    data["test_user1"] = User(
        name="User1",
        login="user1",
        email="user1@test.com",
        password="123456",
    )
    DBSession.add(data["test_user1"])

    data["test_user2"] = User(
        name="User2",
        login="user2",
        email="user2@test.com",
        password="123456",
    )
    DBSession.add(data["test_user2"])

    data["test_user3"] = User(
        name="User3",
        login="user3",
        email="user3@test.com",
        password="123456",
    )
    DBSession.add(data["test_user3"])

    data["test_user4"] = User(
        name="User4",
        login="user4",
        email="user4@test.com",
        password="123456",
    )
    DBSession.add(data["test_user4"])

    data["test_user5"] = User(
        name="User5",
        login="user5",
        email="user5@test.com",
        password="123456",
    )
    DBSession.add(data["test_user5"])

    data["users_list"] = [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
        data["test_user4"],
    ]

    data["date_created"] = data["date_updated"] = datetime.datetime.now(pytz.utc)

    data["kwargs"] = {
        "name": "Test Department",
        "description": "This is a department for testing purposes",
        "created_by": data["test_admin"],
        "updated_by": data["test_admin"],
        "date_created": data["date_created"],
        "date_updated": data["date_updated"],
        "users": data["users_list"],
    }

    # create a default department object
    data["test_department"] = Department(**data["kwargs"])
    DBSession.add(data["test_department"])
    DBSession.commit()
    return data


def test_user_role_attribute(setup_department_db_tests):
    """Automatic generation of the DepartmentUser class."""
    data = setup_department_db_tests
    # assign a user to a department and search for a DepartmentUser
    # representing that relation
    DBSession.commit()
    with DBSession.no_autoflush:
        data["test_department"].users.append(data["test_user5"])

    dus = (
        DepartmentUser.query.filter(DepartmentUser.user == data["test_user5"])
        .filter(DepartmentUser.department == data["test_department"])
        .all()
    )

    assert len(dus) > 0
    du = dus[0]
    assert isinstance(du, DepartmentUser)
    assert du.department == data["test_department"]
    assert du.user == data["test_user5"]
    assert du.role is None


def test_tjp_id_is_working_properly(setup_department_db_tests):
    """tjp_is working properly."""
    data = setup_department_db_tests
    assert data["test_department"].tjp_id == "Department_36"


def test_to_tjp_is_working_properly(setup_department_db_tests):
    """to_tjp property is working properly."""
    data = setup_department_db_tests
    expected_tjp = """
resource Department_36 "Department_36" {
    resource User_31 "User_31" {
    efficiency 1.0
}
    resource User_32 "User_32" {
    efficiency 1.0
}
    resource User_33 "User_33" {
    efficiency 1.0
}
    resource User_34 "User_34" {
    efficiency 1.0
}
}"""
    assert data["test_department"].to_tjp == expected_tjp
