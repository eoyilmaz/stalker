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
from stalker import (Project, Repository, Status, StatusList, Task, TimeLog,
                     User)
from stalker.exceptions import OverBookedError, StatusError, \
    DependencyViolationError


class TimeLogTester(unittest.TestCase):
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

        self.test_task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

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

    def test_task_argument_is_skipped(self):
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
        """testing if the Task given with the task argument is updated
        correctly with the current TimeLog instance is listed in the time_logs
        attribute of the Task
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
        self.assertTrue(new_time_log in new_task.time_logs)

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
        self.assertTrue(self.test_time_log in new_task.time_logs)

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
        """testing if the DateRangeMixin part is initialized correctly
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
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

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
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

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
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

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
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

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
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

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
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

        Simple case diagram:
        #######
          #######
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0) - datetime.timedelta(5)
        self.kwargs["duration"] = datetime.timedelta(15)

        time_log1 = TimeLog(**self.kwargs)

        # time_log2
        self.kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0)
        self.kwargs["duration"] = datetime.timedelta(15)

        self.assertRaises(OverBookedError, TimeLog, **self.kwargs)

    def test_OverbookedError_8(self):
        """testing if no OverBookedError will be raised when the resource is
        not already booked for the given time period.

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
        """testing if no OverBookedError will be raised when the resource is
        not already booked for the given time period.

        Simple case diagram:
                 #######
        #######
        """
        # time_log1
        self.kwargs["resource"] = self.test_resource2
        self.kwargs["start"] =\
            datetime.datetime(2013, 3, 22, 4, 0) + datetime.timedelta(20)
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


class TimeLogDBTestCase(unittest.TestCase):
    """Tests database interaction of TimeLog instances
    """

    def setUp(self):
        """set up the test
        """
        # create an in memory database
        from stalker import db

        db.setup()
        db.init()

        self.status_wfd = Status.query.filter_by(code='WFD').first()
        self.status_rts = Status.query.filter_by(code='RTS').first()
        self.status_wip = Status.query.filter_by(code='WIP').first()
        self.status_prev = Status.query.filter_by(code='PREV').first()
        self.status_hrev = Status.query.filter_by(code='HREV').first()
        self.status_drev = Status.query.filter_by(code='DREV').first()
        self.status_oh = Status.query.filter_by(code='OH').first()
        self.status_stop = Status.query.filter_by(code='STOP').first()
        self.status_cmpl = Status.query.filter_by(code='CMPL').first()

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

        self.test_task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

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
        from stalker.db.session import DBSession

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

        from stalker.db.session import DBSession

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

    def test_time_log_creation_for_a_WFD_leaf_task(self):
        """testing if a StatusError will be raised when a TimeLog instance
        wanted to be created for a WFD leaf task
        """
        new_task = Task(
            name='Test Task 2',
            project=self.test_project
        )
        new_task.depends = [self.test_task]
        self.kwargs['task'] = new_task
        self.assertRaises(StatusError, TimeLog, **self.kwargs)

    def test_time_log_creation_for_a_RTS_leaf_task(self):
        """testing if the status will be updated to WIP when a TimeLog instance
        is created for a RTS leaf task
        """
        task = self.kwargs['task']
        task.status = self.status_rts
        self.assertEqual(task.status, self.status_rts)
        TimeLog(**self.kwargs)
        self.assertEqual(task.status, self.status_wip)

    def test_time_log_creation_for_a_WIP_leaf_task(self):
        """testing if the status will stay at WIP when a TimeLog instance is
        created for a WIP leaf task
        """
        task = self.kwargs['task']
        task.status = self.status_wip
        self.assertEqual(task.status, self.status_wip)
        TimeLog(**self.kwargs)

    def test_time_log_creation_for_a_PREV_leaf_task(self):
        """testing if the status will stay at PREV when a TimeLog instance is
        created for a PREV leaf task
        """
        task = self.kwargs['task']
        task.status = self.status_prev
        self.assertEqual(task.status, self.status_prev)
        tlog = TimeLog(**self.kwargs)
        self.assertEqual(task.status, self.status_prev)

    def test_time_log_creation_for_a_HREV_leaf_task(self):
        """testing if the status will be updated to WIP when a TimeLog instance
        is created for a HREV leaf task
        """
        task = self.kwargs['task']
        task.status = self.status_hrev
        self.assertEqual(task.status, self.status_hrev)
        TimeLog(**self.kwargs)

    def test_time_log_creation_for_a_DREV_leaf_task(self):
        """testing if the status will stay at DREV when a TimeLog instance is
        created for a DREV leaf task
        """
        task = self.kwargs['task']
        task.status = self.status_drev
        self.assertEqual(task.status, self.status_drev)
        TimeLog(**self.kwargs)

    def test_time_log_creation_for_a_OH_leaf_task(self):
        """testing if a StatusError will be raised when a TimeLog instance is
        created for a OH leaf task
        """
        task = self.kwargs['task']
        task.status = self.status_oh
        self.assertEqual(task.status, self.status_oh)
        self.assertRaises(StatusError, TimeLog, **self.kwargs)

    def test_time_log_creation_for_a_STOP_leaf_task(self):
        """testing if a StatusError will be raised when a TimeLog instance is
        created for a STOP leaf task
        """
        task = self.kwargs['task']
        task.status = self.status_stop
        self.assertEqual(task.status, self.status_stop)
        self.assertRaises(StatusError, TimeLog, **self.kwargs)

    def test_time_log_creation_for_a_CMPL_leaf_task(self):
        """testing if a StatusError will be raised when a TimeLog instance is
        created for a CMPL leaf task
        """
        task = self.kwargs['task']
        task.status = self.status_cmpl
        self.assertEqual(task.status, self.status_cmpl)
        self.assertRaises(StatusError, TimeLog, **self.kwargs)

    def test_time_log_creation_that_violates_dependency_condition_WIP_CMPL_onend(self):
        """testing if a DependencyViolationError will be raised when the entered
        TimeLog will violate the dependency relation of the task

            +--------+
            | Task 1 | ----+
            |  CMPL  |     |
            +--------+     |    +--------+
                           +--->| Task 2 |
                                |  WIP   |
                                +--------+
        """
        task = self.kwargs['task']
        task.status = self.status_cmpl
        task.start = datetime.datetime(2014, 3, 16, 10, 0)
        task.end = datetime.datetime(2014, 3, 25, 19, 0)

        dep_task = Task(
            name="test task 2",
            project=self.test_project,
            status_list=self.test_task_status_list,
            schedule_timing=10,
            schedule_unit='d',
            depends=[task],
            resources=[self.test_resource2]
        )

        # set the dependency target to onend
        dep_task.task_depends_to[0].dependency_target = 'onend'

        # entering a time log to the dates before 2014-03-25-19-0 should raise
        # a ValueError
        with self.assertRaises(DependencyViolationError) as cm:
            dep_task.create_time_log(
                self.test_resource2,
                datetime.datetime(2014, 3, 25, 18, 0),
                datetime.datetime(2014, 3, 25, 19, 0)
            )

        self.assertEqual(
            '\'It is not possible to create a TimeLog before %s, which '
            'violates the dependency relation of "%s" to "%s"\'' % (
                datetime.datetime(2014, 3, 25, 19, 0),
                dep_task.name,
                task.name
            ),
            str(cm.exception)
        )

        # and creating a TimeLog after that is possible
        dep_task.create_time_log(
            self.test_resource2,
            datetime.datetime(2014, 3, 25, 19, 0),
            datetime.datetime(2014, 3, 25, 20, 0)
        )

    def test_time_log_creation_that_violates_dependency_condition_WIP_CMPL_onstart(self):
        """testing if a ValueError will be raised when the entered TimeLog will
        violate the dependency relation of the task

            +--------+
          +-| Task 1 |
          | |  CMPL  |
          | +--------+          +--------+
          +-------------------->| Task 2 |
                                |  WIP   |
                                +--------+
        """
        task = self.kwargs['task']
        task.status = self.status_cmpl
        task.start = datetime.datetime(2014, 3, 16, 10, 0)
        task.end = datetime.datetime(2014, 3, 25, 19, 0)

        dep_task = Task(
            name="test task 2",
            project=self.test_project,
            status_list=self.test_task_status_list,
            schedule_timing=10,
            schedule_unit='d',
            depends=[task],
            resources=[self.test_resource2]
        )

        # set the dependency target to onstart
        dep_task.task_depends_to[0].dependency_target = 'onstart'

        # entering a time log to the dates before 2014-03-16-10-0 should raise
        # a ValueError
        with self.assertRaises(DependencyViolationError) as cm:
            dep_task.create_time_log(
                self.test_resource2,
                datetime.datetime(2014, 3, 16, 9, 0),
                datetime.datetime(2014, 3, 16, 10, 0)
            )

        self.assertEqual(
            '\'It is not possible to create a TimeLog before %s, which '
            'violates the dependency relation of "%s" to "%s"\'' % (
                datetime.datetime(2014, 3, 16, 10, 0),
                dep_task.name,
                task.name
            ),
            str(cm.exception)
        )

        # and creating a TimeLog after that is possible
        dep_task.create_time_log(
            self.test_resource2,
            datetime.datetime(2014, 3, 16, 10, 0),
            datetime.datetime(2014, 3, 16, 10, 0)
        )

