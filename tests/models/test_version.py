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
from stalker.db.session import DBSession
from stalker import (db, config, Link, Project, Repository, Asset, Sequence,
                     Shot, Status, StatusList, Task, Type, Version, Structure,
                     FilenameTemplate)
from stalker.exceptions import CircularDependencyError

defaults = config.Config()

import logging
from stalker import log

logger = logging.getLogger('stalker.models.version.Version')
logger.setLevel(log.logging_level)


class VersionTester(unittest.TestCase):
    """tests stalker.models.version.Version class
    """

    @classmethod
    def setUpClass(cls):
        """setting up the test in class level
        """
        DBSession.remove()

    @classmethod
    def tearDownClass(cls):
        """clean up the test in class level
        """
        DBSession.remove()

    def setUp(self):
        """setup the test
        """
        DBSession.remove()
        db.setup()

        # statuses
        self.test_status1 = Status(name='Status1', code='STS1')
        self.test_status2 = Status(name='Status2', code='STS2')
        self.test_status3 = Status(name='Status3', code='STS3')
        self.test_status4 = Status(name='Status4', code='STS4')
        self.test_status5 = Status(name='Status5', code='STS5')

        # status lists
        self.test_project_status_list = StatusList(
            name='Project Status List',
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Project,
        )

        self.test_sequence_status_list = StatusList(
            name='Sequence Status List',
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Sequence,
        )

        self.test_shot_status_list = StatusList(
            name='Shot Status List',
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Shot,
        )

        self.test_task_status_list = StatusList(
            name='Task Status List',
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Task,
        )

        self.test_version_status_list = StatusList(
            name='Version Status List',
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Version,
        )

        # repository
        self.test_repo = Repository(
            name='Test Repository',
            linux_path='/mnt/T/',
            windows_path='T:/',
            osx_path='/Volumes/T/'
        )

        # a project type
        self.test_project_type = Type(
            name='Test',
            code='test',
            target_entity_type=Project,
        )

        # create a structure
        self.test_structure = Structure(
            name='Test Project Structure'
        )

        # create a project
        self.test_project = Project(
            name='Test Project',
            code='tp',
            type=self.test_project_type,
            status_list=self.test_project_status_list,
            repositories=[self.test_repo],
            structure=self.test_structure
        )

        # create a sequence
        self.test_sequence = Sequence(
            name='Test Sequence',
            code='SEQ1',
            project=self.test_project,
            status_list=self.test_sequence_status_list,
        )

        # create a shot
        self.test_shot1 = Shot(
            name='SH001',
            code='SH001',
            project=self.test_project,
            sequences=[self.test_sequence],
            status_list=self.test_shot_status_list,
        )

        # create a group of Tasks for the shot
        self.test_task1 = Task(
            name='Task1',
            parent=self.test_shot1,
            status_list=self.test_task_status_list,
        )

        # a Link for the input file
        self.test_input_link1 = Link(
            name='Input Link 1',
            full_path='/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/'
                      'Outputs/SH001_beauty_v001.###.exr'
        )

        self.test_input_link2 = Link(
            name='Input Link 2',
            full_path='/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/'
                      'Outputs/SH001_occ_v001.###.exr'
        )

        # a Link for the output file
        self.test_output_link1 = Link(
            name='Output Link 1',
            full_path='/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/'
                      'Outputs/SH001_beauty_v001.###.exr'
        )

        self.test_output_link2 = Link(
            name='Output Link 2',
            full_path='/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/'
                      'Outputs/SH001_occ_v001.###.exr'
        )

        # now create a version for the Task
        self.kwargs = {
            'take_name': 'TestTake',
            'inputs': [self.test_input_link1,
                       self.test_input_link2],
            'outputs': [self.test_output_link1,
                        self.test_output_link2],
            'task': self.test_task1,
            'status_list': self.test_version_status_list,
            'created_with': 'Houdini'
        }

        self.take_name_test_values = [
            ('Take Name', 'Take_Name'),
            ('TakeName', 'TakeName'),
            ('take name', 'take_name'),
            ('  take_name', 'take_name'),
            ('take_name   ', 'take_name'),
            ('   take   name   ', 'take_name'),
            ('TakeName', 'TakeName'),
            ('Take___Name', 'Take___Name'),
            ('Take@Name', 'Take@Name'),
        ]

        # and the Version
        self.test_version = Version(**self.kwargs)

        # set the published to False
        self.test_version.is_published = False

    def tearDown(self):
        """clean up test
        """
        DBSession.remove()

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for
        Version class
        """
        self.assertTrue(Version.__auto_name__)

    def test_take_name_argument_is_skipped_defaults_to_default_value(self):
        """testing if the take_name argument is skipped the take attribute is
        going to be set to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE_NAME
        """
        self.kwargs.pop('take_name')
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.take_name,
                         defaults.version_take_name)

    def test_take_name_argument_is_None(self):
        """testing if a TypeError will be raised when the take_name argument is
        None
        """
        self.kwargs['take_name'] = None
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_take_name_attribute_is_None(self):
        """testing if a TypeError will be raised when the take_name attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_version, 'take_name',
                          None)

    def test_take_name_argument_is_empty_string(self):
        """testing if a ValueError will be raised when the take_name argument
        is given as an empty string
        """
        self.kwargs['take_name'] = ''
        self.assertRaises(ValueError, Version, **self.kwargs)

    def test_take_name_attribute_is_empty_string(self):
        """testing if a ValueError will be raised when the take_name attribute
        is set to an empty string
        """
        self.assertRaises(ValueError, setattr, self.test_version, 'take_name',
                          '')

    def test_take_name_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the given take_name
        argument is not a string
        """
        test_values = [1, 1.2, ['a list'], {'a': 'dict'}]

        for test_value in test_values:
            self.kwargs['take_name'] = test_value
            with self.assertRaises(TypeError):
                Version(**self.kwargs)

    def test_take_name_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when take_name attribute is
        set to a value other than a string
        """
        test_values = [1, 1.2, ['a list'], {'a': 'dict'}]

        for test_value in test_values:
            with self.assertRaises(TypeError):
                self.test_version.take_name = test_value

    def test_take_name_argument_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take_name argument
        string is formatted to an empty string
        """
        self.kwargs['take_name'] = '##$½#$'
        self.assertRaises(ValueError, Version, **self.kwargs)

    def test_take_name_attribute_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take_name argument
        string is formatted to an empty string
        """
        self.assertRaises(ValueError, setattr, self.test_version, 'take_name',
                          '##$½#$')

    def test_take_name_argument_is_formatted_correctly(self):
        """testing if the take_name argument value is formatted correctly
        """
        for test_value in self.take_name_test_values:
            self.kwargs['take_name'] = test_value[0]
            new_version = Version(**self.kwargs)
            self.assertEqual(
                new_version.take_name,
                test_value[1]
            )

    def test_take_name_attribute_is_formatted_correctly(self):
        """testing if the take_name attribute value is formatted correctly
        """
        for test_value in self.take_name_test_values:
            self.test_version.take_name = test_value[0]
            self.assertEqual(
                self.test_version.take_name,
                test_value[1]
            )

    def test_task_argument_is_skipped(self):
        """testing if a TypeError will be raised when the task argument
        is skipped
        """
        self.kwargs.pop('task')
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_task_argument_is_None(self):
        """testing if a TypeError will be raised when the task argument
        is None
        """
        self.kwargs['task'] = None
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_task_attribute_is_None(self):
        """testing if a TypeError will be raised when the task attribute
        is None
        """
        self.assertRaises(TypeError, setattr, self.test_version,
                          'task', None)

    def test_task_argument_is_not_a_Task(self):
        """testing if a TypeError will be raised when the task argument
        is not a Task instance
        """
        self.kwargs['task'] = 'a task'
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_task_attribute_is_not_a_Task(self):
        """testing if a TypeError will be raised when the task attribute
        is not a Task instance
        """
        self.assertRaises(TypeError, setattr, self.test_version, 'task',
                          'a task')

    def test_task_attribute_is_working_properly(self):
        """testing if the task attribute is working properly
        """
        new_task = Task(
            name='New Test Task',
            parent=self.test_shot1,
            status_list=self.test_task_status_list,
        )

        self.assertTrue(self.test_version.task is not new_task)
        self.test_version.task = new_task
        self.assertTrue(self.test_version.task is new_task)

    def test_version_number_attribute_is_automatically_generated(self):
        """testing if the version_number attribute is automatically generated
        """
        self.assertEqual(self.test_version.version_number, 1)
        DBSession.add(self.test_version)
        DBSession.commit()

        new_version = Version(**self.kwargs)
        DBSession.add(new_version)
        DBSession.commit()

        self.assertEqual(self.test_version.task, new_version.task)
        self.assertEqual(self.test_version.take_name, new_version.take_name)

        self.assertEqual(new_version.version_number, 2)

        new_version = Version(**self.kwargs)
        DBSession.add(new_version)
        DBSession.commit()

        self.assertEqual(self.test_version.task, new_version.task)
        self.assertEqual(self.test_version.take_name, new_version.take_name)

        self.assertEqual(new_version.version_number, 3)

        new_version = Version(**self.kwargs)
        DBSession.add(new_version)
        DBSession.commit()

        self.assertEqual(self.test_version.task, new_version.task)
        self.assertEqual(self.test_version.take_name, new_version.take_name)

        self.assertEqual(new_version.version_number, 4)

    def test_version_number_attribute_is_starting_from_1(self):
        """testing if the version_number attribute is starting from 1
        """
        self.assertEqual(self.test_version.version_number, 1)

    def test_version_number_attribute_is_set_to_a_lower_then_it_should_be(self):
        """testing if the version_number attribute will be set to a correct
        unique value when it is set to a lower number then it should be
        """
        self.test_version.version_number = -1
        self.assertEqual(self.test_version.version_number, 1)

        self.test_version.version_number = -10
        self.assertEqual(self.test_version.version_number, 1)

        DBSession.add(self.test_version)
        DBSession.commit()

        self.test_version.version_number = -100
        # it should be 1 again
        self.assertEqual(self.test_version.version_number, 1)

        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.version_number, 2)

        new_version.version_number = 1
        self.assertEqual(new_version.version_number, 2)

        new_version.version_number = 100
        self.assertEqual(new_version.version_number, 100)

    def test_inputs_argument_is_skipped(self):
        """testing if the inputs attribute will be an empty list when the
        inputs argument is skipped
        """
        self.kwargs.pop('inputs')
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.inputs, [])

    def test_inputs_argument_is_None(self):
        """testing if the inputs attribute will be an empty list when the
        inputs argument is None
        """
        self.kwargs['inputs'] = None
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.inputs, [])

    def test_inputs_attribute_is_None(self):
        """testing if a TypeError will be raised when the inputs argument is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_version, 'inputs',
                          None)

    def test_inputs_argument_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the inputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, '231123']
        self.kwargs['inputs'] = test_value
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_inputs_attribute_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the inputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, '231123']
        self.assertRaises(TypeError, setattr, self.test_version, 'inputs',
                          test_value)

    def test_inputs_attribute_is_working_properly(self):
        """testing if the inputs attribute is working properly
        """
        self.kwargs.pop('inputs')
        new_version = Version(**self.kwargs)

        self.assertFalse(self.test_input_link1 in new_version.inputs)
        self.assertFalse(self.test_input_link2 in new_version.inputs)

        new_version.inputs = [self.test_input_link1, self.test_input_link2]

        self.assertTrue(self.test_input_link1 in new_version.inputs)
        self.assertTrue(self.test_input_link2 in new_version.inputs)

    def test_outputs_argument_is_skipped(self):
        """testing if the outputs attribute will be an empty list when the
        outputs argument is skipped
        """
        self.kwargs.pop('outputs')
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.outputs, [])

    def test_outputs_argument_is_None(self):
        """testing if the outputs attribute will be an empty list when the
        outputs argument is None
        """
        self.kwargs['outputs'] = None
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.outputs, [])

    def test_outputs_attribute_is_None(self):
        """testing if a TypeError will be raised when the outputs argument is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_version, 'outputs',
                          None)

    def test_outputs_argument_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the outputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, '231123']
        self.kwargs['outputs'] = test_value
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_outputs_attribute_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the outputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, '231123']
        self.assertRaises(TypeError, setattr, self.test_version, 'outputs',
                          test_value)

    def test_outputs_attribute_is_working_properly(self):
        """testing if the outputs attribute is working properly
        """
        self.kwargs.pop('outputs')
        new_version = Version(**self.kwargs)

        self.assertFalse(self.test_output_link1 in new_version.outputs)
        self.assertFalse(self.test_output_link2 in new_version.outputs)

        new_version.outputs = [self.test_output_link1, self.test_output_link2]

        self.assertTrue(self.test_output_link1 in new_version.outputs)
        self.assertTrue(self.test_output_link2 in new_version.outputs)

    def test_is_published_attribute_is_False_by_default(self):
        """testing if the is_published attribute is False by default
        """
        self.assertEqual(self.test_version.is_published, False)

    def test_is_published_attribute_is_working_properly(self):
        """testing if the is_published attribute is working properly
        """
        self.test_version.is_published = True
        self.assertEqual(self.test_version.is_published, True)

        self.test_version.is_published = False
        self.assertEqual(self.test_version.is_published, False)

    def test_parent_argument_is_skipped(self):
        """testing if the parent attribute will be None if the parent argument
        is skipped
        """
        try:
            self.kwargs.pop('parent')
        except KeyError:
            pass
        new_version = Version(**self.kwargs)
        self.assertTrue(new_version.parent is None)

    def test_parent_argument_is_None(self):
        """testing if the parent attribute will be None if the parent argument
        is skipped
        """
        self.kwargs['parent'] = None
        new_version = Version(**self.kwargs)
        self.assertTrue(new_version.parent is None)

    def test_parent_attribute_is_None(self):
        """testing if the parent attribute value will be None if it is set to
        None
        """
        self.test_version.parent = None
        self.assertTrue(self.test_version.parent is None)

    def test_parent_argument_is_not_a_Version_instance(self):
        """testing if a TypeError will be raised when the parent argument is
        not a Version instance
        """
        self.kwargs['parent'] = 'not a version instance'
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_parent_attribute_is_not_set_to_a_Version_instance(self):
        """testing if a TypeError will be raised when the parent attribute is
        not set to a Version instance
        """
        self.assertRaises(TypeError, setattr, self.test_version, 'parent',
                          'not a version instance')

    def test_parent_argument_is_working_properly(self):
        """testing if the parent argument is working properly
        """
        self.kwargs['parent'] = self.test_version
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.parent, self.test_version)

    def test_parent_attribute_is_working_properly(self):
        """testing if the parent attribute is working properly
        """
        self.kwargs['parent'] = None
        new_version = Version(**self.kwargs)
        self.assertNotEqual(new_version.parent, self.test_version)
        new_version.parent = self.test_version
        self.assertEqual(new_version.parent, self.test_version)

    def test_parent_argument_updates_the_children_attribute(self):
        """testing if the parent argument updates the children attribute of the
        parent Version properly
        """
        self.kwargs['parent'] = self.test_version
        new_version = Version(**self.kwargs)
        self.assertTrue(new_version in self.test_version.children)

    def test_parent_attribute_updates_the_children_attribute(self):
        """testing if the parent attribute updates the children attribute of
        the parent Version properly
        """
        self.kwargs['parent'] = None
        new_version = Version(**self.kwargs)
        self.assertNotEqual(new_version.parent, self.test_version)
        new_version.parent = self.test_version
        self.assertTrue(new_version in self.test_version.children)

    def test_parent_attribute_will_not_allow_circular_dependencies(self):
        """testing if a CircularDependency will be raised when the given
        Version to the parent attribute is a children of the current Version
        """
        self.kwargs['parent'] = self.test_version
        version1 = Version(**self.kwargs)
        self.assertRaises(CircularDependencyError, setattr, self.test_version,
                          'parent', version1)

    def test_parent_attribute_will_not_allow_deeper_circular_dependencies(self):
        """testing if a CircularDependency will be raised when the given
        Version is a parent of the current parent
        """
        self.kwargs['parent'] = self.test_version
        version1 = Version(**self.kwargs)

        self.kwargs['parent'] = version1
        version2 = Version(**self.kwargs)

        # now create circular dependency
        self.assertRaises(CircularDependencyError, setattr, self.test_version,
                          'parent', version2)

    def test_children_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the children attribute is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_version, 'children',
                          None)

    def test_children_attribute_is_not_set_to_a_list(self):
        """testing if a TypeError will be raised when the children attribute is
        not set to a list
        """
        self.assertRaises(TypeError, setattr, self.test_version, 'children',
                          'not a list of Version instances')

    def test_children_attribute_is_not_set_to_a_list_of_Version_instances(self):
        """testing if a TypeError will be raised when the children attribute is
        not set to a list of Version instances
        """
        self.assertRaises(TypeError, setattr, self.test_version, 'children',
                          ['not a Version instance', 3])

    def test_children_attribute_is_working_properly(self):
        """testing if the children attribute is working properly
        """
        self.kwargs['parent'] = None
        new_version1 = Version(**self.kwargs)
        self.test_version.children = [new_version1]
        self.assertTrue(new_version1 in self.test_version.children)

        new_version2 = Version(**self.kwargs)
        self.test_version.children.append(new_version2)
        self.assertTrue(new_version2 in self.test_version.children)

    def test_children_attribute_updates_parent_attribute(self):
        """testing if the children attribute updates the parent attribute of
        the children Versions
        """
        self.kwargs['parent'] = None
        new_version1 = Version(**self.kwargs)
        self.test_version.children = [new_version1]
        self.assertEqual(new_version1.parent, self.test_version)

        new_version2 = Version(**self.kwargs)
        self.test_version.children.append(new_version2)
        self.assertEqual(new_version2.parent, self.test_version)

    def test_children_attribute_will_not_allow_circular_dependencies(self):
        """testing if a CircularDependency error will be raised when a parent
        Version is set as a children to its child
        """
        self.kwargs['parent'] = None
        new_version1 = Version(**self.kwargs)
        new_version2 = Version(**self.kwargs)

        new_version1.parent = new_version2
        self.assertRaises(CircularDependencyError,
                          new_version1.children.append, new_version2)

    def test_children_attribute_will_not_allow_deeper_circular_dependencies(self):
        """testing if a CircularDependency error will be raised when the a
        parent Version of a parent Version is set as a children to its grand
        child
        """
        self.kwargs['parent'] = None
        new_version1 = Version(**self.kwargs)
        new_version2 = Version(**self.kwargs)
        new_version3 = Version(**self.kwargs)

        new_version1.parent = new_version2
        new_version2.parent = new_version3

        self.assertRaises(CircularDependencyError,
                          new_version1.children.append, new_version3)

    def test_update_paths_will_render_the_appropriate_template_from_the_related_project(self):
        """testing if update_paths method will update the Version.full_path by
        rendering the related Project FilenameTemplate.
        """
        # create a FilenameTemplate for Task instances

        # A Template for Assets
        # ......../Assets/{{asset.type.name}}/{{asset.nice_name}}/{{task.type.name}}/
        # 
        # Project1/Assets/Character/Sero/Modeling/Sero_Modeling_Main_v001.ma
        #
        # + Project1
        # |
        # +-+ Assets (Task)
        # | |
        # | +-+ Characters
        # |   |
        # |   +-+ Sero (Asset)
        # |     |
        # |     +-> Version 1
        # |     |
        # |     +-+ Modeling (Task)
        # |       |
        # |       +-+ Body Modeling (Task)
        # |         |
        # |         +-+ Coarse Modeling (Task)
        # |         | |
        # |         | +-> Version 1 (Version)
        # |         |
        # |         +-+ Fine Modeling (Task)
        # |           |
        # |           +-> Version 1 (Version): Fine_Modeling_Main_v001.ma
        # |                                  Assets/Characters/Sero/Modeling/Body_Modeling/Fine_Modeling/Fine_Modeling_Main_v001.ma
        # |
        # +-+ Shots (Task)
        #   |
        #   +-+ Shot 10 (Shot)
        #   | |
        #   | +-+ Layout (Task)
        #   |   |
        #   |   +-> Version 1 (Version): Layout_v001.ma
        #   |                            Shots/Shot_1/Layout/Layout_Main_v001.ma
        #   |
        #   +-+ Shot 2 (Shot)
        #     |
        #     +-+ FX (Task)
        #       |
        #       +-> Version 1 (Version)

        ft = FilenameTemplate(
            name='Task Filename Template',
            target_entity_type='Task',
            path='{{project.code}}/{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/{%- endfor -%}',
            filename='{{task.nice_name}}_{{version.take_name}}'
                     '_v{{"%03d"|format(version.version_number)}}{{extension}}'
        )
        self.test_project.structure.templates.append(ft)
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()
        new_version1.update_paths()

        self.assertEqual(
            new_version1.path,
            'tp/SH001/Task1'
        )

        new_version1.extension = '.ma'
        self.assertEqual(
            new_version1.filename,
            'Task1_TestTake_v001.ma'
        )

    def test_update_paths_will_preserve_extension(self):
        """testing if update_paths method will preserve the extension.
        """
        # create a FilenameTemplate for Task instances
        ft = FilenameTemplate(
            name='Task Filename Template',
            target_entity_type='Task',
            path='{{project.code}}/{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/{%- endfor -%}',
            filename='{{task.nice_name}}_{{version.take_name}}'
                     '_v{{"%03d"|format(version.version_number)}}{{extension}}'
        )
        self.test_project.structure.templates.append(ft)
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()
        new_version1.update_paths()

        self.assertEqual(
            new_version1.path,
            'tp/SH001/Task1'
        )

        extension = '.ma'
        new_version1.extension = extension
        self.assertEqual(
            new_version1.filename,
            'Task1_TestTake_v001.ma'
        )

        # rename the task and update the paths
        self.test_task1.name = 'Task2'

        # now call update_paths and expect the extension to be preserved
        new_version1.update_paths()
        self.assertEqual(
            new_version1.filename,
            'Task2_TestTake_v001.ma'
        )
        self.assertEqual(new_version1.extension, extension)

    def test_update_paths_will_raise_a_RuntimeError_if_there_is_no_suitable_FilenameTemplate(self):
        """testing if update_paths method will raise a RuntimeError if there is
        no suitable FilenameTemplate instance found
        """
        self.kwargs['parent'] = None
        new_version1 = Version(**self.kwargs)
        self.assertRaises(RuntimeError, new_version1.update_paths)

    def test_template_variables_project(self):
        """testing if the project in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        self.assertEqual(
            kwargs['project'],
            self.test_version.task.project
        )

    def test_template_variables_sequences(self):
        """testing if the sequences in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        self.assertEqual(
            kwargs['sequences'],
            []
        )

    def test_template_variables_scenes(self):
        """testing if the scenes in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        self.assertEqual(
            kwargs['scenes'],
            []
        )

    def test_template_variables_shot(self):
        """testing if the shot in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        self.assertEqual(
            kwargs['shot'],
            self.test_version.task
        )

    def test_template_variables_asset(self):
        """testing if the asset in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        self.assertEqual(
            kwargs['asset'],
            self.test_version.task
        )

    def test_template_variables_task(self):
        """testing if the task in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        self.assertEqual(
            kwargs['task'],
            self.test_version.task
        )

    def test_template_variables_parent_tasks(self):
        """testing if the parent_tasks in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        parents = self.test_version.task.parents
        parents.append(self.test_version.task)
        self.assertEqual(
            kwargs['parent_tasks'],
            parents
        )

    def test_template_variables_version(self):
        """testing if the version in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        self.assertEqual(
            kwargs['version'],
            self.test_version
        )

    def test_template_variables_type(self):
        """testing if the type in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        self.assertEqual(
            kwargs['type'],
            self.test_version.type
        )

    def test_absolute_full_path_works_properly(self):
        """testing if the absolute_full_path attribute works properly
        """
        ft = FilenameTemplate(
            name='Task Filename Template',
            target_entity_type='Task',
            path='{{project.repositories[0].path}}/{{project.code}}/'
                 '{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/'
                 '{%- endfor -%}',
            filename='{{task.nice_name}}_{{version.take_name}}'
                     '_v{{"%03d"|format(version.version_number)}}{{extension}}'
        )
        self.test_project.structure.templates.append(ft)
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()

        new_version1.take_name = 'TestTake@BBOX'

        new_version1.update_paths()
        new_version1.extension = '.ma'
        self.assertEqual(new_version1.extension, '.ma')

        self.assertEqual(
            new_version1.absolute_full_path,
            '/mnt/T/tp/SH001/Task1/Task1_TestTake@BBOX_v001.ma'
        )

    def test_latest_published_version_is_read_only(self):
        """testing if the latest_published_version is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_version,
                          'latest_published_version', True)

    def test_latest_published_version_is_working_properly(self):
        """testing if the is_latest_published_version is working properly
        """
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()

        new_version2 = Version(**self.kwargs)
        DBSession.add(new_version2)
        DBSession.commit()

        new_version3 = Version(**self.kwargs)
        DBSession.add(new_version3)
        DBSession.commit()

        new_version4 = Version(**self.kwargs)
        DBSession.add(new_version4)
        DBSession.commit()

        new_version5 = Version(**self.kwargs)
        DBSession.add(new_version5)
        DBSession.commit()

        new_version1.is_published = True
        new_version3.is_published = True
        new_version4.is_published = True

        self.assertEqual(new_version1.latest_published_version, new_version4)
        self.assertEqual(new_version2.latest_published_version, new_version4)
        self.assertEqual(new_version3.latest_published_version, new_version4)
        self.assertEqual(new_version4.latest_published_version, new_version4)
        self.assertEqual(new_version5.latest_published_version, new_version4)

    def test_is_latest_published_version_is_working_properly(self):
        """testing if the is_latest_published_version is working properly
        """
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()

        new_version2 = Version(**self.kwargs)
        DBSession.add(new_version2)
        DBSession.commit()

        new_version3 = Version(**self.kwargs)
        DBSession.add(new_version3)
        DBSession.commit()

        new_version4 = Version(**self.kwargs)
        DBSession.add(new_version4)
        DBSession.commit()

        new_version5 = Version(**self.kwargs)
        DBSession.add(new_version5)
        DBSession.commit()

        new_version1.is_published = True
        new_version3.is_published = True
        new_version4.is_published = True

        self.assertFalse(new_version1.is_latest_published_version())
        self.assertFalse(new_version2.is_latest_published_version())
        self.assertFalse(new_version3.is_latest_published_version())
        self.assertTrue(new_version4.is_latest_published_version())
        self.assertFalse(new_version5.is_latest_published_version())

    def test_equality_operator(self):
        """testing equality of two Version instances
        """
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()

        new_version2 = Version(**self.kwargs)
        DBSession.add(new_version2)
        DBSession.commit()

        new_version3 = Version(**self.kwargs)
        DBSession.add(new_version3)
        DBSession.commit()

        new_version4 = Version(**self.kwargs)
        DBSession.add(new_version4)
        DBSession.commit()

        new_version5 = Version(**self.kwargs)
        DBSession.add(new_version5)
        DBSession.commit()

        new_version1.is_published = True
        new_version3.is_published = True
        new_version4.is_published = True

        self.assertFalse(new_version1 == new_version2)
        self.assertFalse(new_version1 == new_version3)
        self.assertFalse(new_version1 == new_version4)
        self.assertFalse(new_version1 == new_version5)

        self.assertFalse(new_version2 == new_version3)
        self.assertFalse(new_version2 == new_version4)
        self.assertFalse(new_version2 == new_version5)

        self.assertFalse(new_version3 == new_version4)
        self.assertFalse(new_version3 == new_version5)

        self.assertFalse(new_version4 == new_version5)

    def test_inequality_operator(self):
        """testing inequality of two Version instances
        """
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()

        new_version2 = Version(**self.kwargs)
        DBSession.add(new_version2)
        DBSession.commit()

        new_version3 = Version(**self.kwargs)
        DBSession.add(new_version3)
        DBSession.commit()

        new_version4 = Version(**self.kwargs)
        DBSession.add(new_version4)
        DBSession.commit()

        new_version5 = Version(**self.kwargs)
        DBSession.add(new_version5)
        DBSession.commit()

        new_version1.is_published = True
        new_version3.is_published = True
        new_version4.is_published = True

        self.assertTrue(new_version1 != new_version2)
        self.assertTrue(new_version1 != new_version3)
        self.assertTrue(new_version1 != new_version4)
        self.assertTrue(new_version1 != new_version5)

        self.assertTrue(new_version2 != new_version3)
        self.assertTrue(new_version2 != new_version4)
        self.assertTrue(new_version2 != new_version5)

        self.assertTrue(new_version3 != new_version4)
        self.assertTrue(new_version3 != new_version5)

        self.assertTrue(new_version4 != new_version5)

    def test_created_with_argument_can_be_skipped(self):
        """testing if the created_with argument can be skipped
        """
        self.kwargs.pop('created_with')
        Version(**self.kwargs)

    def test_created_with_argument_can_be_None(self):
        """testing if the created_with argument can be None
        """
        self.kwargs['created_with'] = None
        Version(**self.kwargs)

    def test_created_with_attribute_can_be_set_to_None(self):
        """testing if the created with attribute can be set to None
        """
        self.test_version.created_with = None

    def test_created_with_argument_accepts_only_string_or_None(self):
        """testing if a TypeError will be raised if the created_with argument
        is something other than a string or None
        """
        self.kwargs['created_with'] = 234
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_created_with_attribute_accepts_only_string_or_None(self):
        """testing if a TypeError will be raised if the created_with attribute
        is set to a value other than a string or None
        """
        self.assertRaises(TypeError, setattr, self.test_version,
                          'created_with', 234)

    def test_created_with_argument_is_working_properly(self):
        """testing if the created_with argument value is passed to created_with
        attribute properly
        """
        test_value = 'Maya'
        self.kwargs['created_with'] = test_value
        test_version = Version(**self.kwargs)
        self.assertEqual(test_version.created_with, test_value)

    def test_created_with_attribute_is_working_properly(self):
        """testing if created_with attribute is working properly
        """
        test_value = 'Maya'
        self.assertNotEqual(self.test_version.created_with, test_value)
        self.test_version.created_with = test_value
        self.assertEqual(self.test_version.created_with, test_value)

    def test_max_version_number_attribute_is_read_only(self):
        """testing if the max_version_number attribute is read only
        """
        self.assertRaises(AttributeError, setattr, self.test_version,
                          'max_version_number', 20)

    def test_max_version_number_attribute_is_working_properly(self):
        """testing if the max_version_number attribute is working properly
        """
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()

        new_version2 = Version(**self.kwargs)
        DBSession.add(new_version2)
        DBSession.commit()

        new_version3 = Version(**self.kwargs)
        DBSession.add(new_version3)
        DBSession.commit()

        new_version4 = Version(**self.kwargs)
        DBSession.add(new_version4)
        DBSession.commit()

        new_version5 = Version(**self.kwargs)
        DBSession.add(new_version5)
        DBSession.commit()

        self.assertEqual(new_version5.version_number, 5)

        self.assertEqual(new_version1.max_version_number, 5)
        self.assertEqual(new_version2.max_version_number, 5)
        self.assertEqual(new_version3.max_version_number, 5)
        self.assertEqual(new_version4.max_version_number, 5)
        self.assertEqual(new_version5.max_version_number, 5)

    def test_latest_version_attribute_is_read_only(self):
        """testing if the last_version attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_version,
                          'latest_version', 3453)

    def test_latest_version_attribute_is_working_properly(self):
        """testing if the last_version attribute is working properly
        """
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()

        new_version2 = Version(**self.kwargs)
        DBSession.add(new_version2)
        DBSession.commit()

        new_version3 = Version(**self.kwargs)
        DBSession.add(new_version3)
        DBSession.commit()

        new_version4 = Version(**self.kwargs)
        DBSession.add(new_version4)
        DBSession.commit()

        new_version5 = Version(**self.kwargs)
        DBSession.add(new_version5)
        DBSession.commit()

        self.assertEqual(new_version5.version_number, 5)

        self.assertEqual(new_version1.latest_version, new_version5)
        self.assertEqual(new_version2.latest_version, new_version5)
        self.assertEqual(new_version3.latest_version, new_version5)
        self.assertEqual(new_version4.latest_version, new_version5)
        self.assertEqual(new_version5.latest_version, new_version5)

    def test_naming_parents_attribute_is_a_read_only_property(self):
        """testing if the naming_parents attribute is a read only property
        """
        self.assertRaises(AttributeError, setattr, self.test_version,
                          'naming_parents', [self.test_task1])

    def test_naming_parents_attribute_is_working_properly(self):
        """testing if the naming_parents attribute is working properly
        """
        # for self.test_version
        self.assertEqual(
            self.test_version.naming_parents,
            [self.test_shot1, self.test_task1]
        )

        # for a new version of a task
        task1 = Task(
            name='Test Task 1',
            project=self.test_project,
            status_list=self.test_task_status_list
        )

        task2 = Task(
            name='Test Task 2',
            parent=task1,
            status_list=self.test_task_status_list
        )

        task3 = Task(
            name='Test Task 3',
            parent=task2,
            status_list=self.test_task_status_list
        )
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        version1 = Version(
            task=task3
        )
        DBSession.add(version1)
        DBSession.commit()

        self.assertEqual(
            version1.naming_parents,
            [task1, task2, task3]
        )

        # for a an asset version
        asset_statuses = StatusList(
            target_entity_type='Asset',
            statuses=[self.test_status1, self.test_status2, self.test_status3]
        )
        character_type = Type(
            target_entity_type='Asset',
            name='Character',
            code='Char'
        )
        asset1 = Asset(
            name='Asset1',
            code='Asset1',
            parent=task1,
            status_list=asset_statuses,
            type=character_type
        )
        version2 = Version(
            task=asset1
        )
        self.assertEqual(
            version2.naming_parents,
            [asset1]
        )

        # for a version of a task of a shot
        shot2 = Shot(
            name='SH002',
            code='SH002',
            parent=task3,
            status_list=self.test_shot_status_list
        )

        task4 = Task(
            name='Test Task 4',
            parent=shot2,
            status_list=self.test_task_status_list
        )

        version3 = Version(
            task=task4
        )

        self.assertEqual(
            version3.naming_parents,
            [shot2, task4]
        )

        # for an asset of a shot
        asset2 = Asset(
            name='Asset2',
            code='Asset2',
            parent=shot2,
            status_list=asset_statuses,
            type=character_type
        )
        version4 = Version(task=asset2)
        self.assertEqual(version4.naming_parents, [asset2])

    def test_nice_name_attribute_is_working_properly(self):
        """testing if the nice_name attribute is working properly
        """
        # for self.test_version
        self.assertEqual(
            self.test_version.naming_parents,
            [self.test_shot1, self.test_task1]
        )

        # for a new version of a task
        task1 = Task(
            name='Test Task 1',
            project=self.test_project,
            status_list=self.test_task_status_list
        )

        task2 = Task(
            name='Test Task 2',
            parent=task1,
            status_list=self.test_task_status_list
        )

        task3 = Task(
            name='Test Task 3',
            parent=task2,
            status_list=self.test_task_status_list
        )
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        version1 = Version(
            task=task3,
            take_name='Take1@Main'
        )
        DBSession.add(version1)
        DBSession.commit()

        self.assertEqual(
            version1.nice_name,
            '%s_%s_%s_%s' % (
                task1.nice_name, task2.nice_name, task3.nice_name,
                version1.take_name
            )
        )

        # for a an asset version
        asset_statuses = StatusList(
            target_entity_type='Asset',
            statuses=[self.test_status1, self.test_status2, self.test_status3]
        )
        character_type = Type(
            target_entity_type='Asset',
            name='Character',
            code='Char'
        )
        asset1 = Asset(
            name='Asset1',
            code='Asset1',
            parent=task1,
            status_list=asset_statuses,
            type=character_type
        )
        version2 = Version(
            task=asset1
        )
        self.assertEqual(
            version2.nice_name,
            '%s_%s' % (asset1.nice_name, version2.take_name)
        )

        # for a version of a task of a shot
        shot2 = Shot(
            name='SH002',
            code='SH002',
            parent=task3,
            status_list=self.test_shot_status_list
        )

        task4 = Task(
            name='Test Task 4',
            parent=shot2,
            status_list=self.test_task_status_list
        )

        version3 = Version(
            task=task4
        )

        self.assertEqual(
            version3.nice_name,
            '%s_%s_%s' % (shot2.nice_name, task4.nice_name, version3.take_name)
        )

        # for an asset of a shot
        asset2 = Asset(
            name='Asset2',
            code='Asset2',
            parent=shot2,
            status_list=asset_statuses,
            type=character_type
        )
        version4 = Version(task=asset2)
        self.assertEqual(
            version4.nice_name,
            '%s_%s' % (asset2.nice_name, version4.take_name)
        )

    def test_string_representation_is_a_little_bit_meaningful(self):
        """testing if the __str__ or __repr__ result is meaningfull
        """
        self.assertEqual(
            '<tp_SH001_Task1_TestTake_v001 (Version)>',
            '%s' % self.test_version
        )

    def test_walk_hierarchy_is_working_properly_in_DFS_mode(self):
        """testing if the walk_hierarchy() method is working in DFS mode
        correctly
        """
        v1 = Version(task=self.test_task1)
        v2 = Version(task=self.test_task1, parent=v1)
        v3 = Version(task=self.test_task1, parent=v2)
        v4 = Version(task=self.test_task1, parent=v3)
        v5 = Version(task=self.test_task1, parent=v1)

        expected_result = [v1, v2, v3, v4, v5]
        visited_versions = []
        for v in v1.walk_hierarchy():
            visited_versions.append(v)

        self.assertEqual(expected_result, visited_versions)

    def test_walk_inputs_is_working_properly_in_DFS_mode(self):
        """testing if the walk_inputs() method is working in DFS mode correctly
        """
        v1 = Version(task=self.test_task1)
        v2 = Version(task=self.test_task1)
        v3 = Version(task=self.test_task1)
        v4 = Version(task=self.test_task1)
        v5 = Version(task=self.test_task1)

        v5.inputs = [v4]
        v4.inputs = [v3, v2]
        v3.inputs = [v1]
        v2.inputs = [v1]

        expected_result = [v5, v4, v3, v1, v2, v1]
        visited_versions = []
        for v in v5.walk_inputs():
            visited_versions.append(v)

        self.assertEqual(expected_result, visited_versions)

    # def test_path_attribute_value_is_calculated_on_init(self):
    #     """testing if the path attribute value is automatically calculated on
    #     Version instance initialize
    #     """
    #     ft = FilenameTemplate(
    #         name='Task Filename Template',
    #         target_entity_type='Task',
    #         path='{{project.code}}/{%- for p in parent_tasks -%}'
    #              '{{p.nice_name}}/{%- endfor -%}',
    #         filename='{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}{{extension}}'
    #     )
    #     self.test_project.structure.templates.append(ft)
    #     db.DBSession.add(self.test_project)
    #     db.DBSession.commit()
    # 
    #     print 'entity_type: %s' % self.test_task1.entity_type
    # 
    #     # v1 = Version(task=self.test_task1)
    #     # self.assertEqual(
    #     #     'tp/SH001/task1/task1_Main_v001',
    #     #     v1.path
    #     # )
    #     self.fail()
