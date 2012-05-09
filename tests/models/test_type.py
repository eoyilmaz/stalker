# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

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
            "description": "this is a test type",
            "target_entity_type": "SimpleEntity"
        }

        self.test_type = Type(**self.kwargs)

        # create another Entity with the same name of the
        # test_type for __eq__ and __ne__ tests
        self.entity1 = Entity(**self.kwargs)


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



        #
        #def test_plural_name(self):
        #"""testing the plural name of Entities class
        #"""

        #self.assertTrue(Entity.plural_name, "Entities")


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
        new_type = Type(**self.kwargs)


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
    
    
    
