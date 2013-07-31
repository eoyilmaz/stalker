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

import unittest2
import datetime
from stalker import (Project, Repository, Status, StatusList, Task, TimeLog,
                     User)
from stalker.exceptions import OverBookedError


class TimeLogTester(unittest2.TestCase):
    """tests the TimeLog class
    """

    def setUp(self):
        """setup the test
        """
        # create a resource
        self.test_resource1 = User(
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
            "task": self.test_task,
            "resource": self.test_resource1,
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
        td = datetime.timedelta
        self.kwargs.pop("task")
        self.kwargs['start'] = self.kwargs['start'] - td(days=100)
        self.kwargs['duration'] = td(hours=10)
        self.assertRaises(TypeError, TimeLog, **self.kwargs)

    def test_task_argument_is_None(self):
        """testing if a TypeError will be raised when the task argument is None
        """
        td = datetime.timedelta
        self.kwargs["task"] = None
        self.kwargs['start'] = self.kwargs['start'] - td(days=100)
        self.kwargs['duration'] = td(hours=10)
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
        td = datetime.timedelta
        self.kwargs["task"] = "this is a task"
        self.kwargs['start'] = self.kwargs['start'] - td(days=100)
        self.kwargs['duration'] = td(hours=10)
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
            resources=[self.test_resource1],
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
            resources=[self.test_resource1],
        )

        # now create a new time_log for the new task
        self.kwargs["task"] = new_task
        self.kwargs["start"] = self.kwargs["start"] + \
                               self.kwargs["duration"] + \
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
            resources=[self.test_resource1],
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
        self.test_time_log.end = self.test_time_log.start + \
                                 datetime.timedelta(10)
        self.assertEqual(self.test_time_log.duration, datetime.timedelta(10))

    def test_OverbookedError_1(self):
        """testing if a OverBookedError will be raised when the resource 
        is already booked for the given time period.

        Simple case diagram:
        #####
        #####
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0),
        self.kwargs["duration"] = datetime.timedelta(10)
        time_log1 = TimeLog(**self.kwargs)

        self.assertRaises(OverBookedError, TimeLog, **self.kwargs)

    def test_OverbookedError_2(self):
        """testing if a OverBookedError will be raised when the resource 
        is already booked for the given time period.

        Simple case diagram:
        #######
        #####
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0),
        self.kwargs["duration"] = datetime.timedelta(10)
        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["duration"] = datetime.timedelta(8)
        self.assertRaises(OverBookedError, TimeLog, **self.kwargs)

    def test_OverbookedError_3(self):
        """testing if a OverBookedError will be raised when the resource 
        is already booked for the given time period.

        Simple case diagram:
        #####
        #######
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0),
        self.kwargs["duration"] = datetime.timedelta(8)
        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["duration"] = datetime.timedelta(10)

        self.assertRaises(OverBookedError, TimeLog, **self.kwargs)

    def test_OverbookedError_4(self):
        """testing if a OverBookedError will be raised when the resource 
        is already booked for the given time period.

        Simple case diagram:
        #######
          #####
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) - \
                               datetime.timedelta(2)
        self.kwargs["duration"] = datetime.timedelta(12)

        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(10)

        self.assertRaises(OverBookedError, TimeLog, **self.kwargs)

    def test_OverbookedError_5(self):
        """testing if a OverBookedError will be raised when the resource 
        is already booked for the given time period.

        Simple case diagram:
          #####
        #######
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(10)

        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) - \
            datetime.timedelta(2)
        self.kwargs["duration"] = datetime.timedelta(12)

        self.assertRaises(OverBookedError, TimeLog, **self.kwargs)

    def test_OverbookedError_6(self):
        """testing if a OverBookedError will be raised when the resource 
        is already booked for the given time period.

        Simple case diagram:
          #######
        #######
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(15)

        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) - \
            datetime.timedelta(5)
        self.kwargs["duration"] = datetime.timedelta(15)

        self.assertRaises(OverBookedError, TimeLog, **self.kwargs)

    def test_OverbookedError_7(self):
        """testing if a OverBookedError will be raised when the resource 
        is already booked for the given time period.

        Simple case diagram:
        #######
          #######
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) - \
                               datetime.timedelta(5)
        self.kwargs["duration"] = datetime.timedelta(15)

        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(15)

        self.assertRaises(OverBookedError, TimeLog, **self.kwargs)

    def test_OverbookedError_8(self):
        """testing if no OverBookedError will be raised when the resource 
        is not already booked for the given time period.

        Simple case diagram:
        #######
                 #######
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(5)
        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) + \
                               datetime.timedelta(20)
        # no warning
        time_log2 = TimeLog(**self.kwargs)

    def test_OverbookedError_9(self):
        """testing if no OverBookedError will be raised when the resource 
        is not already booked for the given time period.

        Simple case diagram:
                 #######
        #######
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0) + \
                               datetime.timedelta(20)
        self.kwargs["duration"] = datetime.timedelta(5)
        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)

        # no warning
        time_log2 = TimeLog(**self.kwargs)

    def test_OverbookedError_10(self):
        """testing i no OverBookedError will be raised for the same TimeLog
        instance
        """
        # time_log1
        self.kwargs['resource'] = self.test_resource2
        self.kwargs['start'] = datetime.datetime(2013, 5, 6, 14, 0)
        self.kwargs['duration'] = datetime.timedelta(20)
        time_log1 = TimeLog(**self.kwargs)

        # no warning
        self.test_resource2.time_logs.append(time_log1)

    # def test_time_log_extends_effort_of_task(self):
    #     """testing if the TimeLog will expand the Task.schedule_timing if it is
    #     getting longer than Task.total_logged_seconds
    #     """
    #     task1 = Task(
    #         name='Test Task 1',
    #         schedule_timing=10,
    #         schedule_unit='h',
    #         schedule_model='effort',
    #         resource=self.test_resource1,
    #         status_list=self.test_task_status_list,
    #         project=self.test_project
    #     )
    # 
    #     # check everything is initialized as they should be
    #     self.assertEqual(task1.total_logged_seconds, 0)
    #     self.assertEqual(task1.remaining_seconds, 36000)
    # 
    #     dt = datetime.datetime
    #     td = datetime.timedelta
    # 
    #     # now create time log for the task
    #     timeLog1 = TimeLog(
    #         task=task1,
    #         resource=self.test_resource1,
    #         start=dt(2013, 5, 2, 15, 0),
    #         duration=td(hours=5)
    #     )
    # 
    #     # now check if the remaining seconds is correctly calculated
    #     self.assertEqual(
    #         task1.remaining_seconds, 18000
    #     )
    # 
    #     # and the schedule_timing is not expanded
    #     self.assertEqual(
    #         task1.schedule_timing,
    #         10
    #     )
    # 
    #     # now add a new timeLog which expands the Task
    #     timeLog2 = TimeLog(
    #         task=task1,
    #         resource=self.test_resource1,
    #         start=dt(2013, 5, 2, 20, 0),
    #         duration=td(hours=8)
    #     )
    # 
    #     # check if the task schedule_timing is correctly expanded to 13 hours
    #     self.assertEqual(
    #         task1.schedule_timing,
    #         13
    #     )

    # def test_time_log_extends_effort_of_task_with_different_time_unit(self):
    #     """testing if the TimeLog will expand the Task.schedule_timing if it is
    #     getting longer than Task.total_logged_seconds and can work with
    #     different time units
    #     """
    #     from stalker import defaults
    #     defaults.daily_working_hours = 10
    # 
    #     task1 = Task(
    #         name='Test Task 1',
    #         schedule_timing=2,
    #         schedule_unit='d',
    #         schedule_model='effort',
    #         resource=self.test_resource1,
    #         status_list=self.test_task_status_list,
    #         project=self.test_project
    #     )
    # 
    #     # check everything is initialized as they should be
    #     self.assertEqual(task1.total_logged_seconds, 0)
    # 
    #     # there are no studio created so it should use the defaults
    #     self.assertEqual(task1.remaining_seconds,
    #                      2 * 10 * 60 * 60)
    # 
    #     dt = datetime.datetime
    #     td = datetime.timedelta
    # 
    #     # now create time log for the task
    #     timeLog1 = TimeLog(
    #         task=task1,
    #         resource=self.test_resource1,
    #         start=dt(2013, 5, 2, 10, 0),
    #         duration=td(hours=10)
    #     )
    # 
    #     # now check if the remaining seconds is correctly calculated
    #     self.assertEqual(
    #         task1.remaining_seconds, 10 * 60 * 60
    #     )
    # 
    #     # and the schedule_timing is not expanded
    #     self.assertEqual(
    #         task1.schedule_timing,
    #         2
    #     )
    # 
    #     # now add a new timeLog which expands the Task
    #     timeLog2 = TimeLog(
    #         task=task1,
    #         resource=self.test_resource1,
    #         start=dt(2013, 5, 2, 20, 0),
    #         duration=td(hours=15)
    #     )
    # 
    #     # check if the task schedule_timing is correctly expanded to 2.5 days
    #     self.assertEqual(
    #         task1.schedule_timing,
    #         2.5
    #     )


class TimeLogDBTestCase(unittest2.TestCase):
    """Tests database interaction of TimeLog instances
    """

    def setUp(self):
        """set up the test
        """
        # create an in memory database
        from stalker import db
        db.setup()
        db.init()

        # create a resource
        self.test_resource1 = User(
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
            status_list=self.test_task_status_list,
            schedule_timing=10,
            schedule_unit='d',
            resources=[self.test_resource1]
        )

        self.kwargs = {
            "name": "test time_log",
            "task": self.test_task,
            "resource": self.test_resource1,
            "start": datetime.datetime(2013, 3, 22, 1, 0),
            "duration": datetime.timedelta(10)
        }

    def test_timeLog_prevents_auto_flush_when_expanding_task_schedule_timing(self):
        """testing timeLog prevents auto flush when expanding task
        schedule_timing attribute
        """
        from stalker.db import DBSession
        tlog1 = TimeLog(**self.kwargs)
        DBSession.add(tlog1)
        DBSession.commit()

        # create a new time log
        self.kwargs['start'] = self.kwargs['start'] + self.kwargs['duration']
        tlog2 = TimeLog(**self.kwargs)

    def test_timeLog_creation_for_a_child_task(self):
        """testing TimeLog creation for a child task which has a couple of
        parent tasks
        """
        dt = datetime.datetime
        td = datetime.timedelta

        parent_task1 = Task(
            name="Parent Task 1",
            project=self.test_project,
            status_list=self.test_task_status_list,
        )

        parent_task2 = Task(
            name="Parent Task 2",
            project=self.test_project,
            status_list=self.test_task_status_list,
        )

        child_task1 = Task(
            name="Child Task 1",
            project=self.test_project,
            status_list=self.test_task_status_list,
            resources=[self.test_resource1]
        )

        child_task2 = Task(
            name="Child Task 1",
            project=self.test_project,
            status_list=self.test_task_status_list,
            resources=[self.test_resource2]
        )

        # Task hierarchy
        # +-> p1
        # |   |
        # |   +-> p2
        # |   |    |
        # |   |    +-> c1
        # |   |
        # |   +-> c2
        # |
        # +-> self.test_task1
        parent_task2.parent = parent_task1
        child_task2.parent = parent_task1
        child_task1.parent = parent_task2

        from stalker.db import DBSession

        self.assertEqual(parent_task1.total_logged_seconds, 0)
        self.assertEqual(parent_task2.total_logged_seconds, 0)
        self.assertEqual(child_task1.total_logged_seconds, 0)
        self.assertEqual(child_task2.total_logged_seconds, 0)

        # now create a time log for child_task2
        tlog1 = TimeLog(
            task=child_task2,
            resource=child_task2.resources[0],
            start=dt(2013, 7, 31, 10, 0),
            end=dt(2013, 7, 31, 19, 0)
        )

        # before commit
        self.assertEqual(parent_task1.total_logged_seconds, 9 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 0)
        self.assertEqual(child_task1.total_logged_seconds, 0)
        self.assertEqual(child_task2.total_logged_seconds, 9 * 3600)

        # commit changes
        DBSession.add(tlog1)
        DBSession.commit()

        # after commit it should not change
        self.assertEqual(parent_task1.total_logged_seconds, 9 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 0)
        self.assertEqual(child_task1.total_logged_seconds, 0)
        self.assertEqual(child_task2.total_logged_seconds, 9 * 3600)

        # add a new tlog to child_task2 and commit it
        # now create a time log for child_task2
        tlog2 = TimeLog(
            task=child_task2,
            resource=child_task2.resources[0],
            start=dt(2013, 7, 31, 19, 0),
            end=dt(2013, 7, 31, 22, 0)
        )

        self.assertEqual(parent_task1.total_logged_seconds, 12 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 0)
        self.assertEqual(child_task1.total_logged_seconds, 0)
        self.assertEqual(child_task2.total_logged_seconds, 12 * 3600)

        # commit changes
        DBSession.add(tlog2)
        DBSession.commit()

        self.assertEqual(parent_task1.total_logged_seconds, 12 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 0)
        self.assertEqual(child_task1.total_logged_seconds, 0)
        self.assertEqual(child_task2.total_logged_seconds, 12 * 3600)

        # add a new time log to child_task1 and commit it
        tlog3 = TimeLog(
            task=child_task1,
            resource=child_task1.resources[0],
            start=dt(2013, 7, 31, 10, 0),
            end=dt(2013, 7, 31, 19, 0)
        )

        self.assertEqual(parent_task1.total_logged_seconds, 21 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 9 * 3600)
        self.assertEqual(child_task1.total_logged_seconds, 9 * 3600)
        self.assertEqual(child_task2.total_logged_seconds, 12 * 3600)

        # commit changes
        DBSession.add(tlog3)
        DBSession.commit()

        self.assertEqual(parent_task1.total_logged_seconds, 21 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 9 * 3600)
        self.assertEqual(child_task1.total_logged_seconds, 9 * 3600)
        self.assertEqual(child_task2.total_logged_seconds, 12 * 3600)
