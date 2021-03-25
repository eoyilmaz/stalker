# -*- coding: utf-8 -*-

import pytest
from stalker.testing import UnitTestDBBase
from stalker import ProjectUser


class ProjectUserTestDBCase(UnitTestDBBase):
    """tests for ProjectUser class
    """

    def setUp(self):
        """set the test up
        """
        super(ProjectUserTestDBCase, self).setUp()

        from stalker import Repository
        self.test_repo = Repository(
            name='Test Repo',
            code='TR'
        )

        from stalker.db.session import DBSession
        DBSession.add(self.test_repo)
        DBSession.commit()

        from stalker import User
        self.test_user1 = User(
            name='Test User 1',
            login='testuser1',
            email='testuser1@users.com',
            password='secret'
        )
        DBSession.add(self.test_user1)

        from stalker import Project
        self.test_project = Project(
            name='Test Project 1',
            code='TP1',
            repositories=[self.test_repo],
        )
        DBSession.add(self.test_project)

        from stalker import Role
        self.test_role = Role(
            name='Test User'
        )
        DBSession.add(self.test_role)
        DBSession.commit()

    def test_project_user_creation(self):
        """testing project user creation
        """
        ProjectUser(
            project=self.test_project,
            user=self.test_user1,
            role=self.test_role
        )

        assert self.test_user1 in self.test_project.users

    def test_role_argument_is_not_a_role_instance(self):
        """testing if a TypeError will be raised when the role argument is not
        a Role instance
        """
        with pytest.raises(TypeError) as cm:
            ProjectUser(
                project=self.test_project,
                user=self.test_user1,
                role='not a role instance'
            )

        assert str(cm.value) == \
            'ProjectUser.role should be a stalker.models.auth.Role ' \
            'instance, not str'

    def test_rate_attribute_is_copied_from_user(self):
        """testing if the rate attribute value is copied from the user on init
        """
        self.test_user1.rate = 100.0
        project_user1 = ProjectUser(
            project=self.test_project,
            user=self.test_user1,
            role=self.test_role
        )
        assert self.test_user1.rate == project_user1.rate

    def test_rate_attribute_initialization_through_user(self):
        """testing of rate attribute initialization through user.projects
        attribute
        """
        self.test_user1.rate = 102.0
        self.test_user1.projects = [self.test_project]
        assert self.test_project.user_role[0].rate == self.test_user1.rate

    def test_rate_attribute_initialization_through_project(self):
        """testing of rate attribute initialization through project.users
        attribute
        """
        self.test_user1.rate = 102.0
        self.test_project.users = [self.test_user1]

        assert self.test_project.user_role[0].rate == self.test_user1.rate
