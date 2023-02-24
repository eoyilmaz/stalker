# -*- coding: utf-8 -*-
"""Tests related to the ProjectClient class."""

import pytest

from stalker import Client, Project, ProjectClient, Repository, Role, Status, User


@pytest.fixture(scope="function")
def setup_project_client_db_test(setup_postgresql_db):
    """Set the test up ProjectClient class tests with a DB."""
    data = dict()
    data["test_repo"] = Repository(name="Test Repo", code="TR")
    data["status_new"] = Status(name="New", code="NEW")
    data["status_wip"] = Status(name="Work In Progress", code="WIP")
    data["status_cmpl"] = Status(name="Completed", code="CMPL")

    data["test_user1"] = User(
        name="Test User 1",
        login="testuser1",
        email="testuser1@users.com",
        password="secret",
    )

    data["test_client"] = Client(name="Test Client")

    data["test_project"] = Project(
        name="Test Project 1",
        code="TP1",
        repositories=[data["test_repo"]],
    )

    data["test_role"] = Role(name="Test Client")
    return data


def test_project_client_creation(setup_project_client_db_test):
    """Project client creation."""
    data = setup_project_client_db_test
    ProjectClient(
        project=data["test_project"], client=data["test_client"], role=data["test_role"]
    )

    assert data["test_client"] in data["test_project"].clients


def test_role_argument_is_not_a_role_instance(setup_project_client_db_test):
    """TypeError will be raised when the role argument is not a Role instance."""
    data = setup_project_client_db_test
    with pytest.raises(TypeError) as cm:
        ProjectClient(
            project=data["test_project"],
            client=data["test_client"],
            role="not a role instance",
        )

    assert (
        str(cm.value) == "ProjectClient.role should be a stalker.models.auth.Role "
        "instance, not str"
    )
