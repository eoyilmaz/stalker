# -*- coding: utf-8 -*-
"""Tests for the Task status workflow."""

import datetime
import pytest
import pytz

from stalker import (
    Asset,
    Project,
    Repository,
    Review,
    Status,
    StatusList,
    Task,
    TaskDependency,
    TimeLog,
    Type,
    User,
    Version,
)
from stalker.db.session import DBSession
from stalker.exceptions import StatusError
from stalker.models.mixins import ScheduleModel, TimeUnit


@pytest.fixture(scope="function")
def setup_task_status_workflow_tests():
    """Set up tests for the Task Status Workflow."""
    data = dict()
    # test users
    data["test_user1"] = User(
        name="Test User 1",
        login="tuser1",
        email="tuser1@test.com",
        password="secret",
    )
    data["test_user2"] = User(
        name="Test User 2",
        login="tuser2",
        email="tuser2@test.com",
        password="secret",
    )
    # create a couple of tasks
    data["status_new"] = Status(name="New", code="NEW")
    data["status_wfd"] = Status(name="Waiting For Dependency", code="WFD")
    data["status_rts"] = Status(name="Ready To Start", code="RTS")
    data["status_wip"] = Status(name="Work In Progress", code="WIP")
    data["status_prev"] = Status(name="Pending Review", code="PREV")
    data["status_hrev"] = Status(name="Has Revision", code="HREV")
    data["status_drev"] = Status(name="Dependency Has Revision", code="DREV")
    data["status_oh"] = Status(name="On Hold", code="OH")
    data["status_stop"] = Status(name="Stopped", code="STOP")
    data["status_cmpl"] = Status(name="Completed", code="CMPL")
    data["status_rrev"] = Status(name="Requested Revision", code="RREV")
    data["status_app"] = Status(name="Approved", code="APP")

    data["test_project_status_list"] = StatusList(
        name="Project Statuses",
        target_entity_type="Project",
        statuses=[data["status_wfd"], data["status_wip"], data["status_cmpl"]],
    )

    data["test_task_status_list"] = StatusList(
        name="Task Statuses",
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

    # repository
    data["test_repo"] = Repository(
        name="Test Repository",
        code="TR",
        linux_path="/mnt/T/",
        windows_path="T:/",
        macos_path="/Volumes/T",
    )

    # proj1
    data["test_project1"] = Project(
        name="Test Project 1",
        code="TProj1",
        status_list=data["test_project_status_list"],
        repository=data["test_repo"],
        start=datetime.datetime(2013, 6, 20, 0, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, 0, tzinfo=pytz.utc),
    )

    # root tasks
    data["test_task1"] = Task(
        name="Test Task 1",
        project=data["test_project1"],
        responsible=[data["test_user1"]],
        status_list=data["test_task_status_list"],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )

    data["test_task2"] = Task(
        name="Test Task 2",
        project=data["test_project1"],
        responsible=[data["test_user1"]],
        status_list=data["test_task_status_list"],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )

    data["test_task3"] = Task(
        name="Test Task 3",
        project=data["test_project1"],
        status_list=data["test_task_status_list"],
        resources=[data["test_user1"], data["test_user2"]],
        responsible=[data["test_user1"], data["test_user2"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )

    # children tasks
    # children of data["test_task1"]
    data["test_task4"] = Task(
        name="Test Task 4",
        parent=data["test_task1"],
        status=data["status_wfd"],
        status_list=data["test_task_status_list"],
        resources=[data["test_user1"]],
        depends_on=[data["test_task3"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )

    data["test_task5"] = Task(
        name="Test Task 5",
        parent=data["test_task1"],
        status_list=data["test_task_status_list"],
        resources=[data["test_user1"]],
        depends_on=[data["test_task4"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )

    data["test_task6"] = Task(
        name="Test Task 6",
        parent=data["test_task1"],
        status_list=data["test_task_status_list"],
        resources=[data["test_user1"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )

    # children of data["test_task2"]
    data["test_task7"] = Task(
        name="Test Task 7",
        parent=data["test_task2"],
        status_list=data["test_task_status_list"],
        resources=[data["test_user2"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )

    data["test_task8"] = Task(
        name="Test Task 8",
        parent=data["test_task2"],
        status_list=data["test_task_status_list"],
        resources=[data["test_user2"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )

    data["test_asset_status_list"] = StatusList(
        name="Asset Statuses",
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
        target_entity_type="Asset",
    )

    # create an asset in between
    data["test_asset1"] = Asset(
        name="Test Asset 1",
        code="TA1",
        parent=data["test_task7"],
        type=Type(
            name="Character",
            code="Char",
            target_entity_type="Asset",
        ),
        status_list=data["test_asset_status_list"],
    )

    # new task under asset
    data["test_task9"] = Task(
        name="Test Task 9",
        parent=data["test_asset1"],
        status_list=data["test_task_status_list"],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        resources=[data["test_user2"]],
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )

    # --------------
    # Task Hierarchy
    # --------------
    #
    # +-> Test Task 1
    # |   |
    # |   +-> Test Task 4
    # |   |
    # |   +-> Test Task 5
    # |   |
    # |   +-> Test Task 6
    # |
    # +-> Test Task 2
    # |   |
    # |   +-> Test Task 7
    # |   |   |
    # |   |   +-> Test Asset 1
    # |   |       |
    # |   |       +-> Test Task 9
    # |   |
    # |   +-> Test Task 8
    # |
    # +-> Test Task 3

    # no children for data["test_task3"]
    data["all_tasks"] = [
        data["test_task1"],
        data["test_task2"],
        data["test_task3"],
        data["test_task4"],
        data["test_task5"],
        data["test_task6"],
        data["test_task7"],
        data["test_task8"],
        data["test_task9"],
        data["test_asset1"],
    ]
    return data


def test_walk_hierarchy_is_working_as_expected(setup_task_status_workflow_tests):
    """walk_hierarchy is working as expected."""
    data = setup_task_status_workflow_tests
    # this test should not be placed here
    visited_tasks = []
    expected_result = [
        data["test_task2"],
        data["test_task7"],
        data["test_task8"],
        data["test_asset1"],
        data["test_task9"],
    ]

    for task in data["test_task2"].walk_hierarchy(method=1):
        visited_tasks.append(task)

    assert expected_result == visited_tasks


def test_walk_dependencies_is_working_as_expected(setup_task_status_workflow_tests):
    """walk_dependencies is working as expected."""
    data = setup_task_status_workflow_tests
    # this test should not be placed here
    visited_tasks = []
    expected_result = [
        data["test_task9"],
        data["test_task6"],
        data["test_task4"],
        data["test_task5"],
        data["test_task8"],
        data["test_task3"],
        data["test_task4"],
        data["test_task8"],
        data["test_task3"],
    ]

    # setup dependencies
    data["test_task9"].depends_on = [data["test_task6"]]
    data["test_task6"].depends_on = [data["test_task4"], data["test_task5"]]
    data["test_task5"].depends_on = [data["test_task4"]]
    data["test_task4"].depends_on = [data["test_task8"], data["test_task3"]]

    for task in data["test_task9"].walk_dependencies():
        visited_tasks.append(task)

    assert expected_result == visited_tasks


# The following tests will test the status changes in dependency changes


# Leaf Tasks - dependency relation changes
# WFD
def test_leaf_wfd_task_updated_to_have_a_dependency_of_wfd_task_task(
    setup_task_status_workflow_tests,
):
    """set dependency between a WFD task to another WFD task and the status stay WFD."""
    # create another dependency to make the task3 a WFD task
    data = setup_task_status_workflow_tests
    data["test_task3"].depends_on = []
    data["test_task9"].status = data["status_wip"]
    assert data["test_task9"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task9"])
    assert data["test_task3"].status == data["status_wfd"]
    # make a task with HREV status
    # create dependency
    data["test_task8"].status = data["status_wfd"]
    assert data["test_task8"].status == data["status_wfd"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_wfd_task_updated_to_have_a_dependency_of_rts_task(
    setup_task_status_workflow_tests,
):
    """set dependency between a WFD task to an RTS task and the status stay WFD."""
    data = setup_task_status_workflow_tests
    # create another dependency to make the task3 a WFD task
    data["test_task3"].depends_on = []
    data["test_task9"].status = data["status_wip"]
    assert data["test_task9"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task9"])
    assert data["test_task3"].status == data["status_wfd"]
    # make a task with HREV status
    # create dependency
    data["test_task8"].status = data["status_rts"]
    assert data["test_task8"].status == data["status_rts"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_wfd_task_updated_to_have_a_dependency_of_wip_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a WFD task to a WIP task and the status stay WFD."""
    data = setup_task_status_workflow_tests
    # create another dependency to make the task3 a WFD task
    data["test_task3"].depends_on = []
    data["test_task9"].status = data["status_wip"]
    assert data["test_task9"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task9"])
    assert data["test_task3"].status == data["status_wfd"]
    # make a task with HREV status
    # create dependency
    data["test_task8"].status = data["status_wip"]
    assert data["test_task8"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_wfd_task_updated_to_have_a_dependency_of_prev_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a WFD task to a PREV task and the status stay WFD."""
    data = setup_task_status_workflow_tests
    # create another dependency to make the task3 a WFD task
    data["test_task3"].depends_on = []
    data["test_task9"].status = data["status_wip"]
    assert data["test_task9"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task9"])
    assert data["test_task3"].status == data["status_wfd"]
    # make a task with HREV status
    # create dependency
    data["test_task8"].status = data["status_prev"]
    assert data["test_task8"].status == data["status_prev"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_wfd_task_updated_to_have_a_dependency_of_hrev_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a WFD task to a HREV task and the status stay WFD."""
    data = setup_task_status_workflow_tests
    # create another dependency to make the task3 a WFD task
    data["test_task3"].depends_on = []
    data["test_task9"].status = data["status_wip"]
    assert data["test_task9"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task9"])
    assert data["test_task3"].status == data["status_wfd"]
    # make a task with HREV status
    # create dependency
    data["test_task8"].status = data["status_hrev"]
    assert data["test_task8"].status == data["status_hrev"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_wfd_task_updated_to_have_a_dependency_of_oh_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a WFD task to a OH task and the status stay WFD."""
    data = setup_task_status_workflow_tests
    # create another dependency to make the task3 a WFD task
    data["test_task3"].depends_on = []
    data["test_task9"].status = data["status_wip"]
    assert data["test_task9"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task9"])
    assert data["test_task3"].status == data["status_wfd"]
    # make a task with HREV status
    # create dependency
    data["test_task8"].status = data["status_oh"]
    assert data["test_task8"].status == data["status_oh"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_wfd_task_updated_to_have_a_dependency_of_stop_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a WFD task to a STOP task and the status stay WFD."""
    data = setup_task_status_workflow_tests
    # create another dependency to make the task3 a WFD task
    data["test_task3"].depends_on = []
    data["test_task9"].status = data["status_wip"]
    assert data["test_task9"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task9"])
    assert data["test_task3"].status == data["status_wfd"]
    # make a task with HREV status
    # create dependency
    data["test_task8"].status = data["status_stop"]
    assert data["test_task8"].status == data["status_stop"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_wfd_task_updated_to_have_a_dependency_of_cmpl_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a WFD task to a CMPL task and the status stay to WFD."""
    data = setup_task_status_workflow_tests
    # create another dependency to make the task3 a WFD task
    data["test_task3"].depends_on = []
    data["test_task9"].status = data["status_wip"]
    assert data["test_task9"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task9"])
    assert data["test_task3"].status == data["status_wfd"]
    # make a task with HREV status
    # create dependency
    data["test_task8"].status = data["status_cmpl"]
    assert data["test_task8"].status == data["status_cmpl"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


# Leaf Tasks - dependency relation changes
# RTS
def test_leaf_rts_task_updated_to_have_a_dependency_of_wfd_task_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a RTS task to a WFD task the status updated to WFD."""
    data = setup_task_status_workflow_tests
    # find an RTS task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    # make a task with WFD status
    data["test_task8"].status = data["status_wfd"]
    assert data["test_task8"].status == data["status_wfd"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_rts_task_updated_to_have_a_dependency_of_rts_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a RTS task to a RTS task the status updated to WFD."""
    data = setup_task_status_workflow_tests
    # find an RTS task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    # make a task with RTS status
    data["test_task8"].status = data["status_rts"]
    assert data["test_task8"].status == data["status_rts"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_rts_task_updated_to_have_a_dependency_of_wip_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a RTS task to a WIP task the status updated to WFD."""
    data = setup_task_status_workflow_tests
    # find an RTS task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    # make a task with WIP status
    data["test_task8"].status = data["status_wip"]
    assert data["test_task8"].status == data["status_wip"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_rts_task_updated_to_have_a_dependency_of_prev_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a RTS task to a PREV task the status updated to WFD."""
    data = setup_task_status_workflow_tests
    # find an RTS task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    # make a task with PREV status
    data["test_task8"].status = data["status_prev"]
    assert data["test_task8"].status == data["status_prev"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_rts_task_updated_to_have_a_dependency_of_hrev_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a RTS task to a HREV task the status updated to WFD."""
    data = setup_task_status_workflow_tests
    # find an RTS task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    # make a task with HREV status
    data["test_task8"].status = data["status_hrev"]
    assert data["test_task8"].status == data["status_hrev"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_rts_task_updated_to_have_a_dependency_of_oh_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between a RTS task to a OH task the status updated to WFD."""
    data = setup_task_status_workflow_tests
    # find an RTS task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    # make a task with OH status
    data["test_task8"].status = data["status_oh"]
    assert data["test_task8"].status == data["status_oh"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_leaf_rts_task_updated_to_have_a_dependency_of_stop_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between an RTS task to a STOP task the status will stay RTS."""
    data = setup_task_status_workflow_tests
    # find an RTS task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    # make a task with STOP status
    data["test_task8"].status = data["status_stop"]
    assert data["test_task8"].status == data["status_stop"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_rts"]


def test_leaf_rts_task_updated_to_have_a_dependency_of_cmpl_task(
    setup_task_status_workflow_tests,
):
    """set a dependency between an RTS task to a CMPL task the status will stay RTS."""
    data = setup_task_status_workflow_tests
    # find an RTS task
    assert data["test_task3"].depends_on == []
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    # make a task with CMPL status
    data["test_task8"].status = data["status_cmpl"]
    assert data["test_task8"].status == data["status_cmpl"]
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_rts"]


# Leaf Tasks - dependency changes
# WIP - DREV - PREV - HREV - OH - STOP - CMPL
def test_leaf_wip_task_dependency_cannot_be_updated(setup_task_status_workflow_tests):
    """it is not possible to update the dependencies of a WIP task."""
    data = setup_task_status_workflow_tests
    # find an WIP task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_wip"]
    assert data["test_task3"].status == data["status_wip"]
    # create dependency
    with pytest.raises(StatusError) as cm:
        data["test_task3"].depends_on.append(data["test_task8"])

    assert (
        str(cm.value) == "This is a WIP task and it is not allowed to change the "
        "dependencies of a WIP task"
    )


def test_leaf_prev_task_dependency_cannot_be_updated(setup_task_status_workflow_tests):
    """it is not possible to update the dependencies of a PREV task."""
    data = setup_task_status_workflow_tests
    # find an PREV task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_prev"]
    assert data["test_task3"].status == data["status_prev"]
    # create dependency
    with pytest.raises(StatusError) as cm:
        data["test_task3"].depends_on.append(data["test_task8"])

    assert (
        str(cm.value) == "This is a PREV task and it is not allowed to change the "
        "dependencies of a PREV task"
    )


def test_leaf_hrev_task_dependency_cannot_be_updated(setup_task_status_workflow_tests):
    """it is not possible to update the dependencies of a HREV task."""
    data = setup_task_status_workflow_tests
    # find an HREV task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_hrev"]
    assert data["test_task3"].status == data["status_hrev"]
    # create dependency
    with pytest.raises(StatusError) as cm:
        data["test_task3"].depends_on.append(data["test_task8"])

    assert (
        str(cm.value) == "This is a HREV task and it is not allowed to change the "
        "dependencies of a HREV task"
    )


def test_leaf_drev_task_dependency_cannot_be_updated(setup_task_status_workflow_tests):
    """it is not possible to update the dependencies of a DREV
    task
    """
    data = setup_task_status_workflow_tests
    # find an DREV task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_drev"]
    assert data["test_task3"].status == data["status_drev"]
    # create dependency
    with pytest.raises(StatusError) as cm:
        data["test_task3"].depends_on.append(data["test_task8"])

    assert (
        str(cm.value) == "This is a DREV task and it is not allowed to change the "
        "dependencies of a DREV task"
    )


def test_leaf_oh_task_dependency_cannot_be_updated(setup_task_status_workflow_tests):
    """it is not possible to update the dependencies of a OH task."""
    data = setup_task_status_workflow_tests
    # find an OH task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_oh"]
    assert data["test_task3"].status == data["status_oh"]
    # create dependency
    with pytest.raises(StatusError) as cm:
        data["test_task3"].depends_on.append(data["test_task8"])

    assert (
        str(cm.value) == "This is a OH task and it is not allowed to change the "
        "dependencies of a OH task"
    )


def test_leaf_stop_task_dependency_cannot_be_updated(setup_task_status_workflow_tests):
    """it is not possible to update the dependencies of a STOP task."""
    data = setup_task_status_workflow_tests
    # find an STOP task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_stop"]
    assert data["test_task3"].status == data["status_stop"]
    # create dependency
    with pytest.raises(StatusError) as cm:
        data["test_task3"].depends_on.append(data["test_task8"])

    assert (
        str(cm.value) == "This is a STOP task and it is not allowed to change the "
        "dependencies of a STOP task"
    )


def test_leaf_cmpl_task_dependency_cannot_be_updated(setup_task_status_workflow_tests):
    """it is not possible to update the dependencies of a CMPL task."""
    data = setup_task_status_workflow_tests
    # find an CMPL task
    data["test_task3"].depends_on = []
    data["test_task3"].status = data["status_cmpl"]
    assert data["test_task3"].status == data["status_cmpl"]
    # create dependency
    with pytest.raises(StatusError) as cm:
        data["test_task3"].depends_on.append(data["test_task8"])

    assert (
        str(cm.value) == "This is a CMPL task and it is not allowed to change the "
        "dependencies of a CMPL task"
    )


# dependencies of containers
# container Tasks - dependency relation changes
# RTS
def test_container_rts_task_updated_to_have_a_dependency_of_wfd_task_task(
    setup_task_status_workflow_tests,
):
    """dep. between an RTS parent task to a WFD task and status is updated to WFD."""
    data = setup_task_status_workflow_tests
    # make a task with WFD status
    data["test_task3"].depends_on = []
    data["test_task8"].status = data["status_wfd"]
    assert data["test_task8"].status == data["status_wfd"]
    # find a RTS container task
    data["test_task3"].children.append(data["test_task2"])
    data["test_task2"].status = data["status_rts"]
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_container_rts_task_updated_to_have_a_dependency_of_rts_task(
    setup_task_status_workflow_tests,
):
    """dep. between an RTS parent task to an RTS task and status is updated to WFD."""
    data = setup_task_status_workflow_tests
    # make a task with WFD status
    data["test_task3"].depends_on = []
    data["test_task8"].status = data["status_rts"]
    assert data["test_task8"].status == data["status_rts"]
    # find a RTS container task
    data["test_task3"].children.append(data["test_task2"])
    data["test_task2"].status = data["status_rts"]
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_container_rts_task_updated_to_have_a_dependency_of_wip_task(
    setup_task_status_workflow_tests,
):
    """dep. between an RTS parent task to a WIP task and status is updated to WFD."""
    data = setup_task_status_workflow_tests
    # make a task with WIP status
    data["test_task3"].depends_on = []
    data["test_task8"].status = data["status_wip"]
    assert data["test_task8"].status == data["status_wip"]
    # find a RTS container task
    data["test_task3"].children.append(data["test_task2"])
    data["test_task2"].status = data["status_rts"]
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_container_rts_task_updated_to_have_a_dependency_of_prev_task(
    setup_task_status_workflow_tests,
):
    """dep. between an RTS parent task to a PREV task and status is updated to WFD."""
    data = setup_task_status_workflow_tests
    # make a task with PREV status
    data["test_task3"].depends_on = []
    data["test_task8"].status = data["status_prev"]
    assert data["test_task8"].status == data["status_prev"]
    # find a RTS container task
    data["test_task3"].children.append(data["test_task2"])
    data["test_task2"].status = data["status_rts"]
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_container_rts_task_updated_to_have_a_dependency_of_hrev_task(
    setup_task_status_workflow_tests,
):
    """dep. between an RTS parent task to an HREV task and status is updated to WFD."""
    data = setup_task_status_workflow_tests
    # make a task with HREV status
    data["test_task3"].depends_on = []
    data["test_task8"].status = data["status_hrev"]
    assert data["test_task8"].status == data["status_hrev"]
    # find a RTS container task
    data["test_task3"].children.append(data["test_task2"])
    data["test_task2"].status = data["status_rts"]
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_container_rts_task_updated_to_have_a_dependency_of_oh_task(
    setup_task_status_workflow_tests,
):
    """dep. between an RTS parent task to an OH task and status is updated to WFD."""
    data = setup_task_status_workflow_tests
    # make a task with OH status
    data["test_task3"].depends_on = []
    data["test_task8"].status = data["status_oh"]
    assert data["test_task8"].status == data["status_oh"]
    # find a RTS container task
    data["test_task3"].children.append(data["test_task2"])
    data["test_task2"].status = data["status_rts"]
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_wfd"]


def test_container_rts_task_updated_to_have_a_dependency_of_stop_task(
    setup_task_status_workflow_tests,
):
    """dep. between an RTS parent task to a STOP task and status will stay RTS."""
    data = setup_task_status_workflow_tests
    # make a task with STOP status
    data["test_task3"].depends_on = []
    data["test_task8"].status = data["status_stop"]
    assert data["test_task8"].status == data["status_stop"]
    # find a RTS container task
    data["test_task3"].children.append(data["test_task2"])
    data["test_task2"].status = data["status_rts"]
    data["test_task3"].status = data["status_rts"]
    assert data["test_task3"].status == data["status_rts"]
    # create dependency
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_rts"]


# Container Tasks - dependency relation changes
# WIP - DREV - PREV - HREV - OH - STOP - CMPL
def test_container_wip_task_dependency_cannot_be_updated(
    setup_task_status_workflow_tests,
):
    """it is not possible to update the dependencies of a WIP container task."""
    data = setup_task_status_workflow_tests
    # find an WIP task
    data["test_task1"].depends_on = []
    data["test_task1"].status = data["status_wip"]
    assert data["test_task1"].status == data["status_wip"]
    # create dependency
    with pytest.raises(StatusError) as cm:
        data["test_task1"].depends_on.append(data["test_task8"])

    assert (
        str(cm.value) == "This is a WIP task and it is not allowed to change the "
        "dependencies of a WIP task"
    )


def test_container_cmpl_task_dependency_cannot_be_updated(
    setup_task_status_workflow_tests,
):
    """it is not possible to update the dependencies of a CMPL container task."""
    data = setup_task_status_workflow_tests
    # find an CMPL task
    data["test_task1"].status = data["status_cmpl"]
    assert data["test_task1"].status == data["status_cmpl"]
    # create dependency
    with pytest.raises(StatusError) as cm:
        data["test_task1"].depends_on.append(data["test_task8"])

    assert (
        str(cm.value) == "This is a CMPL task and it is not allowed to change the "
        "dependencies of a CMPL task"
    )


#
# Action Tests
#


# create_time_log
# WFD
def test_create_time_log_in_wfd_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if create_time_log action is used in a WFD task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wfd"]
    resource = data["test_task3"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    with pytest.raises(StatusError) as cm:
        data["test_task3"].create_time_log(resource, start, end)

    assert (
        str(cm.value) == "Test Task 3 is a WFD task, and it is not allowed to create "
        "TimeLogs for a WFD task, please supply a RTS, WIP, HREV or "
        "DREV task!"
    )


# RTS: status updated to WIP
def test_create_time_log_in_rts_leaf_task_status_updated_to_wip(
    setup_task_status_workflow_tests,
):
    """RTS task converted to WIP if create_time_log action is used."""
    data = setup_task_status_workflow_tests
    data["test_task9"].status = data["status_rts"]
    resource = data["test_task9"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    data["test_task9"].create_time_log(resource, start, end)
    assert data["test_task9"].status == data["status_wip"]


# RTS -> parent update
def test_create_time_log_in_rts_leaf_task_update_parent_status(
    setup_task_status_workflow_tests,
):
    """parent of the RTS task converted to WIP after create_time_log action used."""
    data = setup_task_status_workflow_tests
    data["test_task2"].status = data["status_rts"]
    data["test_task8"].status = data["status_rts"]

    assert data["test_task8"].parent == data["test_task2"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task8"].create_time_log(
        resource=data["test_task8"].resources[0], start=now, end=now + td(hours=1)
    )

    assert data["test_task8"].status == data["status_wip"]
    assert data["test_task2"].status == data["status_wip"]


# RTS -> root task no problem
def test_create_time_log_in_rts_root_task_no_parent_no_problem(
    setup_task_status_workflow_tests,
):
    """RTS leaf task status converted to WIP if create_time_log action is used."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    resource = data["test_task3"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    data["test_task3"].create_time_log(resource, start, end)
    assert data["test_task3"].status == data["status_wip"]


# WIP
def test_create_time_log_in_wip_leaf_task(setup_task_status_workflow_tests):
    """no problem if create_time_log in a WIP task, and the status stays WIP."""
    data = setup_task_status_workflow_tests
    data["test_task9"].status = data["status_wip"]
    resource = data["test_task9"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    data["test_task9"].create_time_log(resource, start, end)
    assert data["test_task9"].status == data["status_wip"]


# PREV
def test_create_time_log_in_prev_leaf_task(setup_task_status_workflow_tests):
    """no problem to call create_time_log for a PREV task and the status stays PREV."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_prev"]
    resource = data["test_task3"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    assert data["test_task3"].status == data["status_prev"]
    tlog = data["test_task3"].create_time_log(resource, start, end)
    assert isinstance(tlog, TimeLog)
    assert data["test_task3"].status == data["status_prev"]


# HREV
def test_create_time_log_in_hrev_leaf_task(setup_task_status_workflow_tests):
    """status converted to WIP if create_time_log is used in a HREV task."""
    data = setup_task_status_workflow_tests
    data["test_task9"].status = data["status_hrev"]
    resource = data["test_task9"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    data["test_task9"].create_time_log(resource, start, end)
    assert data["test_task9"].status == data["status_wip"]


# DREV
def test_create_time_log_in_drev_leaf_task(setup_task_status_workflow_tests):
    """status will stay DREV if create_time_log is used in a DREV task."""
    data = setup_task_status_workflow_tests
    data["test_task9"].status = data["status_drev"]
    resource = data["test_task9"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    data["test_task9"].create_time_log(resource, start, end)
    assert data["test_task9"].status == data["status_drev"]


# OH
def test_create_time_log_in_oh_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the create_time_log actions is used in a OH task."""
    data = setup_task_status_workflow_tests
    data["test_task9"].status = data["status_oh"]
    resource = data["test_task9"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    with pytest.raises(StatusError) as cm:
        data["test_task9"].create_time_log(resource, start, end)

    assert (
        str(cm.value) == "Test Task 9 is a OH task, and it is not allowed to create "
        "TimeLogs for a OH task, please supply a RTS, WIP, HREV or DREV "
        "task!"
    )


# STOP
def test_create_time_log_in_stop_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the create_time_log action is used in a STOP task."""
    data = setup_task_status_workflow_tests
    data["test_task9"].status = data["status_stop"]
    resource = data["test_task9"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    with pytest.raises(StatusError) as cm:
        data["test_task9"].create_time_log(resource, start, end)

    assert (
        str(cm.value) == "Test Task 9 is a STOP task, and it is not allowed to create "
        "TimeLogs for a STOP task, please supply a RTS, WIP, HREV or "
        "DREV task!"
    )


# CMPL
def test_create_time_log_in_cmpl_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the create_time_log action is used in a CMPL task."""
    data = setup_task_status_workflow_tests
    data["test_task9"].status = data["status_cmpl"]
    resource = data["test_task9"].resources[0]
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    with pytest.raises(StatusError) as cm:
        data["test_task9"].create_time_log(resource, start, end)

    assert (
        str(cm.value) == "Test Task 9 is a CMPL task, and it is not allowed to create "
        "TimeLogs for a CMPL task, please supply a RTS, WIP, HREV or "
        "DREV task!"
    )


# On Container Task
def test_create_time_log_on_container_task(setup_task_status_workflow_tests):
    """ValueError raised if the create_time_log action used in a container task."""
    data = setup_task_status_workflow_tests
    start = datetime.datetime.now(pytz.utc)
    end = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1)
    data["test_task2"].id = 36
    with pytest.raises(ValueError) as cm:
        data["test_task2"].create_time_log(resource=None, start=start, end=end)

    assert (
        str(cm.value) == "Test Task 2 (id: 36) is a container task, and it is not "
        "allowed to create TimeLogs for a container task"
    )


def test_create_time_log_is_creating_time_logs(setup_task_status_workflow_tests):
    """create_time_log action is really creating some time logs."""
    data = setup_task_status_workflow_tests
    # initial condition
    assert len(data["test_task3"].time_logs) == 0

    now = datetime.datetime.now(pytz.utc)
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now,
        end=now + datetime.timedelta(hours=1),
    )
    assert len(data["test_task3"].time_logs) == 1
    assert data["test_task3"].total_logged_seconds == 3600

    now = datetime.datetime.now(pytz.utc)
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + datetime.timedelta(hours=1),
        end=now + datetime.timedelta(hours=2),
    )
    assert len(data["test_task3"].time_logs) == 2
    assert data["test_task3"].total_logged_seconds == 7200


def test_create_time_log_returns_time_log_instance(setup_task_status_workflow_tests):
    """create_time_log returns a TimeLog instance."""
    data = setup_task_status_workflow_tests
    assert len(data["test_task3"].time_logs) == 0

    now = datetime.datetime.now(pytz.utc)
    tl = data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now,
        end=now + datetime.timedelta(hours=1),
    )
    assert isinstance(tl, TimeLog)


# request_review
# WFD
def test_request_review_in_wfd_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_review action is used in a WFD leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wfd"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_review()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a WFD task, and it is not "
        "suitable for requesting a review, please supply a WIP task "
        "instead."
    )


# RTS
def test_request_review_in_rts_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_review action is used in a RTS leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_review()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a RTS task, and it is not "
        "suitable for requesting a review, please supply a WIP task "
        "instead."
    )


# PREV
def test_request_review_in_prev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_review action is used in a PREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_prev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_review()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a PREV task, and it is not "
        "suitable for requesting a review, please supply a WIP task "
        "instead."
    )


# HREV
def test_request_review_in_hrev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_review action is used in a HREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_hrev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_review()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a HREV task, and it is not "
        "suitable for requesting a review, please supply a WIP task "
        "instead."
    )


# DREV
def test_request_review_in_drev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_review action is used in a DREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_drev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_review()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a DREV task, and it is not "
        "suitable for requesting a review, please supply a WIP task "
        "instead."
    )


# OH
def test_request_review_in_oh_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_review action is used in a OH leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_oh"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_review()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a OH task, and it is not "
        "suitable for requesting a review, please supply a WIP task "
        "instead."
    )


# STOP
def test_request_review_in_stop_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_review action is used in a STOP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_stop"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_review()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a STOP task, and it is not "
        "suitable for requesting a review, please supply a WIP task "
        "instead."
    )


# CMPL
def test_request_review_in_cmpl_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_review action is used in a CMPL leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_cmpl"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_review()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a CMPL task, and it is not "
        "suitable for requesting a review, please supply a WIP task "
        "instead."
    )


# request_revision
# WFD
def test_request_revision_in_wfd_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if request_revision action is used in a WFD leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wfd"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_revision()

    assert (
        str(cm.value)
        == "Test Task 3 (id: 37) is a WFD task, and it is not suitable for "
        "requesting a revision, please supply a PREV or CMPL task"
    )


# RTS
def test_request_revision_in_rts_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_revision action is used in a RTS leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_revision()

    assert (
        str(cm.value)
        == "Test Task 3 (id: 37) is a RTS task, and it is not suitable for "
        "requesting a revision, please supply a PREV or CMPL task"
    )


# WIP
def test_request_revision_in_wip_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the request_revision action is used in a WIP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wip"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_revision()

    assert (
        str(cm.value)
        == "Test Task 3 (id: 37) is a WIP task, and it is not suitable for "
        "requesting a revision, please supply a PREV or CMPL task"
    )


# HREV
@pytest.mark.parametrize("schedule_unit", ["h", TimeUnit.Hour])
def test_request_revision_in_hrev_leaf_task(
    setup_task_status_workflow_tests, schedule_unit
):
    """StatusError raised if the request_revision action is used in a HREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_hrev"]
    data["test_task3"].id = 37
    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": schedule_unit,
    }
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_revision(**kw)

    assert str(cm.value) == (
        "Test Task 3 (id: 37) is a HREV task, and it is not suitable "
        "for requesting a revision, please supply a PREV or CMPL task"
    )


# OH
@pytest.mark.parametrize("schedule_unit", ["h", TimeUnit.Hour])
def test_request_revision_in_oh_leaf_task(
    setup_task_status_workflow_tests,
    schedule_unit,
):
    """StatusError raised if the request_revision action is used in a OH leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_oh"]
    data["test_task3"].id = 37
    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": schedule_unit,
    }
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_revision(**kw)

    assert (
        str(cm.value)
        == "Test Task 3 (id: 37) is a OH task, and it is not suitable for "
        "requesting a revision, please supply a PREV or CMPL task"
    )


# STOP
@pytest.mark.parametrize("schedule_unit", ["h", TimeUnit.Hour])
def test_request_revision_in_stop_leaf_task(
    setup_task_status_workflow_tests, schedule_unit
):
    """StatusError raised if the request_revision action is used in a STOP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_stop"]
    data["test_task3"].id = 37
    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": schedule_unit,
    }
    with pytest.raises(StatusError) as cm:
        data["test_task3"].request_revision(**kw)

    assert (
        str(cm.value) == "Test Task 3 (id: 37) is a STOP task, and it is not suitable "
        "for requesting a revision, please supply a PREV or CMPL task"
    )


# hold
# WFD
def test_hold_in_wfd_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the hold action is used in a WFD leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wfd"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].hold()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a WFD task, only WIP or DREV tasks can "
        "be set to On Hold"
    )


# RTS
def test_hold_in_rts_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the hold action is used in a RTS leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].hold()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a RTS task, only WIP or DREV tasks can "
        "be set to On Hold"
    )


# WIP: Status updated to OH
def test_hold_in_wip_leaf_task_status(setup_task_status_workflow_tests):
    """status updated to OH if the hold action is used in a WIP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wip"]
    data["test_task3"].hold()
    assert data["test_task3"].status == data["status_oh"]


# WIP: Schedule values are intact
def test_hold_in_wip_leaf_task_schedule_values(setup_task_status_workflow_tests):
    """schedule values intact if the hold action is used in a WIP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wip"]
    data["test_task3"].hold()
    assert data["test_task3"].schedule_timing == 10
    assert data["test_task3"].schedule_unit == TimeUnit.Day


# WIP: Priority is set to 0
def test_hold_in_wip_leaf_task(setup_task_status_workflow_tests):
    """priority set to 0 if the hold action is used in a WIP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wip"]
    data["test_task3"].hold()
    assert data["test_task3"].priority == 0


# PREV
def test_hold_in_prev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the hold action is used in a PREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_prev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].hold()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a PREV task, only WIP or DREV tasks can "
        "be set to On Hold"
    )


# HREV
def test_hold_in_hrev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the hold action is used in a HREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_hrev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].hold()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a HREV task, only WIP or DREV tasks can "
        "be set to On Hold"
    )


# DREV: Status updated to OH
def test_hold_in_drev_leaf_task_status_updated_to_oh(setup_task_status_workflow_tests):
    """status updated to OH if the hold action is used in a DREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_drev"]
    data["test_task3"].hold()
    assert data["test_task3"].status == data["status_oh"]


# DREV: Schedule values are intact
def test_hold_in_drev_leaf_task_schedule_values_are_intact(
    setup_task_status_workflow_tests,
):
    """schedule values intact if the hold action is used in a DREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_drev"]
    data["test_task3"].hold()
    assert data["test_task3"].schedule_timing == 10
    assert data["test_task3"].schedule_unit == TimeUnit.Day


# DREV: Priority is set to 0
def test_hold_in_drev_leaf_task_priority_set_to_0(setup_task_status_workflow_tests):
    """priority set to 0 if the hold action is used in a DREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_drev"]
    data["test_task3"].hold()
    assert data["test_task3"].priority == 0


# OH
def test_hold_in_oh_leaf_task(setup_task_status_workflow_tests):
    """status will stay on OH if the hold action is used in a OH leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_oh"]
    data["test_task3"].hold()
    assert data["test_task3"].status == data["status_oh"]


# STOP
def test_hold_in_stop_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the hold action is used in a STOP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_stop"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].hold()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a STOP task, only WIP or DREV tasks can "
        "be set to On Hold"
    )


# CMPL
def test_hold_in_cmpl_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the hold action is used in a CMPL leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_cmpl"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].hold()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a CMPL task, only WIP or DREV tasks can "
        "be set to On Hold"
    )


# stop
# WFD
def test_stop_in_wfd_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the stop action is used in a WFD leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wfd"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].stop()

    assert (
        str(cm.value) == "Test Task 3 (id:37)is a WFD task and it is not possible to "
        "stop a WFD task."
    )


# RTS
def test_stop_in_rts_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the stop action is used in a RTS leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].stop()

    assert (
        str(cm.value) == "Test Task 3 (id:37)is a RTS task and it is not possible to "
        "stop a RTS task."
    )


# WIP: Status Test
def test_stop_in_wip_leaf_task_status_is_updated_to_stop(
    setup_task_status_workflow_tests,
):
    """status updated to STOP if the stop action is used in a WIP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wip"]
    data["test_task3"].hold()
    assert data["test_task3"].status == data["status_oh"]


# WIP: Schedule Timing Test
def test_stop_in_wip_leaf_task_schedule_values_clamped(
    setup_task_status_workflow_tests,
):
    """stop action on a WIP task clamps the schedule values to total_logged_seconds."""
    data = setup_task_status_workflow_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task8"].status = data["status_rts"]
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )
    data["test_task8"].status = data["status_wip"]
    data["test_task8"].stop()
    assert data["test_task8"].schedule_timing == 2
    assert data["test_task8"].schedule_unit == TimeUnit.Hour


# WIP: Dependency Status: WFD -> RTS
def test_stop_in_wip_leaf_task_dependent_task_status_updated_from_wfd_to_rts(
    setup_task_status_workflow_tests,
):
    """stop action updates dependent task status from WFD to RTS on a WIP task."""
    data = setup_task_status_workflow_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task9"].status = data["status_rts"]
    data["test_task8"].status = data["status_rts"]

    data["test_task9"].depends_on = [data["test_task8"]]

    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )
    data["test_task8"].status = data["status_wip"]
    data["test_task8"].stop()
    assert data["test_task9"].status == data["status_rts"]


# WIP: Dependency Status: DREV -> WIP
def test_stop_in_wip_leaf_task_status_from_drev_to_hrev(
    setup_task_status_workflow_tests,
):
    """stop action updates dependent task status from DREV to HREV on a WIP task."""
    data = setup_task_status_workflow_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task9"].status = data["status_rts"]
    data["test_task8"].status = data["status_cmpl"]

    data["test_task9"].depends_on = [data["test_task8"]]

    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )
    data["test_task9"].status = data["status_wip"]

    data["test_task8"].status = data["status_hrev"]
    data["test_task9"].status = data["status_drev"]

    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now + td(hours=4),
        end=now + td(hours=5),
    )

    data["test_task8"].status = data["status_wip"]
    data["test_task8"].stop()
    assert data["test_task9"].status == data["status_hrev"]


# WIP: parent statuses
def test_stop_in_drev_leaf_task_check_parent_status(setup_task_status_workflow_tests):
    """parent status is updated okay if stop action is used in a DREV leaf task."""
    data = setup_task_status_workflow_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    data["test_task9"].status = data["status_drev"]
    data["test_task9"].stop()
    assert data["test_task9"].status == data["status_stop"]
    assert data["test_asset1"].status == data["status_cmpl"]


# PREV
def test_stop_in_prev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the stop action is used in a PREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_prev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].stop()

    assert (
        str(cm.value) == "Test Task 3 (id:37)is a PREV task and it is not possible to "
        "stop a PREV task."
    )


# HREV
def test_stop_in_hrev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the stop action is used in a HREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_hrev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].stop()

    assert (
        str(cm.value) == "Test Task 3 (id:37)is a HREV task and it is not possible to "
        "stop a HREV task."
    )


# DREV: Status Test
def test_stop_in_drev_leaf_task_status_is_updated_to_stop(
    setup_task_status_workflow_tests,
):
    """status set to STOP if the stop action is used in a DREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_drev"]
    data["test_task3"].stop()
    assert data["test_task3"].status == data["status_stop"]


# DREV: Schedule Timing Test
def test_stop_in_drev_leaf_task_schedule_values_are_clamped(
    setup_task_status_workflow_tests,
):
    """stop action clamps schedule_timing to current time logs in a DREV lef task."""
    data = setup_task_status_workflow_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task8"].status = data["status_rts"]
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now,
        end=now + td(hours=2),
    )
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=4),
    )
    data["test_task8"].status = data["status_drev"]
    data["test_task8"].stop()
    assert data["test_task8"].schedule_timing == 4
    assert data["test_task8"].schedule_unit == TimeUnit.Hour


# DREV: parent statuses
def test_stop_in_drev_leaf_task_parent_status(setup_task_status_workflow_tests):
    """parent status is updated okay if the stop action is used in a DREV leaf task."""
    data = setup_task_status_workflow_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    data["test_task9"].status = data["status_wip"]
    data["test_task9"].stop()
    assert data["test_task9"].status == data["status_stop"]
    assert data["test_asset1"].status == data["status_cmpl"]


# DREV: Dependency Status: WFD -> RTS
def test_stop_in_drev_leaf_task_dependent_task_status_updated_from_wfd_to_rts(
    setup_task_status_workflow_tests,
):
    """dependent task statuses updated okay if stop action taken on a DREV leaf task."""
    data = setup_task_status_workflow_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task9"].status = data["status_rts"]
    data["test_task8"].status = data["status_rts"]

    data["test_task9"].depends_on = [data["test_task8"]]

    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )
    data["test_task8"].status = data["status_wip"]
    data["test_task8"].stop()
    assert data["test_task9"].status == data["status_rts"]


# DREV: Dependency Status: DREV -> WIP
def test_stop_in_drev_leaf_task_dependent_task_status_updated_from_drev_to_hrev(
    setup_task_status_workflow_tests,
):
    """dependent task statuses updated okay if stop action taken on a DREV leaf task."""
    data = setup_task_status_workflow_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task9"].status = data["status_rts"]
    data["test_task8"].status = data["status_rts"]

    data["test_task9"].depends_on = [data["test_task8"]]
    data["test_task9"].status = data["status_drev"]  # this set by an
    # action in normal run
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task8"],
        resource=data["test_task8"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )
    data["test_task8"].status = data["status_wip"]
    data["test_task8"].stop()
    assert data["test_task9"].status == data["status_hrev"]


# OH
def test_stop_in_oh_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the stop action is used in a OH leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_oh"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].stop()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37)is a OH task and it is not possible to stop "
        "a OH task."
    )


# STOP
def test_stop_in_stop_leaf_task(setup_task_status_workflow_tests):
    """status will stay on STOP if the stop action is used in a STOP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_stop"]
    data["test_task3"].stop()
    assert data["test_task3"].status == data["status_stop"]


# CMPL
def test_stop_in_cmpl_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the stop action is used in a CMPL leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_cmpl"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].stop()

    assert (
        str(cm.value) == "Test Task 3 (id:37)is a CMPL task and it is not possible to "
        "stop a CMPL task."
    )


# resume
# WFD
def test_resume_in_wfd_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the resume action is used in a WFD leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wfd"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].resume()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a WFD task, and it is not suitable to "
        "be resumed, please supply an OH or STOP task"
    )


# RTS
def test_resume_in_rts_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the resume action is used in a RTS leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].resume()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a RTS task, and it is not suitable to "
        "be resumed, please supply an OH or STOP task"
    )


# WIP
def test_resume_in_wip_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the resume action is used in a WIP leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_wip"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].resume()

    assert (
        str(cm.value) == "Test Task 3 (id:37) is a WIP task, and it is not suitable to "
        "be resumed, please supply an OH or STOP task"
    )


# PREV
def test_resume_in_prev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the resume action is used in a PREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_prev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].resume()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a PREV task, and it is not suitable to "
        "be resumed, please supply an OH or STOP task"
    )


# HREV
def test_resume_in_hrev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the resume action is used in a HREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_hrev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].resume()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a HREV task, and it is not suitable to "
        "be resumed, please supply an OH or STOP task"
    )


# DREV
def test_resume_in_drev_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the resume action is used in a DREV leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_drev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].resume()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a DREV task, and it is not suitable to "
        "be resumed, please supply an OH or STOP task"
    )


# OH: no dependency -> WIP
def test_resume_in_oh_leaf_task_with_no_dependencies(setup_task_status_workflow_tests):
    """resume action on a OH leaf task with no dependencies updates status to WIP."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_oh"]
    data["test_task3"].depends_on = []
    data["test_task3"].resume()
    # no time logs so it will return back to rts
    # the test is wrong in the first place (no way to turn a task with no
    # time logs in to a OH task),
    # but checks a situation that the system needs to be more robust
    assert data["test_task3"].status == data["status_rts"]


# OH: STOP dependencies -> WIP
def test_resume_in_oh_leaf_task_with_stop_dependencies(
    setup_task_status_workflow_tests,
):
    """resume action on a OH leaf task with STOP dependencies updates status to WIP."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    data["test_task3"].status = data["status_stop"]
    data["test_task9"].status = data["status_oh"]

    data["test_task9"].resume()
    assert data["test_task9"].status == data["status_wip"]


# OH: CMPL dependencies -> WIP
def test_resume_in_oh_leaf_task_with_cmpl_dependencies(
    setup_task_status_workflow_tests,
):
    """resume action on a OH leaf task with CMPL dependencies updates status to WIP."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    data["test_task3"].status = data["status_cmpl"]
    data["test_task9"].status = data["status_oh"]

    data["test_task9"].resume()
    assert data["test_task9"].status == data["status_wip"]


# STOP: no dependency -> WIP
def test_resume_in_stop_leaf_task_with_no_dependencies(
    setup_task_status_workflow_tests,
):
    """resume action on a STOP leaf task with no dependencies updates status to WIP."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_stop"]
    data["test_task3"].depends_on = []
    data["test_task3"].resume()
    # no time logs so it will return back to rts
    # the test is wrong in the first place (no way to turn a task with no
    # time logs in to a OH task),
    # but checks a situation that the system needs to be more robust
    assert data["test_task3"].status == data["status_rts"]


# STOP: STOP dependencies -> WIP
def test_resume_in_stop_leaf_task_with_stop_dependencies(
    setup_task_status_workflow_tests,
):
    """resume action on a STOP leaf task with STOP dep.s updates status to WIP."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    data["test_task3"].status = data["status_stop"]
    data["test_task9"].status = data["status_stop"]

    data["test_task9"].resume()
    assert data["test_task9"].status == data["status_wip"]


# STOP: CMPL dependencies -> WIP
def test_resume_in_stop_leaf_task_with_cmpl_dependencies(
    setup_task_status_workflow_tests,
):
    """resume action on a STOP leaf task with CMPL dep.s updates status to WIP."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    data["test_task3"].status = data["status_cmpl"]
    data["test_task9"].status = data["status_stop"]

    data["test_task9"].resume()
    assert data["test_task9"].status == data["status_wip"]


# CMPL
def test_resume_in_cmpl_leaf_task(setup_task_status_workflow_tests):
    """StatusError raised if the resume action is used in a CMPL leaf task."""
    data = setup_task_status_workflow_tests
    data["test_task3"].status = data["status_drev"]
    data["test_task3"].id = 37
    with pytest.raises(StatusError) as cm:
        data["test_task3"].resume()

    assert (
        str(cm.value)
        == "Test Task 3 (id:37) is a DREV task, and it is not suitable to "
        "be resumed, please supply an OH or STOP task"
    )


def test_review_set_review_number_is_not_an_integer(setup_task_status_workflow_tests):
    """TypeError raised if the review_number arg is not an int in Task.review_set()."""
    data = setup_task_status_workflow_tests
    with pytest.raises(TypeError) as cm:
        data["test_task3"].review_set("not an integer")

    assert (
        str(cm.value)
        == "review_number argument in Task.review_set should be a positive "
        "integer, not str: 'not an integer'"
    )


def test_review_set_review_number_is_a_negative_integer(
    setup_task_status_workflow_tests,
):
    """ValueError raised if the review_number is a negative number."""
    data = setup_task_status_workflow_tests
    with pytest.raises(ValueError) as cm:
        data["test_task3"].review_set(-10)

    assert (
        str(cm.value)
        == "review_number argument in Task.review_set should be a positive "
        "integer, not -10"
    )


def test_review_set_review_number_is_zero(setup_task_status_workflow_tests):
    """ValueError raised if the review_number is zero."""
    data = setup_task_status_workflow_tests
    with pytest.raises(ValueError) as cm:
        data["test_task3"].review_set(0)

    assert (
        str(cm.value)
        == "review_number argument in Task.review_set should be a positive "
        "integer, not 0"
    )


def test_leaf_drev_task_with_no_dependency_and_no_timelogs_update_status_with_dependent_statuses_fixes_status(
    setup_task_status_workflow_tests,
):
    """Task.update_status_with_dependent_statuses() fixes status of a leaf DREV task
    with no deps. (something went wrong) to RTS if there is no TimeLog and to WIP if
    there is a TimeLog.
    """
    data = setup_task_status_workflow_tests
    # use task6 and task5
    data["test_task5"].depends_on = []

    # set the statuses
    data["test_task5"].status = data["status_drev"]

    assert data["status_drev"] == data["test_task5"].status

    # fix status with dependencies
    data["test_task5"].update_status_with_dependent_statuses()

    # check the status
    assert data["status_rts"] == data["test_task5"].status


def test_leaf_drev_task_with_no_dependency_but_with_timelogs_update_status_with_dependent_statuses_fixes_status(
    setup_task_status_workflow_tests,
):
    """Task.update_status_with_dependent_statuses() will fix the status of a leaf DREV
    task with no dependency (something went wrong) to RTS if there is no TimeLog and to
    WIP if there is a TimeLog.
    """
    data = setup_task_status_workflow_tests
    # use task6 and task5
    data["test_task5"].depends_on = []

    # create some time logs for
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    data["test_task5"].create_time_log(
        resource=data["test_task5"].resources[0], start=now, end=now + td(hours=1)
    )

    # set the statuses
    data["test_task5"].status = data["status_drev"]

    assert data["status_drev"] == data["test_task5"].status

    # fix status with dependencies
    data["test_task5"].update_status_with_dependent_statuses()

    # check the status
    assert data["status_wip"] == data["test_task5"].status


def test_leaf_wip_task_with_no_dependency_and_no_timelogs_update_status_with_dependent_statuses_fixes_status(
    setup_task_status_workflow_tests,
):
    """Task.update_status_with_dependent_statuses() will fix the status of a leaf WIP
    task with no dependency (something went wrong) to RTS if there is no TimeLog and to
    WIP if there is a TimeLog.
    """
    data = setup_task_status_workflow_tests
    # use task6 and task5
    data["test_task5"].depends_on = []

    # check if there is no time logs
    assert data["test_task5"].time_logs == []

    # set the statuses
    data["test_task5"].status = data["status_wip"]

    assert data["status_wip"] == data["test_task5"].status

    # fix status with dependencies
    data["test_task5"].update_status_with_dependent_statuses()

    # check the status
    assert data["status_rts"] == data["test_task5"].status


def test_container_task_update_status_with_dependent_status_will_skip(
    setup_task_status_workflow_tests,
):
    """update_status_with_dependent_status() will skip container tasks."""
    data = setup_task_status_workflow_tests
    # the following should do nothing
    data["test_task1"].update_status_with_dependent_statuses()


def test_update_status_with_children_statuses_with_leaf_task(
    setup_task_status_workflow_tests,
):
    """update_status_with_children_statuses will skip leaf tasks."""
    data = setup_task_status_workflow_tests
    # the following should do nothing
    data["test_task4"].update_status_with_children_statuses()


@pytest.fixture(scope="function")
def setup_task_status_workflow_db_tests(setup_postgresql_db):
    """Set up the Task status workflow tests with a database."""
    data = dict()

    # test users
    data["test_user1"] = User(
        name="Test User 1", login="tuser1", email="tuser1@test.com", password="secret"
    )
    DBSession.add(data["test_user1"])

    data["test_user2"] = User(
        name="Test User 2", login="tuser2", email="tuser2@test.com", password="secret"
    )
    DBSession.add(data["test_user2"])

    # create a couple of tasks
    data["status_new"] = Status.query.filter_by(code="NEW").first()
    data["status_wfd"] = Status.query.filter_by(code="WFD").first()
    data["status_rts"] = Status.query.filter_by(code="RTS").first()
    data["status_wip"] = Status.query.filter_by(code="WIP").first()
    data["status_prev"] = Status.query.filter_by(code="PREV").first()
    data["status_hrev"] = Status.query.filter_by(code="HREV").first()
    data["status_drev"] = Status.query.filter_by(code="DREV").first()
    data["status_oh"] = Status.query.filter_by(code="OH").first()
    data["status_stop"] = Status.query.filter_by(code="STOP").first()
    data["status_cmpl"] = Status.query.filter_by(code="CMPL").first()

    data["status_rrev"] = Status.query.filter_by(code="RREV").first()
    data["status_app"] = Status.query.filter_by(code="APP").first()

    # repository
    data["test_repo"] = Repository(
        name="Test Repository",
        code="TR",
        linux_path="/mnt/T/",
        windows_path="T:/",
        macos_path="/Volumes/T",
    )
    DBSession.add(data["test_repo"])

    # proj1
    data["test_project1"] = Project(
        name="Test Project 1",
        code="TProj1",
        repository=data["test_repo"],
        start=datetime.datetime(2013, 6, 20, 0, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, 0, tzinfo=pytz.utc),
    )
    DBSession.add(data["test_project1"])

    # root tasks
    data["test_task1"] = Task(
        name="Test Task 1",
        project=data["test_project1"],
        responsible=[data["test_user1"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )
    DBSession.add(data["test_task1"])

    data["test_task2"] = Task(
        name="Test Task 2",
        project=data["test_project1"],
        responsible=[data["test_user1"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )
    DBSession.add(data["test_task2"])

    data["test_task3"] = Task(
        name="Test Task 3",
        project=data["test_project1"],
        resources=[data["test_user1"], data["test_user2"]],
        responsible=[data["test_user1"], data["test_user2"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )
    DBSession.add(data["test_task3"])

    # children tasks

    # children of data["test_task1"]
    data["test_task4"] = Task(
        name="Test Task 4",
        parent=data["test_task1"],
        status=data["status_wfd"],
        resources=[data["test_user1"]],
        depends_on=[data["test_task3"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )
    DBSession.add(data["test_task4"])

    data["test_task5"] = Task(
        name="Test Task 5",
        parent=data["test_task1"],
        resources=[data["test_user1"]],
        depends_on=[data["test_task4"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )
    DBSession.add(data["test_task5"])

    data["test_task6"] = Task(
        name="Test Task 6",
        parent=data["test_task1"],
        resources=[data["test_user1"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )
    DBSession.add(data["test_task6"])

    # children of data["test_task2"]
    data["test_task7"] = Task(
        name="Test Task 7",
        parent=data["test_task2"],
        resources=[data["test_user2"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )
    DBSession.add(data["test_task7"])

    data["test_task8"] = Task(
        name="Test Task 8",
        parent=data["test_task2"],
        resources=[data["test_user2"]],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )
    DBSession.add(data["test_task8"])

    # create an asset in between
    data["test_asset1"] = Asset(
        name="Test Asset 1",
        code="TA1",
        parent=data["test_task7"],
        type=Type(
            name="Character",
            code="Char",
            target_entity_type="Asset",
        ),
    )
    DBSession.add(data["test_asset1"])

    # new task under asset
    data["test_task9"] = Task(
        name="Test Task 9",
        parent=data["test_asset1"],
        start=datetime.datetime(2013, 6, 20, 0, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc),
        resources=[data["test_user2"]],
        schedule_timing=10,
        schedule_unit=TimeUnit.Day,
        schedule_model=ScheduleModel.Effort,
    )
    DBSession.add(data["test_task9"])
    DBSession.commit()

    # --------------
    # Task Hierarchy
    # --------------
    #
    # +-> Test Task 1
    # |   |
    # |   +-> Test Task 4
    # |   |
    # |   +-> Test Task 5
    # |   |
    # |   +-> Test Task 6
    # |
    # +-> Test Task 2
    # |   |
    # |   +-> Test Task 7
    # |   |   |
    # |   |   +-> Test Asset 1
    # |   |       |
    # |   |       +-> Test Task 9
    # |   |
    # |   +-> Test Task 8
    # |
    # +-> Test Task 3

    # no children for data["test_task3"]
    data["all_tasks"] = [
        data["test_task1"],
        data["test_task2"],
        data["test_task3"],
        data["test_task4"],
        data["test_task5"],
        data["test_task6"],
        data["test_task7"],
        data["test_task8"],
        data["test_task9"],
        data["test_asset1"],
    ]
    return data


def test_container_rts_task_updated_to_have_a_dependency_of_cmpl_task(
    setup_task_status_workflow_db_tests,
):
    """set dependency between an RTS container task to a CMPL task and will stay RTS."""
    data = setup_task_status_workflow_db_tests
    # make a task with CMPL status
    data["test_task3"].depends_on = []
    data["test_task3"].children.append(data["test_task6"])

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    data["test_task8"].create_time_log(
        resource=data["test_task8"].resources[0], start=now, end=now + td(hours=1)
    )

    reviews = data["test_task8"].request_review()
    for review in reviews:
        review.approve()

    assert data["test_task8"].status == data["status_cmpl"]

    # find a RTS container task
    assert data["test_task3"].status == data["status_rts"]

    # create dependency
    data["test_task3"].depends_on.append(data["test_task8"])
    assert data["test_task3"].status == data["status_rts"]


# WIP: review instances
def test_request_review_in_wip_leaf_task_review_instances(
    setup_task_status_workflow_db_tests,
):
    """request_review action returns reviews for each responsible on a WIP leaf task."""
    data = setup_task_status_workflow_db_tests
    data["test_task3"].responsible = [data["test_user1"], data["test_user2"]]
    data["test_task3"].status = data["status_wip"]
    reviews = data["test_task3"].request_review()
    assert len(reviews) == 2
    assert isinstance(reviews[0], Review)
    assert isinstance(reviews[1], Review)


# WIP: review instances review_number is correct
def test_request_review_in_wip_leaf_task_review_instances_review_number(
    setup_task_status_workflow_db_tests,
):
    """review_number attribute of the created Reviews are correctly set."""
    data = setup_task_status_workflow_db_tests
    data["test_task3"].responsible = [data["test_user1"], data["test_user2"]]
    data["test_task3"].status = data["status_wip"]

    # request a review
    reviews = data["test_task3"].request_review()
    review1 = reviews[0]
    review2 = reviews[1]
    assert review1.review_number == 1
    assert review2.review_number == 1

    # finalize reviews
    review1.approve()
    review2.approve()

    # request a revision
    review3 = data["test_task3"].request_revision(
        reviewer=data["test_user1"],
        description="some description",
        schedule_timing=1,
        schedule_unit=TimeUnit.Day,
    )

    # the new_review.revision number still should be 1
    assert review3.review_number == 2

    # and then ask a review again
    data["test_task3"].status = data["status_wip"]

    reviews = data["test_task3"].request_review()
    assert reviews[0].review_number == 3
    assert reviews[1].review_number == 3


# WIP: status updated to PREV
def test_request_review_in_wip_leaf_task_status_updated_to_prev(
    setup_task_status_workflow_db_tests,
):
    """request_review action updates WIP leaf task to PREV."""
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]
    data["test_task3"].request_review()
    assert data["test_task3"].status == data["status_prev"]


# CMPL: dependent task dependency_target update CMPL -> DREV
def test_request_revision_in_cmpl_leaf_task_cmpl_dependent_task_dependency_target_updated_to_onstart(
    setup_task_status_workflow_db_tests,
):
    """dependency_target attribute of the TaskDependency object between the revised task
    and the dependent CMPL task set to 'onstart' if the request_revision action is used
    in a CMPL leaf task.
    """
    data = setup_task_status_workflow_db_tests
    # create a couple of TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    # remove any TaskDependency instances
    # for i in TaskDependency.query.all():
    #     DBSession.delete(i)
    #
    # DBSession.commit()

    data["test_task3"].depends_on = [data["test_task9"]]  # PREV
    data["test_task4"].depends_on = [data["test_task9"]]  # HREV
    data["test_task5"].depends_on = [data["test_task9"]]  # STOP
    data["test_task6"].depends_on = [data["test_task9"]]  # OH
    data["test_task8"].depends_on = [data["test_task9"]]  # DREV
    assert data["test_task9"] in data["test_task5"].depends_on
    assert data["test_task9"] in data["test_task6"].depends_on
    assert data["test_task9"] in data["test_task8"].depends_on

    data["test_task9"].status = data["status_rts"]
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0], start=now, end=now + td(hours=1)
    )
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    reviews = data["test_task9"].request_review()
    for r in reviews:
        r.approve()
    assert data["test_task9"].status == data["status_cmpl"]
    assert data["test_task8"].status == data["status_rts"]

    data["test_task8"].create_time_log(
        resource=data["test_task8"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )
    assert data["test_task8"].status == data["status_wip"]

    [r.approve() for r in data["test_task8"].request_review()]
    assert data["test_task8"].status == data["status_cmpl"]

    # now work on task5
    data["test_task5"].create_time_log(
        resource=data["test_task5"].resources[0],
        start=now + td(hours=3),
        end=now + td(hours=4),
    )
    assert data["test_task5"].status == data["status_wip"]
    data["test_task5"].hold()
    assert data["test_task5"].status == data["status_oh"]

    # now work on task6
    data["test_task6"].create_time_log(
        resource=data["test_task6"].resources[0],
        start=now + td(hours=4),
        end=now + td(hours=5),
    )
    assert data["test_task6"].status == data["status_wip"]
    data["test_task6"].stop()
    assert data["test_task6"].status == data["status_stop"]

    # now work on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=5),
        end=now + td(hours=6),
    )
    assert data["test_task3"].status == data["status_wip"]
    data["test_task3"].request_review()
    assert data["test_task3"].status == data["status_prev"]

    # now work on task4
    data["test_task4"].create_time_log(
        resource=data["test_task4"].resources[0],
        start=now + td(hours=6),
        end=now + td(hours=7),
    )
    assert data["test_task4"].status == data["status_wip"]
    reviews = data["test_task4"].request_review()
    DBSession.add_all(reviews)
    DBSession.commit()

    assert data["test_task4"].status == data["status_prev"]
    for r in reviews:
        r.request_revision(schedule_timing=1, schedule_unit=TimeUnit.Hour)
    assert data["test_task4"].status == data["status_hrev"]

    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": TimeUnit.Hour,
    }
    data["test_task9"].request_revision(**kw)

    tdep_t3 = (
        TaskDependency.query.filter_by(task=data["test_task3"])
        .filter_by(depends_on=data["test_task9"])
        .first()
    )
    tdep_t4 = (
        TaskDependency.query.filter_by(task=data["test_task4"])
        .filter_by(depends_on=data["test_task9"])
        .first()
    )
    tdep_t5 = (
        TaskDependency.query.filter_by(task=data["test_task5"])
        .filter_by(depends_on=data["test_task9"])
        .first()
    )
    tdep_t6 = (
        TaskDependency.query.filter_by(task=data["test_task6"])
        .filter_by(depends_on=data["test_task9"])
        .first()
    )
    tdep_t8 = (
        TaskDependency.query.filter_by(task=data["test_task8"])
        .filter_by(depends_on=data["test_task9"])
        .first()
    )
    assert tdep_t3 is not None
    assert tdep_t4 is not None
    assert tdep_t5 is not None
    assert tdep_t6 is not None
    assert tdep_t8 is not None
    assert tdep_t3.dependency_target == "onstart"
    assert tdep_t4.dependency_target == "onstart"
    assert tdep_t5.dependency_target == "onstart"
    assert tdep_t6.dependency_target == "onstart"
    assert tdep_t8.dependency_target == "onstart"


# CMPL: dependent task status update CMPL -> DREV
def test_request_revision_in_cmpl_leaf_task_cmpl_dependent_task_updated_to_drev(
    setup_task_status_workflow_db_tests,
):
    """status of the dependent CMPL task set to DREV
    if the request_revision action is used in a CMPL leaf task
    """
    data = setup_task_status_workflow_db_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task8"].depends_on = [data["test_task9"]]
    assert data["test_task9"] in data["test_task8"].depends_on

    data["test_task9"].status = data["status_rts"]
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0], start=now, end=now + td(hours=1)
    )
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    reviews = data["test_task9"].request_review()
    for r in reviews:
        r.approve()
    assert data["test_task9"].status == data["status_cmpl"]
    assert data["test_task8"].status == data["status_rts"]

    data["test_task8"].create_time_log(
        resource=data["test_task8"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )
    assert data["test_task8"].status == data["status_wip"]

    [r.approve() for r in data["test_task8"].request_review()]
    assert data["test_task8"].status == data["status_cmpl"]

    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": TimeUnit.Hour,
    }
    data["test_task9"].request_revision(**kw)

    assert data["test_task9"].status == data["status_hrev"]
    assert data["test_task8"].status == data["status_drev"]


# CMPL: dependent task parent status updated to WIP
def test_request_revision_in_cmpl_leaf_task_dependent_task_parent_status_updated_to_wip(
    setup_task_status_workflow_db_tests,
):
    """status of the dependent task parent updated to WIP
    if the request_revision action is used in a CMPL leaf task
    """
    data = setup_task_status_workflow_db_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task9"].depends_on = [data["test_task8"]]
    data["test_task9"].status = data["status_wfd"]
    data["test_asset1"].status = data["status_wfd"]
    data["test_task8"].status = data["status_rts"]

    data["test_task8"].create_time_log(
        resource=data["test_task8"].resources[0], start=now, end=now + td(hours=1)
    )
    data["test_task8"].create_time_log(
        resource=data["test_task8"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    data["test_task8"].status = data["status_cmpl"]
    data["test_task9"].status = data["status_cmpl"]
    data["test_asset1"].status = data["status_cmpl"]
    data["test_task7"].status = data["status_cmpl"]

    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": TimeUnit.Hour,
    }
    review = data["test_task8"].request_revision(**kw)

    assert data["test_task9"].status == data["status_drev"]
    assert data["test_asset1"].status == data["status_wip"]
    assert data["test_task7"].status == data["status_wip"]


# CMPL: parent status update
def test_request_revision_in_cmpl_leaf_task_parent_status_updated_to_wip(
    setup_task_status_workflow_db_tests,
):
    """status of the parent set to WIP if the
    request_revision action is used in a CMPL leaf task
    """
    data = setup_task_status_workflow_db_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task9"].status = data["status_rts"]
    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    data["test_task9"].status = data["status_cmpl"]
    data["test_asset1"].status = data["status_cmpl"]

    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": TimeUnit.Hour,
    }
    review = data["test_task9"].request_revision(**kw)
    assert data["test_asset1"].status == data["status_wip"]


# CMPL: dependent task status update RTS -> WFD
def test_request_revision_in_cmpl_leaf_task_rts_dependent_task_updated_to_wfd(
    setup_task_status_workflow_db_tests,
):
    """status of the dependent RTS task set to WFD
    if the request_revision action is used in a CMPL leaf task
    """
    data = setup_task_status_workflow_db_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task8"].depends_on = [data["test_task9"]]
    data["test_task8"].status = data["status_wfd"]

    data["test_task9"].status = data["status_rts"]
    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    data["test_task9"].status = data["status_cmpl"]

    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": TimeUnit.Hour,
    }
    review = data["test_task9"].request_revision(**kw)
    assert data["test_task8"].status == data["status_wfd"]


# CMPL: schedule info update
def test_request_revision_in_cmpl_leaf_task_schedule_info_update(
    setup_task_status_workflow_db_tests,
):
    """timing values are extended with the supplied values
    if the request_revision action is used in a CMPL leaf task
    """
    data = setup_task_status_workflow_db_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task3"].status = data["status_rts"]
    tlog0 = data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0], start=now, end=now + td(hours=1)
    )
    DBSession.add(tlog0)
    tlog1 = data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )
    DBSession.add(tlog1)
    DBSession.commit()
    assert data["test_task3"].total_logged_seconds == 7200

    reviews = data["test_task3"].request_review()
    review1 = reviews[0]
    review2 = reviews[1]
    review1.approve()
    review2.approve()

    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": TimeUnit.Hour,
    }
    revision = data["test_task3"].request_revision(**kw)
    DBSession.add(revision)
    assert data["test_task3"].schedule_timing == 6
    assert data["test_task3"].schedule_unit == TimeUnit.Hour


# CMPL: status update
def test_request_revision_in_cmpl_leaf_task_status_updated_to_hrev(
    setup_task_status_workflow_db_tests,
):
    """status set to HREV and the timing values are
    extended with the supplied values if the request_revision action is
    used in a CMPL leaf task
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_cmpl"]
    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": TimeUnit.Hour,
    }
    review = data["test_task3"].request_revision(**kw)
    assert data["test_task3"].status == data["status_hrev"]


# CMPL: dependent task status update WIP -> DREV
def test_request_revision_in_cmpl_leaf_task_wip_dependent_task_updated_to_drev(
    setup_task_status_workflow_db_tests,
):
    """status of the dependent WIP task set to DREV
    if the request_revision action is used in a CMPL leaf task
    """
    data = setup_task_status_workflow_db_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task8"].depends_on = [data["test_task9"]]
    data["test_task8"].status = data["status_wip"]

    data["test_task9"].status = data["status_rts"]
    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now,
        end=now + td(hours=1),
    )
    TimeLog(
        task=data["test_task9"],
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    data["test_task9"].status = data["status_cmpl"]

    kw = {
        "reviewer": data["test_user1"],
        "description": "do something uleyn",
        "schedule_timing": 4,
        "schedule_unit": TimeUnit.Hour,
    }
    review = data["test_task9"].request_revision(**kw)
    assert data["test_task8"].status == data["status_drev"]


def test_request_revision_in_deeper_dependency_setup(
    setup_task_status_workflow_db_tests,
):
    """all the dependent task statuses are updated to DREV."""
    data = setup_task_status_workflow_db_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    # # remove any TaskDependency instances
    # for i in TaskDependency.query.all():
    #     DBSession.delete(i)
    # DBSession.commit()

    data["test_task5"].depends_on = []
    data["test_task6"].depends_on = [data["test_task5"]]
    data["test_task3"].depends_on = [data["test_task6"]]
    data["test_task8"].depends_on = [data["test_task3"]]
    data["test_task9"].depends_on = [data["test_task8"]]

    data["test_task5"].update_status_with_dependent_statuses()
    data["test_task6"].update_status_with_dependent_statuses()
    data["test_task3"].update_status_with_dependent_statuses()
    data["test_task8"].update_status_with_dependent_statuses()
    data["test_task9"].update_status_with_dependent_statuses()

    assert data["test_task5"].status == data["status_rts"]
    assert data["test_task6"].status == data["status_wfd"]
    assert data["test_task3"].status == data["status_wfd"]
    assert data["test_task3"].status == data["status_wfd"]
    assert data["test_task3"].status == data["status_wfd"]
    # DBSession.commit()

    # complete each of them first
    # test_task5
    data["test_task5"].create_time_log(
        data["test_task5"].resources[0], now - td(hours=1), now
    )
    data["test_task5"].schedule_timing = 1
    data["test_task5"].schedule_unit = TimeUnit.Hour
    data["test_task5"].status = data["status_cmpl"]

    # test_task6
    data["test_task6"].status = data["status_rts"]
    data["test_task6"].create_time_log(
        data["test_task6"].resources[0], now, now + td(hours=1)
    )
    data["test_task6"].schedule_timing = 1
    data["test_task6"].schedule_unit = TimeUnit.Hour
    data["test_task6"].status = data["status_cmpl"]

    # test_task3
    data["test_task3"].status = data["status_rts"]
    data["test_task3"].create_time_log(
        data["test_task3"].resources[0], now + td(hours=1), now + td(hours=2)
    )
    data["test_task3"].schedule_timing = 1
    data["test_task3"].schedule_unit = TimeUnit.Hour
    data["test_task3"].status = data["status_cmpl"]

    # test_task8
    data["test_task8"].status = data["status_rts"]
    data["test_task8"].create_time_log(
        data["test_task8"].resources[0], now + td(hours=2), now + td(hours=3)
    )
    data["test_task8"].schedule_timing = 1
    data["test_task8"].schedule_unit = TimeUnit.Hour
    data["test_task8"].status = data["status_cmpl"]

    # test_task9
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].create_time_log(
        data["test_task9"].resources[0], now + td(hours=3), now + td(hours=4)
    )
    data["test_task9"].schedule_timing = 1
    data["test_task9"].schedule_unit = TimeUnit.Hour
    data["test_task9"].status = data["status_cmpl"]

    # now request a revision to the first task (test_task6)
    # and expect all of the task dependency targets to be turned
    # in to "onstart"
    data["test_task6"].request_revision(data["test_user1"])

    assert data["test_task6"].task_depends_on[0].dependency_target == "onend"
    assert data["test_task3"].task_depends_on[0].dependency_target == "onstart"
    assert data["test_task8"].task_depends_on[0].dependency_target == "onstart"
    assert data["test_task9"].task_depends_on[0].dependency_target == "onstart"


# PREV: Review instances statuses are updated
def test_request_revision_in_prev_leaf_task_new_review_instance_is_created(
    setup_task_status_workflow_db_tests,
):
    """statuses of review instances are correctly updated to
    RREV if the request_revision action is used in a PREV leaf task
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]

    reviews = data["test_task3"].request_review()
    new_review = data["test_task3"].request_revision(
        reviewer=data["test_user2"],
        description="some description",
        schedule_timing=1,
        schedule_unit=TimeUnit.Week,
    )
    assert isinstance(new_review, Review)


# PREV: Review instances statuses are updated
def test_request_revision_in_prev_leaf_task_review_instances_are_deleted(
    setup_task_status_workflow_db_tests,
):
    """NEW Review instances are deleted if the
    request_revision action is used in a PREV leaf task
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]

    reviews = data["test_task3"].request_review()
    review1 = reviews[0]
    review2 = reviews[1]

    assert review1.status == data["status_new"]
    assert review2.status == data["status_new"]

    review3 = data["test_task3"].request_revision(
        reviewer=data["test_user2"],
        description="some description",
        schedule_timing=4,
        schedule_unit=TimeUnit.Hour,
    )

    # now check if the review instances are not in task3.reviews list
    # anymore
    assert review1 not in data["test_task3"].reviews
    assert review2 not in data["test_task3"].reviews
    assert review3 in data["test_task3"].reviews


# PREV: Schedule info update also consider RREV Reviews
def test_request_revision_in_prev_leaf_task_schedule_info_update_also_considers_other_rrev_reviews_with_same_review_number(
    setup_task_status_workflow_db_tests,
):
    """timing values are extended with the supplied values
    and also any RREV Review timings with the same revision number are
    included if the request_revision action is used in a PREV leaf task
    """
    data = setup_task_status_workflow_db_tests
    # create a couple TimeLogs
    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    data["test_task3"].status = data["status_rts"]
    data["test_task3"].responsible = [data["test_user1"], data["test_user2"]]

    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0], start=now, end=now + td(hours=1)
    )
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # check the status
    assert data["test_task3"].status == data["status_wip"]

    # first request a review
    reviews = data["test_task3"].request_review()

    # only finalize the first review
    review1 = reviews[0]
    review2 = reviews[1]

    review1.request_revision(
        schedule_timing=6, schedule_unit=TimeUnit.Hour, description=""
    )

    # now request_revision using the task
    review3 = data["test_task3"].request_revision(
        reviewer=data["test_user1"],
        description="do something uleyn",
        schedule_timing=4,
        schedule_unit=TimeUnit.Hour,
    )
    assert len(data["test_task3"].reviews) == 2

    # check if they are in the same review set
    assert review1.review_number == review3.review_number

    # the final timing should be 12 hours
    assert data["test_task3"].schedule_timing == 10
    assert data["test_task3"].schedule_unit == TimeUnit.Day


# PREV: Status updated to HREV
def test_request_revision_in_prev_leaf_task_status_updated_to_hrev(
    setup_task_status_workflow_db_tests,
):
    """the status of the PREV leaf task converted to
    HREV if the request_revision action is used in a PREV leaf task
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_prev"]

    reviewer = data["test_user1"]
    description = "do something uleyn"
    schedule_timing = 4
    schedule_unit = TimeUnit.Hour

    data["test_task3"].request_revision(
        reviewer=reviewer,
        description=description,
        schedule_timing=schedule_timing,
        schedule_unit=schedule_unit,
    )
    assert data["test_task3"].status == data["status_hrev"]


# PREV: Schedule info update
def test_request_revision_in_prev_leaf_task_timing_is_extended(
    setup_task_status_workflow_db_tests,
):
    """timing extended as stated in the action when
    the request_revision action is used in a PREV leaf task
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_prev"]

    reviewer = data["test_user1"]
    description = "do something uleyn"
    schedule_timing = 4
    schedule_unit = "h"

    data["test_task3"].request_revision(
        reviewer=reviewer,
        description=description,
        schedule_timing=schedule_timing,
        schedule_unit=schedule_unit,
    )
    assert data["test_task3"].schedule_timing == 10
    assert data["test_task3"].schedule_unit == TimeUnit.Day


# OH: DREV dependencies -> DREV
def test_resume_in_oh_leaf_task_with_drev_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to DREV if the resume action
    is used in a OH leaf task with DREV dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task6"].status = data["status_rts"]
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]
    data["test_task3"].depends_on = [data["test_task6"]]

    # check statuses
    assert data["test_task6"].status == data["status_rts"]
    assert data["test_task3"].status == data["status_wfd"]
    assert data["test_task9"].status == data["status_wfd"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    data["test_task6"].create_time_log(
        resource=data["test_task6"].resources[0], start=now, end=now + td(hours=1)
    )

    # approve task6
    reviews = data["test_task6"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task6"].status == data["status_cmpl"]
    assert data["test_task3"].status == data["status_rts"]
    assert data["test_task9"].status == data["status_wfd"]

    # start working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # approve task3
    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task6"].status == data["status_cmpl"]
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_rts"]

    # start working on task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )

    # check statuses
    assert data["test_task6"].status == data["status_cmpl"]
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_wip"]

    # hold task9
    data["test_task9"].hold()

    # check statuses
    assert data["test_task6"].status == data["status_cmpl"]
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_oh"]

    # request a revision to task6
    data["test_task6"].request_revision(reviewer=data["test_user1"])

    # check statuses
    assert data["test_task6"].status == data["status_hrev"]
    assert data["test_task3"].status == data["status_drev"]
    assert data["test_task9"].status == data["status_oh"]

    # resume task9
    data["test_task9"].resume()

    # check statuses
    assert data["test_task6"].status == data["status_hrev"]
    assert data["test_task3"].status == data["status_drev"]
    assert data["test_task9"].status == data["status_drev"]


# OH: HREV dependencies -> DREV
def test_resume_in_oh_leaf_task_with_hrev_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to DREV if the resume action
    is used in a OH leaf task with HREV dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0], start=now, end=now + td(hours=1)
    )

    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    # task3 should be cmpl
    assert data["test_task3"].status == data["status_cmpl"]

    # start working on task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # now continue working on test_task3
    data["test_task3"].request_revision(reviewer=data["test_task3"].resources[0])

    # check statuses
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_drev"]

    # hold task9
    data["test_task9"].hold()
    assert data["test_task9"].status == data["status_oh"]

    # resume task9
    data["test_task9"].resume()
    assert data["test_task9"].status == data["status_drev"]


# OH: OH dependencies -> DREV
def test_resume_in_oh_leaf_task_with_oh_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to WIP if the resume action
    is used in a OH leaf task with OH dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]

    # finish task3 first
    now = datetime.datetime.now(pytz.utc)
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now,
        end=now + datetime.timedelta(hours=1),
    )
    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    data["test_task9"].depends_on = [data["test_task3"]]

    # start working for task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + datetime.timedelta(hours=1),
        end=now + datetime.timedelta(hours=2),
    )

    # now request a revision for task3
    data["test_task3"].request_revision(reviewer=data["test_user1"])
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_drev"]

    # enter a new time log for task3 to make it wip
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + datetime.timedelta(hours=3),
        end=now + datetime.timedelta(hours=4),
    )

    # and hold task3 and task9
    data["test_task9"].hold()
    data["test_task3"].hold()

    assert data["test_task3"].status == data["status_oh"]
    assert data["test_task9"].status == data["status_oh"]

    data["test_task9"].resume()
    assert data["test_task9"].status == data["status_drev"]


# OH: PREV dependencies -> DREV
def test_resume_in_oh_leaf_task_with_prev_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to DREV if the resume action
    is used in a OH leaf task with PREV dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    # check statuses
    assert data["test_task3"].status == data["status_rts"]
    assert data["test_task9"].status == data["status_wfd"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    # start working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0], start=now, end=now + td(hours=1)
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_wfd"]

    # complete task3
    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_rts"]

    # start working on task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_wip"]

    # hold task9
    data["test_task9"].hold()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_oh"]

    # request a revision to task3
    data["test_task3"].request_revision(reviewer=data["test_user1"])

    # check statuses
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_oh"]

    # now continue working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_oh"]

    # request a review for task3
    data["test_task3"].request_review()

    # check statuses
    assert data["test_task3"].status == data["status_prev"]
    assert data["test_task9"].status == data["status_oh"]

    # now resume task9
    data["test_task9"].resume()

    # check statuses
    assert data["test_task3"].status == data["status_prev"]
    assert data["test_task9"].status == data["status_drev"]


# OH: WIP dependencies -> DREV
def test_resume_in_oh_leaf_task_with_wip_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to DREV if the resume action
    is used in a OH leaf task with WIP dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    # check statuses
    assert data["test_task3"].status == data["status_rts"]
    assert data["test_task9"].status == data["status_wfd"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    # start working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0], start=now, end=now + td(hours=1)
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_wfd"]

    # complete task3
    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_rts"]

    # start working on task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_wip"]

    # hold task9
    data["test_task9"].hold()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_oh"]

    # request a revision to task3
    data["test_task3"].request_revision(reviewer=data["test_user1"])

    # check statuses
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_oh"]

    # now continue working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_oh"]

    # now resume task9
    data["test_task9"].resume()

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_drev"]


# STOP: DREV dependencies -> DREV
def test_resume_in_stop_leaf_task_with_drev_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to DREV if the resume action
    is used in a STOP leaf task with DREV dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task6"].status = data["status_rts"]
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]
    data["test_task3"].depends_on = [data["test_task6"]]

    # check statuses
    assert data["test_task6"].status == data["status_rts"]
    assert data["test_task3"].status == data["status_wfd"]
    assert data["test_task9"].status == data["status_wfd"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    data["test_task6"].create_time_log(
        resource=data["test_task6"].resources[0], start=now, end=now + td(hours=1)
    )

    # approve task6
    reviews = data["test_task6"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task6"].status == data["status_cmpl"]
    assert data["test_task3"].status == data["status_rts"]
    assert data["test_task9"].status == data["status_wfd"]

    # start working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # approve task3
    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task6"].status == data["status_cmpl"]
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_rts"]

    # start working on task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )

    # check statuses
    assert data["test_task6"].status == data["status_cmpl"]
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_wip"]

    # stop task9
    data["test_task9"].stop()

    # check statuses
    assert data["test_task6"].status == data["status_cmpl"]
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_stop"]

    # request a revision to task6
    data["test_task6"].request_revision(reviewer=data["test_user1"])

    # check statuses
    assert data["test_task6"].status == data["status_hrev"]
    assert data["test_task3"].status == data["status_drev"]
    assert data["test_task9"].status == data["status_stop"]

    # resume task9
    data["test_task9"].resume()

    # check statuses
    assert data["test_task6"].status == data["status_hrev"]
    assert data["test_task3"].status == data["status_drev"]
    assert data["test_task9"].status == data["status_drev"]


# STOP: HREV dependencies -> DREV
def test_resume_in_stop_leaf_task_with_hrev_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to DREV if the resume action
    is used in a STOP leaf task with HREV dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    # check statuses
    assert data["test_task3"].status == data["status_rts"]
    assert data["test_task9"].status == data["status_wfd"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    # start working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0], start=now, end=now + td(hours=1)
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_wfd"]

    # complete task3
    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_rts"]

    # start working on task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_wip"]

    # stop task9
    data["test_task9"].stop()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_stop"]

    # request a revision to task3
    data["test_task3"].request_revision(reviewer=data["test_user1"])

    # check statuses
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_stop"]

    # now continue working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_stop"]

    # request a review for task3
    reviews = data["test_task3"].request_review()

    # check statuses
    assert data["test_task3"].status == data["status_prev"]
    assert data["test_task9"].status == data["status_stop"]

    # request revisions
    for r in reviews:
        r.request_revision()

    # check statuses
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_stop"]

    # now resume task9
    data["test_task9"].resume()

    # check statuses
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_drev"]


# STOP: OH dependencies -> DREV
def test_resume_in_stop_leaf_task_with_oh_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to WIP if the resume action
    is used in a STOP leaf task with OH dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    # check statuses
    assert data["test_task3"].status == data["status_rts"]
    assert data["test_task9"].status == data["status_wfd"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    # start working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0], start=now, end=now + td(hours=1)
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_wfd"]

    # complete task3
    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_rts"]

    # start working on task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_wip"]

    # stop task9
    data["test_task9"].stop()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_stop"]

    # request a revision to task3
    data["test_task3"].request_revision(reviewer=data["test_user1"])

    # check statuses
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_stop"]

    # now continue working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_stop"]

    # hold task3
    data["test_task3"].hold()

    # check statuses
    assert data["test_task3"].status == data["status_oh"]
    assert data["test_task9"].status == data["status_stop"]

    # now resume task9
    data["test_task9"].resume()

    # check statuses
    assert data["test_task3"].status == data["status_oh"]
    assert data["test_task9"].status == data["status_drev"]


# STOP: PREV dependencies -> DREV
def test_resume_in_stop_leaf_task_with_prev_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to DREV if the resume action
    is used in a STOP leaf task with PREV dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    # check statuses
    assert data["test_task3"].status == data["status_rts"]
    assert data["test_task9"].status == data["status_wfd"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    # start working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0], start=now, end=now + td(hours=1)
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_wfd"]

    # complete task3
    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_rts"]

    # start working on task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_wip"]

    # stop task9
    data["test_task9"].stop()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_stop"]

    # request a revision to task3
    data["test_task3"].request_revision(reviewer=data["test_user1"])

    # check statuses
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_stop"]

    # now continue working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_stop"]

    # request a review for task3
    data["test_task3"].request_review()

    # check statuses
    assert data["test_task3"].status == data["status_prev"]
    assert data["test_task9"].status == data["status_stop"]

    # now resume task9
    data["test_task9"].resume()

    # check statuses
    assert data["test_task3"].status == data["status_prev"]
    assert data["test_task9"].status == data["status_drev"]


# STOP: WIP dependencies -> DREV
def test_resume_in_stop_leaf_task_with_wip_dependencies(
    setup_task_status_workflow_db_tests,
):
    """status updated to DREV if the resume action
    is used in a STOP leaf task with WIP dependencies
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_rts"]
    data["test_task9"].status = data["status_rts"]
    data["test_task9"].depends_on = [data["test_task3"]]

    # check statuses
    assert data["test_task3"].status == data["status_rts"]
    assert data["test_task9"].status == data["status_wfd"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)

    # start working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0], start=now, end=now + td(hours=1)
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_wfd"]

    # complete task3
    reviews = data["test_task3"].request_review()
    for r in reviews:
        r.approve()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_rts"]

    # start working on task9
    data["test_task9"].create_time_log(
        resource=data["test_task9"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_wip"]

    # stop task9
    data["test_task9"].stop()

    # check statuses
    assert data["test_task3"].status == data["status_cmpl"]
    assert data["test_task9"].status == data["status_stop"]

    # request a revision to task3
    data["test_task3"].request_revision(reviewer=data["test_user1"])

    # check statuses
    assert data["test_task3"].status == data["status_hrev"]
    assert data["test_task9"].status == data["status_stop"]

    # now continue working on task3
    data["test_task3"].create_time_log(
        resource=data["test_task3"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_stop"]

    # now resume task9
    data["test_task9"].resume()

    # check statuses
    assert data["test_task3"].status == data["status_wip"]
    assert data["test_task9"].status == data["status_drev"]


def test_review_set_method_is_working_as_expected(setup_task_status_workflow_db_tests):
    """review_set() method is working as expected"""
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]

    # request a review
    reviews = data["test_task3"].request_review()
    DBSession.add_all(reviews)
    assert len(reviews) == 2

    # check the review_set() method with no review number
    assert data["test_task3"].review_set() == reviews

    # now finalize the reviews
    reviews[0].approve()
    reviews[1].request_revision()

    # task should have been set to hrev
    assert data["status_hrev"] == data["test_task3"].status

    # set the status to wip again
    data["test_task3"].status = data["status_wip"]

    # request a new set of reviews
    reviews2 = data["test_task3"].request_review()

    # confirm that they it is a different set of review
    assert reviews != reviews2

    # now check if review_set() will return reviews2
    assert data["test_task3"].review_set() == reviews2

    # and use a review_number
    assert data["test_task3"].review_set(1) == reviews

    assert data["test_task3"].review_set(2) == reviews2


def test_review_set_review_number_is_skipped(setup_task_status_workflow_db_tests):
    """latest review set returned if the
    review_number argument is skipped in Task.review_set() method
    """
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]

    # request a review
    reviews = data["test_task3"].request_review()
    DBSession.add_all(reviews)
    assert len(reviews) == 2

    # check the review_set() method with no review number
    assert data["test_task3"].review_set() == reviews

    # now finalize the reviews
    reviews[0].approve()
    reviews[1].request_revision()

    # task should have been set to hrev
    assert data["test_task3"].status == data["status_hrev"]

    # set the status to wip again
    data["test_task3"].status = data["status_wip"]

    # request a new set of reviews
    reviews2 = data["test_task3"].request_review()
    DBSession.add_all(reviews2)

    # confirm that it is a different set of review
    assert reviews != reviews2

    # now check if review_set() will return reviews2
    assert data["test_task3"].review_set() == reviews2


def test_request_review_version_arg_is_skipped(setup_task_status_workflow_db_tests):
    """request_review() version arg can be skipped."""
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]

    # request a review
    reviews = data["test_task3"].request_review()  # Version arg is skipped
    assert len(reviews) == 2


def test_request_review_version_arg_is_none(setup_task_status_workflow_db_tests):
    """request_review() version arg can be None."""
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]

    # request a review
    reviews = data["test_task3"].request_review(version=None)
    assert len(reviews) == 2


def test_request_review_version_arg_is_not_a_version_instance(
    setup_task_status_workflow_db_tests,
):
    """request_review() version arg is not a Version instance raises TypeError."""
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]

    # request a review
    with pytest.raises(TypeError) as cm:
        _ = data["test_task3"].request_review(version="Not a version instance")

    assert str(cm.value) == (
        "Review.version should be a Version instance, "
        "not str: 'Not a version instance'"
    )


def test_request_review_version_arg_is_not_related_to_the_task(
    setup_task_status_workflow_db_tests,
):
    """request_review() version arg is not related to the Task raises ValueError."""
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]
    version = Version(task=data["test_task2"])

    # request a review
    with pytest.raises(ValueError) as cm:
        _ = data["test_task3"].request_review(version=version)

    assert str(cm.value) == (
        f"Review.version should be a Version instance related to this Task: {version}"
    )


def test_request_review_accepts_version_instance(setup_task_status_workflow_db_tests):
    """request_review() a Version instance can be passed to it."""
    data = setup_task_status_workflow_db_tests
    data["test_task3"].status = data["status_wip"]
    version = Version(task=data["test_task3"])

    # request a review
    reviews = data["test_task3"].request_review(version=version)
    assert reviews[0].version == version
    assert reviews[1].version == version
