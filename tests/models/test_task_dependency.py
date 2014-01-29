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

import datetime
from sqlalchemy.exc import IntegrityError
import unittest2
from stalker import db, Status, User, Repository, Structure, StatusList, Project, Task, TaskDependency


class TaskDependencyTestCase(unittest2.TestCase):
    """tests the TaskDependency class
    """

    def setUp(self):
        """set up the test
        """
        db.setup()
        db.init()

        # get statuses
        self.status_new = Status.query.filter_by(code="NEW").first()
        self.status_wfd = Status.query.filter_by(code="WFD").first()
        self.status_rts = Status.query.filter_by(code="RTS").first()
        self.status_wip = Status.query.filter_by(code="WIP").first()
        self.status_prev = Status.query.filter_by(code="PREV").first()
        self.status_hrev = Status.query.filter_by(code="HREV").first()
        self.status_drev = Status.query.filter_by(code="DREV").first()
        self.status_oh = Status.query.filter_by(code="OH").first()
        self.status_stop = Status.query.filter_by(code="STOP").first()
        self.status_cmpl = Status.query.filter_by(code="CMPL").first()

        self.test_user1 = User(
            name='Test User 1',
            login='testuser1',
            email='user1@test.com',
            password='secret'
        )

        self.test_user2 = User(
            name='Test User 2',
            login='testuser2',
            email='user2@test.com',
            password='secret'
        )

        self.test_user3 = User(
            name='Test User 1',
            login='testuser1',
            email='user1@test.com',
            password='secret'
        )

        self.test_repo = Repository(
            name='Test Repository'
        )

        self.test_structure = Structure(
            name='test structure'
        )

        # project status list
        self.test_project_status_list = StatusList(
            name='Project Statuses',
            target_entity_type='Project',
            statuses=[
                self.status_new,
                self.status_wip,
                self.status_oh,
                self.status_stop,
                self.status_cmpl
            ]
        )
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            lead=self.test_user1,
            repository=self.test_repo,
            structure=self.test_structure,
            status_list=self.test_project_status_list
        )

        # create three Tasks
        self.test_task1 = Task(
            name='Test Task 1',
            project=self.test_project1
        )

        self.test_task2 = Task(
            name='Test Task 2',
            project=self.test_project1
        )

        self.test_task3 = Task(
            name='Test Task 3',
            project=self.test_project1
        )

        # add everything to db
        db.session.add_all([
            self.test_project1, self.test_project_status_list, self.test_repo,
            self.test_structure, self.test_task1, self.test_task2,
            self.test_task3, self.test_user1, self.test_user2
        ])
        db.session.commit()

        self.kwargs = {
            'task': self.test_task1,
            'depends_to': self.test_task2,
            'dependency_type': 'onend',
            'gap': datetime.timedelta(hours=0),
            'gap_model': 'length'
        }

    def test_task_argument_is_skipped(self):
        """testing if no error will be raised when the task argument is skipped
        """
        self.kwargs.pop('task')
        TaskDependency(**self.kwargs)

    def test_task_argument_is_skipped_raises_error_on_commit(self):
        """testing if an Integrity error will be raised when the task argument
        is skipped and the session is committed
        """
        self.kwargs.pop('task')
        new_dependency = TaskDependency(**self.kwargs)
        db.session.add(new_dependency)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_task_argument_is_not_a_task_instance(self):
        """testing if a TypeError will be raised when the task argument value
        is not a stalker.models.task.Task instance
        """
        self.kwargs['task'] = 'Not a Task instance'
        self.assertRaises(TypeError, TaskDependency, **self.kwargs)

    def test_task_attribute_is_not_a_task_instance(self):
        """testing if a TypeError will be raised when the task attribute value
        is not a stalker.models.task.Task instance
        """
        new_dep = TaskDependency(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_dep, 'task', 'not a task')

    def test_task_argument_is_working_properly(self):
        """testing if the task argument value is correctly passed to task
        attribute
        """
        self.test_task1.depends = []
        new_dep = TaskDependency(**self.kwargs)
        self.assertEqual(new_dep.task, self.test_task1)

    def test_depends_to_argument_is_skipped(self):
        """testing if no error will be raised when the depends_to argument is
        skipped
        """
        self.kwargs.pop('depends_to')
        TaskDependency(**self.kwargs)

    def test_depends_to_argument_is_skipped_raises_error_on_commit(self):
        """testing if an Integrity error will be raised when the depends_to
        argument is skipped and the session is committed
        """
        self.kwargs.pop('depends_to')
        new_dependency = TaskDependency(**self.kwargs)
        db.session.add(new_dependency)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_depends_to_argument_is_not_a_task_instance(self):
        """testing if a TypeError will be raised when the depends_to argument
        value is not a stalker.models.task.Task instance
        """
        self.kwargs['depends_to'] = 'Not a Task instance'
        self.assertRaises(TypeError, TaskDependency, **self.kwargs)

    def test_depends_to_attribute_is_not_a_task_instance(self):
        """testing if a TypeError will be raised when the depends_to attribute
        value is not a stalker.models.task.Task instance
        """
        new_dep = TaskDependency(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_dep, 'depends_to',
                          'not a task')

    def test_depends_to_argument_is_working_properly(self):
        """testing if the depends_to argument value is correctly passed to
        depends_to attribute
        """
        self.test_task1.depends = []
        new_dep = TaskDependency(**self.kwargs)
        self.assertEqual(new_dep.depends_to, self.test_task2)

    def test_gap_argument_is_skipped(self):
        """testing if the gap attribute value will be a datetime.timedelta with
        0 duration when the gap argument is skipped
        """
        self.fail('test is not implemented yet')

    def test_gap_argument_is_None(self):
        """testing if the gap attribute value will be a datetime.timedelta with
        0 duration when the gap argument value is Non
        """
        self.fail('test is not implemented yet')

    def test_gap_attribute_is_set_to_None(self):
        """testing if the gap attribute value will be a datetime.timedelta with
        0 duration when the gap attribute is set to None
        """
        self.fail('test is not implemented yet')

    def test_gap_argument_is_not_a_timedelta(self):
        """testing if a TypeError will be raised when the gap argument value is
        not a datetime.timedelta instance
        """
        self.fail('test is not implemented yet')

    def test_gap_attribute_is_not_a_timedelta(self):
        """testing if a TypeError will be raised when the gap attribute value
        is set to a value other than a datetime.timedelta instance
        """
        self.fail('test is not implemented yet')

    def test_gap_argument_is_working_properly(self):
        """testing if the gap argument value is correctly passed to the gap
        attribute
        """
        self.fail('test is not implemented yet')

    def test_gap_attribute_is_working_properly(self):
        """testing if the gap attribute is working properly
        """
        self.fail('test is not implemented yet')

    def test_gap_model_argument_is_skipped(self):
        """testing if the default value will be used when the gap_model
        argument is skipped
        """
        self.fail('test is not implemented yet')

    def test_gap_model_argument_is_None(self):
        """testing if the default value will be used when the gap_model
        argument is None
        """
        self.fail('test is not implemented yet')

    def test_gap_model_attribute_is_None(self):
        """testing if the default value will be used when the gap_model
        attribute is set to None
        """
        self.fail('test is not implemented yet')

    def test_gap_model_argument_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_model argument is
        not a string
        """
        self.fail('test is not implemented yet')

    def test_gap_model_attribute_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_model attribute
        is not a string
        """
        self.fail('test is not impelemented yet')

    def test_gap_model_argument_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_model argument
        value is not one of ['duration', 'length']
        """
        self.fail('test is not impelemented yet')

    def test_gap_model_attribute_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_model attribute
        value is not one of ['duration', 'length']
        """
        self.fail('test is not implemented yet')

    def test_gap_model_argument_is_working_properly(self):
        """testing if the gap_model argument value is correctly passed to the
        gap_model attribute on init
        """
        self.fail('test is not implemented yet')

    def test_gap_model_attribute_is_working_properly(self):
        """testing if the gap_model attribute is working properly
        """
        self.fail('test is not implemented yet')

    def test_dependency_type_argument_is_skipped(self):
        """testing if the default value will be used when the dependency_type
        argument is skipped
        """
        self.fail('test is not implemented yet')

    def test_dependency_type_argument_is_None(self):
        """testing if the default value will be used when the dependency_type
        argument is None
        """
        self.fail('test is not implemented yet')

    def test_dependency_type_attribute_is_None(self):
        """testing if the default value will be used when the dependency_type
        attribute is set to None
        """
        self.fail('test is not implemented yet')

    def test_dependency_type_argument_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the dependency_type
        argument is not a string
        """
        self.fail('test is not implemented yet')

    def test_dependency_type_attribute_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the dependency_type
        attribute is not a string
        """
        self.fail('test is not impelemented yet')

    def test_dependency_type_argument_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the dependency_type
        argument value is not one of ['duration', 'length']
        """
        self.fail('test is not impelemented yet')

    def test_dependency_type_attribute_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the dependency_type
        attribute value is not one of ['duration', 'length']
        """
        self.fail('test is not implemented yet')

    def test_dependency_type_argument_is_working_properly(self):
        """testing if the dependency_type argument value is correctly passed to
        the dependency_type attribute on init
        """
        self.fail('test is not implemented yet')

    def test_dependency_type_attribute_is_working_properly(self):
        """testing if the dependency_type attribute is working properly
        """
        self.fail('test is not implemented yet')
