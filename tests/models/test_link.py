# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
from stalker import Type, Link

class LinkTester(unittest.TestCase):
    """tests the :class:`stalker.core.models.Link` class
    """
    def setUp(self):
        """setup the test 
        """
        # create a mock LinkType object
        self.test_link_type1 = Type(
            name="Test Type 1",
            target_entity_type=Link,
            )
        self.test_link_type2 = Type(
            name="Test Type 2",
            target_entity_type=Link,
            )

        self.kwargs = {
            "name": "An Image Link",
            "path": "C:/A_NEW_PROJECT/",
            "filename": "this_is_an_image.jpg",
            "type": self.test_link_type1
        }

        self.test_link = Link(**self.kwargs)

    def test_path_argument_accepts_string_or_unicode_only(self):
        """testing if a TypeError will be raised when the path argument is not
        a string or unicode instance
        """
        test_values = [1, 1.1, ["a path"], {"a": "path"}]

        for test_value in test_values:
            self.kwargs["path"] = test_value
            self.assertRaises(TypeError, Link, **self.kwargs)

    def test_path_attribute_accpets_string_or_unicode_only(self):
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

        #
        #def test_filename_argument_accepts_string_or_unicode_only(self):
        #"""testing if filename argument accepts string or unicode only and
        #raises TypeError otherwise
        #"""

        #test_values = [1, 1.1, ["a filename"], {"a": "filename"}]

        #for test_value in test_values:
        #self.kwargs["filename"] = test_value
        #self.assertRaises(TypeError, Link, **self.kwargs)

        #
        #def test_filename_attribute_accpets_string_or_unicode_only(self):
        #"""testing if filename attribute accepts string or unicode only and
        #raises TypeError otherwise
        #"""

        #test_values = [1, 1.1, ["a filename"], {"a": "filename"}]

        #for test_value in test_values:
        #self.assertRaises(
        #TypeError,
        #setattr,
        #self.test_link,
        #"filename",
        #test_value
        #)

        #def test_filename_argument_being_empty(self):
        #"""testing if setting the filename argument to an empty string raises a
        #ValueError
        #"""
        #self.kwargs["filename"] = ""
        #self.assertRaises(ValueError, Link, **self.kwargs)

        #def test_filename_attribute_being_empty(self):
        #"""testing if setting the filename attribute to an empty string raises
        #a ValueError
        #"""
        #self.assertRaises(
        #ValueError,
        #setattr,
        #self.test_link,
        #"filename",
        #""
        #)
        
        #def test_filename_argument_being_None(self):
        #"""testing if setting the filename argument to None raises a TypeError
        #"""
        #self.kwargs["filename"] = None
        #self.assertRaises(TypeError, Link, **self.kwargs)

        #def test_filename_attribute_being_None(self):
        #"""testing if setting the filename attribute to None raises a
        #TypeError
        #"""
        #self.assertRaises(
        #TypeError,
        #setattr,
        #self.test_link,
        #"filename",
        #None
        #)

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

        #def test_plural_name(self):
        #"""testing the plural name of Link class
        #"""
        #self.assertTrue(Link.plural_name, "Links")

        #def test___strictly_typed___is_True(self):
        #"""testing if the __strictly_typed__ class attribute is True
        #"""
        #self.assertEqual(Link.__strictly_typed__, True)
