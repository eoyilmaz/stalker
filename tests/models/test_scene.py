# -*- coding: utf-8 -*-
"""Tests for the Scene class."""

import pytest

from stalker import Entity, Project, Repository, Scene, Type
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_scene_db_tests(setup_postgresql_db):
    """Set up the Scene tests with a DB."""
    data = dict()
    # create a test project, user and a couple of shots
    data["project_type"] = Type(
        name="Test Project Type",
        code="test",
        target_entity_type="Project",
    )

    # create a repository
    data["repository_type"] = Type(
        name="Test Type", code="test", target_entity_type="Repository"
    )

    data["test_repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["repository_type"],
    )

    # create projects
    data["test_project"] = Project(
        name="Test Project 1",
        code="tp1",
        type=data["project_type"],
        repository=data["test_repository"],
    )

    data["test_project2"] = Project(
        name="Test Project 2",
        code="tp2",
        type=data["project_type"],
        repository=data["test_repository"],
    )

    # the parameters
    data["kwargs"] = {
        "name": "Test Scene",
        "code": "tsce",
        "description": "A test scene",
        "project": data["test_project"],
    }

    # the test sequence
    data["test_scene"] = Scene(**data["kwargs"])
    DBSession.add(data["test_scene"])
    DBSession.commit()
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Scene class."""
    assert Scene.__auto_name__ is False


def test_shots_attribute_defaults_to_empty_list(setup_scene_db_tests):
    """shots attribute defaults to an empty list."""
    data = setup_scene_db_tests
    new_scene = Scene(**data["kwargs"])
    assert new_scene.shots == []


def test_shots_attribute_is_set_none(setup_scene_db_tests):
    """TypeError is raised if the shots attribute is set to None."""
    data = setup_scene_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_scene"].shots = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_shots_attribute_is_set_to_other_than_a_list(setup_scene_db_tests):
    """TypeError is raised if the shots attr is not a list."""
    data = setup_scene_db_tests
    test_value = [1, 1.2, "a string"]
    with pytest.raises(TypeError) as cm:
        data["test_scene"].shots = test_value
    assert str(cm.value) == (
        "Scene.shots needs to be all stalker.models.shot.Shot instances, not int: '1'"
    )


def test_shots_attribute_is_a_list_of_other_objects(setup_scene_db_tests):
    """TypeError raised if the shots argument is a list of other type of objects."""
    data = setup_scene_db_tests
    test_value = [1, 1.2, "a string"]
    with pytest.raises(TypeError) as cm:
        data["test_scene"].shots = test_value
    assert str(cm.value) == (
        "Scene.shots needs to be all stalker.models.shot.Shot instances, not int: '1'"
    )


def test_shots_attribute_elements_tried_to_be_set_to_non_shot_object(
    setup_scene_db_tests,
):
    """TypeError raised if shots list appended a not Shot instance."""
    data = setup_scene_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_scene"].shots.append("a string")
    assert str(cm.value) == (
        "Scene.shots needs to be all stalker.models.shot.Shot instances, "
        "not str: 'a string'"
    )


def test_equality(setup_scene_db_tests):
    """equality of scenes."""
    data = setup_scene_db_tests
    new_seq1 = Scene(**data["kwargs"])
    new_seq2 = Scene(**data["kwargs"])
    new_entity = Entity(**data["kwargs"])

    data["kwargs"]["name"] = "a different scene"
    new_seq3 = Scene(**data["kwargs"])

    assert new_seq1 == new_seq2
    assert not new_seq1 == new_seq3
    assert not new_seq1 == new_entity


def test_inequality(setup_scene_db_tests):
    """inequality of scenes."""
    data = setup_scene_db_tests
    new_seq1 = Scene(**data["kwargs"])
    new_seq2 = Scene(**data["kwargs"])
    new_entity = Entity(**data["kwargs"])

    data["kwargs"]["name"] = "a different scene"
    new_seq3 = Scene(**data["kwargs"])

    assert not new_seq1 != new_seq2
    assert new_seq1 != new_seq3
    assert new_seq1 != new_entity


def test_project_mixin_initialization(setup_scene_db_tests):
    """ProjectMixin part is initialized correctly."""
    data = setup_scene_db_tests
    project_type = Type(name="Commercial", code="comm", target_entity_type="Project")

    new_project = Project(
        name="Test Project",
        code="tp",
        type=project_type,
        repository=data["test_repository"],
    )

    data["kwargs"]["project"] = new_project
    new_scene = Scene(**data["kwargs"])
    assert new_scene.project == new_project


def test___strictly_typed___is_false():
    """__strictly_typed__ class attribute is False for Scene class."""
    assert Scene.__strictly_typed__ is False
