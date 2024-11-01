# -*- coding: utf-8 -*-
"""Tests for the EntityGroup class."""

import pytest

from stalker import (
    Asset,
    EntityGroup,
    Project,
    Repository,
    Status,
    StatusList,
    Task,
    Type,
    User,
)


@pytest.fixture(scope="function")
def setup_entity_group_tests():
    """Set up tests for the EntityGroup class."""
    data = dict()

    # create a couple of task
    data["status_new"] = Status(name="Mew", code="NEW")
    data["status_wfd"] = Status(name="Waiting For Dependency", code="WFD")
    data["status_rts"] = Status(name="Ready To Start", code="RTS")
    data["status_wip"] = Status(name="Work In Progress", code="WIP")
    data["status_prev"] = Status(name="Pending Review", code="PREV")
    data["status_hrev"] = Status(name="Has Revision", code="HREV")
    data["status_drev"] = Status(name="Dependency Has Revision", code="DREV")
    data["status_cmpl"] = Status(name="Completed", code="CMPL")

    data["test_user1"] = User(
        name="User1",
        login="user1",
        email="user1@user.com",
        password="1234",
    )

    data["test_user2"] = User(
        name="User2",
        login="user2",
        email="user2@user.com",
        password="1234",
    )

    data["test_user3"] = User(
        name="User3",
        login="user3",
        email="user3@user.com",
        password="1234",
    )

    data["project_status_list"] = StatusList(
        name="Project Status List",
        statuses=[data["status_new"], data["status_wip"], data["status_cmpl"]],
        target_entity_type="Project",
    )

    data["repo"] = Repository(
        name="Test Repo",
        code="TR",
        linux_path="/mnt/M/JOBs",
        windows_path="M:/JOBs",
        macos_path="/Users/Shared/Servers/M",
    )

    data["project1"] = Project(
        name="Tests Project",
        code="tp",
        status_list=data["project_status_list"],
        repository=data["repo"],
    )

    data["char_asset_type"] = Type(
        name="Character Asset", code="char", target_entity_type="Asset"
    )

    data["task_status_list"] = StatusList(
        name="Task Statuses",
        statuses=[
            data["status_wfd"],
            data["status_rts"],
            data["status_wip"],
            data["status_prev"],
            data["status_hrev"],
            data["status_drev"],
            data["status_cmpl"],
        ],
        target_entity_type="Task",
    )

    data["asset_status_list"] = StatusList(
        name="Asset Statuses",
        statuses=[
            data["status_wfd"],
            data["status_rts"],
            data["status_wip"],
            data["status_prev"],
            data["status_hrev"],
            data["status_drev"],
            data["status_cmpl"],
        ],
        target_entity_type="Asset",
    )

    data["asset1"] = Asset(
        name="Char1",
        code="char1",
        type=data["char_asset_type"],
        project=data["project1"],
        responsible=[data["test_user1"]],
        status_list=data["asset_status_list"],
    )

    data["task1"] = Task(
        name="Test Task",
        watchers=[data["test_user3"]],
        parent=data["asset1"],
        schedule_timing=5,
        schedule_unit="h",
        bid_timing=52,
        bid_unit="h",
        status_list=data["task_status_list"],
    )

    data["child_task1"] = Task(
        name="Child Task 1",
        resources=[data["test_user1"], data["test_user2"]],
        parent=data["task1"],
        status_list=data["task_status_list"],
    )

    data["child_task2"] = Task(
        name="Child Task 2",
        resources=[data["test_user1"], data["test_user2"]],
        parent=data["task1"],
        status_list=data["task_status_list"],
    )

    data["task2"] = Task(
        name="Another Task",
        project=data["project1"],
        resources=[data["test_user1"]],
        responsible=[data["test_user2"]],
        status_list=data["task_status_list"],
    )

    data["entity_group1"] = EntityGroup(
        name="My Tasks", entities=[data["task1"], data["child_task2"], data["task2"]]
    )
    return data


def test_entities_argument_is_skipped():
    """entities attribute is an empty list if the entities argument is skipped."""
    eg = EntityGroup()
    assert eg.entities == []


def test_entities_argument_is_none():
    """entities attribute is an empty list if the entities argument is None."""
    eg = EntityGroup(entities=None)
    assert eg.entities == []


def test_entities_argument_is_not_a_list():
    """TypeError is raised if the entities argument is not a list."""
    with pytest.raises(TypeError) as cm:
        EntityGroup(entities="not a list of SimpleEntities")

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_entities_argument_is_not_a_list_of_simple_entity_instances():
    """TypeError is raised if the entities argument is not a list of SimpleEntities."""
    with pytest.raises(TypeError) as cm:
        EntityGroup(entities=["not", 1, "list", "of", "SimpleEntities"])

    assert str(cm.value) == (
        "EntityGroup.entities should be a list of SimpleEntities, not str: 'not'"
    )


def test_entities_argument_is_working_properly(setup_entity_group_tests):
    """entities argument value is correctly passed to the entities attribute."""
    data = setup_entity_group_tests
    test_value = [data["project1"], data["asset1"], data["status_cmpl"]]
    eg = EntityGroup(entities=test_value)
    assert eg.entities == test_value
