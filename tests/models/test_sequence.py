# -*- coding: utf-8 -*-
"""Tests for the Sequence class."""

import pytest

from stalker import Entity, Link, Project, Repository, Sequence, Task, Type
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_sequence_db_tests(setup_postgresql_db):
    """Set up the tests for the Sequence class with a DB."""
    data = dict()
    # create a test project, user and a couple of shots
    data["project_type"] = Type(
        name="Test Project Type",
        code="test",
        target_entity_type="Project",
    )
    DBSession.add(data["project_type"])

    # create a repository
    data["repository_type"] = Type(
        name="Test Type", code="test", target_entity_type="Repository"
    )
    DBSession.add(data["repository_type"])

    data["test_repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["repository_type"],
    )
    DBSession.add(data["test_repository"])

    # create projects
    data["test_project"] = Project(
        name="Test Project 1",
        code="tp1",
        type=data["project_type"],
        repository=data["test_repository"],
    )
    DBSession.add(data["test_project"])

    data["test_project2"] = Project(
        name="Test Project 2",
        code="tp2",
        type=data["project_type"],
        repository=data["test_repository"],
    )
    DBSession.add(data["test_project2"])

    # the parameters
    data["kwargs"] = {
        "name": "Test Sequence",
        "code": "tseq",
        "description": "A test sequence",
        "project": data["test_project"],
    }

    # the test sequence
    data["test_sequence"] = Sequence(**data["kwargs"])
    DBSession.commit()
    return data


def test___auto_name__class_attribute_is_set_to_false(setup_sequence_db_tests):
    """__auto_name__ class attribute is set to False for Sequence class."""
    assert Sequence.__auto_name__ is False


def test_plural_class_name(setup_sequence_db_tests):
    """plural name of Sequence class."""
    data = setup_sequence_db_tests
    assert data["test_sequence"].plural_class_name == "Sequences"


def test___strictly_typed___is_False():
    """__strictly_typed__ class attribute is False for Sequence class."""
    assert Sequence.__strictly_typed__ is False


def test_shots_attribute_defaults_to_empty_list(setup_sequence_db_tests):
    """shots attribute defaults to an empty list."""
    data = setup_sequence_db_tests
    new_sequence = Sequence(**data["kwargs"])
    assert new_sequence.shots == []


def test_shots_attribute_is_set_none(setup_sequence_db_tests):
    """TypeError raised if the shots attribute set to None."""
    data = setup_sequence_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_sequence"].shots = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_shots_attribute_is_set_to_other_than_a_list(setup_sequence_db_tests):
    """TypeError raised if the shots attr is set to something other than a list."""
    data = setup_sequence_db_tests
    test_value = "a string"
    with pytest.raises(TypeError) as cm:
        data["test_sequence"].shots = test_value
    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_shots_attribute_is_a_list_of_other_objects(setup_sequence_db_tests):
    """TypeError raised if the shots argument is a list of other type of objects."""
    data = setup_sequence_db_tests
    test_value = [1, 1.2, "a string"]
    with pytest.raises(TypeError) as cm:
        data["test_sequence"].shots = test_value

    assert str(cm.value) == (
        "Sequence.shots should be all stalker.models.shot.Shot instances, not int: '1'"
    )


def test_shots_attribute_elements_tried_to_be_set_to_non_Shot_object(
    setup_sequence_db_tests,
):
    """TypeError raised if the shots attr appended not a Shot instance."""
    data = setup_sequence_db_tests
    test_value = "a string"
    with pytest.raises(TypeError) as cm:
        data["test_sequence"].shots.append(test_value)

    assert str(cm.value) == (
        "Sequence.shots should be all stalker.models.shot.Shot instances, "
        "not str: 'a string'"
    )


def test_equality(setup_sequence_db_tests):
    """equality of sequences."""
    data = setup_sequence_db_tests
    new_seq1 = Sequence(**data["kwargs"])
    new_seq2 = Sequence(**data["kwargs"])
    new_entity = Entity(**data["kwargs"])

    data["kwargs"]["name"] = "a different sequence"
    new_seq3 = Sequence(**data["kwargs"])

    assert new_seq1 == new_seq2
    assert not new_seq1 == new_seq3
    assert not new_seq1 == new_entity


def test_inequality(setup_sequence_db_tests):
    """inequality of sequences."""
    data = setup_sequence_db_tests
    new_seq1 = Sequence(**data["kwargs"])
    new_seq2 = Sequence(**data["kwargs"])
    new_entity = Entity(**data["kwargs"])

    data["kwargs"]["name"] = "a different sequence"
    new_seq3 = Sequence(**data["kwargs"])

    assert not new_seq1 != new_seq2
    assert new_seq1 != new_seq3
    assert new_seq1 != new_entity


def test_reference_mixin_initialization(setup_sequence_db_tests):
    """ReferenceMixin part is initialized correctly."""
    data = setup_sequence_db_tests
    link_type_1 = Type(name="Image", code="image", target_entity_type="Link")

    link1 = Link(
        name="Artwork 1",
        full_path="/mnt/M/JOBs/TEST_PROJECT",
        filename="a.jpg",
        type=link_type_1,
    )
    link2 = Link(
        name="Artwork 2",
        full_path="/mnt/M/JOBs/TEST_PROJECT",
        filename="b.jbg",
        type=link_type_1,
    )
    references = [link1, link2]
    data["kwargs"]["references"] = references
    new_sequence = Sequence(**data["kwargs"])
    assert new_sequence.references == references


def test_initialization_of_task_part(setup_sequence_db_tests):
    """Task part is initialized correctly."""
    data = setup_sequence_db_tests
    project_type = Type(name="Commercial", code="comm", target_entity_type="Project")

    new_project = Project(
        name="Commercial",
        code="comm",
        type=project_type,
        repository=data["test_repository"],
    )

    data["kwargs"]["project"] = new_project
    new_sequence = Sequence(**data["kwargs"])

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

    assert sorted(new_sequence.tasks, key=lambda x: x.name) == sorted(
        tasks, key=lambda x: x.name
    )


def test_project_mixin_initialization(setup_sequence_db_tests):
    """ProjectMixin part is initialized correctly."""
    data = setup_sequence_db_tests
    project_type = Type(name="Commercial", code="comm", target_entity_type="Project")

    new_project = Project(
        name="Test Project",
        code="tp",
        type=project_type,
        repository=data["test_repository"],
    )

    data["kwargs"]["project"] = new_project
    new_sequence = Sequence(**data["kwargs"])
    assert new_sequence.project == new_project


def test__hash__is_working_as_expected(setup_sequence_db_tests):
    """__hash__ is working as expected."""
    data = setup_sequence_db_tests
    result = hash(data["test_sequence"])
    assert isinstance(result, int)
    assert result == data["test_sequence"].__hash__()
