# -*- coding: utf-8 -*-
"""Tests for the Task class."""

import copy
import datetime
import os
import sys
import warnings

import pytest

import pytz

import stalker
import stalker.db.setup
from stalker import (
    Entity,
    FilenameTemplate,
    Good,
    Project,
    Repository,
    Status,
    StatusList,
    Structure,
    Studio,
    Task,
    Ticket,
    TimeLog,
    Type,
    User,
    defaults,
)
from stalker.db.session import DBSession
from stalker.exceptions import CircularDependencyError
from stalker.models.mixins import (
    DateRangeMixin,
    DependencyTarget,
    ScheduleConstraint,
    ScheduleModel,
    TimeUnit,
)


@pytest.fixture(scope="function")
def setup_task_tests():
    """tests that doesn't require a database."""
    data = dict()
    defaults.config_values = defaults.default_config_values.copy()
    defaults["timing_resolution"] = datetime.timedelta(hours=1)
    assert defaults.daily_working_hours == 9
    assert defaults.weekly_working_days == 5
    assert defaults.yearly_working_days == 261

    data["status_wfd"] = Status(name="Waiting For Dependency", code="WFD")
    data["status_rts"] = Status(name="Ready To Start", code="RTS")
    data["status_wip"] = Status(name="Work In Progress", code="WIP")
    data["status_prev"] = Status(name="Pending Review", code="PREV")
    data["status_hrev"] = Status(name="Has Revision", code="HREV")
    data["status_drev"] = Status(name="Dependency Has Revision", code="DREV")
    data["status_oh"] = Status(name="On Hold", code="OH")
    data["status_stop"] = Status(name="Stopped", code="STOP")
    data["status_cmpl"] = Status(name="Completed", code="CMPL")

    data["task_status_list"] = StatusList(
        statuses=[
            data["status_wfd"],
            data["status_rts"],
            data["status_wip"],
            data["status_prev"],
            data["status_hrev"],
            data["status_drev"],
            data["status_oh"],
            data["status_stop"],
            data["status_cmpl"],
        ],
        target_entity_type="Task",
    )

    data["test_project_status_list"] = StatusList(
        name="Project Statuses",
        statuses=[data["status_wip"], data["status_prev"], data["status_cmpl"]],
        target_entity_type="Project",
    )

    data["test_movie_project_type"] = Type(
        name="Movie Project",
        code="movie",
        target_entity_type="Project",
    )

    data["test_repository_type"] = Type(
        name="Test Repository Type",
        code="test",
        target_entity_type="Repository",
    )

    data["test_repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["test_repository_type"],
        linux_path="/mnt/T/",
        windows_path="T:/",
        macos_path="/Volumes/T/",
    )

    data["test_user1"] = User(
        name="User1", login="user1", email="user1@user1.com", password="1234"
    )

    data["test_user2"] = User(
        name="User2", login="user2", email="user2@user2.com", password="1234"
    )

    data["test_user3"] = User(
        name="User3", login="user3", email="user3@user3.com", password="1234"
    )

    data["test_user4"] = User(
        name="User4", login="user4", email="user4@user4.com", password="1234"
    )

    data["test_user5"] = User(
        name="User5", login="user5", email="user5@user5.com", password="1234"
    )

    data["test_project1"] = Project(
        name="Test Project1",
        code="tp1",
        type=data["test_movie_project_type"],
        status_list=data["test_project_status_list"],
        repositories=[data["test_repository"]],
    )

    data["test_dependent_task1"] = Task(
        name="Dependent Task1",
        project=data["test_project1"],
        status_list=data["task_status_list"],
        responsible=[data["test_user1"]],
    )

    data["test_dependent_task2"] = Task(
        name="Dependent Task2",
        project=data["test_project1"],
        status_list=data["task_status_list"],
        responsible=[data["test_user1"]],
    )

    data["kwargs"] = {
        "name": "Modeling",
        "description": "A Modeling Task",
        "project": data["test_project1"],
        "priority": 500,
        "responsible": [data["test_user1"]],
        "resources": [data["test_user1"], data["test_user2"]],
        "alternative_resources": [
            data["test_user3"],
            data["test_user4"],
            data["test_user5"],
        ],
        "allocation_strategy": "minloaded",
        "persistent_allocation": True,
        "watchers": [data["test_user3"]],
        "bid_timing": 4,
        "bid_unit": TimeUnit.Day,
        "schedule_timing": 1,
        "schedule_unit": TimeUnit.Day,
        "start": datetime.datetime(2013, 4, 8, 13, 0, tzinfo=pytz.utc),
        "end": datetime.datetime(2013, 4, 8, 18, 0, tzinfo=pytz.utc),
        "depends_on": [data["test_dependent_task1"], data["test_dependent_task2"]],
        "time_logs": [],
        "versions": [],
        "is_milestone": False,
        "status": 0,
        "status_list": data["task_status_list"],
    }
    yield data
    defaults.config_values = copy.deepcopy(defaults.default_config_values)
    defaults["timing_resolution"] = datetime.timedelta(hours=1)


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Task class."""
    assert Task.__auto_name__ is False


def test_priority_arg_is_skipped_defaults_to_task_priority(setup_task_tests):
    """priority arg skipped priority attr defaults to task_priority."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("priority")
    new_task = Task(**kwargs)
    assert new_task.priority == defaults.task_priority


def test_priority_arg_is_given_as_none_defaults_to_task_priority(
    setup_task_tests,
):
    """priority arg is None defaults the priority attr to task_priority."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["priority"] = None
    new_task = Task(**kwargs)
    assert new_task.priority == defaults.task_priority


def test_priority_attribute_is_given_as_none_defaults_to_task_priority(
    setup_task_tests,
):
    """priority attr is None defaults the priority attr to task_priority."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    new_task.priority = None
    assert new_task.priority == defaults.task_priority


def test_priority_arg_any_given_other_value_then_int_defaults_to_task_priority(
    setup_task_tests,
):
    """TypeError raised if the priority arg value is not an int."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["priority"] = "a324"
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.priority should be an integer value between 0 and 1000, not str: 'a324'"
    )


def test_priority_attribute_is_not_an_int(setup_task_tests):
    """TypeError raised if priority attr not a number."""
    data = setup_task_tests
    test_value = "test_value_324"
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.priority = test_value

    assert str(cm.value) == (
        "Task.priority should be an integer value between 0 and 1000, "
        "not str: 'test_value_324'"
    )


def test_priority_arg_is_negative(setup_task_tests):
    """priority arg is negative value sets the priority attribute to zero."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["priority"] = -1
    new_task = Task(**kwargs)
    assert new_task.priority == 0


def test_priority_attr_is_negative(setup_task_tests):
    """priority attr is given as a negative value sets the priority attr to zero."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    new_task.priority = -1
    assert new_task.priority == 0


def test_priority_arg_is_too_big(setup_task_tests):
    """priority arg is bigger than 1000 clamps the priority attr value to 1000."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["priority"] = 1001
    new_task = Task(**kwargs)
    assert new_task.priority == 1000


def test_priority_attr_is_too_big(setup_task_tests):
    """priority attr is set to a value bigger than 1000 clamps the value to 1000."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    new_task.priority = 1001
    assert new_task.priority == 1000


@pytest.mark.parametrize("test_value", [500.1, 334.23])
def test_priority_arg_is_float(test_value, setup_task_tests):
    """float numbers for priority arg is converted to int."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["priority"] = test_value
    new_task = Task(**kwargs)
    assert new_task.priority == int(test_value)


@pytest.mark.parametrize("test_value", [500.1, 334.23])
def test_priority_attr_is_float(test_value, setup_task_tests):
    """float numbers for priority attr is converted to int."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    new_task.priority = test_value
    assert new_task.priority == int(test_value)


def test_priority_attr_is_working_as_expected(setup_task_tests):
    """priority attr is working as expected."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    test_value = 234
    new_task.priority = test_value
    assert new_task.priority == test_value


def test_resources_arg_is_skipped(setup_task_tests):
    """resources attr is an empty list if the resources arg is skipped."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("resources")
    new_task = Task(**kwargs)
    assert new_task.resources == []


def test_resources_arg_is_none(setup_task_tests):
    """resources attr is an empty list if the resources arg is None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["resources"] = None
    new_task = Task(**kwargs)
    assert new_task.resources == []


def test_resources_attr_is_none(setup_task_tests):
    """TypeError raised whe the resources attr is set to None."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.resources = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_resources_arg_is_not_list(setup_task_tests):
    """TypeError raised if the resources arg is not a list."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["resources"] = "a resource"
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_resources_attr_is_not_list(setup_task_tests):
    """TypeError raised if the resources attr is set to any other value then a list."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.resources = "a resource"
    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_resources_arg_is_set_to_a_list_of_other_values_then_user(
    setup_task_tests,
):
    """TypeError raised if the resources arg is set to a list non User."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["resources"] = ["a", "list", "of", "resources", data["test_user1"]]
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.resources should be a list of stalker.models.auth.User instances, "
        "not str: 'a'"
    )


def test_resources_attr_is_set_to_a_list_of_other_values_then_user(
    setup_task_tests,
):
    """TypeError raised if the resources attr is set to a list of non User."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.resources = ["a", "list", "of", "resources", data["test_user1"]]

    assert str(cm.value) == (
        "Task.resources should be a list of stalker.models.auth.User instances, "
        "not str: 'a'"
    )


def test_resources_attr_is_working_as_expected(setup_task_tests):
    """resources attr is working as expected."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    test_value = [data["test_user1"]]
    new_task.resources = test_value
    assert new_task.resources == test_value


def test_resources_arg_back_references_to_user(setup_task_tests):
    """User in the resources arg has the current task in their "User.tasks" attr."""
    data = setup_task_tests
    # create a couple of new users
    new_user1 = User(
        name="test1", login="test1", email="test1@test.com", password="test1"
    )
    new_user2 = User(
        name="test2", login="test2", email="test2@test.com", password="test2"
    )

    # assign it to a newly created task
    kwargs = copy.copy(data["kwargs"])
    kwargs["resources"] = [new_user1]
    new_task = Task(**kwargs)

    # now check if the user has the task in its tasks list
    assert new_task in new_user1.tasks

    # now change the resources list
    new_task.resources = [new_user2]
    assert new_task in new_user2.tasks
    assert new_task not in new_user1.tasks

    # now append the new resource
    new_task.resources.append(new_user1)
    assert new_task in new_user1.tasks

    # clean up test
    new_task.resources = []


def test_resources_attr_back_references_to_user(setup_task_tests):
    """User in the resources arg has the current task in their "User.tasks" attr."""
    data = setup_task_tests
    # create a new user
    new_user = User(
        name="Test User",
        login="test_user",
        email="testuser@test.com",
        password="test_pass",
    )
    # assign it to a newly created task
    # data["kwargs"]["resources"] = [new_user]
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    new_task.resources = [new_user]
    # now check if the user has the task in its tasks list
    assert new_task in new_user.tasks


def test_resources_attr_clears_itself_from_the_previous_users(
    setup_task_tests,
):
    """resources attr is update clears itself from the current resources tasks attr."""
    data = setup_task_tests
    # create a couple of new users
    new_user1 = User(
        name="Test User1",
        login="test_user1",
        email="testuser1@test.com",
        password="test_pass",
    )
    new_user2 = User(
        name="Test User2",
        login="test_user2",
        email="testuser2@test.com",
        password="test_pass",
    )
    new_user3 = User(
        name="Test User3",
        login="test_user3",
        email="testuser3@test.com",
        password="test_pass",
    )
    new_user4 = User(
        name="Test User4",
        login="test_user4",
        email="testuser4@test.com",
        password="test_pass",
    )

    # now add the 1 and 2 to the resources with the resources arg
    # assign it to a newly created task
    kwargs = copy.copy(data["kwargs"])
    kwargs["resources"] = [new_user1, new_user2]
    new_task = Task(**kwargs)

    # now check if the user has the task in its tasks list
    assert new_task in new_user1.tasks
    assert new_task in new_user2.tasks

    # now update the resources list
    new_task.resources = [new_user3, new_user4]

    # now check if the new resources has the task in their tasks attr
    assert new_task in new_user3.tasks
    assert new_task in new_user4.tasks

    # and if it is not in the previous users tasks
    assert new_task not in new_user1.tasks
    assert new_task not in new_user2.tasks


def test_watchers_arg_is_skipped(setup_task_tests):
    """watchers attr is an empty list if the watchers arg is skipped."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("watchers")
    new_task = Task(**kwargs)
    assert new_task.watchers == []


def test_watchers_arg_is_none(setup_task_tests):
    """watchers attr is an empty list if the watchers arg is None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["watchers"] = None
    new_task = Task(**kwargs)
    assert new_task.watchers == []


def test_watchers_attr_is_none(setup_task_tests):
    """TypeError raised whe the watchers attr is set to None."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.watchers = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_watchers_arg_is_not_list(setup_task_tests):
    """TypeError raised if the watchers arg is not a list."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["watchers"] = "a resource"
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_watchers_attr_is_not_list(setup_task_tests):
    """TypeError raised if the watchers attr is set to any other value then a list."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.watchers = "a resource"
    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_watchers_arg_is_set_to_a_list_of_other_values_then_user(setup_task_tests):
    """TypeError raised if the watchers arg is not a list of User instances."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["watchers"] = ["a", "list", "of", "watchers", data["test_user1"]]
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.watchers should be a list of stalker.models.auth.User instances,"
        " not str: 'a'"
    )


def test_watchers_attr_is_set_to_a_list_of_other_values_then_user(
    setup_task_tests,
):
    """TypeError raised if the watchers attr is set to a list of non User objects."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    test_values = ["a", "list", "of", "watchers", data["test_user1"]]
    with pytest.raises(TypeError):
        new_task.watchers = test_values


def test_watchers_attr_is_working_as_expected(setup_task_tests):
    """watchers attr is working as expected."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    test_value = [data["test_user1"]]
    new_task.watchers = test_value
    assert new_task.watchers == test_value


def test_watchers_arg_back_references_to_user(setup_task_tests):
    """User in the watchers arg has the current task in their "User.watching" attr."""
    data = setup_task_tests
    # create a couple of new users
    new_user1 = User(
        name="new_user1",
        login="new_user1",
        email="new_user1@test.com",
        password="new_user1",
    )
    new_user2 = User(
        name="new_user2",
        login="new_user2",
        email="new_user2@test.com",
        password="new_user2",
    )
    # assign it to a newly created task
    kwargs = copy.copy(data["kwargs"])
    kwargs["watchers"] = [new_user1]
    new_task = Task(**kwargs)

    # now check if the user has the task in its tasks list
    assert new_task in new_user1.watching

    # now change the watchers list
    new_task.watchers = [new_user2]
    assert new_task in new_user2.watching
    assert new_task not in new_user1.watching

    # now append the new user
    new_task.watchers.append(new_user1)
    assert new_task in new_user1.watching


def test_watchers_attr_back_references_to_user(setup_task_tests):
    """User in the watchers arg has the current task in their "User.watching" attr."""
    data = setup_task_tests
    # create a new user
    new_user = User(
        name="new_user",
        login="new_user",
        email="new_user@test.com",
        password="new_user",
    )

    # assign it to a newly created task
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    new_task.watchers = [new_user]

    # now check if the user has the task in its watching list
    assert new_task in new_user.watching


def test_watchers_attr_clears_itself_from_the_previous_users(setup_task_tests):
    """watchers attr is updated clears itself from the watchers watching attr."""
    data = setup_task_tests
    # create a couple of new users
    new_user1 = User(
        name="new_user1",
        login="new_user1",
        email="new_user1@test.com",
        password="new_user1",
    )
    new_user2 = User(
        name="new_user2",
        login="new_user2",
        email="new_user2@test.com",
        password="new_user2",
    )
    new_user3 = User(
        name="new_user3",
        login="new_user3",
        email="new_user3@test.com",
        password="new_user3",
    )
    new_user4 = User(
        name="new_user4",
        login="new_user4",
        email="new_user4@test.com",
        password="new_user4",
    )
    # now add the 1 and 2 to the watchers with the watchers arg
    # assign it to a newly created task
    kwargs = copy.copy(data["kwargs"])
    kwargs["watchers"] = [new_user1, new_user2]
    new_task = Task(**kwargs)

    # now check if the user has the task in its watching list
    assert new_task in new_user1.watching
    assert new_task in new_user2.watching

    # now update the watchers list
    new_task.watchers = [new_user3, new_user4]

    # now check if the new watchers has the task in their watching
    # attr
    assert new_task in new_user3.watching
    assert new_task in new_user4.watching

    # and if it is not in the previous users watching list
    assert new_task not in new_user1.watching
    assert new_task not in new_user2.watching


def test_depends_arg_is_skipped_depends_attr_is_empty_list(setup_task_tests):
    """ "depends_on" attr is an empty list if the "depends_on" arg is skipped."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("depends_on")
    new_task = Task(**kwargs)
    assert new_task.depends_on == []


def test_depends_arg_is_none_depends_attr_is_empty_list(setup_task_tests):
    """ "depends_on" attr is an empty list if the "depends_on" arg is None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None
    new_task = Task(**kwargs)
    assert new_task.depends_on == []


def test_depends_arg_is_not_a_list(setup_task_tests):
    """TypeError raised if the "depends_on" arg is not a list."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = data["test_dependent_task1"]
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)
    assert str(cm.value) == "'Task' object is not iterable"


def test_depends_attr_is_not_a_list(setup_task_tests):
    """TypeError raised if the "depends_on" attr is set to something else then a list."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    with pytest.raises(TypeError) as cm:
        new_task.depends_on = data["test_dependent_task1"]
    assert str(cm.value) == "'Task' object is not iterable"


def test_depends_arg_is_a_list_of_other_objects_than_a_task(setup_task_tests):
    """AttributeError raised if the "depends_on" arg is a list of non Task objects."""
    data = setup_task_tests
    test_value = ["a", "dependent", "task", 1, 1.2]
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = test_value
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "TaskDependency.depends_on can should be and instance of "
        "stalker.models.task.Task, not str: 'a'"
    )


def test_depends_attr_is_a_list_of_other_objects_than_a_task(setup_task_tests):
    """AttributeError raised if the "depends_on" attr is set to a list of non Task."""
    data = setup_task_tests
    test_value = ["a", "dependent", "task", 1, 1.2]
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    with pytest.raises(TypeError) as cm:
        new_task.depends_on = test_value

    assert str(cm.value) == (
        "TaskDependency.depends_on can should be and instance of "
        "stalker.models.task.Task, not str: 'a'"
    )


def test_depends_attr_does_not_allow_simple_cyclic_dependencies(setup_task_tests):
    """CircularDependencyError raised if "depends_on" in circular dependency."""
    data = setup_task_tests
    # create two new tasks A, B
    # make B dependent to A
    # and make A dependent to B
    # and expect a CircularDependencyError
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None

    task_a = Task(**kwargs)
    task_b = Task(**kwargs)

    task_b.depends_on = [task_a]

    with pytest.raises(CircularDependencyError) as cm:
        task_a.depends_on = [task_b]

    assert (
        str(cm.value)
        == "<Modeling (Task)> (Task) and <Modeling (Task)> (Task) creates "
        'a circular dependency in their "depends_on" attribute'
    )


def test_depends_attr_does_not_allow_cyclic_dependencies(setup_task_tests):
    """CircularDependencyError raised if "depends_on" attr has a circular dependency."""
    data = setup_task_tests
    # create three new tasks A, B, C
    # make B dependent to A
    # make C dependent to B
    # and make A dependent to C
    # and expect a CircularDependencyError
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None

    kwargs["name"] = "taskA"
    task_a = Task(**kwargs)

    kwargs["name"] = "taskB"
    task_b = Task(**kwargs)

    kwargs["name"] = "taskC"
    task_c = Task(**kwargs)

    task_b.depends_on = [task_a]
    task_c.depends_on = [task_b]

    with pytest.raises(CircularDependencyError) as cm:
        task_a.depends_on = [task_c]

    assert (
        str(cm.value) == "<taskC (Task)> (Task) and <taskA (Task)> (Task) creates a "
        'circular dependency in their "depends_on" attribute'
    )


def test_depends_attr_does_not_allow_more_deeper_cyclic_dependencies(
    setup_task_tests,
):
    """CircularDependencyError raised if depends_on attr has deeper circular dependency."""
    data = setup_task_tests
    # create new tasks A, B, C, D
    # make B dependent to A
    # make C dependent to B
    # make D dependent to C
    # and make A dependent to D
    # and expect a CircularDependencyError
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None

    kwargs["name"] = "taskA"
    task_a = Task(**kwargs)

    kwargs["name"] = "taskB"
    task_b = Task(**kwargs)

    kwargs["name"] = "taskC"
    task_c = Task(**kwargs)

    kwargs["name"] = "taskD"
    task_d = Task(**kwargs)

    task_b.depends_on = [task_a]
    task_c.depends_on = [task_b]
    task_d.depends_on = [task_c]

    with pytest.raises(CircularDependencyError) as cm:
        task_a.depends_on = [task_d]

    assert (
        str(cm.value) == "<taskD (Task)> (Task) and <taskA (Task)> (Task) creates a "
        'circular dependency in their "depends_on" attribute'
    )


def test_depends_arg_cyclic_dependency_bug_2(setup_task_tests):
    """CircularDependencyError raised in the following

    case:
      T1 is parent of T2
      T3 depends on T1
      T2 depends on T3
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None
    kwargs["name"] = "T1"
    t1 = Task(**kwargs)

    kwargs["name"] = "T3"
    t3 = Task(**kwargs)

    t3.depends_on.append(t1)

    kwargs["name"] = "T2"
    kwargs["parent"] = t1
    kwargs["depends_on"] = [t3]

    # the following should generate the CircularDependencyError
    with pytest.raises(CircularDependencyError) as cm:
        Task(**kwargs)

    assert (
        str(cm.value) == "One of the parents of <T2 (Task)> is depending on <T3 (Task)>"
    )


def test_depends_arg_does_not_allow_one_of_the_parents_of_the_task(setup_task_tests):
    """CircularDependencyError raised if "depends_on" attr has one of the parents."""
    data = setup_task_tests
    # create two new tasks A, B
    # make A parent to B
    # and make B dependent to A
    # and expect a CircularDependencyError
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None

    task_a = Task(**kwargs)
    task_b = Task(**kwargs)
    task_c = Task(**kwargs)

    task_b.parent = task_a
    task_a.parent = task_c

    assert task_b in task_a.children
    assert task_a in task_c.children

    with pytest.raises(CircularDependencyError) as cm:
        task_b.depends_on = [task_a]

    assert (
        str(cm.value)
        == "<Modeling (Task)> (Task) and <Modeling (Task)> (Task) creates "
        'a circular dependency in their "children" attribute'
    )

    with pytest.raises(CircularDependencyError) as cm:
        task_b.depends_on = [task_c]

    assert (
        str(cm.value)
        == "<Modeling (Task)> (Task) and <Modeling (Task)> (Task) creates "
        'a circular dependency in their "children" attribute'
    )


def test_depends_arg_is_working_as_expected(setup_task_tests):
    """depends_on arg is working as expected."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None
    task_a = Task(**kwargs)
    task_b = Task(**kwargs)

    kwargs["depends_on"] = [task_a, task_b]
    task_c = Task(**kwargs)

    assert task_a in task_c.depends_on
    assert task_b in task_c.depends_on
    assert len(task_c.depends_on) == 2


def test_depends_attr_is_working_as_expected(setup_task_tests):
    """ "depends_on" attr is working as expected."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None
    task_a = Task(**kwargs)
    task_b = Task(**kwargs)
    task_c = Task(**kwargs)
    task_a.depends_on = [task_b]
    task_a.depends_on.append(task_c)
    assert task_b in task_a.depends_on
    assert task_c in task_a.depends_on


def test_percent_complete_attr_is_read_only(setup_task_tests):
    """percent_complete attr is a read-only attr."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(AttributeError) as cm:
        new_task.percent_complete = 32

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'percent_complete'",
    }.get(
        sys.version_info.minor,
        "property 'percent_complete' of 'Task' object has no setter",
    )

    assert str(cm.value) == error_message


def test_percent_complete_attr_is_working_as_expected_for_a_duration_based_leaf_task_1(
    setup_task_tests,
):
    """percent_complete attr is working as expected for a duration based leaf task.

    #########
               ^
               |
              now
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    kwargs["schedule_model"] = ScheduleModel.Duration

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    new_task = Task(**kwargs)

    new_task.computed_start = now - td(days=2)
    new_task.computed_end = now - td(days=1)

    assert new_task.percent_complete == 100


def test_percent_complete_attr_is_working_as_expected_for_a_duration_based_leaf_task_2(
    setup_task_tests,
):
    """percent_complete attr is working as expected for a duration based leaf task.

    #########
            ^
            |
           now
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    kwargs["schedule_model"] = ScheduleModel.Duration

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    new_task = Task(**kwargs)
    new_task.start = now - td(days=1, hours=1)
    new_task.end = now - td(hours=1)

    assert new_task.percent_complete == 100


def test_percent_complete_attr_is_working_as_expected_for_a_duration_based_leaf_task_3(
    setup_task_tests,
):
    """percent_complete attr is working as expected for a duration based leaf task.

    #########
        ^
        |
       now
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    kwargs["schedule_model"] = ScheduleModel.Duration

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    new_task = Task(**kwargs)
    new_task.start = now - td(hours=12)
    new_task.end = now + td(hours=12)

    # it should be somewhere around 50%
    # due to the timing resolution we cannot know it exactly
    # and I don't want to patch datetime.datetime.now(pytz.utc)
    # this is a very simple test
    assert abs(new_task.percent_complete - 50 < 5)


def test_percent_complete_attr_is_working_as_expected_for_a_duration_based_leaf_task_4(
    setup_task_tests,
):
    """percent_complete attr is working as expected for a duration based leaf task.

     #########
     ^
     |
    now
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    kwargs["schedule_model"] = ScheduleModel.Duration

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    new_task = Task(**kwargs)
    new_task.computed_start = now
    new_task.computed_end = now + td(days=1)

    assert new_task.percent_complete < 5


def test_percent_complete_attr_is_working_as_expected_for_a_duration_based_leaf_task_5(
    setup_task_tests,
):
    """percent_complete attr is working as expected for a duration based leaf task.

       #########
     ^
     |
    now
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    kwargs["schedule_model"] = ScheduleModel.Duration

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    new_task = Task(**kwargs)
    new_task.computed_start = now + td(days=1)
    new_task.computed_end = now + td(days=2)

    assert new_task.percent_complete == 0


def test_is_milestone_arg_is_skipped(setup_task_tests):
    """is_milestone attr is False if the is_milestone arg is skipped."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("is_milestone")
    new_task = Task(**kwargs)
    assert new_task.is_milestone is False


def test_is_milestone_arg_is_none(setup_task_tests):
    """is_milestone attr is set to False if the is_milestone arg is given as None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["is_milestone"] = None
    new_task = Task(**kwargs)
    assert new_task.is_milestone is False


def test_is_milestone_attr_is_none(setup_task_tests):
    """is_milestone attr is False if set to None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    new_task.is_milestone = None
    assert new_task.is_milestone is False


def test_is_milestone_arg_is_not_a_bool(setup_task_tests):
    """TypeError raised if the is_milestone arg is anything other than a bool."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["name"] = "test" + str(0)
    kwargs["is_milestone"] = "A string"
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.is_milestone should be a bool value (True or False), not str: 'A string'"
    )


def test_is_milestone_attr_is_not_a_bool(setup_task_tests):
    """TypeError raised if the is_milestone attr is set not to a bool value."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    test_value = "A string"
    with pytest.raises(TypeError) as cm:
        new_task.is_milestone = test_value

    assert str(cm.value) == (
        "Task.is_milestone should be a bool value (True or False), not str: 'A string'"
    )


def test_is_milestone_arg_makes_the_resources_list_an_empty_list(setup_task_tests):
    """resources is an empty list if the is_milestone arg is given as True."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["is_milestone"] = True
    kwargs["resources"] = [data["test_user1"], data["test_user2"]]
    new_task = Task(**kwargs)
    assert new_task.resources == []


def test_is_milestone_attr_makes_the_resource_list_an_empty_list(setup_task_tests):
    """resources is an empty list if the is_milestone attr is given as True."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    new_task.resources = [data["test_user1"], data["test_user2"]]
    new_task.is_milestone = True
    assert new_task.resources == []


def test_time_logs_attr_is_none(setup_task_tests):
    """TypeError raised if the time_logs attr is set to None."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.time_logs = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_time_logs_attr_is_not_a_list(setup_task_tests):
    """TypeError raised if the time_logs attr is not set to a list."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.time_logs = 123

    assert str(cm.value) == "Incompatible collection type: int is not list-like"


def test_time_logs_attr_is_not_a_list_of_timelog_instances(setup_task_tests):
    """TypeError raised if the time_logs attr is not a list of TimeLog instances."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.time_logs = [1, "1", 1.2, "a time_log"]

    assert str(cm.value) == (
        "Task.time_logs should be all stalker.models.task.TimeLog instances, "
        "not int: '1'"
    )


@pytest.mark.parametrize(
    "schedule_timing, schedule_unit, schedule_seconds",
    [
        [10, "h", 10 * 3600],
        [23, "d", 23 * 9 * 3600],
        [2, "w", 2 * 45 * 3600],
        [2.5, "m", 2.5 * 4 * 45 * 3600],
        [10, TimeUnit.Hour, 10 * 3600],
        [23, TimeUnit.Day, 23 * 9 * 3600],
        [2, TimeUnit.Week, 2 * 45 * 3600],
        [2.5, TimeUnit.Month, 2.5 * 4 * 45 * 3600],
        # [
        #     3.1,
        #     "y",
        #     3.1 * defaults.yearly_working_days * defaults.daily_working_hours * 3600,
        # ],
    ],
)
def test_schedule_seconds_is_working_as_expected_for_an_effort_based_task_no_studio(
    setup_task_tests, schedule_timing, schedule_unit, schedule_seconds
):
    """schedule_seconds attr is working okay for an effort based task when no studio."""
    data = setup_task_tests
    # no studio, using defaults
    kwargs = copy.copy(data["kwargs"])
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["schedule_timing"] = schedule_timing
    kwargs["schedule_unit"] = schedule_unit
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == schedule_seconds


@pytest.mark.parametrize(
    "schedule_timing, schedule_unit, schedule_seconds",
    [
        [10, "h", 10 * 3600],
        [23, "d", 23 * 8 * 3600],
        [2, "w", 2 * 40 * 3600],
        [2.5, "m", 2.5 * 4 * 40 * 3600],
        [10, TimeUnit.Hour, 10 * 3600],
        [23, TimeUnit.Day, 23 * 8 * 3600],
        [2, TimeUnit.Week, 2 * 40 * 3600],
        [2.5, TimeUnit.Month, 2.5 * 4 * 40 * 3600],
        # [
        #     3.1,
        #     "y",
        #     3.1 * studio.yearly_working_days * studio.daily_working_hours * 3600,
        # ],
    ],
)
def test_schedule_seconds_is_working_as_expected_for_an_effort_based_task_with_studio(
    setup_task_tests, schedule_timing, schedule_unit, schedule_seconds
):
    """schedule_seconds attr is working okay for an effort based task when no studio."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    # no studio, using defaults
    defaults["timing_resolution"] = datetime.timedelta(hours=1)
    _ = Studio(
        name="Test Studio",
        daily_working_hours=8,
        timing_resolution=datetime.timedelta(hours=1),
    )
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["schedule_timing"] = schedule_timing
    kwargs["schedule_unit"] = schedule_unit
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == schedule_seconds


def test_schedule_seconds_is_working_as_expected_for_a_container_task(setup_task_tests):
    """schedule_seconds attr is working as expected for a container task."""
    assert defaults.daily_working_hours == 9
    assert defaults.weekly_working_days == 5
    assert defaults.yearly_working_days == 261
    data = setup_task_tests
    # no studio, using defaults
    kwargs = copy.copy(data["kwargs"])
    parent_task = Task(**kwargs)
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["schedule_timing"] = 10
    kwargs["schedule_unit"] = TimeUnit.Hour
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == 10 * 3600
    new_task.parent = parent_task
    assert parent_task.schedule_seconds == 10 * 3600
    kwargs["schedule_timing"] = 23
    kwargs["schedule_unit"] = TimeUnit.Day
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == 23 * defaults.daily_working_hours * 3600
    new_task.parent = parent_task
    assert (
        parent_task.schedule_seconds
        == 10 * 3600 + 23 * defaults.daily_working_hours * 3600
    )
    kwargs["schedule_timing"] = 2
    kwargs["schedule_unit"] = TimeUnit.Week
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == 2 * defaults.weekly_working_hours * 3600
    new_task.parent = parent_task
    assert (
        parent_task.schedule_seconds
        == 10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 2 * defaults.weekly_working_hours * 3600
    )

    kwargs["schedule_timing"] = 2.5
    kwargs["schedule_unit"] = TimeUnit.Month
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == 2.5 * 4 * defaults.weekly_working_hours * 3600
    new_task.parent = parent_task
    assert (
        parent_task.schedule_seconds
        == 10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 2 * defaults.weekly_working_hours * 3600
        + 2.5 * 4 * defaults.weekly_working_hours * 3600
    )

    kwargs["schedule_timing"] = 3.1
    kwargs["schedule_unit"] = TimeUnit.Year
    new_task = Task(**kwargs)

    assert new_task.schedule_seconds == pytest.approx(
        3.1 * defaults.yearly_working_days * defaults.daily_working_hours * 3600
    )

    new_task.parent = parent_task
    assert parent_task.schedule_seconds == pytest.approx(
        10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 2 * defaults.weekly_working_hours * 3600
        + 2.5 * 4 * defaults.weekly_working_hours * 3600
        + 3.1 * defaults.yearly_working_days * defaults.daily_working_hours * 3600
    )


def test_schedule_seconds_is_working_okay_for_a_container_task_if_the_child_is_updated(
    setup_task_tests,
):
    """schedule_seconds attr is working as expected for a container task."""
    assert defaults.daily_working_hours == 9
    assert defaults.weekly_working_days == 5
    assert defaults.yearly_working_days == 261
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    # no studio, using defaults
    parent_task = Task(**kwargs)
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["schedule_timing"] = 10
    kwargs["schedule_unit"] = TimeUnit.Hour
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == 10 * 3600
    new_task.parent = parent_task
    assert parent_task.schedule_seconds == 10 * 3600
    # update the schedule_timing of the child
    new_task.schedule_timing = 5
    assert new_task.schedule_seconds == 5 * 3600
    new_task.parent = parent_task
    assert parent_task.schedule_seconds == 5 * 3600
    # update it back to 10 hours
    new_task.schedule_timing = 10
    assert new_task.schedule_seconds == 10 * 3600
    new_task.parent = parent_task
    assert parent_task.schedule_seconds == 10 * 3600
    kwargs["schedule_timing"] = 23
    kwargs["schedule_unit"] = TimeUnit.Day
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == 23 * defaults.daily_working_hours * 3600
    new_task.parent = parent_task
    assert (
        parent_task.schedule_seconds
        == 10 * 3600 + 23 * defaults.daily_working_hours * 3600
    )

    kwargs["schedule_timing"] = 2
    kwargs["schedule_unit"] = TimeUnit.Week
    new_task = Task(**kwargs)

    assert new_task.schedule_seconds == 2 * defaults.weekly_working_hours * 3600

    new_task.parent = parent_task
    assert (
        parent_task.schedule_seconds
        == 10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 2 * defaults.weekly_working_hours * 3600
    )

    kwargs["schedule_timing"] = 2.5
    kwargs["schedule_unit"] = TimeUnit.Month
    new_task = Task(**kwargs)

    assert new_task.schedule_seconds == 2.5 * 4 * defaults.weekly_working_hours * 3600

    new_task.parent = parent_task
    assert (
        parent_task.schedule_seconds
        == 10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 2 * defaults.weekly_working_hours * 3600
        + 2.5 * 4 * defaults.weekly_working_hours * 3600
    )

    kwargs["schedule_timing"] = 3.1
    kwargs["schedule_unit"] = TimeUnit.Year
    new_task = Task(**kwargs)

    assert new_task.schedule_seconds == pytest.approx(
        3.1 * defaults.yearly_working_days * defaults.daily_working_hours * 3600
    )

    new_task.parent = parent_task
    assert parent_task.schedule_seconds == pytest.approx(
        10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 2 * defaults.weekly_working_hours * 3600
        + 2.5 * 4 * defaults.weekly_working_hours * 3600
        + 3.1 * defaults.yearly_working_days * defaults.daily_working_hours * 3600
    )


def test_schedule_seconds_is_working_okay_for_a_task_if_the_child_is_updated_deeper(
    setup_task_tests,
):
    """schedule_seconds attr is working as expected for a container task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    defaults["timing_resolution"] = datetime.timedelta(hours=1)
    defaults["daily_working_hours"] = 9
    # no studio, using defaults
    parent_task1 = Task(**kwargs)
    assert parent_task1.schedule_seconds == 9 * 3600
    parent_task2 = Task(**kwargs)
    assert parent_task2.schedule_seconds == 9 * 3600
    parent_task2.schedule_timing = 5
    assert parent_task2.schedule_seconds == 5 * 9 * 3600
    parent_task2.schedule_unit = TimeUnit.Hour
    assert parent_task2.schedule_seconds == 5 * 3600
    parent_task1.parent = parent_task2
    assert parent_task2.schedule_seconds == 9 * 3600
    # create another child task for parent_task2
    child_task = Task(**kwargs)
    child_task.schedule_timing = 10
    child_task.schedule_unit = TimeUnit.Hour
    assert child_task.schedule_seconds == 10 * 3600
    parent_task2.children.append(child_task)
    assert parent_task2.schedule_seconds, 10 * 3600 + 9 * 3600
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["schedule_timing"] = 10
    kwargs["schedule_unit"] = TimeUnit.Hour
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == 10 * 3600
    new_task.parent = parent_task1
    assert parent_task1.schedule_seconds == 10 * 3600
    assert parent_task2.schedule_seconds == 10 * 3600 + 10 * 3600
    # update the schedule_timing of the child
    new_task.schedule_timing = 5
    assert new_task.schedule_seconds == 5 * 3600
    new_task.parent = parent_task1
    assert parent_task1.schedule_seconds == 5 * 3600
    assert parent_task2.schedule_seconds == 5 * 3600 + 10 * 3600
    # update it back to 10 hours
    new_task.schedule_timing = 10
    assert new_task.schedule_seconds == 10 * 3600
    new_task.parent = parent_task1
    assert parent_task1.schedule_seconds == 10 * 3600
    assert parent_task2.schedule_seconds == 10 * 3600 + 10 * 3600
    kwargs["schedule_timing"] = 23
    kwargs["schedule_unit"] = TimeUnit.Day
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == 23 * defaults.daily_working_hours * 3600
    new_task.parent = parent_task1
    assert (
        parent_task1.schedule_seconds
        == 10 * 3600 + 23 * defaults.daily_working_hours * 3600
    )

    assert (
        parent_task2.schedule_seconds
        == 10 * 3600 + 23 * defaults.daily_working_hours * 3600 + 10 * 3600
    )

    kwargs["schedule_timing"] = 2
    kwargs["schedule_unit"] = TimeUnit.Week
    new_task = Task(**kwargs)
    assert new_task.schedule_seconds == 2 * defaults.weekly_working_hours * 3600
    new_task.parent = parent_task1
    assert (
        parent_task1.schedule_seconds
        == 10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 2 * defaults.weekly_working_hours * 3600
    )

    # update it to 1 week
    new_task.schedule_timing = 1
    assert (
        parent_task1.schedule_seconds
        == 10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 1 * defaults.weekly_working_hours * 3600
    )

    assert (
        parent_task2.schedule_seconds
        == 10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 1 * defaults.weekly_working_hours * 3600
        + 10 * 3600
    )

    kwargs["schedule_timing"] = 2.5
    kwargs["schedule_unit"] = TimeUnit.Month
    new_task = Task(**kwargs)

    assert new_task.schedule_seconds == 2.5 * 4 * defaults.weekly_working_hours * 3600

    new_task.parent = parent_task1
    assert (
        parent_task1.schedule_seconds
        == 10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 1 * defaults.weekly_working_hours * 3600
        + 2.5 * 4 * defaults.weekly_working_hours * 3600
    )

    assert (
        parent_task2.schedule_seconds
        == 10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 1 * defaults.weekly_working_hours * 3600
        + 2.5 * 4 * defaults.weekly_working_hours * 3600
        + 10 * 3600
    )

    kwargs["schedule_timing"] = 3.1
    kwargs["schedule_unit"] = TimeUnit.Year
    new_task = Task(**kwargs)

    assert new_task.schedule_seconds == pytest.approx(
        3.1 * defaults.yearly_working_days * defaults.daily_working_hours * 3600
    )

    new_task.parent = parent_task1
    assert parent_task1.schedule_seconds == pytest.approx(
        10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 1 * defaults.weekly_working_hours * 3600
        + 2.5 * 4 * defaults.weekly_working_hours * 3600
        + 3.1 * defaults.yearly_working_days * defaults.daily_working_hours * 3600
    )

    assert parent_task2.schedule_seconds == pytest.approx(
        10 * 3600
        + 23 * defaults.daily_working_hours * 3600
        + 1 * defaults.weekly_working_hours * 3600
        + 2.5 * 4 * defaults.weekly_working_hours * 3600
        + 3.1 * defaults.yearly_working_days * defaults.daily_working_hours * 3600
        + 10 * 3600
    )


def test_remaining_seconds_attr_is_a_read_only_attr(setup_task_tests):
    """remaining hours is a read only attr."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(AttributeError) as cm:
        setattr(new_task, "remaining_seconds", 2342)

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'remaining_seconds'",
    }.get(
        sys.version_info.minor,
        "property 'remaining_seconds' of 'Task' object has no setter",
    )

    assert str(cm.value) == error_message


def test_versions_attr_is_none(setup_task_tests):
    """TypeError raised if the versions attr is set to None."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.versions = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_versions_attr_is_not_a_list(setup_task_tests):
    """TypeError raised if the versions attr is set to a value other than a list."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.versions = 1

    assert str(cm.value) == "Incompatible collection type: int is not list-like"


def test_versions_attr_is_not_a_list_of_version_instances(setup_task_tests):
    """TypeError raised if the versions attr is set to a list of non Version objects."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.versions = [1, 1.2, "a version"]

    assert str(cm.value) == (
        "Task.versions should only have stalker.models.version.Version instances, "
        "and not int: '1'"
    )


def test_equality(setup_task_tests):
    """equality operator."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    entity1 = Entity(**kwargs)
    task0 = Task(**kwargs)
    task1 = Task(**kwargs)
    task2 = Task(**kwargs)
    task3 = Task(**kwargs)
    task4 = Task(**kwargs)
    task5 = Task(**kwargs)
    task6 = Task(**kwargs)

    task1.depends_on = [task2]
    task2.parent = task3
    task3.parent = task4
    task5.children = [task6]
    task6.depends_on = [task2]

    assert not new_task == entity1
    assert new_task == task0
    assert not new_task == task1
    assert not new_task == task5

    assert not task1 == task2
    assert not task1 == task3
    assert not task1 == task4

    assert not task2 == task3
    assert not task2 == task4
    assert not task3 == task4

    assert not task5 == task6

    # check task with same names but different projects


def test_inequality(setup_task_tests):
    """inequality operator."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    _ = Entity(**kwargs)
    _ = Task(**kwargs)

    entity1 = Entity(**kwargs)
    task0 = Task(**kwargs)
    task1 = Task(**kwargs)
    task2 = Task(**kwargs)
    task3 = Task(**kwargs)
    task4 = Task(**kwargs)
    task5 = Task(**kwargs)
    task6 = Task(**kwargs)

    task1.depends_on = [task2]
    task2.parent = task3
    task3.parent = task4
    task5.children = [task6]

    assert new_task != entity1
    assert not new_task != task0
    assert new_task != task1
    assert new_task != task5

    assert task1 != task2
    assert task1 != task3
    assert task1 != task4

    assert task2 != task3
    assert task2 != task4

    assert task3 != task4

    assert task5 != task6


def test_parent_arg_is_skipped_there_is_a_project_arg(setup_task_tests):
    """Task is created okay without a parent if a Project is supplied in project arg."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    try:
        kwargs.pop("parent")
    except KeyError:
        pass

    kwargs["project"] = data["test_project1"]
    new_task = Task(**kwargs)
    assert new_task.project == data["test_project1"]


# parent arg there but project skipped already tested
# both skipped already tested


def test_parent_arg_is_none_but_there_is_a_project_arg(setup_task_tests):
    """task is created okay without a parent if a Project is given in project arg."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = None
    kwargs["project"] = data["test_project1"]
    new_task = Task(**kwargs)
    assert new_task.project == data["test_project1"]


def test_parent_attr_is_set_to_none(setup_task_tests):
    """parent of a task can be set to None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task1 = Task(**kwargs)

    kwargs["parent"] = new_task1
    new_task2 = Task(**kwargs)
    assert new_task2.parent == new_task1
    # DBSession.add_all([new_task1, new_task2])
    # DBSession.commit()

    # store the id to be used later
    # id_ = new_task2.id
    # assert id_ is not None

    new_task2.parent = None
    assert new_task2.parent is None
    # DBSession.commit()

    # we still should have this task
    # t = DBSession.get(Task, id_)
    # assert t is not None
    # assert t.name == kwargs['name']


def test_parent_arg_is_not_a_task_instance(setup_task_tests):
    """TypeError raised if the parent arg is not a Task instance."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = "not a task"
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.parent should be an instance of stalker.models.task.Task, "
        "not str: 'not a task'"
    )


def test_parent_attr_is_not_a_task_instance(setup_task_tests):
    """TypeError raised if the parent attr is not a Task instance."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(TypeError) as cm:
        new_task.parent = "not a task"

    assert str(cm.value) == (
        "Task.parent should be an instance of stalker.models.task.Task, "
        "not str: 'not a task'"
    )

    # there is no way to generate a CycleError by using the parent arg
    # cause the Task is just created, it is not in relationship with other

    # Tasks, there is no parent nor child.


def test_parent_attr_creates_a_cycle(setup_task_tests):
    """CycleError raised if a child is tried to be set as the parent."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task1 = Task(**kwargs)

    kwargs["name"] = "New Task"
    kwargs["parent"] = new_task1
    new_task2 = Task(**kwargs)

    with pytest.raises(CircularDependencyError) as cm:
        new_task1.parent = new_task2

    assert (
        str(cm.value)
        == "<Modeling (Task)> (Task) and <New Task (Task)> (Task) creates "
        'a circular dependency in their "children" attribute'
    )

    # deeper test
    kwargs["parent"] = new_task2
    new_task3 = Task(**kwargs)

    with pytest.raises(CircularDependencyError) as cm:
        new_task1.parent = new_task3

    assert (
        str(cm.value)
        == "<Modeling (Task)> (Task) and <New Task (Task)> (Task) creates "
        'a circular dependency in their "children" attribute'
    )


def test_parent_arg_is_working_as_expected(setup_task_tests):
    """parent arg is working as expected."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task1 = Task(**kwargs)
    kwargs["parent"] = new_task1
    new_task2 = Task(**kwargs)
    assert new_task2.parent == new_task1


def test_parent_attr_is_working_as_expected(setup_task_tests):
    """parent attr is working as expected."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task1 = Task(**kwargs)

    kwargs["parent"] = new_task1
    kwargs["name"] = "New Task"
    new_task = Task(**kwargs)

    kwargs["name"] = "New Task 2"
    new_task2 = Task(**kwargs)

    assert new_task.parent != new_task2

    new_task.parent = new_task2
    assert new_task.parent == new_task2


def test_parent_arg_do_not_allow_a_dependent_task_to_be_parent(setup_task_tests):
    """CircularDependencyError raised if one of the dependencies assigned as parent."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])

    kwargs["depends_on"] = None
    task_a = Task(**kwargs)
    task_b = Task(**kwargs)
    task_c = Task(**kwargs)

    kwargs["depends_on"] = [task_a, task_b, task_c]
    kwargs["parent"] = task_a
    with pytest.raises(CircularDependencyError) as cm:
        Task(**kwargs)

    assert (
        str(cm.value)
        == "<Modeling (Task)> (Task) and <Modeling (Task)> (Task) creates "
        'a circular dependency in their "children" attribute'
    )


def test_parent_attr_do_not_allow_a_dependent_task_to_be_parent(
    setup_task_tests,
):
    """CircularDependencyError raised if one of the dependent tasks is set as parent."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None
    task_a = Task(**kwargs)
    task_b = Task(**kwargs)
    task_c = Task(**kwargs)
    task_d = Task(**kwargs)

    task_d.depends_on = [task_a, task_b, task_c]

    with pytest.raises(CircularDependencyError) as cm:
        task_d.parent = task_a

    assert (
        str(cm.value)
        == "<Modeling (Task)> (Task) and <Modeling (Task)> (Task) creates "
        'a circular dependency in their "depends_on" attribute'
    )


def test_children_attr_is_empty_list_by_default(setup_task_tests):
    """children attr is an empty list by default."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    assert new_task.children == []


def test_children_attr_is_set_to_none(setup_task_tests):
    """TypeError raised if the children attr is set to None."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.children = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_children_attr_accepts_tasks_only(setup_task_tests):
    """TypeError raised if children attr is set to a non list."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.children = "no task"

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_children_attr_is_working_as_expected(setup_task_tests):
    """children attr is working as expected."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["parent"] = new_task
    kwargs["name"] = "Task 1"
    task1 = Task(**kwargs)

    kwargs["name"] = "Task 2"
    task2 = Task(**kwargs)

    kwargs["name"] = "Task 3"
    task3 = Task(**kwargs)

    assert task2 not in task1.children
    assert task3 not in task1.children

    task1.children.append(task2)
    assert task2 in task1.children

    task3.parent = task1
    assert task3 in task1.children


def test_is_leaf_attr_is_read_only(setup_task_tests):
    """is_leaf attr is a read only attr."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    with pytest.raises(AttributeError) as cm:
        new_task.is_leaf = True

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'is_leaf'",
    }.get(sys.version_info.minor, "property 'is_leaf' of 'Task' object has no setter")

    assert str(cm.value) == error_message


def test_is_leaf_attr_is_working_as_expected(setup_task_tests):
    """is_leaf attr is True for a Task without a child Task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["parent"] = new_task
    kwargs["name"] = "Task 1"
    task1 = Task(**kwargs)

    kwargs["name"] = "Task 2"
    task2 = Task(**kwargs)

    kwargs["name"] = "Task 3"
    task3 = Task(**kwargs)

    task2.parent = task1
    task3.parent = task1

    assert task2.is_leaf
    assert task3.is_leaf
    assert not task1.is_leaf


def test_is_root_attr_is_read_only(setup_task_tests):
    """is_root attr is a read only attr."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(AttributeError) as cm:
        new_task.is_root = True

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'is_root'",
    }.get(sys.version_info.minor, "property 'is_root' of 'Task' object has no setter")

    assert str(cm.value) == error_message


def test_is_root_attr_is_working_as_expected(setup_task_tests):
    """is_root attr is True for a Task without a parent Task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["parent"] = new_task
    kwargs["name"] = "Task 1"
    task1 = Task(**kwargs)

    kwargs["name"] = "Task 2"
    task2 = Task(**kwargs)

    kwargs["name"] = "Task 3"
    task3 = Task(**kwargs)

    task2.parent = task1
    task3.parent = task1

    assert not task2.is_root
    assert not task3.is_root
    assert not task1.is_root
    assert new_task.is_root


def test_is_container_attr_is_read_only(setup_task_tests):
    """is_container attr is a read only attr."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(AttributeError) as cm:
        new_task.is_container = False

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'is_container'",
    }.get(
        sys.version_info.minor, "property 'is_container' of 'Task' object has no setter"
    )

    assert str(cm.value) == error_message


def test_is_container_attr_working_as_expected(setup_task_tests):
    """is_container attr is True for a Task with at least one child Task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["parent"] = new_task
    kwargs["name"] = "Task 1"
    task1 = Task(**kwargs)

    kwargs["name"] = "Task 2"
    task2 = Task(**kwargs)

    kwargs["name"] = "Task 3"
    task3 = Task(**kwargs)

    task2.parent = task1
    task3.parent = task1

    assert not task2.is_container
    assert not task3.is_container
    assert task1.is_container


def test_project_and_parent_args_are_skipped(setup_task_tests):
    """TypeError raised if there is no project nor a
    parent task is given with the project and parent args respectively
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("project")

    try:
        kwargs.pop("parent")
    except KeyError:
        pass

    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert (
        str(cm.value) == "Task.project should be an instance of "
        "stalker.models.project.Project, not NoneType: 'None'.\n\nOr please supply "
        "a stalker.models.task.Task with the parent argument, so "
        "Stalker can use the project of the supplied parent task"
    )


def test_project_arg_is_skipped_but_there_is_a_parent_arg(setup_task_tests):
    """Task created okay without a Project if there is a Task given in parent arg."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs.pop("project")
    kwargs["parent"] = new_task

    new_task2 = Task(**kwargs)
    assert new_task2.project == data["test_project1"]


def test_project_arg_is_not_a_project_instance(setup_task_tests):
    """TypeError raised if the given value for the
    project arg is not a stalker.models.project.Project instance
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["name"] = "New Task 1"
    kwargs["project"] = "Not a Project instance"
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.project should be an instance of stalker.models.project.Project, "
        "not str: 'Not a Project instance'"
    )


def test_project_attr_is_a_read_only_attr(setup_task_tests):
    """project attr is a read only attr."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    with pytest.raises(AttributeError) as cm:
        new_task.project = data["test_project1"]

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute",
        11: "property of 'Task' object has no setter",
        12: "property of 'Task' object has no setter",
    }.get(
        sys.version_info.minor,
        "property '_project_getter' of 'Task' object has no setter",
    )

    assert str(cm.value) == error_message


def test_project_arg_is_not_matching_the_given_parent_arg(setup_task_tests):
    """RuntimeWarning raised if project and parent is not matching.

    The project of the given parent is different from the supplied Project with the
    project arg.
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["name"] = "New Task"
    kwargs["parent"] = new_task
    kwargs["project"] = Project(
        name="Some Other Project",
        code="SOP",
        status_list=data["test_project_status_list"],
        repository=data["test_repository"],
    )
    # catching warnings are different from catching exceptions
    # pytest.raises(RuntimeWarning, Task, **data["kwargs"])
    warnings.simplefilter("always")

    with warnings.catch_warnings(record=True) as w:
        Task(**kwargs)
        assert issubclass(w[-1].category, RuntimeWarning)

    assert str(w[0].message) == (
        "The supplied parent and the project is not matching in <New Task (Task)>, "
        "Stalker will use the parent's project (<Test Project1 (Project)>) as the "
        "parent of this Task"
    )


def test_project_arg_is_not_matching_the_given_parent_arg_new_task_uses_parents_project(
    setup_task_tests,
):
    """task uses the parent's project if project is not matching parent's project."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["name"] = "New Task"
    kwargs["parent"] = new_task
    kwargs["project"] = Project(
        name="Some Other Project",
        code="SOP",
        status_list=data["test_project_status_list"],
        repository=data["test_repository"],
    )
    new_task2 = Task(**kwargs)
    assert new_task2.project == new_task.project


def test_start_and_end_attr_values_of_a_container_task_are_defined_by_its_child_tasks(
    setup_task_tests,
):
    """start and end attr values is defined by the
    earliest start and the latest end date values of the children Tasks for
    a container Task
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])

    # remove effort and duration. Why?
    kwargs.pop("schedule_timing")
    kwargs.pop("schedule_unit")
    kwargs["schedule_constraint"] = ScheduleConstraint.Both

    now = datetime.datetime(2013, 3, 22, 15, 0, tzinfo=pytz.utc)
    dt = datetime.timedelta

    # task1
    kwargs["name"] = "Task1"
    kwargs["start"] = now
    kwargs["end"] = now + dt(3)
    task1 = Task(**kwargs)

    # task2
    kwargs["name"] = "Task2"
    kwargs["start"] = now + dt(1)
    kwargs["end"] = now + dt(5)
    task2 = Task(**kwargs)

    # task3
    kwargs["name"] = "Task3"
    kwargs["start"] = now + dt(3)
    kwargs["end"] = now + dt(8)
    task3 = Task(**kwargs)

    # check start conditions
    assert task1.start == now
    assert task1.end == now + dt(3)

    # now parent the task2 and task3 to task1
    task2.parent = task1
    task1.children.append(task3)

    # check if the start is not `now` anymore
    assert task1.start != now
    assert task1.end != now + dt(3)

    # but
    assert task1.start == now + dt(1)
    assert task1.end == now + dt(8)

    kwargs["name"] = "Task4"
    kwargs["start"] = now + dt(15)
    kwargs["end"] = now + dt(16)
    task4 = Task(**kwargs)
    task3.parent = task4
    assert task4.start == task3.start
    assert task4.end == task3.end
    assert task1.start == task2.start
    assert task1.end == task2.end
    # TODO: with SQLAlchemy 0.9 please also check if removing the last
    #       child from a parent will update the parents start and end date
    #       values


def test_end_value_is_calculated_with_the_schedule_timing_and_schedule_unit(
    setup_task_tests,
):
    """end attr is calculated using schedule_timing and schedule_unit for new task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])

    kwargs["start"] = datetime.datetime(2013, 4, 17, 0, 0, tzinfo=pytz.utc)
    kwargs.pop("end")
    kwargs["schedule_timing"] = 10
    kwargs["schedule_unit"] = TimeUnit.Hour

    new_task = Task(**kwargs)
    assert new_task.end == datetime.datetime(2013, 4, 17, 10, 0, tzinfo=pytz.utc)

    kwargs["schedule_timing"] = 5
    kwargs["schedule_unit"] = TimeUnit.Day
    new_task = Task(**kwargs)
    print(new_task.end)
    print(type(new_task.end))
    assert new_task.end == datetime.datetime(2013, 4, 22, 0, 0, tzinfo=pytz.utc)


def test_start_calc_with_schedule_timing_and_schedule_unit_if_schedule_constraint_is_end(
    setup_task_tests,
):
    """start_date is calc.

    from schedule_timing and schedule_unit if schedule_constraint is "end"."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])

    kwargs["start"] = datetime.datetime(2013, 4, 17, 0, 0, tzinfo=pytz.utc)
    kwargs["end"] = datetime.datetime(2013, 4, 18, 0, 0, tzinfo=pytz.utc)
    kwargs["schedule_constraint"] = ScheduleConstraint.End
    kwargs["schedule_timing"] = 10
    kwargs["schedule_unit"] = TimeUnit.Day

    new_task = Task(**kwargs)
    assert new_task.end == datetime.datetime(2013, 4, 18, 0, 0, tzinfo=pytz.utc)
    assert new_task.start == datetime.datetime(2013, 4, 8, 0, 0, tzinfo=pytz.utc)


def test_start_and_end_values_are_not_touched_if_the_schedule_constraint_is_set_to_both(
    setup_task_tests,
):
    """start and end date are not touched if schedule constraint is set to "both"."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    _ = Task(**kwargs)

    kwargs["start"] = datetime.datetime(2013, 4, 17, 0, 0, tzinfo=pytz.utc)
    kwargs["end"] = datetime.datetime(2013, 4, 27, 0, 0, tzinfo=pytz.utc)
    kwargs["schedule_constraint"] = ScheduleConstraint.Both
    kwargs["schedule_timing"] = 100
    kwargs["schedule_unit"] = TimeUnit.Day

    new_task = Task(**kwargs)
    assert new_task.start == datetime.datetime(2013, 4, 17, 0, 0, tzinfo=pytz.utc)
    assert new_task.end == datetime.datetime(2013, 4, 27, 0, 0, tzinfo=pytz.utc)


def test_level_attr_is_a_read_only_property(setup_task_tests):
    """level attr is a read only property."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(AttributeError) as cm:
        new_task.level = 0

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'level'",
    }.get(sys.version_info.minor, "property 'level' of 'Task' object has no setter")

    assert str(cm.value) == error_message


def test_level_attr_returns_the_hierarchical_level_of_this_task(setup_task_tests):
    """level attr returns the hierarchical level of this task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    _ = Task(**kwargs)

    kwargs["name"] = "T1"
    test_task1 = Task(**kwargs)
    assert test_task1.level == 1

    kwargs["name"] = "T2"
    test_task2 = Task(**kwargs)
    test_task2.parent = test_task1
    assert test_task2.level == 2

    kwargs["name"] = "T3"
    test_task3 = Task(**kwargs)
    test_task3.parent = test_task2
    assert test_task3.level == 3


def test__check_circular_dependency_causes_recursion(setup_task_tests):
    """Bug ID: None

    Try to create one parent and three child tasks, second and third child
    are dependent to the first child. This was causing a recursion.
    """
    data = setup_task_tests
    task1 = Task(
        project=data["test_project1"],
        name="Set Day",
        start=datetime.datetime(2013, 4, 1, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 5, 6, tzinfo=pytz.utc),
        status_list=data["task_status_list"],
        responsible=[data["test_user1"]],
    )

    task2 = Task(
        parent=task1,
        name="Supervising Shootings Part1",
        start=datetime.datetime(2013, 4, 1, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 4, 11, tzinfo=pytz.utc),
        status_list=data["task_status_list"],
    )

    task3 = Task(
        parent=task1,
        name="Supervising Shootings Part2",
        depends_on=[task2],
        start=datetime.datetime(2013, 4, 12, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 4, 16, tzinfo=pytz.utc),
        status_list=data["task_status_list"],
    )

    task4 = Task(
        parent=task1,
        name="Supervising Shootings Part3",
        depends_on=[task3],
        start=datetime.datetime(2013, 4, 12, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 4, 17, tzinfo=pytz.utc),
        status_list=data["task_status_list"],
    )

    # move task4 dependency to task2
    task4.depends_on = [task2]


def test_parent_attr_checks_cycle_on_self(setup_task_tests):
    """Bug ID: None

    Check if a CircularDependency Error raised if the parent attr is pointing itself."""
    data = setup_task_tests
    task1 = Task(
        project=data["test_project1"],
        name="Set Day",
        start=datetime.datetime(2013, 4, 1, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 5, 6, tzinfo=pytz.utc),
        status_list=data["task_status_list"],
        responsible=[data["test_user1"]],
    )

    with pytest.raises(CircularDependencyError) as cm:
        task1.parent = task1

    assert (
        str(cm.value) == "<Set Day (Task)> (Task) and <Set Day (Task)> (Task) creates "
        'a circular dependency in their "children" attribute'
    )


def test_bid_timing_arg_is_skipped(setup_task_tests):
    """bid_timing is equal to schedule_timing if bid_timing arg is skipped."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["schedule_timing"] = 155
    kwargs.pop("bid_timing")
    new_task = Task(**kwargs)
    assert new_task.schedule_timing == kwargs["schedule_timing"]
    assert new_task.bid_timing == new_task.schedule_timing


def test_bid_timing_arg_is_none(setup_task_tests):
    """bid_timing attr value is equal to
    schedule_timing attr value if the bid_timing arg is None
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["bid_timing"] = None
    kwargs["schedule_timing"] = 1342
    new_task = Task(**kwargs)
    assert new_task.schedule_timing == kwargs["schedule_timing"]
    assert new_task.bid_timing == new_task.schedule_timing


def test_bid_timing_attr_is_set_to_none(setup_task_tests):
    """bid_timing attr can be set to None."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    new_task.bid_timing = None
    assert new_task.bid_timing is None


def test_bid_timing_arg_is_not_an_int_or_float(setup_task_tests):
    """TypeError raised if the bid_timing arg is not an int or float."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["bid_timing"] = "10d"
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.bid_timing should be an integer or float showing the value of the "
        "initial bid for this Task, not str: '10d'"
    )


def test_bid_timing_attr_is_not_an_int_or_float(setup_task_tests):
    """TypeError raised if the bid_timing attr
    is set to a value which is not an int or float
    """
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.bid_timing = "10d"

    assert str(cm.value) == (
        "Task.bid_timing should be an integer or float showing the value of the "
        "initial bid for this Task, not str: '10d'"
    )


def test_bid_timing_arg_is_working_as_expected(setup_task_tests):
    """bid_timing arg is working as expected."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["bid_timing"] = 23
    new_task = Task(**kwargs)
    assert new_task.bid_timing == kwargs["bid_timing"]


def test_bid_timing_attr_is_working_as_expected(setup_task_tests):
    """bid_timing attr is working as expected."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    test_value = 23
    new_task.bid_timing = test_value
    assert new_task.bid_timing == test_value


def test_bid_unit_arg_is_skipped(setup_task_tests):
    """bid_unit attr value is equal to
    schedule_unit attr value if the bid_unit arg is skipped
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["schedule_unit"] = TimeUnit.Day
    kwargs.pop("bid_unit")
    new_task = Task(**kwargs)
    assert new_task.schedule_unit == kwargs["schedule_unit"]
    assert new_task.bid_unit == new_task.schedule_unit


def test_bid_unit_arg_is_none(setup_task_tests):
    """bid_unit attr value is equal to
    schedule_unit attr value if the bid_unit arg is None
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["bid_unit"] = None
    kwargs["schedule_unit"] = TimeUnit.Minute
    new_task = Task(**kwargs)
    assert new_task.schedule_unit == kwargs["schedule_unit"]
    assert new_task.bid_unit == new_task.schedule_unit


def test_bid_unit_attr_is_set_to_none(setup_task_tests):
    """bid_unit attr can be set to default value of 'h'."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    new_task.bid_unit = None
    assert new_task.bid_unit == TimeUnit.Hour


def test_bid_unit_arg_is_not_a_str(setup_task_tests):
    """TypeError raised if the bid_hour arg is not a str."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["bid_unit"] = 10
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not int: '10'"
    )


def test_bid_unit_attr_is_not_a_str(setup_task_tests):
    """TypeError raised if the bid_unit attr is set to a value which is not an int."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.bid_unit = 10

    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not int: '10'"
    )


def test_bid_unit_arg_is_working_as_expected(setup_task_tests):
    """bid_unit arg is working as expected."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["bid_unit"] = TimeUnit.Hour
    new_task = Task(**kwargs)
    assert new_task.bid_unit == kwargs["bid_unit"]


def test_bid_unit_attr_is_working_as_expected(setup_task_tests):
    """bid_unit attr is working as expected."""
    data = setup_task_tests
    test_value = TimeUnit.Hour
    new_task = Task(**data["kwargs"])
    new_task.bid_unit = test_value
    assert new_task.bid_unit == test_value


def test_bid_unit_arg_value_not_in_defaults_datetime_units(setup_task_tests):
    """ValueError raised if the given unit value is
    not in the stalker.config.Config.datetime_units
    """
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["bid_unit"] = "os"
    with pytest.raises(ValueError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not 'os'"
    )


def test_bid_unit_attr_value_not_in_defaults_datetime_units(setup_task_tests):
    """ValueError raised if the bid_unit value is
    set to a value which is not in stalker.config.Config.datetime_units.
    """
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(ValueError) as cm:
        new_task.bid_unit = "sys"

    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not 'sys'"
    )


def test_tjp_id_is_a_read_only_attr(setup_task_tests):
    """tjp_id attr is a read only attr."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(AttributeError):
        new_task.tjp_id = "some value"


def test_tjp_abs_id_is_a_read_only_attr(setup_task_tests):
    """tjp_abs_id attr is a read only attr."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(AttributeError) as cm:
        new_task.tjp_abs_id = "some_value"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'tjp_abs_id'",
    }.get(
        sys.version_info.minor, "property 'tjp_abs_id' of 'Task' object has no setter"
    )

    assert str(cm.value) == error_message


def test_tjp_id_attr_is_working_as_expected_for_a_root_task(setup_task_tests):
    """tjp_id is working as expected for a root task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = None
    new_task = Task(**kwargs)
    assert new_task.tjp_id == f"Task_{new_task.id}"


def test_tjp_id_attr_is_working_as_expected_for_a_leaf_task(setup_task_tests):
    """tjp_id is working as expected for a leaf task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task1 = Task(**kwargs)
    kwargs["parent"] = new_task1
    kwargs["depends_on"] = None
    new_task2 = Task(**kwargs)
    assert new_task2.tjp_id == f"Task_{new_task2.id}"


def test_tjp_abs_id_attr_is_working_as_expected_for_a_root_task(setup_task_tests):
    """tjp_abs_id is working as expected for a root task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = None
    new_task = Task(**kwargs)
    assert new_task.tjp_abs_id == "Project_{}.Task_{}".format(
        kwargs["project"].id,
        new_task.id,
    )


def test_tjp_abs_id_attr_is_working_as_expected_for_a_leaf_task(setup_task_tests):
    """tjp_abs_id is working as expected for a leaf task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = None

    t1 = Task(**kwargs)
    t2 = Task(**kwargs)
    t3 = Task(**kwargs)

    t2.parent = t1
    t3.parent = t2

    assert t3.tjp_abs_id == "Project_{}.Task_{}.Task_{}.Task_{}".format(
        kwargs["project"].id,
        t1.id,
        t2.id,
        t3.id,
    )


def test_to_tjp_attr_is_working_as_expected_for_a_root_task(setup_task_tests):
    """to_tjp attr is working as expected for a root task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = None
    kwargs["schedule_timing"] = 10
    kwargs["schedule_unit"] = TimeUnit.Day
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["depends_on"] = []
    kwargs["resources"] = [data["test_user1"], data["test_user2"]]

    dep_t1 = Task(**kwargs)
    dep_t2 = Task(**kwargs)

    kwargs["depends_on"] = [dep_t1, dep_t2]
    kwargs["name"] = "Modeling"

    t1 = Task(**kwargs)

    data["test_project1"].id = 120
    t1.id = 121
    dep_t1.id = 122
    dep_t2.id = 123
    data["test_user1"].id = 124
    data["test_user2"].id = 125
    data["test_user3"].id = 126
    data["test_user4"].id = 127
    data["test_user5"].id = 128

    expected_tjp = """task Task_{t1_id} "Task_{t1_id}" {{
    depends Project_{project1_id}.Task_{dep_t1_id} {{onend}}, Project_{project1_id}.Task_{dep_t2_id} {{onend}}
    effort 10d
    allocate User_{user1_id} {{
        alternative
        User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
        persistent
    }}, User_{user2_id} {{
        alternative
        User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
        persistent
    }}
}}""".format(
        project1_id=data["test_project1"].id,
        t1_id=t1.id,
        dep_t1_id=dep_t1.id,
        dep_t2_id=dep_t2.id,
        user1_id=data["test_user1"].id,
        user2_id=data["test_user2"].id,
        user3_id=data["test_user3"].id,
        user4_id=data["test_user4"].id,
        user5_id=data["test_user5"].id,
    )
    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print('---------------------------------')
    # print("Result:")
    # print("-------")
    # print(t1.to_tjp)
    assert t1.to_tjp == expected_tjp


def test_to_tjp_attr_is_working_as_expected_for_a_leaf_task(setup_task_tests):
    """to_tjp attr is working as expected for a leaf task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["parent"] = new_task
    kwargs["depends_on"] = []

    dep_task1 = Task(**kwargs)
    dep_task2 = Task(**kwargs)

    kwargs["name"] = "Modeling"
    kwargs["schedule_timing"] = 1003
    kwargs["schedule_unit"] = TimeUnit.Hour
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["depends_on"] = [dep_task1, dep_task2]

    kwargs["resources"] = [data["test_user1"], data["test_user2"]]

    new_task2 = Task(**kwargs)

    # create some random ids
    data["test_project1"].id = 120
    new_task.id = 121
    new_task2.id = 122
    dep_task1.id = 123
    dep_task2.id = 124
    data["test_user1"].id = 125
    data["test_user2"].id = 126
    data["test_user3"].id = 127
    data["test_user4"].id = 128
    data["test_user5"].id = 129

    # data["maxDiff"] = None
    expected_tjp = """    task Task_{new_task2_id} "Task_{new_task2_id}" {{
        depends Project_{project1_id}.Task_{new_task_id}.Task_{dep_task1_id} {{onend}}, Project_{project1_id}.Task_{new_task_id}.Task_{dep_task2_id} {{onend}}
        effort 1003h
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}""".format(
        project1_id=data["test_project1"].id,
        new_task_id=new_task.id,
        new_task2_id=new_task2.id,
        dep_task1_id=dep_task1.id,
        dep_task2_id=dep_task2.id,
        user1_id=data["test_user1"].id,
        user2_id=data["test_user2"].id,
        user3_id=data["test_user3"].id,
        user4_id=data["test_user4"].id,
        user5_id=data["test_user5"].id,
    )
    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print('---------------------------------')
    # print("Result:")
    # print("-------")
    # print(new_task2.to_tjp)
    assert new_task2.to_tjp == expected_tjp


def test_to_tjp_attr_is_working_as_expected_for_a_leaf_task_with_timelogs(
    setup_task_tests,
):
    """to_tjp attr is working as expected for a leaf task with timelogs."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["parent"] = new_task
    kwargs["depends_on"] = []

    dep_task1 = Task(**kwargs)
    dep_task2 = Task(**kwargs)

    kwargs["name"] = "Modeling"
    kwargs["schedule_timing"] = 1003
    kwargs["schedule_unit"] = TimeUnit.Hour
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["resources"] = [data["test_user1"], data["test_user2"]]

    new_task2 = Task(**kwargs)

    # create some random ids
    data["test_project1"].id = 120
    new_task.id = 121
    new_task2.id = 122
    dep_task1.id = 123
    dep_task2.id = 124
    data["test_user1"].id = 125
    data["test_user2"].id = 126
    data["test_user3"].id = 127
    data["test_user4"].id = 128
    data["test_user5"].id = 129

    # add some timelogs
    start = datetime.datetime(2024, 11, 13, 12, 0, tzinfo=pytz.utc)
    end = start + datetime.timedelta(hours=2)
    new_task2.create_time_log(data["test_user1"], start, end)

    # data["maxDiff"] = None
    expected_tjp = """    task Task_{new_task2_id} "Task_{new_task2_id}" {{
        effort 1003h
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
        booking User_125 2024-11-13-12:00:00 - 2024-11-13-14:00:00 {{ overtime 2 }}
    }}""".format(
        project1_id=data["test_project1"].id,
        new_task_id=new_task.id,
        new_task2_id=new_task2.id,
        dep_task1_id=dep_task1.id,
        dep_task2_id=dep_task2.id,
        user1_id=data["test_user1"].id,
        user2_id=data["test_user2"].id,
        user3_id=data["test_user3"].id,
        user4_id=data["test_user4"].id,
        user5_id=data["test_user5"].id,
    )
    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print('---------------------------------')
    # print("Result:")
    # print("-------")
    # print(new_task2.to_tjp)
    assert new_task2.to_tjp == expected_tjp


def test_to_tjp_attr_is_working_as_expected_for_a_leaf_task_with_dependency_details(
    setup_task_tests,
):
    """to_tjp attr is working as expected for a leaf task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    kwargs["parent"] = new_task
    kwargs["depends_on"] = []

    dep_task1 = Task(**kwargs)
    dep_task2 = Task(**kwargs)
    kwargs["name"] = "Modeling"
    kwargs["schedule_timing"] = 1003
    kwargs["schedule_unit"] = TimeUnit.Hour
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["depends_on"] = [dep_task1, dep_task2]
    kwargs["resources"] = [data["test_user1"], data["test_user2"]]

    new_task2 = Task(**kwargs)

    # modify dependency attributes
    tdep1 = new_task2.task_depends_on[0]
    tdep1.dependency_target = DependencyTarget.OnStart
    tdep1.gap_timing = 2
    tdep1.gap_unit = TimeUnit.Day
    tdep1.gap_model = ScheduleModel.Length

    tdep2 = new_task2.task_depends_on[1]
    tdep1.dependency_target = DependencyTarget.OnStart
    tdep2.gap_timing = 4
    tdep2.gap_unit = TimeUnit.Day
    tdep2.gap_model = ScheduleModel.Duration

    # create some random ids
    data["test_project1"].id = 120
    new_task.id = 121
    new_task2.id = 122
    dep_task1.id = 123
    dep_task2.id = 124
    data["test_user1"].id = 125
    data["test_user2"].id = 126
    data["test_user3"].id = 127
    data["test_user4"].id = 128
    data["test_user5"].id = 129

    expected_tjp = """    task Task_{new_task2_id} "Task_{new_task2_id}" {{
        depends Project_{project1_id}.Task_{new_task_id}.Task_{dep_task1_id} {{onstart gaplength 2d}}, Project_{project1_id}.Task_{new_task_id}.Task_{dep_task2_id} {{onend gapduration 4d}}
        effort 1003h
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}""".format(
        project1_id=data["test_project1"].id,
        new_task_id=new_task.id,
        new_task2_id=new_task2.id,
        dep_task1_id=dep_task1.id,
        dep_task2_id=dep_task2.id,
        user1_id=data["test_user1"].id,
        user2_id=data["test_user2"].id,
        user3_id=data["test_user3"].id,
        user4_id=data["test_user4"].id,
        user5_id=data["test_user5"].id,
    )
    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print('---------------------------------')
    # print("Result:")
    # print("-------")
    # print(new_task2.to_tjp)
    assert new_task2.to_tjp == expected_tjp


def test_to_tjp_attr_is_working_okay_for_a_leaf_task_with_custom_allocation_strategy(
    setup_task_tests,
):
    """to_tjp attr is working okay for a leaf task with custom allocation_strategy."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task1 = Task(**kwargs)

    kwargs["parent"] = new_task1
    kwargs["depends_on"] = []

    dep_task1 = Task(**kwargs)
    dep_task2 = Task(**kwargs)

    kwargs["name"] = "Modeling"
    kwargs["schedule_timing"] = 1003
    kwargs["schedule_unit"] = TimeUnit.Hour
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["depends_on"] = [dep_task1, dep_task2]
    kwargs["resources"] = [data["test_user1"], data["test_user2"]]
    kwargs["alternative_resources"] = [data["test_user3"]]
    kwargs["allocation_strategy"] = "minloaded"

    new_task2 = Task(**kwargs)

    # modify dependency attributes
    tdep1 = new_task2.task_depends_on[0]
    tdep1.dependency_target = DependencyTarget.OnStart
    tdep1.gap_timing = 2
    tdep1.gap_unit = TimeUnit.Day
    tdep1.gap_model = ScheduleModel.Length

    tdep2 = new_task2.task_depends_on[1]
    tdep1.dependency_target = DependencyTarget.OnStart
    tdep2.gap_timing = 4
    tdep2.gap_unit = TimeUnit.Day
    tdep2.gap_model = ScheduleModel.Duration

    # create some random id
    data["test_project1"].id = 120
    new_task1.id = 121
    new_task2.id = 122
    dep_task1.id = 123
    dep_task2.id = 124
    data["test_user1"].id = 125
    data["test_user2"].id = 126
    data["test_user3"].id = 127
    data["test_user4"].id = 128
    data["test_user5"].id = 129

    expected_tjp = """    task Task_{new_task2_id} "Task_{new_task2_id}" {{
        depends Project_{project1_id}.Task_{new_task1_id}.Task_{dep_task1_id} {{onstart gaplength 2d}}, Project_{project1_id}.Task_{new_task1_id}.Task_{dep_task2_id} {{onend gapduration 4d}}
        effort 1003h
        allocate User_{user1_id} {{
            alternative
            User_{user3_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id} select minloaded
            persistent
        }}
    }}""".format(
        project1_id=data["test_project1"].id,
        new_task1_id=new_task1.id,
        new_task2_id=new_task2.id,
        dep_task1_id=dep_task1.id,
        dep_task2_id=dep_task2.id,
        user1_id=data["test_user1"].id,
        user2_id=data["test_user2"].id,
        user3_id=data["test_user3"].id,
        user4_id=data["test_user4"].id,
        user5_id=data["test_user5"].id,
    )
    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print('---------------------------------')
    # print("Result:")
    # print("-------")
    # print(new_task2.to_tjp)
    assert new_task2.to_tjp == expected_tjp


def test_to_tjp_attr_is_working_as_expected_for_a_container_task(setup_task_tests):
    """to_tjp attr is working as expected for a container task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = None
    kwargs["depends_on"] = []

    t1 = Task(**kwargs)
    kwargs["parent"] = t1

    dep_task1 = Task(**kwargs)
    dep_task2 = Task(**kwargs)

    kwargs["name"] = "Modeling"
    kwargs["schedule_timing"] = 1
    kwargs["schedule_unit"] = TimeUnit.Day
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["depends_on"] = [dep_task1, dep_task2]

    kwargs["resources"] = [data["test_user1"], data["test_user2"]]

    t2 = Task(**kwargs)
    # set some random ids
    data["test_user1"].id = 123
    data["test_user2"].id = 124
    data["test_user3"].id = 125
    data["test_user4"].id = 126
    data["test_user5"].id = 127

    data["test_project1"].id = 128

    t1.id = 129
    t2.id = 130
    dep_task1.id = 131
    dep_task2.id = 132

    expected_tjp = """task Task_{t1_id} "Task_{t1_id}" {{
    task Task_{dep_task1_id} "Task_{dep_task1_id}" {{
        effort 1d
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}
    task Task_{dep_task2_id} "Task_{dep_task2_id}" {{
        effort 1d
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}
    task Task_{t2_id} "Task_{t2_id}" {{
        depends Project_{project1_id}.Task_{t1_id}.Task_{dep_task1_id} {{onend}}, Project_{project1_id}.Task_{t1_id}.Task_{dep_task2_id} {{onend}}
        effort 1d
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}
}}""".format(
        user1_id=data["test_user1"].id,
        user2_id=data["test_user2"].id,
        user3_id=data["test_user3"].id,
        user4_id=data["test_user4"].id,
        user5_id=data["test_user5"].id,
        project1_id=data["test_project1"].id,
        t1_id=t1.id,
        t2_id=t2.id,
        dep_task1_id=dep_task1.id,
        dep_task2_id=dep_task2.id,
    )
    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print('---------------------------------')
    # print("Result:")
    # print("-------")
    # print(t1.to_tjp)
    assert t1.to_tjp == expected_tjp


def test_to_tjp_attr_is_working_as_expected_for_a_container_task_with_dependency(
    setup_task_tests,
):
    """to_tjp attr is working as expected for a container task which has dependency."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])

    # kwargs['project'].id = 87987
    kwargs["parent"] = None
    kwargs["depends_on"] = []
    kwargs["name"] = "Random Task Name 1"

    t0 = Task(**kwargs)

    kwargs["depends_on"] = [t0]
    kwargs["name"] = "Modeling"

    t1 = Task(**kwargs)
    t1.priority = 888

    kwargs["parent"] = t1
    kwargs["depends_on"] = []

    dep_task1 = Task(**kwargs)
    dep_task1.depends_on = []

    dep_task2 = Task(**kwargs)
    dep_task1.depends_on = []

    kwargs["name"] = "Modeling"
    kwargs["schedule_timing"] = 1
    kwargs["schedule_unit"] = TimeUnit.Day
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["depends_on"] = [dep_task1, dep_task2]

    data["test_user1"].name = "Test User 1"
    data["test_user1"].login = "test_user1"
    # data["test_user1"].id = 1231

    data["test_user2"].name = "Test User 2"
    data["test_user2"].login = "test_user2"
    # data["test_user2"].id = 1232

    kwargs["resources"] = [data["test_user1"], data["test_user2"]]

    t2 = Task(**kwargs)

    # generate random ids
    data["test_user1"].id = 123
    data["test_user2"].id = 124
    data["test_user3"].id = 125
    data["test_user4"].id = 126
    data["test_user5"].id = 127

    data["test_project1"].id = 128

    t0.id = 129
    t1.id = 130
    t2.id = 131
    dep_task1.id = 132
    dep_task2.id = 133

    expected_tjp = """task Task_{t1_id} "Task_{t1_id}" {{
    priority 888
    depends Project_{project1_id}.Task_{t0_id} {{onend}}
    task Task_{dep_task1_id} "Task_{dep_task1_id}" {{
        effort 1d
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}
    task Task_{dep_task2_id} "Task_{dep_task2_id}" {{
        effort 1d
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}
    task Task_{t2_id} "Task_{t2_id}" {{
        depends Project_{project1_id}.Task_{t1_id}.Task_{dep_task1_id} {{onend}}, Project_{project1_id}.Task_{t1_id}.Task_{dep_task2_id} {{onend}}
        effort 1d
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}
}}""".format(
        user1_id=data["test_user1"].id,
        user2_id=data["test_user2"].id,
        user3_id=data["test_user3"].id,
        user4_id=data["test_user4"].id,
        user5_id=data["test_user5"].id,
        project1_id=data["test_project1"].id,
        t0_id=t0.id,
        t1_id=t1.id,
        t2_id=t2.id,
        dep_task1_id=dep_task1.id,
        dep_task2_id=dep_task2.id,
    )
    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print('---------------------------------')
    # print("Result:")
    # print("-------")
    # print(t1.to_tjp)
    assert t1.to_tjp == expected_tjp


def test_to_tjp_schedule_constraint_is_reflected_in_tjp_file(setup_task_tests):
    """schedule_constraint is reflected in the tjp file."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])

    # kwargs['project'].id = 87987
    kwargs["parent"] = None
    kwargs["depends_on"] = []

    t1 = Task(**kwargs)
    kwargs["parent"] = t1
    dep_task1 = Task(**kwargs)
    dep_task2 = Task(**kwargs)

    kwargs["name"] = "Modeling"
    kwargs["schedule_timing"] = 1
    kwargs["schedule_unit"] = TimeUnit.Day
    kwargs["schedule_model"] = ScheduleModel.Effort
    kwargs["depends_on"] = [dep_task1, dep_task2]
    kwargs["schedule_constraint"] = 3
    kwargs["start"] = datetime.datetime(2013, 5, 3, 14, 0, tzinfo=pytz.utc)
    kwargs["end"] = datetime.datetime(2013, 5, 4, 14, 0, tzinfo=pytz.utc)

    data["test_user1"].name = "Test User 1"
    data["test_user1"].login = "test_user1"
    # data["test_user1"].id = 1231

    data["test_user2"].name = "Test User 2"
    data["test_user2"].login = "test_user2"
    # data["test_user2"].id = 1232

    kwargs["resources"] = [data["test_user1"], data["test_user2"]]

    t2 = Task(**kwargs)

    # create some random ids
    data["test_user1"].id = 120
    data["test_user2"].id = 121
    data["test_user3"].id = 122
    data["test_user4"].id = 123
    data["test_user5"].id = 124
    data["test_project1"].id = 125
    t1.id = 126
    t2.id = 127
    dep_task1.id = 128
    dep_task2.id = 129

    expected_tjp = """task Task_{t1_id} "Task_{t1_id}" {{
    task Task_{dep_task1_id} "Task_{dep_task1_id}" {{
        effort 1d
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}
    task Task_{dep_task2_id} "Task_{dep_task2_id}" {{
        effort 1d
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}
    task Task_{t2_id} "Task_{t2_id}" {{
        depends Project_{project1_id}.Task_{t1_id}.Task_{dep_task1_id} {{onend}}, Project_{project1_id}.Task_{t1_id}.Task_{dep_task2_id} {{onend}}
        start 2013-05-03-14:00
        end 2013-05-04-14:00
        effort 1d
        allocate User_{user1_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}, User_{user2_id} {{
            alternative
            User_{user3_id}, User_{user4_id}, User_{user5_id} select minloaded
            persistent
        }}
    }}
}}""".format(
        user1_id=data["test_user1"].id,
        user2_id=data["test_user2"].id,
        user3_id=data["test_user3"].id,
        user4_id=data["test_user4"].id,
        user5_id=data["test_user5"].id,
        project1_id=data["test_project1"].id,
        t1_id=t1.id,
        t2_id=t2.id,
        dep_task1_id=dep_task1.id,
        dep_task2_id=dep_task2.id,
    )
    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print('---------------------------------')
    # print("Result:")
    # print("-------")
    # print(t1.to_tjp)
    data["maxDiff"] = None
    assert t1.to_tjp == expected_tjp


def test_is_scheduled_is_a_read_only_attr(setup_task_tests):
    """is_scheduled is a read-only attr."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(AttributeError) as cm:
        new_task.is_scheduled = True

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'is_scheduled'",
    }.get(
        sys.version_info.minor, "property 'is_scheduled' of 'Task' object has no setter"
    )

    assert str(cm.value) == error_message


def test_is_scheduled_is_true_if_the_computed_start_and_computed_end_is_not_none(
    setup_task_tests,
):
    """is_scheduled attr is True if computed_start and computed_end are both valid."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    new_task.computed_start = datetime.datetime.now(pytz.utc)
    new_task.computed_end = datetime.datetime.now(pytz.utc) + datetime.timedelta(10)
    assert new_task.is_scheduled is True


def test_is_scheduled_is_false_if_one_of_computed_start_and_computed_end_is_none(
    setup_task_tests,
):
    """is_scheduled attr is False if one of computed_start or computed_end is None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    new_task.computed_start = None
    new_task.computed_end = datetime.datetime.now(pytz.utc)
    assert new_task.is_scheduled is False
    new_task.computed_start = datetime.datetime.now(pytz.utc)
    new_task.computed_end = None
    assert new_task.is_scheduled is False


def test_parents_attr_is_read_only(setup_task_tests):
    """parents attr is read only."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    with pytest.raises(AttributeError) as cm:
        new_task.parents = data["test_dependent_task1"]

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'parents'",
    }.get(sys.version_info.minor, "property 'parents' of 'Task' object has no setter")

    assert str(cm.value) == error_message


def test_parents_attr_is_working_as_expected(setup_task_tests):
    """parents attr is working as expected."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = None
    t1 = Task(**kwargs)
    t2 = Task(**kwargs)
    t3 = Task(**kwargs)
    t2.parent = t1
    t3.parent = t2
    assert t3.parents == [t1, t2]


def test_responsible_arg_is_skipped_for_a_root_task(setup_task_tests):
    """responsible list is an empty list if a root task have no responsible set."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("responsible")
    new_task = Task(**kwargs)
    assert new_task.responsible == []


def test_responsible_arg_is_skipped_for_a_non_root_task(setup_task_tests):
    """parent task's responsible is used if the responsible arg is skipped."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["name"] = "Root Task"
    root_task = Task(**kwargs)
    assert root_task.responsible == [data["test_user1"]]

    kwargs.pop("responsible")
    kwargs["parent"] = root_task
    kwargs["name"] = "Child Task"
    new_task = Task(**kwargs)
    assert new_task.responsible == root_task.responsible


def test_responsible_arg_is_none_for_a_root_task(setup_task_tests):
    """RuntimeError raised if the responsible arg is None for a root task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["responsible"] = None
    new_task = Task(**kwargs)
    assert new_task.responsible == []


def test_responsible_arg_is_none_for_a_non_root_task(setup_task_tests):
    """parent tasks responsible is used if responsible arg is None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["name"] = "Root Task"
    root_task = Task(**kwargs)
    assert root_task.responsible == [data["test_user1"]]

    kwargs["responsible"] = None
    kwargs["parent"] = root_task
    kwargs["name"] = "Child Task"
    new_task = Task(**kwargs)
    assert new_task.responsible == root_task.responsible


def test_responsible_arg_not_a_list_instance(setup_task_tests):
    """TypeError raised if the responsible arg is not a List instance."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["responsible"] = "not a list"
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_responsible_attr_not_a_list_instance(setup_task_tests):
    """TypeError raised if the responsible attr is not a List of User instances."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(TypeError) as cm:
        new_task.responsible = "not a list of users"

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_responsible_arg_is_not_a_list_of_user_instance(setup_task_tests):
    """TypeError raised if the responsible arg value is not a List of User instance."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["responsible"] = ["not a user instance"]

    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.responsible should be a list of stalker.models.auth.User instances, "
        "not str: 'not a user instance'"
    )


def test_responsible_attr_is_set_to_something_other_than_a_list_of_user_instance(
    setup_task_tests,
):
    """TypeError raised if the responsible attr is not list of Users."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(TypeError) as cm:
        new_task.responsible = ["not a user instance"]

    assert str(cm.value) == (
        "Task.responsible should be a list of stalker.models.auth.User instances, "
        "not str: 'not a user instance'"
    )


def test_responsible_arg_is_none_or_skipped_responsible_attr_comes_from_parents(
    setup_task_tests,
):
    """responsible arg is None or skipped, responsible attr value comes from parents."""
    data = setup_task_tests
    # create two new tasks
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["responsible"] = None

    kwargs["parent"] = new_task
    new_task1 = Task(**kwargs)

    kwargs["parent"] = new_task1
    new_task2 = Task(**kwargs)

    kwargs["parent"] = new_task2
    new_task3 = Task(**kwargs)

    assert new_task1.responsible == [data["test_user1"]]
    assert new_task2.responsible == [data["test_user1"]]
    assert new_task3.responsible == [data["test_user1"]]

    new_task2.responsible = [data["test_user2"]]
    assert new_task1.responsible == [data["test_user1"]]
    assert new_task2.responsible == [data["test_user2"]]
    assert new_task3.responsible == [data["test_user1"]]


def test_responsible_arg_is_none_or_skipped_responsible_attr_comes_from_the_first_parent_with_responsible(
    setup_task_tests,
):
    """responsible arg is None or skipped, responsible attr value comes from the first parent with responsible."""
    data = setup_task_tests
    # create two new tasks
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["responsible"] = None

    kwargs["parent"] = new_task
    new_task1 = Task(**kwargs)

    kwargs["parent"] = new_task1
    new_task2 = Task(**kwargs)

    kwargs["parent"] = new_task2
    new_task3 = Task(**kwargs)

    new_task2.responsible = [data["test_user2"]]
    assert new_task1.responsible == [data["test_user1"]]
    assert new_task2.responsible == [data["test_user2"]]
    assert new_task3.responsible == [data["test_user2"]]


def test_responsible_attr_is_set_to_none_responsible_attr_comes_from_parents(
    setup_task_tests,
):
    """responsible attr is None or skipped then its value comes from parents."""
    data = setup_task_tests
    # create two new tasks
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["parent"] = new_task
    new_task1 = Task(**kwargs)

    kwargs["parent"] = new_task1
    new_task2 = Task(**kwargs)

    kwargs["parent"] = new_task2
    new_task3 = Task(**kwargs)

    new_task1.responsible = []
    new_task2.responsible = []
    new_task3.responsible = []
    new_task.responsible = [data["test_user2"]]

    assert new_task1.responsible == [data["test_user2"]]
    assert new_task2.responsible == [data["test_user2"]]
    assert new_task3.responsible == [data["test_user2"]]

    new_task2.responsible = [data["test_user1"]]
    assert new_task1.responsible == [data["test_user2"]]
    assert new_task2.responsible == [data["test_user1"]]
    assert new_task3.responsible == [data["test_user2"]]


def test_responsible_attr_is_set_to_none_responsible_attr_comes_from_parents_immutable(
    setup_task_tests,
):
    """responsible attr is None or skipped then its value comes from parents."""
    data = setup_task_tests
    # create two new tasks
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    kwargs["parent"] = new_task
    new_task1 = Task(**kwargs)

    kwargs["parent"] = new_task1
    new_task2 = Task(**kwargs)

    kwargs["parent"] = new_task2
    new_task3 = Task(**kwargs)

    new_task1.responsible = []
    new_task2.responsible = []
    new_task3.responsible = []
    new_task.responsible = [data["test_user2"]]

    # set the attr now and expect the parent and the current tasks
    # responsible are divergent
    new_task1.responsible.append(data["test_user3"])
    assert data["test_user3"] in new_task1.responsible
    assert data["test_user2"] in new_task1.responsible
    assert data["test_user3"] not in new_task.responsible
    assert data["test_user2"] in new_task.responsible


def test_computed_start_also_sets_start(setup_task_tests):
    """computed_start also sets the start value of the task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task1 = Task(**kwargs)
    test_value = datetime.datetime(2013, 8, 2, 13, 0, tzinfo=pytz.utc)
    assert new_task1.start != test_value
    new_task1.computed_start = test_value
    assert new_task1.computed_start == test_value
    assert new_task1.start == test_value


def test_computed_end_also_sets_end(setup_task_tests):
    """computed_end also sets the end value of the task."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    _ = Task(**kwargs)

    new_task1 = Task(**kwargs)
    test_value = datetime.datetime(2013, 8, 2, 13, 0, tzinfo=pytz.utc)
    assert new_task1.end != test_value
    new_task1.computed_end = test_value
    assert new_task1.computed_end == test_value
    assert new_task1.end == test_value


# TODO: please add tests for _total_logged_seconds for leaf tasks


def test_tickets_attr_is_a_read_only_property(setup_task_tests):
    """tickets attr is a read-only property."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(AttributeError) as cm:
        new_task.tickets = "some value"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'tickets'",
    }.get(sys.version_info.minor, "property 'tickets' of 'Task' object has no setter")

    assert str(cm.value) == error_message


def test_open_tickets_attr_is_a_read_only_property(setup_task_tests):
    """open_tickets attr is a read-only property."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(AttributeError) as cm:
        new_task.open_tickets = "some value"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'open_tickets'",
    }.get(
        sys.version_info.minor, "property 'open_tickets' of 'Task' object has no setter"
    )

    assert str(cm.value) == error_message


def test_reviews_attr_is_an_empty_list_by_default(setup_task_tests):
    """reviews attr is an empty list by default."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    assert new_task.reviews == []


def test_reviews_is_not_a_list_of_review_instances(setup_task_tests):
    """reviews attr is not a List[Review] raises TypeError."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    test_value = [1234, "test value"]
    with pytest.raises(TypeError) as cm:
        new_task.reviews = test_value

    assert str(cm.value) == (
        "Task.reviews should be all stalker.models.review.Review "
        "instances, not int: '1234'"
    )


def test_reviews_attr_is_validated_as_expected(setup_task_db_tests):
    """reviews attr is validated as expected."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    from stalker import Review

    assert new_task.reviews == []
    new_review = Review(
        task=new_task,
        reviewer=data["test_user1"],
    )
    assert new_task.reviews == [new_review]


def test_status_is_wfd_for_a_newly_created_task_with_dependencies(setup_task_tests):
    """status for a newly created task is WFD by default if there are dependencies."""
    data = setup_task_tests
    # try to trick it
    kwargs = copy.copy(data["kwargs"])
    kwargs["status"] = data["status_cmpl"]  # this is ignored
    new_task = Task(**kwargs)
    assert new_task.status == data["status_wfd"]


def test_status_is_rts_for_a_newly_created_task_without_dependency(setup_task_tests):
    """status for a newly created task is RTS if there are no dependencies."""
    data = setup_task_tests
    # try to trick it
    kwargs = copy.copy(data["kwargs"])
    kwargs["status"] = data["status_cmpl"]
    kwargs.pop("depends_on")
    new_task = Task(**kwargs)
    assert new_task.status == data["status_rts"]


def test_review_number_attr_is_read_only(setup_task_tests):
    """review_number attr is read-only."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    with pytest.raises(AttributeError) as cm:
        new_task.review_number = 12

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute",
        11: "property of 'Task' object has no setter",
        12: "property of 'Task' object has no setter",
    }.get(
        sys.version_info.minor,
        "property '_review_number_getter' of 'Task' object has no setter",
    )

    assert str(cm.value) == error_message


def test_review_number_attr_initializes_with_0(setup_task_tests):
    """review_number attr initializes to 0."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    assert new_task.review_number == 0


def test_task_dependency_auto_generates_task_dependency_object(setup_task_tests):
    """TaskDependency instance is automatically created if association proxy is used."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    new_task = Task(**kwargs)
    new_task.depends_on.append(data["test_dependent_task1"])
    task_depends = new_task.task_depends_on[0]
    assert task_depends.task == new_task
    assert task_depends.depends_on == data["test_dependent_task1"]


def test_task_depends_on_is_an_empty_list(setup_task_tests):
    """task_depends_on is an empty list."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    new_task.task_depends_on = []


def test_task_depends_on_is_not_a_task_dependency_object(setup_task_tests):
    """task_depends_on is not a TaskDependency object raises TypeError."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    with pytest.raises(TypeError) as cm:
        new_task.task_depends_on.append("not a TaskDependency object.")
    assert str(cm.value) == (
        "All the items in the Task.task_depends_on should be a TaskDependency "
        "instance, not str: 'not a TaskDependency object.'"
    )


def test_alternative_resources_arg_is_skipped(setup_task_tests):
    """alternative_resources attr is an empty list if it is skipped."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("alternative_resources")
    new_task = Task(**kwargs)
    assert new_task.alternative_resources == []


def test_alternative_resources_arg_is_none(setup_task_tests):
    """alternative_resources attr is empty list if alternative_resources arg is None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["alternative_resources"] = None
    new_task = Task(**kwargs)
    assert new_task.alternative_resources == []


def test_alternative_resources_attr_is_set_to_none(setup_task_tests):
    """TypeError raised if the alternative_resources attr is set to None."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.alternative_resources = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_alternative_resources_arg_is_not_a_list(setup_task_tests):
    """TypeError raised if the alternative_resources arg value is not a list."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["alternative_resources"] = data["test_user3"]
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == "Incompatible collection type: User is not list-like"


def test_alternative_resources_attr_is_not_a_list(setup_task_tests):
    """TypeError raised if the alternative_resources attr is not a list."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.alternative_resources = data["test_user3"]

    assert str(cm.value) == "Incompatible collection type: User is not list-like"


def test_alternative_resources_arg_elements_are_not_user_instances(
    setup_task_tests,
):
    """TypeError raised if items in the alternative_resources arg are not all User."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["alternative_resources"] = ["not", 1, "user"]
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.alternative_resources should be a list of stalker.models.auth.User "
        "instances, not str: 'not'"
    )


def test_alternative_resources_attr_elements_are_not_all_user_instances(
    setup_task_tests,
):
    """TypeError raised if the items in the alternative_resources attr not all User."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.alternative_resources = ["not", 1, "user"]

    assert str(cm.value) == (
        "Task.alternative_resources should be a list of stalker.models.auth.User "
        "instances, not str: 'not'"
    )


def test_alternative_resources_arg_is_working_as_expected(setup_task_tests):
    """alternative_resources arg is passed okay to the alternative_resources attr."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    assert sorted(
        [data["test_user3"], data["test_user4"], data["test_user5"]],
        key=lambda x: x.name,
    ) == sorted(new_task.alternative_resources, key=lambda x: x.name)


def test_alternative_resources_attr_is_working_as_expected(setup_task_tests):
    """alternative_resources attr value can be correctly set."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    assert sorted(new_task.alternative_resources, key=lambda x: x.name) == sorted(
        [data["test_user3"], data["test_user4"], data["test_user5"]],
        key=lambda x: x.name,
    )
    alternative_resources = [data["test_user4"], data["test_user5"]]
    new_task.alternative_resources = alternative_resources
    assert sorted(alternative_resources, key=lambda x: x.name) == sorted(
        new_task.alternative_resources, key=lambda x: x.name
    )


def test_allocation_strategy_arg_is_skipped(setup_task_tests):
    """default value is used for allocation_strategy attr if arg is skipped."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("allocation_strategy")
    new_task = Task(**kwargs)
    assert new_task.allocation_strategy == defaults.allocation_strategy[0]


def test_allocation_strategy_arg_is_none(setup_task_tests):
    """default value is used for allocation_strategy attr if arg is None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["allocation_strategy"] = None
    new_task = Task(**kwargs)
    assert new_task.allocation_strategy == defaults.allocation_strategy[0]


def test_allocation_strategy_attr_is_set_to_none(setup_task_tests):
    """default value is used for the allocation_strategy if it is set to None."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    new_task.allocation_strategy = None
    assert new_task.allocation_strategy == defaults.allocation_strategy[0]


def test_allocation_strategy_arg_is_not_a_str(setup_task_tests):
    """TypeError raised if the allocation_strategy arg value is not a str."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["allocation_strategy"] = 234
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.allocation_strategy should be one of ['minallocated', "
        "'maxloaded', 'minloaded', 'order', 'random'], not int: '234'"
    )


def test_allocation_strategy_attr_is_set_to_a_value_other_than_str(
    setup_task_tests,
):
    """TypeError is raised if the allocation_strategy attr is not a str."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.allocation_strategy = 234

    assert (
        str(cm.value) == "Task.allocation_strategy should be one of ['minallocated', "
        "'maxloaded', 'minloaded', 'order', 'random'], not int: '234'"
    )


def test_allocation_strategy_arg_value_is_not_correct(setup_task_tests):
    """ValueError raised if the allocation_strategy arg value is not valid."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["allocation_strategy"] = "not in the list"
    with pytest.raises(ValueError) as cm:
        Task(**kwargs)

    assert (
        str(cm.value) == "Task.allocation_strategy should be one of ['minallocated', "
        "'maxloaded', 'minloaded', 'order', 'random'], not 'not in the list'"
    )


def test_allocation_strategy_attr_value_is_not_correct(setup_task_tests):
    """ValueError raised if the allocation_strategy attr is set to an invalid value."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(ValueError) as cm:
        new_task.allocation_strategy = "not in the list"

    assert (
        str(cm.value) == "Task.allocation_strategy should be one of ['minallocated', "
        "'maxloaded', 'minloaded', 'order', 'random'], not 'not in the list'"
    )


def test_allocation_strategy_arg_is_working_as_expected(setup_task_tests):
    """allocation_strategy arg value is passed to the allocation_strategy attr."""
    data = setup_task_tests
    test_value = defaults.allocation_strategy[1]
    kwargs = copy.copy(data["kwargs"])
    kwargs["allocation_strategy"] = test_value
    new_task = Task(**kwargs)
    assert test_value == new_task.allocation_strategy


def test_allocation_strategy_attr_is_working_as_expected(setup_task_tests):
    """allocation_strategy attr value can be correctly set."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])

    test_value = defaults.allocation_strategy[1]
    assert new_task.allocation_strategy != test_value

    new_task.allocation_strategy = test_value
    assert new_task.allocation_strategy == test_value


def test_computed_resources_attr_value_is_equal_to_the_resources_attr_for_a_new_task(
    setup_task_tests,
):
    """computed_resources attr is equal to the resources attr if a task initialized."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    # DBSession.commit()

    assert new_task.is_scheduled is False
    assert new_task.resources == new_task.computed_resources


def test_computed_resources_attr_updates_with_resources_if_is_scheduled_is_false_append(
    setup_task_tests,
):
    """computed_resources attr updated with the resources if is_scheduled is False."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    assert new_task.is_scheduled is False
    test_value = [data["test_user3"], data["test_user5"]]
    assert new_task.resources != test_value
    assert new_task.computed_resources != test_value
    new_task.resources = test_value
    assert sorted(new_task.computed_resources, key=lambda x: x.name) == sorted(
        test_value, key=lambda x: x.name
    )


def test_computed_resources_attr_updates_with_resources_if_is_scheduled_is_false_remove(
    setup_task_tests,
):
    """computed_resources attr updated with the resources if is_scheduled is False."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    assert new_task.is_scheduled is False
    test_value = [data["test_user3"], data["test_user5"]]
    assert new_task.resources != test_value
    assert new_task.computed_resources != test_value
    new_task.resources = test_value
    assert sorted(new_task.computed_resources, key=lambda x: x.name) == sorted(
        test_value, key=lambda x: x.name
    )


def test_computed_resources_attr_dont_update_with_resources_if_is_scheduled_is_true(
    setup_task_tests,
):
    """computed_resources attr not updated with resources if is_scheduled is True."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    assert new_task.is_scheduled is False
    test_value = [data["test_user3"], data["test_user5"]]
    assert new_task.resources != test_value
    assert new_task.computed_resources != test_value

    # now set computed_start and computed_end to emulate a computation has
    # been done
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    assert new_task.is_scheduled is False
    new_task.computed_start = now
    new_task.computed_end = now + td(hours=1)

    assert new_task.is_scheduled is True

    new_task.resources = test_value
    assert new_task.computed_resources != test_value


def test_computed_resources_is_not_a_user_instance(setup_task_tests):
    """computed_resource is not a User instance raises TypeError."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    with pytest.raises(TypeError) as cm:
        new_task.computed_resources.append("not a user")

    assert str(cm.value) == (
        "Task.computed_resources should be a list of stalker.models.auth.User "
        "instances, not str: 'not a user'"
    )


def test_persistent_allocation_arg_is_skipped(setup_task_tests):
    """persistent_allocation defaults if the persistent_allocation arg is skipped."""
    data = setup_task_tests
    data["kwargs"].pop("persistent_allocation")
    new_task = Task(**data["kwargs"])
    assert new_task.persistent_allocation is True


def test_persistent_allocation_arg_is_none(setup_task_tests):
    """persistent_allocation defaults if the persistent_allocation arg is None."""
    data = setup_task_tests
    data["kwargs"]["persistent_allocation"] = None
    new_task = Task(**data["kwargs"])
    assert new_task.persistent_allocation is True


def test_persistent_allocation_attr_is_set_to_none(setup_task_tests):
    """persistent_allocation defaults if it is set to None."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    new_task.persistent_allocation = None
    assert new_task.persistent_allocation is True


def test_persistent_allocation_arg_is_not_bool(setup_task_tests):
    """persistent_allocation is converted to bool if arg is not a bool value."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])

    test_value = "not a bool"
    kwargs["persistent_allocation"] = test_value
    new_task1 = Task(**kwargs)
    assert bool(test_value) == new_task1.persistent_allocation

    test_value = 0
    kwargs["persistent_allocation"] = test_value
    new_task2 = Task(**kwargs)
    assert bool(test_value) == new_task2.persistent_allocation


def test_persistent_allocation_attr_is_not_bool(setup_task_tests):
    """persistent_allocation attr is converted to a bool if is not set to a bool."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])

    test_value = "not a bool"
    new_task.persistent_allocation = test_value
    assert bool(test_value) == new_task.persistent_allocation

    test_value = 0
    new_task.persistent_allocation = test_value
    assert bool(test_value) == new_task.persistent_allocation


def test_persistent_allocation_arg_is_working_as_expected(setup_task_tests):
    """persistent_allocation arg is passed to the persistent_allocation attr."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["persistent_allocation"] = False
    new_task = Task(**kwargs)
    assert new_task.persistent_allocation is False


def test_persistent_allocation_attr_is_working_as_expected(setup_task_tests):
    """persistent_allocation attr value can be correctly set."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)

    new_task.persistent_allocation = False
    assert new_task.persistent_allocation is False


def test_path_attr_is_read_only(setup_task_tests):
    """path attr is read only."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(AttributeError) as cm:
        new_task.path = "some_path"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'path'",
    }.get(sys.version_info.minor, "property 'path' of 'Task' object has no setter")

    assert str(cm.value) == error_message


def test_path_attr_raises_a_runtime_error_if_no_filename_template_found(
    setup_task_tests,
):
    """path attr raises RuntimeError if no FilenameTemplate w/ matching entity_type."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(RuntimeError) as cm:
        _ = new_task.path

    assert (
        str(cm.value)
        == "There are no suitable FilenameTemplate (target_entity_type == "
        "'Task') defined in the Structure of the related Project "
        "instance, please create a new "
        "stalker.models.template.FilenameTemplate instance with its "
        "'target_entity_type' attribute is set to 'Task' and assign it "
        "to the `templates` attribute of the structure of the project"
    )


def test_path_attr_raises_a_runtime_error_if_no_matching_filename_template_found(
    setup_task_tests,
):
    """path attr raises RuntimeError if no FilenameTemplate w/ matching entity_type."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    ft = FilenameTemplate(
        name="Asset Filename Template",
        target_entity_type="Asset",
        path="{{project.code}}/{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/{%- endfor -%}",
        filename="{{task.nice_name}}"
        '_v{{"%03d"|format(version.version_number)}}{{extension}}',
    )
    structure = Structure(name="Movie Project Structure", templates=[ft])
    data["test_project1"].structure = structure
    with pytest.raises(RuntimeError) as cm:
        _ = new_task.path

    assert (
        str(cm.value)
        == "There are no suitable FilenameTemplate (target_entity_type == "
        "'Task') defined in the Structure of the related Project "
        "instance, please create a new "
        "stalker.models.template.FilenameTemplate instance with its "
        "'target_entity_type' attribute is set to 'Task' and assign it "
        "to the `templates` attribute of the structure of the project"
    )


def test_path_attr_is_the_rendered_vers_of_the_related_filename_template_in_the_project(
    setup_task_tests,
):
    """path attr is the rendered from the FilenameTemplate with matching entity_type."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])

    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Task",
        path="{{project.code}}/{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/{%- endfor -%}",
        filename="{{task.nice_name}}"
        '_v{{"%03d"|format(version.version_number)}}{{extension}}',
    )

    structure = Structure(name="Movie Project Structure", templates=[ft])

    data["test_project1"].structure = structure

    assert new_task.path == "tp1/Modeling"
    data["test_project1"].structure = None


def test_absolute_path_attr_is_read_only(setup_task_tests):
    """absolute_path is read only."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(AttributeError) as cm:
        new_task.absolute_path = "some_path"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'absolute_path'",
    }.get(
        sys.version_info.minor,
        "property 'absolute_path' of 'Task' object has no setter",
    )

    assert str(cm.value) == error_message


def test_absolute_path_attr_raises_a_runtime_error_if_no_filename_template_found(
    setup_task_tests,
):
    """absolute_path attr raises RuntimeError.

    if there are no FilenameTemplate with matching entity_type."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(RuntimeError) as cm:
        _ = new_task.absolute_path

    assert (
        str(cm.value)
        == "There are no suitable FilenameTemplate (target_entity_type == "
        "'Task') defined in the Structure of the related Project "
        "instance, please create a new "
        "stalker.models.template.FilenameTemplate instance with its "
        "'target_entity_type' attribute is set to 'Task' and assign it "
        "to the `templates` attribute of the structure of the project"
    )


def test_absolute_path_attr_raises_a_runtime_error_if_no_matching_filename_template(
    setup_task_tests,
):
    """absolute_path attr raises RuntimeError.

    if there is no FilenameTemplate with matching entity_type."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])

    ft = FilenameTemplate(
        name="Asset Filename Template",
        target_entity_type="Asset",
        path="{{project.code}}/{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/{%- endfor -%}",
        filename="{{task.nice_name}}"
        '_v{{"%03d"|format(version.version_number)}}{{extension}}',
    )

    structure = Structure(name="Movie Project Structure", templates=[ft])

    data["test_project1"].structure = structure
    with pytest.raises(RuntimeError) as cm:
        _ = new_task.path

    assert (
        str(cm.value)
        == "There are no suitable FilenameTemplate (target_entity_type == "
        "'Task') defined in the Structure of the related Project "
        "instance, please create a new "
        "stalker.models.template.FilenameTemplate instance with its "
        "'target_entity_type' attribute is set to 'Task' and assign it "
        "to the `templates` attribute of the structure of the project"
    )


def test_absolute_path_attr_is_rendered_version_of_related_filename_template_in_project(
    setup_task_tests,
):
    """absolute_path attr is rendered vers. of FilenameTemplate matching entity_type."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])

    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Task",
        path="{{project.repository.path}}/{{project.code}}/"
        "{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/"
        "{%- endfor -%}",
        filename="{{task.nice_name}}"
        '_v{{"%03d"|format(version.version_number)}}{{extension}}',
    )

    structure = Structure(name="Movie Project Structure", templates=[ft])
    data["test_project1"].structure = structure

    assert (
        os.path.normpath(
            "{}/tp1/Modeling".format(data["test_project1"].repositories[0].path)
        ).replace("\\", "/")
        == new_task.absolute_path
    )


def test_good_arg_is_skipped(setup_task_tests):
    """good attr is None if good arg is skipped."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    try:
        kwargs.pop("good")
    except KeyError:
        pass

    new_task = Task(**kwargs)
    # DBSession.add(new_task)
    # DBSession.commit()
    assert new_task.good is None


def test_good_arg_is_none(setup_task_tests):
    """good attr is None if good arg is None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["good"] = None
    new_task = Task(**kwargs)
    # DBSession.add(new_task)
    # DBSession.commit()
    assert new_task.good is None


def test_good_attr_is_none(setup_task_tests):
    """it is possible to set the good attr to None."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["good"] = Good(name="Some Good")
    new_task = Task(**kwargs)
    # DBSession.add(new_task)
    # DBSession.commit()
    assert new_task.good is not None
    new_task.good = None
    assert new_task.good is None


def test_good_arg_is_not_a_good_instance(setup_task_tests):
    """TypeError raised if the good arg value is not a Good instance."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["good"] = "not a good instance"
    with pytest.raises(TypeError) as cm:
        Task(**kwargs)

    assert str(cm.value) == (
        "Task.good should be a stalker.models.budget.Good instance, "
        "not str: 'not a good instance'"
    )


def test_good_attr_is_not_a_good_instance(setup_task_tests):
    """TypeError raised if the good attr is not set to a Good instance."""
    data = setup_task_tests
    new_task = Task(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_task.good = "not a good instance"

    assert str(cm.value) == (
        "Task.good should be a stalker.models.budget.Good instance, "
        "not str: 'not a good instance'"
    )


def test_good_arg_is_working_as_expected(setup_task_tests):
    """good arg value is passed to the good attr."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    new_good = Good(name="Some Good")
    kwargs["good"] = new_good
    new_task = Task(**kwargs)
    assert new_task.good == new_good


def test_good_attr_is_working_as_expected(setup_task_tests):
    """good attr value can be correctly set."""
    data = setup_task_tests
    new_good = Good(name="Some Good")
    new_task = Task(**data["kwargs"])
    assert new_task.good != new_good
    new_task.good = new_good
    assert new_task.good == new_good


@pytest.mark.parametrize("schedule_unit", ["d", TimeUnit.Day])
def test_reschedule_on_a_container_task(setup_task_tests, schedule_unit):
    """_reschedule on a container task will return immediately."""
    data = setup_task_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = None

    task_a = Task(**kwargs)
    task_b = Task(**kwargs)
    task_c = Task(**kwargs)

    task_b.parent = task_a
    task_a.parent = task_c

    start = task_a.start
    end = task_a.end
    assert task_a._reschedule(10, schedule_unit) is None
    assert task_a.start == start
    assert task_a.end == end


@pytest.fixture(scope="function")
def setup_task_db_tests(setup_postgresql_db):
    """stalker.models.task.Task class with a DB."""
    data = dict()
    data["status_wfd"] = Status.query.filter_by(code="WFD").first()
    data["status_rts"] = Status.query.filter_by(code="RTS").first()
    data["status_wip"] = Status.query.filter_by(code="WIP").first()
    data["status_prev"] = Status.query.filter_by(code="PREV").first()
    data["status_hrev"] = Status.query.filter_by(code="HREV").first()
    data["status_drev"] = Status.query.filter_by(code="DREV").first()
    data["status_oh"] = Status.query.filter_by(code="OH").first()
    data["status_stop"] = Status.query.filter_by(code="STOP").first()
    data["status_cmpl"] = Status.query.filter_by(code="CMPL").first()
    data["task_status_list"] = StatusList.query.filter_by(
        target_entity_type="Task"
    ).first()
    data["test_movie_project_type"] = Type(
        name="Movie Project",
        code="movie",
        target_entity_type="Project",
    )
    data["test_repository_type"] = Type(
        name="Test Repository Type",
        code="test",
        target_entity_type="Repository",
    )
    data["test_repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["test_repository_type"],
        linux_path="/mnt/T/",
        windows_path="T:/",
        macos_path="/Volumes/T/",
    )
    data["test_user1"] = User(
        name="User1",
        login="user1",
        email="user1@user1.com",
        password="1234",
    )
    data["test_user2"] = User(
        name="User2",
        login="user2",
        email="user2@user2.com",
        password="1234",
    )
    data["test_user3"] = User(
        name="User3",
        login="user3",
        email="user3@user3.com",
        password="1234",
    )
    data["test_user4"] = User(
        name="User4",
        login="user4",
        email="user4@user4.com",
        password="1234",
    )
    data["test_user5"] = User(
        name="User5",
        login="user5",
        email="user5@user5.com",
        password="1234",
    )
    data["test_project1"] = Project(
        name="Test Project1",
        code="tp1",
        type=data["test_movie_project_type"],
        repositories=[data["test_repository"]],
    )
    data["test_dependent_task1"] = Task(
        name="Dependent Task1",
        project=data["test_project1"],
        status_list=data["task_status_list"],
        responsible=[data["test_user1"]],
    )
    data["test_dependent_task2"] = Task(
        name="Dependent Task2",
        project=data["test_project1"],
        status_list=data["task_status_list"],
        responsible=[data["test_user1"]],
    )
    data["kwargs"] = {
        "name": "Modeling",
        "description": "A Modeling Task",
        "project": data["test_project1"],
        "priority": 500,
        "responsible": [data["test_user1"]],
        "resources": [data["test_user1"], data["test_user2"]],
        "alternative_resources": [
            data["test_user3"],
            data["test_user4"],
            data["test_user5"],
        ],
        "allocation_strategy": "minloaded",
        "persistent_allocation": True,
        "watchers": [data["test_user3"]],
        "bid_timing": 4,
        "bid_unit": TimeUnit.Day,
        "schedule_timing": 1,
        "schedule_unit": TimeUnit.Day,
        "start": datetime.datetime(2013, 4, 8, 13, 0, tzinfo=pytz.utc),
        "end": datetime.datetime(2013, 4, 8, 18, 0, tzinfo=pytz.utc),
        "depends_on": [data["test_dependent_task1"], data["test_dependent_task2"]],
        "time_logs": [],
        "versions": [],
        "is_milestone": False,
        "status": 0,
        "status_list": data["task_status_list"],
    }
    # create a test Task
    DBSession.add_all(
        [
            data["test_movie_project_type"],
            data["test_repository_type"],
            data["test_repository"],
            data["test_user1"],
            data["test_user2"],
            data["test_user3"],
            data["test_user4"],
            data["test_user5"],
            data["test_project1"],
            data["test_dependent_task1"],
            data["test_dependent_task2"],
        ]
    )
    DBSession.commit()
    return data


def test_open_tickets_attr_is_working_as_expected(setup_task_db_tests):
    """open_tickets attr is working as expected."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    DBSession.add(new_task)
    DBSession.commit()

    # create ticket statuses
    stalker.db.setup.init()

    new_ticket1 = Ticket(project=new_task.project, links=[new_task])
    DBSession.add(new_ticket1)
    DBSession.commit()

    new_ticket2 = Ticket(project=new_task.project, links=[new_task])
    DBSession.add(new_ticket2)
    DBSession.commit()

    # close this ticket
    new_ticket2.resolve(None, "fixed")
    DBSession.commit()

    # add some other tickets
    new_ticket3 = Ticket(
        project=new_task.project,
        links=[],
    )
    DBSession.add(new_ticket3)
    DBSession.commit()

    assert new_task.open_tickets == [new_ticket1]


def test_tickets_attr_is_working_as_expected(setup_task_db_tests):
    """tickets attr is working as expected."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    new_task = Task(**kwargs)
    DBSession.add(new_task)
    DBSession.commit()

    # create ticket statuses
    stalker.db.setup.init()

    new_ticket1 = Ticket(project=new_task.project, links=[new_task])
    DBSession.add(new_ticket1)
    DBSession.commit()

    new_ticket2 = Ticket(project=new_task.project, links=[new_task])
    DBSession.add(new_ticket2)
    DBSession.commit()

    # add some other tickets
    new_ticket3 = Ticket(project=new_task.project, links=[])
    DBSession.add(new_ticket3)
    DBSession.commit()

    assert sorted(new_task.tickets, key=lambda x: x.name) == sorted(
        [new_ticket1, new_ticket2], key=lambda x: x.name
    )


def test_percent_complete_attr_is_not_using_any_time_logs_for_a_duration_task(
    setup_task_db_tests,
):
    """percent_complete attr doesn't use any time log info if task is duration based."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    kwargs["schedule_model"] = ScheduleModel.Duration

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    new_task = Task(**kwargs)
    new_task.computed_start = now + td(days=1)
    new_task.computed_end = now + td(days=2)

    _ = TimeLog(
        task=new_task,
        resource=new_task.resources[0],
        start=now + td(days=1),
        end=now + td(days=2),
    )

    assert new_task.percent_complete == 0


def test_percent_complete_attr_is_working_as_expected_for_a_container_task(
    setup_task_db_tests,
):
    """percent complete attr is working as expected for a container task."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []  # remove dependencies just to make it
    # easy to create time logs after stalker
    # v0.2.6.1

    new_task = Task(**kwargs)
    new_task.status = data["status_rts"]
    DBSession.add(new_task)

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    defaults["timing_resolution"] = td(hours=1)
    defaults["daily_working_hours"] = 9

    parent_task = Task(**kwargs)
    DBSession.add(parent_task)

    new_task.time_logs = []
    tlog1 = TimeLog(
        task=new_task,
        resource=new_task.resources[0],
        start=now - td(hours=4),
        end=now - td(hours=2),
    )
    DBSession.add(tlog1)

    assert tlog1 in new_task.time_logs

    tlog2 = TimeLog(
        task=new_task,
        resource=new_task.resources[1],
        start=now - td(hours=4),
        end=now + td(hours=1),
    )
    DBSession.add(tlog2)
    DBSession.commit()

    new_task.parent = parent_task
    DBSession.commit()

    assert tlog2 in new_task.time_logs
    assert new_task.total_logged_seconds == 7 * 3600
    assert new_task.schedule_seconds == 9 * 3600
    assert new_task.percent_complete == pytest.approx(77.7777778)
    assert parent_task.percent_complete == pytest.approx(77.7777778)


def test_percent_complete_attr_is_working_as_expected_for_a_container_task_with_no_data_1(
    setup_task_db_tests,
):
    """percent complete attr is working as expected for a container task with no data."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []  # remove dependencies just to make it
    # easy to create time logs after stalker
    # v0.2.6.1

    new_task = Task(**kwargs)
    new_task.status = data["status_rts"]
    DBSession.add(new_task)

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    defaults["timing_resolution"] = td(hours=1)
    defaults["daily_working_hours"] = 9

    parent_task = Task(**kwargs)
    DBSession.add(parent_task)

    new_task.time_logs = []
    tlog1 = TimeLog(
        task=new_task,
        resource=new_task.resources[0],
        start=now - td(hours=4),
        end=now - td(hours=2),
    )
    DBSession.add(tlog1)
    assert tlog1 in new_task.time_logs

    tlog2 = TimeLog(
        task=new_task,
        resource=new_task.resources[1],
        start=now - td(hours=4),
        end=now + td(hours=1),
    )
    DBSession.add(tlog2)
    DBSession.commit()

    new_task.parent = parent_task
    DBSession.commit()

    assert tlog2 in new_task.time_logs
    assert new_task.total_logged_seconds == 7 * 3600
    assert new_task.schedule_seconds == 9 * 3600
    assert new_task.percent_complete == pytest.approx(77.7777778)

    parent_task._total_logged_seconds = None
    # parent_task._schedule_seconds = None
    assert parent_task.percent_complete == pytest.approx(77.7777778)


def test_percent_complete_attr_is_working_as_expected_for_a_container_task_with_no_data_2(
    setup_task_db_tests,
):
    """percent complete attr is working as expected for a container task with no data."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []  # remove dependencies just to make it
    # easy to create time logs after stalker
    # v0.2.6.1

    new_task = Task(**kwargs)
    new_task.status = data["status_rts"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    defaults["timing_resolution"] = td(hours=1)
    defaults["daily_working_hours"] = 9

    parent_task = Task(**kwargs)

    new_task.time_logs = []
    tlog1 = TimeLog(
        task=new_task,
        resource=new_task.resources[0],
        start=now - td(hours=4),
        end=now - td(hours=2),
    )
    DBSession.add(tlog1)

    assert tlog1 in new_task.time_logs

    tlog2 = TimeLog(
        task=new_task,
        resource=new_task.resources[1],
        start=now - td(hours=4),
        end=now + td(hours=1),
    )
    DBSession.add(tlog2)
    DBSession.commit()

    new_task.parent = parent_task
    DBSession.commit()

    assert tlog2 in new_task.time_logs
    assert new_task.total_logged_seconds == 7 * 3600
    assert new_task.schedule_seconds == 9 * 3600
    assert new_task.percent_complete == pytest.approx(77.7777778)

    # parent_task._total_logged_seconds = None
    parent_task._schedule_seconds = None
    assert parent_task.percent_complete == pytest.approx(77.7777778)


def test_percent_complete_attr_working_okay_for_a_task_w_effort_and_duration_children(
    setup_task_db_tests,
):
    """percent complete attr is okay with effort and duration based children tasks."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []  # remove dependencies just to make it
    # easy to create time logs after stalker
    # v0.2.6.1
    dt = datetime.datetime
    td = datetime.timedelta

    defaults["timing_resolution"] = td(hours=1)
    defaults["daily_working_hours"] = 9

    now = DateRangeMixin.round_time(dt.now(pytz.utc))

    new_task1 = Task(**kwargs)
    new_task1.status = data["status_rts"]
    DBSession.add(new_task1)

    parent_task = Task(**kwargs)
    DBSession.add(parent_task)

    new_task1.time_logs = []
    tlog1 = TimeLog(
        task=new_task1,
        resource=new_task1.resources[0],
        start=now - td(hours=4),
        end=now - td(hours=2),
    )
    DBSession.add(tlog1)
    assert tlog1 in new_task1.time_logs

    tlog2 = TimeLog(
        task=new_task1,
        resource=new_task1.resources[1],
        start=now - td(hours=6),
        end=now - td(hours=1),
    )
    DBSession.add(tlog2)
    DBSession.commit()

    # create a duration based task
    new_task2 = Task(**kwargs)
    new_task2.status = data["status_rts"]
    new_task2.schedule_model = ScheduleModel.Duration
    new_task2.start = now - td(days=1, hours=1)
    new_task2.end = now - td(hours=1)
    DBSession.add(new_task2)
    DBSession.commit()

    new_task1.parent = parent_task
    DBSession.commit()

    new_task2.parent = parent_task
    DBSession.commit()

    assert tlog2 in new_task1.time_logs
    assert new_task1.total_logged_seconds == 7 * 3600
    assert new_task1.schedule_seconds == 9 * 3600
    assert new_task1.percent_complete == pytest.approx(77.7777778)
    assert (
        new_task2.total_logged_seconds == 24 * 3600
    )  # 1 day for a duration task is 24 hours
    assert (
        new_task2.schedule_seconds == 24 * 3600
    )  # 1 day for a duration task is 24 hours
    assert new_task2.percent_complete == 100

    # as if there are 9 * 3600 seconds of time logs entered to new_task2
    assert parent_task.percent_complete == pytest.approx(93.939393939)


def test_percent_complete_attr_is_okay_for_a_task_with_effort_and_length_based_children(
    setup_task_db_tests,
):
    """percent complete attr is okay with effort and length based children tasks."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []  # remove dependencies just to make it
    # easy to create time logs after stalker
    # v0.2.6.1
    dt = datetime.datetime
    td = datetime.timedelta

    defaults["timing_resolution"] = td(hours=1)
    defaults["daily_working_hours"] = 9

    now = DateRangeMixin.round_time(dt.now(pytz.utc))

    new_task1 = Task(**kwargs)
    new_task1.status = data["status_rts"]
    DBSession.add(new_task1)

    parent_task = Task(**kwargs)
    DBSession.add(parent_task)

    new_task1.time_logs = []
    tlog1 = TimeLog(
        task=new_task1,
        resource=new_task1.resources[0],
        start=now - td(hours=4),
        end=now - td(hours=2),
    )
    DBSession.add(tlog1)

    assert tlog1 in new_task1.time_logs

    tlog2 = TimeLog(
        task=new_task1,
        resource=new_task1.resources[1],
        start=now - td(hours=6),
        end=now - td(hours=1),
    )
    DBSession.add(tlog2)
    DBSession.commit()

    # create a length based task
    new_task2 = Task(**kwargs)
    new_task2.status = data["status_rts"]
    new_task2.schedule_model = ScheduleModel.Length
    new_task2.start = now - td(hours=10)
    new_task2.end = now - td(hours=1)
    DBSession.add(new_task2)
    DBSession.commit()

    new_task1.parent = parent_task
    DBSession.commit()

    new_task2.parent = parent_task
    DBSession.commit()

    assert tlog2 in new_task1.time_logs
    assert new_task1.total_logged_seconds == 7 * 3600
    assert new_task1.schedule_seconds == 9 * 3600
    assert new_task1.percent_complete == pytest.approx(77.7777778)
    assert (
        new_task2.total_logged_seconds == 9 * 3600
    )  # 1 day for a length task is 9 hours
    assert new_task2.schedule_seconds == 9 * 3600  # 1 day for a length task is 9 hours
    assert new_task2.percent_complete == 100

    # as if there are 9 * 3600 seconds of time logs entered to new_task2
    assert parent_task.percent_complete == pytest.approx(88.8888889)


def test_percent_complete_attr_is_working_as_expected_for_a_leaf_task(
    setup_task_db_tests,
):
    """percent_complete attr is working as expected for a leaf task."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []

    new_task = Task(**kwargs)

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    new_task.time_logs = []
    tlog1 = TimeLog(
        task=new_task, resource=new_task.resources[0], start=now, end=now + td(hours=8)
    )
    DBSession.add(tlog1)
    DBSession.commit()

    assert tlog1 in new_task.time_logs

    tlog2 = TimeLog(
        task=new_task, resource=new_task.resources[1], start=now, end=now + td(hours=12)
    )
    DBSession.add(tlog2)
    DBSession.commit()

    assert tlog2 in new_task.time_logs
    assert new_task.total_logged_seconds == 20 * 3600
    assert new_task.percent_complete == 20.0 / 9.0 * 100.0


def test_time_logs_attr_is_working_as_expected(setup_task_db_tests):
    """time_log attr is working as expected."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    new_task1 = Task(**kwargs)

    assert new_task1.depends_on == []

    now = datetime.datetime.now(pytz.utc)
    dt = datetime.timedelta

    new_time_log1 = TimeLog(
        task=new_task1,
        resource=new_task1.resources[0],
        start=now + dt(100),
        end=now + dt(101),
    )

    new_time_log2 = TimeLog(
        task=new_task1,
        resource=new_task1.resources[0],
        start=now + dt(101),
        end=now + dt(102),
    )

    # create a new task
    kwargs["name"] = "New Task"
    new_task2 = Task(**kwargs)

    # create a new TimeLog for that task
    new_time_log3 = TimeLog(
        task=new_task2,
        resource=new_task2.resources[0],
        start=now + dt(102),
        end=now + dt(103),
    )
    # logger.debug('DBSession.get(Task, 37): {}'.format(DBSession.get(Task, 37)))

    assert new_task2.depends_on == []

    # check if everything is in place
    assert new_time_log1 in new_task1.time_logs
    assert new_time_log2 in new_task1.time_logs
    assert new_time_log3 in new_task2.time_logs

    # now move the time_log to test_task1
    new_task1.time_logs.append(new_time_log3)

    # check if new_time_log3 is in test_task1
    assert new_time_log3 in new_task1.time_logs

    # there needs to be a database session commit to remove the time_log
    # from the previous tasks time_logs attr

    assert new_time_log3 in new_task1.time_logs
    assert new_time_log3 not in new_task2.time_logs


def test_total_logged_seconds_attr_is_correct_if_the_time_log_of_child_is_changed(
    setup_task_db_tests,
):
    """total_logged_seconds attr is correct if time log updated on children."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    _ = Task(**kwargs)

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    parent_task = Task(**kwargs)
    child_task = Task(**kwargs)
    parent_task.children.append(child_task)

    tlog1 = TimeLog(
        task=child_task,
        resource=child_task.resources[0],
        start=now,
        end=now + td(hours=8),
    )

    assert parent_task.total_logged_seconds == 8 * 60 * 60

    # now update the time log
    tlog1.end = now + td(hours=16)
    assert parent_task.total_logged_seconds == 16 * 60 * 60


def test_total_logged_seconds_is_the_sum_of_all_time_logs(setup_task_db_tests):
    """total_logged_seconds is the sum of all time_logs in hours."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    new_task = Task(**kwargs)
    new_task.depends_on = []
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    new_task.time_logs = []
    tlog1 = TimeLog(
        task=new_task, resource=new_task.resources[0], start=now, end=now + td(hours=8)
    )
    DBSession.add(tlog1)
    DBSession.commit()

    assert tlog1 in new_task.time_logs

    tlog2 = TimeLog(
        task=new_task, resource=new_task.resources[1], start=now, end=now + td(hours=12)
    )
    DBSession.add(tlog2)
    DBSession.commit()

    assert tlog2 in new_task.time_logs
    assert new_task.total_logged_seconds == 20 * 3600


def test_total_logged_seconds_calls_update_schedule_info(
    setup_task_db_tests,
):
    """total_logged_seconds is the sum of all time_logs of the child tasks."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    new_task = Task(**kwargs)
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    kwargs.pop("schedule_timing")
    kwargs.pop("schedule_unit")
    parent_task = Task(**kwargs)
    new_task.parent = parent_task
    new_task.time_logs = []
    tlog1 = TimeLog(
        task=new_task, resource=new_task.resources[0], start=now, end=now + td(hours=8)
    )
    DBSession.add(tlog1)
    DBSession.commit()
    assert tlog1 in new_task.time_logs
    tlog2 = TimeLog(
        task=new_task, resource=new_task.resources[1], start=now, end=now + td(hours=12)
    )
    DBSession.add(tlog2)
    DBSession.commit()
    # set the total_logged_seconds to None
    # so the getter calls the update_schedule_info
    parent_task._total_logged_seconds = None
    assert tlog2 in new_task.time_logs
    assert new_task.total_logged_seconds == 20 * 3600
    assert parent_task.total_logged_seconds == 20 * 3600


def test_update_schedule_info_on_a_container_of_containers_task(
    setup_task_db_tests,
):
    """total_logged_seconds is the sum of all time_logs of the child tasks."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    new_task = Task(**kwargs)
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    kwargs.pop("schedule_timing")
    kwargs.pop("schedule_unit")
    parent_task = Task(**kwargs)
    root_task = Task(**kwargs)
    new_task.parent = parent_task
    parent_task.parent = root_task
    new_task.time_logs = []
    tlog1 = TimeLog(
        task=new_task, resource=new_task.resources[0], start=now, end=now + td(hours=8)
    )
    DBSession.add(new_task)
    DBSession.add(parent_task)
    DBSession.add(root_task)
    DBSession.add(tlog1)
    DBSession.commit()
    assert tlog1 in new_task.time_logs
    tlog2 = TimeLog(
        task=new_task, resource=new_task.resources[1], start=now, end=now + td(hours=12)
    )
    DBSession.add(tlog2)
    DBSession.commit()
    # set the total_logged_seconds to None
    # so the getter calls the update_schedule_info
    root_task.update_schedule_info()


def test_update_schedule_info_with_leaf_tasks(
    setup_task_db_tests,
):
    """total_logged_seconds is the sum of all time_logs of the child tasks."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    new_task = Task(**kwargs)
    new_task.update_schedule_info()


def test_total_logged_seconds_is_the_sum_of_all_time_logs_of_children(
    setup_task_db_tests,
):
    """total_logged_seconds is the sum of all time_logs of the child tasks."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []
    new_task = Task(**kwargs)
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    kwargs.pop("schedule_timing")
    kwargs.pop("schedule_unit")
    parent_task = Task(**kwargs)
    new_task.parent = parent_task
    new_task.time_logs = []
    tlog1 = TimeLog(
        task=new_task, resource=new_task.resources[0], start=now, end=now + td(hours=8)
    )
    DBSession.add(tlog1)
    DBSession.commit()
    assert tlog1 in new_task.time_logs
    tlog2 = TimeLog(
        task=new_task, resource=new_task.resources[1], start=now, end=now + td(hours=12)
    )
    DBSession.add(tlog2)
    DBSession.commit()
    assert tlog2 in new_task.time_logs
    assert new_task.total_logged_seconds == 20 * 3600
    assert parent_task.total_logged_seconds == 20 * 3600


def test_total_logged_seconds_is_the_sum_of_all_time_logs_of_children_deeper(
    setup_task_db_tests,
):
    """total_logged_seconds is the sum of all time_logs of the children (deeper)."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []

    new_task = Task(**kwargs)

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    kwargs.pop("schedule_timing")
    kwargs.pop("schedule_unit")

    parent_task1 = Task(**kwargs)
    assert parent_task1.total_logged_seconds == 0

    parent_task2 = Task(**kwargs)
    assert parent_task2.total_logged_seconds == 0

    # create some other child
    child = Task(**kwargs)

    assert child.total_logged_seconds == 0
    # create a TimeLog for that child
    tlog1 = TimeLog(
        task=child,
        resource=child.resources[0],
        start=now - td(hours=50),
        end=now - td(hours=40),
    )
    DBSession.add(tlog1)
    DBSession.commit()

    assert child.total_logged_seconds == 10 * 3600
    parent_task2.children.append(child)
    assert parent_task2.total_logged_seconds == 10 * 3600

    # data["test_task1"].parent = parent_task
    parent_task1.children.append(new_task)
    assert parent_task1.total_logged_seconds == 0

    parent_task1.parent = parent_task2
    assert parent_task2.total_logged_seconds == 10 * 3600

    new_task.time_logs = []
    tlog2 = TimeLog(
        task=new_task, resource=new_task.resources[0], start=now, end=now + td(hours=8)
    )
    DBSession.add(tlog2)
    DBSession.commit()

    assert tlog2 in new_task.time_logs
    assert new_task.total_logged_seconds == 8 * 3600
    assert parent_task1.total_logged_seconds == 8 * 3600
    assert parent_task2.total_logged_seconds == 18 * 3600

    tlog3 = TimeLog(
        task=new_task, resource=new_task.resources[1], start=now, end=now + td(hours=12)
    )
    DBSession.add(tlog3)
    DBSession.commit()

    assert new_task.total_logged_seconds == 20 * 3600
    assert parent_task1.total_logged_seconds == 20 * 3600
    assert parent_task2.total_logged_seconds == 30 * 3600


def test_remaining_seconds_is_working_as_expected(setup_task_db_tests):
    """remaining hours is working as expected."""
    data = setup_task_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["depends_on"] = []

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt(2013, 4, 19, 10, 0, tzinfo=pytz.utc)

    kwargs["schedule_model"] = ScheduleModel.Effort

    # -------------- HOURS --------------
    kwargs["schedule_timing"] = 10
    kwargs["schedule_unit"] = TimeUnit.Hour
    new_task = Task(**kwargs)

    # create a time_log of 2 hours
    _ = TimeLog(
        task=new_task, start=now, duration=td(hours=2), resource=new_task.resources[0]
    )
    # check
    assert (
        new_task.remaining_seconds
        == new_task.schedule_seconds - new_task.total_logged_seconds
    )

    # -------------- DAYS --------------
    kwargs["schedule_timing"] = 23
    kwargs["schedule_unit"] = TimeUnit.Day
    new_task = Task(**kwargs)

    # create a time_log of 5 days
    _ = TimeLog(
        task=new_task,
        start=now + td(hours=2),
        end=now + td(days=5),
        resource=new_task.resources[0],
    )
    # check
    assert (
        new_task.remaining_seconds
        == new_task.schedule_seconds - new_task.total_logged_seconds
    )

    # add another 2 hours
    _ = TimeLog(
        task=new_task,
        start=now + td(days=5),
        duration=td(hours=2),
        resource=new_task.resources[0],
    )
    assert (
        new_task.remaining_seconds
        == new_task.schedule_seconds - new_task.total_logged_seconds
    )

    # ------------------- WEEKS ------------------
    kwargs["schedule_timing"] = 2
    kwargs["schedule_unit"] = TimeUnit.Week
    new_task = Task(**kwargs)

    # create a time_log of 2 hours
    tlog4 = TimeLog(
        task=new_task,
        start=now + td(days=6),
        duration=td(hours=2),
        resource=new_task.resources[0],
    )
    new_task.time_logs.append(tlog4)

    # check
    assert (
        new_task.remaining_seconds
        == new_task.schedule_seconds - new_task.total_logged_seconds
    )

    # create a time_log of 1 week
    tlog5 = TimeLog(
        task=new_task,
        start=now + td(days=7),
        duration=td(weeks=1),
        resource=new_task.resources[0],
    )
    new_task.time_logs.append(tlog5)

    # check
    assert (
        new_task.remaining_seconds
        == new_task.schedule_seconds - new_task.total_logged_seconds
    )

    # ------------------ MONTH -------------------
    kwargs["schedule_timing"] = 2.5
    kwargs["schedule_unit"] = TimeUnit.Month
    new_task = Task(**kwargs)

    # create a time_log of 1 month or 30 days, remaining_seconds can be
    # negative
    tlog6 = TimeLog(
        task=new_task,
        start=now + td(days=15),
        duration=td(days=30),
        resource=new_task.resources[0],
    )
    new_task.time_logs.append(tlog6)

    # check
    assert (
        new_task.remaining_seconds
        == new_task.schedule_seconds - new_task.total_logged_seconds
    )

    # ------------------ YEARS ---------------------
    kwargs["schedule_timing"] = 3.1
    kwargs["schedule_unit"] = TimeUnit.Year
    new_task = Task(**kwargs)

    # create a time_log of 1 month or 30 days, remaining_seconds can be
    # negative
    tlog8 = TimeLog(
        task=new_task,
        start=now + td(days=55),
        duration=td(days=30),
        resource=new_task.resources[0],
    )
    new_task.time_logs.append(tlog8)
    # check
    assert (
        new_task.remaining_seconds
        == new_task.schedule_seconds - new_task.total_logged_seconds
    )


def test_template_variables_for_non_shot_related_task(setup_task_db_tests):
    """_template_variables() for a non shot related task returns correct data."""
    data = setup_task_db_tests
    task = Task(**data["kwargs"])
    assert task._template_variables() == {
        "asset": None,
        "parent_tasks": [task],
        "project": data["test_project1"],
        "scene": None,
        "sequence": None,
        "shot": None,
        "task": task,
        "type": None,
    }
