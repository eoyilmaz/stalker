# -*- coding: utf-8 -*-
"""Tests related to the ProjectUser class."""

import pytest

from stalker import Project, ProjectUser, Repository, Role, User
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_project_user_db_tests(setup_postgresql_db):
    """Set up the tests database and data for the ProjectUser class related tests."""
    data = dict()
    data["test_repo"] = Repository(name="Test Repo", code="TR")

    DBSession.add(data["test_repo"])
    DBSession.commit()

    data["test_user1"] = User(
        name="Test User 1",
        login="testuser1",
        email="testuser1@users.com",
        password="secret",
    )
    DBSession.add(data["test_user1"])

    data["test_project"] = Project(
        name="Test Project 1",
        code="TP1",
        repositories=[data["test_repo"]],
    )
    DBSession.add(data["test_project"])

    data["test_role"] = Role(name="Test User")
    DBSession.add(data["test_role"])
    DBSession.commit()
    return data


def test_project_user_creation(setup_project_user_db_tests):
    """project user creation."""
    data = setup_project_user_db_tests
    ProjectUser(
        project=data["test_project"], user=data["test_user1"], role=data["test_role"]
    )
    assert data["test_user1"] in data["test_project"].users


def test_role_argument_is_not_a_role_instance(setup_project_user_db_tests):
    """TypeError will be raised if the role argument is not a Role instance."""
    data = setup_project_user_db_tests
    with pytest.raises(TypeError) as cm:
        ProjectUser(
            project=data["test_project"],
            user=data["test_user1"],
            role="not a role instance",
        )

    assert str(cm.value) == (
        "ProjectUser.role should be a stalker.models.auth.Role instance, "
        "not str: 'not a role instance'"
    )


def test_rate_attribute_is_copied_from_user(setup_project_user_db_tests):
    """rate attribute value is copied from the user on init."""
    data = setup_project_user_db_tests
    data["test_user1"].rate = 100.0
    project_user1 = ProjectUser(
        project=data["test_project"], user=data["test_user1"], role=data["test_role"]
    )
    assert data["test_user1"].rate == project_user1.rate


def test_rate_attribute_initialization_through_user(setup_project_user_db_tests):
    """rate attribute initialization through ``user.projects`` attribute."""
    data = setup_project_user_db_tests
    data["test_user1"].rate = 102.0
    data["test_user1"].projects = [data["test_project"]]
    assert data["test_project"].user_role[0].rate == data["test_user1"].rate


def test_rate_attribute_initialization_through_project(setup_project_user_db_tests):
    """rate attribute initialization through ``project.users`` attribute."""
    data = setup_project_user_db_tests
    data["test_user1"].rate = 102.0
    data["test_project"].users = [data["test_user1"]]

    assert data["test_project"].user_role[0].rate == data["test_user1"].rate
