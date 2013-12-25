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

import tempfile
import datetime
import unittest2

from stalker import (Task, Project, User, Status, StatusList, Repository,
                     Structure, Review, TimeLog)


class ReviewTestCase(unittest2.TestCase):
    """tests the stalker.models.review.Review class
    """

    def setUp(self):
        """set up the test
        """
        self.user1 = User(
            name='Test User',
            login='test_user',
            email='test@user.com',
            password='secret'
        )

        self.status_new = Status(name='New', code='NEW')
        self.status_rts = Status(name='Ready To Start', code='RTS')
        self.status_wip = Status(name='Work In Progress', code='WIP')
        self.status_prev = Status(name='Pending Review', code='PREV')
        self.status_hrev = Status(name='Has Review', code='HREV')
        self.status_cmpl = Status(name='Complete', code='CMPL')

        # Review Statuses
        self.status_app = Status(name='Approved', code='APP')
        self.status_rrev = Status(name='Request Review', code='RREV')

        self.project_status_list = StatusList(
            target_entity_type='Project',
            statuses=[
                self.status_new, self.status_wip, self.status_cmpl
            ]
        )

        self.task_status_list = StatusList(
            target_entity_type='Task',
            statuses=[
                self.status_new, self.status_rts, self.status_wip,
                self.status_prev, self.status_hrev, self.status_cmpl
            ]
        )

        self.review_status_list = StatusList(
            target_entity_type='Review',
            statuses=[
                self.status_new, self.status_rrev, self.status_app
            ]
        )

        self.temp_path = tempfile.mkdtemp()
        self.repo = Repository(
            name='Test Repository',
            linux_path=self.temp_path,
            windows_path=self.temp_path,
            osx_path=self.temp_path
        )

        self.structure = Structure(
            name='Test Project Structure'
        )

        self.project = Project(
            name='Test Project',
            code='TP',
            lead=self.user1,
            status_list=self.project_status_list,
            repository=self.repo
        )

        self.task = Task(
            name='Test Task',
            project=self.project,
            status_list=self.task_status_list
        )

        self.kwargs = {
            'task': self.task
        }
        self.review = Review(**self.kwargs)

    def test_task_argument_is_skipped(self):
        """testing if a TypeError will be raised when the task argument is
        skipped
        """
        self.kwargs.pop('task')
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_task_argument_is_None(self):
        """testing if a TypeError will be raised when the task argument is None
        """
        self.kwargs['task'] = None
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_task_argument_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the task argument value
        is not a Task instance
        """
        self.kwargs['task'] = 'not a Task instance'
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_task_attribute_is_read_only(self):
        """testing if a the task attribute is read only
        """
        self.assertRaises(AttributeError, setattr, self.review, 'task',
                          self.task)

    def test_task_argument_is_not_a_leaf_task(self):
        """testing if a ValueError will be raised when the task given in task
        argument is not a leaf task
        """
        task1 = Task(
            name='Task1',
            project=self.project,
            status_list=self.task_status_list
        )
        task2 = Task(
            name='Task2',
            parent=task1,
            status_list=self.task_status_list
        )
        self.kwargs['task'] = task1
        self.assertRaises(ValueError, Review, **self.kwargs)

    def test_task_argument_is_working_properly(self):
        """testing if the task argument value is passed to the task argument
        properly
        """
        self.assertEqual(self.review.task, self.task)

    def test_auto_name_is_true(self):
        """testing if review instances are named automatically
        """
        self.assertTrue(Review.__auto_name__)

    def test_task_argument_schedule_timing_values_are_clipped_and_extended_with_Review_schedule_info_if_the_review_is_rrev(self):
        """testing if the task given with the task argument schedule timing
        values are capped to the current total logged seconds and then it is
        extended with the review timing values when the review.status is RREV
        """
        task1 = Task(
            name='Test Task 2',
            project=self.project,
            status_list=self.task_status_list,
            schedule_timing=2,
            schedule_unit='d',
            schedule_model='effort',
            resources=[self.user1]
        )

        dt = datetime.datetime
        td = datetime.timedelta

        # create some time logs
        tlog1 = TimeLog(
            task=task1,
            resource=self.user1,
            start=dt.now(),
            end=dt.now() + td(hours=5)
        )

        # now create a review for that task
        rev1 = Review(
            task=task1,
            schedule_timing=1,
            schedule_unit='h'
        )

        # expect the schedule_unit of the task to be hours
        self.assertEqual(task1.schedule_unit, 'h')

        # and the schedule_timing of 6
        self.assertEqual(task1.schedule_timing, 6)

        # create another review with 15 minutes of schedule timing
        rev2 = Review(
            task=task1,
            schedule_timing=15,
            schedule_unit='min'
        )

        # and expect the schedule_unit to be converted to minutes
        self.assertEqual(task1.schedule_unit, 'min')

        # and the schedule_timing of 375
        self.assertEqual(task1.schedule_timing, 315)

        rev3 = Review(
            task=task1,
            schedule_timing=120,
            schedule_unit='min'
        )
        # and expect the schedule_unit to be converted to minutes
        self.assertEqual(task1.schedule_unit, 'h')

        # and the schedule_timing of 375
        self.assertEqual(task1.schedule_timing, 7)
