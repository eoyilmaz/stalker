# -*- coding: utf-8 -*-
"""ProjectMixin related tests."""
import pytest

from sqlalchemy import Column, ForeignKey, Integer

from stalker import (
    Project,
    ProjectMixin,
    Repository,
    SimpleEntity,
    Status,
    StatusList,
    Type,
)


class DeclProjMixA(SimpleEntity, ProjectMixin):
    """A class for testing ProjectMixin."""

    __tablename__ = "DeclProjMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclProjMixA"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    def __init__(self, **kwargs):
        super(DeclProjMixA, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)


class DeclProjMixB(SimpleEntity, ProjectMixin):
    """A class for testing ProjectMixin."""

    __tablename__ = "DeclProjMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclProjMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    def __init__(self, **kwargs):
        super(DeclProjMixB, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def setup_project_mixin_tester():
    """Set up the tests for ProjectMixin.

    Returns:
        dict: Test data.
    """
    data = dict()
    data["test_stat1"] = Status(name="On Hold", code="OH")
    data["test_stat2"] = Status(name="Work In Progress", code="WIP")
    data["test_stat3"] = Status(name="Approved", code="APP")
    data["test_status_list_1"] = StatusList(
        name="A Statuses",
        statuses=[data["test_stat1"], data["test_stat3"]],
        target_entity_type=DeclProjMixA,
    )

    data["test_status_list_2"] = StatusList(
        name="B Statuses",
        statuses=[data["test_stat2"], data["test_stat3"]],
        target_entity_type=DeclProjMixB,
    )

    data["test_project_statuses"] = StatusList(
        name="Project Statuses",
        statuses=[data["test_stat2"], data["test_stat3"]],
        target_entity_type="Project",
    )

    data["test_project_type"] = Type(
        name="Test Project Type",
        code="testproj",
        target_entity_type="Project",
    )

    data["test_repository"] = Repository(
        name="Test Repo",
        code="TR",
    )

    data["test_project"] = Project(
        name="Test Project",
        code="tp",
        type=data["test_project_type"],
        status_list=data["test_project_statuses"],
        repository=data["test_repository"],
    )

    data["kwargs"] = {
        "name": "ozgur",
        "status_list": data["test_status_list_1"],
        "project": data["test_project"],
    }

    data["test_a_obj"] = DeclProjMixA(**data["kwargs"])
    return data


def test_project_attribute_is_working_properly(setup_project_mixin_tester):
    """project attribute is working properly."""
    data = setup_project_mixin_tester
    assert data["test_a_obj"].project == data["test_project"]
