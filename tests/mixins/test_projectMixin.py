# -*- coding: utf-8 -*-

import unittest

import pytest
from sqlalchemy import Column, Integer, ForeignKey
from stalker import SimpleEntity, ProjectMixin


class ProjMixClass(SimpleEntity, ProjectMixin):
    __tablename__ = "ProjMixClasses"
    __mapper_args__ = {"polymorphic_identity": "ProjMixClass"}
    projMixClass_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                             primary_key=True)

    def __init__(self, **kwargs):
        super(ProjMixClass, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)


class ProjectMixinTester(unittest.TestCase):
    """Tests the ProjectMixin
    """

    def setUp(self):
        """setup the test
        """
        super(ProjectMixinTester, self).setUp()

        # create a repository
        from stalker import db, Type
        self.repository_type = Type(
            name="Test Repository Type",
            code='testproj',
            target_entity_type='Repository'
        )

        from stalker import Repository
        self.test_repository = Repository(
            name="Test Repository",
            code='TR',
            type=self.repository_type,
        )

        # statuses
        from stalker import Status
        self.status1 = Status(name="Status1", code="STS1")
        self.status2 = Status(name="Status2", code="STS2")
        self.status3 = Status(name="Status3", code="STS3")

        # project status list
        from stalker import StatusList
        self.project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.status1,
                self.status2,
                self.status3,
                ],
            target_entity_type='Project'
        )

        # project type
        self.test_project_type = Type(
            name="Test Project Type",
            code='testproj',
            target_entity_type='Project',
        )

        # create projects
        from stalker import Project
        self.test_project1 = Project(
            name="Test Project 1",
            code='tp1',
            type=self.test_project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )

        self.test_project2 = Project(
            name="Test Project 2",
            code='tp2',
            type=self.test_project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )

        self.kwargs = {
            "name": "Test Class",
            "project": self.test_project1,
        }

        self.test_foo_obj = ProjMixClass(**self.kwargs)

    def test_project_argument_is_skipped(self):
        """testing if a TypeError will be raised when the project argument is
        skipped
        """
        self.kwargs.pop("project")
        with pytest.raises(TypeError) as cm:
            ProjMixClass(**self.kwargs)

        assert str(cm.value) == \
            'ProjMixClass.project can not be None it must be an instance of ' \
            'stalker.models.project.Project'

    def test_project_argument_is_None(self):
        """testing if a TypeError will be raised when the project argument is
        None
        """
        self.kwargs["project"] = None
        with pytest.raises(TypeError) as cm:
            ProjMixClass(**self.kwargs)

        assert str(cm.value) == \
            'ProjMixClass.project can not be None it must be an instance of ' \
            'stalker.models.project.Project'

    def test_project_attribute_is_None(self):
        """testing if a TypeError will be raised when the project attribute is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_foo_obj.project = None

        assert str(cm.value) == \
            'ProjMixClass.project can not be None it must be an instance of ' \
            'stalker.models.project.Project'

    def test_project_argument_is_not_a_Project_instance(self):
        """testing if a TypeError will be raised when the project argument is
        not a stalker.models.project.Project instance
        """
        self.kwargs["project"] = "a project"
        with pytest.raises(TypeError) as cm:
            ProjMixClass(**self.kwargs)

        assert str(cm.value) == \
            'ProjMixClass.project should be an instance of ' \
            'stalker.models.project.Project instance not str'

    def test_project_attribute_is_not_a_Project_instance(self):
        """testing if a TypeError will be raised when the project attribute is
        set to something other than a stalker.models.project.Project instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_foo_obj.project = "a project"

        assert str(cm.value) == \
            'ProjMixClass.project should be an instance of ' \
            'stalker.models.project.Project instance not str'

    def test_project_attribute_is_working_properly(self):
        """testing if the project attribute is working properly
        """
        self.test_foo_obj.project = self.test_project2
        assert self.test_foo_obj.project == self.test_project2
