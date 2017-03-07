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

from stalker.testing import UnitTestBase
from stalker import Client


class ClientTestCase(UnitTestBase):
    """tests the Client class
    """

    def setUp(self):
        """lets setup the tests
        """
        super(ClientTestCase, self).setUp()
        # create a couple of test users
        from stalker import User
        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@test.com",
            password="123456",
        )
        from stalker import db
        db.DBSession.add(self.test_user1)

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@test.com",
            password="123456",
        )
        db.DBSession.add(self.test_user2)

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@test.com",
            password="123456",
        )
        db.DBSession.add(self.test_user3)

        self.test_user4 = User(
            name="User4",
            login="user4",
            email="user4@test.com",
            password="123456",
        )
        db.DBSession.add(self.test_user4)

        self.users_list = [
            self.test_user1,
            self.test_user2,
            self.test_user3,
            self.test_user4
        ]
        db.DBSession.commit()

        self.test_admin = User.query.filter(User.name == 'admin').first()

        from stalker import Status
        self.status_new = Status.query.filter(Status.code == 'NEW').first()
        self.status_wip = Status.query.filter(Status.code == 'WIP').first()
        self.status_cmpl = Status.query.filter(Status.code == 'CMPL').first()

        from stalker import StatusList
        self.project_statuses = StatusList(
            name="Project Status List",
            statuses=[
                self.status_new,
                self.status_wip,
                self.status_cmpl
            ],
            target_entity_type='Project'
        )
        db.DBSession.add(self.project_statuses)

        from stalker import Repository
        self.test_repo = Repository(
            name="Test Repository"
        )
        db.DBSession.add(self.test_repo)

        from stalker import Project
        self.test_project1 = Project(
            name="Test Project 1",
            code='proj1',
            status_list=self.project_statuses,
            repository=self.test_repo,
        )
        db.DBSession.add(self.test_project1)

        self.test_project2 = Project(
            name="Test Project 1",
            code='proj2',
            status_list=self.project_statuses,
            repository=self.test_repo,
        )
        db.DBSession.add(self.test_project2)

        self.test_project3 = Project(
            name="Test Project 1",
            code='proj3',
            status_list=self.project_statuses,
            repository=self.test_repo,
        )
        db.DBSession.add(self.test_project3)

        self.projects_list = [
            self.test_project1,
            self.test_project2,
            self.test_project3

        ]

        import pytz
        import datetime
        self.date_created = self.date_updated = datetime.datetime.now(pytz.utc)

        self.kwargs = {
            "name": "Test Client",
            "description": "This is a client for testing purposes",
            "created_by": self.test_admin,
            "updated_by": self.test_admin,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "users": self.users_list,
            "projects": self.projects_list
        }

        # create a default client object
        self.test_client = Client(**self.kwargs)
        db.DBSession.add(self.test_client)
        db.DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_false(self):
        """testing if the __auto_name__ class attribute is set to False for
        Department class
        """
        self.assertFalse(Client.__auto_name__)

    def test_users_argument_accepts_an_empty_list(self):
        """testing if users argument accepts an empty list
        """
        # this should work without raising any error
        self.kwargs["users"] = []
        new_dep = Client(**self.kwargs)
        self.assertTrue(isinstance(new_dep, Client))

    def test_users_attribute_accepts_an_empty_list(self):
        """testing if users attribute accepts an empty list
        """
        # this should work without raising any error
        self.test_client.users = []

    def test_users_argument_accepts_only_a_list_of_user_objects(self):
        """testing if users argument accepts only a list of user objects
        """
        test_value = [1, 2.3, [], {}]
        self.kwargs["users"] = test_value
        # this should raise a TypeError
        with self.assertRaises(TypeError) as cm:
            Client(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'ClientUser.user should be an instance of '
            'stalker.models.auth.User, not int'
        )

    def test_users_attribute_accepts_only_a_list_of_user_objects(self):
        """testing if users attribute accepts only a list of user objects
        """
        test_value = [1, 2.3, [], {}]
        # this should raise a TypeError
        with self.assertRaises(TypeError) as cm:
            self.test_client.users = test_value

        self.assertEqual(
            str(cm.exception),
            'ClientUser.user should be an instance of '
            'stalker.models.auth.User, not int'
        )

    def test_users_attribute_elements_accepts_user_only_append(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a User object to the users list
        """
        # append
        with self.assertRaises(TypeError) as cm:
            self.test_client.users.append(0)

        self.assertEqual(
            str(cm.exception),
            'ClientUser.user should be an instance of '
            'stalker.models.auth.User, not int'
        )

    def test_users_attribute_elements_accepts_user_only_setitem(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a User object to the users list
        """
        # __setitem__
        with self.assertRaises(TypeError) as cm:
            self.test_client.users[0] = 0

        self.assertEqual(
            str(cm.exception),
            'ClientUser.user should be an instance of '
            'stalker.models.auth.User, not int'
        )

    def test_users_argument_is_not_iterable(self):
        """testing if a TypeError will be raised when the given users
        argument is not an instance of list
        """
        self.kwargs["users"] = "a user"
        with self.assertRaises(TypeError) as cm:
            Client(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'ClientUser.user should be an instance of '
            'stalker.models.auth.User, not str'
        )

    def test_users_attribute_is_not_iterable(self):
        """testing if a TypeError will be raised when the users attribute
        is tried to be set to a non-iterable value
        """
        test_value = "a user"
        with self.assertRaises(TypeError) as cm:
            self.test_client.users = test_value

        self.assertEqual(
            str(cm.exception),
            'ClientUser.user should be an instance of '
            'stalker.models.auth.User, not str'
        )

    def test_users_attribute_defaults_to_empty_list(self):
        """testing if the users attribute defaults to an empty list if the
         users argument is skipped
        """
        self.kwargs.pop("users")
        new_client = Client(**self.kwargs)
        self.assertEqual(new_client.users, [])

    def test_users_attribute_set_to_None(self):
        """testing if a TypeError will be raised when the users attribute is
        set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_client.users = None

        self.assertEqual(
            str(cm.exception),
            "'NoneType' object is not iterable"
        )

    def test_projects_argument_accepts_an_empty_list(self):
        """testing if projects argument accepts an empty list
        """
        # this should work without raising any error
        self.kwargs["projects"] = []
        new_dep = Client(**self.kwargs)
        self.assertTrue(isinstance(new_dep, Client))

    def test_projects_attribute_accepts_an_empty_list(self):
        """testing if projects attribute accepts an empty list
        """
        # this should work without raising any error
        self.test_client.projects = []

    def test_projects_argument_accepts_only_a_list_of_project_objects(self):
        """testing if projects argument accepts only a list of project objects
        """
        test_value = [1, 2.3, [], {}]
        self.kwargs["projects"] = test_value
        # this should raise a TypeError
        with self.assertRaises(TypeError) as cm:
            Client(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'ProjectClient.project should be a stalker.models.project.Project '
            'instance, not int'
        )

    def test_projects_attribute_accepts_only_a_list_of_project_objects(self):
        """testing if users attribute accepts only a list of project objects
        """
        test_value = [1, 2.3, 'a project']
        # this should raise a TypeError
        with self.assertRaises(TypeError) as cm:
            self.test_client.projects = test_value

        self.assertEqual(
            str(cm.exception),
            'ProjectClient.project should be a stalker.models.project.Project '
            'instance, not int'
        )

    def test_projects_attribute_elements_accepts_Project_only_append(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Project object to the projects list
        """
        # append
        with self.assertRaises(TypeError) as cm:
            self.test_client.projects.append(0)

        self.assertEqual(
            str(cm.exception),
            'ProjectClient.project should be a stalker.models.project.Project '
            'instance, not int'
        )

    def test_projects_attribute_elements_accepts_Project_only_setitem(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Project object to the projects list
        """
        # __setitem__
        with self.assertRaises(TypeError) as cm:
            self.test_client.projects[0] = 0

        self.assertEqual(
            str(cm.exception),
            'ProjectClient.project should be a stalker.models.project.Project '
            'instance, not int'
        )

    def test_projects_argument_is_not_iterable(self):
        """testing if a TypeError will be raised when the given projects
        argument is not an instance of list
        """
        from stalker import Project
        self.kwargs["projects"] = "a project"
        with self.assertRaises(TypeError) as cm:
            Project(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Project.code cannot be None'
        )

    def test_projects_attribute_is_not_iterable(self):
        """testing if a TypeError will be raised when the projects attribute
        is tried to be set to a non-iterable value
        """
        test_value = "a project"
        with self.assertRaises(TypeError) as cm:
            self.test_client.projects = test_value

        self.assertEqual(
            str(cm.exception),
            'ProjectClient.project should be a '
            'stalker.models.project.Project instance, not str'
        )

    def test_projects_attribute_defaults_to_empty_list(self):
        """testing if the projects attribute defaults to an empty list if the
         projects argument is skipped
        """
        self.kwargs.pop("projects")
        new_client = Client(**self.kwargs)
        self.assertEqual(new_client.projects, [])

    def test_projects_attribute_set_to_None(self):
        """testing if a TypeError will be raised when the projects attribute is
        set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_client.projects = None

        self.assertEqual(
            str(cm.exception),
            "'NoneType' object is not iterable"
        )

    def test_user_remove_also_removes_client_from_user(self):
        """testing if removing an user from the users list also removes the
        client from the users companies attribute
        """
        # check if the user is in the company
        self.assertTrue(self.test_client in self.test_user1.companies)

        # now remove the user from the company
        self.test_client.users.remove(self.test_user1)

        # now check if company is not in users companies anymore
        self.assertFalse(self.test_client in self.test_user1.companies)

        # assign the user back
        self.test_user1.companies.append(self.test_client)

        # check if the user is in the companies users list
        self.assertTrue(self.test_user1 in self.test_client.users)

    # def test_project_remove_also_removes_project_from_client(self):
    #     """testing if removing an user from the users list also removes the
    #     client from the users companies attribute
    #     """
    #     # check if the project is registered with the client
    #     self.assertTrue(self.test_client in self.test_project1.clients)
    #
    #     # now remove the project from the client
    #     # self.test_client.projects.remove(self.test_project1)
    #     self.test_client.project_role.remove(self.test_client.project_role[0])
    #
    #     # now check if project no longer belongs to client
    #     self.assertFalse(self.test_project1 in self.test_client.projects)
    #
    #     # assign the project back
    #     self.test_client.projects.append(self.test_project1)
    #
    #     # check if the project is in the companies projects list
    #     self.assertTrue(self.test_project1 in self.test_client.projects)

    def test_equality(self):
        """testing equality of two Client objects
        """
        dep1 = Client(**self.kwargs)
        dep2 = Client(**self.kwargs)

        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("users")
        entity_kwargs.pop("projects")
        from stalker import Entity
        entity1 = Entity(**entity_kwargs)

        self.kwargs["name"] = "Company X"
        dep3 = Client(**self.kwargs)

        self.assertTrue(dep1 == dep2)
        self.assertFalse(dep1 == dep3)
        self.assertFalse(dep1 == entity1)

    def test_inequality(self):
        """testing inequality of two Client objects
        """
        dep1 = Client(**self.kwargs)
        dep2 = Client(**self.kwargs)

        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("users")
        entity_kwargs.pop("projects")
        from stalker import Entity
        entity1 = Entity(**entity_kwargs)

        self.kwargs["name"] = "Company X"
        dep3 = Client(**self.kwargs)

        self.assertFalse(dep1 != dep2)
        self.assertTrue(dep1 != dep3)
        self.assertTrue(dep1 != entity1)

    # def test_hash_value(self):
    #     """testing if the hash value is correctly calculated
    #     """
    #     self.assertEqual(
    #         hash(self.test_client),
    #         self.test_client.__hash__()
    #     )
