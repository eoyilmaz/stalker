# -*- coding: utf-8 -*-
"""Tests for the Not class."""

import pytest

from stalker import Note


@pytest.fixture(scope="function")
def setup_note_tests():
    """Set up the test Note related tests."""
    data = dict()
    data["kwargs"] = {
        "name": "Note to something",
        "description": "this is a simple note",
        "content": "this is a note content",
    }
    # create a Note object
    data["test_note"] = Note(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_true():
    """__auto_name__ class attribute is set to True for Note class."""
    assert Note.__auto_name__ is True


def test_content_argument_is_missing(setup_note_tests):
    """Nothing is going to happen if no content argument is given."""
    data = setup_note_tests
    data["kwargs"].pop("content")
    new_note = Note(**data["kwargs"])
    assert isinstance(new_note, Note)


def test_content_argument_is_set_to_none(setup_note_tests):
    """nothing is going to happen if content argument is given as None."""
    data = setup_note_tests
    data["kwargs"]["content"] = None
    new_note = Note(**data["kwargs"])
    assert isinstance(new_note, Note)


def test_content_attribute_is_set_to_none(setup_note_tests):
    """nothing is going to happen if content attribute is set to None."""
    data = setup_note_tests
    # nothing should happen
    data["test_note"].content = None


def test_content_argument_is_set_to_empty_string(setup_note_tests):
    """nothing is going to happen if content argument is given as an empty string."""
    data = setup_note_tests
    data["kwargs"]["content"] = ""
    Note(**data["kwargs"])


def test_content_attribute_is_set_to_empty_string(setup_note_tests):
    """nothing is going to happen if content argument is set to an empty string."""
    data = setup_note_tests
    # nothing should happen
    data["test_note"].content = ""


def test_content_argument_is_set_to_something_other_than_a_string(setup_note_tests):
    """TypeError is raised if content arg is not a str."""
    data = setup_note_tests
    test_value = 1.24
    data["kwargs"]["content"] = test_value
    with pytest.raises(TypeError) as cm:
        Note(**data["kwargs"])
    assert str(cm.value) == "Note.description should be a string, not float"


def test_content_attribute_is_set_to_something_other_than_a_string(setup_note_tests):
    """TypeError is raised if content attr is not a string."""
    data = setup_note_tests
    test_value = 1
    with pytest.raises(TypeError) as cm:
        data["test_note"].content = test_value
    assert str(cm.value) == "Note.description should be a string, not int"


def test_content_attribute_is_working_properly(setup_note_tests):
    """content attribute is working properly."""
    data = setup_note_tests
    new_content = (
        "This is my new content for the note, and I expect it to "
        "work fine if I assign it to a Note object"
    )
    data["test_note"].content = new_content
    assert data["test_note"].content == new_content


def test_equality_operator(setup_note_tests):
    """Equality operator."""
    data = setup_note_tests
    note1 = Note(**data["kwargs"])
    note2 = Note(**data["kwargs"])
    data["kwargs"]["content"] = "this is a different content"
    note3 = Note(**data["kwargs"])
    assert note1 == note2
    assert not note1 == note3


def test_inequality_operator(setup_note_tests):
    """Inequality operator."""
    data = setup_note_tests
    note1 = Note(**data["kwargs"])
    note2 = Note(**data["kwargs"])
    data["kwargs"]["content"] = "this is a different content"
    note3 = Note(**data["kwargs"])
    assert not note1 != note2
    assert note1 != note3


def test_plural_class_name(setup_note_tests):
    """plural name of Note class."""
    data = setup_note_tests
    assert data["test_note"].plural_class_name == "Notes"
