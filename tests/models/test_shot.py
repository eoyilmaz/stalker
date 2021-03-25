# -*- coding: utf-8 -*-

import pytest
from stalker.testing import UnitTestDBBase
from stalker import Shot


class ShotTester(UnitTestDBBase):
    """Tests the Shot class
    """

    def setUp(self):
        """setup the test
        """
        super(ShotTester, self).setUp()
        # statuses
        # types
        from stalker.db.session import DBSession
        from stalker import Type
        self.test_commercial_project_type = Type(
            name="Commercial Project",
            code='comm',
            target_entity_type='Project',
        )
        DBSession.add(self.test_commercial_project_type)

        self.test_character_asset_type = Type(
            name="Character",
            code='char',
            target_entity_type='Asset',
        )
        DBSession.add(self.test_character_asset_type)

        self.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type='Repository'
        )
        DBSession.add(self.test_repository_type)

        # repository
        from stalker import Repository
        self.test_repository = Repository(
            name="Test Repository",
            code="TR",
            type=self.test_repository_type,
        )
        DBSession.add(self.test_repository)

        # image format
        from stalker import ImageFormat
        self.test_image_format1 = ImageFormat(
            name='Test Image Format 1',
            width=1920,
            height=1080,
            pixel_aspect=1.0
        )
        DBSession.add(self.test_image_format1)

        self.test_image_format2 = ImageFormat(
            name='Test Image Format 2',
            width=1280,
            height=720,
            pixel_aspect=1.0
        )
        DBSession.add(self.test_image_format2)

        # project and sequences
        from stalker import Project
        self.test_project1 = Project(
            name='Test Project1',
            code='tp1',
            type=self.test_commercial_project_type,
            repository=self.test_repository,
            image_format=self.test_image_format1
        )
        DBSession.add(self.test_project1)
        DBSession.commit()

        self.test_project2 = Project(
            name='Test Project2',
            code='tp2',
            type=self.test_commercial_project_type,
            repository=self.test_repository,
            image_format=self.test_image_format1
        )
        DBSession.add(self.test_project2)
        DBSession.commit()

        from stalker import Sequence
        self.test_sequence1 = Sequence(
            name="Test Seq1",
            code='ts1',
            project=self.test_project1,
        )
        DBSession.add(self.test_sequence1)
        DBSession.commit()

        self.test_sequence2 = Sequence(
            name="Test Seq2",
            code='ts2',
            project=self.test_project1,
        )
        DBSession.add(self.test_sequence2)
        DBSession.commit()

        self.test_sequence3 = Sequence(
            name="Test Seq3",
            code='ts3',
            project=self.test_project1,
        )
        DBSession.add(self.test_sequence3)
        DBSession.commit()

        from stalker import Scene
        self.test_scene1 = Scene(
            name='Test Sce1',
            code='tsc1',
            project=self.test_project1,
        )
        DBSession.add(self.test_scene1)
        DBSession.commit()

        self.test_scene2 = Scene(
            name='Test Sce2',
            code='tsc2',
            project=self.test_project1,
        )
        DBSession.add(self.test_scene2)
        DBSession.commit()

        self.test_scene3 = Scene(
            name='Test Sce3',
            code='tsc3',
            project=self.test_project1
        )
        DBSession.add(self.test_scene3)
        DBSession.commit()

        from stalker import Asset
        self.test_asset1 = Asset(
            name="Test Asset1",
            code='ta1',
            project=self.test_project1,
            type=self.test_character_asset_type,
        )
        DBSession.add(self.test_asset1)
        DBSession.commit()

        self.test_asset2 = Asset(
            name="Test Asset2",
            code='ta2',
            project=self.test_project1,
            type=self.test_character_asset_type,
        )
        DBSession.add(self.test_asset2)
        DBSession.commit()

        self.test_asset3 = Asset(
            name="Test Asset3",
            code='ta3',
            project=self.test_project1,
            type=self.test_character_asset_type,
        )
        DBSession.add(self.test_asset3)
        DBSession.commit()

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
            image_format=self.test_image_format2
        )

        # create a mock shot object
        self.test_shot = Shot(**self.kwargs)
        DBSession.add(self.test_project1)
        DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for Shot
        class
        """
        assert Shot.__auto_name__ is True

    def test___hash___value_is_correctly_calculated(self):
        """testing if __hash__ value is correctly calculated
        """
        assert self.test_shot.__hash__() == \
            hash(self.test_shot.id) + \
            2 * hash(self.test_shot.name) + \
            3 * hash(self.test_shot.entity_type)

    def test_project_argument_is_skipped(self):
        """testing if a TypeError will be raised when the project argument is
        skipped
        """
        self.kwargs.pop('project')
        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.project should be an instance of ' \
            'stalker.models.project.Project, not NoneType. Or please supply ' \
            'a stalker.models.task.Task with the parent argument, so ' \
            'Stalker can use the project of the supplied parent task'

    def test_project_argument_is_None(self):
        """testing if a TypeError will be raised when the project argument is
        None
        """
        self.kwargs["project"] = None

        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.project should be an instance of ' \
            'stalker.models.project.Project, not NoneType. Or please supply ' \
            'a stalker.models.task.Task with the parent argument, so ' \
            'Stalker can use the project of the supplied parent task'

    def test_project_argument_is_not_Project_instance(self):
        """testing if a TypeError will be raised when the given project
        argument is not a Project instance
        """
        test_values = [1, 1.2, "project", ["a", "project"]]
        for test_value in test_values:
            self.kwargs["project"] = test_value
            with pytest.raises(TypeError) as cm:
                Shot(self.kwargs)

            assert str(cm.value) == 'Shot.project should be an instance ' \
                                        'of stalker.models.project.Project, ' \
                                        'not NoneType. Or please supply a ' \
                                        'stalker.models.task.Task with the ' \
                                        'parent argument, so Stalker can ' \
                                        'use the project of the supplied ' \
                                        'parent task'

    def test_project_already_has_a_shot_with_the_same_code(self):
        """testing if a ValueError will be raised when the given project
        argument already has a shot with the same code
        """
        # lets try to assign the shot to the same sequence2 which has another
        # shot with the same code
        assert self.kwargs['code'] == self.test_shot.code
        with pytest.raises(ValueError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == 'There is a Shot with the same code: SH123'

        # this should not raise a ValueError
        self.kwargs["code"] = "DifferentCode"
        new_shot2 = Shot(**self.kwargs)
        assert isinstance(new_shot2, Shot)

    def test_code_attribute_is_set_to_the_same_value(self):
        """testing if a ValueError will NOT be raised when the shot.code is set
        to the same value
        """
        self.test_shot.code = self.test_shot.code

    def test_project_attribute_is_read_only(self):
        """testing if the project attribute is read only
        """
        with pytest.raises(AttributeError) as cm:
            self.test_shot.project = self.test_project2

        assert str(cm.value) == "can't set attribute"

    def test_project_contains_shots(self):
        """testing if the current shot is going to be added to the Project, so
        the Project.shots list will contain the current shot
        """
        assert self.test_shot in self.test_shot.project.shots

    def test_project_argument_is_working_properly(self):
        """testing if the project argument is working properly
        """
        assert self.test_shot.project == self.kwargs["project"]

    def test_sequences_argument_is_skipped(self):
        """testing if the sequences attribute will be an empty list when the
        sequences argument is skipped
        """
        self.kwargs.pop('sequences')
        self.kwargs['code'] = 'DifferentCode'
        new_shot = Shot(**self.kwargs)
        assert new_shot.sequences == []

    def test_sequences_argument_is_None(self):
        """testing if the sequences attribute will be an empty list when the
        sequences argument is set to None
        """
        self.kwargs['sequences'] = None
        self.kwargs['code'] = 'NewCode'
        new_shot = Shot(**self.kwargs)
        assert new_shot.sequences == []

    def test_sequences_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the sequences attribute
        is set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.sequences = None

        assert str(cm.value) == 'Incompatible collection type: None is not ' \
                                'list-like'

    def test_sequences_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the sequences argument is
        not a list
        """
        self.kwargs['sequences'] = 'not a list'
        self.kwargs['code'] = 'NewCode'
        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == 'Incompatible collection type: str is not ' \
                                'list-like'

    def test_sequences_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the sequences attribute
        is not a list
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.sequences = 'not a list'

        assert str(cm.value) == 'Incompatible collection type: str is not ' \
                                'list-like'

    def test_sequences_argument_is_not_a_list_of_Sequence_instances(self):
        """testing if a TypeError will be raised when the sequences argument is
        not a list of Sequences
        """
        self.kwargs['sequences'] = ['not', 1, 'list', 'of', 'sequences']
        self.kwargs['code'] = 'NewShot'
        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == 'Shot.sequences should all be ' \
                                'stalker.models.sequence.Sequence ' \
                                'instances, not str'

    def test_sequences_attribute_is_not_a_list_of_Sequence_instances(self):
        """testing if a TypeError will be raised when the sequences attribute
        is not a list of Sequence instances
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.sequences = ['not', 1, 'list', 'of', 'sequences']

        assert str(cm.value) == 'Shot.sequences should all be ' \
                                'stalker.models.sequence.Sequence ' \
                                'instances, not str'

    def test_sequences_argument_is_working_properly(self):
        """testing if the sequences attribute is working properly
        """
        self.kwargs['code'] = 'NewShot'
        from stalker import Sequence
        seq1 = Sequence(
            name='seq1',
            code='seq1',
            project=self.test_project1,
        )
        seq2 = Sequence(
            name='seq2',
            code='seq2',
            project=self.test_project1,
        )
        seq3 = Sequence(
            name='seq3',
            code='seq3',
            project=self.test_project1,
        )

        seqs = [seq1, seq2, seq3]
        self.kwargs['sequences'] = seqs
        new_shot = Shot(**self.kwargs)

        assert \
            sorted(new_shot.sequences, key=lambda x: x.name) == \
            sorted(seqs, key=lambda x: x.name)

    def test_sequences_attribute_is_working_properly(self):
        """testing if the sequences attribute is working properly
        """
        self.kwargs['code'] = 'NewShot'

        from stalker import Sequence
        seq1 = Sequence(
            name='seq1',
            code='seq1',
            project=self.test_project1,
        )
        seq2 = Sequence(
            name='seq2',
            code='seq2',
            project=self.test_project1,
        )
        seq3 = Sequence(
            name='seq3',
            code='seq3',
            project=self.test_project1,
        )

        new_shot = Shot(**self.kwargs)

        new_shot.sequences = [seq1]
        new_shot.sequences.append(seq2)
        new_shot.sequences.append(seq3)

        seqs = [seq1, seq2, seq3]
        assert \
            sorted(new_shot.sequences, key=lambda x: x.name) == \
            sorted(seqs, key=lambda x: x.name)

    def test_scenes_argument_is_skipped(self):
        """testing if the scenes attribute will be an empty list when the
        scenes argument is skipped
        """
        self.kwargs.pop('scenes')
        self.kwargs['code'] = 'DifferentCode'
        new_shot = Shot(**self.kwargs)
        assert new_shot.scenes == []

    def test_scenes_argument_is_None(self):
        """testing if the scenes attribute will be an empty list when the
        scenes argument is set to None
        """
        self.kwargs['scenes'] = None
        self.kwargs['code'] = 'NewCode'
        new_shot = Shot(**self.kwargs)
        assert new_shot.scenes == []

    def test_scenes_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the scenes attribute
        is set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.scenes = None

        assert str(cm.value) == \
            'Incompatible collection type: None is not list-like'

    def test_scenes_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the scenes argument is
        not a list
        """
        self.kwargs['scenes'] = 'not a list'
        self.kwargs['code'] = 'NewCode'
        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Incompatible collection type: str is not list-like'

    def test_scenes_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the scenes attribute
        is not a list
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.scenes = 'not a list'

        assert str(cm.value) == \
            'Incompatible collection type: str is not list-like'

    def test_scenes_argument_is_not_a_list_of_Scene_instances(self):
        """testing if a TypeError will be raised when the scenes argument is
        not a list of Scenes
        """
        self.kwargs['scenes'] = ['not', 1, 'list', 'of', 'scenes']
        self.kwargs['code'] = 'NewShot'
        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.scenes should all be stalker.models.scene.Scene ' \
            'instances, not str'

    def test_scenes_attribute_is_not_a_list_of_Scene_instances(self):
        """testing if a TypeError will be raised when the scenes attribute
        is not a list of Scene instances
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.scenes = ['not', 1, 'list', 'of', 'scenes']

        assert str(cm.value) == \
            'Shot.scenes should all be stalker.models.scene.Scene ' \
            'instances, not str'

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

        assert \
            sorted(new_shot.scenes, key=lambda x: x.name) == \
            sorted(seqs, key=lambda x: x.name)

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
        assert \
            sorted(new_shot.scenes, key=lambda x: x.name) == \
            sorted(seqs, key=lambda x: x.name)

    def test_cut_in_argument_is_skipped(self):
        """testing if the cut_in argument is skipped the cut_in argument will
        be calculated from cut_out argument
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_in")
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        new_shot = Shot(**self.kwargs)
        assert new_shot.cut_out == self.kwargs['cut_out']
        assert new_shot.cut_in == new_shot.cut_out

    def test_cut_in_argument_is_none(self):
        """testing if the cut_in attribute value will be calculated from the
        cut_out attribute value if the cut_in argument is None
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = None
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        shot = Shot(**self.kwargs)
        assert shot.cut_out == self.kwargs['cut_out']
        assert shot.cut_in == shot.cut_out

    def test_cut_in_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised when the cut_in attribute is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.cut_in = None

        assert str(cm.value) == 'Shot.cut_in should be an int, not NoneType'

    def test_cut_in_argument_is_not_integer(self):
        """testing if a TypeError will be raised if the cut_in argument is not
        an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = "a string"

        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == 'Shot.cut_in should be an int, not str'

    def test_cut_in_attribute_is_not_integer(self):
        """testing if a TypeError will be raised if the cut_in attribute is set
        to a value other than an integer
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.cut_in = 'a string'

        assert str(cm.value) == 'Shot.cut_in should be an int, not str'

    def test_cut_in_argument_is_bigger_than_cut_out_argument(self):
        """testing if a cut_out will be offset when the cut_in argument
        value is bigger than the cut_out argument value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = self.kwargs["cut_out"] + 10
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        shot = Shot(**self.kwargs)
        assert shot.cut_in == 149
        assert shot.cut_out == 149

    def test_cut_in_attribute_is_bigger_than_cut_out_attribute(self):
        """testing if a the cut_out attribute value will be offset when the
        cut_in attribute is set bigger than cut_out attribute value
        """
        self.test_shot.cut_in = self.test_shot.cut_out + 10
        assert self.test_shot.cut_in == 159
        assert self.test_shot.cut_out == self.test_shot.cut_in

    def test_cut_out_argument_is_skipped(self):
        """testing if the cut_out attribute will be calculated from cut_in
        argument value when the cut_out argument is skipped
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_out")
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        new_shot = Shot(**self.kwargs)
        assert new_shot.cut_in == self.kwargs['cut_in']
        assert new_shot.cut_out == new_shot.cut_in

    def test_cut_out_argument_is_set_to_none(self):
        """testing if the cut_out argument is set to None the cut_out attribute
        will be calculated from cut_in argument value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = None
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None

        shot = Shot(**self.kwargs)
        assert shot.cut_in == self.kwargs['cut_in']
        assert shot.cut_out == shot.cut_in

    def test_cut_out_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised if the cut_out attribute is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.cut_out = None
        assert str(cm.value) == 'Shot.cut_out should be an int, not NoneType'

    def test_cut_out_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the cut_out argument is
        not an integer
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = "a string"
        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == 'Shot.cut_out should be an int, not str'

    def test_cut_out_attribute_is_not_integer(self):
        """testing if a TypeError will be raised if the cut_out attribute is
        set to a value other than an integer
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.cut_out = "a string"
        assert str(cm.value) == 'Shot.cut_out should be an int, not str'

    def test_cut_out_argument_is_smaller_than_cut_in_argument(self):
        """testing if the cut_out attribute is updated when the cut_out
        argument is smaller than cut_in argument
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = self.kwargs["cut_in"] - 10
        self.kwargs['source_in'] = None
        self.kwargs['source_out'] = None
        shot = Shot(**self.kwargs)
        assert shot.cut_in == 102
        assert shot.cut_out == 102

    def test_cut_out_attribute_is_smaller_than_cut_in_attribute(self):
        """testing if the cut_out attribute is updated when it is smaller than
        cut_in attribute
        """
        self.test_shot.cut_out = self.test_shot.cut_in - 10
        assert self.test_shot.cut_in == 102
        assert self.test_shot.cut_out == 102

    def test_cut_duration_attribute_is_not_instance_of_int(self):
        """testing if a TypeError will be raised when the cut_duration
        attribute is set to a value other than an integer
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.cut_duration = "a string"

        assert str(cm.value) == \
            'Shot.cut_duration should be a positive integer value, not str'

    def test_cut_duration_attribute_will_be_updated_when_cut_in_attribute_changed(self):
        """testing if the cut_duration attribute will be updated when the
        cut_in attribute changed
        """
        self.test_shot.cut_in = 1
        assert self.test_shot.cut_duration == \
            self.test_shot.cut_out - self.test_shot.cut_in + 1

    def test_cut_duration_attribute_will_be_updated_when_cut_out_attribute_changed(self):
        """testing if the cut_duration attribute will be updated when the
        cut_out attribute changed
        """
        self.test_shot.cut_out = 1000
        assert self.test_shot.cut_duration == \
            self.test_shot.cut_out - self.test_shot.cut_in + 1

    def test_cut_duration_attribute_changes_cut_out_attribute(self):
        """testing if changes in cut_duration attribute will also affect
-        cut_out value.
        """
        first_cut_out = self.test_shot.cut_out
        self.test_shot.cut_duration = 245
        assert self.test_shot.cut_out != first_cut_out
        assert self.test_shot.cut_out == \
            self.test_shot.cut_in + self.test_shot.cut_duration - 1

    def test_cut_duration_attribute_is_zero(self):
        """testing if a ValueError will be raised when the cut_duration
        attribute is set to zero
        """
        with pytest.raises(ValueError) as cm:
            self.test_shot.cut_duration = 0

        assert str(cm.value) == \
            'Shot.cut_duration can not be set to zero or a negative value'

    def test_cut_duration_attribute_is_negative(self):
        """testing if a ValueError will be raised when the cut_duration
        attribute is set to a negative value
        """
        with pytest.raises(ValueError) as cm:
            self.test_shot.cut_duration = -100

        assert str(cm.value) == \
            'Shot.cut_duration can not be set to zero or a negative value'

    def test_source_in_argument_is_skipped(self):
        """testing if the source_in argument is skipped the source_in argument
        will be equal to cut_in attribute value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop('source_in')
        shot = Shot(**self.kwargs)
        assert shot.source_in == shot.cut_in

    def test_source_in_argument_is_none(self):
        """testing if the source_in attribute value will be equal to the cut_in
        attribute value when the source_in argument is None
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_in"] = None
        shot = Shot(**self.kwargs)
        assert shot.source_in == shot.cut_in

    def test_source_in_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised when the source_in attribute
        is set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.source_in = None

        assert str(cm.value) == \
            'Shot.source_in should be an int, not NoneType'

    def test_source_in_argument_is_not_integer(self):
        """testing if a TypeError will be raised if the source_in argument is
        not an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_in"] = "a string"

        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.source_in should be an int, not str'

    def test_source_in_attribute_is_not_integer(self):
        """testing if a TypeError will be raised if the source_in attribute is
        set to a value other than an integer
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.source_in = 'a string'

        assert str(cm.value) == \
            'Shot.source_in should be an int, not str'

    def test_source_in_argument_is_bigger_than_source_out_argument(self):
        """testing if a ValueError will be raised when the source_in argument
        value is set to bigger than source_out argument value
        """
        self.kwargs['code'] = 'SH123A'
        self.kwargs['source_out'] = self.kwargs['cut_out'] - 10
        self.kwargs['source_in'] = self.kwargs['source_out'] + 5
        with pytest.raises(ValueError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.source_out can not be smaller than Shot.source_in, ' \
            'source_in: 144 where as source_out: 139'

    def test_source_in_attribute_is_bigger_than_source_out_attribute(self):
        """testing if a ValueError will be raised when the source_ni attribute
        value is set to bigger than source out
        """
        # give it a little bit of room, to be sure that the ValueError is not
        # due to the cut_out
        self.test_shot.source_out -= 5
        with pytest.raises(ValueError) as cm:
            self.test_shot.source_in = self.test_shot.source_out + 1

        assert str(cm.value) == \
            'Shot.source_in can not be bigger than Shot.source_out, ' \
            'source_in: 136 where as source_out: 135'

    def test_source_in_argument_is_smaller_than_cut_in(self):
        """testing if a ValueError will be raised when the source_in argument
        value is smaller than cut_in attribute value
        """
        self.kwargs['code'] = 'SH123A'
        self.kwargs['source_in'] = self.kwargs['cut_in'] - 10
        with pytest.raises(ValueError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.source_in can not be smaller than Shot.cut_in, cut_in: ' \
            '112 where as source_in: 102'

    def test_source_in_argument_is_bigger_than_cut_out(self):
        """testing if a ValueError will be raised when the source_in argument
        value is bigger than cut_out attribute value
        """
        self.kwargs['code'] = 'SH123A'
        self.kwargs['source_in'] = self.kwargs['cut_out'] + 10
        with pytest.raises(ValueError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.source_in can not be bigger than Shot.cut_out, cut_out: ' \
            '149 where as source_in: 159'

    def test_source_out_argument_is_skipped(self):
        """testing if the source_out attribute will be equal to cut_out
        argument value when the source_out argument is skipped
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("source_out")
        new_shot = Shot(**self.kwargs)
        assert new_shot.source_out == new_shot.cut_out

    def test_source_out_argument_is_none(self):
        """testing if the source_out attribute value will be equal to cut_out
        if the source_out argument value is None
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_out"] = None

        shot = Shot(**self.kwargs)
        assert shot.source_out == shot.cut_out

    def test_source_out_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised if the source_out attribute is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.source_out = None
        assert str(cm.value) == \
            'Shot.source_out should be an int, not NoneType'

    def test_source_out_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the source_out argument
        is not an integer
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_out"] = "a string"
        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == 'Shot.source_out should be an int, not str'

    def test_source_out_attribute_is_not_integer(self):
        """testing if a TypeError will be raised if the source_out attribute is
        set to a value other than an integer
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.source_out = "a string"
        assert str(cm.value) == 'Shot.source_out should be an int, not str'

    def test_source_out_argument_is_smaller_than_source_in_argument(self):
        """testing if a ValueError will be raised when the source_out argument
        is smaller than the source_in attibute value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["source_in"] = self.kwargs['cut_in'] + 15
        self.kwargs["source_out"] = self.kwargs["source_in"] - 10
        with pytest.raises(ValueError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.source_out can not be smaller than Shot.source_in, ' \
            'source_in: 127 where as source_out: 117'

    def test_source_out_attribute_is_smaller_than_source_in_attribute(self):
        """testing if a ValueError will be raised when the source_out attribute
        is set to a value smaller than source_in
        """
        with pytest.raises(ValueError) as cm:
            self.test_shot.source_out = self.test_shot.source_in - 2

        assert str(cm.value) == \
            'Shot.source_out can not be smaller than Shot.source_in, ' \
            'source_in: 120 where as source_out: 118'

    def test_image_format_argument_is_skipped(self):
        """testing if the image_format is copied from the Project instance when
        the image_format argument is skipped
        """
        self.kwargs.pop('image_format')
        self.kwargs['code'] = 'TestShot'
        new_shot = Shot(**self.kwargs)
        assert new_shot.image_format == self.kwargs['project'].image_format

    def test_image_format_argument_is_None(self):
        """testing if the image format is copied from the Project instance when
        the image_format argument is None
        """
        self.kwargs['image_format'] = None
        self.kwargs['code'] = 'newShot'
        new_shot = Shot(**self.kwargs)
        assert new_shot.image_format == self.kwargs['project'].image_format

    def test_image_format_attribute_is_None(self):
        """testing if the image format is copied from the Project instance when
        the image_format attribute is set to None
        """
        # test start conditions
        assert self.test_shot.image_format != \
            self.test_shot.project.image_format
        self.test_shot.image_format = None
        assert self.test_shot.image_format == \
            self.test_shot.project.image_format

    def test_image_format_argument_is_not_a_ImageFormat_instance_and_not_None(self):
        """testing if a TypeError will be raised when the image_format argument
        is not a ImageFormat instance and not None
        """
        self.kwargs['code'] = 'new_shot'
        self.kwargs['image_format'] = 'not an image format instance'
        with pytest.raises(TypeError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.image_format should be an instance of ' \
            'stalker.models.format.ImageFormat, not str'

    def test_image_format_attribute_is_not_a_ImageFormat_instance_and_not_None(self):
        """testing if a TypeError will be raised when the image_format
        attribute is not a ImageFormat instance and not None
        """
        with pytest.raises(TypeError) as cm:
            self.test_shot.image_format = 'not an image f'

        assert str(cm.value) == \
            'Shot.image_format should be an instance of ' \
            'stalker.models.format.ImageFormat, not str'

    def test_image_format_argument_is_working_properly(self):
        """testing if the image_format argument value is passed to the
        image_format attribute correctly
        """
        assert self.kwargs['image_format'] == self.test_shot.image_format

    def test_image_format_attribute_is_working_properly(self):
        """testing if the image_format attribute is working properly
        """
        assert self.test_shot.image_format != self.test_image_format1
        self.test_shot.image_format = self.test_image_format1
        assert self.test_shot.image_format == self.test_image_format1

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

        assert not new_shot1 == new_shot2
        assert not new_shot1 == new_entity
        assert not new_shot1 == new_shot3

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

        assert new_shot1 != new_shot2
        assert new_shot1 != new_entity
        assert new_shot1 != new_shot3

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

        assert new_shot.references == references

    def test_TaskMixin_initialization(self):
        """testing if the TaskMixin part is initialized correctly
        """
        from stalker import StatusList
        project_status_list = \
            StatusList.query\
                .filter(StatusList.target_entity_type=='Project').first()

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
        from stalker.db.session import DBSession
        DBSession.add(new_project)
        DBSession.commit()

        self.kwargs['project'] = new_project
        self.kwargs['code'] = "SH12314"

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

        assert \
            sorted(new_shot.tasks, key=lambda x: x.name) == \
            sorted(tasks, key=lambda x: x.name)

    def test__repr__(self):
        """testing the representation of Shot
        """
        assert self.test_shot.__repr__() == \
            "<Shot (%s, %s)>" % (self.test_shot.code, self.test_shot.code)

    def test_plural_class_name(self):
        """testing the plural name of Shot class
        """
        assert self.test_shot.plural_class_name == "Shots"

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ class attribute is False for
        Shot class
        """
        assert Shot.__strictly_typed__ is False

    def test_cut_duration_initialization_bug_with_cut_in(self):
        """testing if the _cut_duration attribute is initialized correctly for
        a Shot restored from DB
        """
        # retrieve the shot back from DB
        from stalker import Shot
        test_shot_db = Shot.query.filter_by(name=self.kwargs['name']).first()
        # trying to change the cut_in and cut_out values should not raise any
        # errors
        test_shot_db.cut_in = 1
        from stalker.db.session import DBSession
        DBSession.add(test_shot_db)
        DBSession.commit()

    def test_cut_duration_initialization_bug_with_cut_out(self):
        """testing if the _cut_duration attribute is initialized correctly for
        a Shot restored from DB
        """
        from stalker import Shot
        # reconnect to the database
        # retrieve the shot back from DB
        test_shot_db = Shot.query.filter_by(name=self.kwargs['name']).first()
        # trying to change the cut_in and cut_out values should not raise any
        # errors
        test_shot_db.cut_out = 100
        from stalker.db.session import DBSession
        DBSession.add(test_shot_db)
        DBSession.commit()

    def test_cut_values_are_set_correctly(self):
        """testing if the cut_in attribute is set correctly in db
        """
        self.test_shot.cut_in = 100
        assert self.test_shot.cut_in == 100

        self.test_shot.cut_out = 153
        assert self.test_shot.cut_in == 100
        assert self.test_shot.cut_out == 153

        from stalker import Shot
        from stalker.db.session import DBSession
        DBSession.add(self.test_shot)
        DBSession.commit()

        # retrieve the shot back from DB
        test_shot_db = Shot.query.filter_by(name=self.kwargs['name']).first()

        assert test_shot_db.cut_in == 100
        assert test_shot_db.cut_out == 153

    def test_fps_argument_is_skipped(self):
        """testing if the default value will be used when fps is skipped
        """
        if 'fps' in self.kwargs:
            self.kwargs.pop("fps")

        self.kwargs['code'] = 'SHnew'
        new_shot = Shot(**self.kwargs)
        assert new_shot.fps == self.test_project1.fps

    def test_fps_attribute_is_set_to_None(self):
        """testing if the Project.fps will be used if the fps argument is None
        """
        self.kwargs["fps"] = None
        self.kwargs['code'] = 'SHnew'
        new_shot = Shot(**self.kwargs)

        assert new_shot.fps == self.test_project1.fps

    def test_fps_argument_is_given_as_non_float_or_integer(self):
        """testing if a TypeError will be raised when the fps argument is
        given as a value other than a float or integer, or a string which is
        convertible to float.
        """
        test_values = [["a", "list"], {"a": "list"}]
        for i, test_value in enumerate(test_values):
            self.kwargs["fps"] = test_value
            self.kwargs['code'] = 'SH%i'
            with pytest.raises(TypeError) as cm:
                Shot(**self.kwargs)

            assert str(cm.value) == \
                'Shot.fps should be a positive float or int, not %s' % \
                test_value.__class__.__name__

    def test_fps_attribute_is_given_as_non_float_or_integer(self):
        """testing if a TypeError will be raised when the fps attribute is
        set to a value other than a float, integer or valid string literals
        """
        test_values = ["a str", ["a", "list"], {"a": "list"}]
        for test_value in test_values:
            with pytest.raises(TypeError) as cm:
                self.test_shot.fps = test_value

            assert str(cm.value) == \
                'Shot.fps should be a positive float or int, not %s' % \
                test_value.__class__.__name__

    def test_fps_attribute_float_conversion(self):
        """testing if the fps attribute is converted to float when the float
        argument is given as an integer
        """
        test_value = 1
        self.kwargs["fps"] = test_value
        self.kwargs['code'] = 'SHnew'
        new_shot = Shot(**self.kwargs)
        assert isinstance(new_shot.fps, float)
        assert new_shot.fps == float(test_value)

    def test_fps_attribute_float_conversion_2(self):
        """testing if the fps attribute is converted to float when it is set to
        an integer value
        """
        test_value = 1
        self.test_shot.fps = test_value
        assert isinstance(self.test_shot.fps, float)
        assert self.test_shot.fps == float(test_value)

    def test_fps_argument_is_zero(self):
        """testing if a ValueError will be raised when the fps is 0
        """
        self.kwargs['fps'] = 0
        self.kwargs['code'] = 'SHnew'
        with pytest.raises(ValueError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.fps should be a positive float or int, not 0.0'

    def test_fps_attribute_is_set_to_zero(self):
        """testing if a value error will be raised when the fps attribute is
        set to zero
        """
        with pytest.raises(ValueError) as cm:
            self.test_shot.fps = 0

        assert str(cm.value) == \
            'Shot.fps should be a positive float or int, not 0.0'

    def test_fps_argument_is_negative(self):
        """testing if a ValueError will be raised when the fps argument is
        negative
        """
        self.kwargs['fps'] = -1.0
        self.kwargs['code'] = 'SHrandom'
        with pytest.raises(ValueError) as cm:
            Shot(**self.kwargs)

        assert str(cm.value) == \
            'Shot.fps should be a positive float or int, not -1.0'

    def test_fps_attribute_is_negative(self):
        """testing if a ValueError will be raised when the fps attribute is
        set to a negative value
        """
        with pytest.raises(ValueError) as cm:
            self.test_shot.fps = -1

        assert str(cm.value) == \
            'Shot.fps should be a positive float or int, not -1.0'

    def test_fps_changes_with_project(self):
        """testing if the fps reflects the project.fps unless it is set to a
        value
        """
        new_shot = Shot(
            name='New Shot',
            code='ns',
            project=self.test_project1
        )
        assert new_shot.fps == self.test_project1.fps
        self.test_project1.fps = 335
        assert new_shot.fps == 335
        new_shot.fps = 12
        assert new_shot.fps == 12
        self.test_project1.fps = 24
        assert new_shot.fps == 12
