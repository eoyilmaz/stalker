#-*- coding: utf-8 -*-



import unittest
from stalker.core.declarativeModels import (FilenameTemplate, Type, Entity)


# a test class
class Asset(object):
    pass



########################################################################
class FilenameTemplateTester(unittest.TestCase):
    """tests the stalker.core.models.FilenameTemplate class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.kwargs = {
            "name": "Test FilenameTemplate",
            "path_code": "ASSETS/{{asset.code}}/{{task.code}}/",
            "file_code": "{{asset.code}}_{{version.take}}_{{task.code}}_"\
                         "{{version.version}}_{{user.initials}}",
            "output_path_code": "",
            "output_file_code": "",
            "output_is_relative": "",
            "target_entity_type": Asset,
        }
        
        self.mock_filenameTemplate = FilenameTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_argument_is_skipped(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is skipped
        """
        
        self.kwargs.pop("target_entity_type")
        self.assertRaises(TypeError, FilenameTemplate, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_argument_is_None(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is given as None
        """
        
        self.kwargs["target_entity_type"] = None
        self.assertRaises(TypeError, FilenameTemplate, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_attribute_is_read_only(self):
        """testing if a AttributeError will be raised when the
        target_entity_type attribute is tried to be changed
        """
        
        self.assertRaises(AttributeError, setattr, self.mock_filenameTemplate,
                          "target_entity_type", "Asset")
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_argument_accepts_Classes(self):
        """testing if the target_entity_type can be set to a class directly
        """
        
        self.kwargs["target_entity_type"] = Asset
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_attribute_is_converted_to_a_string_if_given_as_a_class(self):
        """testing if the target_entity_type attribute is converted when the
        target_entity_type is given as a class
        """
        
        self.kwargs["target_entity_type"] = Asset
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual( new_filenameTemplate.target_entity_type, "Asset")
    
    
    
    #----------------------------------------------------------------------
    def test_path_code_argument_is_skipped(self):
        """testing if nothing happens when the path_code argument is skipped
        """
        
        self.kwargs.pop("path_code")
        new_fileTemplate = FilenameTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_path_code_argument_skipped_path_code_attribute_is_empty_string(self):
        """testing if the path_code attribute is an empty string if the
        path_code argument is skipped
        """
        
        self.kwargs.pop("path_code")
        new_fileTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_fileTemplate.path_code, "")
    
    
    
    #----------------------------------------------------------------------
    def test_path_code_argument_is_None_path_code_attribute_is_empty_string(self):
        """testing if the path_code attribute is an empty string when the
        path_code argument is None
        """
        
        self.kwargs["path_code"] = None
        new_fileTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_fileTemplate.path_code, "")
    
    
    
    #----------------------------------------------------------------------
    def test_path_code_argument_is_empty_string(self):
        """testing if nothing happens when the path_code argument is empty
        string
        """
        
        self.kwargs["path_code"] = ""
        new_fileTemplate = FilenameTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_path_code_attribute_is_empty_string(self):
        """testing if nothing happens when the path_code attribute is set to
        empty string
        """
        
        self.mock_filenameTemplate.path_code = ""
    
    
    
    #----------------------------------------------------------------------
    def test_path_code_argument_is_not_string(self):
        """testing if the given value converted to string for the path_code
        argument
        """
        
        test_value = list("a list from a string")
        self.kwargs["path_code"] = test_value
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        
        self.assertEqual(new_filenameTemplate.path_code, str(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_path_code_attribute_is_not_string(self):
        """testing if the given value converted to string for the path_code
        attribute
        """
        
        test_value = list("a list from a string")
        self.mock_filenameTemplate.path_code = test_value
        self.assertEqual(self.mock_filenameTemplate.path_code,
                         str(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_file_code_argument_is_skipped(self):
        """testing if nothing happens when the file_code argument is skipped
        """
        
        self.kwargs.pop("file_code")
        new_fileTemplate = FilenameTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_file_code_argument_skipped_file_code_attribute_is_empty_string(self):
        """testing if the file_code attribute is an empty string if the
        file_code argument is skipped
        """
        
        self.kwargs.pop("file_code")
        new_fileTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_fileTemplate.file_code, "")
    
    
    
    #----------------------------------------------------------------------
    def test_file_code_argument_is_None_file_code_attribute_is_empty_string(self):
        """testing if the file_code attribute is an empty string when the
        file_code argument is None
        """
        
        self.kwargs["file_code"] = None
        new_fileTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_fileTemplate.file_code, "")
    
    
    
    #----------------------------------------------------------------------
    def test_file_code_argument_is_empty_string(self):
        """testing if nothing happens when the file_code argument is empty
        string
        """
        
        self.kwargs["file_code"] = ""
        new_fileTemplate = FilenameTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_file_code_attribute_is_empty_string(self):
        """testing if nothing happens when the file_code attribute is set to
        empty string
        """
        
        self.mock_filenameTemplate.file_code = ""
    
    
    
    #----------------------------------------------------------------------
    def test_file_code_argument_is_not_string(self):
        """testing if the given value converted to string for the file_code
        argument
        """
        
        test_value = list("a list from a string")
        self.kwargs["file_code"] = test_value
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        
        self.assertEqual(new_filenameTemplate.file_code, str(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_file_code_attribute_is_not_string(self):
        """testing if the given value converted to string for the file_code
        attribute
        """
        
        test_value = list("a list from a string")
        self.mock_filenameTemplate.file_code = test_value
        self.assertEqual(self.mock_filenameTemplate.file_code,
                         str(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_output_path_code_argument_is_skipped_nothing_happens(self):
        """testing there will be no problem if the output_path argument is
        skipped 
        """
        
        self.kwargs.pop("output_path_code")
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_output_path_code_argument_is_None_and_output_is_relative_is_true_will_set_the_output_path_code_attribute_to_empty_string(self):
        """testing if the output_path_code argument is None will set the
        output_path attribute to empty string
        """
        
        self.kwargs["output_path_code"] = None
        self.kwargs["output_is_relative"] = True
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_path_code, "")
    
    
    
    #----------------------------------------------------------------------
    def test_output_path_code_argument_is_None_and_output_is_relative_is_false(self):
        """testing if the output_path_code attribute will be the same with
        path_code if the output_path_code is given as None and the
        output_is_relative_is False
        """
        
        self.kwargs["output_path_code"] = None
        self.kwargs["output_is_relative"] = False
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_path_code,
                         new_filenameTemplate.path_code)
    
    
    
    #----------------------------------------------------------------------
    def test_output_path_code_argument_is_empty_string_and_output_is_relative_is_true_will_set_the_output_path_code_attribute_to_empty_string(self):
        """testing if the output_path_code argument is None will set the
        output_path attribute to empty string
        """
        
        self.kwargs["output_path_code"] = ""
        self.kwargs["output_is_relative"] = True
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_path_code, "")
    
    
    
    #----------------------------------------------------------------------
    def test_output_path_code_argument_is_empty_string_and_output_is_relative_is_false(self):
        """testing if the output_path_code attribute will be the same with
        path_code if the output_path_code is given as None and the
        output_is_relative_is False
        """
        
        self.kwargs["output_path_code"] = ""
        self.kwargs["output_is_relative_false"] = False
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_path_code,
                         new_filenameTemplate.path_code)
    
    
    
    #----------------------------------------------------------------------
    def test_output_file_code_argument_is_skipped_nothing_happens(self):
        """testing there will be no problem if the output_path argument is
        skipped 
        """
        
        self.kwargs.pop("output_file_code")
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_output_file_code_argument_is_None_and_output_is_relative_is_true_will_set_the_output_path_attribute_to_empty_string(self):
        """testing if the output_file_code argument is None will set the
        output_path attribute to empty string
        """
        
        self.kwargs["output_file_code"] = None
        self.kwargs["output_is_relative"] = True
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_file_code, "")
    
    
    
    #----------------------------------------------------------------------
    def test_output_file_code_argument_is_None_and_output_is_relative_is_false(self):
        """testing if the output_file_code attribute will be the same with
        file_code if the output_file_code is given as None and the
        output_is_relative_is False
        """
        
        self.kwargs["output_file_code"] = None
        self.kwargs["output_is_relative"] = False
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_file_code,
                         new_filenameTemplate.file_code)
    
    
    
    #----------------------------------------------------------------------
    def test_output_file_code_argument_is_empty_string_and_output_is_relative_is_true_will_set_the_output_file_code_attribute_to_empty_string(self):
        """testing if the output_file_code argument is None will set the
        output_file_code attribute to empty string
        """
        
        self.kwargs["output_file_code"] = ""
        self.kwargs["output_is_relative"] = True
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_file_code, "")
    
    
    
    #----------------------------------------------------------------------
    def test_output_file_code_argument_is_empty_string_and_output_is_relative_is_false(self):
        """testing if the output_file_code attribute will be the same with
        file_code if the output_file_code is given as None and the
        output_is_relative_is False
        """
        
        self.kwargs["output_file_code"] = ""
        self.kwargs["output_is_relative"] = False
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_file_code,
                         new_filenameTemplate.file_code)
    
    
    
    #----------------------------------------------------------------------
    def test_output_is_relative_is_evaluated_the_given_value_to_a_bool_value(self):
        """testing if the output_is_relative is evaluated as a bool value for
        non bool values
        """
        
        test_values = [1, 1.2, "False", "True", [], [1]]
        
        for test_value in test_values:
            self.kwargs["output_is_relative"] = test_value
            new_filetemplate = FilenameTemplate(**self.kwargs)
            self.assertEqual(new_filetemplate.output_is_relative,
                             bool(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_output_is_relative_attribute_is_working_properly(self):
        """testing if the output_is_relatvie attribute is working properly
        """
        
        self.kwargs["output_is_relative"] = False
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_is_relative, False)
        
        self.kwargs["output_is_relative"] = True
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_is_relative, True)
        
        new_filenameTemplate.output_is_relative = False
        self.assertEqual(new_filenameTemplate.output_is_relative, False)
    
    
    
    #----------------------------------------------------------------------
    def test_output_is_relative_default_value_is_True(self):
        """testing if the default value for output_is_relative is True
        """
        
        self.kwargs.pop("output_is_relative")
        new_filenameTemplate = FilenameTemplate(**self.kwargs)
        self.assertEqual(new_filenameTemplate.output_is_relative, True)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality of FilenameTemplate objects
        """
        
        new_filenameTemplate1 = FilenameTemplate(**self.kwargs)
        
        new_entity = Entity(**self.kwargs)
        
        self.kwargs["target_entity_type"] = "Entity"
        new_filenameTemplate2 = FilenameTemplate(**self.kwargs)
        
        self.kwargs["path_code"] = "different path code"
        new_filenameTemplate3 = FilenameTemplate(**self.kwargs)
        
        self.kwargs["file_code"] = "different file code"
        new_filenameTemplate4 = FilenameTemplate(**self.kwargs)
        
        self.kwargs["output_path_code"] = "different output path code"
        new_filenameTemplate5 = FilenameTemplate(**self.kwargs)
        
        self.kwargs["output_file_code"] = "different output file code"
        new_filenameTemplate6 = FilenameTemplate(**self.kwargs)
        
        self.assertTrue(self.mock_filenameTemplate == new_filenameTemplate1)
        self.assertFalse(self.mock_filenameTemplate == new_entity)
        self.assertFalse(new_filenameTemplate1 == new_filenameTemplate2)
        self.assertFalse(new_filenameTemplate2 == new_filenameTemplate3)
        self.assertFalse(new_filenameTemplate3 == new_filenameTemplate4)
        self.assertFalse(new_filenameTemplate4 == new_filenameTemplate5)
        self.assertFalse(new_filenameTemplate5 == new_filenameTemplate6)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality of FilenameTemplate objects
        """
        
        new_filenameTemplate1 = FilenameTemplate(**self.kwargs)
        
        new_entity = Entity(**self.kwargs)
        
        self.kwargs["target_entity_type"] = "Entity"
        new_filenameTemplate2 = FilenameTemplate(**self.kwargs)
        
        self.kwargs["path_code"] = "different path code"
        new_filenameTemplate3 = FilenameTemplate(**self.kwargs)
        
        self.kwargs["file_code"] = "different file code"
        new_filenameTemplate4 = FilenameTemplate(**self.kwargs)
        
        self.kwargs["output_path_code"] = "different output path code"
        new_filenameTemplate5 = FilenameTemplate(**self.kwargs)
        
        self.kwargs["output_file_code"] = "different output file code"
        new_filenameTemplate6 = FilenameTemplate(**self.kwargs)
        
        self.assertFalse(self.mock_filenameTemplate != new_filenameTemplate1)
        self.assertTrue(self.mock_filenameTemplate != new_entity)
        self.assertTrue(new_filenameTemplate1 != new_filenameTemplate2)
        self.assertTrue(new_filenameTemplate2 != new_filenameTemplate3)
        self.assertTrue(new_filenameTemplate3 != new_filenameTemplate4)
        self.assertTrue(new_filenameTemplate4 != new_filenameTemplate5)
        self.assertTrue(new_filenameTemplate5 != new_filenameTemplate6)
