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
from stalker import (Asset, Entity, Link, Project, Repository, Scene, Sequence,
                     Shot, Status, StatusList, Task, Type, ImageFormat)


class ShotTester(unittest2.TestCase):
    """Tests the Shot class
    """

    def setUp(self):
        """setup the test
        """
        # statuses
        self.test_status_complete = Status(
            name="Complete",
            code="CMPLT"
        )
        self.test_status_wip = Status(
            name="Work In Progress",
            code="WIP"
        )
        self.test_status_waiting = Status(
            name="Waiting To Start",
            code="WTS"
        )

        # status lists
        self.test_project_status_list = StatusList(
            name="Project Status List",
            statuses=[self.test_status_complete,
                      self.test_status_waiting,
                      self.test_status_wip],
            target_entity_type=Project,
        )

        self.test_sequence_status_list = StatusList(
            name="Project Status List",
            statuses=[self.test_status_complete,
                      self.test_status_waiting,
                      self.test_status_wip],
            target_entity_type='Sequence',
        )

        self.test_shot_status_list = StatusList(
            name="Shot Status List",
            statuses=[self.test_status_complete,
                      self.test_status_waiting,
                      self.test_status_wip],
            target_entity_type=Shot,
        )

        self.test_asset_status_list = StatusList(
            name="Asset Status List",
            statuses=[self.test_status_complete,
                      self.test_status_waiting,
                      self.test_status_wip],
            target_entity_type=Asset,
        )

        # types
        self.test_commercial_project_type = Type(
            name="Commercial Project",
            code='comm',
            target_entity_type=Project,
        )

        self.test_character_asset_type = Type(
            name="Character",
            code='char',
            target_entity_type=Asset,
        )

        self.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type=Repository
        )

        # repository
        self.test_repository = Repository(
            name="Test Repository",
            type=self.test_repository_type,
        )

        # image format
        self.test_image_format1 = ImageFormat(
            name='Test Image Format 1',
            width=1920,
            height=1080,
            pixel_aspect=1.0
        )

        self.test_image_format2 = ImageFormat(
            name='Test Image Format 2',
            width=1280,
            height=720,
            pixel_aspect=1.0
        )

        # project and sequences
        self.test_project1 = Project(
            name='Test Project1',
            code='tp1',
            type=self.test_commercial_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repository,
            image_format=self.test_image_format1
        )

        self.test_project2 = Project(
            name='Test Project2',
            code='tp2',
            type=self.test_commercial_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repository,
            image_format=self.test_image_format1
        )

        self.test_sequence1 = Sequence(
            name="Test Seq1",
            code='ts1',
            project=self.test_project1,
            status_list=self.test_sequence_status_list,
        )

        self.test_sequence2 = Sequence(
            name="Test Seq2",
            code='ts2',
            project=self.test_project1,
            status_list=self.test_sequence_status_list,
        )

        self.test_sequence3 = Sequence(
            name="Test Seq3",
            code='ts3',
            project=self.test_project1,
            status_list=self.test_sequence_status_list,
        )

        self.test_scene1 = Scene(
            name='Test Sce1',
            code='tsc1',
            project=self.test_project1,
        )

        self.test_scene2 = Scene(
            name='Test Sce2',
            code='tsc2',
            project=self.test_project1,
        )

        self.test_scene3 = Scene(
            name='Test Sce3',
            code='tsc3',
            project=self.test_project1
        )

        self.test_asset1 = Asset(
            name="Test Asset1",
            code='ta1',
            project=self.test_project1,
            status_list=self.test_asset_status_list,
            type=self.test_character_asset_type,
        )

        self.test_asset2 = Asset(
            name="Test Asset2",
            code='ta2',
            project=self.test_project1,
            status_list=self.test_asset_status_list,
            type=self.test_character_asset_type,
        )

        self.test_asset3 = Asset(
            name="Test Asset3",
            code='ta3',
            project=self.test_project1,
            status_list=self.test_asset_status_list,
            type=self.test_character_asset_type,
        )

        self.test_cut_in_default = 1
        self.test_cut_duration_default = 1
        self.test_cut_out_default = 1

        self.kwargs = dict(
            name='SH123',
            code='SH123',
            description='This is a test Shot',
            project=self.test_project1,
            sequences=[self.test_sequence1, self.test_sequence2],
            scenes=[self.test_scene1, self.test_scene2],
            cut_in=112,
            cut_out=149,
            cut_duration=123,
            status=0,
            status_list=self.test_shot_status_list,
            image_format=self.test_image_format2
        )

        # create a mock shot object
        self.test_shot = Shot(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for Shot
        class
        """
        self.assertTrue(Shot.__auto_name__)

    def test_project_argument_is_skipped(self):
        """testing if a TypeError will be raised when the project argument is
        skipped
        """
        self.kwargs.pop('project')
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_project_argument_is_None(self):
        """testing if a TypeError will be raised when the project argument is
        None
        """
        self.kwargs["project"] = None
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_project_argument_is_not_Project_instance(self):
        """testing if a TypeError will be raised when the given sequence
        argument is not a Project instance
        """
        test_values = [1, 1.2, "project", ["a", "project"]]
        for test_value in test_values:
            self.kwargs["project"] = test_value
            self.assertRaises(TypeError, Shot, self.kwargs)

    def test_project_argument_already_has_a_shot_with_the_same_code(self):
        """testing if a ValueError will be raised when the given project
        argument already has a shot with the same code
        """
        # lets try to assign the shot to the sequence2 which has another shot
        # with the same code
        self.kwargs['project'] = self.test_project1
        self.assertRaises(ValueError, Shot, **self.kwargs)

        # this should not raise a ValueError
        self.kwargs["code"] = "DifferentCode"
        new_shot2 = Shot(**self.kwargs)
        self.assertIsInstance(new_shot2, Shot)

    def test_project_attribute_is_read_only(self):
        """testing if the project attribute is read only
        """
        self.assertRaises(AttributeError, setattr, self.test_shot, "project",
                          self.test_project2)

    def test_project_contains_shots(self):
        """testing if the current shot is going to be added to the Project, so
        the Project.shots list will contain the current shot
        """
        self.assertIn(self.test_shot, self.test_shot.project.shots)

    def test_project_argument_is_working_properly(self):
        """testing if the project argument is working properly
        """
        self.assertEqual(self.test_shot.project, self.kwargs["project"])

    def test_sequences_argument_is_skipped(self):
        """testing if the sequences attribute will be an empty list when the
        sequences argument is skipped
        """
        self.kwargs.pop('sequences')
        self.kwargs['code'] = 'DifferentCode'
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.sequences, [])

    def test_sequences_argument_is_None(self):
        """testing if the sequences attribute will be an empty list when the
        sequences argument is set to None
        """
        self.kwargs['sequences'] = None
        self.kwargs['code'] = 'NewCode'
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.sequences, [])

    def test_sequences_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the sequences attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_shot, 'sequences',
                          None)

    def test_sequences_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the sequences argument is
        not a list
        """
        self.kwargs['sequences'] = 'not a list'
        self.kwargs['code'] = 'NewCode'
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_sequences_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the sequences attribute
        is not a list
        """
        self.assertRaises(TypeError, setattr, self.test_shot, 'sequences',
                          'not a list')

    def test_sequences_argument_is_not_a_list_of_Sequence_instances(self):
        """testing if a TypeError will be raised when the sequences argument is
        not a list of Sequences
        """
        self.kwargs['sequences'] = ['not', 1, 'list', 'of', 'sequences']
        self.kwargs['code'] = 'NewShot'
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_sequences_attribute_is_not_a_list_of_Sequence_instances(self):
        """testing if a TypeError will be raised when the sequences attribute
        is not a list of Sequence instances
        """
        self.assertRaises(TypeError, setattr, self.test_shot, 'sequences',
                          ['not', 1, 'list', 'of', 'sequences'])

    def test_sequences_argument_is_working_properly(self):
        """testing if the sequences attribute is working properly
        """
        self.kwargs['code'] = 'NewShot'

        seq1 = Sequence(
            name='seq1',
            code='seq1',
            project=self.test_project1,
            status_list=self.test_sequence_status_list
        )
        seq2 = Sequence(
            name='seq2',
            code='seq2',
            project=self.test_project1,
            status_list=self.test_sequence_status_list
        )
        seq3 = Sequence(
            name='seq3',
            code='seq3',
            project=self.test_project1,
            status_list=self.test_sequence_status_list
        )

        seqs = [seq1, seq2, seq3]
        self.kwargs['sequences'] = seqs
        new_shot = Shot(**self.kwargs)

        self.assertItemsEqual(new_shot.sequences, seqs)

    def test_sequences_attribute_is_working_properly(self):
        """testing if the sequences attribute is working properly
        """
        self.kwargs['code'] = 'NewShot'

        seq1 = Sequence(
            name='seq1',
            code='seq1',
            project=self.test_project1,
            status_list=self.test_sequence_status_list
        )
        seq2 = Sequence(
            name='seq2',
            code='seq2',
            project=self.test_project1,
            status_list=self.test_sequence_status_list
        )
        seq3 = Sequence(
            name='seq3',
            code='seq3',
            project=self.test_project1,
            status_list=self.test_sequence_status_list
        )

        new_shot = Shot(**self.kwargs)

        new_shot.sequences = [seq1]
        new_shot.sequences.append(seq2)
        new_shot.sequences.append(seq3)

        seqs = [seq1, seq2, seq3]
        self.assertItemsEqual(new_shot.sequences, seqs)

    def test_scenes_argument_is_skipped(self):
        """testing if the scenes attribute will be an empty list when the
        scenes argument is skipped
        """
        self.kwargs.pop('scenes')
        self.kwargs['code'] = 'DifferentCode'
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.scenes, [])

    def test_scenes_argument_is_None(self):
        """testing if the scenes attribute will be an empty list when the
        scenes argument is set to None
        """
        self.kwargs['scenes'] = None
        self.kwargs['code'] = 'NewCode'
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.scenes, [])

    def test_scenes_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the scenes attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_shot, 'scenes',
                          None)

    def test_scenes_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the scenes argument is
        not a list
        """
        self.kwargs['scenes'] = 'not a list'
        self.kwargs['code'] = 'NewCode'
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_scenes_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the scenes attribute
        is not a list
        """
        self.assertRaises(TypeError, setattr, self.test_shot, 'scenes',
                          'not a list')

    def test_scenes_argument_is_not_a_list_of_Scene_instances(self):
        """testing if a TypeError will be raised when the scenes argument is
        not a list of Scenes
        """
        self.kwargs['scenes'] = ['not', 1, 'list', 'of', 'scenes']
        self.kwargs['code'] = 'NewShot'
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_scenes_attribute_is_not_a_list_of_Scene_instances(self):
        """testing if a TypeError will be raised when the scenes attribute
        is not a list of Scene instances
        """
        self.assertRaises(TypeError, setattr, self.test_shot, 'scenes',
                          ['not', 1, 'list', 'of', 'scenes'])

    def test_scenes_argument_is_working_properly(self):
        """testing if the scenes attribute is working properly
        """
        self.kwargs['code'] = 'NewShot'

        sce1 = Scene(name='sce1', code='sce1', project=self.test_project1)
        sce2 = Scene(name='sce2', code='sce2', project=self.test_project1)
        sce3 = Scene(name='sce3', code='sce3', project=self.test_project1)

        seqs = [sce1, sce2, sce3]
        self.kwargs['scenes'] = seqs
        new_shot = Shot(**self.kwargs)

        self.assertItemsEqual(new_shot.scenes, seqs)

    def test_scenes_attribute_is_working_properly(self):
        """testing if the scenes attribute is working properly
        """
        self.kwargs['code'] = 'NewShot'

        sce1 = Scene(name='sce1', code='sce1', project=self.test_project1)
        sce2 = Scene(name='sce2', code='sce2', project=self.test_project1)
        sce3 = Scene(name='sce3', code='sce3', project=self.test_project1)

        new_shot = Shot(**self.kwargs)

        new_shot.scenes = [sce1]
        new_shot.scenes.append(sce2)
        new_shot.scenes.append(sce3)

        seqs = [sce1, sce2, sce3]
        self.assertItemsEqual(new_shot.scenes, seqs)

    def test_cut_in_argument_is_skipped_defaults_to_default_value(self):
        """testing if the cut_in argument is skipped the cut_in argument will
        be set to the default value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_in")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_in, self.test_cut_in_default)

    def test_cut_in_argument_is_set_to_None_defaults_to_default_value(self):
        """testing if the cut_in argument is set to None the cut_in attribute
        is set to default value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = None
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_in, self.test_cut_in_default)

    def test_cut_in_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the cut_in argument is
        not an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = "a string"
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_cut_in_attribute_is_not_integer(self):
        """testing if a TypeError will be used when the cut_in attribute is
        not an instance of int
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_shot,
            "cut_in",
            "a string"
        )

    def test_cut_in_argument_is_bigger_than_cut_out_argument(self):
        """testing if the cut_out attribute is updated when the cut_in
        argument is bigger than cut_out argument
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = self.kwargs["cut_out"] + 10
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)
        self.assertEqual(new_shot.cut_duration, 1)

    def test_cut_in_attribute_is_bigger_than_cut_out_attribute(self):
        """testing if the cut_out attribute is updated when the cut_in
        attribute is bigger than cut_out attribute
        """
        self.test_shot.cut_in = self.test_shot.cut_out + 10
        self.assertEqual(self.test_shot.cut_out,
                         self.test_shot.cut_in)
        self.assertEqual(self.test_shot.cut_duration, 1)

    def test_cut_out_argument_is_skipped_defaults_to_default_value(self):
        """testing if the cut_out argument is skipped the cut_out attribute
        will be set to the default value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_out")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_out,
                         new_shot.cut_in + new_shot.cut_duration - 1)

    def test_cut_out_argument_is_set_to_None_defaults_to_default_value(self):
        """testing if the cut_out argument is set to None the cut_out attribute
        is set to default value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = None
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_out,
                         new_shot.cut_in + new_shot.cut_duration - 1)

    def test_cut_out_attribute_is_set_to_None_defaults_to_default_value(self):
        """testing if the cut_out attribute is set to None it is going to be
        set to default value
        """
        self.test_shot.cut_out = None
        self.assertEqual(self.test_shot.cut_out,
                         self.test_shot.cut_in +
                         self.test_shot.cut_duration - 1)

    def test_cut_out_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the cut_out argument is
        not an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = "a string"
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_cut_out_attribute_is_not_integer(self):
        """testing if a TypeError will be used when the cut_out attribute is
        not an instance of int
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_shot,
            "cut_out",
            "a string"
        )

    def test_cut_out_argument_is_smaller_than_cut_in_argument(self):
        """testing if the cut_out attribute is updated when the cut_out
        argument is smaller than cut_in argument
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = self.kwargs["cut_in"] - 10
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)
        self.assertEqual(new_shot.cut_duration, 1)

    def test_cut_out_attribute_is_smaller_than_cut_in_attribute(self):
        """testing if the cut_out attribute is updated when it is smaller than
        cut_in attribute
        """
        self.test_shot.cut_out = self.test_shot.cut_in - 10
        self.assertEqual(self.test_shot.cut_out,
                         self.test_shot.cut_in)
        self.assertEqual(self.test_shot.cut_duration, 1)

    def test_cut_duration_argument_is_skipped(self):
        """testing if the cut_duration attribute will be calculated from the
        cut_in and cut_out attributes when the cut_duration argument is skipped
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_duration")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration,
                         new_shot.cut_out - new_shot.cut_in + 1)

    def test_cut_duration_argument_is_None(self):
        """testing if the value of cut_duration will be calculated from the
        cut_in and cut_out attributes.
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = None
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration,
                         new_shot.cut_out - new_shot.cut_in + 1)

    def test_cut_duration_argument_is_not_instance_of_int(self):
        """testing if a TypeError will be raised when the cut_duration
        argument is not an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = "a string"
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_cut_duration_attribute_is_not_instance_of_int(self):
        """testing if a TypeError will be raised when the cut_duration
        attribute is not an instance of int
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_shot,
            "cut_duration",
            "a string"
        )

    def test_cut_duration_attribute_will_be_updated_when_cut_in_attribute_changed(self):
        """testing if the cut_duration attribute will be updated when the
        cut_in attribute changed
        """
        self.test_shot.cut_in = 1
        self.assertEqual(
            self.test_shot.cut_duration,
            self.test_shot.cut_out -
            self.test_shot.cut_in + 1
        )

    def test_cut_duration_attribute_will_be_updated_when_cut_out_attribute_changed(self):
        """testing if the cut_duration attribute will be updated when the
        cut_out attribute changed
        """
        self.test_shot.cut_out = 1000
        self.assertEqual(self.test_shot.cut_duration,
                         self.test_shot.cut_out - \
                         self.test_shot.cut_in + 1)

    def test_cut_duration_attribute_changes_cut_out_attribute(self):
        """testing if changes in cut_duration attribute will also affect
        cut_out value.
        """
        first_cut_out = self.test_shot.cut_out
        self.test_shot.cut_duration = 245
        self.assertNotEquals(self.test_shot.cut_out, first_cut_out)
        self.assertEqual(
            self.test_shot.cut_out,
            self.test_shot.cut_in + self.test_shot.cut_duration - 1
        )

    def test_cut_duration_attribute_is_zero(self):
        """testing if the cut_duration attribute will be set to 1 and the
        cut_out is updated to the same value with cut_in when the cut_duration
        attribute is set to zero
        """
        self.test_shot.cut_duration = 0
        self.assertEqual(self.test_shot.cut_out,
                         self.test_shot.cut_in)
        self.assertEqual(self.test_shot.cut_duration, 1)

    def test_cut_duration_attribute_is_negative(self):
        """testing if the cut_duration attribute will be set to 1  and the
        cut_out is updated to the same value with cut_in when the cut_duration
        attribute is set to a negative value
        """
        self.test_shot.cut_duration = -100
        self.assertEqual(self.test_shot.cut_out,
                         self.test_shot.cut_in)
        self.assertEqual(self.test_shot.cut_duration, 1)

    def test_cut_duration_argument_is_zero_and_cut_out_argument_is_skipped(self):
        """testing if the cut_duration attribute will be set to 1 and the
        cut_out is updated to the same value with cut_in when the cut_duration
        argument is zero and there is no cut_out argument given
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = 0
        self.kwargs.pop("cut_out")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, 1)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)

    def test_cut_duration_argument_is_negative_and_cut_out_argument_is_skipped(self):
        """testing if the cut_duration attribute is going to be set to 1 and
        the cut_out will be updated to the same value with the cut_in attribute
        when the cut_duration argument is given as zero and the cut_out
        argument is skipped
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = -10
        self.kwargs.pop("cut_out")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, 1)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)

    def test_cut_duration_argument_is_zero_and_cut_out_argument_is_not_None(self):
        """testing if the cut_duration attribute is going to be set to 1 and
        cut_output will be calculated from cut_in and cut_duration when the
        cut_duration argument is given as zero and there is a cut_out argument
        given
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = 0
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, 1)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)

    def test_cut_duration_argument_is_negative_and_cut_out_argument_is_not_None(self):
        """testing if the cut_duration attribute is going to be set to 1 and
        cut_output will be calculated from cut_in and cut_duration when the
        cut_duration argument is given as negative and there is a cut_out
        argument given
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = -100
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, 1)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)

    def test_image_format_argument_is_skipped(self):
        """testing if the image_format is copied from the Project instance when
        the image_format argument is skipped
        """
        self.kwargs.pop('image_format')
        self.kwargs['code'] = 'TestShot'
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.image_format,
                         self.kwargs['project'].image_format)

    def test_image_format_argument_is_None(self):
        """testing if the image format is copied from the Project instance when
        the image_format argument is None
        """
        self.kwargs['image_format'] = None
        self.kwargs['code'] = 'newShot'
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.image_format,
                         self.kwargs['project'].image_format)

    def test_image_format_attribute_is_None(self):
        """testing if the image format is copied from the Project instance when
        the image_format attribute is set to None
        """
        # test start conditions
        self.assertNotEqual(self.test_shot.image_format,
                            self.test_shot.project.image_format)
        self.test_shot.image_format = None
        self.assertEqual(self.test_shot.image_format,
                         self.test_shot.project.image_format)

    def test_image_format_argument_is_not_a_ImageFormat_instance_and_not_None(self):
        """testing if a TypeError will be raised when the image_format argument
        is not a ImageFormat instance and not None
        """
        self.kwargs['code'] = 'new_shot'
        self.kwargs['image_format'] = 'not an image format instance'
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_image_format_attribute_is_not_a_ImageFormat_instance_and_not_None(self):
        """testing if a TypeError will be raised when the image_format
        attribute is not a ImageFormat instance and not None
        """
        self.assertRaises(TypeError, setattr, self.test_shot, 'not an image f')

    def test_image_format_argument_is_working_properly(self):
        """testing if the image_format argument value is passed to the
        image_format attribute correctly
        """
        self.assertEqual(self.kwargs['image_format'],
                         self.test_shot.image_format)

    def test_image_format_attribute_is_working_properly(self):
        """testing if the image_format attribute is working properly
        """
        self.assertNotEqual(self.test_shot.image_format,
                            self.test_image_format1)
        self.test_shot.image_format = self.test_image_format1
        self.assertEqual(self.test_shot.image_format,
                         self.test_image_format1)

    def test_equality(self):
        """testing equality of shot objects
        """
        self.kwargs["code"] = "SH123A"
        new_shot1 = Shot(**self.kwargs)

        self.kwargs["project"] = self.test_project2
        new_shot2 = Shot(**self.kwargs)
        # an entity with the same parameters
        # just set the name to the code too
        self.kwargs["name"] = self.kwargs["code"]
        new_entity = Entity(**self.kwargs)

        # another shot with different code
        self.kwargs["code"] = "SHAnotherShot"
        new_shot3 = Shot(**self.kwargs)

        self.assertFalse(new_shot1 == new_shot2)
        self.assertFalse(new_shot1 == new_entity)
        self.assertFalse(new_shot1 == new_shot3)

    def test_inequality(self):
        """testing inequality of shot objects
        """
        self.kwargs['code'] = 'SH123A'
        new_shot1 = Shot(**self.kwargs)

        self.kwargs['project'] = self.test_project2
        new_shot2 = Shot(**self.kwargs)
        # an entity with the same parameters
        # just set the name to the code too
        self.kwargs['name'] = self.kwargs['code']
        new_entity = Entity(**self.kwargs)

        # another shot with different code
        self.kwargs['code'] = 'SHAnotherShot'
        new_shot3 = Shot(**self.kwargs)

        self.assertTrue(new_shot1 != new_shot2)
        self.assertTrue(new_shot1 != new_entity)
        self.assertTrue(new_shot1 != new_shot3)

    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """
        link_type_1 = Type(
            name="Image",
            code='image',
            target_entity_type="Link"
        )

        link1 = Link(name="Artwork 1", full_path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="a.jpg", type=link_type_1)

        link2 = Link(name="Artwork 2", full_path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="b.jbg", type=link_type_1)

        references = [link1, link2]

        self.kwargs["code"] = "SH12314"
        self.kwargs["references"] = references

        new_shot = Shot(**self.kwargs)

        self.assertEqual(new_shot.references, references)

    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Complete", code="CMPLT")

        status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2],
            target_entity_type=Shot
        )

        self.kwargs["code"] = "SH12314"
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list

        new_shot = Shot(**self.kwargs)

        self.assertEqual(new_shot.status_list, status_list)

    def test_TaskMixin_initialization(self):
        """testing if the TaskMixin part is initialized correctly
        """
        status1 = Status(name="On Hold", code="OH")

        task_status_list = StatusList(name="Task Statuses",
                                      statuses=[status1],
                                      target_entity_type=Task)

        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1],
            target_entity_type=Project
        )

        project_type = Type(
            name="Commercial",
            code='comm',
            target_entity_type=Project
        )

        new_project = Project(
            name="Commercial1",
            code='comm1',
            status_list=project_status_list,
            type=project_type,
            repository=self.test_repository,
        )

        self.kwargs["code"] = "SH12314"

        new_shot = Shot(**self.kwargs)

        task1 = Task(
            name="Modeling", status=0,
            status_list=task_status_list,
            project=new_project,
            parent=new_shot,
        )

        task2 = Task(
            name="Lighting",
            status=0,
            status_list=task_status_list,
            project=new_project,
            parent=new_shot,
        )

        tasks = [task1, task2]

        self.assertItemsEqual(new_shot.tasks, tasks)

    def test__repr__(self):
        """testing the represantation of Shot
        """
        self.assertEqual(
            self.test_shot.__repr__(),
            "<Shot (%s, %s)>" % (self.test_shot.code,
                                 self.test_shot.code)
        )

    def test_plural_class_name(self):
        """testing the plural name of Shot class
        """
        self.assertTrue(self.test_shot.plural_class_name, "Shots")

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ class attribute is False for
        Shot class
        """
        self.assertEqual(Shot.__strictly_typed__, False)
