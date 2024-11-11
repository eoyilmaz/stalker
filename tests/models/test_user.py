# -*- coding: utf-8 -*-
"""Tests for the User class."""

import copy
import datetime
import logging
import sys

import pytest

import pytz

from stalker import (
    Client,
    Department,
    Group,
    Project,
    Repository,
    Sequence,
    Status,
    StatusList,
    Task,
    Ticket,
    Type,
    User,
    Vacation,
    Version,
)
from stalker.db.session import DBSession
from stalker.models.ticket import FIXED, CANTFIX, INVALID

from sqlalchemy.exc import IntegrityError

from tests.utils import get_admin_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@pytest.fixture(scope="function")
def setup_user_db_tests(setup_postgresql_db):
    """Set up tests for the User class with a DB."""
    data = dict()

    # need to have some test object for
    # a department
    data["test_department1"] = Department(name="Test Department 1")
    data["test_department2"] = Department(name="Test Department 2")
    data["test_department3"] = Department(name="Test Department 3")

    DBSession.add_all(
        [data["test_department1"], data["test_department2"], data["test_department3"]]
    )

    # a couple of groups
    data["test_group1"] = Group(name="Test Group 1")
    data["test_group2"] = Group(name="Test Group 2")
    data["test_group3"] = Group(name="Test Group 3")

    DBSession.add_all([data["test_group1"], data["test_group2"], data["test_group3"]])
    DBSession.commit()

    # a couple of statuses
    data["status_cmpl"] = Status.query.filter(Status.code == "CMPL").first()
    data["status_wip"] = Status.query.filter(Status.code == "WIP").first()
    data["status_rts"] = Status.query.filter(Status.code == "RTS").first()
    data["status_prev"] = Status.query.filter(Status.code == "PREV").first()

    # a repository type
    data["test_repository_type"] = Type(
        name="Test",
        code="test",
        target_entity_type="Repository",
    )

    # a repository
    data["test_repository"] = Repository(
        name="Test Repository", code="TR", type=data["test_repository_type"]
    )

    # a project type
    data["commercial_project_type"] = Type(
        name="Commercial Project",
        code="comm",
        target_entity_type="Project",
    )

    # a couple of projects
    data["test_project1"] = Project(
        name="Test Project 1",
        code="tp1",
        type=data["commercial_project_type"],
        repository=data["test_repository"],
    )

    data["test_project2"] = Project(
        name="Test Project 2",
        code="tp2",
        type=data["commercial_project_type"],
        repository=data["test_repository"],
    )

    data["test_project3"] = Project(
        name="Test Project 3",
        code="tp3",
        type=data["commercial_project_type"],
        repository=data["test_repository"],
    )

    DBSession.add_all(
        [data["test_project1"], data["test_project2"], data["test_project3"]]
    )
    DBSession.commit()

    # a task status list
    data["task_status_list"] = StatusList.query.filter_by(
        target_entity_type="Task"
    ).first()

    data["test_lead"] = User(
        name="lead", login="lead", email="lead@lead.com", password="12345"
    )

    # a couple of tasks
    data["test_task1"] = Task(
        name="Test Task 1",
        status_list=data["task_status_list"],
        project=data["test_project1"],
        responsible=[data["test_lead"]],
    )

    data["test_task2"] = Task(
        name="Test Task 2",
        status_list=data["task_status_list"],
        project=data["test_project1"],
        responsible=[data["test_lead"]],
    )

    data["test_task3"] = Task(
        name="Test Task 3",
        status_list=data["task_status_list"],
        project=data["test_project2"],
        responsible=[data["test_lead"]],
    )

    data["test_task4"] = Task(
        name="Test Task 4",
        status_list=data["task_status_list"],
        project=data["test_project3"],
        responsible=[data["test_lead"]],
    )

    DBSession.add_all(
        [data["test_task1"], data["test_task2"], data["test_task3"], data["test_task4"]]
    )
    DBSession.commit()

    # for task1
    data["test_version1"] = Version(task=data["test_task1"], full_path="some/path")
    DBSession.add(data["test_version1"])
    DBSession.commit()

    data["test_version2"] = Version(task=data["test_task1"], full_path="some/path")
    DBSession.add(data["test_version2"])
    DBSession.commit()

    data["test_version3"] = Version(task=data["test_task1"], full_path="some/path")
    DBSession.add(data["test_version3"])
    DBSession.commit()

    # for task2
    data["test_version4"] = Version(task=data["test_task2"], full_path="some/path")
    DBSession.add(data["test_version4"])
    DBSession.commit()

    data["test_version5"] = Version(task=data["test_task2"], full_path="some/path")
    DBSession.add(data["test_version5"])
    DBSession.commit()

    data["test_version6"] = Version(task=data["test_task2"], full_path="some/path")
    DBSession.add(data["test_version6"])
    DBSession.commit()

    # for task3
    data["test_version7"] = Version(task=data["test_task3"], full_path="some/path")
    DBSession.add(data["test_version7"])
    DBSession.commit()

    data["test_version8"] = Version(task=data["test_task3"], full_path="some/path")
    DBSession.add(data["test_version8"])
    DBSession.commit()

    data["test_version9"] = Version(task=data["test_task3"], full_path="some/path")
    DBSession.add(data["test_version9"])
    DBSession.commit()

    # for task4
    data["test_version10"] = Version(task=data["test_task4"], full_path="some/path")
    DBSession.add(data["test_version10"])
    DBSession.commit()

    data["test_version11"] = Version(task=data["test_task4"], full_path="some/path")
    DBSession.add(data["test_version11"])
    DBSession.commit()

    data["test_version12"] = Version(task=data["test_task4"], full_path="some/path")
    DBSession.add(data["test_version12"])
    DBSession.commit()

    # *********************************************************************
    # Tickets
    # *********************************************************************

    # no need to create status list for tickets because we have a database
    # setup is running, so it will automatically be linked

    # tickets for version1
    data["test_ticket1"] = Ticket(
        project=data["test_project1"],
        links=[data["test_version1"]],
    )
    DBSession.add(data["test_ticket1"])
    # set it to closed
    data["test_ticket1"].resolve()
    DBSession.commit()

    # create a new ticket and leave it open
    data["test_ticket2"] = Ticket(
        project=data["test_project1"],
        links=[data["test_version1"]],
    )
    DBSession.add(data["test_ticket2"])
    DBSession.commit()

    # create a new ticket and close and then reopen it
    data["test_ticket3"] = Ticket(
        project=data["test_project1"],
        links=[data["test_version1"]],
    )
    DBSession.add(data["test_ticket3"])
    data["test_ticket3"].resolve()
    data["test_ticket3"].reopen()
    DBSession.commit()

    # *********************************************************************
    # tickets for version2
    # create a new ticket and leave it open
    data["test_ticket4"] = Ticket(
        project=data["test_project1"],
        links=[data["test_version2"]],
    )
    DBSession.add(data["test_ticket4"])
    DBSession.commit()

    # create a new Ticket and close it
    data["test_ticket5"] = Ticket(
        project=data["test_project1"],
        links=[data["test_version2"]],
    )
    DBSession.add(data["test_ticket5"])
    data["test_ticket5"].resolve()
    DBSession.commit()

    # create a new Ticket and close it
    data["test_ticket6"] = Ticket(
        project=data["test_project1"],
        links=[data["test_version3"]],
    )
    DBSession.add(data["test_ticket6"])
    data["test_ticket6"].resolve()
    DBSession.commit()

    # *********************************************************************
    # tickets for version3
    # create a new ticket and close it
    data["test_ticket7"] = Ticket(
        project=data["test_project1"],
        links=[data["test_version3"]],
    )
    DBSession.add(data["test_ticket7"])
    data["test_ticket7"].resolve()
    DBSession.commit()

    # create a new ticket and close it
    data["test_ticket8"] = Ticket(
        project=data["test_project1"],
        links=[data["test_version3"]],
    )
    DBSession.add(data["test_ticket8"])
    data["test_ticket8"].resolve()
    DBSession.commit()

    # *********************************************************************
    # tickets for version4
    # create a new ticket and close it
    data["test_ticket9"] = Ticket(
        project=data["test_project1"],
        links=[data["test_version4"]],
    )
    DBSession.add(data["test_ticket9"])
    data["test_ticket9"].resolve()
    DBSession.commit()

    # no tickets for any other version
    # *********************************************************************

    # a status list for sequence
    with DBSession.no_autoflush:
        data["sequence_status_list"] = StatusList.query.filter_by(
            target_entity_type="Sequence"
        ).first()

    # a couple of sequences
    data["test_sequence1"] = Sequence(
        name="Test Seq 1",
        code="ts1",
        project=data["test_project1"],
        status_list=data["sequence_status_list"],
    )

    data["test_sequence2"] = Sequence(
        name="Test Seq 2",
        code="ts2",
        project=data["test_project1"],
        status_list=data["sequence_status_list"],
    )

    data["test_sequence3"] = Sequence(
        name="Test Seq 3",
        code="ts3",
        project=data["test_project1"],
        status_list=data["sequence_status_list"],
    )

    data["test_sequence4"] = Sequence(
        name="Test Seq 4",
        code="ts4",
        project=data["test_project1"],
        status_list=data["sequence_status_list"],
    )

    DBSession.add_all(
        [
            data["test_sequence1"],
            data["test_sequence2"],
            data["test_sequence3"],
            data["test_sequence4"],
        ]
    )
    DBSession.commit()

    data["test_admin"] = get_admin_user()
    assert data["test_admin"] is not None

    # create test company
    data["test_company"] = Client(name="Test Company")

    # create the default values for parameters
    data["kwargs"] = {
        "name": "Erkan Ozgur Yilmaz",
        "login": "eoyilmaz",
        "description": "this is a test user",
        "password": "hidden",
        "email": "eoyilmaz@fake.com",
        "departments": [data["test_department1"]],
        "groups": [data["test_group1"], data["test_group2"]],
        "created_by": data["test_admin"],
        "updated_by": data["test_admin"],
        "efficiency": 1.0,
        "companies": [data["test_company"]],
    }

    # create a proper user object
    data["test_user"] = User(**data["kwargs"])
    DBSession.add(data["test_user"])
    DBSession.commit()

    # just change the kwargs for other tests
    data["kwargs"]["name"] = "some other name"
    data["kwargs"]["email"] = "some@other.email"
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for User class."""
    assert User.__auto_name__ is False


def test_email_argument_accepting_only_string(setup_user_db_tests):
    """email argument accepting only string values."""
    data = setup_user_db_tests
    # try to create a new user with wrong attribute
    data["kwargs"]["email"] = 1.3
    with pytest.raises(TypeError) as cm:
        User(**data["kwargs"])

    assert str(cm.value) == "User.email should be an instance of str, not float: '1.3'"


def test_email_attribute_accepting_only_string_1(setup_user_db_tests):
    """email attribute accepting only string values."""
    data = setup_user_db_tests
    # try to assign something else than a string
    test_value = 1

    with pytest.raises(TypeError) as cm:
        data["test_user"].email = test_value

    assert str(cm.value) == "User.email should be an instance of str, not int: '1'"


def test_email_attribute_accepting_only_string_2(setup_user_db_tests):
    """email attribute accepting only string values."""
    data = setup_user_db_tests
    # try to assign something else than a string
    test_value = ["an email"]

    with pytest.raises(TypeError) as cm:
        data["test_user"].email = test_value

    assert str(cm.value) == (
        "User.email should be an instance of str, not list: '['an email']'"
    )


def test_email_argument_format_1(setup_user_db_tests):
    """Given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of this values should raise a ValueError
    data["kwargs"]["email"] = "an email in no format"
    with pytest.raises(ValueError) as cm:
        User(**data["kwargs"])

    assert str(cm.value) == "check the formatting of User.email, there is no @ sign"


def test_email_argument_format_2(setup_user_db_tests):
    """given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of this values should raise a ValueError
    data["kwargs"]["email"] = "an_email_with_no_part2"
    with pytest.raises(ValueError) as cm:
        User(**data["kwargs"])

    assert str(cm.value) == "check the formatting of User.email, there is no @ sign"


def test_email_argument_format_3(setup_user_db_tests):
    """given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of this values should raise a ValueError
    data["kwargs"]["email"] = "@an_email_with_only_part2"
    with pytest.raises(ValueError) as cm:
        User(**data["kwargs"])

    assert (
        str(cm.value) == "check the formatting of User.email, the name part is missing"
    )


def test_email_argument_format_4(setup_user_db_tests):
    """given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of this values should raise a ValueError
    data["kwargs"]["email"] = "@"
    with pytest.raises(ValueError) as cm:
        User(**data["kwargs"])

    assert (
        str(cm.value) == "check the formatting of User.email, the name part is missing"
    )


def test_email_attribute_format_1(setup_user_db_tests):
    """given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of these email values should raise a ValueError
    with pytest.raises(ValueError) as cm:
        data["test_user"].email = "an email in no format"

    assert str(cm.value) == "check the formatting of User.email, there is no @ sign"


def test_email_attribute_format_2(setup_user_db_tests):
    """given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of these email values should raise a ValueError
    with pytest.raises(ValueError) as cm:
        data["test_user"].email = "an_email_with_no_part2"

    assert str(cm.value) == "check the formatting of User.email, there is no @ sign"


def test_email_attribute_format_3(setup_user_db_tests):
    """given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of these email values should raise a ValueError
    with pytest.raises(ValueError) as cm:
        data["test_user"].email = "@an_email_with_only_part2"

    assert (
        str(cm.value) == "check the formatting of User.email, the name part is missing"
    )


def test_email_attribute_format_4(setup_user_db_tests):
    """given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of these email values should raise a ValueError
    with pytest.raises(ValueError) as cm:
        data["test_user"].email = "@"

    assert (
        str(cm.value) == "check the formatting of User.email, the name part is missing"
    )


def test_email_attribute_format_5(setup_user_db_tests):
    """given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of these email values should raise a ValueError
    with pytest.raises(ValueError) as cm:
        data["test_user"].email = "eoyilmaz@"

    assert (
        str(cm.value) == "check the formatting User.email, the domain part is missing"
    )


def test_email_attribute_format_6(setup_user_db_tests):
    """given an email in wrong format will raise a ValueError."""
    data = setup_user_db_tests
    # any of these email values should raise a ValueError
    with pytest.raises(ValueError) as cm:
        data["test_user"].email = "eoyilmaz@some.compony@com"

    assert (
        str(cm.value)
        == "check the formatting of User.email, there are more than one @ sign"
    )


def test_email_argument_should_be_a_unique_value(setup_user_db_tests):
    """email argument should be a unique value."""
    data = setup_user_db_tests
    # this test should include a database
    test_email = "test@email.com"
    data["kwargs"]["login"] = "test_user1"
    data["kwargs"]["email"] = test_email
    user1 = User(**data["kwargs"])
    DBSession.add(user1)
    DBSession.commit()

    data["kwargs"]["login"] = "test_user2"
    user2 = User(**data["kwargs"])
    DBSession.add(user2)

    with pytest.raises(IntegrityError) as cm:
        DBSession.commit()

    assert (
        "(psycopg2.errors.UniqueViolation) duplicate key value "
        'violates unique constraint "Users_email_key"' in str(cm.value)
    )


def test_email_attribute_is_working_as_expected(setup_user_db_tests):
    """email attribute works as expected."""
    data = setup_user_db_tests
    test_email = "eoyilmaz@somemail.com"
    data["test_user"].email = test_email
    assert data["test_user"].email == test_email


def test_login_argument_conversion_to_strings(setup_user_db_tests):
    """ValueError raised if login converted to string results an empty string."""
    data = setup_user_db_tests
    data["kwargs"]["login"] = "----++==#@#$"
    with pytest.raises(ValueError) as cm:
        User(**data["kwargs"])
    assert str(cm.value) == "User.login cannot be an empty string"


def test_login_argument_for_empty_string(setup_user_db_tests):
    """ValueError raised if trying to assign an empty string to login argument."""
    data = setup_user_db_tests
    data["kwargs"]["login"] = ""
    with pytest.raises(ValueError) as cm:
        User(**data["kwargs"])
    assert str(cm.value) == "User.login cannot be an empty string"


def test_login_attribute_for_empty_string(setup_user_db_tests):
    """ValueError raised if trying to assign an empty string to login attribute."""
    data = setup_user_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_user"].login = ""
    assert str(cm.value) == "User.login cannot be an empty string"


def test_login_argument_is_skipped(setup_user_db_tests):
    """TypeError raised if the login argument is skipped."""
    data = setup_user_db_tests
    data["kwargs"].pop("login")
    with pytest.raises(TypeError) as cm:
        User(**data["kwargs"])
    assert str(cm.value) == "User.login cannot be None"


def test_login_argument_is_none(setup_user_db_tests):
    """TypeError raised if trying to assign None to login argument."""
    data = setup_user_db_tests
    data["kwargs"]["login"] = None
    with pytest.raises(TypeError) as cm:
        User(**data["kwargs"])
    assert str(cm.value) == "User.login cannot be None"


def test_login_attribute_is_none(setup_user_db_tests):
    """TypeError raised if trying to assign None to login attribute."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].login = None

    assert str(cm.value) == "User.login cannot be None"


@pytest.mark.parametrize(
    "test_value,expected",
    [
        ("e. ozgur", "eozgur"),
        ("erkan", "erkan"),
        ("Ozgur", "ozgur"),
        ("Erkan ozgur", "erkanozgur"),
        ("eRKAN", "erkan"),
        ("eRkaN", "erkan"),
        (" eRkAn", "erkan"),
        (" eRkan ozGur", "erkanozgur"),
        ("213 e.ozgur", "eozgur"),
    ],
)
def test_login_argument_formatted_correctly(test_value, expected, setup_user_db_tests):
    """login argument formatted correctly."""
    data = setup_user_db_tests
    # set the input and expect the expected output
    data["kwargs"]["login"] = test_value
    test_user = User(**data["kwargs"])
    assert expected == test_user.login


@pytest.mark.parametrize(
    "test_value,expected",
    [
        ("e. ozgur", "eozgur"),
        ("erkan", "erkan"),
        ("Ozgur", "ozgur"),
        ("Erkan ozgur", "erkanozgur"),
        ("eRKAN", "erkan"),
        ("eRkaN", "erkan"),
        (" eRkAn", "erkan"),
        (" eRkan ozGur", "erkanozgur"),
    ],
)
def test_login_attribute_formatted_correctly(test_value, expected, setup_user_db_tests):
    """login attribute formatted correctly."""
    data = setup_user_db_tests
    # set the input and expect the expected output
    data["test_user"].login = test_value
    assert expected == data["test_user"].login


def test_login_argument_should_be_a_unique_value(setup_user_db_tests):
    """login argument should be a unique value."""
    data = setup_user_db_tests
    # this test should include a database
    test_login = "test_user1"
    data["kwargs"]["login"] = test_login
    data["kwargs"]["email"] = "test1@email.com"

    user1 = User(**data["kwargs"])
    DBSession.add(user1)
    DBSession.commit()

    data["kwargs"]["email"] = "test2@email.com"
    user2 = User(**data["kwargs"])
    DBSession.add(user2)
    with pytest.raises(IntegrityError) as cm:
        DBSession.commit()

    assert (
        "(psycopg2.errors.UniqueViolation) duplicate key value "
        'violates unique constraint "Users_login_key"' in str(cm.value)
    )


def test_login_argument_is_working_as_expected(setup_user_db_tests):
    """login argument is working as expected."""
    data = setup_user_db_tests
    assert data["test_user"].login == data["kwargs"]["login"]


def test_login_attribute_is_working_as_expected(setup_user_db_tests):
    """login attribute is working as expected."""
    data = setup_user_db_tests
    test_value = "newlogin"
    data["test_user"].login = test_value
    assert data["test_user"].login == test_value


def test_last_login_attribute_none(setup_user_db_tests):
    """nothing happens if the last login attribute is set to None."""
    data = setup_user_db_tests
    # nothing should happen
    data["test_user"].last_login = None


def test_departments_argument_is_skipped(setup_user_db_tests):
    """User can be created without a Department instance."""
    data = setup_user_db_tests
    data["kwargs"].pop("departments")

    new_user = User(**data["kwargs"])
    assert new_user.departments == []


def test_departments_argument_is_none(setup_user_db_tests):
    """User can be created with the departments argument value is to None."""
    data = setup_user_db_tests
    data["kwargs"]["departments"] = None
    new_user = User(**data["kwargs"])
    assert new_user.departments == []


def test_departments_attribute_is_set_none(setup_user_db_tests):
    """TypeError raised if the User's departments attribute set to None."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].departments = None
    assert str(cm.value) == "'NoneType' object is not iterable"


def test_departments_argument_is_an_empty_list(setup_user_db_tests):
    """User can be created with the departments argument is an empty list."""
    data = setup_user_db_tests
    data["kwargs"]["departments"] = []
    User(**data["kwargs"])


def test_departments_attribute_is_an_empty_list(setup_user_db_tests):
    """departments attribute can be set to an empty list."""
    data = setup_user_db_tests
    data["test_user"].departments = []
    assert data["test_user"].departments == []


def test_departments_argument_only_accepts_list_of_department_objects(
    setup_user_db_tests,
):
    """TypeError raised if departments arg is not a Department instance."""
    data = setup_user_db_tests
    # try to assign something other than a department object
    test_values = ["A department", 1, 1.0, ["a department"], {"a": "department"}]
    data["kwargs"]["departments"] = test_values
    with pytest.raises(TypeError) as cm:
        User(**data["kwargs"])

    assert str(cm.value) == (
        "DepartmentUser.department should be a "
        "stalker.models.department.Department instance, not str: 'A department'"
    )


def test_departments_attribute_only_accepts_department_objects(setup_user_db_tests):
    """TypeError raised if department attribute is not a Department instance."""
    data = setup_user_db_tests
    # try to assign something other than a department
    test_value = "a department"
    with pytest.raises(TypeError) as cm:
        data["test_user"].departments = test_value

    assert str(cm.value) == (
        "DepartmentUser.department should be a "
        "stalker.models.department.Department instance, not str: 'a'"
    )


def test_departments_attribute_works_as_expected(setup_user_db_tests):
    """departments attribute works as expected."""
    data = setup_user_db_tests
    # try to set and get the same value back
    data["test_user"].departments = [data["test_department2"]]
    assert sorted(data["test_user"].departments, key=lambda x: x.name) == sorted(
        [data["test_department2"]], key=lambda x: x.name
    )


def test_departments_attribute_supports_appending(setup_user_db_tests):
    """departments attribute supports appending."""
    data = setup_user_db_tests
    data["test_user"].departments = []
    data["test_user"].departments.append(data["test_department1"])
    data["test_user"].departments.append(data["test_department2"])
    assert sorted(data["test_user"].departments, key=lambda x: x.name) == sorted(
        [data["test_department1"], data["test_department2"]], key=lambda x: x.name
    )


def test_password_arg_is_none(setup_user_db_tests):
    """TypeError raised if password arg value is None."""
    data = setup_user_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["password"] = None
    with pytest.raises(TypeError) as cm:
        User(**kwargs)
    assert str(cm.value) == "User.password cannot be None"


def test_password_argument_is_an_empty_string(setup_user_db_tests):
    """ValueError raised the password argument is an empty string."""
    data = setup_user_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["password"] = ""
    with pytest.raises(ValueError) as cm:
        User(**kwargs)
    assert str(cm.value) == "User.password cannot be an empty string"


def test_password_attribute_being_none(setup_user_db_tests):
    """TypeError raised if tyring to assign None to the password attribute."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].password = None
    assert str(cm.value) == "User.password cannot be None"


def test_password_attribute_works_as_expected(setup_user_db_tests):
    """password attribute works as expected."""
    data = setup_user_db_tests
    test_password = "a new test password"
    data["test_user"].password = test_password
    assert data["test_user"].password != test_password


def test_password_argument_being_scrambled(setup_user_db_tests):
    """password is scrambled if trying to store it."""
    data = setup_user_db_tests
    test_password = "a new test password"
    data["kwargs"]["password"] = test_password
    new_user = User(**data["kwargs"])
    assert new_user.password != test_password


def test_password_attribute_being_scrambled(setup_user_db_tests):
    """password is scrambled if trying to store it."""
    data = setup_user_db_tests
    test_password = "a new test password"
    data["test_user"].password = test_password

    # test if they are not the same anymore
    assert data["test_user"].password != test_password


def test_check_password_works_as_expected(setup_user_db_tests):
    """check_password method works as expected."""
    data = setup_user_db_tests
    test_password = "a new test password"
    data["test_user"].password = test_password

    # check if it is scrambled
    assert data["test_user"].password != test_password

    # check if check_password returns True
    assert data["test_user"].check_password(test_password) is True

    # check if check_password returns False
    assert data["test_user"].check_password("wrong pass") is False


def test_groups_argument_for_none(setup_user_db_tests):
    """groups attribute an empty list if the groups argument is None."""
    data = setup_user_db_tests
    data["kwargs"]["groups"] = None
    new_user = User(**data["kwargs"])
    assert new_user.groups == []


def test_groups_attribute_for_none(setup_user_db_tests):
    """TypeError raised if groups attribute is set to None."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].groups = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_groups_argument_accepts_only_group_instances(setup_user_db_tests):
    """TypeError raised if group arg is not a Group instance."""
    data = setup_user_db_tests
    data["kwargs"]["groups"] = "a_group"
    with pytest.raises(TypeError) as cm:
        User(**data["kwargs"])

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_groups_attribute_accepts_only_group_instances(setup_user_db_tests):
    """TypeError raised if group attr is not a Group instance."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].groups = "a_group"
    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_groups_attribute_works_as_expected(setup_user_db_tests):
    """groups attribute works as expected."""
    data = setup_user_db_tests
    test_pg = [data["test_group3"]]
    data["test_user"].groups = test_pg
    assert data["test_user"].groups == test_pg


def test_groups_attribute_elements_accepts_group_only_1(setup_user_db_tests):
    """TypeError raised if groups list appended a non Group object."""
    data = setup_user_db_tests
    # append
    with pytest.raises(TypeError) as cm:
        data["test_user"].groups.append(0)
    assert str(cm.value) == (
        "Any group in User.groups should be an instance of "
        "stalker.models.auth.Group, not int: '0'"
    )


def test_groups_attribute_elements_accepts_group_only_2(setup_user_db_tests):
    """TypeError raised if groups list set an item other than a Group instance."""
    data = setup_user_db_tests
    # __setitem__
    with pytest.raises(TypeError) as cm:
        data["test_user"].groups[0] = 0
    assert str(cm.value) == (
        "Any group in User.groups should be an instance of "
        "stalker.models.auth.Group, not int: '0'"
    )


def test_projects_attribute_is_none(setup_user_db_tests):
    """TypeError raised if the projects attribute is set to None."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].projects = None
    assert str(cm.value) == "'NoneType' object is not iterable"


def test_projects_attribute_is_set_to_a_value_which_is_not_a_list(setup_user_db_tests):
    """projects attribute is accepting lists only."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].projects = "not a list"

    assert str(cm.value) == (
        "ProjectUser.project should be a stalker.models.project.Project "
        "instance, not str: 'n'"
    )


def test_projects_attribute_is_set_to_list_of_other_objects_than_project_instances(
    setup_user_db_tests,
):
    """TypeError raised if the projects attr is not all Project instances."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].projects = ["not", "a", "list", "of", "projects", 32]

    assert (
        str(cm.value)
        == "ProjectUser.project should be a stalker.models.project.Project "
        "instance, not str: 'not'"
    )


def test_projects_attribute_is_working_as_expected(setup_user_db_tests):
    """projects attribute is working as expected."""
    data = setup_user_db_tests
    data["test_user"].rate = 102.0
    test_list = [data["test_project1"], data["test_project2"]]
    data["test_user"].projects = test_list
    assert sorted(test_list, key=lambda x: x.name) == sorted(
        data["test_user"].projects, key=lambda x: x.name
    )
    data["test_user"].projects.append(data["test_project3"])
    assert data["test_project3"] in data["test_user"].projects
    # also check the back ref
    assert data["test_user"] in data["test_project1"].users
    assert data["test_user"] in data["test_project2"].users
    assert data["test_user"] in data["test_project3"].users


def test_tasks_attribute_none(setup_user_db_tests):
    """TypeError raised if the tasks attribute is set to None."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].tasks = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_tasks_attribute_accepts_only_list_of_task_objects(setup_user_db_tests):
    """TypeError raised if tasks arg is not all Task instances."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].tasks = "aTask1"

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_tasks_attribute_accepts_an_empty_list(setup_user_db_tests):
    """nothing happens if trying to assign an empty list to tasks attribute."""
    data = setup_user_db_tests
    # this should work without any error
    data["test_user"].tasks = []


def test_tasks_attribute_works_as_expected(setup_user_db_tests):
    """tasks attribute is working as expected."""
    data = setup_user_db_tests
    tasks = [
        data["test_task1"],
        data["test_task2"],
        data["test_task3"],
        data["test_task4"],
    ]
    data["test_user"].tasks = tasks
    assert data["test_user"].tasks == tasks


def test_tasks_attribute_elements_accepts_tasks_only(setup_user_db_tests):
    """TypeError raised if tasks is not all Task instances."""
    data = setup_user_db_tests
    # append
    with pytest.raises(TypeError) as cm:
        data["test_user"].tasks.append(0)

    assert str(cm.value) == (
        "Any element in User.tasks should be an instance of "
        "stalker.models.task.Task, not int: '0'"
    )


def test_equality_operator(setup_user_db_tests):
    """equality of two users."""
    data = setup_user_db_tests
    data["kwargs"].update(
        {
            "name": "Generic User",
            "description": "this is a different user",
            "login": "guser",
            "email": "generic.user@generic.com",
            "password": "verysecret",
        }
    )
    new_user = User(**data["kwargs"])
    assert not data["test_user"] == new_user


def test_inequality_operator(setup_user_db_tests):
    """inequality of two users."""
    data = setup_user_db_tests
    data["kwargs"].update(
        {
            "name": "Generic User",
            "description": "this is a different user",
            "login": "guser",
            "email": "generic.user@generic.com",
            "password": "verysecret",
        }
    )
    new_user = User(**data["kwargs"])
    assert data["test_user"] != new_user


def test___repr__(setup_user_db_tests):
    """representation."""
    data = setup_user_db_tests
    assert data["test_user"].__repr__() == "<{} ('{}') (User)>".format(
        data["test_user"].name, data["test_user"].login
    )


def test_tickets_attribute_is_an_empty_list_by_default(setup_user_db_tests):
    """User.tickets is an empty list by default."""
    data = setup_user_db_tests
    assert data["test_user"].tickets == []


def test_open_tickets_attribute_is_an_empty_list_by_default(setup_user_db_tests):
    """User.open_tickets is an empty list by default."""
    data = setup_user_db_tests
    assert data["test_user"].open_tickets == []


def test_tickets_attribute_is_read_only(setup_user_db_tests):
    """User.tickets attribute is a read only attribute."""
    data = setup_user_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_user"].tickets = []

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'tickets'",
    }.get(sys.version_info.minor, "property 'tickets' of 'User' object has no setter")

    assert str(cm.value) == error_message


def test_open_tickets_attribute_is_read_only(setup_user_db_tests):
    """User.open_tickets attribute is a read only attribute."""
    data = setup_user_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_user"].open_tickets = []

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'open_tickets'",
    }.get(
        sys.version_info.minor, "property 'open_tickets' of 'User' object has no setter"
    )

    assert str(cm.value) == error_message


def test_tickets_attribute_returns_all_tickets_owned_by_this_user(setup_user_db_tests):
    """User.tickets returns all the tickets owned by this user."""
    data = setup_user_db_tests
    assert len(data["test_user"].tasks) == 0
    # there should be no tickets assigned to this user
    assert data["test_user"].tickets == []

    # be careful not all of these are open tickets
    data["test_ticket1"].reassign(data["test_user"], data["test_user"])
    data["test_ticket2"].reassign(data["test_user"], data["test_user"])
    data["test_ticket3"].reassign(data["test_user"], data["test_user"])
    data["test_ticket4"].reassign(data["test_user"], data["test_user"])
    data["test_ticket5"].reassign(data["test_user"], data["test_user"])
    data["test_ticket6"].reassign(data["test_user"], data["test_user"])
    data["test_ticket7"].reassign(data["test_user"], data["test_user"])
    data["test_ticket8"].reassign(data["test_user"], data["test_user"])

    # now we should have some tickets
    assert len(data["test_user"].tickets) > 0

    # now check for exact items
    assert sorted(data["test_user"].tickets, key=lambda x: x.name) == sorted(
        [data["test_ticket2"], data["test_ticket3"], data["test_ticket4"]],
        key=lambda x: x.name,
    )


def test_open_tickets_attribute_returns_all_open_tickets_owned_by_this_user(
    setup_user_db_tests,
):
    """User.open_tickets returns all the open tickets owned by this user."""
    data = setup_user_db_tests
    assert len(data["test_user"].tasks) == 0

    # there should be no tickets assigned to this user
    assert data["test_user"].open_tickets == []

    # assign the user to some tickets
    data["test_ticket1"].reopen(data["test_user"])
    data["test_ticket2"].reopen(data["test_user"])
    data["test_ticket3"].reopen(data["test_user"])
    data["test_ticket4"].reopen(data["test_user"])
    data["test_ticket5"].reopen(data["test_user"])
    data["test_ticket6"].reopen(data["test_user"])
    data["test_ticket7"].reopen(data["test_user"])
    data["test_ticket8"].reopen(data["test_user"])

    # be careful not all of these are open tickets
    data["test_ticket1"].reassign(data["test_user"], data["test_user"])
    data["test_ticket2"].reassign(data["test_user"], data["test_user"])
    data["test_ticket3"].reassign(data["test_user"], data["test_user"])
    data["test_ticket4"].reassign(data["test_user"], data["test_user"])
    data["test_ticket5"].reassign(data["test_user"], data["test_user"])
    data["test_ticket6"].reassign(data["test_user"], data["test_user"])
    data["test_ticket7"].reassign(data["test_user"], data["test_user"])
    data["test_ticket8"].reassign(data["test_user"], data["test_user"])

    # now we should have some open tickets
    assert len(data["test_user"].open_tickets) > 0

    # now check for exact items
    assert sorted(data["test_user"].open_tickets, key=lambda x: x.name) == sorted(
        [
            data["test_ticket1"],
            data["test_ticket2"],
            data["test_ticket3"],
            data["test_ticket4"],
            data["test_ticket5"],
            data["test_ticket6"],
            data["test_ticket7"],
            data["test_ticket8"],
        ],
        key=lambda x: x.name,
    )

    # close a couple of them

    data["test_ticket1"].resolve(data["test_user"], FIXED)
    data["test_ticket2"].resolve(data["test_user"], INVALID)
    data["test_ticket3"].resolve(data["test_user"], CANTFIX)

    # new check again
    assert sorted(data["test_user"].open_tickets, key=lambda x: x.name) == sorted(
        [
            data["test_ticket4"],
            data["test_ticket5"],
            data["test_ticket6"],
            data["test_ticket7"],
            data["test_ticket8"],
        ],
        key=lambda x: x.name,
    )


def test_tjp_id_is_working_as_expected(setup_user_db_tests):
    """tjp_id is working as expected."""
    data = setup_user_db_tests
    assert data["test_user"].tjp_id == "User_{}".format(data["test_user"].id)


def test_to_tjp_is_working_as_expected(setup_user_db_tests):
    """to_tjp property is working as expected."""
    data = setup_user_db_tests
    expected_tjp = 'resource User_{} "User_{}" {{\n    efficiency 1.0\n}}'.format(
        data["test_user"].id, data["test_user"].id
    )
    assert data["test_user"].to_tjp == expected_tjp


def test_to_tjp_is_working_as_expected_for_a_user_with_vacations(setup_user_db_tests):
    """to_tjp property is working as expected for a user with vacations."""
    data = setup_user_db_tests
    personal_vacation = Type(
        name="Personal", code="PERS", target_entity_type="Vacation"
    )

    Vacation(
        user=data["test_user"],
        type=personal_vacation,
        start=datetime.datetime(2013, 6, 7, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 21, 0, 0, tzinfo=pytz.utc),
    )

    Vacation(
        user=data["test_user"],
        type=personal_vacation,
        start=datetime.datetime(2013, 7, 1, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 7, 15, 0, 0, tzinfo=pytz.utc),
    )

    expected_tjp = """resource User_{} "User_{}" {{
    efficiency 1.0
    vacation 2013-06-07-00:00:00 - 2013-06-21-00:00:00
    vacation 2013-07-01-00:00:00 - 2013-07-15-00:00:00
}}""".format(
        data["test_user"].id,
        data["test_user"].id,
    )

    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print('---------------')
    # print("Result:")
    # print("-------")
    # print(data["test_user"].to_tjp)

    assert data["test_user"].to_tjp == expected_tjp


def test_vacations_attribute_is_set_to_none(setup_user_db_tests):
    """TypeError raised if the vacations attribute is set to None."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].vacations = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_vacations_attribute_is_not_a_list(setup_user_db_tests):
    """TypeError raised if the vacations attr is set to a value other than a list."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].vacations = "not a list of Vacation instances"
    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_vacations_attribute_is_not_a_list_of_vacation_instances(setup_user_db_tests):
    """TypeError raised if the vacations attr is not a list of all Vacation objects."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].vacations = ["list of", "other", "instances", 1]

    assert str(cm.value) == (
        "All of the elements in User.vacations should be a "
        "stalker.models.studio.Vacation instance, not str: 'list of'"
    )


def test_vacations_attribute_is_working_as_expected(setup_user_db_tests):
    """vacations attribute is working as expected."""
    data = setup_user_db_tests
    some_other_user = User(
        name="Some Other User",
        login="sou",
        email="some@other.user.com",
        password="my password",
    )

    personal_vac_type = Type(
        name="Personal Vacation", code="PERS", target_entity_type="Vacation"
    )

    vac1 = Vacation(
        user=some_other_user,
        type=personal_vac_type,
        start=datetime.datetime(2013, 6, 7, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 10, tzinfo=pytz.utc),
    )

    assert vac1 not in data["test_user"].vacations
    data["test_user"].vacations.append(vac1)
    assert vac1 in data["test_user"].vacations


def test_efficiency_argument_skipped(setup_user_db_tests):
    """efficiency attribute value 1.0 if the efficiency argument is skipped."""
    data = setup_user_db_tests
    data["kwargs"].pop("efficiency")
    new_user = User(**data["kwargs"])
    assert new_user.efficiency == 1.0


def test_efficiency_argument_is_none(setup_user_db_tests):
    """efficiency attribute value 1.0 if the efficiency argument is None."""
    data = setup_user_db_tests
    data["kwargs"]["efficiency"] = None
    new_user = User(**data["kwargs"])
    assert new_user.efficiency == 1.0


def test_efficiency_attribute_is_set_to_none(setup_user_db_tests):
    """efficiency attribute value 1.0 if it is set to None."""
    data = setup_user_db_tests
    data["test_user"].efficiency = 4.0
    data["test_user"].efficiency = None
    assert data["test_user"].efficiency == 1.0


def test_efficiency_argument_is_not_a_float_or_integer(setup_user_db_tests):
    """TypeError raised if the efficiency argument is not a float or integer."""
    data = setup_user_db_tests
    data["kwargs"]["efficiency"] = "not a float or integer"
    with pytest.raises(TypeError) as cm:
        User(**data["kwargs"])

    assert str(cm.value) == (
        "User.efficiency should be a float number greater or equal to 0.0, "
        "not str: 'not a float or integer'"
    )


def test_efficiency_attribute_is_not_a_float_or_integer(setup_user_db_tests):
    """TypeError raised if the efficiency attr is not a float or int."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].efficiency = "not a float or integer"

    assert str(cm.value) == (
        "User.efficiency should be a float number greater or equal to 0.0, "
        "not str: 'not a float or integer'"
    )


def test_efficiency_argument_is_a_negative_float_or_integer(setup_user_db_tests):
    """ValueError raised if the efficiency argument is a negative float or integer."""
    data = setup_user_db_tests
    data["kwargs"]["efficiency"] = -1
    with pytest.raises(ValueError) as cm:
        User(**data["kwargs"])

    assert (
        str(cm.value)
        == "User.efficiency should be a float number greater or equal to 0.0, not -1"
    )


def test_efficiency_attribute_is_a_negative_float_or_integer(setup_user_db_tests):
    """ValueError raised if the efficiency attr is set to a negative float or int."""
    data = setup_user_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_user"].efficiency = -2.0

    assert (
        str(cm.value)
        == "User.efficiency should be a float number greater or equal to 0.0, not -2.0"
    )


def test_efficiency_argument_is_working_as_expected(setup_user_db_tests):
    """efficiency argument value is correctly passed to the efficiency attribute."""
    data = setup_user_db_tests
    # integer value
    data["kwargs"]["efficiency"] = 2
    new_user = User(**data["kwargs"])
    assert new_user.efficiency == 2.0

    # float value
    data["kwargs"]["efficiency"] = 2.3
    new_user = User(**data["kwargs"])
    assert new_user.efficiency == 2.3


def test_efficiency_attribute_is_working_as_expected(setup_user_db_tests):
    """efficiency attribute value can correctly be changed"""
    data = setup_user_db_tests
    # integer
    assert data["test_user"].efficiency != 2

    data["test_user"].efficiency = 2
    assert data["test_user"].efficiency == 2.0

    # float
    assert data["test_user"].efficiency != 2.3

    data["test_user"].efficiency = 2.3
    assert data["test_user"].efficiency == 2.3


def test_companies_argument_is_skipped(setup_user_db_tests):
    """companies attribute set to an empty list if the company argument is skipped."""
    data = setup_user_db_tests
    data["kwargs"].pop("companies")
    new_user = User(**data["kwargs"])
    assert new_user.companies == []


def test_companies_argument_is_none(setup_user_db_tests):
    """companies argument is set to None the companies attribute an empty list."""
    data = setup_user_db_tests
    data["kwargs"]["companies"] = None
    new_user = User(**data["kwargs"])
    assert new_user.companies == []


def test_companies_attribute_is_set_to_none(setup_user_db_tests):
    """the companies attribute an empty list if it is set to None."""
    data = setup_user_db_tests
    assert data["test_user"].companies is not None
    with pytest.raises(TypeError) as cm:
        data["test_user"].companies = None
    assert str(cm.value) == "'NoneType' object is not iterable"


def test_companies_argument_is_not_a_list(setup_user_db_tests):
    """TypeError raised if the companies argument is not a list."""
    data = setup_user_db_tests
    data["kwargs"]["companies"] = "not a list of clients"
    with pytest.raises(TypeError) as cm:
        User(**data["kwargs"])

    assert str(cm.value) == (
        "ClientUser.client should be instance of stalker.models.client.Client, "
        "not str: 'n'"
    )


def test_companies_argument_is_not_a_list_of_client_instances(setup_user_db_tests):
    """TypeError raised if the companies argument is not a list of Client instances."""
    data = setup_user_db_tests
    test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
    data["kwargs"]["companies"] = test_value
    with pytest.raises(TypeError) as cm:
        User(**data["kwargs"])

    assert (
        str(cm.value) == "ClientUser.client should be instance of "
        "stalker.models.client.Client, not int: '1'"
    )


def test_companies_attribute_is_set_to_a_value_other_than_a_list_of_client_instances(
    setup_user_db_tests,
):
    """TypeError raised if the companies attr is not list of all Client instances."""
    data = setup_user_db_tests
    test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
    with pytest.raises(TypeError) as cm:
        data["test_user"].companies = test_value

    assert str(cm.value) == (
        "ClientUser.client should be instance of stalker.models.client.Client, "
        "not int: '1'"
    )


def test_companies_attribute_is_working_as_expected(setup_user_db_tests):
    """from issue #27."""
    new_companies = []
    c1 = Client(name="Company X")
    c2 = Client(name="Company Y")
    c3 = Client(name="Company Z")
    DBSession.add_all([c1, c2, c3])
    DBSession.commit()

    c1 = Client.query.filter_by(name="Company X").first()
    c2 = Client.query.filter_by(name="Company Y").first()
    c3 = Client.query.filter_by(name="Company Z").first()

    user = User(
        name="test_user",
        password="1234",
        email="a@a.com",
        login="test_user",
        clients=[c3],
    )
    DBSession.commit()

    new_companies.append(c1)
    new_companies.append(c2)
    user.companies = new_companies
    DBSession.commit()

    assert c1 in user.companies
    assert c2 in user.companies
    assert c3 not in user.companies


def test_companies_attribute_is_working_as_expected_2(setup_user_db_tests):
    """from issue #27."""
    c1 = Client(name="Company X")
    c2 = Client(name="Company Y")
    c3 = Client(name="Company Z")

    user = User(
        name="Fredrik",
        login="fredrik",
        email="f@f.f",
        password="pass",
        companies=[c1, c2, c3],
    )

    DBSession.add(user)

    assert c1 in DBSession
    assert c2 in DBSession
    assert c3 in DBSession

    DBSession.commit()

    c1 = Client(name="New Company X")
    c2 = Client(name="New Company Y")
    c3 = Client(name="New Company Z")

    DBSession.add_all([c1, c2, c3])
    DBSession.commit()

    user = User.query.filter_by(name="Fredrik").first()
    user.companies = [c1, c2, c3]

    DBSession.commit()


def test_watching_attribute_is_a_list_of_other_values_than_task(setup_user_db_tests):
    """TypeError raised if the watching attr not a list of all Task instances."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].watching = ["not", 1, "list of tasks"]

    assert str(cm.value) == (
        "Any element in User.watching should be an instance of "
        "stalker.models.task.Task, not str: 'not'"
    )


def test_watching_attribute_is_working_as_expected(setup_user_db_tests):
    """watching attribute is working as expected."""
    data = setup_user_db_tests
    test_value = [data["test_task1"], data["test_task2"]]
    assert data["test_user"].watching == []
    data["test_user"].watching = test_value
    assert sorted(test_value, key=lambda x: x.name) == sorted(
        data["test_user"].watching, key=lambda x: x.name
    )


def test_rate_argument_is_skipped(setup_user_db_tests):
    """rate attribute 0 if the rate argument is skipped."""
    data = setup_user_db_tests
    if "rate" in data["kwargs"]:
        data["kwargs"].pop("rate")
    new_user = User(**data["kwargs"])
    assert new_user.rate == 0


def test_rate_argument_is_none(setup_user_db_tests):
    """rate attribute 0 if the rate argument is None."""
    data = setup_user_db_tests
    data["kwargs"]["rate"] = None
    new_user = User(**data["kwargs"])
    assert new_user.rate == 0


def test_rate_attribute_is_set_to_none(setup_user_db_tests):
    """rate set to 0 if it is set to None."""
    data = setup_user_db_tests
    assert data["test_user"].rate is not None

    data["test_user"].rate = None
    assert data["test_user"].rate == 0


def test_rate_argument_is_not_a_float_or_integer_value(setup_user_db_tests):
    """TypeError raised if the rate argument is not an integer or float value."""
    data = setup_user_db_tests
    data["kwargs"]["rate"] = "some string"
    with pytest.raises(TypeError) as cm:
        User(**data["kwargs"])

    assert str(cm.value) == (
        "User.rate should be a float number greater or equal to 0.0, "
        "not str: 'some string'"
    )


def test_rate_attribute_is_not_a_float_or_integer_value(setup_user_db_tests):
    """TypeError raised if the rate attr is not an int or float."""
    data = setup_user_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_user"].rate = "some string"

    assert str(cm.value) == (
        "User.rate should be a float number greater or equal to 0.0, "
        "not str: 'some string'"
    )


def test_rate_argument_is_a_negative_number(setup_user_db_tests):
    """ValueError raised if the rate argument is a negative value."""
    data = setup_user_db_tests
    data["kwargs"]["rate"] = -1
    with pytest.raises(ValueError) as cm:
        User(**data["kwargs"])

    assert (
        str(cm.value)
        == "User.rate should be a float number greater or equal to 0.0, not -1"
    )


def test_rate_attribute_is_set_to_a_negative_number(setup_user_db_tests):
    """ValueError raised if the rate attribute is set to a negative number."""
    data = setup_user_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_user"].rate = -1

    assert (
        str(cm.value)
        == "User.rate should be a float number greater or equal to 0.0, not -1"
    )


def test_rate_argument_is_working_as_expected(setup_user_db_tests):
    """rate argument is working as expected."""
    data = setup_user_db_tests
    test_value = 102.3
    data["kwargs"]["rate"] = test_value
    new_user = User(**data["kwargs"])
    assert new_user.rate == test_value


def test_rate_attribute_is_working_as_expected(setup_user_db_tests):
    """rate attribute is working as expected."""
    data = setup_user_db_tests
    test_value = 212.5
    assert data["test_user"].rate != test_value
    data["test_user"].rate = test_value
    assert data["test_user"].rate == test_value


def test_hash_value():
    """__hash__ returns the hash of the User instance."""
    user = User(
        name="Erkan Ozgur Yilmaz",
        login="eoyilmaz",
        password="hidden",
        email="eoyilmaz@fake.com",
    )
    result = hash(user)
    assert isinstance(result, int)
