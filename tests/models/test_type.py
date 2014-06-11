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
from stalker import Entity, Type


class TypeTester(unittest.TestCase):
    """Tests Type class
    """

    def setUp(self):
        """set up the test
        """
        self.kwargs = {
            "name": "test type",
            'code': 'test',
            "description": "this is a test type",
            "target_entity_type": "SimpleEntity"
        }

        self.test_type = Type(**self.kwargs)

        # create another Entity with the same name of the
        # test_type for __eq__ and __ne__ tests
        self.entity1 = Entity(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Ticket class
        """
        self.assertFalse(Type.__auto_name__)

    def test_equality(self):
        """testing the equality operator
        """
        new_type2 = Type(**self.kwargs)

        self.kwargs["target_entity_type"] = "Asset"
        new_type3 = Type(**self.kwargs)

        self.kwargs["name"] = "a different type"
        self.kwargs["description"] = "this is a different type"
        new_type4 = Type(**self.kwargs)

        self.assertTrue(self.test_type == new_type2)
        self.assertFalse(self.test_type == new_type3)
        self.assertFalse(self.test_type == new_type4)
        self.assertFalse(self.test_type == self.entity1)

    def test_inequality(self):
        """testing the inequality operator
        """
        new_type2 = Type(**self.kwargs)

        self.kwargs["target_entity_type"] = "Asset"
        new_type3 = Type(**self.kwargs)

        self.kwargs["name"] = "a different type"
        self.kwargs["description"] = "this is a different type"
        new_type4 = Type(**self.kwargs)

        self.assertFalse(self.test_type != new_type2)
        self.assertTrue(self.test_type != new_type3)
        self.assertTrue(self.test_type != new_type4)
        self.assertTrue(self.test_type != self.entity1)

    def test_plural_class_name(self):
        """testing the plural name of Type class
        """
        self.assertTrue(self.test_type.plural_class_name, "Types")

    def test_target_entity_type_argument_can_not_be_skipped(self):
        """testing if a TypeError will be raised when the created Type doesn't
        have any target_entity_type
        """
        self.kwargs.pop("target_entity_type")
        self.assertRaises(TypeError, Type, **self.kwargs)

    def test_target_entity_type_argument_can_not_be_None(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is None
        """
        self.kwargs["target_entity_type"] = None
        self.assertRaises(TypeError, Type, **self.kwargs)

    def test_target_entity_type_argument_can_not_be_empty_string(self):
        """testing if a ValueError will be raised when the target_entity_type
        argument is an empty string
        """
        self.kwargs["target_entity_type"] = ""
        self.assertRaises(ValueError, Type, **self.kwargs)

    def test_target_entity_type_argument_accepts_strings(self):
        """testing if target_entity_type argument accepts strings
        """
        self.kwargs["target_entity_type"] = "Asset"
        # no error should be raised
        Type(**self.kwargs)

    def test_target_entity_type_argument_accepts_Python_classes(self):
        """testing if target_entity_type argument is given as a Python class
        will be converted to a string
        """
        from stalker.models.asset import Asset

        self.kwargs["target_entity_type"] = Asset
        new_type = Type(**self.kwargs)
        self.assertEqual(new_type.target_entity_type, "Asset")

    def test_target_entity_type_attribute_is_read_only(self):
        """testing if the target_entity_type attribute is read-only
        """
        self.assertRaises(AttributeError, setattr, self.test_type,
                          "target_entity_type", "Asset")

    def test_target_entity_type_attribute_is_working_properly(self):
        """testing if the target_entity_type attribute is working properly
        """
        self.assertEqual(self.test_type.target_entity_type,
                         self.kwargs["target_entity_type"])

    # def test_hash_value(self):
    #     """testing if the hash value is correctly calculated
    #     """
    #     self.assertEqual(
    #         hash(self.test_type),
    #         hash(self.test_type.id) +
    #         2 * hash(self.test_type.name) +
    #         3 * hash(self.test_type.entity_type)
    #     )
