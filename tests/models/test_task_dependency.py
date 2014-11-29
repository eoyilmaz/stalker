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

from sqlalchemy.exc import IntegrityError
import unittest

from stalker.db import DBSession
from stalker import (db, Status, User, Repository, Structure, StatusList,
                     Project, Task, TaskDependency, defaults)


class TaskDependencyTestCase(unittest.TestCase):
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
        DBSession.add_all([
            self.test_project1, self.test_project_status_list, self.test_repo,
            self.test_structure, self.test_task1, self.test_task2,
            self.test_task3, self.test_user1, self.test_user2
        ])
        DBSession.commit()

        self.kwargs = {
            'task': self.test_task1,
            'depends_to': self.test_task2,
            'dependency_target': 'onend',
            'gap_timing': 0,
            'gap_unit': 'h',
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
        DBSession.add(new_dependency)
        self.assertRaises(IntegrityError, DBSession.commit)

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
        DBSession.add(new_dependency)
        self.assertRaises(IntegrityError, DBSession.commit)

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

    def test_gap_timing_argument_is_skipped(self):
        """testing if the gap_timing attribute value will be 0 when the
        gap_timing argument is skipped
        """
        self.kwargs.pop('gap_timing')
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_timing, 0)

    def test_gap_timing_argument_is_None(self):
        """testing if the gap_timing attribute value will be 0 when the
        gap_timing argument value is None
        """
        self.kwargs['gap_timing'] = None
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_timing, 0)

    def test_gap_timing_attribute_is_set_to_None(self):
        """testing if the gap_timing attribute value will be 0 when it is set
        to None
        """
        tdep = TaskDependency(**self.kwargs)
        tdep.gap_timing = None
        self.assertEqual(tdep.gap_timing, 0)

    def test_gap_timing_argument_is_not_a_float(self):
        """testing if a TypeError will be raised when the gap_timing argument
        value is not a float value
        """
        self.kwargs['gap_timing'] = 'not a time delta'
        self.assertRaises(TypeError, TaskDependency, **self.kwargs)

    def test_gap_timing_attribute_is_not_a_float(self):
        """testing if a TypeError will be raised when the gap_timing attribute
        value is set to a value other than a float
        """
        tdep = TaskDependency(**self.kwargs)
        self.assertRaises(TypeError, setattr, tdep, 'gap_timing', 'not float')

    def test_gap_timing_argument_is_working_properly(self):
        """testing if the gap_timing argument value is correctly passed to the
        gap_timing attribute
        """
        test_value = 11
        self.kwargs['gap_timing'] = test_value
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_timing, test_value)

    def test_gap_timing_attribute_is_working_properly(self):
        """testing if the gap_timing attribute is working properly
        """
        tdep = TaskDependency(**self.kwargs)
        test_value = 11
        tdep.gap_timing = test_value
        self.assertEqual(tdep.gap_timing, test_value)

    def test_gap_unit_argument_is_skipped(self):
        """testing if the default value will be used when the gap_unit argument
        is skipped
        """
        self.kwargs.pop('gap_unit')
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_unit,
                         TaskDependency.__default_schedule_unit__)

    def test_gap_unit_argument_is_None(self):
        """testing if the default value will be used when the gap_unit argument
        is None
        """
        self.kwargs['gap_unit'] = None
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_unit,
                         TaskDependency.__default_schedule_unit__)

    def test_gap_unit_attribute_is_None(self):
        """testing if the default value will be used when the gap_unit
        attribute is set to None
        """
        tdep = TaskDependency(**self.kwargs)
        tdep.gap_unit = None
        self.assertEqual(tdep.gap_unit,
                         TaskDependency.__default_schedule_unit__)

    def test_gap_unit_argument_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_unit argument is
        not a string
        """
        self.kwargs['gap_unit'] = 231
        self.assertRaises(TypeError, TaskDependency, **self.kwargs)

    def test_gap_unit_attribute_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_unit attribute
        is not a string
        """
        tdep = TaskDependency(**self.kwargs)
        self.assertRaises(TypeError, setattr, tdep, 'gap_unit', 2342)

    def test_gap_unit_argument_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_unit argument
        value is not one of ['min', 'h', 'd', 'w', 'm', 'y']
        """
        self.kwargs['gap_unit'] = 'not in the list'
        self.assertRaises(ValueError, TaskDependency, **self.kwargs)

    def test_gap_unit_attribute_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_unit attribute
        value is not one of ['min', 'h', 'd', 'w', 'm', 'y']
        """
        tdep = TaskDependency(**self.kwargs)
        self.assertRaises(ValueError, setattr, tdep, 'gap_unit',
                          'not in the list')

    def test_gap_unit_argument_is_working_properly(self):
        """testing if the gap_unit argument value is correctly passed to the
        gap_unit attribute on init
        """
        test_value = 'y'
        self.kwargs['gap_unit'] = test_value
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(test_value, tdep.gap_unit)

    def test_gap_unit_attribute_is_working_properly(self):
        """testing if the gap_unit attribute is working properly
        """
        tdep = TaskDependency(**self.kwargs)
        test_value = 'w'
        self.assertNotEqual(tdep.gap_unit, test_value)
        tdep.gap_unit = test_value
        self.assertEqual(tdep.gap_unit, test_value)

    def test_gap_model_argument_is_skipped(self):
        """testing if the default value will be used when the gap_model
        argument is skipped
        """
        self.kwargs.pop('gap_model')
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_model,
                         defaults.task_dependency_gap_models[0])

    def test_gap_model_argument_is_None(self):
        """testing if the default value will be used when the gap_model
        argument is None
        """
        self.kwargs['gap_model'] = None
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_model,
                         defaults.task_dependency_gap_models[0])

    def test_gap_model_attribute_is_None(self):
        """testing if the default value will be used when the gap_model
        attribute is set to None
        """
        tdep = TaskDependency(**self.kwargs)
        tdep.gap_model = None
        self.assertEqual(tdep.gap_model,
                         defaults.task_dependency_gap_models[0])

    def test_gap_model_argument_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_model argument is
        not a string
        """
        self.kwargs['gap_model'] = 231
        self.assertRaises(TypeError, TaskDependency, **self.kwargs)

    def test_gap_model_attribute_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_model attribute
        is not a string
        """
        tdep = TaskDependency(**self.kwargs)
        self.assertRaises(TypeError, setattr, tdep, 'gap_model', 2342)

    def test_gap_model_argument_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_model argument
        value is not one of ['duration', 'length']
        """
        self.kwargs['gap_model'] = 'not in the list'
        self.assertRaises(ValueError, TaskDependency, **self.kwargs)

    def test_gap_model_attribute_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_model attribute
        value is not one of ['duration', 'length']
        """
        tdep = TaskDependency(**self.kwargs)
        self.assertRaises(ValueError, setattr, tdep, 'gap_model',
                          'not in the list')

    def test_gap_model_argument_is_working_properly(self):
        """testing if the gap_model argument value is correctly passed to the
        gap_model attribute on init
        """
        test_value = 'duration'
        self.kwargs['gap_model'] = test_value
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(test_value, tdep.gap_model)

    def test_gap_model_attribute_is_working_properly(self):
        """testing if the gap_model attribute is working properly
        """
        tdep = TaskDependency(**self.kwargs)
        test_value = 'duration'
        self.assertNotEqual(tdep.gap_model, test_value)
        tdep.gap_model = test_value
        self.assertEqual(tdep.gap_model, test_value)

    def test_dependency_target_argument_is_skipped(self):
        """testing if the default value will be used when the dependency_target
        argument is skipped
        """
        self.kwargs.pop('dependency_target')
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.dependency_target,
                         defaults.task_dependency_targets[0])

    def test_dependency_target_argument_is_None(self):
        """testing if the default value will be used when the dependency_target
        argument is None
        """
        self.kwargs['dependency_target'] = None
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.dependency_target,
                         defaults.task_dependency_targets[0])

    def test_dependency_target_attribute_is_None(self):
        """testing if the default value will be used when the dependency_target
        attribute is set to None
        """
        tdep = TaskDependency(**self.kwargs)
        tdep.dependency_target = None
        self.assertEqual(tdep.dependency_target,
                         defaults.task_dependency_targets[0])

    def test_dependency_target_argument_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the dependency_target
        argument is not a string
        """
        self.kwargs['dependency_target'] = 0
        self.assertRaises(TypeError, TaskDependency, **self.kwargs)

    def test_dependency_target_attribute_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the dependency_target
        attribute is not a string
        """
        tdep = TaskDependency(**self.kwargs)
        self.assertRaises(TypeError, setattr, tdep, 'dependency_target', 0)

    def test_dependency_target_argument_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the dependency_target
        argument value is not one of ['duration', 'length']
        """
        self.kwargs['dependency_target'] = 'not in the list'
        self.assertRaises(ValueError, TaskDependency, **self.kwargs)

    def test_dependency_target_attribute_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the dependency_target
        attribute value is not one of ['duration', 'length']
        """
        tdep = TaskDependency(**self.kwargs)
        self.assertRaises(ValueError, setattr, tdep, 'dependency_target',
                          'not in the list')

    def test_dependency_target_argument_is_working_properly(self):
        """testing if the dependency_target argument value is correctly passed
        to the dependency_target attribute on init
        """
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.dependency_target, 'onend')

    def test_dependency_target_attribute_is_working_properly(self):
        """testing if the dependency_target attribute is working properly
        """
        tdep = TaskDependency(**self.kwargs)
        onstart = 'onstart'
        tdep.dependency_target = onstart
        self.assertEqual(onstart, tdep.dependency_target)
