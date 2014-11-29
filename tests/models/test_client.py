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
import datetime
from stalker import (Client, Entity, User, Project, Status, StatusList,
                     Repository)


class ClientTestCase(unittest.TestCase):
    """tests the Client class
    """

    def setUp(self):
        """lets setup the tests
        """
        # create a couple of test users
        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@test.com",
            password="123456",
        )

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@test.com",
            password="123456",
        )

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@test.com",
            password="123456",
        )

        self.test_user4 = User(
            name="User4",
            login="user4",
            email="user4@test.com",
            password="123456",
        )

        self.users_list = [
            self.test_user1,
            self.test_user2,
            self.test_user3,
            self.test_user4
        ]

        self.test_admin = User(
            name="admin",
            login="admin",
            email="admin@test.com",
            password="admin",
        )

        self.status_new = Status(name="Test status 1", code="Status1")
        self.status_wip = Status(name="Test status 2", code="Status2")
        self.status_cmpl = Status(name="Test status 3", code="Status3")

        self.project_statuses = StatusList(
            name="Project Status List",
            statuses=[
                self.status_new,
                self.status_wip,
                self.status_cmpl
            ],
            target_entity_type='Project'
        )

        self.test_repo = Repository(
            name="Test Repository"
        )

        self.test_project1 = Project(
            name="Test Project 1",
            code='proj1',
            status_list=self.project_statuses,
            repository=self.test_repo,
        )

        self.test_project2 = Project(
            name="Test Project 1",
            code='proj2',
            status_list=self.project_statuses,
            repository=self.test_repo,
        )

        self.test_project3 = Project(
            name="Test Project 1",
            code='proj3',
            status_list=self.project_statuses,
            repository=self.test_repo,
        )

        self.projects_list = [
            self.test_project1,
            self.test_project2,
            self.test_project3

        ]

        self.date_created = self.date_updated = datetime.datetime.now()

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
        self.assertRaises(
            TypeError,
            Client,
            **self.kwargs
        )

    def test_users_attribute_accepts_only_a_list_of_user_objects(self):
        """testing if users attribute accepts only a list of user objects
        """
        test_value = [1, 2.3, [], {}]
        # this should raise a TypeError
        self.assertRaises(
            TypeError,
            setattr,
            self.test_client,
            "users",
            test_value
        )

    def test_users_attribute_elements_accepts_user_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a User object to the users list
        """
        # append
        self.assertRaises(
            TypeError,
            self.test_client.users.append,
            0
        )

        # __setitem__
        self.assertRaises(
            TypeError,
            self.test_client.users.__setitem__,
            0,
            0
        )

    def test_users_argument_is_not_iterable(self):
        """testing if a TypeError will be raised when the given users
        argument is not an instance of list
        """
        test_values = [1, 1.2, "a user"]
        for test_value in test_values:
            self.kwargs["users"] = test_value
            self.assertRaises(TypeError, Client, **self.kwargs)

    def test_users_attribute_is_not_iterable(self):
        """testing if a TypeError will be raised when the users attribute
        is tried to be set to a non-iterable value
        """
        test_values = [1, 1.2, "a user"]
        for test_value in test_values:
            self.assertRaises(
                TypeError, setattr, self.test_client, "users", test_value
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
        self.assertRaises(TypeError, setattr, self.test_client, "users", None)

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
        self.assertRaises(
            TypeError,
            Client,
            **self.kwargs
        )

    def test_projects_attribute_accepts_only_a_list_of_project_objects(self):
        """testing if users attribute accepts only a list of project objects
        """
        test_value = [1, 2.3, [], {}]
        # this should raise a TypeError
        self.assertRaises(
            TypeError,
            setattr,
            self.test_client,
            "projects",
            test_value
        )

    def test_projects_attribute_elements_accepts_Project_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Project object to the projects list
        """
        # append
        self.assertRaises(
            TypeError,
            self.test_client.projects.append,
            0
        )

        # __setitem__
        self.assertRaises(
            TypeError,
            self.test_client.projects.__setitem__,
            0,
            0
        )

    def test_projects_argument_is_not_iterable(self):
        """testing if a TypeError will be raised when the given projects
        argument is not an instance of list
        """
        test_values = [1, 1.2, "a project"]
        for test_value in test_values:
            self.kwargs["projects"] = test_value
            self.assertRaises(TypeError, Project, **self.kwargs)

    def test_projects_attribute_is_not_iterable(self):
        """testing if a TypeError will be raised when the projects attribute
        is tried to be set to a non-iterable value
        """
        test_values = [1, 1.2, "a project"]
        for test_value in test_values:
            self.assertRaises(TypeError, setattr, self.test_client,
                              "projects", test_value)

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
        self.assertRaises(
            TypeError, setattr, self.test_client, "projects", None
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

    def test_project_remove_also_removes_project_from_client(self):
        """testing if removing an user from the users list also removes the
        client from the users companies attribute
        """
        # check if the project is registered with the client
        self.assertTrue(self.test_project1.client is self.test_client)

        # now remove the project from the client
        self.test_client.projects.remove(self.test_project1)

        # now check if project no longer belongs to client
        self.assertFalse(self.test_project1 is self.test_client.projects)

        # assign the project back
        self.test_client.projects.append(self.test_project1)

        # check if the project is in the companies projects list
        self.assertTrue(self.test_project1 in self.test_client.projects)

    def test_equality(self):
        """testing equality of two Client objects
        """
        dep1 = Client(**self.kwargs)
        dep2 = Client(**self.kwargs)

        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("users")
        entity_kwargs.pop("projects")
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
