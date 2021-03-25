# -*- coding: utf-8 -*-

import pytest
from stalker import ProjectClient
from stalker.testing import UnitTestDBBase


class ProjectClientTestDBCase(UnitTestDBBase):
    """tests for ProjectClient class
    """

    def setUp(self):
        """set the test up
        """
        super(ProjectClientTestDBCase, self).setUp()

        from stalker import Status, Repository
        self.test_repo = Repository(
            name='Test Repo',
            code='TR'
        )
        self.status_new = Status(name='New', code='NEW')
        self.status_wip = Status(name='Work In Progress', code='WIP')
        self.status_cmpl = Status(name='Completed', code='CMPL')

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
        )

        from stalker import Role
        self.test_role = Role(
            name='Test Client'
        )

    def test_project_client_creation(self):
        """testing project client creation
        """
        ProjectClient(
            project=self.test_project,
            client=self.test_client,
            role=self.test_role
        )

        assert self.test_client in self.test_project.clients

    def test_role_argument_is_not_a_role_instance(self):
        """testing if a TypeError will be raised when the role argument is not
        a Role instance
        """
        with pytest.raises(TypeError) as cm:
            ProjectClient(
                project=self.test_project,
                client=self.test_client,
                role='not a role instance'
            )

        assert str(cm.value) == \
            'ProjectClient.role should be a stalker.models.auth.Role ' \
            'instance, not str'
