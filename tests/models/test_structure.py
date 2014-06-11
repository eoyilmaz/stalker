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
from stalker import Structure, FilenameTemplate, Type


# mock classes
class Asset(object):
    pass


class Shot(object):
    pass


class Link(object):
    pass


class StructureTester(unittest.TestCase):
    """tests the stalker.models.structure.Structure class
    """

    def setUp(self):
        """setting up the tests
        """

        vers_type = Type(
            name="Version",
            code='vers',
            target_entity_type="FilenameTemplate"
        )

        ref_type = Type(
            name="Reference",
            code='ref',
            target_entity_type="FilenameTemplate"
        )

        # type templates
        self.asset_template = FilenameTemplate(
            name="Test Asset Template",
            target_entity_type="Asset",
            type=vers_type
        )

        self.shot_template = FilenameTemplate(
            name="Test Shot Template",
            target_entity_type="Shot",
            type=vers_type
        )

        self.reference_template = FilenameTemplate(
            name="Test Reference Template",
            target_entity_type="Link",
            type=ref_type
        )

        self.test_templates = [self.asset_template,
                               self.shot_template,
                               self.reference_template]

        self.test_templates2 = [self.asset_template]

        self.custom_template = "a custom template"

        self.test_type = Type(
            name="Commercial Structure",
            code='comm',
            target_entity_type=Structure,
        )

        # keyword arguments
        self.kwargs = {
            "name": "Test Structure",
            "description": "This is a test structure",
            "templates": self.test_templates,
            "custom_template": self.custom_template,
            "type": self.test_type,
        }
        self.test_structure = Structure(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Structure class
        """
        self.assertFalse(Structure.__auto_name__)

    def test_custom_template_argument_can_be_skipped(self):
        """testing if the custom_template argument can be skipped
        """
        self.kwargs.pop("custom_template")
        new_structure = Structure(**self.kwargs)
        self.assertEqual(new_structure.custom_template, "")

    def test_custom_template_argument_is_None(self):
        """testing if no error will be raised when the custom_template argument
        is None.
        """
        self.kwargs["custom_template"] = None
        new_structure = Structure(**self.kwargs)
        self.assertEqual(new_structure.custom_template, "")

    def test_custom_template_argument_is_empty_string(self):
        """testing if no error will be raised when the custom_template argument
        is an empty string
        """
        self.kwargs["custom_template"] = ""
        new_structure = Structure(**self.kwargs)
        self.assertEqual(new_structure.custom_template, "")

    def test_custom_template_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the custom_template
        argument is not a string
        """
        self.kwargs['custom_template'] = ["this is not a string"]
        self.assertRaises(TypeError, Structure, **self.kwargs)

    def test_custom_template_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the custom_template
        attribute is not a string
        """
        self.assertRaises(TypeError, setattr, self.test_structure,
                          'custom_template', ['this is not a string'])

    def test_templates_argument_can_be_skipped(self):
        """testing if no error will be raised when the templates argument is
        skipped
        """
        self.kwargs.pop("templates")
        new_structure = Structure(**self.kwargs)
        self.assertTrue(isinstance(new_structure, Structure))

    def test_templates_argument_can_be_None(self):
        """testing if no error will be raised when the templates argument is
        None
        """
        self.kwargs["templates"] = None
        new_structure = Structure(**self.kwargs)
        self.assertTrue(isinstance(new_structure, Structure))

    def test_templates_attribute_cannot_be_set_to_None(self):
        """testing if a TypeError will be raised when the templates attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_structure, "templates",
                          None)

    def test_templates_argument_only_accepts_list(self):
        """testing if a TypeError will be raised when the given templates
        argument is not a list
        """
        self.kwargs["templates"] = 1
        self.assertRaises(TypeError, Structure, **self.kwargs)

    def test_templates_attribute_only_accepts_list(self):
        """testing if a TypeError will be raised when the templates attribute
        is tried to be set to an object which is not a list instance.
        """
        self.assertRaises(TypeError, setattr, self.test_structure, "templates",
                          1.121)
        # test the correct value
        self.test_structure.templates = self.test_templates

    def test_templates_argument_accepts_only_list_of_FilenameTemplate_instances(self):
        """testing if a TypeError will be raised when the templates argument is
        a list but the elements are not all instances of FilenameTemplate
        class.
        """
        test_value = [1, 1.2, "a string"]
        self.kwargs["templates"] = test_value
        self.assertRaises(TypeError, Structure, **self.kwargs)

        # test the correct value
        self.kwargs["templates"] = self.test_templates
        new_structure = Structure(**self.kwargs)
        self.assertTrue(isinstance(new_structure, Structure))

    def test_templates_attribute_accpets_only_list_of_FilenameTemplate_instances(self):
        """testing if a TypeError will be raised when the templates attribute
        is a list but the elements are not all instances of FilenameTemplate
        class.
        """
        test_value = [1, 1.2, "a string"]
        self.assertRaises(TypeError, setattr, self.test_structure, "templates",
                          test_value)

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ is False
        """
        self.assertEqual(Structure.__strictly_typed__, False)

    def test_equality_operator(self):
        """testing equality of two Structure objects
        """
        new_structure2 = Structure(**self.kwargs)

        self.kwargs["custom_template"] = "a test custom template"
        new_structure3 = Structure(**self.kwargs)

        self.kwargs["custom_template"] = self.test_structure.custom_template
        self.kwargs["templates"] = self.test_templates2
        new_structure4 = Structure(**self.kwargs)

        self.assertTrue(self.test_structure == new_structure2)
        self.assertFalse(self.test_structure == new_structure3)
        self.assertFalse(self.test_structure == new_structure4)

    def test_inequality_operator(self):
        """testing inequality of two Structure objects
        """
        new_structure2 = Structure(**self.kwargs)

        self.kwargs["custom_template"] = "a test custom template"
        new_structure3 = Structure(**self.kwargs)

        self.kwargs["custom_template"] = self.test_structure.custom_template
        self.kwargs["templates"] = self.test_templates2
        new_structure4 = Structure(**self.kwargs)

        self.assertFalse(self.test_structure != new_structure2)
        self.assertTrue(self.test_structure != new_structure3)
        self.assertTrue(self.test_structure != new_structure4)

    def test_plural_class_name(self):
        """testing the plural name of Structure class
        """
        self.assertTrue(self.test_structure.plural_class_name, "Structures")

    # def test_hash_value(self):
    #     """testing if the hash value is correctly calculated
    #     """
    #     self.assertEqual(
    #         hash(self.test_structure),
    #         hash(self.test_structure.id) +
    #         2 * hash(self.test_structure.name) +
    #         3 * hash(self.test_structure.entity_type)
    #     )
