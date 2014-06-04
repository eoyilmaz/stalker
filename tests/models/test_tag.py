# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import unittest
from stalker import Tag, SimpleEntity


class TagTest(unittest.TestCase):
    """testing the Tag class
    """

    def setUp(self):
        """setup the test
        """
        self.kwargs = {
            "name": "a test tag",
            "description": "this is a test tag",
        }

        # create another SimpleEntity with kwargs for __eq__ and __ne__ tests
        self.simple_entity = SimpleEntity(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_false(self):
        """testing if the __auto_name__ class attribute is set to False for Tag
        class
        """
        self.assertFalse(Tag.__auto_name__)

    def test_tag_init(self):
        """testing if tag inits properly
        """
        # this should work without any error
        tag = Tag(**self.kwargs)
        self.assertTrue(isinstance(tag, Tag))

    def test_equality(self):
        """testing the equality of two Tags
        """
        a_tag_object1 = Tag(**self.kwargs)
        a_tag_object2 = Tag(**self.kwargs)

        self.kwargs["name"] = "a new test Tag"
        self.kwargs["description"] = "this is a new test Tag"

        a_tag_object3 = Tag(**self.kwargs)

        self.assertTrue(a_tag_object1 == a_tag_object2)
        self.assertFalse(a_tag_object1 == a_tag_object3)
        self.assertFalse(a_tag_object1 == self.simple_entity)

    def test_inequality(self):
        """testing the inequality of two Tags
        """
        a_tag_object1 = Tag(**self.kwargs)
        a_tag_object2 = Tag(**self.kwargs)

        self.kwargs["name"] = "a new test Tag"
        self.kwargs["description"] = "this is a new test Tag"

        a_tag_object3 = Tag(**self.kwargs)

        self.assertFalse(a_tag_object1 != a_tag_object2)
        self.assertTrue(a_tag_object1 != a_tag_object3)
        self.assertTrue(a_tag_object1 != self.simple_entity)

    def test_plural_class_name(self):
        """testing the plural name of Tag class
        """
        test_tag = Tag(**self.kwargs)
        self.assertTrue(test_tag.plural_class_name, "Tags")
