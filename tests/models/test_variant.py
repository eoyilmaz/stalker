# -*- coding: utf-8 -*-
"""Tests for the Variant class."""

import pytest

from stalker.models.auth import User
from stalker.models.project import Project
from stalker.models.repository import Repository
from stalker.models.type import Type
from stalker.models.variant import Variant
from stalker.models.status import Status, StatusList
from stalker.models.task import Task
from stalker.models.version import Version


@pytest.fixture(scope="function")
def setup_variant_tests():
    """Setup Variant tests."""
    data = dict()

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

    data["variant_status_list"] = StatusList(
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
        target_entity_type="Variant",
    )

    data["test_project_status_list"] = StatusList(
        name="Project Statuses",
        statuses=[data["status_wip"], data["status_prev"], data["status_cmpl"]],
        target_entity_type="Project",
    )

    data["test_variant_status_list"] = StatusList(
        name="Variant Statuses",
        statuses=[data["status_wip"], data["status_prev"], data["status_cmpl"]],
        target_entity_type="Variant",
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

    data["test_variant"] = Variant(
        name="Main",
        project=data["test_project1"],
        status_list=data["test_variant_status_list"],
    )
    yield data


# @pytest.fixture(scope="function")
# def setup_variant_db_tests(setup_postgresql_db):
#     """Setup Variant tests with a test DB."""
#     data = dict()


def test_variant_is_derived_from_task():
    """Variant is deriving from Task class."""
    assert Task in Variant.__mro__


def test_variant_entity_type_is_variant(setup_variant_tests):
    """Variant.entity_type is "Variant"."""
    data = setup_variant_tests
    assert data["test_variant"].entity_type == "Variant"


def test_variant_is_not_auto_named():
    """Variant.__auto_name__ is False."""
    assert Variant.__auto_name__ is False


def test_variant_can_be_used_in_task_hierarchies(setup_variant_tests):
    """Variant instances can be used in task hierarchies."""
    data = setup_variant_tests
    task = Task(
        name="Test Task 1",
        project=data["test_project1"],
        status_list=data["task_status_list"],
    )
    # should not raise any errors
    variant = data["test_variant"]
    variant.parent = task
    assert variant.parent == task


def test_variant_accepts_version_instances(setup_variant_tests):
    """Variant instances accepts Version instances."""
    data = setup_variant_tests
    variant = data["test_variant"]
    version = Version(task=variant)
    assert version in variant.versions
