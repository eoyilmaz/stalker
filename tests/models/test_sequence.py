# -*- coding: utf-8 -*-

import pytest
from stalker.testing import UnitTestDBBase


class SequenceTester(UnitTestDBBase):
    """Tests stalker.models.sequence.Sequence class
    """

    def setUp(self):
        """setup the test
        """
        super(SequenceTester, self).setUp()

        # create a test project, user and a couple of shots
        from stalker import Type
        self.project_type = Type(
            name="Test Project Type",
            code='test',
            target_entity_type='Project',
        )
        from stalker.db.session import DBSession
        DBSession.add(self.project_type)

        # create a repository
        self.repository_type = Type(
            name="Test Type",
            code='test',
            target_entity_type='Repository'
        )
        DBSession.add(self.repository_type)

        from stalker import Repository
        self.test_repository = Repository(
            name="Test Repository",
            code="TR",
            type=self.repository_type,
        )
        DBSession.add(self.test_repository)

        # create projects
        from stalker import Project
        self.test_project = Project(
            name="Test Project 1",
            code='tp1',
            type=self.project_type,
            repository=self.test_repository,
        )
        DBSession.add(self.test_project)

        self.test_project2 = Project(
            name="Test Project 2",
            code='tp2',
            type=self.project_type,
            repository=self.test_repository,
        )
        DBSession.add(self.test_project2)

        # the parameters
        self.kwargs = {
            "name": "Test Sequence",
            'code': 'tseq',
            "description": "A test sequence",
            "project": self.test_project,
        }

        # the test sequence
        from stalker import Sequence
        self.test_sequence = Sequence(**self.kwargs)
        DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Sequence class
        """
        from stalker import Sequence
        assert Sequence.__auto_name__ is False

    def test_plural_class_name(self):
        """testing the plural name of Sequence class
        """
        assert self.test_sequence.plural_class_name == "Sequences"

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ class attribute is False for
        Sequence class.
        """
        from stalker import Sequence
        assert Sequence.__strictly_typed__ is False

    def test_shots_attribute_defaults_to_empty_list(self):
        """testing if the shots attribute defaults to an empty list
        """
        from stalker import Sequence
        new_sequence = Sequence(**self.kwargs)
        assert new_sequence.shots == []

    def test_shots_attribute_is_set_None(self):
        """testing if a TypeError will be raised when the shots attribute will
        be set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_sequence.shots = None

        assert str(cm.value) == \
            'Incompatible collection type: None is not list-like'

    def test_shots_attribute_is_set_to_other_than_a_list(self):
        """testing if a TypeError will be raised when the shots attribute is
        tried to be set to something other than a list
        """
        test_value = "a string"
        with pytest.raises(TypeError) as cm:
            self.test_sequence.shots = test_value

        assert str(cm.value) == \
            'Incompatible collection type: str is not list-like'

    def test_shots_attribute_is_a_list_of_other_objects(self):
        """testing if a TypeError will be raised when the shots argument is a
        list of other type of objects
        """
        test_value = [1, 1.2, "a string"]
        with pytest.raises(TypeError) as cm:
            self.test_sequence.shots = test_value

        assert str(cm.value) == \
            'Sequence.shots should be all stalker.models.shot.Shot ' \
            'instances, not int'

    def test_shots_attribute_elements_tried_to_be_set_to_non_Shot_object(self):
        """testing if a TypeError will be raised when the individual elements
        in the shots list tried to be set to something other than a Shot
        instance
        """
        test_value = "a string"
        with pytest.raises(TypeError) as cm:
            self.test_sequence.shots.append(test_value)

        assert str(cm.value) == \
            'Sequence.shots should be all stalker.models.shot.Shot ' \
            'instances, not str'

    def test_equality(self):
        """testing the equality of sequences
        """
        from stalker import Entity, Sequence
        new_seq1 = Sequence(**self.kwargs)
        new_seq2 = Sequence(**self.kwargs)
        new_entity = Entity(**self.kwargs)

        self.kwargs["name"] = "a different sequence"
        new_seq3 = Sequence(**self.kwargs)

        assert new_seq1 == new_seq2
        assert not new_seq1 == new_seq3
        assert not new_seq1 == new_entity

    def test_inequality(self):
        """testing the inequality of sequences
        """
        from stalker import Entity, Sequence
        new_seq1 = Sequence(**self.kwargs)
        new_seq2 = Sequence(**self.kwargs)
        new_entity = Entity(**self.kwargs)

        self.kwargs["name"] = "a different sequence"
        new_seq3 = Sequence(**self.kwargs)

        assert not new_seq1 != new_seq2
        assert new_seq1 != new_seq3
        assert new_seq1 != new_entity

    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """
        from stalker import Type, Link, Sequence
        link_type_1 = Type(
            name="Image",
            code='image',
            target_entity_type="Link"
        )

        link1 = Link(
            name="Artwork 1",
            full_path="/mnt/M/JOBs/TEST_PROJECT",
            filename="a.jpg",
            type=link_type_1
        )
        link2 = Link(
            name="Artwork 2",
            full_path="/mnt/M/JOBs/TEST_PROJECT",
            filename="b.jbg",
            type=link_type_1
        )
        references = [link1, link2]
        self.kwargs["references"] = references
        new_sequence = Sequence(**self.kwargs)
        assert new_sequence.references == references

    def test_initialization_of_task_part(self):
        """testing if the Task part is initialized correctly
        """
        from stalker import Type, Project, Sequence, Task
        project_type = Type(
            name="Commercial",
            code='comm',
            target_entity_type='Project'
        )

        new_project = Project(
            name="Commercial",
            code='comm',
            type=project_type,
            repository=self.test_repository,
        )

        self.kwargs["project"] = new_project
        new_sequence = Sequence(**self.kwargs)

        task1 = Task(
            name="Modeling",
            status=0,
            project=new_project,
            parent=new_sequence,
        )

        task2 = Task(
            name="Lighting",
            status=0,
            project=new_project,
            parent=new_sequence,
        )

        tasks = [task1, task2]

        assert \
            sorted(new_sequence.tasks, key=lambda x: x.name) == \
            sorted(tasks, key=lambda x: x.name)

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

        from stalker import Sequence
        self.kwargs["project"] = new_project
        new_sequence = Sequence(**self.kwargs)
        assert new_sequence.project == new_project
