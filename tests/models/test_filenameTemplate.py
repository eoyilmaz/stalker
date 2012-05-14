# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
from stalker import Entity, FilenameTemplate

# a test class
class Asset(object):
    pass

class FilenameTemplateTester(unittest.TestCase):
    """tests the stalker.models.templates.FilenameTemplate class
    """
    
    def setUp(self):
        """setup the test
        """
        self.kwargs = {
            "name": "Test FilenameTemplate",
            "path": "ASSETS/{{asset.code}}/{{task.type.code}}/",
            "filename": "{{asset.code}}_{{version.take}}_{{task.type.code}}_"\
                         "{{version.version}}_{{user.initials}}",
            "output_path": "",
            "target_entity_type": Asset,
        }
        self.mock_filenameTemplate = FilenameTemplate(**self.kwargs)
    
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
        self.assertRaises(AttributeError, setattr, self.mock_filenameTemplate,
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
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.target_entity_type, "Asset")

    def test_path_argument_is_skipped(self):
        """testing if nothing happens when the path argument is skipped
        """
        self.kwargs.pop("path")
        new_fileTemplate = FilenameTemplate(**self.kwargs)

    def test_path_argument_skipped_path_attribute_is_empty_string(self):
        """testing if the path attribute is an empty string if the
        path argument is skipped
        """
        self.kwargs.pop("path")
        new_fileTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_fileTemplate.path, "")

    def test_path_argument_is_None_path_attribute_is_empty_string(self):
        """testing if the path attribute is an empty string when the
        path argument is None
        """
        self.kwargs["path"] = None
        new_fileTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_fileTemplate.path, "")

    def test_path_argument_is_empty_string(self):
        """testing if nothing happens when the path argument is empty
        string
        """
        self.kwargs["path"] = ""
        new_fileTemplate = FilenameTemplate(**self.kwargs)

    def test_path_attribute_is_empty_string(self):
        """testing if nothing happens when the path attribute is set to
        empty string
        """
        self.mock_filenameTemplate.path = ""

    def test_path_argument_is_not_string(self):
        """testing if the given value converted to string for the path
        argument
        """
        test_value = list("a list from a string")
        self.kwargs["path"] = test_value
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.path, str(test_value))

    def test_path_attribute_is_not_string(self):
        """testing if the given value converted to string for the path
        attribute
        """
        test_value = list("a list from a string")
        self.mock_filenameTemplate.path = test_value
        self.assertEqual(self.mock_filenameTemplate.path,
                         str(test_value))

    def test_filename_argument_is_skipped(self):
        """testing if nothing happens when the filename argument is skipped
        """
        self.kwargs.pop("filename")
        new_fileTemplate = FilenameTemplate(**self.kwargs)

    def test_filename_argument_skipped_filename_attribute_is_empty_string(self):
        """testing if the filename attribute is an empty string if the
        filename argument is skipped
        """
        self.kwargs.pop("filename")
        new_fileTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_fileTemplate.filename, "")

    def test_filename_argument_is_None_filename_attribute_is_empty_string(self):
        """testing if the filename attribute is an empty string when the
        filename argument is None
        """
        self.kwargs["filename"] = None
        new_fileTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_fileTemplate.filename, "")

    def test_filename_argument_is_empty_string(self):
        """testing if nothing happens when the filename argument is empty
        string
        """
        self.kwargs["filename"] = ""
        new_fileTemplate = FilenameTemplate(**self.kwargs)

    def test_filename_attribute_is_empty_string(self):
        """testing if nothing happens when the filename attribute is set to
        empty string
        """
        self.mock_filenameTemplate.filename = ""
    
    def test_filename_argument_is_not_string(self):
        """testing if the given value converted to string for the filename
        argument
        """
        test_value = list("a list from a string")
        self.kwargs["filename"] = test_value
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        
        self.assertEqual(new_filenameTemplate.filename, str(test_value))
    
    def test_filename_attribute_is_not_string(self):
        """testing if the given value converted to string for the filename
        attribute
        """
        test_value = list("a list from a string")
        self.mock_filenameTemplate.filename = test_value
        self.assertEqual(self.mock_filenameTemplate.filename,
                         str(test_value))
    
    def test_output_path_argument_is_skipped_nothing_happens(self):
        """testing there will be no problem if the output_path argument is
        skipped 
        """
        self.kwargs.pop("output_path")
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
    
    def test_output_path_argument_is_None_will_set_the_output_path_attribute_to_empty_string(self):
        """testing if the output_path argument is None will set the
        output_path attribute to empty string
        """
        self.kwargs["output_path"] = None
        self.kwargs["output_is_relative"] = True
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_path, "")
   
    def test_equality(self):
        """testing the equality of FilenameTemplate objects
        """

        new_filenameTemplate1 = FilenameTemplate(**self.kwargs)

        new_entity = Entity(**self.kwargs)

        self.kwargs["target_entity_type"] = "Entity"
        new_filenameTemplate2 = FilenameTemplate(**self.kwargs)

        self.kwargs["path"] = "different path"
        new_filenameTemplate3 = FilenameTemplate(**self.kwargs)

        self.kwargs["filename"] = "different filename"
        new_filenameTemplate4 = FilenameTemplate(**self.kwargs)

        self.kwargs["output_path"] = "different output path"
        new_filenameTemplate5 = FilenameTemplate(**self.kwargs)

        self.assertTrue(self.mock_filenameTemplate == new_filenameTemplate1)
        self.assertFalse(self.mock_filenameTemplate == new_entity)
        self.assertFalse(new_filenameTemplate1 == new_filenameTemplate2)
        self.assertFalse(new_filenameTemplate2 == new_filenameTemplate3)
        self.assertFalse(new_filenameTemplate3 == new_filenameTemplate4)
        self.assertFalse(new_filenameTemplate4 == new_filenameTemplate5)

    def test_inequality(self):
        """testing the inequality of FilenameTemplate objects
        """

        new_filenameTemplate1 = FilenameTemplate(**self.kwargs)

        new_entity = Entity(**self.kwargs)

        self.kwargs["target_entity_type"] = "Entity"
        new_filenameTemplate2 = FilenameTemplate(**self.kwargs)

        self.kwargs["path"] = "different path"
        new_filenameTemplate3 = FilenameTemplate(**self.kwargs)

        self.kwargs["filename"] = "different filename"
        new_filenameTemplate4 = FilenameTemplate(**self.kwargs)

        self.kwargs["output_path"] = "different output path"
        new_filenameTemplate5 = FilenameTemplate(**self.kwargs)

        self.assertFalse(self.mock_filenameTemplate != new_filenameTemplate1)
        self.assertTrue(self.mock_filenameTemplate != new_entity)
        self.assertTrue(new_filenameTemplate1 != new_filenameTemplate2)
        self.assertTrue(new_filenameTemplate2 != new_filenameTemplate3)
        self.assertTrue(new_filenameTemplate3 != new_filenameTemplate4)
        self.assertTrue(new_filenameTemplate4 != new_filenameTemplate5)
