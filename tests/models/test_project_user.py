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
from stalker import ProjectUser


class ProjectUserTestCase(unittest.TestCase):
    """tests for ProjectUser class
    """

    def setUp(self):
        """set the test up
        """
        from stalker import Status, StatusList, Repository
        self.test_repo = Repository(
            name='Test Repo'
        )
        self.status_new = Status(name='New', code='NEW')
        self.status_wip = Status(name='Work In Progress', code='WIP')
        self.status_cmpl = Status(name='Completed', code='CMPL')

        self.project_statuses = StatusList(
            name='Project Status List',
            statuses=[self.status_new, self.status_wip, self.status_cmpl],
            target_entity_type='Project'
        )

        from stalker import User
        self.test_user1 = User(
            name='Test User 1',
            login='testuser1',
            email='testuser1@users.com',
            password='secret'
        )

        from stalker import Project
        self.test_project = Project(
            name='Test Project 1',
            code='TP1',
            repositories=[self.test_repo],
            status_list=self.project_statuses
        )

        from stalker import Role
        self.test_role = Role(
            name='Test User'
        )

    def test_project_user_creation(self):
        """testing project user creation
        """
        project_user1 = ProjectUser(
            project=self.test_project,
            user=self.test_user1,
            role=self.test_role
        )

        self.assertTrue(self.test_user1 in self.test_project.users)

    def test_role_argument_is_not_a_role_instance(self):
        """testing if a TypeError will be raised when the role argument is not
        a Role instance
        """
        with self.assertRaises(TypeError) as cm:
            project_user1 = ProjectUser(
                project=self.test_project,
                user=self.test_user1,
                role='not a role instance'
            )

        self.assertEqual(
            str(cm.exception),
            'ProjectUser.role should be a stalker.models.auth.Role instance, '
            'not str'
        )

    def test_rate_attribute_is_copied_from_user(self):
        """testing if the rate attribute value is copied from the user on init
        """
        self.test_user1.rate = 100.0
        project_user1 = ProjectUser(
            project=self.test_project,
            user=self.test_user1,
            role=self.test_role
        )
        self.assertEqual(self.test_user1.rate, project_user1.rate)

    def test_rate_attribute_initialization_through_user(self):
        """testing of rate attribute initialization through user.projects
        attribute
        """
        self.test_user1.rate = 102.0
        self.test_user1.projects = [self.test_project]
        self.assertEqual(
            self.test_project.user_role[0].rate,
            self.test_user1.rate
        )

    def test_rate_attribute_initialization_through_project(self):
        """testing of rate attribute initialization through project.users
        attribute
        """
        self.test_user1.rate = 102.0
        self.test_project.users = [self.test_user1]

        self.assertEqual(
            self.test_project.user_role[0].rate,
            self.test_user1.rate
        )
