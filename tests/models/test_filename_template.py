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
from stalker import Entity, FilenameTemplate, Type


# a test class
class Asset(object):
    pass


class FilenameTemplateTester(unittest.TestCase):
    """tests the stalker.models.template.FilenameTemplate class
    """

    def setUp(self):
        """setup the test
        """
        self.kwargs = {
            "name": "Test FilenameTemplate",
            "type": Type(
                name="Test Type",
                code='tt',
                target_entity_type="FilenameTemplate"
            ),
            "path": "ASSETS/{{asset.code}}/{{task.type.code}}/",
            "filename": "{{asset.code}}_{{version.take}}_{{task.type.code}}_" \
                        "{{version.version}}_{{user.initials}}",
            "output_path": "",
            "target_entity_type": Asset,
        }
        self.filename_template = FilenameTemplate(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Asset class
        """
        self.assertFalse(FilenameTemplate.__auto_name__)

    def test_filename_template_is_not_strictly_typed(self):
        """testing if the FilenameTemplate class is not strictly typed
        """
        self.kwargs.pop("type")
        # no errors
        ft = FilenameTemplate(**self.kwargs)
        self.assertTrue(isinstance(ft, FilenameTemplate))

    def test_target_entity_type_argument_is_skipped(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is skipped
        """
        self.kwargs.pop("target_entity_type")
        self.assertRaises(TypeError, FilenameTemplate, **self.kwargs)

    def test_target_entity_type_argument_is_None(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is given as None
        """
        self.kwargs["target_entity_type"] = None
        self.assertRaises(TypeError, FilenameTemplate, **self.kwargs)

    def test_target_entity_type_attribute_is_read_only(self):
        """testing if a AttributeError will be raised when the
        target_entity_type attribute is tried to be changed
        """
        self.assertRaises(AttributeError, setattr, self.filename_template,
                          "target_entity_type", "Asset")

    def test_target_entity_type_argument_accepts_Classes(self):
        """testing if the target_entity_type can be set to a class directly
        """
        self.kwargs["target_entity_type"] = Asset
        new_filenameTemplate = FilenameTemplate(**self.kwargs)

    def test_target_entity_type_attribute_is_converted_to_a_string_if_given_as_a_class(self):
        """testing if the target_entity_type attribute is converted when the
        target_entity_type is given as a class
        """
        self.kwargs["target_entity_type"] = Asset
        ft = FilenameTemplate(**self.kwargs)
        self.assertEqual(ft.target_entity_type, "Asset")

    def test_path_argument_is_skipped(self):
        """testing if nothing happens when the path argument is skipped
        """
        self.kwargs.pop("path")
        ft = FilenameTemplate(**self.kwargs)
        self.assertTrue(isinstance(ft, FilenameTemplate))

    def test_path_argument_skipped_path_attribute_is_empty_string(self):
        """testing if the path attribute is an empty string if the
        path argument is skipped
        """
        self.kwargs.pop("path")
        ft = FilenameTemplate(**self.kwargs)
        self.assertEqual(ft.path, "")

    def test_path_argument_is_None_path_attribute_is_empty_string(self):
        """testing if the path attribute is an empty string when the
        path argument is None
        """
        self.kwargs["path"] = None
        ft = FilenameTemplate(**self.kwargs)
        self.assertEqual(ft.path, "")

    def test_path_argument_is_empty_string(self):
        """testing if nothing happens when the path argument is empty
        string
        """
        self.kwargs["path"] = ""
        ft = FilenameTemplate(**self.kwargs)
        self.assertTrue(isinstance(ft, FilenameTemplate))

    def test_path_attribute_is_empty_string(self):
        """testing if nothing happens when the path attribute is set to
        empty string
        """
        self.filename_template.path = ""

    def test_path_argument_is_not_string(self):
        """testing if a TypeError will be raised when the path argument is not
        a string
        """
        test_value = list("a list from a string")
        self.kwargs["path"] = test_value
        self.assertRaises(TypeError, FilenameTemplate, **self.kwargs)

    def test_path_attribute_is_not_string(self):
        """testing if a TypeError will be raised when the path attribute is not
        set to a string
        """
        test_value = list("a list from a string")
        self.assertRaises(TypeError, setattr, self.filename_template, "path",
                          test_value)

    def test_filename_argument_is_skipped(self):
        """testing if nothing happens when the filename argument is skipped
        """
        self.kwargs.pop("filename")
        ft = FilenameTemplate(**self.kwargs)
        self.assertTrue(isinstance(ft, FilenameTemplate))

    def test_filename_argument_skipped_filename_attribute_is_empty_string(self):
        """testing if the filename attribute is an empty string if the
        filename argument is skipped
        """
        self.kwargs.pop("filename")
        ft = FilenameTemplate(**self.kwargs)
        self.assertEqual(ft.filename, "")

    def test_filename_argument_is_None_filename_attribute_is_empty_string(self):
        """testing if the filename attribute is an empty string when the
        filename argument is None
        """
        self.kwargs["filename"] = None
        ft = FilenameTemplate(**self.kwargs)
        self.assertEqual(ft.filename, "")

    def test_filename_argument_is_empty_string(self):
        """testing if nothing happens when the filename argument is empty
        string
        """
        self.kwargs["filename"] = ""
        ft = FilenameTemplate(**self.kwargs)
        self.assertTrue(isinstance(ft, FilenameTemplate))

    def test_filename_attribute_is_empty_string(self):
        """testing if nothing happens when the filename attribute is set to
        empty string
        """
        self.filename_template.filename = ""

    def test_filename_argument_is_not_string(self):
        """testing if a TypeError will be raised when filename argument is not
        string
        """
        test_value = list("a list from a string")
        self.kwargs["filename"] = test_value
        self.assertRaises(TypeError, FilenameTemplate, **self.kwargs)

    def test_filename_attribute_is_not_string(self):
        """testing if the given value converted to string for the filename
        attribute
        """
        test_value = list("a list from a string")
        self.assertRaises(TypeError, self.filename_template, "filename",
                          test_value)

    def test_equality(self):
        """testing the equality of FilenameTemplate objects
        """
        ft1 = FilenameTemplate(**self.kwargs)

        new_entity = Entity(**self.kwargs)

        self.kwargs["target_entity_type"] = "Entity"
        ft2 = FilenameTemplate(**self.kwargs)

        self.kwargs["path"] = "different path"
        ft3 = FilenameTemplate(**self.kwargs)

        self.kwargs["filename"] = "different filename"
        ft4 = FilenameTemplate(**self.kwargs)

        self.assertTrue(self.filename_template == ft1)
        self.assertFalse(self.filename_template == new_entity)
        self.assertFalse(ft1 == ft2)
        self.assertFalse(ft2 == ft3)
        self.assertFalse(ft3 == ft4)

    def test_inequality(self):
        """testing the inequality of FilenameTemplate objects
        """
        ft1 = FilenameTemplate(**self.kwargs)

        new_entity = Entity(**self.kwargs)

        self.kwargs["target_entity_type"] = "Entity"
        ft2 = FilenameTemplate(**self.kwargs)

        self.kwargs["path"] = "different path"
        ft3 = FilenameTemplate(**self.kwargs)

        self.kwargs["filename"] = "different filename"
        ft4 = FilenameTemplate(**self.kwargs)

        self.assertFalse(self.filename_template != ft1)
        self.assertTrue(self.filename_template != new_entity)
        self.assertTrue(ft1 != ft2)
        self.assertTrue(ft2 != ft3)
        self.assertTrue(ft3 != ft4)
