# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2017 Erkan Ozgur Yilmaz
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

import pytest
from stalker.testing import UnitTestDBBase


class TaskDependencyTestDBCase(UnitTestDBBase):
    """tests the TaskDependency class
    """

    def setUp(self):
        """set up the test
        """
        super(TaskDependencyTestDBCase, self).setUp()

        from stalker.db.session import DBSession
        from stalker import User
        self.test_user1 = User(
            name='Test User 1',
            login='testuser1',
            email='user1@test.com',
            password='secret'
        )
        DBSession.add(self.test_user1)

        self.test_user2 = User(
            name='Test User 2',
            login='testuser2',
            email='user2@test.com',
            password='secret'
        )
        DBSession.add(self.test_user2)

        self.test_user3 = User(
            name='Test User 3',
            login='testuser3',
            email='user3@test.com',
            password='secret'
        )
        DBSession.add(self.test_user3)

        from stalker import Repository
        self.test_repo = Repository(
            name='Test Repository'
        )
        DBSession.add(self.test_repo)

        from stalker import Structure
        self.test_structure = Structure(
            name='test structure'
        )
        DBSession.add(self.test_structure)

        from stalker import Project
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            repository=self.test_repo,
            structure=self.test_structure,
        )
        DBSession.add(self.test_project1)
        DBSession.commit()

        # create three Tasks
        from stalker import Task
        self.test_task1 = Task(
            name='Test Task 1',
            project=self.test_project1
        )
        DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Test Task 2',
            project=self.test_project1
        )
        DBSession.add(self.test_task2)

        self.test_task3 = Task(
            name='Test Task 3',
            project=self.test_project1
        )
        DBSession.add(self.test_task3)
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
        from stalker import TaskDependency
        TaskDependency(**self.kwargs)

    def test_task_argument_is_skipped_raises_error_on_commit(self):
        """testing if an Integrity error will be raised when the task argument
        is skipped and the session is committed
        """
        from stalker.db.session import DBSession
        from stalker import TaskDependency
        from sqlalchemy.exc import IntegrityError
        self.kwargs.pop('task')
        new_dependency = TaskDependency(**self.kwargs)
        DBSession.add(new_dependency)
        with pytest.raises(IntegrityError) as cm:
            DBSession.commit()

        assert '(psycopg2.IntegrityError) null value in column "task_id" ' \
               'violates not-null constraint' in str(cm.value)

    def test_task_argument_is_not_a_task_instance(self):
        """testing if a TypeError will be raised when the task argument value
        is not a stalker.models.task.Task instance
        """
        self.kwargs['task'] = 'Not a Task instance'
        with self.assertRaises(TypeError) as cm:
            from stalker import TaskDependency
            TaskDependency(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'TaskDependency.task should be and instance of '
            'stalker.models.task.Task, not str'
        )

    def test_task_attribute_is_not_a_task_instance(self):
        """testing if a TypeError will be raised when the task attribute value
        is not a stalker.models.task.Task instance
        """
        from stalker import TaskDependency
        new_dep = TaskDependency(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            new_dep.task = 'not a task'

        self.assertEqual(
            str(cm.exception),
            'TaskDependency.task should be and instance of '
            'stalker.models.task.Task, not str'
        )

    def test_task_argument_is_working_properly(self):
        """testing if the task argument value is correctly passed to task
        attribute
        """
        from stalker import TaskDependency
        self.test_task1.depends = []
        new_dep = TaskDependency(**self.kwargs)
        self.assertEqual(new_dep.task, self.test_task1)

    def test_depends_to_argument_is_skipped(self):
        """testing if no error will be raised when the depends_to argument is
        skipped
        """
        from stalker import TaskDependency
        self.kwargs.pop('depends_to')
        TaskDependency(**self.kwargs)

    def test_depends_to_argument_is_skipped_raises_error_on_commit(self):
        """testing if an Integrity error will be raised when the depends_to
        argument is skipped and the session is committed
        """
        self.kwargs.pop('depends_to')
        from stalker.db.session import DBSession
        from stalker import TaskDependency
        from sqlalchemy.exc import IntegrityError
        new_dependency = TaskDependency(**self.kwargs)
        DBSession.add(new_dependency)
        with self.assertRaises(IntegrityError) as cm:
            DBSession.commit()

        self.assertTrue(
            str(cm.exception).startswith(
                '(psycopg2.IntegrityError) null value in column '
                '"depends_to_id" violates not-null constraint'
            )
        )

    def test_depends_to_argument_is_not_a_task_instance(self):
        """testing if a TypeError will be raised when the depends_to argument
        value is not a stalker.models.task.Task instance
        """
        self.kwargs['depends_to'] = 'Not a Task instance'
        from stalker import TaskDependency
        with self.assertRaises(TypeError) as cm:
            TaskDependency(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'TaskDependency.depends_to can should be and instance of '
            'stalker.models.task.Task, not str'
        )

    def test_depends_to_attribute_is_not_a_task_instance(self):
        """testing if a TypeError will be raised when the depends_to attribute
        value is not a stalker.models.task.Task instance
        """
        from stalker import TaskDependency
        new_dep = TaskDependency(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            new_dep.depends_to = 'not a task'

        self.assertEqual(
            str(cm.exception),
            'TaskDependency.depends_to can should be and instance of '
            'stalker.models.task.Task, not str'
        )

    def test_depends_to_argument_is_working_properly(self):
        """testing if the depends_to argument value is correctly passed to
        depends_to attribute
        """
        from stalker import TaskDependency
        self.test_task1.depends = []
        new_dep = TaskDependency(**self.kwargs)
        self.assertEqual(new_dep.depends_to, self.test_task2)

    def test_gap_timing_argument_is_skipped(self):
        """testing if the gap_timing attribute value will be 0 when the
        gap_timing argument is skipped
        """
        self.kwargs.pop('gap_timing')
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_timing, 0)

    def test_gap_timing_argument_is_None(self):
        """testing if the gap_timing attribute value will be 0 when the
        gap_timing argument value is None
        """
        self.kwargs['gap_timing'] = None
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_timing, 0)

    def test_gap_timing_attribute_is_set_to_None(self):
        """testing if the gap_timing attribute value will be 0 when it is set
        to None
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        tdep.gap_timing = None
        self.assertEqual(tdep.gap_timing, 0)

    def test_gap_timing_argument_is_not_a_float(self):
        """testing if a TypeError will be raised when the gap_timing argument
        value is not a float value
        """
        self.kwargs['gap_timing'] = 'not a time delta'
        from stalker import TaskDependency
        with self.assertRaises(TypeError) as cm:
            TaskDependency(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'TaskDependency.gap_timing should be an integer or float number '
            'showing the value of the gap timing of this TaskDependency, not '
            'str'
        )

    def test_gap_timing_attribute_is_not_a_float(self):
        """testing if a TypeError will be raised when the gap_timing attribute
        value is set to a value other than a float
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            tdep.gap_timing = 'not float'

        self.assertEqual(
            str(cm.exception),
            'TaskDependency.gap_timing should be an integer or float number '
            'showing the value of the gap timing of this TaskDependency, '
            'not str'
        )

    def test_gap_timing_argument_is_working_properly(self):
        """testing if the gap_timing argument value is correctly passed to the
        gap_timing attribute
        """
        from stalker import TaskDependency
        test_value = 11
        self.kwargs['gap_timing'] = test_value
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.gap_timing, test_value)

    def test_gap_timing_attribute_is_working_properly(self):
        """testing if the gap_timing attribute is working properly
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        test_value = 11
        tdep.gap_timing = test_value
        self.assertEqual(tdep.gap_timing, test_value)

    def test_gap_unit_argument_is_skipped(self):
        """testing if the default value will be used when the gap_unit argument
        is skipped
        """
        from stalker import TaskDependency
        self.kwargs.pop('gap_unit')
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(
            tdep.gap_unit,
            TaskDependency.__default_schedule_unit__
        )

    def test_gap_unit_argument_is_None(self):
        """testing if the default value will be used when the gap_unit argument
        is None
        """
        from stalker import TaskDependency
        self.kwargs['gap_unit'] = None
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(
            tdep.gap_unit,
            TaskDependency.__default_schedule_unit__
        )

    def test_gap_unit_attribute_is_None(self):
        """testing if the default value will be used when the gap_unit
        attribute is set to None
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        tdep.gap_unit = None
        self.assertEqual(
            tdep.gap_unit,
            TaskDependency.__default_schedule_unit__
        )

    def test_gap_unit_argument_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_unit argument is
        not a string
        """
        from stalker import TaskDependency
        self.kwargs['gap_unit'] = 231
        with self.assertRaises(TypeError) as cm:
            TaskDependency(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.gap_unit should be a string value one of ['min', "
            "'h', 'd', 'w', 'm', 'y'] showing the unit of the gap timing of "
            "this TaskDependency, not int"
        )

    def test_gap_unit_attribute_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_unit attribute
        is not a string
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            tdep.gap_unit = 2342

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.gap_unit should be a string value one of ['min', "
            "'h', 'd', 'w', 'm', 'y'] showing the unit of the gap timing of "
            "this TaskDependency, not int"
        )

    def test_gap_unit_argument_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_unit argument
        value is not one of ['min', 'h', 'd', 'w', 'm', 'y']
        """
        from stalker import TaskDependency
        self.kwargs['gap_unit'] = 'not in the list'
        with self.assertRaises(ValueError) as cm:
            TaskDependency(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.gap_unit should be a string value one of ['min', "
            "'h', 'd', 'w', 'm', 'y'] showing the unit of the gap timing of "
            "this TaskDependency, not str"
        )

    def test_gap_unit_attribute_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_unit attribute
        value is not one of ['min', 'h', 'd', 'w', 'm', 'y']
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        with self.assertRaises(ValueError) as cm:
            tdep.gap_unit = 'not in the list'

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.gap_unit should be a string value one of ['min', "
            "'h', 'd', 'w', 'm', 'y'] showing the unit of the gap timing of "
            "this TaskDependency, not str"
        )

    def test_gap_unit_argument_is_working_properly(self):
        """testing if the gap_unit argument value is correctly passed to the
        gap_unit attribute on init
        """
        from stalker import TaskDependency
        test_value = 'y'
        self.kwargs['gap_unit'] = test_value
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(test_value, tdep.gap_unit)

    def test_gap_unit_attribute_is_working_properly(self):
        """testing if the gap_unit attribute is working properly
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        test_value = 'w'
        self.assertNotEqual(tdep.gap_unit, test_value)
        tdep.gap_unit = test_value
        self.assertEqual(tdep.gap_unit, test_value)

    def test_gap_model_argument_is_skipped(self):
        """testing if the default value will be used when the gap_model
        argument is skipped
        """
        from stalker import defaults, TaskDependency
        self.kwargs.pop('gap_model')
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(
            tdep.gap_model,
            defaults.task_dependency_gap_models[0]
        )

    def test_gap_model_argument_is_None(self):
        """testing if the default value will be used when the gap_model
        argument is None
        """
        from stalker import defaults, TaskDependency
        self.kwargs['gap_model'] = None
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(
            tdep.gap_model,
            defaults.task_dependency_gap_models[0]
        )

    def test_gap_model_attribute_is_None(self):
        """testing if the default value will be used when the gap_model
        attribute is set to None
        """
        from stalker import defaults, TaskDependency
        tdep = TaskDependency(**self.kwargs)
        tdep.gap_model = None
        self.assertEqual(
            tdep.gap_model,
            defaults.task_dependency_gap_models[0]
        )

    def test_gap_model_argument_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_model argument is
        not a string
        """
        from stalker import TaskDependency
        self.kwargs['gap_model'] = 231
        with self.assertRaises(TypeError) as cm:
            TaskDependency(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.gap_model should be one of ['length', "
            "'duration'], not int"
        )

    def test_gap_model_attribute_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the gap_model attribute
        is not a string
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            tdep.gap_model = 2342

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.gap_model should be one of ['length', "
            "'duration'], not int"
        )

    def test_gap_model_argument_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_model argument
        value is not one of ['duration', 'length']
        """
        from stalker import TaskDependency
        self.kwargs['gap_model'] = 'not in the list'
        with self.assertRaises(ValueError) as cm:
            TaskDependency(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.gap_model should be one of ['length', "
            "'duration'], not str"
        )

    def test_gap_model_attribute_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the gap_model attribute
        value is not one of ['duration', 'length']
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        with self.assertRaises(ValueError) as cm:
            tdep.gap_model = 'not in the list'

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.gap_model should be one of ['length', "
            "'duration'], not str"
        )

    def test_gap_model_argument_is_working_properly(self):
        """testing if the gap_model argument value is correctly passed to the
        gap_model attribute on init
        """
        from stalker import TaskDependency
        test_value = 'duration'
        self.kwargs['gap_model'] = test_value
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(test_value, tdep.gap_model)

    def test_gap_model_attribute_is_working_properly(self):
        """testing if the gap_model attribute is working properly
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        test_value = 'duration'
        self.assertNotEqual(tdep.gap_model, test_value)
        tdep.gap_model = test_value
        self.assertEqual(tdep.gap_model, test_value)

    def test_dependency_target_argument_is_skipped(self):
        """testing if the default value will be used when the dependency_target
        argument is skipped
        """
        from stalker import defaults, TaskDependency
        self.kwargs.pop('dependency_target')
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.dependency_target,
                         defaults.task_dependency_targets[0])

    def test_dependency_target_argument_is_None(self):
        """testing if the default value will be used when the dependency_target
        argument is None
        """
        from stalker import defaults, TaskDependency
        self.kwargs['dependency_target'] = None
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.dependency_target,
                         defaults.task_dependency_targets[0])

    def test_dependency_target_attribute_is_None(self):
        """testing if the default value will be used when the dependency_target
        attribute is set to None
        """
        from stalker import defaults, TaskDependency
        tdep = TaskDependency(**self.kwargs)
        tdep.dependency_target = None
        self.assertEqual(tdep.dependency_target,
                         defaults.task_dependency_targets[0])

    def test_dependency_target_argument_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the dependency_target
        argument is not a string
        """
        from stalker import TaskDependency
        self.kwargs['dependency_target'] = 0
        with self.assertRaises(TypeError) as cm:
            TaskDependency(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.dependency_target should be a string with a value "
            "one of ['onend', 'onstart'], not int"
        )

    def test_dependency_target_attribute_is_not_a_string_instance(self):
        """testing if a TypeError will be raised when the dependency_target
        attribute is not a string
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            tdep.dependency_target = 0

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.dependency_target should be a string with a value "
            "one of ['onend', 'onstart'], not int"
        )

    def test_dependency_target_argument_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the dependency_target
        argument value is not one of ['duration', 'length']
        """
        from stalker import TaskDependency
        self.kwargs['dependency_target'] = 'not in the list'
        with self.assertRaises(ValueError) as cm:
            TaskDependency(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.dependency_target should be one of ['onend', "
            "'onstart'], not 'not in the list'"
        )

    def test_dependency_target_attribute_value_is_not_in_the_enum_list(self):
        """testing if a ValueError will be raised when the dependency_target
        attribute value is not one of ['duration', 'length']
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        with self.assertRaises(ValueError) as cm:
            tdep.dependency_target = 'not in the list'

        self.assertEqual(
            str(cm.exception),
            "TaskDependency.dependency_target should be one of ['onend', "
            "'onstart'], not 'not in the list'"
        )

    def test_dependency_target_argument_is_working_properly(self):
        """testing if the dependency_target argument value is correctly passed
        to the dependency_target attribute on init
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        self.assertEqual(tdep.dependency_target, 'onend')

    def test_dependency_target_attribute_is_working_properly(self):
        """testing if the dependency_target attribute is working properly
        """
        from stalker import TaskDependency
        tdep = TaskDependency(**self.kwargs)
        onstart = 'onstart'
        tdep.dependency_target = onstart
        self.assertEqual(onstart, tdep.dependency_target)
