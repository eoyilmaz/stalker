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

from stalker import db
from stalker import (Task, Project, User, Status, StatusList, Repository,
                     Structure, Review, TimeLog)


class ReviewTestCase(unittest2.TestCase):
    """tests the stalker.models.review.Review class
    """

    def setUp(self):
        """set up the test
        """
        db.setup()

        self.user1 = User(
            name='Test User 1',
            login='test_user1',
            email='test1@user.com',
            password='secret'
        )
        self.user2 = User(
            name='Test User 2',
            login='test_user2',
            email='test2@user.com',
            password='secret'
        )
        self.user3 = User(
            name='Test User 2',
            login='test_user3',
            email='test3@user.com',
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
            'task': self.task,
            'reviewer': self.user1
        }
        self.review = Review(**self.kwargs)

    def tearDown(self):
        """clean up test
        """
        db.session.close()

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

    def test_status_is_new_for_a_newly_created_review_instance(self):
        """testing if the status is NEW for a newly created review instance
        """
        review = Review(**self.kwargs)
        self.assertEqual(review.status == self.status_new)

    def test_revision_number_attribute_is_a_read_only_attribute(self):
        """testing if the revision_number attribute is a read only attribute
        """
        review = Review(**self.kwargs)
        self.assertRaises(
            AttributeError, setattr, review, 'revision_number', 2
        )

    def test_revision_number_attribute_is_initialized_to_the_task_revision_number_plus_1(self):
        """testing if the revision_number attribute is initialized with
        task.revision_number + 1
        """
        review = Review(**self.kwargs)
        self.assertEqual(
            self.task.revision_number,
            review.revision_number
        )

    def test_revision_number_for_multiple_responsible_task_is_equal_to_each_other(self):
        """testing if the review.revision_number attribute for each review
        instance created for a task with multiple responsible are equal to each
        other
        """
        self.task.responsible = [self.user1, self.user2, self.user3]
        revisions = self.task.request_revision()
        expected_revision_number = self.task.revision_number + 1

        self.assertEqual(3, len(revisions))

        self.assertEqual(
            expected_revision_number,
            revisions[0].revision_number
        )

        self.assertEqual(
            expected_revision_number,
            revisions[1].revision_number
        )

        self.assertEqual(
            expected_revision_number,
            revisions[2].revision_number
        )

    def test_reviewer_argument_is_skipped(self):
        """testing if a TypeError will be raised when the reviewer argument is
        skipped
        """
        self.kwargs.pop('reviewer')
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_reviewer_argument_is_None(self):
        """testing if a TypeError will be raised when the reviewer argument is
        None
        """
        self.kwargs['reviewer'] = None
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_reviewer_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the reviewer attribute is
        set to None
        """
        review = Review(**self.kwargs)
        self.assertRaises(TypeError, setattr, review, 'reviewer', None)

    def test_reviewer_argument_is_not_a_User_instance(self):
        """testing if a TeypeError will be raised when the reviewer argument is
        not a User instance
        """
        self.kwargs['reviewer'] = 'not a user instance'
        self.assertRaises(TypeError, Review, **self.kwargs)

    def test_reviewer_attribute_is_not_a_User_instance(self):
        """testing if a TypeError will be raised when the reviewer attribute is
        set to a value other than a User instance
        """
        review = Review(**self.kwargs)
        self.assertRaises(TypeError, setattr, review, 'reviewer', 'not a user')

    def test_reviewer_argument_is_not_in_Task_responsible_list(self):
        """testing if it is possible to use some other user which is not in the
        Task.responsible list as the reviewer
        """
        self.task.responsible = [self.user1]
        self.kwargs['reviewer'] = self.user2
        review = Review(**self.kwargs)
        self.assertEqual(review.reviewer, self.user2)

    def test_reviewer_attribute_is_not_in_Task_responsible_list(self):
        """testing if it is possible to use some other user which is not in the
        Task.responsible list as the reviewer
        """
        self.task.responsible = [self.user1]
        self.kwargs['reviewer'] = self.user1
        review = Review(**self.kwargs)
        review.reviewer = self.user2
        self.assertEqual(review.reviewer, self.user2)

    def test_reviewer_argument_is_working_properly(self):
        """testing if the reviewer argument value is correctly passed to
        reviewer attribute
        """
        self.task.responsible = [self.user1]
        self.kwargs['reviewer'] = self.user1
        review = Review(**self.kwargs)
        self.assertEqual(
            self.user1,
            review.reviewer
        )

    def test_reviewer_attribute_is_working_properly(self):
        """testing if the reviewer attribute is working properly
        """
        self.task.responsible = [self.user1, self.user2]
        self.kwargs['reviewer'] = self.user1
        review = Review(**self.kwargs)
        review.reviewer = self.user2
        self.assertEqual(
            self.user2,
            review.reviewer
        )

    # TODO: think about adding tests for the same user is being the reviewer for
    #       multiple reviews with same level with same task

    def test_approve_method_updates_task_status_correctly_for_a_single_responsible_task(self):
        """testing if the Review.approve() method will update the task status
        correctly for a task with only one responsible
        """
        self.task.responsible = [self.user1]
        self.kwargs['reviewer'] = self.user1
        self.assertNotEqual(
            self.status_cmpl,
            self.task.status
        )
        review = Review(**self.kwargs)
        review.approve()
        self.assertEqual(
            self.status_cmpl,
            self.task.status
        )

    def test_approve_method_updates_task_status_correctly_for_a_multi_responsible_task_when_all_approve(self):
        """testing if the Review.approve() method will update the task status
        correctly for a task with multiple responsible
        """
        self.task.responsible = [self.user1, self.user2]
        self.assertNotEqual(
            self.status_cmpl,
            self.task.status
        )

        # first reviewer
        self.kwargs['reviewer'] = self.user1
        review1 = Review(**self.kwargs)
        review1.approve()
        # still pending review
        self.assertEqual(
            self.status_prev,
            self.task.status
        )

        # first reviewer
        self.kwargs['reviewer'] = self.user2
        review2 = Review(**self.kwargs)
        review2.approve()
        self.assertEqual(
            self.status_cmpl,
            self.task.status
        )

    def test_approve_method_updates_task_parent_status(self):
        """testing if approve method will also update the task parent status
        """
        self.fail('test is not implemented yet')

    def test_approve_method_updates_task_status_correctly_for_a_multi_responsible_task_when_one_approve(self):
        """testing if the Review.approve() method will update the task status
        correctly for a task with multiple responsible
        """
        self.task.responsible = [self.user1, self.user2]
        self.assertNotEqual(
            self.status_cmpl,
            self.task.status
        )

        # first reviewer requests a revision
        self.kwargs['reviewer'] = self.user1
        review1 = Review(**self.kwargs)
        review1.request_revision()
        # one requst review should be enough to set the status to hrev,
        # note that this is another tests duty to check
        self.assertEqual(
            self.status_hrev,
            self.task.status
        )

        # first reviewer
        self.kwargs['reviewer'] = self.user2
        review2 = Review(**self.kwargs)
        review2.approve()
        self.assertEqual(
            self.status_hrev,
            self.task.status
        )

    def test_request_revision_method_updates_task_status_correctly_for_a_single_responsible_task(self):
        """testing if the Review.request_revision() method will update the
        task status correctly for a Task with only one responsible
        """
        self.task.responsible = [self.user1]
        self.kwargs['reviewer'] = self.user1
        self.assertNotEqual(
            self.status_cmpl,
            self.task.status
        )
        review = Review(**self.kwargs)
        review.request_revision()
        self.assertEqual(
            self.status_cmpl,
            self.task.status
        )

    def test_request_revision_method_updates_task_status_correctly_for_a_multi_responsible_task_when_one_request_revision(self):
        """testing if the Review.request_revision() method will update the
        task status correctly for a Task with multiple responsible
        """
        self.task.responsible = [self.user1, self.user2]
        self.assertNotEqual(
            self.status_cmpl,
            self.task.status
        )

        # first reviewer requests a revision
        self.kwargs['reviewer'] = self.user1
        review1 = Review(**self.kwargs)
        review1.approve()
        self.assertEqual(
            self.status_prev,
            self.task.status
        )

        # first reviewer
        self.kwargs['reviewer'] = self.user2
        review2 = Review(**self.kwargs)
        review2.request_revision()
        self.assertEqual(
            self.status_hrev,
            self.task.status
        )

    def test_request_revision_method_updates_task_status_correctly_for_a_multi_responsible_task_when_all_request_revision(self):
        """testing if the Review.request_revision() method will update the
        task status correctly for a Task with multiple responsible
        """
        self.task.responsible = [self.user1, self.user2]
        self.assertNotEqual(
            self.status_cmpl,
            self.task.status
        )

        # first reviewer requests a revision
        self.kwargs['reviewer'] = self.user1
        review1 = Review(**self.kwargs)
        review1.request_revision()
        self.assertEqual(
            self.status_hrev,
            self.task.status
        )

        # first reviewer
        self.kwargs['reviewer'] = self.user2
        review2 = Review(**self.kwargs)
        review2.request_revision()
        self.assertEqual(
            self.status_hrev,
            self.task.status
        )

    def test_request_revision_method_updates_parent_task_status(self):
        """testing if the request_revision method also updates the task parent
        statuses
        """
        self.fail('test is not implemented yet')
