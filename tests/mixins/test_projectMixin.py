# -*- coding: utf-8 -*-
"""ProjectMixin related tests."""
import pytest

from sqlalchemy import Column, ForeignKey, Integer

from stalker import Project, ProjectMixin, Repository, SimpleEntity, Type


class ProjMixClass(SimpleEntity, ProjectMixin):
    """A class for testing ProjectMixin."""

    __tablename__ = "ProjMixClasses"
    __mapper_args__ = {"polymorphic_identity": "ProjMixClass"}
    projMixClass_id = Column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(ProjMixClass, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def setup_project_mixin_tester():
    """Set up the tests for the ProjectMixin.

    Returns:
        dict: Test data.
    """
    # create a repository
    data = dict()
    data["repository_type"] = Type(
        name="Test Repository Type",
        code="testproj",
        target_entity_type="Repository",
    )

    data["test_repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["repository_type"],
    )

    # statuses
    from stalker import Status

    data["status1"] = Status(name="Status1", code="STS1")
    data["status2"] = Status(name="Status2", code="STS2")
    data["status3"] = Status(name="Status3", code="STS3")

    # project status list
    from stalker import StatusList

    data["project_status_list"] = StatusList(
        name="Project Status List",
        statuses=[
            data["status1"],
            data["status2"],
            data["status3"],
        ],
        target_entity_type="Project",
    )

    # project type
    data["test_project_type"] = Type(
        name="Test Project Type",
        code="testproj",
        target_entity_type="Project",
    )

    # create projects
    data["test_project1"] = Project(
        name="Test Project 1",
        code="tp1",
        type=data["test_project_type"],
        status_list=data["project_status_list"],
        repository=data["test_repository"],
    )
    data["test_project2"] = Project(
        name="Test Project 2",
        code="tp2",
        type=data["test_project_type"],
        status_list=data["project_status_list"],
        repository=data["test_repository"],
    )
    data["kwargs"] = {
        "name": "Test Class",
        "project": data["test_project1"],
    }
    data["test_foo_obj"] = ProjMixClass(**data["kwargs"])
    return data


def test_project_argument_is_skipped(setup_project_mixin_tester):
    """TypeError will be raised if the project argument is skipped."""
    data = setup_project_mixin_tester
    data["kwargs"].pop("project")
    with pytest.raises(TypeError) as cm:
        ProjMixClass(**data["kwargs"])

    assert (
        str(cm.value)
        == "ProjMixClass.project cannot be None it must be an instance of "
        "stalker.models.project.Project"
    )


def test_project_argument_is_none(setup_project_mixin_tester):
    """TypeError will be raised if the project argument is None."""
    data = setup_project_mixin_tester
    data["kwargs"]["project"] = None
    with pytest.raises(TypeError) as cm:
        ProjMixClass(**data["kwargs"])

    assert (
        str(cm.value)
        == "ProjMixClass.project cannot be None it must be an instance of "
        "stalker.models.project.Project"
    )


def test_project_attribute_is_none(setup_project_mixin_tester):
    """TypeError is raised if the project attribute is set to None."""
    data = setup_project_mixin_tester
    with pytest.raises(TypeError) as cm:
        data["test_foo_obj"].project = None

    assert (
        str(cm.value)
        == "ProjMixClass.project cannot be None it must be an instance of "
        "stalker.models.project.Project"
    )


def test_project_argument_is_not_a_project_instance(setup_project_mixin_tester):
    """TypeError is raised if the project argument is not a Project."""
    data = setup_project_mixin_tester
    data["kwargs"]["project"] = "a project"
    with pytest.raises(TypeError) as cm:
        ProjMixClass(**data["kwargs"])

    assert str(cm.value) == (
        "ProjMixClass.project should be an instance of stalker.models.project.Project "
        "instance, not str: 'a project'"
    )


def test_project_attribute_is_not_a_project_instance(setup_project_mixin_tester):
    """TypeError is raised if the project attribute is not a Project."""
    data = setup_project_mixin_tester
    with pytest.raises(TypeError) as cm:
        data["test_foo_obj"].project = "a project"

    assert str(cm.value) == (
        "ProjMixClass.project should be an instance of stalker.models.project.Project "
        "instance, not str: 'a project'"
    )


def test_project_attribute_is_working_properly(setup_project_mixin_tester):
    """project attribute is working properly."""
    data = setup_project_mixin_tester
    data["test_foo_obj"].project = data["test_project2"]
    assert data["test_foo_obj"].project == data["test_project2"]
