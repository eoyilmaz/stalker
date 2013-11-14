# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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

import datetime
import unittest2
from stalker.exceptions import CircularDependencyError

from stalker import config

defaults = config.Config()

from stalker import db
from stalker.db.session import DBSession
from stalker import (Entity, Project, Repository, StatusList, Status, Task,
                     Type, User, TimeLog)

from stalker.models.task import CONSTRAIN_END, CONSTRAIN_BOTH

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TaskTester(unittest2.TestCase):
    """Tests the stalker.models.task.Task class
    """

    @classmethod
    def setUpClass(cls):
        """set up tests in class level
        """
        DBSession.remove()
        DBSession.configure(extension=None)

    @classmethod
    def tearDownClass(cls):
        """clean up the test
        """
        DBSession.configure(extension=None)

    def setUp(self):
        """setup the test
        """
        # create a new DBSession
        db.setup({
            "sqlalchemy.url": "sqlite:///:memory:",
            "sqlalchemy.echo": False,
        })

        self.test_status_wip = Status(
            name="Work In Progress",
            code="WIP"
        )

        self.test_status_complete = Status(
            name="Complete",
            code="CMPLT"
        )

        self.test_status_pending_review = Status(
            name="Pending Review",
            code="PNDR"
        )

        self.test_task_status_list = StatusList(
            name="Task Statuses",
            statuses=[self.test_status_wip,
                      self.test_status_pending_review,
                      self.test_status_complete],
            target_entity_type=Task,
        )

        self.test_project_status_list = StatusList(
            name="Project Statuses",
            statuses=[self.test_status_wip,
                      self.test_status_pending_review,
                      self.test_status_complete],
            target_entity_type=Project,
        )

        self.test_movie_project_type = Type(
            name="Movie Project",
            code='movie',
            target_entity_type=Project,
        )

        self.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type=Repository,
        )

        self.test_repository = Repository(
            name="Test Repository",
            type=self.test_repository_type
        )

        self.test_project1 = Project(
            name="Test Project1",
            code='tp1',
            type=self.test_movie_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repository
        )

        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@user1.com",
            password="1234"
        )

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@user2.com",
            password="1234"
        )

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@user3.com",
            password="1234"
        )

        self.test_dependent_task1 = Task(
            name="Dependent Task1",
            project=self.test_project1,
            status_list=self.test_task_status_list,
        )

        self.test_dependent_task2 = Task(
            name="Dependent Task2",
            project=self.test_project1,
            status_list=self.test_task_status_list,
        )

        self.kwargs = {
            'name': 'Modeling',
            'description': 'A Modeling Task',
            'project': self.test_project1,
            'priority': 500,
            'responsible': self.test_user1,
            'resources': [self.test_user1, self.test_user2],
            'watchers': [self.test_user3],
            'bid_timing': 4,
            'bid_unit': 'd',
            'schedule_timing': 1,
            'schedule_unit': 'd',
            'start': datetime.datetime(2013, 4, 8, 13, 0),
            'end': datetime.datetime(2013, 4, 8, 18, 0),
            'depends': [self.test_dependent_task1,
                        self.test_dependent_task2],
            'is_complete': False,
            'time_logs': [],
            'versions': [],
            'is_milestone': False,
            'status': 0,
            'status_list': self.test_task_status_list,
        }

        # create a test Task
        self.test_task = Task(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Task class
        """
        self.assertFalse(Task.__auto_name__)

    def test_priority_argument_is_skipped_defaults_to_task_priority(self):
        """testing if skipping the priority argument will default the priority
        attribute to task_priority.
        """
        self.kwargs.pop("priority")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.priority, defaults.task_priority)

    def test_priority_argument_is_given_as_None_will_default_to_task_priority(self):
        """testing if the priority argument is given as None will default the
        priority attribute to task_priority.
        """
        self.kwargs["priority"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.priority, defaults.task_priority)

    def test_priority_attribute_is_given_as_None_will_default_to_task_priority(self):
        """testing if the priority attribute is given as None will default the
        priority attribute to task_priority.
        """
        self.test_task.priority = None
        self.assertEqual(self.test_task.priority, defaults.task_priority)

    def test_priority_argument_any_given_other_value_then_integer_will_default_to_task_priority(self):
        """testing if any other value then an positive integer for priority
        argument will default the priority attribute to task_priority.
        """
        test_values = ["a324", None, []]

        for test_value in test_values:
            self.kwargs["priority"] = test_value
            new_task = Task(**self.kwargs)
            self.assertEqual(new_task.priority, defaults.task_priority)

    def test_priority_attribute_any_given_other_value_then_integer_will_default_to_task_priority(self):
        """testing if any other value then an positive integer for priority
        attribute will default it to task_priority.
        """
        test_values = ["a324", None, []]

        for test_value in test_values:
            self.test_task.priority = test_value
            self.assertEqual(self.test_task.priority, defaults.task_priority)

    def test_priority_argument_is_negative(self):
        """testing if the priority argument is given as a negative value will
        set the priority attribute to zero.
        """
        self.kwargs["priority"] = -1
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.priority, 0)

    def test_priority_attribute_is_negative(self):
        """testing if the priority attribute is given as a negative value will
        set the priority attribute to zero.
        """
        self.test_task.priority = -1
        self.assertEqual(self.test_task.priority, 0)

    def test_priority_argument_is_too_big(self):
        """testing if the priority argument is given bigger then 1000 will
        clamp the priority attribute value to 1000
        """
        self.kwargs["priority"] = 1001
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.priority, 1000)

    def test_priority_attribute_is_too_big(self):
        """testing if the priority attribute is set to a value bigger than 1000
        will clamp the value to 1000
        """
        self.test_task.priority = 1001
        self.assertEqual(self.test_task.priority, 1000)

    def test_priority_argument_is_float(self):
        """testing if float numbers for prority argument will be converted to
        integer
        """
        test_values = [500.1, 334.23]
        for test_value in test_values:
            self.kwargs["priority"] = test_value
            new_task = Task(**self.kwargs)
            self.assertEqual(new_task.priority, int(test_value))

    def test_priority_attribute_is_float(self):
        """testing if float numbers for priority attribute will be converted to
        integer
        """
        test_values = [500.1, 334.23]
        for test_value in test_values:
            self.test_task.priority = test_value
            self.assertEqual(self.test_task.priority, int(test_value))

    def test_priority_attribute_is_working_properly(self):
        """testing if the priority attribute is working properly
        """
        test_value = 234
        self.test_task.priority = test_value
        self.assertEqual(self.test_task.priority, test_value)

    def test_resources_argument_is_skipped(self):
        """testing if the resources attribute will be an empty list when the
        resources argument is skipped
        """
        self.kwargs.pop("resources")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.resources, [])

    def test_resources_argument_is_None(self):
        """testing if the resources attribute will be an empty list when the
        resources argument is None
        """
        self.kwargs["resources"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.resources, [])

    def test_resources_attribute_is_None(self):
        """testing if a TypeError will be raised whe the resources attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_task, "resources",
                          None)

    def test_resources_argument_is_not_list(self):
        """testing if a TypeError will be raised when the resources argument is
        not a list
        """
        self.kwargs["resources"] = "a resource"
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_resources_attribute_is_not_list(self):
        """testing if a TypeError will be raised when the resources attribute
        is set to any other value then a list
        """
        self.assertRaises(TypeError, setattr, self.test_task, "resources",
                          "a resource")

    def test_resources_argument_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the resources argument is
        set to a list of other values then a User
        """
        self.kwargs["resources"] = ["a", "list", "of", "resources",
                                    self.test_user1]
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_resources_attribute_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the resources attribute
        is set to a list of other values then a User
        """
        self.kwargs["resources"] = ["a", "list", "of", "resources",
                                    self.test_user1]
        self.assertRaises(TypeError, self.test_task, **self.kwargs)

    def test_resources_attribute_is_working_properly(self):
        """testing if the resources attribute is working properly
        """
        test_value = [self.test_user1]
        self.test_task.resources = test_value
        self.assertEqual(self.test_task.resources, test_value)

    def test_resources_argument_backreferences_to_User(self):
        """testing if the User instances passed with the resources argument
        will have the current task in their User.tasks attribute
        """
        # create a couple of new users
        new_user1 = User(
            name="test1",
            login="test1",
            email="test1@test.com",
            password="test1"
        )

        new_user2 = User(
            name="test2",
            login="test2",
            email="test2@test.com",
            password="test2"
        )

        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)

        # now change the resources list
        new_task.resources = [new_user2]
        self.assertIn(new_task, new_user2.tasks)
        self.assertNotIn(new_task, new_user1.tasks)

        # now append the new resource
        new_task.resources.append(new_user1)
        self.assertIn(new_task, new_user1.tasks)

    def test_resources_attribute_backreferences_to_User(self):
        """testing if the User instances passed with the resources argument
        will have the current task in their User.tasks attribute
        """
        # create a new user
        new_user = User(
            name="Test User",
            login="testuser",
            email="testuser@test.com",
            password="testpass"
        )

        # assign it to a newly created task
        #self.kwargs["resources"] = [new_user]
        new_task = Task(**self.kwargs)
        new_task.resources = [new_user]

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user.tasks)

    def test_resources_attribute_will_clear_itself_from_the_previous_Users(self):
        """testing if the resources attribute is updated will clear itself from
        the current resources tasks attribute.
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now update the resources list
        new_task.resources = [new_user3, new_user4]

        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)

        # and if it is not in the previous users tasks
        self.assertNotIn(new_task, new_user1.tasks)
        self.assertNotIn(new_task, new_user2.tasks)

    def test_resources_attribute_will_handle_append(self):
        """testing if the resources attribute will handle appending users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now update the resources list
        new_task.resources.append(new_user3)
        new_task.resources.append(new_user4)

        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)

    def test_resources_attribute_will_handle_extend(self):
        """testing if the resources attribute will handle extendeding users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now update the resources list
        new_task.resources.extend([new_user3, new_user4])

        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)

    def test_resources_attribute_will_handle___setitem__(self):
        """testing if the resources attribute will handle __setitem__ing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now update the resources list
        new_task.resources[0] = new_user3
        new_task.resources[1] = new_user4

        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)

        # and check if the first and second tasks doesn't have task anymore
        self.assertNotIn(new_task, new_user1.tasks)
        self.assertNotIn(new_task, new_user2.tasks)

    def test_resources_attribute_will_handle___setslice__(self):
        """testing if the resources attribute will handle __setslice__ing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now update the resources list
        new_task.resources[1:2] = [new_user3, new_user4]

        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)

        # and check if the first and second tasks doesn't have task anymore
        self.assertNotIn(new_task, new_user2.tasks)

    def test_resources_attribute_will_handle_insert(self):
        """testing if the resources attribute will handle inserting users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now update the resources list
        new_task.resources.insert(0, new_user3)
        new_task.resources.insert(0, new_user4)

        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)

    def test_resources_attribute_will_handle___add__(self):
        """testing if the resources attribute will handle __add__ing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now update the resources list
        new_task.resources = new_task.resources + [new_user3, new_user4]

        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)

    def test_resources_attribute_will_handle___iadd__(self):
        """testing if the resources attribute will handle __iadd__ing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass")

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass")

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now update the resources list
        new_task.resources += [new_user3, new_user4]

        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)

    def test_resources_attribute_will_handle_pop(self):
        """testing if the resources attribute will handle popping users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now pop the resources
        new_task.resources.pop(0)
        self.assertNotIn(new_task, new_user1.tasks)

        new_task.resources.pop()
        self.assertNotIn(new_task, new_user2.tasks)

    def test_resources_attribute_will_handle_remove(self):
        """testing if the resources attribute will handle removing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)

        # now pop the resources
        new_task.resources.remove(new_user1)
        self.assertNotIn(new_task, new_user1.tasks)

        new_task.resources.remove(new_user2)
        self.assertNotIn(new_task, new_user2.tasks)

    def test_watchers_argument_is_skipped(self):
        """testing if the watchers attribute will be an empty list when the
        watchers argument is skipped
        """
        self.kwargs.pop("watchers")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.watchers, [])

    def test_watchers_argument_is_None(self):
        """testing if the watchers attribute will be an empty list when the
        watchers argument is None
        """
        self.kwargs["watchers"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.watchers, [])

    def test_watchers_attribute_is_None(self):
        """testing if a TypeError will be raised whe the watchers attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_task, "watchers",
                          None)

    def test_watchers_argument_is_not_list(self):
        """testing if a TypeError will be raised when the watchers argument is
        not a list
        """
        self.kwargs["watchers"] = "a resource"
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_watchers_attribute_is_not_list(self):
        """testing if a TypeError will be raised when the watchers attribute
        is set to any other value then a list
        """
        self.assertRaises(TypeError, setattr, self.test_task, "watchers",
                          "a resource")

    def test_watchers_argument_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the watchers argument is
        set to a list of other values then a User
        """
        self.kwargs["watchers"] = ["a", "list", "of", "watchers",
                                   self.test_user1]
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_watchers_attribute_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the watchers attribute
        is set to a list of other values then a User
        """
        self.kwargs["watchers"] = ["a", "list", "of", "watchers",
                                   self.test_user1]
        self.assertRaises(TypeError, self.test_task, **self.kwargs)

    def test_watchers_attribute_is_working_properly(self):
        """testing if the watchers attribute is working properly
        """
        test_value = [self.test_user1]
        self.test_task.watchers = test_value
        self.assertEqual(self.test_task.watchers, test_value)

    def test_watchers_argument_back_references_to_User(self):
        """testing if the User instances passed with the watchers argument
        will have the current task in their User.watching attribute
        """
        # create a couple of new users
        new_user1 = User(
            name="test1",
            login="test1",
            email="test1@test.com",
            password="test1"
        )

        new_user2 = User(
            name="test2",
            login="test2",
            email="test2@test.com",
            password="test2"
        )

        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.watching)

        # now change the watchers list
        new_task.watchers = [new_user2]
        self.assertIn(new_task, new_user2.watching)
        self.assertNotIn(new_task, new_user1.watching)

        # now append the new user
        new_task.watchers.append(new_user1)
        self.assertIn(new_task, new_user1.watching)

    def test_watchers_attribute_back_references_to_User(self):
        """testing if the User instances passed with the watchers argument will
        have the current task in their User.watching attribute
        """
        # create a new user
        new_user = User(
            name="Test User",
            login="testuser",
            email="testuser@test.com",
            password="testpass"
        )

        # assign it to a newly created task
        #self.kwargs["watchers"] = [new_user]
        new_task = Task(**self.kwargs)
        new_task.watchers = [new_user]

        # now check if the user has the task in its watching list
        self.assertIn(new_task, new_user.watching)

    def test_watchers_attribute_will_clear_itself_from_the_previous_Users(self):
        """testing if the watchers attribute is updated will clear itself from
        the current watchers watching attribute.
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its watching list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now update the watchers list
        new_task.watchers = [new_user3, new_user4]

        # now check if the new watchers has the task in their watching
        # attribute
        self.assertIn(new_task, new_user3.watching)
        self.assertIn(new_task, new_user4.watching)

        # and if it is not in the previous users watching list
        self.assertNotIn(new_task, new_user1.watching)
        self.assertNotIn(new_task, new_user2.watching)

    def test_watchers_attribute_will_handle_append(self):
        """testing if the watchers attribute will handle appending users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now update the watchers list
        new_task.watchers.append(new_user3)
        new_task.watchers.append(new_user4)

        # now check if the new watchers has the task in their watching
        # attribute
        self.assertIn(new_task, new_user3.watching)
        self.assertIn(new_task, new_user4.watching)

    def test_watchers_attribute_will_handle_extend(self):
        """testing if the watchers attribute will handle extending users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now update the watchers list
        new_task.watchers.extend([new_user3, new_user4])

        # now check if the new watchers has the task in their watching
        # attribute
        self.assertIn(new_task, new_user3.watching)
        self.assertIn(new_task, new_user4.watching)

    def test_watchers_attribute_will_handle___setitem__(self):
        """testing if the watchers attribute will handle __setitem__ing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its watching list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now update the watchers list
        new_task.watchers[0] = new_user3
        new_task.watchers[1] = new_user4

        # now check if the new watchers has the task in their watching
        # attribute
        self.assertIn(new_task, new_user3.watching)
        self.assertIn(new_task, new_user4.watching)

        # and check if the first and second users doesn't have task anymore
        self.assertNotIn(new_task, new_user1.watching)
        self.assertNotIn(new_task, new_user2.watching)

    def test_watchers_attribute_will_handle___setslice__(self):
        """testing if the watchers attribute will handle __setslice__ing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its watching list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now update the watchers list
        new_task.watchers[1:2] = [new_user3, new_user4]

        # now check if the new watchers has the task in their tasks attribute
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user3.watching)
        self.assertIn(new_task, new_user4.watching)

        # and check if the users watching list doesn't have the task anymore
        self.assertNotIn(new_task, new_user2.watching)

    def test_watchers_attribute_will_handle_insert(self):
        """testing if the watchers attribute will handle inserting users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its watching list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now update the watchers list
        new_task.watchers.insert(0, new_user3)
        new_task.watchers.insert(0, new_user4)

        # now check if the new watchers has the task in their watching
        # attribute
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)
        self.assertIn(new_task, new_user3.watching)
        self.assertIn(new_task, new_user4.watching)

    def test_watchers_attribute_will_handle___add__(self):
        """testing if the watchers attribute will handle __add__ing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its watching list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now update the watchers list
        new_task.watchers = new_task.watchers + [new_user3, new_user4]

        # now check if the new watchers has the task in their watching
        # attribute
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)
        self.assertIn(new_task, new_user3.watching)
        self.assertIn(new_task, new_user4.watching)

    def test_watchers_attribute_will_handle___iadd__(self):
        """testing if the watchers attribute will handle __iadd__ing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass")

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass")

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its watching list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now update the watchers list
        new_task.watchers += [new_user3, new_user4]

        # now check if the new watchers has the task in their watching
        # attribute
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)
        self.assertIn(new_task, new_user3.watching)
        self.assertIn(new_task, new_user4.watching)

    def test_watchers_attribute_will_handle_pop(self):
        """testing if the watchers attribute will handle popping users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its watching list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now pop the watchers
        new_task.watchers.pop(0)
        self.assertNotIn(new_task, new_user1.watching)

        new_task.watchers.pop()
        self.assertNotIn(new_task, new_user2.watching)

    def test_watchers_attribute_will_handle_remove(self):
        """testing if the watchers attribute will handle removing users
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        self.kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)

        # now check if the user has the task in its watching list
        self.assertIn(new_task, new_user1.watching)
        self.assertIn(new_task, new_user2.watching)

        # now pop the watchers
        new_task.watchers.remove(new_user1)
        self.assertNotIn(new_task, new_user1.watching)

        new_task.watchers.remove(new_user2)
        self.assertNotIn(new_task, new_user2.watching)

    def test_schedule_timing_argument_skipped(self):
        """testing if the schedule_timing attribute will be equal to the
        stalker.config.Config.timing_resolution.seconds/3600 if the
        schedule_timing argument is skipped
        """
        self.kwargs.pop("schedule_timing")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_timing,
                         defaults.timing_resolution.seconds / 3600)

    def test_schedule_timing_argument_is_None(self):
        """testing if the schedule_timing attribute will be equal to the
        stalker.config.Config.timing_resolution.seconds/3600 if the
        schedule_timing argument is None
        """
        self.kwargs["schedule_timing"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_timing,
                         defaults.timing_resolution.seconds / 3600)

    def test_schedule_timing_attribute_is_set_to_None(self):
        """testing if the schedule_timing attribute will be equal to the
        stalker.config.Config.timing_resolution.seconds/3600 if it is set to
        None
        """
        self.test_task.schedule_timing = None
        self.assertEqual(self.test_task.schedule_timing,
                         defaults.timing_resolution.seconds / 3600)

    def test_schedule_timing_argument_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised when the schedule_timing
        is not an integer or float
        """
        self.kwargs["schedule_timing"] = '10d'
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_schedule_timing_attribute_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised when the schedule_timing
        attribute is not set to an integer or float
        """
        self.assertRaises(TypeError, setattr, self.test_task,
                          'schedule_timing', '10d')

    def test_schedule_timing_attribute_is_working_properly(self):
        """testing if the schedule_timing attribute is working properly
        """
        test_value = 18
        self.test_task.schedule_timing = test_value
        self.assertEqual(self.test_task.schedule_timing, test_value)

    def test_schedule_unit_argument_skipped(self):
        """testing if the schedule_unit attribute will be 'h' if the
        schedule_unit argument is skipped
        """
        self.kwargs.pop("schedule_unit")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_unit, 'h')

    def test_schedule_unit_argument_is_None(self):
        """testing if the schedule_unit attribute will be 'h' if the
        schedule_unit argument is None
        """
        self.kwargs["schedule_unit"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_unit, 'h')

    def test_schedule_unit_attribute_is_set_to_None(self):
        """testing if the schedule_unit attribute will be 'h' if it is set to
        None
        """
        self.test_task.schedule_unit = None
        self.assertEqual(self.test_task.schedule_unit, 'h')

    def test_schedule_unit_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the schedule_unit is not
        an integer
        """
        self.kwargs["schedule_unit"] = 10
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_schedule_unit_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the schedule_unit
        attribute is not set to a string
        """
        self.assertRaises(TypeError, setattr, self.test_task, 'schedule_unit',
                          23)

    def test_schedule_unit_attribute_is_working_properly(self):
        """testing if the schedule_unit attribute is working properly
        """
        test_value = 'w'
        self.test_task.schedule_unit = test_value
        self.assertEqual(self.test_task.schedule_unit, test_value)

    def test_schedule_unit_argument_value_is_not_in_defaults_datetime_units(self):
        """testing if a ValueError will be raised when the schedule_unit value
        is not in stalker.config.Config.datetime_units list
        """
        self.kwargs['schedule_unit'] = 'os'
        self.assertRaises(ValueError, Task, **self.kwargs)

    def test_schedule_unit_attribute_value_is_not_in_defaults_datetime_units(self):
        """testing if a ValueError will be raised when it is set to a value
        which is not in stalker.config.Config.datetime_units list
        """
        self.assertRaises(ValueError, setattr, self.test_task, 'schedule_unit',
                          'so')

    def test_depends_argument_is_skipped_depends_attribute_is_empty_list(self):
        """testing if the depends attribute is an empty list when the depends
        argument is skipped
        """
        self.kwargs.pop("depends")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.depends, [])

    def test_depends_argument_is_none_depends_attribute_is_empty_list(self):
        """testing if the depends attribute is an empty list when the depends
        argument is None
        """
        self.kwargs["depends"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.depends, [])

    def test_depends_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the depends argument is
        not a list
        """
        self.kwargs["depends"] = self.test_dependent_task1
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_depends_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the depends attribute is
        set to something else then a list
        """
        self.assertRaises(TypeError, setattr, self.test_task, "depends",
                          self.test_dependent_task1)

    def test_depends_argument_is_a_list_of_other_objects_than_a_Task(self):
        """testing if a TypeError will be raised when the depends argument is
        a list of other typed objects than Task
        """
        test_value = ["a", "dependent", "task", 1, 1.2]
        self.kwargs["depends"] = test_value
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_depends_attribute_is_a_list_of_other_objects_than_a_Task(self):
        """testing if a TypeError will be raised when the depends attribute is
        set to a list of other typed objects than Task
        """
        test_value = ["a", "dependent", "task", 1, 1.2]
        self.assertRaises(TypeError, setattr, self.test_task, "depends",
                          test_value)

    def test_depends_attribute_doesnt_allow_simple_cyclic_dependencies(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has a simple circular dependency in dependencies
        """
        # create two new tasks A, B
        # make B dependent to A
        # and make A dependent to B
        # and expect a CircularDependencyError
        self.kwargs["depends"] = None

        task_a = Task(**self.kwargs)
        task_b = Task(**self.kwargs)

        task_b.depends = [task_a]

        self.assertRaises(CircularDependencyError, setattr, task_a, "depends",
                          [task_b])

    def test_depends_attribute_doesnt_allow_cyclic_dependencies(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has a circular dependency in dependencies
        """
        # create three new tasks A, B, C
        # make B dependent to A
        # make C dependent to B
        # and make A dependent to C
        # and expect a CircularDependencyError
        self.kwargs["depends"] = None

        self.kwargs["name"] = "taskA"
        task_a = Task(**self.kwargs)

        self.kwargs["name"] = "taskB"
        task_b = Task(**self.kwargs)

        self.kwargs["name"] = "taskC"
        task_c = Task(**self.kwargs)

        task_b.depends = [task_a]
        task_c.depends = [task_b]

        self.assertRaises(CircularDependencyError, setattr, task_a, "depends",
                          [task_c])

    def test_depends_attribute_doesnt_allow_more_deeper_cyclic_dependencies(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has a deeper circular dependency in dependencies
        """
        # create new tasks A, B, C, D
        # make B dependent to A
        # make C dependent to B
        # make D dependent to C
        # and make A dependent to D
        # and expect a CircularDependencyError
        self.kwargs["depends"] = None

        self.kwargs["name"] = "taskA"
        task_a = Task(**self.kwargs)
        self.kwargs["name"] = "taskB"
        task_b = Task(**self.kwargs)
        self.kwargs["name"] = "taskC"
        task_c = Task(**self.kwargs)
        self.kwargs["name"] = "taskD"
        task_d = Task(**self.kwargs)

        task_b.depends = [task_a]
        task_c.depends = [task_b]
        task_d.depends = [task_c]

        self.assertRaises(CircularDependencyError, setattr, task_a, "depends",
                          [task_d])

    def test_depends_argument_cyclic_dependency_bug_2(self):
        """testing if a CircularDependencyError will be raised in the following
        case:
          T1 is parent of T2
          T3 depends to T1
          T2 depends to T3
        """

        self.kwargs['name'] = 'T1'
        t1 = Task(**self.kwargs)

        self.kwargs['name'] = 'T3'
        t3 = Task(**self.kwargs)

        t3.depends.append(t1)

        self.kwargs['name'] = 'T2'
        self.kwargs['parent'] = t1
        self.kwargs['depends'] = [t3]

        # the following should generate the CircularDependencyError
        self.assertRaises(CircularDependencyError, Task, **self.kwargs)

    def test_depends_argument_doesnt_allow_one_of_the_parents_of_the_task(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has one of the parents of this task
        """
        # create two new tasks A, B
        # make A parent to B
        # and make B dependent to A
        # and expect a CircularDependencyError
        self.kwargs["depends"] = None

        task_a = Task(**self.kwargs)
        task_b = Task(**self.kwargs)
        task_c = Task(**self.kwargs)

        task_b.parent = task_a
        task_a.parent = task_c

        self.assertIn(task_b, task_a.children)
        self.assertIn(task_a, task_c.children)

        self.assertRaises(CircularDependencyError, setattr, task_b, 'depends',
                          [task_a])
        self.assertRaises(CircularDependencyError, setattr, task_b, 'depends',
                          [task_c])

    def test_depends_argument_is_working_properly(self):
        """testing if the depends argument is working properly
        """
        self.kwargs['depends'] = None
        task_a = Task(**self.kwargs)
        task_b = Task(**self.kwargs)
        self.kwargs['depends'] = [task_a, task_b]
        task_c = Task(**self.kwargs)
        self.assertIn(task_a, task_c.depends)
        self.assertIn(task_b, task_c.depends)
        self.assertEqual(len(task_c.depends), 2)

    def test_depends_attribute_is_working_properly(self):
        """testing if the depends attribute is working properly
        """
        self.kwargs['depends'] = None
        task_a = Task(**self.kwargs)
        task_b = Task(**self.kwargs)
        task_c = Task(**self.kwargs)

        task_a.depends = [task_b]
        task_a.depends.append(task_c)

        self.assertIn(task_b, task_a.depends)
        self.assertIn(task_c, task_a.depends)

    def test_is_complete_attribute_is_None(self):
        """testing if the is_complete attribute will be False when set to None
        """
        self.test_task.is_complete = None
        self.assertEqual(self.test_task.is_complete, False)

    def test_is_complete_attribute_evaluates_the_given_value_to_a_bool(self):
        """testing if the is_complete attribute is evaluated correctly to a
        bool value when set to anything other than a bool value.
        """
        test_values = [1, 0, 1.2, "A string", "", [], [1]]
        for test_value in test_values:
            self.test_task.is_complete = test_value
            self.assertEqual(self.test_task.is_complete, bool(test_value))

    def test_percent_complete_attribute_is_read_only(self):
        """testing if the percent_complete attribute is a read-only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_task,
                          'percent_complete', 32)

    def test_percent_complete_attribute_is_working_properly_for_a_leaf_task(self):
        """testing if the percent_complete attribute is working properly for a
        leaf task
        """
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task.time_logs = []
        book1 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )

        self.assertIn(book1, self.test_task.time_logs)

        book2 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[1],
            start=now,
            end=now + td(hours=12)
        )
        self.assertIn(book2, self.test_task.time_logs)
        self.assertEqual(self.test_task.total_logged_seconds, 20 * 3600)
        self.assertEqual(self.test_task.percent_complete, 100)

    def test_percent_complete_attribute_is_working_properly_for_a_container_task(self):
        """testing if the percent complete attribute is working properly for a
        container task
        """
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        parent_task = Task(**self.kwargs)

        self.test_task.time_logs = []
        book1 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[0],
            start=now,
            end=now + td(hours=2)
        )

        self.assertIn(book1, self.test_task.time_logs)

        book2 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[1],
            start=now,
            end=now + td(hours=5)
        )
        self.test_task.parent = parent_task

        self.assertIn(book2, self.test_task.time_logs)
        self.assertEqual(self.test_task.total_logged_seconds, 7 * 3600)
        self.assertEqual(self.test_task.schedule_seconds, 9 * 3600)
        self.assertAlmostEqual(
            self.test_task.percent_complete,
            77.7777778,
            delta=0.01
        )
        self.assertAlmostEqual(
            parent_task.percent_complete,
            77.7777778,
            delta=0.01
        )

    def test_is_milestone_argument_is_skipped(self):
        """testing if the default value of the is_milestone attribute is going
        to be False when the is_milestone argument is skipped
        """
        self.kwargs.pop("is_milestone")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.is_milestone, False)

    def test_is_milestone_argument_is_None(self):
        """testing if the is_milestone attribute will be set to False when the
        is_milestone argument is given as None
        """
        self.kwargs["is_milestone"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.is_milestone, False)

    def test_is_milestone_attribute_is_None(self):
        """testing if the is_milestone attribute will be False when set to None
        """
        self.test_task.is_milestone = None
        self.assertEqual(self.test_task.is_milestone, False)

    def test_is_milestone_argument_evaluates_the_given_value_to_a_bool(self):
        """testing if the is_milestone attribute is evaluated correctly to a
        bool value when the is_milestone argument is anything other than a bool
        value.
        """
        test_values = [1, 0, 1.2, "A string", "", [], [1]]
        for i, test_value in enumerate(test_values):
            self.kwargs["name"] = "test" + str(i)
            self.kwargs["is_milestone"] = test_value
            new_task = Task(**self.kwargs)
            self.assertEqual(new_task.is_milestone, bool(test_value))

    def test_is_milestone_attribute_evaluates_the_given_value_to_a_bool(self):
        """testing if the is_milestone attribute is evaluated correctly to a
        bool value when set to anything other than a bool value.
        """
        test_values = [1, 0, 1.2, "A string", "", [], [1]]
        for test_value in test_values:
            self.test_task.is_milestone = test_value
            self.assertEqual(self.test_task.is_milestone, bool(test_value))

    def test_is_milestone_argument_makes_the_resources_list_an_empty_list(self):
        """testing if the resources will be an empty list when the is_milestone
        argument is given as True
        """
        self.kwargs["is_milestone"] = True
        self.kwargs["resources"] = [self.test_user1,
                                    self.test_user2]
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.resources, [])

    def test_is_milestone_attribute_makes_the_resource_list_an_empty_list(self):
        """testing if the resources will be an empty list when the is_milestone
        attribute is given as True
        """
        self.test_task.resources = [self.test_user1, self.test_user2]
        self.test_task.is_milestone = True
        self.assertEqual(self.test_task.resources, [])

    def test_time_logs_attribute_is_None(self):
        """testing if a TypeError will be raised when the time_logs attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_task, "time_logs",
                          None)

    def test_time_logs_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the time_logs attribute
        is not set to a list
        """
        self.assertRaises(TypeError, setattr, self.test_task, "time_logs", 123)

    def test_time_logs_attribute_is_not_a_list_of_TimeLog_instances(self):
        """testing if a TypeError will be raised when the time_logs attribute
        is not a list of TimeLog instances
        """
        self.assertRaises(TypeError, setattr, self.test_task, "time_logs",
                          [1, "1", 1.2, "a time_log", []])

    def test_time_logs_attribute_is_working_properly(self):
        """testing if the time_log attribute is working properly
        """
        now = datetime.datetime.now()
        dt = datetime.timedelta

        new_time_log1 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[0],
            start=now + dt(100),
            end=now + dt(101)
        )

        new_time_log2 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[0],
            start=now + dt(101),
            end=now + dt(102)
        )

        # create a new task
        self.kwargs['name'] = 'New Task'
        new_task = Task(**self.kwargs)

        # create a new TimeLog for that task
        new_time_log3 = TimeLog(
            task=new_task,
            resource=new_task.resources[0],
            start=now + dt(102),
            end=now + dt(103)
        )

        DBSession.add_all([new_time_log1, new_time_log2, new_time_log3])
        DBSession.commit()

        # check if everything is in place
        self.assertIn(new_time_log1, self.test_task.time_logs)
        self.assertIn(new_time_log2, self.test_task.time_logs)
        self.assertIn(new_time_log3, new_task.time_logs)

        # now move the time_log to test_task
        self.test_task.time_logs.append(new_time_log3)

        # check if new_time_log3 is in test_task
        self.assertIn(new_time_log3, self.test_task.time_logs)

        # there needs to be a database session commit to remove the time_log
        # from the previous tasks time_logs attribute

        DBSession.commit()

        self.assertIn(new_time_log3, self.test_task.time_logs)
        self.assertNotIn(new_time_log3, new_task.time_logs)

    # def test_total_logged_seconds_is_a_read_only_attribute(self):
    #     """testing if the total_logged_seconds is a read only attribute
    #     """
    #     self.assertRaises(AttributeError, setattr, self.test_task,
    #                       'total_logged_seconds', 33)

    def test_total_logged_seconds_is_the_sum_of_all_time_logs(self):
        """testing if the total_logged_seconds is the sum of all time_logs in
        hours
        """
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task.time_logs = []
        book1 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )

        self.assertIn(book1, self.test_task.time_logs)

        book2 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[1],
            start=now,
            end=now + td(hours=12)
        )
        self.assertIn(book2, self.test_task.time_logs)
        self.assertEqual(self.test_task.total_logged_seconds, 20 * 3600)

    def test_total_logged_seconds_is_the_sum_of_all_time_logs_of_children_for_a_container_task(self):
        """testing if the total_logged_seconds is the sum of all time_logs of
        the child tasks for a container task
        """
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.kwargs.pop('schedule_timing')
        self.kwargs.pop('schedule_unit')
        parent_task = Task(**self.kwargs)

        self.test_task.parent = parent_task

        self.test_task.time_logs = []
        book1 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )

        self.assertIn(book1, self.test_task.time_logs)

        book2 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[1],
            start=now,
            end=now + td(hours=12)
        )
        self.assertIn(book2, self.test_task.time_logs)
        self.assertEqual(self.test_task.total_logged_seconds, 20 * 3600)
        self.assertEqual(parent_task.total_logged_seconds, 20 * 3600)

    def test_total_logged_seconds_is_the_sum_of_all_time_logs_of_children_for_a_container_task_deeper(self):
        """testing if the total_logged_seconds is the sum of all time_logs of
        the child tasks for a container task (test deeper)
        """
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.kwargs.pop('schedule_timing')
        self.kwargs.pop('schedule_unit')
        parent_task1 = Task(**self.kwargs)
        self.assertEqual(parent_task1.total_logged_seconds, 0)
        parent_task2 = Task(**self.kwargs)
        self.assertEqual(parent_task2.total_logged_seconds, 0)

        # create some other child
        child = Task(**self.kwargs)
        self.assertEqual(child.total_logged_seconds, 0)
        # create a TimeLog for that child
        tlog1 = TimeLog(
            task=child,
            resource=child.resources[0],
            start=now - td(hours=50),
            end=now - td(hours=40)
        )
        self.assertEqual(child.total_logged_seconds, 10 * 3600)
        parent_task2.children.append(child)
        self.assertEqual(parent_task2.total_logged_seconds, 10 * 3600)

        # self.test_task.parent = parent_task
        parent_task1.children.append(self.test_task)
        self.assertEqual(parent_task1.total_logged_seconds, 0)

        parent_task1.parent = parent_task2
        self.assertEqual(parent_task2.total_logged_seconds, 10 * 3600)

        self.test_task.time_logs = []
        book1 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )

        self.assertIn(book1, self.test_task.time_logs)
        self.assertEqual(self.test_task.total_logged_seconds, 8 * 3600)
        self.assertEqual(parent_task1.total_logged_seconds, 8 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 18 * 3600)

        book2 = TimeLog(
            task=self.test_task,
            resource=self.test_task.resources[1],
            start=now,
            end=now + td(hours=12)
        )
        self.assertEqual(self.test_task.total_logged_seconds, 20 * 3600)
        self.assertEqual(parent_task1.total_logged_seconds, 20 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 30 * 3600)

    def test_total_logged_seconds_attribute_is_working_properly_for_a_container_task_when_the_time_log_of_child_is_changed(self):
        """testing if the total_logged_seconds attribute is working properly
        for a container task when one of the time logs of one of the children
        of the task is changed
        """
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        parent_task = Task(**self.kwargs)
        child_task = Task(**self.kwargs)
        parent_task.children.append(child_task)

        tlog1 = TimeLog(
            task=child_task,
            resource=child_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )

        self.assertEqual(
            parent_task.total_logged_seconds, 8 * 60 * 60
        )

        # now update the time log
        tlog1.end = now + td(hours=16)
        self.assertEqual(
            parent_task.total_logged_seconds, 16 * 60 * 60
        )

    def test_schedule_seconds_is_working_properly_for_an_effort_based_task_no_studio(self):
        """testing if schedule_seconds attribute is working properly for a
        effort based task on an environment where there are no studio
        """
        # no studio, using defaults
        self.kwargs['schedule_model'] = 'effort'

        self.kwargs['schedule_timing'] = 10
        self.kwargs['schedule_unit'] = 'h'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds, 10 * 3600)

        self.kwargs['schedule_timing'] = 23
        self.kwargs['schedule_unit'] = 'd'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         23 * defaults.daily_working_hours * 3600)

        self.kwargs['schedule_timing'] = 2
        self.kwargs['schedule_unit'] = 'w'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2 * defaults.weekly_working_hours * 3600)

        self.kwargs['schedule_timing'] = 2.5
        self.kwargs['schedule_unit'] = 'm'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2.5 * 4 * defaults.weekly_working_hours * 3600)

        self.kwargs['schedule_timing'] = 3.1
        self.kwargs['schedule_unit'] = 'y'
        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.schedule_seconds,
            3.1 * defaults.yearly_working_days * defaults.daily_working_hours * 3600
        )

    def test_schedule_seconds_is_working_properly_for_an_effort_based_task_with_studio(self):
        """testing if schedule_seconds attribute is working properly for a
        effort based task where there is a studio present
        """
        # no studio, using defaults
        from stalker import Studio

        studio = Studio(name='Test Studio')

        self.kwargs['schedule_model'] = 'effort'

        self.kwargs['schedule_timing'] = 10
        self.kwargs['schedule_unit'] = 'h'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds, 10 * 3600)

        self.kwargs['schedule_timing'] = 23
        self.kwargs['schedule_unit'] = 'd'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         23 * studio.daily_working_hours * 3600)

        self.kwargs['schedule_timing'] = 2
        self.kwargs['schedule_unit'] = 'w'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2 * studio.weekly_working_hours * 3600)

        self.kwargs['schedule_timing'] = 2.5
        self.kwargs['schedule_unit'] = 'm'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2.5 * 4 * studio.weekly_working_hours * 3600)

        self.kwargs['schedule_timing'] = 3.1
        self.kwargs['schedule_unit'] = 'y'
        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.schedule_seconds,
            3.1 * studio.yearly_working_days * studio.daily_working_hours *
            3600
        )

    def test_schedule_seconds_is_working_properly_for_a_container_task(self):
        """testing if schedule_seconds attribute is working properly for a
        container task
        """
        # no studio, using defaults
        parent_task = Task(**self.kwargs)

        self.kwargs['schedule_model'] = 'effort'

        self.kwargs['schedule_timing'] = 10
        self.kwargs['schedule_unit'] = 'h'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds, 10 * 3600)

        self.kwargs['schedule_timing'] = 23
        self.kwargs['schedule_unit'] = 'd'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         23 * defaults.daily_working_hours * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600)

        self.kwargs['schedule_timing'] = 2
        self.kwargs['schedule_unit'] = 'w'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2 * defaults.weekly_working_hours * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         2 * defaults.weekly_working_hours * 3600)

        self.kwargs['schedule_timing'] = 2.5
        self.kwargs['schedule_unit'] = 'm'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2.5 * 4 * defaults.weekly_working_hours * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         2 * defaults.weekly_working_hours * 3600 +
                         2.5 * 4 * defaults.weekly_working_hours * 3600)

        self.kwargs['schedule_timing'] = 3.1
        self.kwargs['schedule_unit'] = 'y'
        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.schedule_seconds,
            3.1 * defaults.yearly_working_days * defaults.daily_working_hours *
            3600
        )
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         2 * defaults.weekly_working_hours * 3600 +
                         2.5 * 4 * defaults.weekly_working_hours * 3600 +
                         3.1 * defaults.yearly_working_days *
                         defaults.daily_working_hours * 3600)

    def test_schedule_seconds_is_working_properly_for_a_container_task_when_the_child_is_updated(self):
        """testing if schedule_seconds attribute is working properly for a
        container task
        """
        # no studio, using defaults
        parent_task = Task(**self.kwargs)

        self.kwargs['schedule_model'] = 'effort'

        self.kwargs['schedule_timing'] = 10
        self.kwargs['schedule_unit'] = 'h'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds, 10 * 3600)

        # update the schedule_timing of the child
        new_task.schedule_timing = 5
        self.assertEqual(new_task.schedule_seconds, 5 * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds, 5 * 3600)

        # update it back to 10 hours
        new_task.schedule_timing = 10
        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds, 10 * 3600)

        self.kwargs['schedule_timing'] = 23
        self.kwargs['schedule_unit'] = 'd'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         23 * defaults.daily_working_hours * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600)

        self.kwargs['schedule_timing'] = 2
        self.kwargs['schedule_unit'] = 'w'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2 * defaults.weekly_working_hours * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         2 * defaults.weekly_working_hours * 3600)

        self.kwargs['schedule_timing'] = 2.5
        self.kwargs['schedule_unit'] = 'm'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2.5 * 4 * defaults.weekly_working_hours * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         2 * defaults.weekly_working_hours * 3600 +
                         2.5 * 4 * defaults.weekly_working_hours * 3600)

        self.kwargs['schedule_timing'] = 3.1
        self.kwargs['schedule_unit'] = 'y'
        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.schedule_seconds,
            3.1 * defaults.yearly_working_days * defaults.daily_working_hours *
            3600
        )
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         2 * defaults.weekly_working_hours * 3600 +
                         2.5 * 4 * defaults.weekly_working_hours * 3600 +
                         3.1 * defaults.yearly_working_days *
                         defaults.daily_working_hours * 3600)

    def test_schedule_seconds_is_working_properly_for_a_container_task_when_the_child_is_updated_deeper(self):
        """testing if schedule_seconds attribute is working properly for a
        container task
        """
        # no studio, using defaults
        parent_task1 = Task(**self.kwargs)
        self.assertEqual(parent_task1.schedule_seconds, 9 * 3600)

        parent_task2 = Task(**self.kwargs)
        self.assertEqual(parent_task2.schedule_seconds, 9 * 3600)
        parent_task2.schedule_timing = 5
        self.assertEqual(parent_task2.schedule_seconds, 5 * 9 * 3600)
        parent_task2.schedule_unit = 'h'
        self.assertEqual(parent_task2.schedule_seconds, 5 * 3600)

        parent_task1.parent = parent_task2
        self.assertEqual(parent_task2.schedule_seconds, 9 * 3600)

        # create another child task for parent_task2
        child_task = Task(**self.kwargs)
        child_task.schedule_timing = 10
        child_task.schedule_unit = 'h'
        self.assertEqual(child_task.schedule_seconds, 10 * 3600)

        parent_task2.children.append(child_task)
        self.assertEqual(parent_task2.schedule_seconds, 10 * 3600 + 9 * 3600)

        self.kwargs['schedule_model'] = 'effort'
        self.kwargs['schedule_timing'] = 10
        self.kwargs['schedule_unit'] = 'h'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds, 10 * 3600)
        self.assertEqual(parent_task2.schedule_seconds, 10 * 3600 + 10 * 3600)

        # update the schedule_timing of the child
        new_task.schedule_timing = 5
        self.assertEqual(new_task.schedule_seconds, 5 * 3600)
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds, 5 * 3600)
        self.assertEqual(parent_task2.schedule_seconds, 5 * 3600 + 10 * 3600)

        # update it back to 10 hours
        new_task.schedule_timing = 10
        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds, 10 * 3600)
        self.assertEqual(parent_task2.schedule_seconds, 10 * 3600 + 10 * 3600)

        self.kwargs['schedule_timing'] = 23
        self.kwargs['schedule_unit'] = 'd'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         23 * defaults.daily_working_hours * 3600)
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600)
        self.assertEqual(parent_task2.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         10 * 3600)

        self.kwargs['schedule_timing'] = 2
        self.kwargs['schedule_unit'] = 'w'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2 * defaults.weekly_working_hours * 3600)
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         2 * defaults.weekly_working_hours * 3600)

        # update it to 1 week
        new_task.schedule_timing = 1
        self.assertEqual(parent_task1.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         1 * defaults.weekly_working_hours * 3600)
        self.assertEqual(parent_task2.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         1 * defaults.weekly_working_hours * 3600 + 10 * 3600)

        self.kwargs['schedule_timing'] = 2.5
        self.kwargs['schedule_unit'] = 'm'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_seconds,
                         2.5 * 4 * defaults.weekly_working_hours * 3600)
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         1 * defaults.weekly_working_hours * 3600 +
                         2.5 * 4 * defaults.weekly_working_hours * 3600)
        self.assertEqual(parent_task2.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         1 * defaults.weekly_working_hours * 3600 +
                         2.5 * 4 * defaults.weekly_working_hours * 3600 +
                         10 * 3600)

        self.kwargs['schedule_timing'] = 3.1
        self.kwargs['schedule_unit'] = 'y'
        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.schedule_seconds,
            3.1 * defaults.yearly_working_days * defaults.daily_working_hours *
            3600
        )
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         1 * defaults.weekly_working_hours * 3600 +
                         2.5 * 4 * defaults.weekly_working_hours * 3600 +
                         3.1 * defaults.yearly_working_days *
                         defaults.daily_working_hours * 3600)
        self.assertEqual(parent_task2.schedule_seconds,
                         10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
                         1 * defaults.weekly_working_hours * 3600 +
                         2.5 * 4 * defaults.weekly_working_hours * 3600 +
                         3.1 * defaults.yearly_working_days *
                         defaults.daily_working_hours * 3600 + 10 * 3600)

    def test_remaining_seconds_attribute_is_a_read_only_attribute(self):
        """testing if the remaining hours is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_task,
                          'remaining_seconds', 2342)

    def test_remaining_seconds_is_working_properly(self):
        """testing if the remaining hours is working properly
        """
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt(2013, 4, 19, 10, 0)

        self.kwargs['schedule_model'] = 'effort'

        # -------------- HOURS --------------
        self.kwargs['schedule_timing'] = 10
        self.kwargs['schedule_unit'] = 'h'
        new_task = Task(**self.kwargs)

        # create a time_log of 2 hours
        book1 = TimeLog(
            task=new_task,
            start=now,
            duration=td(hours=2),
            resource=new_task.resources[0]
        )
        new_task.time_logs.append(book1)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # -------------- DAYS --------------
        self.kwargs['schedule_timing'] = 23
        self.kwargs['schedule_unit'] = 'd'
        new_task = Task(**self.kwargs)

        # create a time_log of 5 days
        book1 = TimeLog(
            task=new_task,
            start=now + td(hours=2),
            end=now + td(days=5),
            resource=new_task.resources[0]
        )

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # add another 2 hours
        book2 = TimeLog(
            task=new_task,
            start=now + td(days=5),
            duration=td(hours=2),
            resource=new_task.resources[0]
        )
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # ------------------- WEEKS ------------------
        self.kwargs['schedule_timing'] = 2
        self.kwargs['schedule_unit'] = 'w'
        new_task = Task(**self.kwargs)

        # create a time_log of 2 hours
        book1 = TimeLog(
            task=new_task,
            start=now + td(days=6),
            duration=td(hours=2),
            resource=new_task.resources[0]
        )
        new_task.time_logs.append(book1)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # create a time_log of 1 week
        book2 = TimeLog(
            task=new_task,
            start=now + td(days=7),
            duration=td(weeks=1),
            resource=new_task.resources[0]
        )
        new_task.time_logs.append(book2)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # ------------------ MONTH -------------------
        self.kwargs['schedule_timing'] = 2.5
        self.kwargs['schedule_unit'] = 'm'
        new_task = Task(**self.kwargs)

        # create a time_log of 1 months or 30 days, remaining_seconds can be
        # negative
        book1 = TimeLog(
            task=new_task,
            start=now + td(days=15),
            duration=td(days=30),
            resource=new_task.resources[0]
        )

        new_task.time_logs.append(book1)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # ------------------ YEARS ---------------------
        self.kwargs['schedule_timing'] = 3.1
        self.kwargs['schedule_unit'] = 'y'
        new_task = Task(**self.kwargs)

        # create a time_log of 1 months or 30 days, remaining_seconds can be
        # negative
        book1 = TimeLog(
            task=new_task,
            start=now + td(days=55),
            duration=td(days=30),
            resource=new_task.resources[0]
        )

        new_task.time_logs.append(book1)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

    def test_versions_attribute_is_None(self):
        """testing if a TypeError will be raised when the versions attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_task, "versions",
                          None)

        #def test_versions_argument_is_not_a_list(self):
        #"""testing if a TypeError will be raised when the versions argument is
        #not a list
        #"""
        #self.fail("test is not implemented yet")

    def test_versions_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the versions attribute is
        set to a value other than a list
        """
        self.assertRaises(TypeError, setattr, self.test_task, "versions", 1)

        #def test_versions_argument_is_not_a_list_of_Version_instances(self):
        #"""testing if a TypeError will be raised when the versions argument is
        #a list of other objects than Version instances
        #"""
        #self.fail("test is not implemented yet")

    def test_versions_attribute_is_not_a_list_of_Version_instances(self):
        """testing if a TypeError will be raised when the versions attribute is
        set to a list of other objects than Version instances
        """

        self.assertRaises(TypeError, setattr, self.test_task, "versions",
                          [1, 1.2, "a version"])

    def test_equality(self):
        """testing the equality operator
        """
        entity1 = Entity(**self.kwargs)
        task0 = Task(**self.kwargs)
        task1 = Task(**self.kwargs)
        task2 = Task(**self.kwargs)
        task3 = Task(**self.kwargs)
        task4 = Task(**self.kwargs)
        task5 = Task(**self.kwargs)
        task6 = Task(**self.kwargs)

        task1.depends = [task2]
        task2.parent = task3
        task3.parent = task4
        task5.children = [task6]
        task6.depends = [task2]

        self.assertFalse(self.test_task == entity1)
        self.assertTrue(self.test_task == task0)
        self.assertFalse(self.test_task == task1)
        self.assertFalse(self.test_task == task5)

        self.assertFalse(task1 == task2)
        self.assertFalse(task1 == task3)
        self.assertFalse(task1 == task4)

        self.assertFalse(task2 == task3)
        self.assertFalse(task2 == task4)

        self.assertFalse(task3 == task4)

        self.assertFalse(task5 == task6)

        # check task with same names but different projects

    def test_inequality(self):
        """testing the inequality operator
        """
        entity1 = Entity(**self.kwargs)
        task1 = Task(**self.kwargs)

        entity1 = Entity(**self.kwargs)
        task0 = Task(**self.kwargs)
        task1 = Task(**self.kwargs)
        task2 = Task(**self.kwargs)
        task3 = Task(**self.kwargs)
        task4 = Task(**self.kwargs)
        task5 = Task(**self.kwargs)
        task6 = Task(**self.kwargs)

        task1.depends = [task2]
        task2.parent = task3
        task3.parent = task4
        task5.children = [task6]

        self.assertTrue(self.test_task != entity1)
        self.assertFalse(self.test_task != task0)
        self.assertTrue(self.test_task != task1)
        self.assertTrue(self.test_task != task5)

        self.assertTrue(task1 != task2)
        self.assertTrue(task1 != task3)
        self.assertTrue(task1 != task4)

        self.assertTrue(task2 != task3)
        self.assertTrue(task2 != task4)

        self.assertTrue(task3 != task4)

        self.assertTrue(task5 != task6)

    def test_parent_argument_is_skipped_there_is_a_project_arg(self):
        """testing if the Task is still be able to be created without a parent
        if a Project is supplied with the project argument
        """
        try:
            self.kwargs.pop('parent')
        except KeyError:
            pass
        self.kwargs['project'] = self.test_project1
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.project, self.test_project1)

    # parent arg there but project skipped already tested
    # both skipped already tested

    def test_parent_argument_is_None_but_there_is_a_project_arg(self):
        """testing if the task is still be able to be created without a parent
        if a Project is supplied with the project argument
        """
        self.kwargs['parent'] = None
        self.kwargs['project'] = self.test_project1
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.project, self.test_project1)

    def test_parent_attribute_is_set_to_None(self):
        """testing if the parent of a task can be set to None
        """
        self.kwargs['parent'] = self.test_task
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.parent, self.test_task)
        new_task.parent = None
        self.assertIsNone(new_task.parent)

    def test_parent_argument_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the parent argument is
        not a Task instance
        """
        self.kwargs['parent'] = 'not a task'
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_parent_attribute_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the parent attribute is
        not a Task instance
        """
        self.assertRaises(TypeError, self.test_task.parent, 'not a task')

        # there is no way to generate a CycleError by using the parent argument

        # cause the Task is just created, it is not in relationship with other

    # Tasks, there is no parent nor child.

    def test_parent_attribute_creates_a_cycle(self):
        """testing if a CycleError will be raised if a child class is tried to
        be set as a parent.
        """
        self.kwargs['name'] = 'New Task'
        self.kwargs['parent'] = self.test_task
        new_task = Task(**self.kwargs)

        self.assertRaises(CircularDependencyError, setattr, self.test_task,
                          'parent', new_task)

        # more deeper test
        self.kwargs['parent'] = new_task
        new_task2 = Task(**self.kwargs)

        self.assertRaises(CircularDependencyError, setattr, self.test_task,
                          'parent', new_task2)

    def test_parent_argument_is_working_properly(self):
        """testing if the parent argument is working properly
        """
        self.kwargs['parent'] = self.test_task
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.parent, self.test_task)

    def test_parent_attribute_is_working_properly(self):
        """testing if the parent attribute is working properly
        """
        self.kwargs['parent'] = self.test_task
        self.kwargs['name'] = 'New Task'
        new_task = Task(**self.kwargs)

        self.kwargs['name'] = 'New Task 2'
        new_task2 = Task(**self.kwargs)

        self.assertNotEqual(new_task.parent, new_task2)

        new_task.parent = new_task2
        self.assertEqual(new_task.parent, new_task2)

    def test_parent_argument_will_not_allow_a_dependent_task_to_be_parent(self):
        """testing if a CircularDependencyError will be raised when one of the
        dependencies assigned also as the parent
        """
        self.kwargs['depends'] = None
        task_a = Task(**self.kwargs)
        task_b = Task(**self.kwargs)
        task_c = Task(**self.kwargs)
        self.kwargs['depends'] = [task_a, task_b, task_c]
        self.kwargs['parent'] = task_a
        self.assertRaises(CircularDependencyError, Task, **self.kwargs)

    def test_parent_attribute_will_not_allow_a_dependent_task_to_be_parent(self):
        """testing if a CircularDependencyError will be raised when one of the
        dependent tasks are assigned as the parent
        """
        self.kwargs['depends'] = None
        task_a = Task(**self.kwargs)
        task_b = Task(**self.kwargs)
        task_c = Task(**self.kwargs)
        task_d = Task(**self.kwargs)

        task_d.depends = [task_a, task_b, task_c]

        self.assertRaises(CircularDependencyError, setattr, task_d, 'parent',
                          task_a)

    def test_children_attribute_is_empty_list_by_default(self):
        """testing if the children attribute is an empty list by default
        """
        self.assertEqual(self.test_task.children, [])

    def test_children_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the children attribute is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_task, 'children', None)

    def test_children_attribute_accepts_Tasks_only(self):
        """testing if a TypeError will be raised when the item assigned to the
        children attribute is not a Task instance
        """
        self.assertRaises(TypeError, setattr, self.test_task, 'children',
                          'no task')

    def test_children_attribute_is_working_properly(self):
        """testing if the children attribute is working properly
        """
        self.kwargs['parent'] = self.test_task
        self.kwargs['name'] = 'Task 1'
        task1 = Task(**self.kwargs)

        self.kwargs['name'] = 'Task 2'
        task2 = Task(**self.kwargs)

        self.kwargs['name'] = 'Task 3'
        task3 = Task(**self.kwargs)

        self.assertNotIn(task2, task1.children)
        self.assertNotIn(task3, task1.children)

        task1.children.append(task2)
        self.assertIn(task2, task1.children)

        task3.parent = task1
        self.assertIn(task3, task1.children)

    def test_is_leaf_attribute_is_read_only(self):
        """testing if the is_leaf attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_task, 'is_leaf',
                          True)

    def test_is_leaf_attribute_is_working_properly(self):
        """testing if the is_leaf attribute is True for a Task without a child
        Task and False for Task with at least one child Task
        """
        self.kwargs['parent'] = self.test_task
        self.kwargs['name'] = 'Task 1'
        task1 = Task(**self.kwargs)

        self.kwargs['name'] = 'Task 2'
        task2 = Task(**self.kwargs)

        self.kwargs['name'] = 'Task 3'
        task3 = Task(**self.kwargs)

        task2.parent = task1
        task3.parent = task1

        # we need to commit the Session
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        self.assertTrue(task2.is_leaf)
        self.assertTrue(task3.is_leaf)
        self.assertFalse(task1.is_leaf)

    def test_is_root_attribute_is_read_only(self):
        """testing if the is_root attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_task, 'is_root',
                          True)

    def test_is_root_attribute_is_working_properly(self):
        """testing if the is_root attribute is True for a Task without a parent
        Task and False for Task with a parent Task
        """
        self.kwargs['parent'] = self.test_task
        self.kwargs['name'] = 'Task 1'
        task1 = Task(**self.kwargs)

        self.kwargs['name'] = 'Task 2'
        task2 = Task(**self.kwargs)

        self.kwargs['name'] = 'Task 3'
        task3 = Task(**self.kwargs)

        task2.parent = task1
        task3.parent = task1

        # we need to commit the Session
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        self.assertFalse(task2.is_root)
        self.assertFalse(task3.is_root)
        self.assertFalse(task1.is_root)
        self.assertTrue(self.test_task)

    def test_is_container_attribute_is_read_only(self):
        """testing if the is_container attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_task,
                          'is_container', False)

    def test_is_container_attribute_working_properly(self):
        """testing if the is_container attribute is True for a Task with at
        least one child Task and False for a Task with no child Task
        """
        self.kwargs['parent'] = self.test_task
        self.kwargs['name'] = 'Task 1'
        task1 = Task(**self.kwargs)

        self.kwargs['name'] = 'Task 2'
        task2 = Task(**self.kwargs)

        self.kwargs['name'] = 'Task 3'
        task3 = Task(**self.kwargs)

        # we need to commit the Session
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        task2.parent = task1
        task3.parent = task1

        DBSession.commit()

        self.assertFalse(task2.is_container)
        self.assertFalse(task3.is_container)
        self.assertTrue(task1.is_container)

    def test_project_and_parent_args_are_skipped(self):
        """testing if a TypeError will be raised when there is no project nor a
        parent task is given with the project and parent arguments respectively
        """
        try:
            self.kwargs.pop('project')
        except KeyError:
            pass

        try:
            self.kwargs.pop('parent')
        except KeyError:
            pass

        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_project_arg_is_skipped_but_there_is_a_parent_arg(self):
        """testing if there is no problem creating a Task without a Project
        instance when there is a Task given in parent argument
        """
        try:
            self.kwargs.pop('project')
        except KeyError:
            pass

        self.kwargs['parent'] = self.test_task
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.project, self.test_project1)

    def test_project_argument_is_not_a_Project_instance(self):
        """testing if a TypeError will be raised if the given value for the
        project argument is not a stalker.models.project.Project instance
        """
        self.kwargs['name'] = 'New Task 1'
        self.kwargs['project'] = 'Not a Project instance'
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_project_attribute_is_a_read_only_attribute(self):
        """testing if the project attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_task, 'project',
                          self.test_project1)

    def test_project_argument_is_not_matching_the_given_parent_argument(self):
        """testing if a RuntimeWarning will be raised when the given project
        and parent is not matching, that is, the project of the given parent is
        different than the supplied Project with the project argument
        """
        self.kwargs['name'] = 'New Task'
        self.kwargs['parent'] = self.test_task
        self.kwargs['project'] = Project(
            name='Some Other Project',
            code='SOP',
            status_list=self.test_project_status_list,
            repository=self.test_repository
        )
        # catching warnings are different then catching exceptions
        #self.assertRaises(RuntimeWarning, Task, **self.kwargs)
        import warnings

        with warnings.catch_warnings(record=True) as w:
            Task(**self.kwargs)
            self.assertTrue(
                issubclass(w[-1].category, RuntimeWarning)
            )

    def test_project_argument_is_not_matching_the_given_parent_argument_new_task_will_use_parents_project(self):
        """testing if the new task will use the parents project when the given
        project is not matching the given parent
        """
        self.kwargs['name'] = 'New Task'
        self.kwargs['parent'] = self.test_task
        self.kwargs['project'] = Project(
            name='Some Other Project',
            code='SOP',
            status_list=self.test_project_status_list,
            repository=self.test_repository
        )
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.project, self.test_task.project)

    def test_start_and_end_attribute_values_of_a_container_task_are_defined_by_its_child_tasks(self):
        """testing if the start and end attribute values is defined by the
        earliest start and the latest end date values of the children Tasks for
        a container Task
        """

        # remove effort and duration. Why?
        self.kwargs.pop('schedule_timing')
        self.kwargs.pop('schedule_unit')
        self.kwargs['schedule_constraint'] = CONSTRAIN_BOTH

        now = datetime.datetime(2013, 3, 22, 15, 0)
        dt = datetime.timedelta

        # task1
        self.kwargs['name'] = 'Task1'
        self.kwargs['start'] = now
        self.kwargs['end'] = now + dt(3)
        task1 = Task(**self.kwargs)

        logger.debug('now                   : %s' % now)
        logger.debug('now + dt(3)           : %s' % (now + dt(3)))
        logger.debug('now + dt(3) - now     : %s' % (now + dt(3) - now))
        logger.debug('task1.start           : %s' % task1.start)
        logger.debug('task1.end             : %s' % task1.end)
        logger.debug('task1.schedule_timing : %s' % task1.schedule_timing)
        logger.debug('task1.schedule_unit   : %s' % task1.schedule_unit)
        logger.debug('task1.is_leaf         : %s' % task1.is_leaf)

        # task2
        self.kwargs['name'] = 'Task2'
        self.kwargs['start'] = now + dt(1)
        self.kwargs['end'] = now + dt(5)
        task2 = Task(**self.kwargs)

        # task3
        self.kwargs['name'] = 'Task3'
        self.kwargs['start'] = now + dt(3)
        self.kwargs['end'] = now + dt(8)
        task3 = Task(**self.kwargs)

        # check start conditions
        logger.debug('task1.start: %s' % task1.start)
        logger.debug('task1.end  : %s' % task1.end)
        self.assertEqual(task1.start, now)
        self.assertEqual(task1.end, now + dt(3))

        # now parent the task2 and task3 to task1
        task2.parent = task1
        task1.children.append(task3)

        # check if the start is not `now` anymore
        self.assertNotEqual(task1.start, now)
        self.assertNotEqual(task1.end, now + dt(3))

        # but
        self.assertEqual(task1.start, now + dt(1))
        self.assertEqual(task1.end, now + dt(8))

        self.kwargs['name'] = 'Task4'
        self.kwargs['start'] = now + dt(15)
        self.kwargs['end'] = now + dt(16)
        task4 = Task(**self.kwargs)
        task3.parent = task4
        self.assertEqual(task4.start, task3.start)
        self.assertEqual(task4.end, task3.end)
        self.assertEqual(task1.start, task2.start)
        self.assertEqual(task1.end, task2.end)
        # TODO: with SQLAlchemy 0.9 please also check if removing the last child from a parent will update the parents start and end date values

    def test_end_value_is_calculated_with_the_schedule_timing_and_schedule_unit(self):
        """testing for a newly created task the end attribute value will be
        calculated using the schedule_timing and schedule_unit
        """
        self.kwargs['start'] = datetime.datetime(2013, 4, 17, 0, 0)
        self.kwargs.pop('end')
        self.kwargs['schedule_timing'] = 10
        self.kwargs['schedule_unit'] = 'h'

        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.end,
            datetime.datetime(2013, 4, 17, 10, 0)
        )

        self.kwargs['schedule_timing'] = 5
        self.kwargs['schedule_unit'] = 'd'
        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.end,
            datetime.datetime(2013, 4, 22, 0, 0)
        )

    def test_start_value_is_calculated_with_the_schedule_timing_and_schedule_unit_if_schedule_constraint_is_set_to_end(self):
        """testing if the start date value will be recalculated from the
        schedule_timing and schedule_unit if the schedule_constraint is set to
        end
        """
        self.kwargs['start'] = datetime.datetime(2013, 4, 17, 0, 0)
        self.kwargs['end'] = datetime.datetime(2013, 4, 18, 0, 0)
        self.kwargs['schedule_constraint'] = CONSTRAIN_END
        self.kwargs['schedule_timing'] = 10
        self.kwargs['schedule_unit'] = 'd'

        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.end,
            datetime.datetime(2013, 4, 18, 0, 0)
        )
        self.assertEqual(
            new_task.start,
            datetime.datetime(2013, 4, 8, 0, 0)
        )

    def test_start_and_end_values_are_not_touched_if_the_schedule_constraint_is_set_to_both(self):
        """testing if the start and end date values are not touched if the
        schedule constraint is set to both
        """
        self.kwargs['start'] = datetime.datetime(2013, 4, 17, 0, 0)
        self.kwargs['end'] = datetime.datetime(2013, 4, 27, 0, 0)
        self.kwargs['schedule_constraint'] = CONSTRAIN_BOTH
        self.kwargs['schedule_timing'] = 100
        self.kwargs['schedule_unit'] = 'd'

        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.start,
            datetime.datetime(2013, 4, 17, 0, 0)
        )
        self.assertEqual(
            new_task.end,
            datetime.datetime(2013, 4, 27, 0, 0)
        )

    def test_level_attribute_is_a_read_only_property(self):
        """testing if the level attribute is a read only property
        """
        self.assertRaises(AttributeError, setattr, self.test_task, 'level', 0)

    def test_level_attribute_returns_the_hierarchical_level_of_this_task(self):
        """testing if the level attribute returns the hierarchical level of
        this task
        """
        self.kwargs['name'] = 'T1'
        test_task1 = Task(**self.kwargs)
        self.assertEqual(test_task1.level, 1)

        self.kwargs['name'] = 'T2'
        test_task2 = Task(**self.kwargs)
        test_task2.parent = test_task1
        self.assertEqual(test_task2.level, 2)

        self.kwargs['name'] = 'T3'
        test_task3 = Task(**self.kwargs)
        test_task3.parent = test_task2
        self.assertEqual(test_task3.level, 3)

    def test__check_circular_dependency_causes_recursion(self):
        """Bug ID: None

        Try to create one parent and three child tasks, second and third child
        are dependent to the first child. This was causing a recursion.
        """

        task1 = Task(
            project=self.test_project1,
            name='Cekimler',
            start=datetime.datetime(2013, 4, 1),
            end=datetime.datetime(2013, 5, 6),
            status_list=self.test_task_status_list
        )

        task2 = Task(
            parent=task1,
            name='Supervising Shootings Part1',
            start=datetime.datetime(2013, 4, 1),
            end=datetime.datetime(2013, 4, 11),
            status_list=self.test_task_status_list
        )

        task3 = Task(
            parent=task1,
            name='Supervising Shootings Part2',
            depends=[task2],
            start=datetime.datetime(2013, 4, 12),
            end=datetime.datetime(2013, 4, 16),
            status_list=self.test_task_status_list
        )

        task4 = Task(
            parent=task1,
            name='Supervising Shootings Part3',
            depends=[task3],
            start=datetime.datetime(2013, 4, 12),
            end=datetime.datetime(2013, 4, 17),
            status_list=self.test_task_status_list
        )

        DBSession.add_all([task1, task2, task3, task4])
        DBSession.commit()

        # move task4 dependency to task2
        task4.depends = [task2]
        DBSession.commit()

    def test_parent_attribute_checks_cycle_on_self(self):
        """Bug ID: None

        Check if a CircularDependency Error will be raised if the parent
        attribute is pointing itself
        """
        task1 = Task(
            project=self.test_project1,
            name='Cekimler',
            start=datetime.datetime(2013, 4, 1),
            end=datetime.datetime(2013, 5, 6),
            status_list=self.test_task_status_list
        )
        self.assertRaises(CircularDependencyError, setattr, task1, 'parent',
                          task1)

    def test_bid_timing_argument_is_skipped(self):
        """testing if the bid_timing attribute value will be equal to
        schedule_timing attribute value if the bid_timing argument is skipped
        """
        self.kwargs['schedule_timing'] = 155
        self.kwargs.pop('bid_timing')
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_timing,
                         self.kwargs['schedule_timing'])
        self.assertEqual(new_task.bid_timing,
                         new_task.schedule_timing)

    def test_bid_timing_argument_is_None(self):
        """testing if the bid_timing attribute value will be equal to
        schedule_timing attribute value if the bid_timing argument is None
        """
        self.kwargs['bid_timing'] = None
        self.kwargs['schedule_timing'] = 1342
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_timing,
                         self.kwargs['schedule_timing'])
        self.assertEqual(new_task.bid_timing, new_task.schedule_timing)

    def test_bid_timing_attribute_is_set_to_None(self):
        """testing if the bid_timing attribute can be set to None
        """
        self.test_task.bid_timing = None
        self.assertIsNone(self.test_task.bid_timing)

    def test_bid_timing_argument_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised when the bid_timing argument
        is not an integer or float
        """
        self.kwargs['bid_timing'] = '10d'
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_bid_timing_attribute_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised when the bid_timing attribute
        is set to a value which is not an integer or float
        """
        self.assertRaises(TypeError, setattr, self.test_task, 'bid_timing',
                          '10d')

    def test_bid_timing_argument_is_working_properly(self):
        """testing if the bid_timing argument is working properly
        """
        self.kwargs['bid_timing'] = 23
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.bid_timing, self.kwargs['bid_timing'])

    def test_bid_timing_attribute_is_working_properly(self):
        """testing if the bid_timning attribute is working properly
        """
        test_value = 23
        self.test_task.bid_timing = test_value
        self.assertEqual(self.test_task.bid_timing, test_value)

    def test_bid_unit_argument_is_skipped(self):
        """testing if the bid_unit attribute value will be equal to
        schedule_unit attribute value if the bid_unit argument is skipped
        """
        self.kwargs['schedule_unit'] = 'd'
        self.kwargs.pop('bid_unit')
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_unit,
                         self.kwargs['schedule_unit'])
        self.assertEqual(new_task.bid_unit, new_task.schedule_unit)

    def test_bid_unit_argument_is_None(self):
        """testing if the bid_unit attribute value will be equal to
        schedule_unit attribute value if the bid_unit argument is None
        """
        self.kwargs['bid_unit'] = None
        self.kwargs['schedule_unit'] = 'min'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_unit, self.kwargs['schedule_unit'])
        self.assertEqual(new_task.bid_unit, new_task.schedule_unit)

    def test_bid_unit_attribute_is_set_to_None(self):
        """testing if the bid_unit attribute can be set to default value of 'h'
        """
        self.test_task.bid_unit = None
        self.assertEqual(self.test_task.bid_unit, 'h')

    def test_bid_unit_argument_is_not_a_string_or_unicode(self):
        """testing if a TypeError will be raised when the bid_hour argument is
        not a strign or unicode
        """
        self.kwargs['bid_unit'] = 10
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_bid_unit_attribute_is_not_a_string_or_unicode(self):
        """testing if a TypeError will be raised when the bid_unit attribute is
        set to a value which is not an integer
        """
        self.assertRaises(TypeError, setattr, self.test_task, 'bid_unit', 10)

    def test_bid_unit_argument_is_working_properly(self):
        """testing if the bid_unit argument is working properly
        """
        self.kwargs['bid_unit'] = 'h'
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.bid_unit, self.kwargs['bid_unit'])

    def test_bid_unit_attribute_is_working_properly(self):
        """testing if the bid_unit attribute is working properly
        """
        test_value = 'h'
        self.test_task.bid_unit = test_value
        self.assertEqual(self.test_task.bid_unit, test_value)

    def test_bid_unit_argument_value_not_in_defaults_datetime_units(self):
        """testing if a ValueError will be raised when the given unit value is
        not in the stalker.config.Config.datetime_units
        """
        self.kwargs['bid_unit'] = 'os'
        self.assertRaises(ValueError, Task, **self.kwargs)

    def test_bid_unit_attribute_value_not_in_defaults_datetime_units(self):
        """testing if a ValueError will be raised when the bid_unit value is
        set to a value which is not in stalker.config.Config.datetime_units.
        """
        self.assertRaises(ValueError, setattr, self.test_task, 'bid_unit',
                          'sys')

    def test_tjp_id_is_a_read_only_attribute(self):
        """testing if the tjp_id attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_task, 'tjp_id',
                          'some value')

    def test_tjp_abs_id_is_a_read_only_attribute(self):
        """testing if the tjp_abs_id attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_task,
                          'tjp_abs_id', 'some_value')

    def test_tjp_id_attribute_is_working_properly_for_a_root_task(self):
        """testing if the tjp_id is working properly for a root task
        """
        self.kwargs['parent'] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.tjp_id, 'Task_%s' % new_task.id)

    def test_tjp_id_attribute_is_working_properly_for_a_leaf_task(self):
        """testing if the tjp_id is working properly for a leaf task
        """
        self.kwargs['parent'] = self.test_task
        self.kwargs['depends'] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.tjp_id, 'Task_%s' % new_task.id)

    def test_tjp_abs_id_attribute_is_working_properly_for_a_root_task(self):
        """testing if the tjp_abs_id is working properly for a root task
        """
        self.kwargs['parent'] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.tjp_abs_id,
                         'Project_%s.Task_%s' % (self.kwargs['project'].id,
                                                 new_task.id))

    def test_tjp_abs_id_attribute_is_working_properly_for_a_leaf_task(self):
        """testing if the tjp_abs_id is working properly for a leaf task
        """
        self.kwargs['parent'] = None

        t1 = Task(**self.kwargs)
        t2 = Task(**self.kwargs)
        t3 = Task(**self.kwargs)

        t2.parent = t1
        t3.parent = t2

        t1.id = 100
        t2.id = 200
        t3.id = 300

        self.assertEqual(
            t3.tjp_abs_id,
            'Project_%s.Task_%s.Task_%s.Task_%s' % (
                self.kwargs['project'].id,
                t1.id, t2.id, t3.id
            )
        )

    def test_to_tjp_attribute_is_working_properly_for_a_root_task(self):
        """testing if the to_tjp attribute is working properly for a root task
        """
        self.kwargs['parent'] = None
        self.kwargs['schedule_timing'] = 10
        self.kwargs['schedule_unit'] = 'd'
        self.kwargs['schedule_model'] = 'effort'
        self.kwargs['depends'] = []
        self.kwargs['resources'] = [self.test_user1, self.test_user2]
        self.test_user1.id = 5648
        self.test_user2.id = 7999

        dep_t1 = Task(**self.kwargs)
        dep_t2 = Task(**self.kwargs)

        dep_t1.id = 6484
        dep_t2.id = 6485

        self.kwargs['project'].id = 14875

        self.kwargs['depends'] = [dep_t1, dep_t2]
        self.kwargs['name'] = 'Modeling'
        t1 = Task(**self.kwargs)
        t1.id = 10221

        expected_tjp = """task Task_10221 "Modeling" {
        
            depends Project_14875.Task_6484, Project_14875.Task_6485
            
            effort 10d
            allocate User_5648, User_7999
        }
        """
        self.assertEqual(t1.to_tjp, expected_tjp)

    def test_to_tjp_attribute_is_working_properly_for_a_leaf_task(self):
        """testing if the to_tjp attribute is working properly for a leaf task
        """
        self.kwargs['parent'] = self.test_task
        self.kwargs['depends'] = []

        self.test_task.id = 987879

        dep_task1 = Task(**self.kwargs)
        dep_task1.id = 23423

        dep_task2 = Task(**self.kwargs)
        dep_task2.id = 23424

        self.kwargs['name'] = 'Modeling'
        self.kwargs['schedule_timing'] = 1003
        self.kwargs['schedule_unit'] = 'h'
        self.kwargs['schedule_model'] = 'effort'
        self.kwargs['depends'] = [dep_task1, dep_task2]

        self.test_user1.name = 'Test User 1'
        self.test_user1.login = 'testuser1'
        self.test_user1.id = 1231

        self.test_user2.name = 'Test User 2'
        self.test_user2.login = 'testuser2'
        self.test_user2.id = 1232

        self.kwargs['resources'] = [self.test_user1, self.test_user2]

        self.kwargs['project'].id = 8898

        new_task = Task(**self.kwargs)
        new_task.id = 234234
        # self.maxDiff = None
        expected_tjp = """task Task_234234 "Modeling" {
        
            depends Project_8898.Task_987879.Task_23423, Project_8898.Task_987879.Task_23424
            
            effort 1003h
            allocate User_1231, User_1232
        }
        """
        self.assertEqual(new_task.to_tjp, expected_tjp)

    def test_to_tjp_attribute_is_working_properly_for_a_container_task(self):
        """testing if the to_tjp attribute is working properly for a container
        task
        """
        self.kwargs['project'].id = 87987
        self.kwargs['parent'] = None
        self.kwargs['depends'] = []

        t1 = Task(**self.kwargs)
        t1.id = 5648

        self.kwargs['parent'] = t1

        dep_task1 = Task(**self.kwargs)
        dep_task1.id = 23423
        dep_task1.depends = []

        dep_task2 = Task(**self.kwargs)
        dep_task2.id = 23424
        dep_task1.depends = []

        self.kwargs['name'] = 'Modeling'
        self.kwargs['schedule_timing'] = 1
        self.kwargs['schedule_unit'] = 'd'
        self.kwargs['schedule_model'] = 'effort'
        self.kwargs['depends'] = [dep_task1, dep_task2]

        self.test_user1.name = 'Test User 1'
        self.test_user1.login = 'testuser1'
        self.test_user1.id = 1231

        self.test_user2.name = 'Test User 2'
        self.test_user2.login = 'testuser2'
        self.test_user2.id = 1232

        self.kwargs['resources'] = [self.test_user1, self.test_user2]

        t2 = Task(**self.kwargs)
        t2.id = 5679

        expected_tjp = '''task Task_5648 "Modeling" {
        
                task Task_23423 "Modeling" {
        
            
            effort 1d
            allocate User_1231, User_1232
        }
        
                task Task_23424 "Modeling" {
        
            
            effort 1d
            allocate User_1231, User_1232
        }
        
                task Task_5679 "Modeling" {
        
            depends Project_87987.Task_5648.Task_23423, Project_87987.Task_5648.Task_23424
            
            effort 1d
            allocate User_1231, User_1232
        }
        
        }
        '''
        self.maxDiff = None
        self.assertMultiLineEqual(t1.to_tjp, expected_tjp)

    def test_to_tjp_attribute_is_working_properly_for_a_container_task_with_dependency(self):
        """testing if the to_tjp attribute is working properly for a container
        task which has dependency
        """

        self.kwargs['project'].id = 87987
        self.kwargs['parent'] = None
        self.kwargs['depends'] = []
        self.kwargs['name'] = 'Random Task Name 1'

        t0 = Task(**self.kwargs)
        t0.id = 35546

        self.kwargs['depends'] = [t0]
        self.kwargs['name'] = 'Modeling'

        t1 = Task(**self.kwargs)
        t1.id = 5648
        t1.priority = 888

        self.kwargs['parent'] = t1
        self.kwargs['depends'] = []

        dep_task1 = Task(**self.kwargs)
        dep_task1.id = 23423
        dep_task1.depends = []

        dep_task2 = Task(**self.kwargs)
        dep_task2.id = 23424
        dep_task1.depends = []

        self.kwargs['name'] = 'Modeling'
        self.kwargs['schedule_timing'] = 1
        self.kwargs['schedule_unit'] = 'd'
        self.kwargs['schedule_model'] = 'effort'
        self.kwargs['depends'] = [dep_task1, dep_task2]

        self.test_user1.name = 'Test User 1'
        self.test_user1.login = 'testuser1'
        self.test_user1.id = 1231

        self.test_user2.name = 'Test User 2'
        self.test_user2.login = 'testuser2'
        self.test_user2.id = 1232

        self.kwargs['resources'] = [self.test_user1, self.test_user2]

        t2 = Task(**self.kwargs)
        t2.id = 5679

        expected_tjp = '''task Task_5648 "Modeling" {
        priority 888
            depends Project_87987.Task_35546
                task Task_23423 "Modeling" {
        
            
            effort 1d
            allocate User_1231, User_1232
        }
        
                task Task_23424 "Modeling" {
        
            
            effort 1d
            allocate User_1231, User_1232
        }
        
                task Task_5679 "Modeling" {
        
            depends Project_87987.Task_5648.Task_23423, Project_87987.Task_5648.Task_23424
            
            effort 1d
            allocate User_1231, User_1232
        }
        
        }
        '''
        # self.maxDiff = None
        self.assertMultiLineEqual(t1.to_tjp, expected_tjp)

    def test_to_tjp_schedule_constraint_is_reflected_in_tjp_file(self):
        """testing if the schedule_constraint is reflected in the tjp file
        """
        self.kwargs['project'].id = 87987
        self.kwargs['parent'] = None
        self.kwargs['depends'] = []

        t1 = Task(**self.kwargs)
        t1.id = 5648

        self.kwargs['parent'] = t1

        dep_task1 = Task(**self.kwargs)
        dep_task1.id = 23423
        dep_task1.depends = []

        dep_task2 = Task(**self.kwargs)
        dep_task2.id = 23424
        dep_task1.depends = []

        self.kwargs['name'] = 'Modeling'
        self.kwargs['schedule_timing'] = 1
        self.kwargs['schedule_unit'] = 'd'
        self.kwargs['schedule_model'] = 'effort'
        self.kwargs['depends'] = [dep_task1, dep_task2]
        self.kwargs['schedule_constraint'] = 3
        self.kwargs['start'] = datetime.datetime(2013, 5, 3, 14, 0)
        self.kwargs['end'] = datetime.datetime(2013, 5, 4, 14, 0)

        self.test_user1.name = 'Test User 1'
        self.test_user1.login = 'testuser1'
        self.test_user1.id = 1231

        self.test_user2.name = 'Test User 2'
        self.test_user2.login = 'testuser2'
        self.test_user2.id = 1232

        self.kwargs['resources'] = [self.test_user1, self.test_user2]

        t2 = Task(**self.kwargs)
        t2.id = 5679

        expected_tjp = '''task Task_5648 "Modeling" {
        
                task Task_23423 "Modeling" {
        
            
            effort 1d
            allocate User_1231, User_1232
        }
        
                task Task_23424 "Modeling" {
        
            
            effort 1d
            allocate User_1231, User_1232
        }
        
                task Task_5679 "Modeling" {
        
            depends Project_87987.Task_5648.Task_23423, Project_87987.Task_5648.Task_23424
            start 2013-05-03-14:00
                    end 2013-05-04-14:00
            effort 1d
            allocate User_1231, User_1232
        }
        
        }
        '''
        self.maxDiff = None
        #print t1.to_tjp
        #print '-----------------------'
        #print expected_tjp
        #print '-----------------------'
        self.assertMultiLineEqual(t1.to_tjp, expected_tjp)

    def test_is_scheduled_is_a_read_only_attribute(self):
        """testing if the is_scheduled is a read-only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_task,
                          'is_scheduled', True)

    def test_is_scheduled_is_true_if_the_computed_start_and_computed_end_is_not_None(self):
        """testing if the is_scheduled attribute value is True if the
        computed_start and computed_end has both valid values
        """
        self.test_task.computed_start = datetime.datetime.now()
        self.test_task.computed_end = datetime.datetime.now() \
                                      + datetime.timedelta(10)
        self.assertTrue(self.test_task.is_scheduled)

    def test_is_scheduled_is_false_if_one_of_computed_start_and_computed_end_is_None(self):
        """testing if the is_scheduled attribute value is False if one of the
        computed_start and computed_end values is None
        """
        self.test_task.computed_start = None
        self.test_task.computed_end = datetime.datetime.now()
        self.assertFalse(self.test_task.is_scheduled)

        self.test_task.computed_start = datetime.datetime.now()
        self.test_task.computed_end = None
        self.assertFalse(self.test_task.is_scheduled)

    def test_schedule_model_attribute_is_effort_by_default(self):
        """testing if the schedule_model is effort by default
        """
        self.assertEqual(self.test_task.schedule_model, 'effort')

    def test_schedule_model_argument_is_None(self):
        """testing if the schedule model attribute will be 'effort' if the
        schedule_model argument is set to None
        """
        self.kwargs['schedule_model'] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(
            new_task.schedule_model,
            'effort'
        )

    def test_schedule_model_attribute_is_set_to_None(self):
        """testing if the schedule_model will be 'effort' if it is set to None
        """
        self.test_task.schedule_model = None
        self.assertEqual(
            self.test_task.schedule_model,
            'effort'
        )

    def test_schedule_model_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the schedule_model
        argument is not a string
        """
        self.kwargs['schedule_model'] = 234
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_schedule_model_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the schedule_model
        attribute is set to a value other than a string
        """
        self.assertRaises(
            TypeError, setattr, self.test_task, 'schedule_model', 2343
        )

    def test_schedule_model_argument_is_not_in_correct_value(self):
        """testing if a ValueError will be raised when the schedule_model
        argument is not in correct value
        """
        self.kwargs['schedule_model'] = 'not in the list'
        self.assertRaises(ValueError, Task, **self.kwargs)

    def test_schedule_model_attribute_is_not_in_correct_value(self):
        """testing if a ValueError will be raised when the schedule_model
        attribute is not set to a correct value
        """
        self.assertRaises(
            ValueError, setattr, self.test_task, 'schedule_model',
            'not in the list'
        )

    def test_schedule_model_argument_is_working_properly(self):
        """testing if the schedule_model argument value is correctly passed to
        the schedule_model attribute
        """
        test_value = 'duration'
        self.kwargs['schedule_model'] = test_value
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_model, test_value)

    def test_schedule_model_attribute_is_working_properly(self):
        """testing if the schedule_model attribute is working properly
        """
        test_value = 'duration'
        self.assertNotEqual(
            self.test_task.schedule_model, test_value
        )
        self.test_task.schedule_model = test_value
        self.assertEqual(
            self.test_task.schedule_model, test_value
        )

    def test_schedule_constraint_is_0_by_default(self):
        """testing if the schedule_constraint attribute is None by default
        """
        self.assertEqual(self.test_task.schedule_constraint, 0)

    def test_schedule_constraint_argument_is_skipped(self):
        """testing if the schedule_constraint attribute will be 0 if
        schedule_constraint is skipped
        """
        try:
            self.kwargs.pop('schedule_constraint')
        except KeyError:
            pass
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, 0)

    def test_schedule_constraint_argument_is_None(self):
        """testing if the schedule_constraint attribute will be 0 if
        schedule_constraint is None
        """
        self.kwargs['schedule_constraint'] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, 0)

    def test_schedule_constraint_attribute_is_set_to_None(self):
        """testing if the schedule_constraint attribute will be 0 if
        it is set to None
        """
        self.test_task.schedule_constraint = None
        self.assertEqual(self.test_task.schedule_constraint, 0)

    def test_schedule_constraint_argument_is_not_an_integer(self):
        """testing if a TypeError will be raised when the schedule_constraint
        argument is not an integer
        """
        self.kwargs['schedule_constraint'] = 'not an integer'
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_schedule_constraint_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the schedule_constraint
        attribute is set to a value other than an integer
        """
        self.assertRaises(TypeError, setattr, self.test_task,
                          'schedule_constraint', 'not an integer')

    def test_schedule_constraint_argument_is_working_properly(self):
        """testing if the schedule_constraint argument value is correctly
        passed to schedule_constraint attribute
        """
        test_value = 2
        self.kwargs['schedule_constraint'] = test_value
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, test_value)

    def test_schedule_constraint_attribute_is_working_properly(self):
        """testing if the schedule_constraint attribute value is correctly
        changed
        """
        test_value = 3
        self.test_task.schedule_constraint = test_value
        self.assertEqual(self.test_task.schedule_constraint, test_value)

    def test_schedule_constraint_argument_value_is_out_of_range(self):
        """testing if the value of schedule_constraint argument value will be
        clamped to the [0-3] range if it is out of range
        """
        self.kwargs['schedule_constraint'] = -1
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, 0)

        self.kwargs['schedule_constraint'] = 4
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, 3)

    def test_schedule_constraint_attribute_value_is_out_of_range(self):
        """testing if the value of schedule_constraint attribute value will be
        clamped to the [0-3] range if it is out of range
        """
        self.test_task.schedule_constraint = -1
        self.assertEqual(self.test_task.schedule_constraint, 0)

        self.test_task.schedule_constraint = 4
        self.assertEqual(self.test_task.schedule_constraint, 3)

    def test_parents_attribute_is_read_only(self):
        """testing if the parents attribute is read only
        """
        self.assertRaises(
            AttributeError,
            setattr,
            self.test_task,
            'parents',
            self.test_dependent_task1
        )

    def test_parents_attribute_is_working_properly(self):
        """testing if the parents attribute is working properly
        """
        self.kwargs['parent'] = None

        t1 = Task(**self.kwargs)
        t2 = Task(**self.kwargs)
        t3 = Task(**self.kwargs)

        t2.parent = t1
        t3.parent = t2

        self.assertEqual(
            t3.parents,
            [t1, t2]
        )

    def test_responsible_argument_is_skipped(self):
        """testing if the responsible argument can be skipped
        """
        self.kwargs.pop('responsible')
        Task(**self.kwargs)

    def test_responsible_argument_is_None(self):
        """testing if the responsible argument can be None
        """
        self.kwargs['responsible'] = None
        Task(**self.kwargs)

    def test_responsible_attribute_is_set_to_None(self):
        """testing if the responsible attribute can be set to None
        """
        self.test_task.responsible = None

    def test_responsible_argument_is_not_a_User_instance(self):
        """testing if a TypeError will be raised if the responsible argument
        value is not a User instance
        """
        self.kwargs['responsible'] = 'not a user instance'
        self.assertRaises(TypeError, Task, **self.kwargs)

    def test_responsible_attribute_is_set_to_something_other_than_User_instance(self):
        """testing if a TypeError will be raised if the responsible attribute
        is set to something other than a User instance
        """
        self.assertRaises(TypeError, setattr, self.test_task, 'responsible',
                          'not a user instance')

    def test_responsible_argument_is_None_or_skipped_responsible_attribute_comes_from_parents(self):
        """testing if the responsible argument is None or skipped then the
        responsible attribute value comes from parents
        """
        # create two new tasks
        self.kwargs['responsible'] = None
        new_task1 = Task(**self.kwargs)
        new_task1.parent = self.test_task

        new_task2 = Task(**self.kwargs)
        new_task2.parent = new_task1

        self.assertEqual(new_task1.responsible, self.test_user1)
        self.assertEqual(new_task2.responsible, self.test_user1)

    def test_responsible_attribute_is_set_to_None_responsible_attribute_comes_from_parents(self):
        """testing if the responsible attribute is None or skipped then its
        value comes from parents
        """
        # create two new tasks
        new_task1 = Task(**self.kwargs)
        new_task1.parent = self.test_task

        new_task2 = Task(**self.kwargs)
        new_task2.parent = new_task1

        new_task1.responsible = None
        new_task2.responsible = None
        self.test_task.responsible = self.test_user2

        self.assertEqual(new_task1.responsible, self.test_user2)
        self.assertEqual(new_task2.responsible, self.test_user2)

    def test_responsible_attribute_value_comes_from_project_if_no_parent_exists(self):
        """testing if the responsible attribute value comes from project.lead
        attribute if there are no parents
        """
        self.test_task.responsible = None
        self.test_project1.lead = self.test_user3

        self.assertEqual(self.test_task.responsible, self.test_user3)

    def test_responsible_attribute_value_comes_from_project_if_parents_doesnt_have_a_responsible(self):
        """testing if the responsible attribute value comes from the
        project.lead attribute if parents doesn't have a responsible
        """
        # create two new tasks
        self.kwargs['responsible'] = None
        new_task1 = Task(**self.kwargs)
        new_task1.parent = self.test_task

        new_task2 = Task(**self.kwargs)
        new_task2.parent = new_task1

        new_task1.responsible = None
        new_task2.responsible = None
        self.test_task.responsible = None
        self.test_project1.lead = self.test_user2

        self.assertEqual(new_task1.responsible, self.test_user2)
        self.assertEqual(new_task2.responsible, self.test_user2)

    def test_computed_start_also_sets_start(self):
        """testing if computed_start also sets the start value of the task
        """
        new_task1 = Task(**self.kwargs)
        test_value = datetime.datetime(2013, 8, 2, 13, 0)
        self.assertNotEqual(new_task1.start, test_value)
        new_task1.computed_start = test_value
        self.assertEqual(new_task1.computed_start, test_value)
        self.assertEqual(new_task1.start, test_value)

    def test_computed_end_also_sets_end(self):
        """testing if computed_end also sets the end value of the task
        """
        new_task1 = Task(**self.kwargs)
        test_value = datetime.datetime(2013, 8, 2, 13, 0)
        self.assertNotEqual(new_task1.end, test_value)
        new_task1.computed_end = test_value
        self.assertEqual(new_task1.computed_end, test_value)
        self.assertEqual(new_task1.end, test_value)
