# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

from stalker import ProjectClient
from stalker.testing import UnitTestBase


class ProjectClientTestCase(UnitTestBase):
    """tests for ProjectClient class
    """

    def setUp(self):
        """set the test up
        """
        super(ProjectClientTestCase, self).setUp()

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

        from stalker import Client
        self.test_client = Client(
            name='Test Client'
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
            name='Test Client'
        )

    def test_project_client_creation(self):
        """testing project client creation
        """
        project_client1 = ProjectClient(
            project=self.test_project,
            client=self.test_client,
            role=self.test_role
        )

        self.assertTrue(self.test_client in self.test_project.clients)

    def test_role_argument_is_not_a_role_instance(self):
        """testing if a TypeError will be raised when the role argument is not
        a Role instance
        """
        with self.assertRaises(TypeError) as cm:
            project_client1 = ProjectClient(
                project=self.test_project,
                client=self.test_client,
                role='not a role instance'
            )

        self.assertEqual(
            str(cm.exception),
            'ProjectClient.role should be a stalker.models.auth.Role '
            'instance, not str'
        )
