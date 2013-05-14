# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
# 
# This file is part of Stalker.
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
import os

import unittest2
from stalker import Type, Link


class LinkTester(unittest2.TestCase):
    """tests the :class:`stalker.models.link.Link` class
    """

    def setUp(self):
        """setup the test 
        """
        # create a mock LinkType object
        self.test_link_type1 = Type(
            name="Test Type 1",
            code='test type1',
            target_entity_type=Link,
        )
        self.test_link_type2 = Type(
            name="Test Type 2",
            code='test type2',
            target_entity_type=Link,
        )

        self.kwargs = {
            "name": "An Image Link",
            "path": "C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3",
            "original_filename": "this_is_an_image.jpg",
            "type": self.test_link_type1
        }

        self.test_link = Link(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to False for
        Link class
        """
        self.assertTrue(Link.__auto_name__)

    def test_path_argument_accepts_string_or_unicode_only(self):
        """testing if a TypeError will be raised when the path argument is not
        a string or unicode instance
        """
        test_values = [1, 1.1, ["a path"], {"a": "path"}]

        for test_value in test_values:
            self.kwargs["path"] = test_value
            self.assertRaises(TypeError, Link, **self.kwargs)

    def test_path_attribute_accepts_string_or_unicode_only(self):
        """testing if a TypeError will be raised when the path attribute
        is not a string or unicode instance
        """
        test_values = [1, 1.1, ["a path"], {"a": "path"}]

        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_link,
                "path",
                test_value
            )

    def test_path_argument_being_empty(self):
        """testing if setting the path argument to an empty string raises a
        ValueError
        """
        self.kwargs["path"] = ""
        self.assertRaises(ValueError, Link, **self.kwargs)

    def test_path_attribute_being_empty(self):
        """testing if setting the path attribute to an empty string raises a
        ValueError
        """
        self.assertRaises(
            ValueError,
            setattr,
            self.test_link,
            "path",
            ""
        )

    def test_path_argument_being_None(self):
        """testing if setting the path argument to None raises a TypeError
        """
        self.kwargs["path"] = None
        self.assertRaises(TypeError, Link, **self.kwargs)

    def test_path_attribute_being_None(self):
        """testing if setting the path attribute to None raises a TypeError
        """

        self.assertRaises(
            TypeError,
            setattr,
            self.test_link,
            "path",
            None
        )

    def test_path_windows_to_other_conversion(self):
        """testing if the path is stored in internal format
        """
        windows_path = "M:\\path\\to\\object"
        expected_result = "M:/path/to/object"

        self.test_link.path = windows_path
        self.assertEqual(self.test_link.path, expected_result)


    def test_original_filename_argument_is_None(self):
        """testing if the original_filename attribute value will be set to the
        filename part of the path attribute if the original_filename argument
        is None
        """
        self.kwargs["original_filename"] = None
        new_link = Link(**self.kwargs)
        filename = os.path.basename(new_link.path)
        self.assertEqual(new_link.original_filename, filename)

    def test_original_filename_attribute_is_set_to_None(self):
        """testing if the original_filename attribute value will be equal to
        the filename part of the path if it is set to None
        """
        self.test_link.original_filename = None
        filename = os.path.basename(self.test_link.path)
        self.assertEqual(self.test_link.original_filename, filename)

    def test_original_filename_argument_is_empty_string(self):
        """testing if setting the original_filename argument to an empty string
        will set the original_filename attribute value to the filename part of
        the path
        """
        self.kwargs["original_filename"] = ""
        new_link = Link(**self.kwargs)
        filename = os.path.basename(new_link.path)
        self.assertEqual(new_link.original_filename, filename)

    def test_original_filename_attribute_set_to_empty_string(self):
        """testing if setting the original_filename attribute to an empty
        string will set its value to filename part of the path attribute
        """
        self.test_link.original_filename = ''
        filename = os.path.basename(self.test_link.path)
        self.assertEqual(self.test_link.original_filename, filename)

    def test_original_filename_argument_accepts_string_or_unicode_only(self):
        """testing if original_filename argument accepts string or unicode only
        and raises TypeError for other types
        """
        test_values = [1, 1.1, ["a original_filename"],
                       {"a": "original_filename"}]
        for test_value in test_values:
            self.kwargs["original_filename"] = test_value
            self.assertRaises(TypeError, Link, **self.kwargs)

    def test_original_filename_attribute_accepts_string_or_unicode_only(self):
        """testing if original_filename attribute accepts string or unicode
        only and raises TypeError for other types
        """
        test_values = [1, 1.1, ["a original_filename"],
                       {"a": "original_filename"}]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_link,
                "original_filename",
                test_value
            )

    def test_original_filename_argument_is_working_properly(self):
        """testing if the original_filename argument is working properly
        """
        self.assertEqual(
            self.kwargs['original_filename'],
            self.test_link.original_filename
        )

    def test_original_filename_attribute_is_working_properly(self):
        """testing if the original_filename attribute is working properly
        """
        new_value = 'this_is_the_original_filename.jpg'
        self.assertNotEqual(
            self.test_link.original_filename,
            new_value
        )
        self.test_link.original_filename = new_value
        self.assertEqual(
            self.test_link.original_filename,
            new_value
        )

    def test_equality_of_two_links(self):
        """testing the equality operator
        """
        # with same parameters
        mock_link1 = Link(**self.kwargs)
        self.assertTrue(self.test_link == mock_link1)

        # with different parameters
        self.kwargs["type"] = self.test_link_type2
        mock_link2 = Link(**self.kwargs)

        self.assertFalse(self.test_link == mock_link2)

    def test_inequality_of_two_links(self):
        """testing the inequality operator
        """
        # with same parameters
        mock_link1 = Link(**self.kwargs)
        self.assertTrue(self.test_link == mock_link1)

        # with different parameters
        self.kwargs["type"] = self.test_link_type2
        mock_link2 = Link(**self.kwargs)

        self.assertFalse(self.test_link != mock_link1)
        self.assertTrue(self.test_link != mock_link2)

    def test_plural_class_name(self):
        """testing the plural name of Link class
        """
        self.assertEqual(self.test_link.plural_class_name, "Links")

    # def test___strictly_typed___is_True(self):
        # """testing if the __strictly_typed__ class attribute is True
        # """
        # self.assertEqual(Link.__strictly_typed__, True)
