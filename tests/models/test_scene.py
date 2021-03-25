# -*- coding: utf-8 -*-

import pytest

from stalker.testing import UnitTestDBBase
from stalker import Scene


class SceneTester(UnitTestDBBase):
    """Tests stalker.models.scene.Scene class
    """

    def setUp(self):
        """setup the test
        """
        super(SceneTester, self).setUp()
        # create a test project, user and a couple of shots
        from stalker import Type
        self.project_type = Type(
            name="Test Project Type",
            code='test',
            target_entity_type='Project',
        )

        # create a repository
        self.repository_type = Type(
            name="Test Type",
            code='test',
            target_entity_type='Repository'
        )

        from stalker import Repository
        self.test_repository = Repository(
            name="Test Repository",
            code="TR",
            type=self.repository_type,
        )

        # create projects
        from stalker import Project
        self.test_project = Project(
            name="Test Project 1",
            code='tp1',
            type=self.project_type,
            repository=self.test_repository,
        )

        self.test_project2 = Project(
            name="Test Project 2",
            code='tp2',
            type=self.project_type,
            repository=self.test_repository,
        )

        # the parameters
        self.kwargs = {
            "name": "Test Scene",
            'code': 'tsce',
            "description": "A test scene",
            "project": self.test_project,
        }

        # the test sequence
        self.test_scene = Scene(**self.kwargs)
        from stalker.db.session import DBSession
        DBSession.add(self.test_scene)
        DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Scene class
        """
        assert Scene.__auto_name__ is False

    def test_shots_attribute_defaults_to_empty_list(self):
        """testing if the shots attribute defaults to an empty list
        """
        new_scene = Scene(**self.kwargs)
        assert new_scene.shots == []

    def test_shots_attribute_is_set_None(self):
        """testing if a TypeError will be raised when the shots attribute will
        be set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_scene.shots = None

        assert str(cm.value) == \
            'Incompatible collection type: None is not list-like'

    def test_shots_attribute_is_set_to_other_than_a_list(self):
        """testing if a TypeError will be raised when the shots attribute is
        tried to be set to something other than a list
        """
        test_value = [1, 1.2, "a string"]
        with pytest.raises(TypeError) as cm:
            self.test_scene.shots = test_value

        assert str(cm.value) == \
            'Scene.shots needs to be all stalker.models.shot.Shot ' \
            'instances, not int'

    def test_shots_attribute_is_a_list_of_other_objects(self):
        """testing if a TypeError will be raised when the shots argument is a
        list of other type of objects
        """
        test_value = [1, 1.2, "a string"]
        with pytest.raises(TypeError) as cm:
            self.test_scene.shots = test_value

        assert str(cm.value) == \
            'Scene.shots needs to be all stalker.models.shot.Shot ' \
            'instances, not int'

    def test_shots_attribute_elements_tried_to_be_set_to_non_Shot_object(self):
        """testing if a TypeError will be raised when the individual elements
        in the shots list tried to be set to something other than a Shot
        instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_scene.shots.append("a string")

        assert str(cm.value) == \
            'Scene.shots needs to be all stalker.models.shot.Shot ' \
            'instances, not str'

    def test_equality(self):
        """testing the equality of scenes
        """
        new_seq1 = Scene(**self.kwargs)
        new_seq2 = Scene(**self.kwargs)
        from stalker import Entity
        new_entity = Entity(**self.kwargs)

        self.kwargs["name"] = "a different scene"
        new_seq3 = Scene(**self.kwargs)

        assert new_seq1 == new_seq2
        assert not new_seq1 == new_seq3
        assert not new_seq1 == new_entity

    def test_inequality(self):
        """testing the inequality of scenes
        """
        new_seq1 = Scene(**self.kwargs)
        new_seq2 = Scene(**self.kwargs)
        from stalker import Entity
        new_entity = Entity(**self.kwargs)

        self.kwargs["name"] = "a different scene"
        new_seq3 = Scene(**self.kwargs)

        assert not new_seq1 != new_seq2
        assert new_seq1 != new_seq3
        assert new_seq1 != new_entity

    def test_ProjectMixin_initialization(self):
        """testing if the ProjectMixin part is initialized correctly
        """
        from stalker import Type
        project_type = Type(
            name="Commercial",
            code='comm',
            target_entity_type='Project'
        )

        from stalker import Project
        new_project = Project(
            name="Test Project",
            code='tp',
            type=project_type,
            repository=self.test_repository
        )

        self.kwargs["project"] = new_project
        new_scene = Scene(**self.kwargs)
        assert new_scene.project == new_project

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ class attribute is False for
        Scene class.
        """
        assert Scene.__strictly_typed__ is False
