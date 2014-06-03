# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import unittest

from sqlalchemy import Column, Integer, ForeignKey
from stalker.db.session import DBSession
from stalker import (SimpleEntity, ProjectMixin, Status, StatusList, Type,
                     Project, Repository)


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

        # create a repository
        self.repository_type = Type(
            name="Test Repository Type",
            code='testproj',
            target_entity_type=Repository
        )

        self.test_repository = Repository(
            name="Test Repository",
            type=self.repository_type,
            )

        # statuses
        self.status1 = Status(name="Status1", code="STS1")
        self.status2 = Status(name="Status2", code="STS2")
        self.status3 = Status(name="Status3", code="STS3")

        # project status list
        self.project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.status1,
                self.status2,
                self.status3,
                ],
            target_entity_type=Project
        )

        # project type
        self.test_project_type = Type(
            name="Test Project Type",
            code='testproj',
            target_entity_type=Project,
        )

        # create projects
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

    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()

    def test_project_argument_is_skipped(self):
        """testing if a TypeError will be raised when the project argument is
        skipped
        """
        self.kwargs.pop("project")
        self.assertRaises(TypeError, ProjMixClass, **self.kwargs)

    def test_project_argument_is_None(self):
        """testing if a TypeError will be raised when the project argument is
        None
        """
        self.kwargs["project"] = None
        self.assertRaises(TypeError, ProjMixClass, **self.kwargs)

    def test_project_attribute_is_None(self):
        """testing if a TypeError will be raised when the project attribute is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_foo_obj, "project",
                          None)

    def test_project_argument_is_not_a_Project_instance(self):
        """testing if a TypeError will be raised when the project argument is
        not a stalker.models.project.Project instance
        """
        self.kwargs["project"] = "a project"
        self.assertRaises(TypeError, ProjMixClass, **self.kwargs)

    def test_project_attribute_is_not_a_Project_instance(self):
        """testing if a TypeError will be raised when the project attribute is
        set to something other than a stalker.models.project.Project instance
        """
        self.assertRaises(TypeError, setattr, self.test_foo_obj, "project",
                          "a project")

    def test_project_attribute_is_working_properly(self):
        """testing if the project attribute is working properly
        """
        self.test_foo_obj.project = self.test_project2
        self.assertEqual(self.test_foo_obj.project, self.test_project2)
