# -*- coding: utf-8 -*-

import unittest
import pytest
from stalker import Note


class NoteTester(unittest.TestCase):
    """tests  the Note class
    """

    def setUp(self):
        """setup the test
        """
        super(NoteTester, self).setUp()
        self.kwargs = {
            "name": "Note to something",
            "description": "this is a simple note",
            "content": "this is a note content",
        }

        # create a Note object
        self.test_note = Note(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for
        Note class
        """
        assert Note.__auto_name__ is True

    def test_content_argument_is_missing(self):
        """testing if nothing is going to happen when no content argument is
        given
        """
        self.kwargs.pop("content")
        new_note = Note(**self.kwargs)
        assert isinstance(new_note, Note)

    def test_content_argument_is_set_to_None(self):
        """testing if nothing is going to happen when content argument is given
        as None
        """
        self.kwargs["content"] = None
        new_note = Note(**self.kwargs)
        assert isinstance(new_note, Note)

    def test_content_attribute_is_set_to_None(self):
        """testing if nothing is going to happen when content attribute is set
        to None
        """
        # nothing should happen
        self.test_note.content = None

    def test_content_argument_is_set_to_empty_string(self):
        """testing if nothing is going to happen when content argument is given
        as an empty string
        """
        self.kwargs["content"] = ""
        Note(**self.kwargs)

    def test_content_attribute_is_set_to_empty_string(self):
        """testing if nothing is going to happen when content argument is set
        to an empty string
        """
        # nothing should happen
        self.test_note.content = ""

    def test_content_argument_is_set_to_something_other_than_a_string(self):
        """testing if a TypeError will be raised when trying to set the content
        argument to something other than a string
        """
        test_value = 1.24

        self.kwargs["content"] = test_value
        with pytest.raises(TypeError) as cm:
            Note(**self.kwargs)

        assert str(cm.value) == \
            'Note.description should be a string, not float'

    def test_content_attribute_is_set_to_something_other_than_a_string(self):
        """testing if a TypeError will be raised when trying to set the
        content attribute to something other than a string
        """
        test_value = 1

        with pytest.raises(TypeError) as cm:
            self.test_note.content = test_value

        assert str(cm.value) == \
            'Note.description should be a string, not int'

    def test_content_attribute_is_working_properly(self):
        """testing if the content attribute is working properly
        """
        new_content = "This is my new content for the note, and I expect it to\
        work fine when I assign it to a Note object"
        self.test_note.content = new_content
        assert self.test_note.content == new_content

    def test_equality_operator(self):
        """testing equality operator
        """
        note1 = Note(**self.kwargs)
        note2 = Note(**self.kwargs)

        self.kwargs["content"] = "this is a different content"
        note3 = Note(**self.kwargs)

        assert note1 == note2
        assert not note1 == note3

    def test_inequality_operator(self):
        """testing inequality operator
        """
        note1 = Note(**self.kwargs)
        note2 = Note(**self.kwargs)

        self.kwargs["content"] = "this is a different content"
        note3 = Note(**self.kwargs)

        assert not note1 != note2
        assert note1 != note3

    def test_plural_class_name(self):
        """testing the plural name of Note class
        """
        assert self.test_note.plural_class_name == "Notes"
