# -*- coding: utf-8 -*-
"""Tests for the Entity class."""

import copy

import pytest

from stalker import Entity, Note, Tag, User


@pytest.fixture(scope="function")
def setup_entity_tests():
    """Set up Entity class test data."""
    data = dict()
    # create a user
    data["test_user"] = User(
        name="Test User", login="testuser", email="test@user.com", password="test"
    )

    # create some test Tag objects, not necessarily needed but create them
    data["test_tag1"] = Tag(name="Test Tag 1")
    data["test_tag2"] = Tag(name="Test Tag 1")  # make it equal to tag1
    data["test_tag3"] = Tag(name="Test Tag 3")

    data["tags"] = [data["test_tag1"], data["test_tag2"]]

    # create a couple of test Note objects
    data["test_note1"] = Note(name="test note1", content="test note1")
    data["test_note2"] = Note(name="test note2", content="test note2")
    data["test_note3"] = Note(name="test note3", content="test note3")

    data["notes"] = [data["test_note1"], data["test_note2"]]

    data["kwargs"] = {
        "name": "Test Entity",
        "description": "This is a test entity, and this is a proper \
        description for it",
        "created_by": data["test_user"],
        "updated_by": data["test_user"],
        "tags": data["tags"],
        "notes": data["notes"],
    }

    # create a proper SimpleEntity to use it later in the tests
    data["test_entity"] = Entity(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_true():
    """__auto_name__ class attribute is set to False for Entity class."""
    assert Entity.__auto_name__ is True


def test_notes_argument_being_omitted(setup_entity_tests):
    """no error raised if omitted the notes argument."""
    data = setup_entity_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("notes")
    new_entity = Entity(**kwargs)
    assert isinstance(new_entity, Entity)


def test_notes_argument_is_set_to_none(setup_entity_tests):
    """notes attr is set to an empty list if the notes argument is set to None."""
    data = setup_entity_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["notes"] = None
    new_entity = Entity(**kwargs)
    assert new_entity.notes == []


def test_notes_attribute_is_set_to_none(setup_entity_tests):
    """TypeError is raised if the notes attribute is set to None."""
    data = setup_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_entity"].notes = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_notes_argument_set_to_something_other_than_a_list(setup_entity_tests):
    """TypeError is raised if setting the notes argument something other than a list."""
    data = setup_entity_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["notes"] = ["a string note"]
    with pytest.raises(TypeError) as cm:
        Entity(**kwargs)

    assert str(cm.value) == (
        "Entity.note should be a stalker.models.note.Note instance, "
        "not str: 'a string note'"
    )


def test_notes_attribute_set_to_something_other_than_a_list(setup_entity_tests):
    """TypeError is raised if setting the notes argument something other than a list."""
    data = setup_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_entity"].notes = ["a string note"]

    assert str(cm.value) == (
        "Entity.note should be a stalker.models.note.Note instance, "
        "not str: 'a string note'"
    )


def test_notes_argument_set_to_a_list_of_other_objects(setup_entity_tests):
    """TypeError is raised if notes argument is a list of non-Note objects."""
    data = setup_entity_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["notes"] = [1, 12.2, "this is a string"]

    with pytest.raises(TypeError) as cm:
        Entity(**kwargs)

    assert str(cm.value) == (
        "Entity.note should be a stalker.models.note.Note instance, not int: '1'"
    )


def test_notes_attribute_set_to_a_list_of_other_objects(setup_entity_tests):
    """TypeError is raised if notes attr set to a list of non Note objects."""
    data = setup_entity_tests
    test_value = [1, 12.2, "this is a string"]
    with pytest.raises(TypeError) as cm:
        data["test_entity"].notes = test_value

    assert str(cm.value) == (
        "Entity.note should be a stalker.models.note.Note instance, not int: '1'"
    )


def test_notes_attribute_works_properly(setup_entity_tests):
    """notes attribute works properly,"""
    data = setup_entity_tests
    test_value = [data["test_note3"]]
    data["test_entity"].notes = test_value
    assert data["test_entity"].notes == test_value


def test_notes_attribute_element_is_set_to_non_note_object(setup_entity_tests):
    """TypeError is raised if non-Note instance assigned to the notes list."""
    data = setup_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_entity"].notes[0] = 0

    assert str(cm.value) == (
        "Entity.note should be a stalker.models.note.Note instance, not int: '0'"
    )


def test_tags_argument_being_omitted(setup_entity_tests):
    """no error is raised if creating an entity without setting the tags argument."""
    data = setup_entity_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("tags")
    # this should work without errors
    new_entity = Entity(**kwargs)
    assert isinstance(new_entity, Entity)


def test_tags_argument_being_initialized_as_an_empty_list(setup_entity_tests):
    """nothing happens if tags argument an empty list."""
    data = setup_entity_tests
    # this should work without errors
    kwargs = copy.copy(data["kwargs"])
    kwargs.pop("tags")
    new_entity = Entity(**kwargs)
    expected_result = []
    assert new_entity.tags == expected_result


def test_tags_argument_set_to_something_other_than_a_list(setup_entity_tests):
    """TypeError is raised if tags arg is not a list."""
    data = setup_entity_tests
    kwargs = copy.copy(data["kwargs"])
    kwargs["tags"] = ["a tag", 1243, 12.12]
    with pytest.raises(TypeError) as cm:
        Entity(**kwargs)

    assert str(cm.value) == (
        "Entity.tag should be a stalker.models.tag.Tag instance, not str: 'a tag'"
    )


def test_tags_attribute_works_properly(setup_entity_tests):
    """tags attribute works properly."""
    data = setup_entity_tests
    test_value = [data["test_tag1"]]
    data["test_entity"].tags = test_value
    assert data["test_entity"].tags == test_value


def test_tags_attribute_element_is_set_to_non_tag_object(setup_entity_tests):
    """TypeError is raised if assign something to tags list that is not a Tag."""
    data = setup_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_entity"].tags[0] = 0

    assert str(cm.value) == (
        "Entity.tag should be a stalker.models.tag.Tag instance, not int: '0'"
    )


def test_tags_attribute_set_to_none(setup_entity_tests):
    """TypeError is raised if the tags attribute is set to None."""
    data = setup_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_entity"].tags = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_equality(setup_entity_tests):
    """equality of two entities."""
    data = setup_entity_tests
    # create two entities with same parameters and check for equality
    kwargs = copy.copy(data["kwargs"])

    entity1 = Entity(**kwargs)
    entity2 = Entity(**kwargs)

    kwargs["name"] = "another entity"
    kwargs["tags"] = [data["test_tag3"]]
    kwargs["notes"] = []
    entity3 = Entity(**kwargs)

    assert entity1 == entity2
    assert not entity1 == entity3


def test_inequality(setup_entity_tests):
    """inequality of two entities."""
    data = setup_entity_tests
    # change the tags and test it again, expect False
    kwargs = copy.copy(data["kwargs"])
    entity1 = Entity(**kwargs)
    entity2 = Entity(**kwargs)

    kwargs["name"] = "another entity"
    kwargs["tags"] = [data["test_tag3"]]
    kwargs["notes"] = []
    entity3 = Entity(**kwargs)

    assert not entity1 != entity2
    assert entity1 != entity3
