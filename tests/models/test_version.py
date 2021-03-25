# -*- coding: utf-8 -*-

import unittest

import pytest

from stalker.testing import UnitTestDBBase, PlatformPatcher

import logging
from stalker import log

logger = logging.getLogger('stalker.models.version.Version')
logger.setLevel(log.logging_level)


class VersionDBTester(UnitTestDBBase):
    """tests stalker.models.version.Version class
    """

    def setUp(self):
        """setup the test
        """
        super(self.__class__, self).setUp()
        self.patcher = PlatformPatcher()

        from stalker import Status, StatusList

        # statuses
        self.test_status1 = Status(name='Status1', code='STS1')
        self.test_status2 = Status(name='Status2', code='STS2')
        self.test_status3 = Status(name='Status3', code='STS3')
        self.test_status4 = Status(name='Status4', code='STS4')
        self.test_status5 = Status(name='Status5', code='STS5')
        from stalker.db.session import DBSession
        DBSession.add_all([
            self.test_status1, self.test_status2, self.test_status3,
            self.test_status4, self.test_status5
        ])
        DBSession.commit()

        # repository
        from stalker import Repository, Type
        self.test_repo = Repository(
            name='Test Repository',
            code='TR',
            linux_path='/mnt/T/',
            windows_path='T:/',
            osx_path='/Volumes/T/'
        )
        DBSession.add(self.test_repo)

        # a project type
        self.test_project_type = Type(
            name='Test',
            code='test',
            target_entity_type='Project',
        )
        DBSession.add(self.test_project_type)

        # create a structure
        from stalker import Structure
        self.test_structure = Structure(
            name='Test Project Structure'
        )
        DBSession.add(self.test_structure)

        # create a project
        from stalker import Project
        self.test_project = Project(
            name='Test Project',
            code='tp',
            type=self.test_project_type,
            repositories=[self.test_repo],
            structure=self.test_structure
        )
        DBSession.add(self.test_project)
        DBSession.commit()

        # create a sequence
        from stalker import Sequence
        self.test_sequence = Sequence(
            name='Test Sequence',
            code='SEQ1',
            project=self.test_project,
        )
        DBSession.add(self.test_sequence)
        DBSession.commit()

        # create a shot
        from stalker import Shot
        self.test_shot1 = Shot(
            name='SH001',
            code='SH001',
            project=self.test_project,
            sequences=[self.test_sequence]
        )
        DBSession.add(self.test_shot1)
        DBSession.commit()

        # create a group of Tasks for the shot
        from stalker import Task
        self.test_task1 = Task(
            name='Task1',
            parent=self.test_shot1
        )
        DBSession.add(self.test_task1)
        DBSession.commit()

        # a Link for the input file
        from stalker import Link
        self.test_input_link1 = Link(
            name='Input Link 1',
            full_path='/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/'
                      'Outputs/SH001_beauty_v001.###.exr'
        )
        DBSession.add(self.test_input_link1)

        self.test_input_link2 = Link(
            name='Input Link 2',
            full_path='/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/'
                      'Outputs/SH001_occ_v001.###.exr'
        )
        DBSession.add(self.test_input_link2)

        # a Link for the output file
        self.test_output_link1 = Link(
            name='Output Link 1',
            full_path='/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/'
                      'Outputs/SH001_beauty_v001.###.exr'
        )
        DBSession.add(self.test_output_link1)

        self.test_output_link2 = Link(
            name='Output Link 2',
            full_path='/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/'
                      'Outputs/SH001_occ_v001.###.exr'
        )
        DBSession.add(self.test_output_link2)
        DBSession.commit()

        # now create a version for the Task
        self.kwargs = {
            'take_name': 'TestTake',
            'inputs': [self.test_input_link1,
                       self.test_input_link2],
            'outputs': [self.test_output_link1,
                        self.test_output_link2],
            'task': self.test_task1,
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
        from stalker import Version
        self.test_version = Version(**self.kwargs)
        DBSession.add(self.test_version)

        # set the published to False
        self.test_version.is_published = False
        DBSession.commit()

    def tearDown(self):
        """clean up test
        """
        self.patcher.restore()
        super(self.__class__, self).tearDown()

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for
        Version class
        """
        from stalker import Version
        assert Version.__auto_name__ is True

    def test_take_name_argument_is_skipped_defaults_to_default_value(self):
        """testing if the take_name argument is skipped the take attribute is
        going to be set to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE_NAME
        """
        from stalker import defaults, Version
        self.kwargs.pop('take_name')
        new_version = Version(**self.kwargs)
        assert new_version.take_name == defaults.version_take_name

    def test_take_name_argument_is_None(self):
        """testing if a TypeError will be raised when the take_name argument is
        None
        """
        from stalker import Version
        self.kwargs['take_name'] = None
        with pytest.raises(TypeError) as cm:
            Version(**self.kwargs)

        assert str(cm.value) == \
            'Version.take_name should be a string, not NoneType'

    def test_take_name_attribute_is_None(self):
        """testing if a TypeError will be raised when the take_name attribute
        is set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.take_name = None

        assert str(cm.value) == \
            'Version.take_name should be a string, not NoneType'

    def test_take_name_argument_is_empty_string(self):
        """testing if a ValueError will be raised when the take_name argument
        is given as an empty string
        """
        from stalker import Version
        self.kwargs['take_name'] = ''
        with pytest.raises(ValueError) as cm:
            Version(**self.kwargs)

        assert str(cm.value) == \
            'Version.take_name can not be an empty string'

    def test_take_name_attribute_is_empty_string(self):
        """testing if a ValueError will be raised when the take_name attribute
        is set to an empty string
        """
        with pytest.raises(ValueError) as cm:
            self.test_version.take_name = ''

        assert str(cm.value) == \
            'Version.take_name can not be an empty string'

    def test_take_name_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the given take_name
        argument is not a string
        """
        from stalker import Version
        test_values = [1, 1.2, ['a list'], {'a': 'dict'}]

        for test_value in test_values:
            self.kwargs['take_name'] = test_value
            with pytest.raises(TypeError):
                Version(**self.kwargs)

    def test_take_name_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when take_name attribute is
        set to a value other than a string
        """
        test_values = [1, 1.2, ['a list'], {'a': 'dict'}]

        for test_value in test_values:
            with pytest.raises(TypeError):
                self.test_version.take_name = test_value

    def test_take_name_argument_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take_name argument
        string is formatted to an empty string
        """
        from stalker import Version
        self.kwargs['take_name'] = '##$½#$'
        with pytest.raises(ValueError) as cm:
            v = Version(**self.kwargs)

        assert str(cm.value) == \
            'Version.take_name can not be an empty string'

    def test_take_name_attribute_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take_name argument
        string is formatted to an empty string
        """
        with pytest.raises(ValueError) as cm:
            self.test_version.take_name = '##$½#$'

        assert str(cm.value) == \
            'Version.take_name can not be an empty string'

    def test_take_name_argument_is_formatted_correctly(self):
        """testing if the take_name argument value is formatted correctly
        """
        from stalker import Version
        for test_value in self.take_name_test_values:
            self.kwargs['take_name'] = test_value[0]
            new_version = Version(**self.kwargs)
            assert new_version.take_name == test_value[1]

    def test_take_name_attribute_is_formatted_correctly(self):
        """testing if the take_name attribute value is formatted correctly
        """
        for test_value in self.take_name_test_values:
            self.test_version.take_name = test_value[0]
            assert self.test_version.take_name == test_value[1]

    def test_task_argument_is_skipped(self):
        """testing if a TypeError will be raised when the task argument
        is skipped
        """
        from stalker import Version
        self.kwargs.pop('task')
        with pytest.raises(TypeError) as cm:
            Version(**self.kwargs)

        assert str(cm.value) == 'Version.task can not be None'

    def test_task_argument_is_None(self):
        """testing if a TypeError will be raised when the task argument
        is None
        """
        from stalker import Version
        self.kwargs['task'] = None
        with pytest.raises(TypeError) as cm:
            Version(**self.kwargs)

        assert str(cm.value) == 'Version.task can not be None'

    def test_task_attribute_is_None(self):
        """testing if a TypeError will be raised when the task attribute
        is None
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.task = None

        assert str(cm.value) == 'Version.task can not be None'

    def test_task_argument_is_not_a_Task(self):
        """testing if a TypeError will be raised when the task argument
        is not a Task instance
        """
        from stalker import Version
        self.kwargs['task'] = 'a task'
        with pytest.raises(TypeError) as cm:
            Version(**self.kwargs)

        assert str(cm.value) == \
            'Version.task should be a stalker.models.task.Task instance not ' \
            'str'

    def test_task_attribute_is_not_a_Task(self):
        """testing if a TypeError will be raised when the task attribute
        is not a Task instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.task = 'a task'

        assert str(cm.value) == \
            'Version.task should be a stalker.models.task.Task instance not ' \
            'str'

    def test_task_attribute_is_working_properly(self):
        """testing if the task attribute is working properly
        """
        from stalker import Task
        new_task = Task(
            name='New Test Task',
            parent=self.test_shot1,
        )

        assert self.test_version.task is not new_task
        self.test_version.task = new_task
        assert self.test_version.task is new_task

    def test_version_number_attribute_is_automatically_generated(self):
        """testing if the version_number attribute is automatically generated
        """
        from stalker.db.session import DBSession
        from stalker import Version
        assert self.test_version.version_number == 1
        DBSession.add(self.test_version)
        DBSession.commit()

        new_version = Version(**self.kwargs)
        DBSession.add(new_version)
        DBSession.commit()

        assert self.test_version.task == new_version.task
        assert self.test_version.take_name == new_version.take_name

        assert new_version.version_number == 2

        new_version = Version(**self.kwargs)
        DBSession.add(new_version)
        DBSession.commit()

        assert self.test_version.task == new_version.task
        assert self.test_version.take_name == new_version.take_name

        assert new_version.version_number == 3

        new_version = Version(**self.kwargs)
        DBSession.add(new_version)
        DBSession.commit()

        assert self.test_version.task == new_version.task
        assert self.test_version.take_name == new_version.take_name

        assert new_version.version_number == 4

    def test_version_number_attribute_is_starting_from_1(self):
        """testing if the version_number attribute is starting from 1
        """
        assert self.test_version.version_number == 1

    def test_version_number_attribute_is_set_to_a_lower_then_it_should_be(self):
        """testing if the version_number attribute will be set to a correct
        unique value when it is set to a lower number then it should be
        """
        from stalker import Version
        self.test_version.version_number = -1
        assert self.test_version.version_number == 1

        self.test_version.version_number = -10
        assert self.test_version.version_number == 1

        from stalker.db.session import DBSession
        DBSession.add(self.test_version)
        DBSession.commit()

        self.test_version.version_number = -100
        # it should be 1 again
        assert self.test_version.version_number == 1

        new_version = Version(**self.kwargs)
        assert new_version.version_number == 2

        new_version.version_number = 1
        assert new_version.version_number == 2

        new_version.version_number = 100
        assert new_version.version_number == 100

    def test_inputs_argument_is_skipped(self):
        """testing if the inputs attribute will be an empty list when the
        inputs argument is skipped
        """
        from stalker import Version
        self.kwargs.pop('inputs')
        new_version = Version(**self.kwargs)
        assert new_version.inputs == []

    def test_inputs_argument_is_None(self):
        """testing if the inputs attribute will be an empty list when the
        inputs argument is None
        """
        from stalker import Version
        self.kwargs['inputs'] = None
        new_version = Version(**self.kwargs)
        assert new_version.inputs == []

    def test_inputs_attribute_is_None(self):
        """testing if a TypeError will be raised when the inputs argument is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.inputs = None

        assert str(cm.value) == \
            'Incompatible collection type: None is not list-like'

    def test_inputs_argument_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the inputs attribute is
        set to something other than a Link instance
        """
        from stalker import Version
        test_value = [132, '231123']
        self.kwargs['inputs'] = test_value
        with pytest.raises(TypeError) as cm:
            Version(**self.kwargs)

        assert str(cm.value) == \
            'All elements in Version.inputs should be all ' \
            'stalker.models.link.Link instances not int'

    def test_inputs_attribute_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the inputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, '231123']
        with pytest.raises(TypeError) as cm:
            self.test_version.inputs = test_value

        assert str(cm.value) == \
            'All elements in Version.inputs should be all ' \
            'stalker.models.link.Link instances not int'

    def test_inputs_attribute_is_working_properly(self):
        """testing if the inputs attribute is working properly
        """
        from stalker import Version
        self.kwargs.pop('inputs')
        new_version = Version(**self.kwargs)

        assert self.test_input_link1 not in new_version.inputs
        assert self.test_input_link2 not in new_version.inputs

        new_version.inputs = [self.test_input_link1, self.test_input_link2]

        assert self.test_input_link1 in new_version.inputs
        assert self.test_input_link2 in new_version.inputs

    def test_outputs_argument_is_skipped(self):
        """testing if the outputs attribute will be an empty list when the
        outputs argument is skipped
        """
        from stalker import Version
        self.kwargs.pop('outputs')
        new_version = Version(**self.kwargs)
        assert new_version.outputs == []

    def test_outputs_argument_is_None(self):
        """testing if the outputs attribute will be an empty list when the
        outputs argument is None
        """
        from stalker import Version
        self.kwargs['outputs'] = None
        new_version = Version(**self.kwargs)
        assert new_version.outputs == []

    def test_outputs_attribute_is_None(self):
        """testing if a TypeError will be raised when the outputs argument is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.outputs = None

        assert str(cm.value) == \
            'Incompatible collection type: None is not list-like'

    def test_outputs_argument_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the outputs attribute is
        set to something other than a Link instance
        """
        from stalker import Version
        test_value = [132, '231123']
        self.kwargs['outputs'] = test_value
        with pytest.raises(TypeError) as cm:
            Version(**self.kwargs)

        assert str(cm.value) == \
            'All elements in Version.outputs should be all ' \
            'stalker.models.link.Link instances not int'

    def test_outputs_attribute_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the outputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, '231123']
        with pytest.raises(TypeError) as cm:
            self.test_version.outputs = test_value

        assert str(cm.value) == \
            'All elements in Version.outputs should be all ' \
            'stalker.models.link.Link instances not int'

    def test_outputs_attribute_is_working_properly(self):
        """testing if the outputs attribute is working properly
        """
        from stalker import Version
        self.kwargs.pop('outputs')
        new_version = Version(**self.kwargs)

        assert self.test_output_link1 not in new_version.outputs
        assert self.test_output_link2 not in new_version.outputs

        new_version.outputs = [self.test_output_link1, self.test_output_link2]

        assert self.test_output_link1 in new_version.outputs
        assert self.test_output_link2 in new_version.outputs

    def test_is_published_attribute_is_False_by_default(self):
        """testing if the is_published attribute is False by default
        """
        assert self.test_version.is_published is False

    def test_is_published_attribute_is_working_properly(self):
        """testing if the is_published attribute is working properly
        """
        self.test_version.is_published = True
        assert self.test_version.is_published is True

        self.test_version.is_published = False
        assert self.test_version.is_published is False

    def test_parent_argument_is_skipped(self):
        """testing if the parent attribute will be None if the parent argument
        is skipped
        """
        from stalker import Version
        try:
            self.kwargs.pop('parent')
        except KeyError:
            pass
        new_version = Version(**self.kwargs)
        assert new_version.parent is None

    def test_parent_argument_is_None(self):
        """testing if the parent attribute will be None if the parent argument
        is skipped
        """
        from stalker import Version
        self.kwargs['parent'] = None
        new_version = Version(**self.kwargs)
        assert new_version.parent is None

    def test_parent_attribute_is_None(self):
        """testing if the parent attribute value will be None if it is set to
        None
        """
        self.test_version.parent = None
        assert self.test_version.parent is None

    def test_parent_argument_is_not_a_Version_instance(self):
        """testing if a TypeError will be raised when the parent argument is
        not a Version instance
        """
        from stalker import Version
        self.kwargs['parent'] = 'not a version instance'
        with pytest.raises(TypeError) as cm:
            Version(**self.kwargs)

        assert str(cm.value) == \
            'Version.parent should be an instance of Version class or ' \
            'derivative, not str'

    def test_parent_attribute_is_not_set_to_a_Version_instance(self):
        """testing if a TypeError will be raised when the parent attribute is
        not set to a Version instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.parent = 'not a version instance'

        assert str(cm.value) == \
            'Version.parent should be an instance of Version class or ' \
            'derivative, not str'

    def test_parent_argument_is_working_properly(self):
        """testing if the parent argument is working properly
        """
        self.kwargs['parent'] = self.test_version
        from stalker import Version
        new_version = Version(**self.kwargs)
        assert new_version.parent == self.test_version

    def test_parent_attribute_is_working_properly(self):
        """testing if the parent attribute is working properly
        """
        self.kwargs['parent'] = None
        from stalker import Version
        new_version = Version(**self.kwargs)
        assert new_version.parent != self.test_version
        new_version.parent = self.test_version
        assert new_version.parent == self.test_version

    def test_parent_argument_updates_the_children_attribute(self):
        """testing if the parent argument updates the children attribute of the
        parent Version properly
        """
        from stalker import Version
        self.kwargs['parent'] = self.test_version
        new_version = Version(**self.kwargs)
        assert new_version in self.test_version.children

    def test_parent_attribute_updates_the_children_attribute(self):
        """testing if the parent attribute updates the children attribute of
        the parent Version properly
        """
        from stalker import Version
        self.kwargs['parent'] = None
        new_version = Version(**self.kwargs)
        assert new_version.parent != self.test_version
        new_version.parent = self.test_version
        assert new_version in self.test_version.children

    def test_parent_attribute_will_not_allow_circular_dependencies(self):
        """testing if a CircularDependency will be raised when the given
        Version to the parent attribute is a children of the current Version
        """
        from stalker import Version
        from stalker.exceptions import CircularDependencyError
        self.kwargs['parent'] = self.test_version
        version1 = Version(**self.kwargs)
        with pytest.raises(CircularDependencyError) as cm:
            self.test_version.parent = version1

        assert str(cm.value) == \
            '<tp_SH001_Task1_TestTake_v001 (Version)> (Version) and ' \
            '<tp_SH001_Task1_TestTake_v002 (Version)> (Version) creates a ' \
            'circular dependency in their "children" attribute'

    def test_parent_attribute_will_not_allow_deeper_circular_dependencies(self):
        """testing if a CircularDependency will be raised when the given
        Version is a parent of the current parent
        """
        from stalker import Version
        self.kwargs['parent'] = self.test_version
        version1 = Version(**self.kwargs)

        self.kwargs['parent'] = version1
        version2 = Version(**self.kwargs)

        # now create circular dependency
        from stalker.exceptions import CircularDependencyError
        with pytest.raises(CircularDependencyError) as cm:
            self.test_version.parent = version2

        assert str(cm.value) == \
            '<tp_SH001_Task1_TestTake_v001 (Version)> (Version) and ' \
            '<tp_SH001_Task1_TestTake_v002 (Version)> (Version) creates a ' \
            'circular dependency in their "children" attribute'

    def test_children_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the children attribute is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.children = None

        assert str(cm.value) == \
            'Incompatible collection type: None is not list-like'

    def test_children_attribute_is_not_set_to_a_list(self):
        """testing if a TypeError will be raised when the children attribute is
        not set to a list
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.children = 'not a list of Version instances'

        assert str(cm.value) == \
            'Incompatible collection type: str is not list-like'

    def test_children_attribute_is_not_set_to_a_list_of_Version_instances(self):
        """testing if a TypeError will be raised when the children attribute is
        not set to a list of Version instances
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.children = ['not a Version instance', 3]

        assert str(cm.value) == \
            'Version.children should be a list of Version (or derivative) ' \
            'instances, not str'

    def test_children_attribute_is_working_properly(self):
        """testing if the children attribute is working properly
        """
        self.kwargs['parent'] = None
        from stalker import Version
        new_version1 = Version(**self.kwargs)
        self.test_version.children = [new_version1]
        assert new_version1 in self.test_version.children

        new_version2 = Version(**self.kwargs)
        self.test_version.children.append(new_version2)
        assert new_version2 in self.test_version.children

    def test_children_attribute_updates_parent_attribute(self):
        """testing if the children attribute updates the parent attribute of
        the children Versions
        """
        self.kwargs['parent'] = None
        from stalker import Version
        new_version1 = Version(**self.kwargs)
        self.test_version.children = [new_version1]
        assert new_version1.parent == self.test_version

        new_version2 = Version(**self.kwargs)
        self.test_version.children.append(new_version2)
        assert new_version2.parent == self.test_version

    def test_children_attribute_will_not_allow_circular_dependencies(self):
        """testing if a CircularDependency error will be raised when a parent
        Version is set as a children to its child
        """
        from stalker import Version
        self.kwargs['parent'] = None
        new_version1 = Version(**self.kwargs)
        from stalker.db.session import DBSession
        DBSession.add(new_version1)
        DBSession.commit()
        new_version2 = Version(**self.kwargs)
        DBSession.add(new_version2)
        DBSession.commit()

        new_version1.parent = new_version2
        from stalker.exceptions import CircularDependencyError
        with pytest.raises(CircularDependencyError) as cm:
            new_version1.children.append(new_version2)

        assert str(cm.value) == \
            '<tp_SH001_Task1_TestTake_v003 (Version)> (Version) and ' \
            '<tp_SH001_Task1_TestTake_v002 (Version)> (Version) creates a ' \
            'circular dependency in their "children" attribute'

    def test_children_attribute_will_not_allow_deeper_circular_dependencies(self):
        """testing if a CircularDependency error will be raised when the a
        parent Version of a parent Version is set as a children to its grand
        child
        """
        self.kwargs['parent'] = None
        from stalker import Version
        from stalker.db.session import DBSession
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()
        new_version2 = Version(**self.kwargs)
        DBSession.add(new_version2)
        DBSession.commit()
        new_version3 = Version(**self.kwargs)
        DBSession.add(new_version2)
        DBSession.commit()

        new_version1.parent = new_version2
        new_version2.parent = new_version3

        from stalker.exceptions import CircularDependencyError
        with pytest.raises(CircularDependencyError) as cm:
            new_version1.children.append(new_version3)

        assert str(cm.value) == \
            '<tp_SH001_Task1_TestTake_v004 (Version)> (Version) and ' \
            '<tp_SH001_Task1_TestTake_v002 (Version)> (Version) creates a ' \
            'circular dependency in their "children" attribute'

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

        from stalker import FilenameTemplate
        ft = FilenameTemplate(
            name='Task Filename Template',
            target_entity_type='Task',
            path='{{project.code}}/{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/{%- endfor -%}',
            filename='{{task.nice_name}}_{{version.take_name}}'
                     '_v{{"%03d"|format(version.version_number)}}{{extension}}'
        )
        self.test_project.structure.templates.append(ft)
        from stalker.db.session import DBSession
        from stalker import Version
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()
        new_version1.update_paths()

        assert new_version1.path == 'tp/SH001/Task1'

        new_version1.extension = '.ma'
        assert new_version1.filename == 'Task1_TestTake_v002.ma'

    def test_update_paths_will_preserve_extension(self):
        """testing if update_paths method will preserve the extension.
        """
        # create a FilenameTemplate for Task instances
        from stalker import FilenameTemplate
        ft = FilenameTemplate(
            name='Task Filename Template',
            target_entity_type='Task',
            path='{{project.code}}/{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/{%- endfor -%}',
            filename='{{task.nice_name}}_{{version.take_name}}'
                     '_v{{"%03d"|format(version.version_number)}}{{extension}}'
        )
        self.test_project.structure.templates.append(ft)
        from stalker.db.session import DBSession
        from stalker import Version
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()
        new_version1.update_paths()

        assert new_version1.path == 'tp/SH001/Task1'

        extension = '.ma'
        new_version1.extension = extension
        assert new_version1.filename == 'Task1_TestTake_v002.ma'

        # rename the task and update the paths
        self.test_task1.name = 'Task2'

        # now call update_paths and expect the extension to be preserved
        new_version1.update_paths()
        assert new_version1.filename == 'Task2_TestTake_v002.ma'
        assert new_version1.extension == extension

    def test_update_paths_will_raise_a_RuntimeError_if_there_is_no_suitable_FilenameTemplate(self):
        """testing if update_paths method will raise a RuntimeError if there is
        no suitable FilenameTemplate instance found
        """
        from stalker import Version
        self.kwargs['parent'] = None
        new_version1 = Version(**self.kwargs)
        with pytest.raises(RuntimeError) as cm:
            new_version1.update_paths()

        assert str(cm.value) == \
            "There are no suitable FilenameTemplate (target_entity_type == " \
            "'Task') defined in the Structure of the related Project " \
            "instance, please create a new " \
            "stalker.models.template.FilenameTemplate instance with its " \
            "'target_entity_type' attribute is set to 'Task' and assign it " \
            "to the `templates` attribute of the structure of the project"

    def test_template_variables_project(self):
        """testing if the project in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        assert kwargs['project'] == self.test_version.task.project

    def test_template_variables_sequences(self):
        """testing if the sequences in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        assert kwargs['sequences'] == []

    def test_template_variables_scenes(self):
        """testing if the scenes in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        assert kwargs['scenes'] == []

    def test_template_variables_shot(self):
        """testing if the shot in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        assert kwargs['shot'] == self.test_version.task

    def test_template_variables_asset(self):
        """testing if the asset in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        assert kwargs['asset'] == self.test_version.task

    def test_template_variables_task(self):
        """testing if the task in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        assert kwargs['task'] == self.test_version.task

    def test_template_variables_parent_tasks(self):
        """testing if the parent_tasks in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        parents = self.test_version.task.parents
        parents.append(self.test_version.task)
        assert kwargs['parent_tasks'] == parents

    def test_template_variables_version(self):
        """testing if the version in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        assert kwargs['version'] == self.test_version

    def test_template_variables_type(self):
        """testing if the type in template variables is correct
        """
        kwargs = self.test_version._template_variables()
        assert kwargs['type'] == self.test_version.type

    def test_absolute_full_path_works_properly(self):
        """testing if the absolute_full_path attribute works properly
        """
        self.patcher.patch('Linux')
        from stalker import FilenameTemplate
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
        from stalker.db.session import DBSession
        from stalker import Version
        new_version1 = Version(**self.kwargs)
        DBSession.add(new_version1)
        DBSession.commit()

        new_version1.take_name = 'TestTake@BBOX'

        new_version1.update_paths()
        new_version1.extension = '.ma'
        assert new_version1.extension == '.ma'

        assert new_version1.absolute_full_path == \
            '/mnt/T/tp/SH001/Task1/Task1_TestTake@BBOX_v002.ma'

    def test_latest_published_version_is_read_only(self):
        """testing if the latest_published_version is a read only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_version.latest_published_version = True

        assert str(cm.value) == "can't set attribute"

    def test_latest_published_version_is_working_properly(self):
        """testing if the is_latest_published_version is working properly
        """
        from stalker.db.session import DBSession
        from stalker import Version
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

        assert new_version1.latest_published_version == new_version4
        assert new_version2.latest_published_version == new_version4
        assert new_version3.latest_published_version == new_version4
        assert new_version4.latest_published_version == new_version4
        assert new_version5.latest_published_version == new_version4

    def test_is_latest_published_version_is_working_properly(self):
        """testing if the is_latest_published_version is working properly
        """
        from stalker.db.session import DBSession
        from stalker import Version
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

        assert not new_version1.is_latest_published_version()
        assert not new_version2.is_latest_published_version()
        assert not new_version3.is_latest_published_version()
        assert new_version4.is_latest_published_version()
        assert not new_version5.is_latest_published_version()

    def test_equality_operator(self):
        """testing equality of two Version instances
        """
        from stalker.db.session import DBSession
        from stalker import Version
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

        assert not new_version1 == new_version2
        assert not new_version1 == new_version3
        assert not new_version1 == new_version4
        assert not new_version1 == new_version5

        assert not new_version2 == new_version3
        assert not new_version2 == new_version4
        assert not new_version2 == new_version5

        assert not new_version3 == new_version4
        assert not new_version3 == new_version5

        assert not new_version4 == new_version5

    def test_inequality_operator(self):
        """testing inequality of two Version instances
        """
        from stalker.db.session import DBSession
        from stalker import Version
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

        assert new_version1 != new_version2
        assert new_version1 != new_version3
        assert new_version1 != new_version4
        assert new_version1 != new_version5

        assert new_version2 != new_version3
        assert new_version2 != new_version4
        assert new_version2 != new_version5

        assert new_version3 != new_version4
        assert new_version3 != new_version5

        assert new_version4 != new_version5

    def test_created_with_argument_can_be_skipped(self):
        """testing if the created_with argument can be skipped
        """
        from stalker import Version
        self.kwargs.pop('created_with')
        Version(**self.kwargs)

    def test_created_with_argument_can_be_None(self):
        """testing if the created_with argument can be None
        """
        from stalker import Version
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
        from stalker import Version
        self.kwargs['created_with'] = 234
        with pytest.raises(TypeError) as cm:
            Version(**self.kwargs)

        assert str(cm.value) == \
            'Version.created_with should be an instance of str, not int'

    def test_created_with_attribute_accepts_only_string_or_None(self):
        """testing if a TypeError will be raised if the created_with attribute
        is set to a value other than a string or None
        """
        with pytest.raises(TypeError) as cm:
            self.test_version.created_with = 234

        assert str(cm.value) == \
            'Version.created_with should be an instance of str, not int'

    def test_created_with_argument_is_working_properly(self):
        """testing if the created_with argument value is passed to created_with
        attribute properly
        """
        from stalker import Version
        test_value = 'Maya'
        self.kwargs['created_with'] = test_value
        test_version = Version(**self.kwargs)
        assert test_version.created_with == test_value

    def test_created_with_attribute_is_working_properly(self):
        """testing if created_with attribute is working properly
        """
        test_value = 'Maya'
        assert self.test_version.created_with != test_value
        self.test_version.created_with = test_value
        assert self.test_version.created_with == test_value

    def test_max_version_number_attribute_is_read_only(self):
        """testing if the max_version_number attribute is read only
        """
        with pytest.raises(AttributeError) as cm:
            self.test_version.max_version_number = 20

        assert str(cm.value) == "can't set attribute"

    def test_max_version_number_attribute_is_working_properly(self):
        """testing if the max_version_number attribute is working properly
        """
        from stalker.db.session import DBSession
        from stalker import Version
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

        assert new_version5.version_number == 6

        assert new_version1.max_version_number == 6
        assert new_version2.max_version_number == 6
        assert new_version3.max_version_number == 6
        assert new_version4.max_version_number == 6
        assert new_version5.max_version_number == 6

    def test_latest_version_attribute_is_read_only(self):
        """testing if the last_version attribute is a read only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_version.latest_version = 3453

        assert str(cm.value) == "can't set attribute"

    def test_latest_version_attribute_is_working_properly(self):
        """testing if the last_version attribute is working properly
        """
        from stalker.db.session import DBSession
        from stalker import Version
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

        assert new_version5.version_number == 6

        assert new_version1.latest_version == new_version5
        assert new_version2.latest_version == new_version5
        assert new_version3.latest_version == new_version5
        assert new_version4.latest_version == new_version5
        assert new_version5.latest_version == new_version5

    def test_naming_parents_attribute_is_a_read_only_property(self):
        """testing if the naming_parents attribute is a read only property
        """
        with pytest.raises(AttributeError) as cm:
            self.test_version.naming_parents = [self.test_task1]

        assert str(cm.value) == "can't set attribute"

    def test_naming_parents_attribute_is_working_properly(self):
        """testing if the naming_parents attribute is working properly
        """
        from stalker import Task
        # for self.test_version
        assert self.test_version.naming_parents == \
            [self.test_shot1, self.test_task1]

        # for a new version of a task
        task1 = Task(
            name='Test Task 1',
            project=self.test_project,
        )

        task2 = Task(
            name='Test Task 2',
            parent=task1,
        )

        task3 = Task(
            name='Test Task 3',
            parent=task2,
        )
        from stalker.db.session import DBSession
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        from stalker import Version
        version1 = Version(
            task=task3
        )
        DBSession.add(version1)
        DBSession.commit()

        assert version1.naming_parents == [task1, task2, task3]

        # for a an asset version
        from stalker import Type
        character_type = Type(
            target_entity_type='Asset',
            name='Character',
            code='Char'
        )
        from stalker import Asset
        asset1 = Asset(
            name='Asset1',
            code='Asset1',
            parent=task1,
            type=character_type
        )
        DBSession.add(asset1)
        DBSession.commit()

        version2 = Version(
            task=asset1
        )
        assert version2.naming_parents == [asset1]

        # for a version of a task of a shot
        from stalker import Shot
        shot2 = Shot(
            name='SH002',
            code='SH002',
            parent=task3,
        )
        DBSession.add(shot2)
        DBSession.commit()

        task4 = Task(
            name='Test Task 4',
            parent=shot2,
        )
        DBSession.add(task4)
        DBSession.commit()

        version3 = Version(
            task=task4
        )

        assert version3.naming_parents == [shot2, task4]

        # for an asset of a shot
        asset2 = Asset(
            name='Asset2',
            code='Asset2',
            parent=shot2,
            type=character_type
        )
        DBSession.add(asset2)
        DBSession.commit()

        version4 = Version(task=asset2)
        assert version4.naming_parents == [asset2]

    def test_nice_name_attribute_is_working_properly(self):
        """testing if the nice_name attribute is working properly
        """
        from stalker import Task
        # for self.test_version
        assert self.test_version.naming_parents == \
            [self.test_shot1, self.test_task1]

        # for a new version of a task
        task1 = Task(
            name='Test Task 1',
            project=self.test_project,
        )

        task2 = Task(
            name='Test Task 2',
            parent=task1,
        )

        task3 = Task(
            name='Test Task 3',
            parent=task2,
        )
        from stalker.db.session import DBSession
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        from stalker import Version
        version1 = Version(
            task=task3,
            take_name='Take1@Main'
        )
        DBSession.add(version1)
        DBSession.commit()

        assert version1.nice_name == \
            '%s_%s_%s_%s' % (
                task1.nice_name, task2.nice_name, task3.nice_name,
                version1.take_name
            )

        # for a an asset version
        from stalker import Type
        character_type = Type(
            target_entity_type='Asset',
            name='Character',
            code='Char'
        )
        from stalker import Asset
        asset1 = Asset(
            name='Asset1',
            code='Asset1',
            parent=task1,
            type=character_type
        )
        DBSession.add(asset1)
        DBSession.commit()

        version2 = Version(
            task=asset1
        )
        assert version2.nice_name == \
            '%s_%s' % (asset1.nice_name, version2.take_name)

        # for a version of a task of a shot
        from stalker import Shot
        shot2 = Shot(
            name='SH002',
            code='SH002',
            parent=task3,
        )
        DBSession.add(shot2)
        DBSession.commit()

        task4 = Task(
            name='Test Task 4',
            parent=shot2,
        )
        DBSession.add(task4)
        DBSession.commit()

        version3 = Version(
            task=task4
        )

        assert version3.nice_name == \
            '%s_%s_%s' % (shot2.nice_name, task4.nice_name, version3.take_name)

        # for an asset of a shot
        asset2 = Asset(
            name='Asset2',
            code='Asset2',
            parent=shot2,
            type=character_type
        )
        DBSession.add(asset2)
        DBSession.commit()

        version4 = Version(task=asset2)
        assert version4.nice_name == \
            '%s_%s' % (asset2.nice_name, version4.take_name)

    def test_string_representation_is_a_little_bit_meaningful(self):
        """testing if the __str__ or __repr__ result is meaningfull
        """
        assert '<tp_SH001_Task1_TestTake_v001 (Version)>' == \
            '%s' % self.test_version

    def test_walk_hierarchy_is_working_properly_in_DFS_mode(self):
        """testing if the walk_hierarchy() method is working in DFS mode
        correctly
        """
        from stalker import Version
        v1 = Version(task=self.test_task1)
        v2 = Version(task=self.test_task1, parent=v1)
        v3 = Version(task=self.test_task1, parent=v2)
        v4 = Version(task=self.test_task1, parent=v3)
        v5 = Version(task=self.test_task1, parent=v1)

        expected_result = [v1, v2, v3, v4, v5]
        visited_versions = []
        for v in v1.walk_hierarchy():
            visited_versions.append(v)

        assert expected_result == visited_versions

    def test_walk_inputs_is_working_properly_in_DFS_mode(self):
        """testing if the walk_inputs() method is working in DFS mode correctly
        """
        from stalker import Version
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

        assert expected_result == visited_versions

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
    #     DBSession.add(self.test_project)
    #     DBSession.commit()
    # 
    #     print 'entity_type: %s' % self.test_task1.entity_type
    # 
    #     # v1 = Version(task=self.test_task1)
    #     # assert 'tp/SH001/task1/task1_Main_v001' == v1.path
    #     self.fail()


class VersionTester(unittest.TestCase):
    """Non-DB related tests of Version class
    """

    def setUp(self):
        """setup the test
        """
        super(self.__class__, self).setUp()
        self.patcher = PlatformPatcher()

        from stalker import Status, StatusList

        # statuses
        self.test_status1 = Status(name='Status1', code='STS1')
        self.test_status2 = Status(name='Status2', code='STS2')
        self.test_status3 = Status(name='Status3', code='STS3')
        self.test_status4 = Status(name='Status4', code='STS4')
        self.test_status5 = Status(name='Status5', code='STS5')

        # status lists
        self.test_task_status_list = StatusList(
            name='Task Status List',
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type='Task',
        )

        self.test_asset_status_list = StatusList(
            name='Asset Status List',
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type='Asset',
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
            target_entity_type='Shot',
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
            target_entity_type='Sequence',
        )

        self.test_project_status_list = StatusList(
            name='Project Status List',
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type='Project',
        )

        # repository
        from stalker import Repository, Type
        self.test_repo = Repository(
            name='Test Repository',
            code='TR',
            linux_path='/mnt/T/',
            windows_path='T:/',
            osx_path='/Volumes/T/'
        )

        # a project type
        self.test_project_type = Type(
            name='Test',
            code='test',
            target_entity_type='Project',
        )

        # create a structure
        from stalker import Structure
        self.test_structure = Structure(
            name='Test Project Structure'
        )

        # create a project
        from stalker import Project
        self.test_project = Project(
            name='Test Project',
            code='tp',
            type=self.test_project_type,
            status_list=self.test_project_status_list,
            repositories=[self.test_repo],
            structure=self.test_structure
        )

        # create a sequence
        from stalker import Sequence
        self.test_sequence = Sequence(
            name='Test Sequence',
            code='SEQ1',
            project=self.test_project,
            status_list=self.test_sequence_status_list
        )

        # create a shot
        from stalker import Shot
        self.test_shot1 = Shot(
            name='SH001',
            code='SH001',
            project=self.test_project,
            sequences=[self.test_sequence],
            status_list=self.test_shot_status_list
        )

        # create a group of Tasks for the shot
        from stalker import Task
        self.test_task1 = Task(
            name='Task1',
            parent=self.test_shot1,
            status_list=self.test_task_status_list
        )

        # a Link for the input file
        from stalker import Link
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
        from stalker import Version
        self.test_version = Version(**self.kwargs)

        # set the published to False
        self.test_version.is_published = False

    def tearDown(self):
        """clean up test
        """
        self.patcher.restore()
        super(VersionTester, self).tearDown()

    def test_children_attribute_will_not_allow_circular_dependencies(self):
        """testing if a CircularDependency error will be raised when a parent
        Version is set as a children to its child
        """
        from stalker import Version
        self.kwargs['parent'] = None
        new_version1 = Version(**self.kwargs)
        new_version2 = Version(**self.kwargs)

        new_version1.parent = new_version2
        from stalker.exceptions import CircularDependencyError
        with pytest.raises(CircularDependencyError) as cm:
            new_version1.children.append(new_version2)

        assert str(cm.value) == \
            '<tp_SH001_Task1_TestTake_v003 (Version)> (Version) and ' \
            '<tp_SH001_Task1_TestTake_v002 (Version)> (Version) creates a ' \
            'circular dependency in their "children" attribute'

    def test_children_attribute_will_not_allow_deeper_circular_dependencies(self):
        """testing if a CircularDependency error will be raised when the a
        parent Version of a parent Version is set as a children to its grand
        child
        """
        self.kwargs['parent'] = None
        from stalker import Version
        new_version1 = Version(**self.kwargs)
        new_version2 = Version(**self.kwargs)
        new_version3 = Version(**self.kwargs)

        new_version1.parent = new_version2
        new_version2.parent = new_version3

        from stalker.exceptions import CircularDependencyError
        with pytest.raises(CircularDependencyError) as cm:
            new_version1.children.append(new_version3)

        assert str(cm.value) == \
            '<tp_SH001_Task1_TestTake_v004 (Version)> (Version) and ' \
            '<tp_SH001_Task1_TestTake_v002 (Version)> (Version) creates a ' \
            'circular dependency in their "children" attribute'
