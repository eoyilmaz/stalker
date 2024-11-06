# -*- coding: utf-8 -*-
"""Tests for the TimeLog class."""

import copy
import datetime

import pytest

import pytz

import tzlocal

from sqlalchemy.exc import IntegrityError

from stalker import Project, Repository, Status, Task, TimeLog, User
from stalker.db.session import DBSession
from stalker.exceptions import DependencyViolationError, OverBookedError, StatusError


@pytest.fixture(scope="function")
def setup_time_log_db_tests(setup_postgresql_db):
    """Set up the tests for the TimeLog class."""
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

    # create a resource
    data["test_resource1"] = User(
        name="User1",
        login="user1",
        email="user1@users.com",
        password="1234",
    )
    DBSession.add(data["test_resource1"])

    data["test_resource2"] = User(
        name="User2", login="user2", email="user2@users.com", password="1234"
    )
    DBSession.add(data["test_resource2"])

    data["test_repo"] = Repository(name="test repository", code="tr")
    DBSession.add(data["test_repo"])

    # create a Project
    data["test_status1"] = Status(name="Status1", code="STS1")
    data["test_status2"] = Status(name="Status2", code="STS2")
    data["test_status3"] = Status(name="Status3", code="STS3")
    DBSession.add_all(
        [data["test_status1"], data["test_status2"], data["test_status3"]]
    )

    data["test_project"] = Project(
        name="test project",
        code="tp",
        repository=data["test_repo"],
    )
    DBSession.add(data["test_project"])

    # create Tasks
    data["test_task1"] = Task(
        name="test task 1",
        project=data["test_project"],
        schedule_timing=10,
        schedule_unit="d",
        resources=[data["test_resource1"]],
    )
    DBSession.add(data["test_task1"])

    data["test_task2"] = Task(
        name="test task 2",
        project=data["test_project"],
        schedule_timing=10,
        schedule_unit="d",
        resources=[data["test_resource1"]],
    )
    DBSession.add(data["test_task2"])

    data["kwargs"] = {
        "task": data["test_task1"],
        "resource": data["test_resource1"],
        "start": datetime.datetime(2013, 3, 22, 1, 0, tzinfo=pytz.utc),
        "duration": datetime.timedelta(10),
    }

    # create a TimeLog
    # and test it
    data["test_time_log"] = TimeLog(**data["kwargs"])
    DBSession.add(data["test_time_log"])
    DBSession.commit()
    return data


def test___auto_name__class_attribute_is_set_to_true():
    """__auto_name__ class attribute is set to True for TimeLog class."""
    assert TimeLog.__auto_name__ is True


def test_task_argument_is_skipped(setup_time_log_db_tests):
    """TypeError raised if the task argument is skipped."""
    data = setup_time_log_db_tests
    td = datetime.timedelta
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("task")
    kwargs["start"] = kwargs["start"] - td(days=100)
    kwargs["duration"] = td(hours=10)
    with pytest.raises(TypeError) as cm:
        TimeLog(**kwargs)

    assert str(cm.value) == (
        "TimeLog.task should be an instance of stalker.models.task.Task, "
        "not NoneType: 'None'"
    )


def test_task_argument_is_none(setup_time_log_db_tests):
    """TypeError raised if the task argument is None."""
    data = setup_time_log_db_tests
    td = datetime.timedelta
    kwargs = copy.copy(data["kwargs"])
    kwargs["task"] = None
    kwargs["start"] = kwargs["start"] - td(days=100)
    kwargs["duration"] = td(hours=10)
    with pytest.raises(TypeError) as cm:
        TimeLog(**kwargs)

    assert str(cm.value) == (
        "TimeLog.task should be an instance of stalker.models.task.Task, "
        "not NoneType: 'None'"
    )


def test_task_attribute_is_none(setup_time_log_db_tests):
    """TypeError raised if the task attribute is None."""
    data = setup_time_log_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_time_log"].task = None

    assert str(cm.value) == (
        "TimeLog.task should be an instance of stalker.models.task.Task, "
        "not NoneType: 'None'"
    )


def test_task_argument_is_not_a_task_instance(setup_time_log_db_tests):
    """TypeError raised if the task arg is not a Task instance."""
    data = setup_time_log_db_tests
    td = datetime.timedelta
    kwargs = copy.copy(data["kwargs"])
    kwargs["task"] = "this is a task"
    kwargs["start"] = kwargs["start"] - td(days=100)
    kwargs["duration"] = td(hours=10)
    with pytest.raises(TypeError) as cm:
        TimeLog(**kwargs)

    assert str(cm.value) == (
        "TimeLog.task should be an instance of stalker.models.task.Task, "
        "not str: 'this is a task'"
    )


def test_task_attribute_is_not_a_task_instance(setup_time_log_db_tests):
    """TypeError raised if the task attribute is not a Task instance."""
    data = setup_time_log_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_time_log"].task = "this is a task"

    assert str(cm.value) == (
        "TimeLog.task should be an instance of stalker.models.task.Task, "
        "not str: 'this is a task'"
    )


def test_task_attribute_is_working_as_expected(setup_time_log_db_tests):
    """task attribute is working as expected."""
    data = setup_time_log_db_tests
    new_task = Task(
        name="Test task 2",
        project=data["test_project"],
        resources=[data["test_resource1"]],
    )
    assert data["test_time_log"].task != new_task
    data["test_time_log"].task = new_task
    assert data["test_time_log"].task == new_task


def test_task_argument_updates_backref(setup_time_log_db_tests):
    """setting Task in TimeLog task arg updates Task.timee_logs attr."""
    data = setup_time_log_db_tests
    new_task = Task(
        name="Test Task 3",
        project=data["test_project"],
        resources=[data["test_resource1"]],
    )

    # now create a new time_log for the new task
    kwargs = copy.copy(data["kwargs"])
    kwargs["task"] = new_task
    kwargs["start"] = kwargs["start"] + kwargs["duration"] + datetime.timedelta(120)
    new_time_log = TimeLog(**kwargs)

    # now check if the new_time_log is in task.time_logs
    assert new_time_log in new_task.time_logs


def test_task_attribute_updates_backref(setup_time_log_db_tests):
    """setting Task in TimeLog.task attr updates Task.timee_logs attr."""
    data = setup_time_log_db_tests
    new_task = Task(
        name="Test Task 3",
        project=data["test_project"],
        resources=[data["test_resource1"]],
    )

    data["test_time_log"].task = new_task
    assert data["test_time_log"] in new_task.time_logs


def test_resource_argument_is_skipped(setup_time_log_db_tests):
    """TypeError raised if the resource argument is skipped."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("resource")
    kwargs["start"] -= datetime.timedelta(days=200)
    kwargs["end"] = kwargs["start"] + datetime.timedelta(days=10)
    with pytest.raises(TypeError) as cm:
        TimeLog(**kwargs)

    assert str(cm.value) == "TimeLog.resource cannot be None"


def test_resource_argument_is_none(setup_time_log_db_tests):
    """TypeError raised if the resource argument is None."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = None
    with pytest.raises(TypeError) as cm:
        TimeLog(**kwargs)

    assert str(cm.value) == "TimeLog.resource cannot be None"


def test_resource_attribute_is_none(setup_time_log_db_tests):
    """TypeError raised if the resource attribute is set to None."""
    data = setup_time_log_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_time_log"].resource = None

    assert str(cm.value) == "TimeLog.resource cannot be None"


def test_resource_argument_is_not_a_user_instance(setup_time_log_db_tests):
    """TypeError raised if the resource arg is not a User instance."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = "This is a resource"
    with pytest.raises(TypeError) as cm:
        TimeLog(**kwargs)

    assert str(cm.value) == (
        "TimeLog.resource should be a stalker.models.auth.User instance, "
        "not str: 'This is a resource'"
    )


def test_resource_attribute_is_not_a_user_instance(setup_time_log_db_tests):
    """TypeError raised if the resource attr is not a User instance."""
    data = setup_time_log_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_time_log"].resource = "this is a resource"

    assert str(cm.value) == (
        "TimeLog.resource should be a stalker.models.auth.User instance, "
        "not str: 'this is a resource'"
    )


def test_resource_attribute_is_working_as_expected(setup_time_log_db_tests):
    """resource attribute is working okay."""
    data = setup_time_log_db_tests
    new_resource = User(
        name="Test Resource",
        login="test resource 2",
        email="test@resource2.com",
        password="1234",
    )

    assert data["test_time_log"].resource != new_resource
    data["test_time_log"].resource = new_resource
    assert data["test_time_log"].resource == new_resource


def test_resource_argument_updates_backref(setup_time_log_db_tests):
    """setting User in TimeLog resource arg updates User.timee_logs attr."""
    data = setup_time_log_db_tests
    new_resource = User(
        name="Test Resource",
        login="test resource 2",
        email="test@resource2.com",
        password="1234",
    )
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = new_resource
    new_time_log = TimeLog(**kwargs)
    assert new_time_log.resource == new_resource


def test_resource_attribute_updates_backref(setup_time_log_db_tests):
    """setting User in TimeLog.resource attr updates User.timee_logs attr."""
    data = setup_time_log_db_tests
    new_resource = User(
        name="Test Resource",
        login="test resource 2",
        email="test@resource2.com",
        password="1234",
    )

    assert data["test_time_log"].resource != new_resource
    data["test_time_log"].resource = new_resource
    assert data["test_time_log"].resource == new_resource


def test_schedule_mixin_initialization(setup_time_log_db_tests):
    """DateRangeMixin part is initialized correctly."""
    data = setup_time_log_db_tests
    # it should have schedule attributes
    assert data["test_time_log"].start == data["kwargs"]["start"]
    assert data["test_time_log"].duration == data["kwargs"]["duration"]

    data["test_time_log"].start = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    data["test_time_log"].end = data["test_time_log"].start + datetime.timedelta(10)
    assert data["test_time_log"].duration == datetime.timedelta(10)


def test_overbooked_error_1(setup_time_log_db_tests):
    """OverBookedError raised if resource is already booked for the given time period.

    Simple case diagram:
    #####
    #####
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = (datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc),)
    kwargs["duration"] = datetime.timedelta(10)
    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)
    DBSession.commit()

    with pytest.raises(OverBookedError) as cm:
        TimeLog(**kwargs)

    assert str(cm.value) == "The resource has another TimeLog between {} and {}".format(
        time_log1.start,
        time_log1.end,
    )


def test_overbooked_error_2(setup_time_log_db_tests):
    """OverBookedError raised if resource is already booked for the given time period.

    Simple case diagram:
    #######
    #####
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(10)
    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)
    DBSession.commit()

    # time_log2
    kwargs["duration"] = datetime.timedelta(8)
    with pytest.raises(OverBookedError) as cm:
        TimeLog(**kwargs)

    assert str(cm.value) == "The resource has another TimeLog between {} and {}".format(
        time_log1.start,
        time_log1.end,
    )


def test_overbooked_error_3(setup_time_log_db_tests):
    """OverBookedError raised if resource is already booked for the given time period.

    Simple case diagram:
    #####
    #######
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(8)
    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)
    DBSession.commit()

    # time_log2
    kwargs["duration"] = datetime.timedelta(10)
    with pytest.raises(OverBookedError) as cm:
        TimeLog(**kwargs)

    assert str(cm.value) == "The resource has another TimeLog between {} and {}".format(
        time_log1.start,
        time_log1.end,
    )


def test_overbooked_error_4(setup_time_log_db_tests):
    """OverBookedError raised if resource is already booked for the given time period.

    Simple case diagram:
    #######
      #####
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(
        2013, 3, 22, 4, 0, tzinfo=pytz.utc
    ) - datetime.timedelta(2)
    kwargs["duration"] = datetime.timedelta(12)
    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)
    DBSession.commit()

    # time_log2
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(10)

    with pytest.raises(OverBookedError) as cm:
        TimeLog(**kwargs)

    local_tz = tzlocal.get_localzone()
    assert str(cm.value) == "The resource has another TimeLog between {} and {}".format(
        datetime.datetime(2013, 3, 20, 4, 0, tzinfo=pytz.utc).astimezone(local_tz),
        (
            datetime.datetime(2013, 3, 20, 4, 0, tzinfo=pytz.utc)
            + datetime.timedelta(12)
        ).astimezone(local_tz),
    )


def test_overbooked_error_5(setup_time_log_db_tests):
    """OverBookedError raised if resource is already booked for the given time period.

    Simple case diagram:
      #####
    #######
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(10)

    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)
    DBSession.commit()

    # time_log2
    kwargs["start"] = datetime.datetime(
        2013, 3, 22, 4, 0, tzinfo=pytz.utc
    ) - datetime.timedelta(2)
    kwargs["duration"] = datetime.timedelta(12)

    with pytest.raises(OverBookedError) as cm:
        TimeLog(**kwargs)

    local_tz = tzlocal.get_localzone()
    assert str(cm.value) == "The resource has another TimeLog between {} and {}".format(
        datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc).astimezone(local_tz),
        datetime.datetime(2013, 4, 1, 4, 0, tzinfo=pytz.utc).astimezone(local_tz),
    )


def test_overbooked_error_6(setup_time_log_db_tests):
    """OverBookedError raised if resource is already booked for the given time period.

    Simple case diagram:
      #######
    #######
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(15)

    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)
    DBSession.commit()

    # time_log2
    kwargs["start"] = datetime.datetime(
        2013, 3, 22, 4, 0, tzinfo=pytz.utc
    ) - datetime.timedelta(5)
    kwargs["duration"] = datetime.timedelta(15)

    with pytest.raises(OverBookedError) as cm:
        TimeLog(**kwargs)

    local_tz = tzlocal.get_localzone()
    assert str(cm.value) == "The resource has another TimeLog between {} and {}".format(
        datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc).astimezone(local_tz),
        datetime.datetime(2013, 4, 6, 4, 0, tzinfo=pytz.utc).astimezone(local_tz),
    )


def test_overbooked_error_7(setup_time_log_db_tests):
    """OverBookedError raised if resource is already booked for the given time period.

    Simple case diagram:
    #######
      #######
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(
        2013, 3, 22, 4, 0, tzinfo=pytz.utc
    ) - datetime.timedelta(5)
    kwargs["duration"] = datetime.timedelta(15)

    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)
    DBSession.commit()

    # time_log2
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(15)

    with pytest.raises(OverBookedError) as cm:
        TimeLog(**kwargs)

    local_tz = tzlocal.get_localzone()
    assert str(cm.value) == "The resource has another TimeLog between {} and {}".format(
        datetime.datetime(2013, 3, 17, 4, 0, tzinfo=pytz.utc).astimezone(local_tz),
        datetime.datetime(2013, 4, 1, 4, 0, tzinfo=pytz.utc).astimezone(local_tz),
    )


def test_overbooked_error_8(setup_time_log_db_tests):
    """OverBookedError raised if resource is already booked for the given time period.

    Simple case diagram:
    #######
             #######
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(5)
    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)
    DBSession.commit()

    # time_log2
    kwargs["start"] = datetime.datetime(
        2013, 3, 22, 4, 0, tzinfo=pytz.utc
    ) + datetime.timedelta(20)
    # no warning
    time_log2 = TimeLog(**kwargs)
    DBSession.add(time_log2)
    DBSession.commit()


def test_overbooked_error_9(setup_time_log_db_tests):
    """OverBookedError raised if resource is already booked for the given time period.

    Simple case diagram:
             #######
    #######
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(
        2013, 3, 22, 4, 0, tzinfo=pytz.utc
    ) + datetime.timedelta(20)
    kwargs["duration"] = datetime.timedelta(5)
    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)
    DBSession.commit()

    # time_log2
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)

    # no warning
    time_log2 = TimeLog(**kwargs)
    DBSession.add(time_log2)
    DBSession.commit()


def test_overbooked_error_10(setup_time_log_db_tests):
    """no OverBookedError raised for the same TimeLog instance."""
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(2013, 5, 6, 14, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(20)
    time_log1 = TimeLog(**kwargs)

    # no warning
    data["test_resource2"].time_logs.append(time_log1)


def test_overbooked_error_11(setup_time_log_db_tests):
    """DB backend raises IntegrityError if the resource is booked for time the period.

    It is not caught in Python side.

    Simple case diagram:
    #######
      #######
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(
        2013, 3, 22, 4, 0, tzinfo=pytz.utc
    ) - datetime.timedelta(5)
    kwargs["duration"] = datetime.timedelta(15)

    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)

    # time_log2
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(15)

    time_log2 = TimeLog(**kwargs)
    DBSession.add(time_log2)

    # there should be an DatabaseError raised
    with pytest.raises(IntegrityError) as cm:
        DBSession.commit()

    assert (
        "(psycopg2.errors.ExclusionViolation) conflicting key value "
        'violates exclusion constraint "overlapping_time_logs"' in str(cm.value)
    )


def test_overbooked_error_12(setup_time_log_db_tests):
    """DB backend raises IntegrityError if the resource is booked for the time period.

    It is not caught in Python side. But this one ensures that the error is raised even
    if the tasks are different.

    Simple case diagram:
    #######
      #######
    """
    data = setup_time_log_db_tests
    # time_log1
    kwargs = copy.copy(data["kwargs"])
    kwargs["resource"] = data["test_resource2"]
    kwargs["start"] = datetime.datetime(
        2013, 3, 22, 4, 0, tzinfo=pytz.utc
    ) - datetime.timedelta(5)
    kwargs["duration"] = datetime.timedelta(15)
    kwargs["task"] = data["test_task1"]

    time_log1 = TimeLog(**kwargs)

    DBSession.add(time_log1)

    # time_log2
    kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
    kwargs["duration"] = datetime.timedelta(15)
    kwargs["task"] = data["test_task2"]

    time_log2 = TimeLog(**kwargs)
    DBSession.add(time_log2)

    # there should be an DatabaseError raised
    with pytest.raises(IntegrityError) as cm:
        DBSession.commit()

    assert (
        "(psycopg2.errors.ExclusionViolation) conflicting key value "
        'violates exclusion constraint "overlapping_time_logs"' in str(cm.value)
    )


def test_timelog_prevents_auto_flush_if_expanding_task_schedule_timing(
    setup_time_log_db_tests,
):
    """timeLog prevents auto flush if expanding task schedule_timing attribute."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["start"] = kwargs["start"] - datetime.timedelta(days=100)
    tlog1 = TimeLog(**kwargs)

    DBSession.add(tlog1)
    DBSession.commit()

    # create a new time log
    kwargs["start"] = kwargs["start"] + kwargs["duration"]
    _ = TimeLog(**kwargs)


def test_timelog_creation_for_a_child_task(setup_time_log_db_tests):
    """TimeLog creation for a child task which has a couple of parent tasks."""
    data = setup_time_log_db_tests
    dt = datetime.datetime
    parent_task1 = Task(
        name="Parent Task 1",
        project=data["test_project"],
    )
    parent_task2 = Task(
        name="Parent Task 2",
        project=data["test_project"],
    )
    child_task1 = Task(
        name="Child Task 1",
        project=data["test_project"],
        resources=[data["test_resource1"]],
    )
    child_task2 = Task(
        name="Child Task 1",
        project=data["test_project"],
        resources=[data["test_resource2"]],
    )

    # Task hierarchy
    # +-> p1
    # |   |
    # |   +-> p2
    # |   |    |
    # |   |    +-> c1
    # |   |
    # |   +-> c2
    # |
    # +-> data["test_task1"]
    parent_task2.parent = parent_task1
    child_task2.parent = parent_task1
    child_task1.parent = parent_task2

    assert parent_task1.total_logged_seconds == 0
    assert parent_task2.total_logged_seconds == 0
    assert child_task1.total_logged_seconds == 0
    assert child_task2.total_logged_seconds == 0

    # now create a time log for child_task2
    tlog1 = TimeLog(
        task=child_task2,
        resource=child_task2.resources[0],
        start=dt(2013, 7, 31, 10, 0, tzinfo=pytz.utc),
        end=dt(2013, 7, 31, 19, 0, tzinfo=pytz.utc),
    )

    # before commit
    assert parent_task1.total_logged_seconds == 9 * 3600
    assert parent_task2.total_logged_seconds == 0
    assert child_task1.total_logged_seconds == 0
    assert child_task2.total_logged_seconds == 0

    # commit changes
    DBSession.add(tlog1)
    DBSession.commit()

    # after "commit" it should not change
    assert parent_task1.total_logged_seconds == 9 * 3600
    assert parent_task2.total_logged_seconds == 0
    assert child_task1.total_logged_seconds == 0
    assert child_task2.total_logged_seconds == 9 * 3600

    # add a new tlog to child_task2 and commit it
    # now create a time log for child_task2
    tlog2 = TimeLog(
        task=child_task2,
        resource=child_task2.resources[0],
        start=dt(2013, 7, 31, 19, 0, tzinfo=pytz.utc),
        end=dt(2013, 7, 31, 22, 0, tzinfo=pytz.utc),
    )

    assert parent_task1.total_logged_seconds == 12 * 3600
    assert parent_task2.total_logged_seconds == 0
    assert child_task1.total_logged_seconds == 0
    assert child_task2.total_logged_seconds == 9 * 3600

    # commit changes
    DBSession.add(tlog2)
    DBSession.commit()

    assert parent_task1.total_logged_seconds == 12 * 3600
    assert parent_task2.total_logged_seconds == 0
    assert child_task1.total_logged_seconds == 0
    assert child_task2.total_logged_seconds == 12 * 3600

    # add a new time log to child_task1 and commit it
    tlog3 = TimeLog(
        task=child_task1,
        resource=child_task1.resources[0],
        start=dt(2013, 7, 31, 10, 0, tzinfo=pytz.utc),
        end=dt(2013, 7, 31, 19, 0, tzinfo=pytz.utc),
    )
    # commit changes
    DBSession.add(tlog3)
    DBSession.commit()

    assert parent_task1.total_logged_seconds == 21 * 3600
    assert parent_task2.total_logged_seconds == 9 * 3600
    assert child_task1.total_logged_seconds == 9 * 3600
    assert child_task2.total_logged_seconds == 12 * 3600

    # assert parent_task1.total_logged_seconds == 21 * 3600
    # assert parent_task2.total_logged_seconds == 9 * 3600
    # assert child_task1.total_logged_seconds == 9 * 3600
    # assert child_task2.total_logged_seconds == 12 * 3600


def test_time_log_creation_for_a_wfd_leaf_task(setup_time_log_db_tests):
    """StatusError raised if TimeLog is created for a WFD leaf task."""
    data = setup_time_log_db_tests
    new_task = Task(name="Test Task 2", project=data["test_project"])
    new_task.depends_on = [data["test_task1"]]
    kwargs = copy.copy(data["kwargs"])
    kwargs["task"] = new_task
    with pytest.raises(StatusError) as cm:
        TimeLog(**kwargs)

    assert (
        str(cm.value) == "Test Task 2 is a WFD task, and it is not allowed to create "
        "TimeLogs for a WFD task, please supply a RTS, WIP, HREV or "
        "DREV task!"
    )


def test_time_log_creation_for_a_rts_leaf_task(setup_time_log_db_tests):
    """status updated to WIP if a TimeLog instance is created for an RTS leaf task."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    kwargs["start"] -= datetime.timedelta(days=100)
    task.status = data["status_rts"]
    assert task.status == data["status_rts"]
    TimeLog(**kwargs)
    assert task.status == data["status_wip"]


def test_time_log_creation_for_a_wip_leaf_task(setup_time_log_db_tests):
    """status will stay at WIP if a TimeLog instance is created for a WIP leaf task."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    kwargs["start"] -= datetime.timedelta(days=10)
    task.status = data["status_wip"]
    assert task.status == data["status_wip"]
    TimeLog(**kwargs)


def test_time_log_creation_for_a_prev_leaf_task(setup_time_log_db_tests):
    """status will stay PREV if a TimeLog instance is created for a PREV leaf task."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    kwargs["start"] -= datetime.timedelta(days=100)
    task.status = data["status_prev"]
    assert task.status == data["status_prev"]
    TimeLog(**kwargs)
    assert task.status == data["status_prev"]


def test_time_log_creation_for_a_hrev_leaf_task(setup_time_log_db_tests):
    """status updated to WIP if a TimeLog instance is created for a HREV leaf task."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    kwargs["start"] -= datetime.timedelta(days=100)
    task.status = data["status_hrev"]
    assert task.status == data["status_hrev"]
    TimeLog(**kwargs)


def test_time_log_creation_for_a_drev_leaf_task(setup_time_log_db_tests):
    """status will stay DREV if a TimeLog instance is created for a DREV leaf task."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    kwargs["start"] -= datetime.timedelta(days=100)
    task.status = data["status_drev"]
    assert task.status == data["status_drev"]
    TimeLog(**kwargs)


def test_time_log_creation_for_a_oh_leaf_task(setup_time_log_db_tests):
    """StatusError raised if a TimeLog instance is created for a OH leaf task."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    task.status = data["status_oh"]
    assert task.status == data["status_oh"]
    with pytest.raises(StatusError) as cm:
        TimeLog(**kwargs)

    assert (
        str(cm.value) == "test task 1 is a OH task, and it is not allowed to create "
        "TimeLogs for a OH task, please supply a RTS, WIP, HREV or DREV "
        "task!"
    )


def test_time_log_creation_for_a_stop_leaf_task(setup_time_log_db_tests):
    """StatusError raised if a TimeLog instance is created for a STOP leaf task."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    task.status = data["status_stop"]
    assert task.status == data["status_stop"]
    with pytest.raises(StatusError) as cm:
        TimeLog(**kwargs)

    assert (
        str(cm.value) == "test task 1 is a STOP task, and it is not allowed to create "
        "TimeLogs for a STOP task, please supply a RTS, WIP, HREV or "
        "DREV task!"
    )


def test_time_log_creation_for_a_cmpl_leaf_task(setup_time_log_db_tests):
    """StatusError raised if a TimeLog instance is created for a CMPL leaf task."""
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    task.status = data["status_cmpl"]
    assert task.status == data["status_cmpl"]
    with pytest.raises(StatusError) as cm:
        TimeLog(**kwargs)

    assert (
        str(cm.value) == "test task 1 is a CMPL task, and it is not allowed to create "
        "TimeLogs for a CMPL task, please supply a RTS, WIP, HREV or "
        "DREV task!"
    )


def test_time_log_creation_that_violates_dependency_condition_wip_cmpl_onend(
    setup_time_log_db_tests,
):
    """DependencyViolationError raised if the TimeLog violates dependency task relation.

    +--------+
    | Task 1 | ----+
    |  CMPL  |     |
    +--------+     |    +--------+
                   +--->| Task 2 |
                        |  WIP   |
                        +--------+
    """
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    task.status = data["status_cmpl"]
    task.start = datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc)
    task.end = datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc)

    dep_task = Task(
        name="test task 2",
        project=data["test_project"],
        schedule_timing=10,
        schedule_unit="d",
        depends_on=[task],
        resources=[data["test_resource2"]],
    )

    # set the dependency target to onend
    dep_task.task_depends_on[0].dependency_target = "onend"

    # entering a time log to the dates before 2014-03-25-19-0 should raise
    # a ValueError
    with pytest.raises(DependencyViolationError) as cm:
        dep_task.create_time_log(
            data["test_resource2"],
            datetime.datetime(2014, 3, 25, 18, 0, tzinfo=pytz.utc),
            datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc),
        )

    assert str(cm.value) == (
        "It is not possible to create a TimeLog before {}, which "
        'violates the dependency relation of "{}" to "{}"'.format(
            datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc),
            dep_task.name,
            task.name,
        )
    )

    # and creating a TimeLog after that is possible
    dep_task.create_time_log(
        data["test_resource2"],
        datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc),
        datetime.datetime(2014, 3, 25, 20, 0, tzinfo=pytz.utc),
    )


def test_time_log_creation_that_violates_dependency_condition_wip_cmpl_onstart(
    setup_time_log_db_tests,
):
    """ValueError raised if the entered TimeLog violates the dependency relation tasks.

      +--------+
    +-| Task 1 |
    | |  CMPL  |
    | +--------+          +--------+
    +-------------------->| Task 2 |
                          |  WIP   |
                          +--------+
    """
    data = setup_time_log_db_tests
    kwargs = copy.copy(data["kwargs"])
    task = kwargs["task"]
    task.status = data["status_cmpl"]
    task.start = datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc)
    task.end = datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc)

    dep_task = Task(
        name="test task 2",
        project=data["test_project"],
        schedule_timing=10,
        schedule_unit="d",
        depends_on=[task],
        resources=[data["test_resource2"]],
    )

    # set the dependency target to onstart
    dep_task.task_depends_on[0].dependency_target = "onstart"

    # entering a time log to the dates before 2014-03-16-10-0 should raise
    # a ValueError
    with pytest.raises(DependencyViolationError) as cm:
        dep_task.create_time_log(
            data["test_resource2"],
            datetime.datetime(2014, 3, 16, 9, 0, tzinfo=pytz.utc),
            datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc),
        )

    assert str(cm.value) == (
        "It is not possible to create a TimeLog before {}, which "
        'violates the dependency relation of "{}" to "{}"'.format(
            datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc),
            dep_task.name,
            task.name,
        )
    )

    # and creating a TimeLog after that is possible
    dep_task.create_time_log(
        data["test_resource2"],
        datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc),
        datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc),
    )
