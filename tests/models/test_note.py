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
from stalker import Note


class NoteTester(UnitTestBase):
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
        self.assertTrue(Note.__auto_name__)

    def test_content_argument_is_missing(self):
        """testing if nothing is going to happen when no content argument is
        given
        """
        self.kwargs.pop("content")
        new_note = Note(**self.kwargs)
        self.assertTrue(isinstance(new_note, Note))

    def test_content_argument_is_set_to_None(self):
        """testing if nothing is going to happen when content argument is given
        as None
        """
        self.kwargs["content"] = None
        new_note = Note(**self.kwargs)
        self.assertTrue(isinstance(new_note, Note))

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
        with self.assertRaises(TypeError) as cm:
            Note(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Note.description should be a string, not float'
        )

    def test_content_attribute_is_set_to_something_other_than_a_string(self):
        """testing if a TypeError will be raised when trying to set the
        content attribute to something other than a string
        """
        test_value = 1

        with self.assertRaises(TypeError) as cm:
            self.test_note.content = test_value

        self.assertEqual(
            str(cm.exception),
            'Note.description should be a string, not int'
        )

    def test_content_attribute_is_working_properly(self):
        """testing if the content attribute is working properly
        """
        new_content = "This is my new content for the note, and I expect it to\
        work fine when I assign it to a Note object"
        self.test_note.content = new_content
        self.assertEqual(self.test_note.content, new_content)

    def test_equality_operator(self):
        """testing equality operator
        """
        note1 = Note(**self.kwargs)
        note2 = Note(**self.kwargs)

        self.kwargs["content"] = "this is a different content"
        note3 = Note(**self.kwargs)

        self.assertTrue(note1 == note2)
        self.assertFalse(note1 == note3)

    def test_inequality_operator(self):
        """testing inequality operator
        """
        note1 = Note(**self.kwargs)
        note2 = Note(**self.kwargs)

        self.kwargs["content"] = "this is a different content"
        note3 = Note(**self.kwargs)

        self.assertFalse(note1 != note2)
        self.assertTrue(note1 != note3)

    def test_plural_class_name(self):
        """testing the plural name of Note class
        """
        self.assertTrue(self.test_note.plural_class_name, "Notes")
