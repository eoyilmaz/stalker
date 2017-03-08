# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
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

from stalker.testing import UnitTestBase
from stalker import Shot


class ShotTester(UnitTestBase):
    """Tests the Shot class
    """

    def setUp(self):
        """setup the test
        """
        super(ShotTester, self).setUp()
        # statuses
        from stalker import db, Status, StatusList
        self.status_new = Status.query.filter_by(code='NEW').first()
        self.status_wfd = Status.query.filter_by(code='WFD').first()
        self.status_rts = Status.query.filter_by(code='RTS').first()
        self.status_wip = Status.query.filter_by(code='WIP').first()
        self.status_prev = Status.query.filter_by(code='PREV').first()
        self.status_hrev = Status.query.filter_by(code='HREV').first()
        self.status_drev = Status.query.filter_by(code='DREV').first()
        self.status_oh = Status.query.filter_by(code='OH').first()
        self.status_stop = Status.query.filter_by(code='STOP').first()
        self.status_cmpl = Status.query.filter_by(code='CMPL').first()

        self.test_sequence_status_list = \
            StatusList.query.filter_by(target_entity_type='Sequence').first()

        self.test_shot_status_list = \
            StatusList.query.filter_by(target_entity_type='Shot').first()

        self.test_asset_status_list = \
            StatusList.query.filter_by(target_entity_type='Asset').first()

        # status lists
        self.test_project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.status_new,
                self.status_wip,
                self.status_cmpl
            ],
            target_entity_type='Project',
        )
        db.DBSession.add(self.test_project_status_list)

        # types
        from stalker import Type
        self.test_commercial_project_type = Type(
            name="Commercial Project",
            code='comm',
            target_entity_type='Project',
        )
        db.DBSession.add(self.test_commercial_project_type)

        self.test_character_asset_type = Type(
            name="Character",
            code='char',
            target_entity_type='Asset',
        )
        db.DBSession.add(self.test_character_asset_type)

        self.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type='Repository'
        )
        db.DBSession.add(self.test_repository_type)

        # repository
        from stalker import Repository
        self.test_repository = Repository(
            name="Test Repository",
            type=self.test_repository_type,
        )
        db.DBSession.add(self.test_repository)

        # image format
        from stalker import ImageFormat
        self.test_image_format1 = ImageFormat(
            name='Test Image Format 1',
            width=1920,
            height=1080,
            pixel_aspect=1.0
        )
        db.DBSession.add(self.test_image_format1)

        self.test_image_format2 = ImageFormat(
            name='Test Image Format 2',
            width=1280,
            height=720,
            pixel_aspect=1.0
        )
        db.DBSession.add(self.test_image_format2)

        # project and sequences
        from stalker import Project
        self.test_project1 = Project(
            name='Test Project1',
            code='tp1',
            type=self.test_commercial_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repository,
            image_format=self.test_image_format1
        )
        db.DBSession.add(self.test_project1)

        self.test_project2 = Project(
            name='Test Project2',
            code='tp2',
            type=self.test_commercial_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repository,
            image_format=self.test_image_format1
        )
        db.DBSession.add(self.test_project2)

        from stalker import Sequence
        self.test_sequence1 = Sequence(
            name="Test Seq1",
            code='ts1',
            project=self.test_project1,
            status_list=self.test_sequence_status_list,
        )
        db.DBSession.add(self.test_sequence1)

        self.test_sequence2 = Sequence(
            name="Test Seq2",
            code='ts2',
            project=self.test_project1,
            status_list=self.test_sequence_status_list,
        )
        db.DBSession.add(self.test_sequence2)

        self.test_sequence3 = Sequence(
            name="Test Seq3",
            code='ts3',
            project=self.test_project1,
            status_list=self.test_sequence_status_list,
        )
        db.DBSession.add(self.test_sequence3)

        from stalker import Scene
        self.test_scene1 = Scene(
            name='Test Sce1',
            code='tsc1',
            project=self.test_project1,
        )
        db.DBSession.add(self.test_scene1)

        self.test_scene2 = Scene(
            name='Test Sce2',
            code='tsc2',
            project=self.test_project1,
        )
        db.DBSession.add(self.test_scene2)

        self.test_scene3 = Scene(
            name='Test Sce3',
            code='tsc3',
            project=self.test_project1
        )
        db.DBSession.add(self.test_scene3)

        from stalker import Asset
        self.test_asset1 = Asset(
            name="Test Asset1",
            code='ta1',
            project=self.test_project1,
            status_list=self.test_asset_status_list,
            type=self.test_character_asset_type,
        )
        db.DBSession.add(self.test_asset1)

        self.test_asset2 = Asset(
            name="Test Asset2",
            code='ta2',
            project=self.test_project1,
            status_list=self.test_asset_status_list,
            type=self.test_character_asset_type,
        )
        db.DBSession.add(self.test_asset2)

        self.test_asset3 = Asset(
            name="Test Asset3",
            code='ta3',
            project=self.test_project1,
            status_list=self.test_asset_status_list,
            type=self.test_character_asset_type,
        )
        db.DBSession.add(self.test_asset3)

        self.kwargs = dict(
            name='SH123',
            code='SH123',
            description='This is a test Shot',
            project=self.test_project1,
            sequences=[self.test_sequence1, self.test_sequence2],
            scenes=[self.test_scene1, self.test_scene2],
            cut_in=112,
            cut_out=149,
            source_in=120,
            source_out=140,
            record_in=85485,
            status=0,
            status_list=self.test_shot_status_list,
            image_format=self.test_image_format2
        )

        # create a mock shot object
        self.test_shot = Shot(**self.kwargs)
        db.DBSession.add(self.test_project1)
        db.DBSession.commit()

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
        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.project should be an instance of '
            'stalker.models.project.Project, not NoneType. Or please supply a '
            'stalker.models.task.Task with the parent argument, so Stalker '
            'can use the project of the supplied parent task'
        )

    def test_project_argument_is_None(self):
        """testing if a TypeError will be raised when the project argument is
        None
        """
        self.kwargs["project"] = None

        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.project should be an instance of '
            'stalker.models.project.Project, not NoneType. Or please supply a '
            'stalker.models.task.Task with the parent argument, so Stalker '
            'can use the project of the supplied parent task'
        )

    def test_project_argument_is_not_Project_instance(self):
        """testing if a TypeError will be raised when the given sequence
        argument is not a Project instance
        """
        test_values = [1, 1.2, "project", ["a", "project"]]
        for test_value in test_values:
            self.kwargs["project"] = test_value
            with self.assertRaises(TypeError) as cm:
                Shot(self.kwargs)

    def test_project_already_has_a_shot_with_the_same_code(self):
        """testing if a ValueError will be raised when the given project
        argument already has a shot with the same code
        """
        # lets try to assign the shot to the same sequence2 which has another
        # shot with the same code
        self.assertEqual(
            self.kwargs['code'],
            self.test_shot.code
        )
        with self.assertRaises(ValueError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'There is a Shot with the same code: SH123'
        )

        # this should not raise a ValueError
        self.kwargs["code"] = "DifferentCode"
        new_shot2 = Shot(**self.kwargs)
        self.assertTrue(isinstance(new_shot2, Shot))

    def test_code_attribute_is_set_to_the_same_value(self):
        """testing if a ValueError will NOT be raised when the shot.code is set
        to the same value
        """
        self.test_shot.code = self.test_shot.code

    def test_project_attribute_is_read_only(self):
        """testing if the project attribute is read only
        """
        with self.assertRaises(AttributeError) as cm:
            self.test_shot.project = self.test_project2

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_project_contains_shots(self):
        """testing if the current shot is going to be added to the Project, so
        the Project.shots list will contain the current shot
        """
        self.assertTrue(self.test_shot in self.test_shot.project.shots)

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
        with self.assertRaises(TypeError) as cm:
            self.test_shot.sequences = None

    def test_sequences_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the sequences argument is
        not a list
        """
        self.kwargs['sequences'] = 'not a list'
        self.kwargs['code'] = 'NewCode'
        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

    def test_sequences_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the sequences attribute
        is not a list
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.sequences = 'not a list'

    def test_sequences_argument_is_not_a_list_of_Sequence_instances(self):
        """testing if a TypeError will be raised when the sequences argument is
        not a list of Sequences
        """
        self.kwargs['sequences'] = ['not', 1, 'list', 'of', 'sequences']
        self.kwargs['code'] = 'NewShot'
        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

    def test_sequences_attribute_is_not_a_list_of_Sequence_instances(self):
        """testing if a TypeError will be raised when the sequences attribute
        is not a list of Sequence instances
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.sequences = ['not', 1, 'list', 'of', 'sequences']

    def test_sequences_argument_is_working_properly(self):
        """testing if the sequences attribute is working properly
        """
        self.kwargs['code'] = 'NewShot'
        from stalker import Sequence
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

        self.assertEqual(
            sorted(new_shot.sequences, key=lambda x: x.name),
            sorted(seqs, key=lambda x: x.name)
        )

    def test_sequences_attribute_is_working_properly(self):
        """testing if the sequences attribute is working properly
        """
        self.kwargs['code'] = 'NewShot'

        from stalker import Sequence
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
        self.assertEqual(
            sorted(new_shot.sequences, key=lambda x: x.name),
            sorted(seqs, key=lambda x: x.name)
        )

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
        with self.assertRaises(TypeError) as cm:
            self.test_shot.scenes = None

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: None is not list-like'
        )

    def test_scenes_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the scenes argument is
        not a list
        """
        self.kwargs['scenes'] = 'not a list'
        self.kwargs['code'] = 'NewCode'
        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_scenes_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the scenes attribute
        is not a list
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.scenes = 'not a list'

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_scenes_argument_is_not_a_list_of_Scene_instances(self):
        """testing if a TypeError will be raised when the scenes argument is
        not a list of Scenes
        """
        self.kwargs['scenes'] = ['not', 1, 'list', 'of', 'scenes']
        self.kwargs['code'] = 'NewShot'
        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.scenes should all be stalker.models.scene.Scene instances, '
            'not str'
        )

    def test_scenes_attribute_is_not_a_list_of_Scene_instances(self):
        """testing if a TypeError will be raised when the scenes attribute
        is not a list of Scene instances
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.scenes = ['not', 1, 'list', 'of', 'scenes']

        self.assertEqual(
            str(cm.exception),
            'Shot.scenes should all be stalker.models.scene.Scene '
            'instances, not str'
        )

    def test_scenes_argument_is_working_properly(self):
        """testing if the scenes attribute is working properly
        """
        from stalker import Scene
        self.kwargs['code'] = 'NewShot'
        sce1 = Scene(name='sce1', code='sce1', project=self.test_project1)
        sce2 = Scene(name='sce2', code='sce2', project=self.test_project1)
        sce3 = Scene(name='sce3', code='sce3', project=self.test_project1)

        seqs = [sce1, sce2, sce3]
        self.kwargs['scenes'] = seqs
        new_shot = Shot(**self.kwargs)

        self.assertEqual(
            sorted(new_shot.scenes, key=lambda x: x.name),
            sorted(seqs, key=lambda x: x.name)
        )

    def test_scenes_attribute_is_working_properly(self):
        """testing if the scenes attribute is working properly
        """
        from stalker import Scene
        self.kwargs['code'] = 'NewShot'

        sce1 = Scene(name='sce1', code='sce1', project=self.test_project1)
        sce2 = Scene(name='sce2', code='sce2', project=self.test_project1)
        sce3 = Scene(name='sce3', code='sce3', project=self.test_project1)

        new_shot = Shot(**self.kwargs)

        new_shot.scenes = [sce1]
        new_shot.scenes.append(sce2)
        new_shot.scenes.append(sce3)

        seqs = [sce1, sce2, sce3]
        self.assertEqual(
            sorted(new_shot.scenes, key=lambda x: x.name),
            sorted(seqs, key=lambda x: x.name)
        )

    def test_cut_in_argument_is_skipped(self):
        """testing if the cut_in argument is skipped the cut_in argument will
        be calculated from cut_out argument
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_in")
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_out, self.kwargs['cut_out'])
        self.assertEqual(new_shot.cut_in, new_shot.cut_out)

    def test_cut_in_argument_is_none(self):
        """testing if the cut_in attribute value will be calculated from the
        cut_out attribute value if the cut_in argument is None
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = None
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        shot = Shot(**self.kwargs)
        self.assertEqual(shot.cut_out, self.kwargs['cut_out'])
        self.assertEqual(shot.cut_in, shot.cut_out)

    def test_cut_in_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised when the cut_in attribute is
        set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.cut_in = None

        self.assertEqual(
            str(cm.exception),
            'Shot.cut_in should be an int, not NoneType'
        )

    def test_cut_in_argument_is_not_integer(self):
        """testing if a TypeError will be raised if the cut_in argument is not
        an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = "a string"

        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.cut_in should be an int, not str'
        )

    def test_cut_in_attribute_is_not_integer(self):
        """testing if a TypeError will be raised if the cut_in attribute is set
        to a value other than an integer
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.cut_in = 'a string'

        self.assertEqual(
            str(cm.exception),
            'Shot.cut_in should be an int, not str'
        )

    def test_cut_in_argument_is_bigger_than_cut_out_argument(self):
        """testing if a cut_out will be offset when the cut_in argument
        value is bigger than the cut_out argument value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = self.kwargs["cut_out"] + 10
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        shot = Shot(**self.kwargs)
        self.assertEqual(shot.cut_in, 149)
        self.assertEqual(shot.cut_out, 149)

    def test_cut_in_attribute_is_bigger_than_cut_out_attribute(self):
        """testing if a the cut_out attribute value will be offset when the
        cut_in attribute is set bigger than cut_out attribute value
        """
        self.test_shot.cut_in = self.test_shot.cut_out + 10
        self.assertEqual(self.test_shot.cut_in, 159)
        self.assertEqual(self.test_shot.cut_out, self.test_shot.cut_in)

    def test_cut_out_argument_is_skipped(self):
        """testing if the cut_out attribute will be calculated from cut_in
        argument value when the cut_out argument is skipped
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_out")
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_in, self.kwargs['cut_in'])
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)

    def test_cut_out_argument_is_set_to_none(self):
        """testing if the cut_out argument is set to None the cut_out attribute
        will be calculated from cut_in argument value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = None
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None

        shot = Shot(**self.kwargs)
        self.assertEqual(shot.cut_in, self.kwargs['cut_in'])
        self.assertEqual(shot.cut_out, shot.cut_in)

    def test_cut_out_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised if the cut_out attribute is
        set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.cut_out = None
        self.assertEqual(
            str(cm.exception),
            'Shot.cut_out should be an int, not NoneType'
        )

    def test_cut_out_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the cut_out argument is
        not an integer
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = "a string"
        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.cut_out should be an int, not str'
        )

    def test_cut_out_attribute_is_not_integer(self):
        """testing if a TypeError will be raised if the cut_out attribute is
        set to a value other than an integer
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.cut_out = "a string"
        self.assertEqual(
            str(cm.exception),
            'Shot.cut_out should be an int, not str'
        )

    def test_cut_out_argument_is_smaller_than_cut_in_argument(self):
        """testing if the cut_out attribute is updated when the cut_out
        argument is smaller than cut_in argument
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = self.kwargs["cut_in"] - 10
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        shot = Shot(**self.kwargs)
        self.assertEqual(shot.cut_in, 102)
        self.assertEqual(shot.cut_out, 102)

    def test_cut_out_attribute_is_smaller_than_cut_in_attribute(self):
        """testing if the cut_out attribute is updated when it is smaller than
        cut_in attribute
        """
        self.test_shot.cut_out = self.test_shot.cut_in - 10
        self.assertEqual(self.test_shot.cut_in, 102)
        self.assertEqual(self.test_shot.cut_out, 102)

    def test_cut_duration_attribute_is_not_instance_of_int(self):
        """testing if a TypeError will be raised when the cut_duration
        attribute is set to a value other than an integer
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.cut_duration = "a string"

        self.assertEqual(
            str(cm.exception),
            'Shot.cut_duration should be a positive integer value, not '
            'str'
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
-        cut_out value.
        """
        first_cut_out = self.test_shot.cut_out
        self.test_shot.cut_duration = 245
        self.assertNotEquals(self.test_shot.cut_out, first_cut_out)
        self.assertEqual(
            self.test_shot.cut_out,
            self.test_shot.cut_in + self.test_shot.cut_duration - 1
        )

    def test_cut_duration_attribute_is_zero(self):
        """testing if a ValueError will be raised when the cut_duration
        attribute is set to zero
        """
        with self.assertRaises(ValueError) as cm:
            self.test_shot.cut_duration = 0

        self.assertEqual(
            str(cm.exception),
            'Shot.cut_duration can not be set to zero or a negative value'
        )

    def test_cut_duration_attribute_is_negative(self):
        """testing if a ValueError will be raised when the cut_duration
        attribute is set to a negative value
        """
        with self.assertRaises(ValueError) as cm:
            self.test_shot.cut_duration = -100

        self.assertEqual(
            str(cm.exception),
            'Shot.cut_duration can not be set to zero or a negative value'
        )

    def test_source_in_argument_is_skipped(self):
        """testing if the source_in argument is skipped the source_in argument
        will be equal to cut_in attribute value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop('source_in')
        shot = Shot(**self.kwargs)
        self.assertEqual(shot.source_in, shot.cut_in)

    def test_source_in_argument_is_none(self):
        """testing if the source_in attribute value will be equal to the cut_in
        attribute value when the source_in argument is None
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_in"] = None
        shot = Shot(**self.kwargs)
        self.assertEqual(shot.source_in, shot.cut_in)

    def test_source_in_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised when the source_in attribute
        is set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.source_in = None

        self.assertEqual(
            str(cm.exception),
            'Shot.source_in should be an int, not NoneType'
        )

    def test_source_in_argument_is_not_integer(self):
        """testing if a TypeError will be raised if the source_in argument is
        not an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_in"] = "a string"

        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.source_in should be an int, not str'
        )

    def test_source_in_attribute_is_not_integer(self):
        """testing if a TypeError will be raised if the source_in attribute is
        set to a value other than an integer
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.source_in = 'a string'

        self.assertEqual(
            str(cm.exception),
            'Shot.source_in should be an int, not str'
        )

    def test_source_in_argument_is_bigger_than_source_out_argument(self):
        """testing if a ValueError will be raised when the source_in argument
        value is set to bigger than source_out argument value
        """
        self.kwargs['code'] = 'SH123A'
        self.kwargs['source_out'] = self.kwargs['cut_out'] - 10
        self.kwargs['source_in'] = self.kwargs['source_out'] + 5
        with self.assertRaises(ValueError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.source_out can not be smaller than Shot.source_in, '
            'source_in: 144 where as source_out: 139'
        )

    def test_source_in_attribute_is_bigger_than_source_out_attribute(self):
        """testing if a ValueError will be raised when the source_ni attribute
        value is set to bigger than source out
        """
        # give it a little bit of room, to be sure that the ValueError is not
        # due to the cut_out
        self.test_shot.source_out -= 5
        with self.assertRaises(ValueError) as cm:
            self.test_shot.source_in = self.test_shot.source_out + 1

        self.assertEqual(
            str(cm.exception),
            'Shot.source_in can not be bigger than Shot.source_out, '
            'source_in: 136 where as source_out: 135'
        )

    def test_source_in_argument_is_smaller_than_cut_in(self):
        """testing if a ValueError will be raised when the source_in argument
        value is smaller than cut_in attribute value
        """
        self.kwargs['code'] = 'SH123A'
        self.kwargs['source_in'] = self.kwargs['cut_in'] - 10
        with self.assertRaises(ValueError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.source_in can not be smaller than Shot.cut_in, cut_in: 112 '
            'where as source_in: 102'
        )

    def test_source_in_argument_is_bigger_than_cut_out(self):
        """testing if a ValueError will be raised when the source_in argument
        value is bigger than cut_out attribute value
        """
        self.kwargs['code'] = 'SH123A'
        self.kwargs['source_in'] = self.kwargs['cut_out'] + 10
        with self.assertRaises(ValueError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.source_in can not be bigger than Shot.cut_out, cut_out: 149 '
            'where as source_in: 159'
        )

    def test_source_out_argument_is_skipped(self):
        """testing if the source_out attribute will be equal to cut_out
        argument value when the source_out argument is skipped
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("source_out")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.source_out, new_shot.cut_out)

    def test_source_out_argument_is_none(self):
        """testing if the source_out attribute value will be equal to cut_out
        if the source_out argument value is None
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_out"] = None

        shot = Shot(**self.kwargs)
        self.assertEqual(shot.source_out, shot.cut_out)

    def test_source_out_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised if the source_out attribute is
        set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.source_out = None
        self.assertEqual(
            str(cm.exception),
            'Shot.source_out should be an int, not NoneType'
        )

    def test_source_out_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the source_out argument
        is not an integer
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_out"] = "a string"
        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.source_out should be an int, not str'
        )

    def test_source_out_attribute_is_not_integer(self):
        """testing if a TypeError will be raised if the source_out attribute is
        set to a value other than an integer
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.source_out = "a string"
        self.assertEqual(
            str(cm.exception),
            'Shot.source_out should be an int, not str'
        )

    def test_source_out_argument_is_smaller_than_source_in_argument(self):
        """testing if a ValueError will be raised when the source_out argument
        is smaller than the source_in attibute value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_in"] = self.kwargs['cut_in'] + 15
        self.kwargs["source_out"] = self.kwargs["source_in"] - 10
        with self.assertRaises(ValueError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.source_out can not be smaller than Shot.source_in, '
            'source_in: 127 where as source_out: 117'
        )

    def test_source_out_attribute_is_smaller_than_source_in_attribute(self):
        """testing if a ValueError will be raised when the source_out attribute
        is set to a value smaller than source_in
        """
        with self.assertRaises(ValueError) as cm:
            self.test_shot.source_out = self.test_shot.source_in - 2

        self.assertEqual(
            str(cm.exception),
            'Shot.source_out can not be smaller than Shot.source_in, '
            'source_in: 120 where as source_out: 118'
        )

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
        with self.assertRaises(TypeError) as cm:
            Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.image_format should be an instance of '
            'stalker.models.format.ImageFormat, not str'
        )

    def test_image_format_attribute_is_not_a_ImageFormat_instance_and_not_None(self):
        """testing if a TypeError will be raised when the image_format
        attribute is not a ImageFormat instance and not None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_shot.image_format = 'not an image f'

        self.assertEqual(
            str(cm.exception),
            'Shot.image_format should be an instance of '
            'stalker.models.format.ImageFormat, not str'
        )

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
        from stalker import Entity
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
        from stalker import Entity
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
        from stalker import Type, Link
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

    def test_TaskMixin_initialization(self):
        """testing if the TaskMixin part is initialized correctly
        """
        from stalker import Status, StatusList
        status1 = Status(name="On Hold", code="OH")

        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1],
            target_entity_type='Project'
        )

        from stalker import Type
        project_type = Type(
            name="Commercial",
            code='comm',
            target_entity_type='Project'
        )

        from stalker import Project
        new_project = Project(
            name="Commercial1",
            code='comm1',
            status_list=project_status_list,
            type=project_type,
            repository=self.test_repository,
        )

        self.kwargs["code"] = "SH12314"

        from stalker import Task
        new_shot = Shot(**self.kwargs)

        task1 = Task(
            name="Modeling", status=0,
            project=new_project,
            parent=new_shot,
        )

        task2 = Task(
            name="Lighting",
            status=0,
            project=new_project,
            parent=new_shot,
        )

        tasks = [task1, task2]

        self.assertEqual(
            sorted(new_shot.tasks, key=lambda x: x.name),
            sorted(tasks, key=lambda x: x.name)
        )

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

    def test_fps_argument_is_skipped(self):
        """testing if the default value will be used when fps is skipped
        """
        if 'fps' in self.kwargs:
            self.kwargs.pop("fps")

        self.kwargs['code'] = 'SHnew'
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.fps, self.test_project1.fps)

    def test_fps_attribute_is_set_to_None(self):
        """testing if the Project.fps will be used if the fps argument is None
        """
        self.kwargs["fps"] = None
        self.kwargs['code'] = 'SHnew'
        new_shot = Shot(**self.kwargs)

        self.assertEqual(new_shot.fps, self.test_project1.fps)

    def test_fps_argument_is_given_as_non_float_or_integer(self):
        """testing if a TypeError will be raised when the fps argument is
        given as a value other than a float or integer, or a string which is
        convertible to float.
        """
        test_values = [["a", "list"], {"a": "list"}]
        for i, test_value in enumerate(test_values):
            self.kwargs["fps"] = test_value
            self.kwargs['code'] = 'SH%i'
            with self.assertRaises(TypeError) as cm:
                s = Shot(**self.kwargs)

            self.assertEqual(
                str(cm.exception),
                'Shot.fps should be a positive float or int, not %s' %
                test_value.__class__.__name__
            )

    def test_fps_attribute_is_given_as_non_float_or_integer(self):
        """testing if a TypeError will be raised when the fps attribute is
        set to a value other than a float, integer or valid string literals
        """
        test_values = ["a str", ["a", "list"], {"a": "list"}]
        for test_value in test_values:
            with self.assertRaises(TypeError) as cm:
                self.test_shot.fps = test_value

            self.assertEqual(
                str(cm.exception),
                'Shot.fps should be a positive float or int, not %s' %
                test_value.__class__.__name__
            )

    def test_fps_attribute_float_conversion(self):
        """testing if the fps attribute is converted to float when the float
        argument is given as an integer
        """
        test_value = 1
        self.kwargs["fps"] = test_value
        self.kwargs['code'] = 'SHnew'
        new_shot = Shot(**self.kwargs)
        self.assertIsInstance(new_shot.fps, float)
        self.assertEqual(new_shot.fps, float(test_value))

    def test_fps_attribute_float_conversion_2(self):
        """testing if the fps attribute is converted to float when it is set to
        an integer value
        """
        test_value = 1
        self.test_shot.fps = test_value
        self.assertIsInstance(self.test_shot.fps, float)
        self.assertEqual(self.test_shot.fps, float(test_value))

    def test_fps_argument_is_zero(self):
        """testing if a ValueError will be raised when the fps is 0
        """
        self.kwargs['fps'] = 0
        self.kwargs['code'] = 'SHnew'
        with self.assertRaises(ValueError) as cm:
            s = Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.fps should be a positive float or int, not 0.0'
        )

    def test_fps_attribute_is_set_to_zero(self):
        """testing if a value error will be raised when the fps attribute is
        set to zero
        """
        with self.assertRaises(ValueError) as cm:
            self.test_shot.fps = 0

        self.assertEqual(
            str(cm.exception),
            'Shot.fps should be a positive float or int, not 0.0'
        )

    def test_fps_argument_is_negative(self):
        """testing if a ValueError will be raised when the fps argument is
        negative
        """
        self.kwargs['fps'] = -1.0
        self.kwargs['code'] = 'SHrandom'
        with self.assertRaises(ValueError) as cm:
            s = Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.fps should be a positive float or int, not -1.0'
        )

    def test_fps_attribute_is_negative(self):
        """testing if a ValueError will be raised when the fps attribute is
        set to a negative value
        """
        with self.assertRaises(ValueError) as cm:
            self.test_shot.fps = -1

        self.assertEqual(
            str(cm.exception),
            'Shot.fps should be a positive float or int, not -1.0'
        )

    def test_fps_changes_with_project(self):
        """testing if the fps reflects the project.fps unless it is set to a
        value
        """
        new_shot = Shot(
            name='New Shot',
            code='ns',
            project=self.test_project1
        )
        self.assertEqual(new_shot.fps, self.test_project1.fps)
        self.test_project1.fps = 335
        self.assertEqual(new_shot.fps, 335)
        new_shot.fps = 12
        self.assertEqual(new_shot.fps, 12)
        self.test_project1.fps = 24
        self.assertEqual(new_shot.fps, 12)

    def test_cut_duration_initialization_bug_with_cut_in(self):
        """testing if the _cut_duration attribute is initialized correctly for
        a Shot restored from DB
        """
        # retrieve the shot back from DB
        from stalker import db, Shot
        test_shot_db = Shot.query.filter_by(name=self.kwargs['name']).first()
        # trying to change the cut_in and cut_out values should not raise any
        # errors
        test_shot_db.cut_in = 1
        db.DBSession.add(test_shot_db)
        db.DBSession.commit()

    def test_cut_duration_initialization_bug_with_cut_out(self):
        """testing if the _cut_duration attribute is initialized correctly for
        a Shot restored from DB
        """
        from stalker import db, Shot
        # reconnect to the database
        # retrieve the shot back from DB
        test_shot_db = Shot.query.filter_by(name=self.kwargs['name']).first()
        # trying to change the cut_in and cut_out values should not raise any
        # errors
        test_shot_db.cut_out = 100
        db.DBSession.add(test_shot_db)
        db.DBSession.commit()

    def test_cut_values_are_set_correctly(self):
        """testing if the cut_in attribute is set correctly in db
        """
        self.test_shot.cut_in = 100
        self.assertEqual(self.test_shot.cut_in, 100)

        self.test_shot.cut_out = 153
        self.assertEqual(self.test_shot.cut_in, 100)
        self.assertEqual(self.test_shot.cut_out, 153)

        from stalker import db, Shot
        db.DBSession.add(self.test_shot)
        db.DBSession.commit()

        # retrieve the shot back from DB
        test_shot_db = Shot.query.filter_by(name=self.kwargs['name']).first()

        self.assertEqual(test_shot_db.cut_in, 100)
        self.assertEqual(test_shot_db.cut_out, 153)

    def test_fps_argument_is_skipped(self):
        """testing if the default value will be used when fps is skipped
        """
        if 'fps' in self.kwargs:
            self.kwargs.pop("fps")

        self.kwargs['code'] = 'SHnew'
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.fps, self.test_project1.fps)

    def test_fps_attribute_is_set_to_None(self):
        """testing if the Project.fps will be used if the fps argument is None
        """
        self.kwargs["fps"] = None
        self.kwargs['code'] = 'SHnew'
        new_shot = Shot(**self.kwargs)

        self.assertEqual(new_shot.fps, self.test_project1.fps)

    def test_fps_argument_is_given_as_non_float_or_integer(self):
        """testing if a TypeError will be raised when the fps argument is
        given as a value other than a float or integer, or a string which is
        convertible to float.
        """
        test_values = [["a", "list"], {"a": "list"}]
        for i, test_value in enumerate(test_values):
            self.kwargs["fps"] = test_value
            self.kwargs['code'] = 'SH%i'
            with self.assertRaises(TypeError) as cm:
                s = Shot(**self.kwargs)

            self.assertEqual(
                str(cm.exception),
                'Shot.fps should be a positive float or int, not %s' %
                test_value.__class__.__name__
            )

    def test_fps_attribute_is_given_as_non_float_or_integer(self):
        """testing if a TypeError will be raised when the fps attribute is
        set to a value other than a float, integer or valid string literals
        """
        test_values = ["a str", ["a", "list"], {"a": "list"}]
        for test_value in test_values:
            with self.assertRaises(TypeError) as cm:
                self.test_shot.fps = test_value

            self.assertEqual(
                str(cm.exception),
                'Shot.fps should be a positive float or int, not %s' %
                test_value.__class__.__name__
            )

    def test_fps_attribute_float_conversion(self):
        """testing if the fps attribute is converted to float when the float
        argument is given as an integer
        """
        test_value = 1
        self.kwargs["fps"] = test_value
        self.kwargs['code'] = 'SHnew'
        new_shot = Shot(**self.kwargs)
        self.assertIsInstance(new_shot.fps, float)
        self.assertEqual(new_shot.fps, float(test_value))

    def test_fps_attribute_float_conversion_2(self):
        """testing if the fps attribute is converted to float when it is set to
        an integer value
        """
        test_value = 1
        self.test_shot.fps = test_value
        self.assertIsInstance(self.test_shot.fps, float)
        self.assertEqual(self.test_shot.fps, float(test_value))

    def test_fps_argument_is_zero(self):
        """testing if a ValueError will be raised when the fps is 0
        """
        self.kwargs['fps'] = 0
        self.kwargs['code'] = 'SHnew'
        with self.assertRaises(ValueError) as cm:
            s = Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.fps should be a positive float or int, not 0.0'
        )

    def test_fps_attribute_is_set_to_zero(self):
        """testing if a value error will be raised when the fps attribute is
        set to zero
        """
        with self.assertRaises(ValueError) as cm:
            self.test_shot.fps = 0

        self.assertEqual(
            str(cm.exception),
            'Shot.fps should be a positive float or int, not 0.0'
        )

    def test_fps_argument_is_negative(self):
        """testing if a ValueError will be raised when the fps argument is
        negative
        """
        self.kwargs['fps'] = -1.0
        self.kwargs['code'] = 'SHrandom'
        with self.assertRaises(ValueError) as cm:
            s = Shot(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Shot.fps should be a positive float or int, not -1.0'
        )

    def test_fps_attribute_is_negative(self):
        """testing if a ValueError will be raised when the fps attribute is
        set to a negative value
        """
        with self.assertRaises(ValueError) as cm:
            self.test_shot.fps = -1

        self.assertEqual(
            str(cm.exception),
            'Shot.fps should be a positive float or int, not -1.0'
        )

    def test_fps_changes_with_project(self):
        """testing if the fps reflects the project.fps unless it is set to a
        value
        """
        new_shot = Shot(
            name='New Shot',
            code='ns',
            project=self.test_project1
        )
        self.assertEqual(new_shot.fps, self.test_project1.fps)
        self.test_project1.fps = 335
        self.assertEqual(new_shot.fps, 335)
        new_shot.fps = 12
        self.assertEqual(new_shot.fps, 12)
        self.test_project1.fps = 24
        self.assertEqual(new_shot.fps, 12)
