# -*- coding: utf-8 -*-

import unittest
from sqlalchemy import Column, Integer, ForeignKey
from stalker.models.project import Project
from stalker.models.type import Type
from stalker.models.status import Status, StatusList
from stalker.models.repository import Repository
from stalker.models.mixins import ProjectMixin

# create a new mixed in SimpleEntity
from stalker.models.entity import SimpleEntity


class DeclProjMixA(SimpleEntity, ProjectMixin):
    __tablename__ = "DeclProjMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclProjMixA"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)

    def __init__(self, **kwargs):
        super(DeclProjMixA, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)


class DeclProjMixB(SimpleEntity, ProjectMixin):
    __tablename__ = "DeclProjMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclProjMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)

    def __init__(self, **kwargs):
        super(DeclProjMixB, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)


class ProjectMixinTester(unittest.TestCase):
    """tests ProjectMixin
    """

    def setUp(self):
        """setup the test
        """
        super(ProjectMixinTester, self).setUp()
        self.test_stat1 = Status(name="On Hold", code="OH")
        self.test_stat2 = Status(name="Work In Progress", code="WIP")
        self.test_stat3 = Status(name="Approved", code="APP")

        self.test_status_list_1 = StatusList(
            name="A Statuses",
            statuses=[self.test_stat1, self.test_stat3],
            target_entity_type=DeclProjMixA,
        )

        self.test_status_list_2 = StatusList(
            name="B Statuses",
            statuses=[self.test_stat2, self.test_stat3],
            target_entity_type=DeclProjMixB
        )

        self.test_project_statuses = StatusList(
            name="Project Statuses",
            statuses=[self.test_stat2, self.test_stat3],
            target_entity_type='Project'
        )

        self.test_project_type = Type(
            name='Test Project Type',
            code='testproj',
            target_entity_type='Project',
        )

        self.test_repository = Repository(
            name="Test Repo",
            code='TR',
        )

        self.test_project = Project(
            name="Test Project",
            code='tp',
            type=self.test_project_type,
            status_list=self.test_project_statuses,
            repository=self.test_repository,
        )

        self.kwargs = {
            "name": "ozgur",
            "status_list": self.test_status_list_1,
            "project": self.test_project,
        }

        self.test_a_obj = DeclProjMixA(**self.kwargs)

    def test_project_attribute_is_working_properly(self):
        """testing if the project attribute is working properly
        """

        assert self.test_a_obj.project == self.test_project
