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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import unittest
import datetime
from stalker import (Project, Repository, Status, StatusList, Task, TimeLog,
                     User)
from stalker.exceptions import OverBookedWarning


class TimeLogTester(unittest.TestCase):
    """tests the TimeLog class
    """

    def setUp(self):
        """setup the test
        """
        # create a resource
        self.test_resource = User(
            name="User1",
            login="user1",
            email="user1@users.com",
            password="1234",
        )

        self.test_resource2 = User(
            name="User2",
            login="user2",
            email="user2@users.com",
            password="1234"
        )

        self.test_repo = Repository(name="test repository")

        # create a Project
        self.test_status1 = Status(name="Status1", code="STS1")
        self.test_status2 = Status(name="Status2", code="STS2")
        self.test_status3 = Status(name="Status3", code="STS3")

        self.test_project_status_list = StatusList(
            name="Project Statuses",
            statuses=[self.test_status1],
            target_entity_type=Project
        )

        self.test_task_status_list = StatusList(
            name="Task Statuses",
            statuses=[self.test_status1, self.test_status2, self.test_status3],
            target_entity_type=Task
        )

        self.test_project = Project(
            name="test project",
            code='tp',
            repository=self.test_repo,
            status_list=self.test_project_status_list
        )

        # create a Task
        self.test_task = Task(
            name="test task",
            project=self.test_project,
            status_list=self.test_task_status_list
        )

        self.kwargs = {
            "name": "test time_log",
            "task": self.test_task,
            "resource": self.test_resource,
            "start": datetime.datetime(2013, 3, 22, 1, 0),
            "duration": datetime.timedelta(10)
        }

        # create a TimeLog
        # and test it
        self.test_time_log = TimeLog(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for
        TimeLog class
        """
        self.assertTrue(TimeLog.__auto_name__)
    
    def test_task_argument_is_Skipped(self):
        """testing if a TypeError will be raised when the task argument is
        skipped
        """
        self.kwargs.pop("task")
        self.assertRaises(TypeError, TimeLog, **self.kwargs)

    def test_task_argument_is_None(self):
        """testing if a TypeError will be raised when the task argument is None
        """
        self.kwargs["task"] = None
        self.assertRaises(TypeError, TimeLog, **self.kwargs)

    def test_task_attribute_is_None(self):
        """testing if a TypeError will be raised when the task attribute i
        None
        """
        self.assertRaises(TypeError, setattr, self.test_time_log, "task", None)

    def test_task_argument_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the task argument is not
        a stalker.models.task.Task instance
        """
        self.kwargs["task"] = "this is a task"
        self.assertRaises(TypeError, TimeLog, **self.kwargs)

    def test_task_attribute_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the task attribute is not
        a stalker.models.task.Task instance
        """
        self.assertRaises(TypeError, setattr, self.test_time_log, "task",
                          "this is a task")

    def test_task_attribute_is_working_properly(self):
        """testing if the task attribute is working properly
        """
        new_task = Task(
            name="Test task 2",
            project=self.test_project,
            status_list=self.test_task_status_list,
            resources=[self.test_resource],
        )
        self.assertNotEqual(self.test_time_log.task, new_task)
        self.test_time_log.task = new_task
        self.assertEqual(self.test_time_log.task, new_task)

    def test_task_argument_updates_backref(self):
        """testing if the Task given with the task argument is updated correctly
        with the current TimeLog instance is listed in the time_logs attribute of
        the Task
        """
        new_task = Task(
            name="Test Task 3",
            project=self.test_project,
            status_list=self.test_task_status_list,
            resources=[self.test_resource],
        )

        # now create a new time_log for the new task
        self.kwargs["task"] = new_task
        self.kwargs["start"] = self.kwargs["start"] +\
                                    self.kwargs["duration"] +\
                                    datetime.timedelta(120)
        new_time_log = TimeLog(**self.kwargs)

        # now check if the new_time_log is in task.time_logs
        self.assertIn(new_time_log, new_task.time_logs)

    def test_task_attribute_updates_backref(self):
        """testing if the Task given with the task attribute is updated
        correctly with the current TimeLog instance is listed in the time_logs
        attribute of the Task
        """
        new_task = Task(
            name="Test Task 3",
            project=self.test_project,
            status_list=self.test_task_status_list,
            resources=[self.test_resource],
        )
        
        self.test_time_log.task = new_task
        self.assertIn(self.test_time_log, new_task.time_logs)
    
    def test_resource_argument_is_skipped(self):
        """testing if a TypeError will be raised when the resource argument is
        skipped
        """
        self.kwargs.pop("resource")
        self.assertRaises(TypeError, TimeLog, **self.kwargs)
    
    def test_resource_argument_is_None(self):
        """testing if a TypeError will be raised when the resource argument is
        None
        """
        self.kwargs["resource"] = None
        self.assertRaises(TypeError, TimeLog, **self.kwargs)

    def test_resource_attribute_is_None(self):
        """testing if a TypeError will be raised when the resource attribute is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_time_log, "resource",
                          None)

    def test_resource_argument_is_not_a_User_instance(self):
        """testing if a TypeError will be raised when the resource argument is
        not a stalker.models.user.User instance
        """
        self.kwargs["resource"] = "This is a resource"
        self.assertRaises(TypeError, TimeLog, **self.kwargs)

    def test_resource_attribute_is_not_a_User_instance(self):
        """testing if a TypeError will be raised when the resource attribute is
        set to a value other than a stalker.models.user.User instance
        """
        self.assertRaises(TypeError, setattr, self.test_time_log, "resource",
                          "this is a resource")

    def test_resource_attribute_is_working_properly(self):
        """testing if the resource attribute is working properly
        """
        new_resource = User(
            name="Test Resource",
            login="test resource 2",
            email="test@resource2.com",
            password="1234",
        )

        self.assertNotEqual(self.test_time_log.resource, new_resource)
        self.test_time_log.resource = new_resource
        self.assertEqual(self.test_time_log.resource, new_resource)

    def test_resource_argument_updates_backref(self):
        """testing if the User instance given with the resource argument is
        updated with the current TimeLog is listed in the time_logs attribute of
        the User instance
        """
        new_resource = User(
            name="Test Resource",
            login="test resource 2",
            email="test@resource2.com",
            password="1234",
        )

        self.kwargs["resource"] = new_resource
        new_time_log = TimeLog(**self.kwargs)

        self.assertEqual(new_time_log.resource, new_resource)

    def test_resource_attribute_updates_backref(self):
        """testing if the User instance given with the resource attribute is
        updated with the current TimeLog is listed in the time_logs attribute of
        the User instance
        """
        new_resource = User(
            name="Test Resource",
            login="test resource 2",
            email="test@resource2.com",
            password="1234",
        )

        self.assertNotEqual(self.test_time_log.resource, new_resource)
        self.test_time_log.resource = new_resource
        self.assertEqual(self.test_time_log.resource, new_resource)

    def test_ScheduleMixin_initialization(self):
        """testing if the ScheduleMixin part is initialized correctly
        """
        # it should have schedule attributes
        self.assertEqual(self.test_time_log.start,
                         self.kwargs["start"])
        self.assertEqual(self.test_time_log.duration, self.kwargs["duration"])

        self.test_time_log.start = datetime.datetime(2013, 3, 22, 4, 0)
        self.test_time_log.end = self.test_time_log.start +\
                                     datetime.timedelta(10)
        self.assertEqual(self.test_time_log.duration, datetime.timedelta(10))

    def test_OverbookedWarning_1(self):
        """testing if a OverTimeLogWarning will be raised when the resource 
        is already booked for the given time period.
        
        Simple case diagram:
        #####
        #####
        """
        # time_log1
        self.kwargs["name"] = "time_log1"
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0),
        self.kwargs["duration"] = datetime.timedelta(10)
        
        time_log1 = TimeLog(**self.kwargs)
        
        # time_log2
        self.kwargs["name"] = "time_log2"
        import warnings
        warnings.resetwarnings()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            new_time_log = TimeLog(**self.kwargs)
            self.assertTrue(
                issubclass(w[-1].category, OverBookedWarning)
            )

    def test_OverbookedWarning_2(self):
        """testing if a OverTimeLogWarning will be raised when the resource 
        is already booked for the given time period.
        
        Simple case diagram:
        #######
        #####
        """
        # time_log1
        self.kwargs["name"] = "time_log1"
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0),
        self.kwargs["duration"] = datetime.timedelta(10)

        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["name"] = "time_log2"
        self.kwargs["duration"] = datetime.timedelta(8)
        
        import warnings
        warnings.resetwarnings()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            new_time_log = TimeLog(**self.kwargs)
            self.assertTrue(
                issubclass(w[-1].category, OverBookedWarning)
            )
    
    def test_OverbookedWarning_3(self):
        """testing if a OverTimeLogWarning will be raised when the resource 
        is already booked for the given time period.
        
        Simple case diagram:
        #####
        #######
        """
        # time_log1
        self.kwargs["name"] = "time_log1"
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0),
        self.kwargs["duration"] = datetime.timedelta(8)

        time_log1 = TimeLog(**self.kwargs)

        # time_log2        
        self.kwargs["name"] = "time_log2"
        self.kwargs["duration"] = datetime.timedelta(10)
        
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            new_time_log = TimeLog(**self.kwargs)
            self.assertTrue(
                issubclass(w[-1].category, OverBookedWarning)
            )

    def test_OverbookedWarning_4(self):
        """testing if a OverTimeLogWarning will be raised when the resource 
        is already booked for the given time period.
        
        Simple case diagram:        
        #######
          #####
        """
        # time_log1
        self.kwargs["name"] = "time_log1"
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) -\
                                    datetime.timedelta(2)
        self.kwargs["duration"] = datetime.timedelta(12)
        
        time_log1 = TimeLog(**self.kwargs)
        
        # time_log2
        self.kwargs["name"] = "time_log2"
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(10)
        
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            new_time_log = TimeLog(**self.kwargs)
            self.assertTrue(
                issubclass(w[-1].category, OverBookedWarning)
            )

    def test_OverbookedWarning_5(self):
        """testing if a OverTimeLogWarning will be raised when the resource 
        is already booked for the given time period.
        
        Simple case diagram:
          #####
        #######
        """
        # time_log1
        self.kwargs["name"] = "time_log1"
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(10)
        
        time_log1 = TimeLog(**self.kwargs)
        
        # time_log2
        self.kwargs["name"] = "time_log2"
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) -\
                                    datetime.timedelta(2)
        self.kwargs["duration"] = datetime.timedelta(12)
        
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            new_time_log = TimeLog(**self.kwargs)
            self.assertTrue(
                issubclass(w[-1].category, OverBookedWarning)
            )

    def test_OverbookedWarning_6(self):
        """testing if a OverTimeLogWarning will be raised when the resource 
        is already booked for the given time period.
        
        Simple case diagram:
          #######
        #######
        """
        # time_log1
        self.kwargs["name"] = "time_log1"
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(15)
        
        time_log1 = TimeLog(**self.kwargs)
        
        # time_log2
        self.kwargs["name"] = "time_log2"
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) -\
                                    datetime.timedelta(5)
        self.kwargs["duration"] = datetime.timedelta(15)
        
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            new_time_log = TimeLog(**self.kwargs)
            self.assertTrue(
                issubclass(w[-1].category, OverBookedWarning)
            ) 
    
    def test_OverbookedWarning_7(self):
        """testing if a OverTimeLogWarning will be raised when the resource 
        is already booked for the given time period.
        
        Simple case diagram:
        #######
          #######
        """
        # time_log1
        self.kwargs["name"] = "time_log1"
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) -\
                                    datetime.timedelta(5)
        self.kwargs["duration"] = datetime.timedelta(15)
        
        time_log1 = TimeLog(**self.kwargs)
        
        # time_log2        
        self.kwargs["name"] = "time_log2"
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(15)
        
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            new_time_log = TimeLog(**self.kwargs)
            self.assertTrue(
                issubclass(w[-1].category, OverBookedWarning)
            )

    def test_OverbookedWarning_8(self):
        """testing if no OverTimeLogWarning will be raised when the resource 
        is not already booked for the given time period.
        
        Simple case diagram:
        #######
                 #######
        """
        # time_log1
        self.kwargs["name"] = "time_log1"
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(5)

        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["name"] = "time_log2"
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) +\
                                    datetime.timedelta(20)
        # no warning
        time_log2 = TimeLog(**self.kwargs)

    def test_OverbookedWarning_9(self):
        """testing if no OverTimeLogWarning will be raised when the resource 
        is not already booked for the given time period.
        
        Simple case diagram:
                 #######
        #######
        """
        # time_log1
        self.kwargs["name"] = "time_log1"
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) +\
                                    datetime.timedelta(20)
        self.kwargs["duration"] = datetime.timedelta(5)

        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["name"] = "time_log2"
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)

        # no warning
        time_log2 = TimeLog(**self.kwargs)
