#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import entity, types, pipelineStep, tag






########################################################################
class AssetTypeTester(mocker.MockerTestCase):
    """tests AssetType class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """lets setup the test
        """
        
        # we need a couple of mocke PipelineStep objects
        self.mock_pipeline_step1 = self.mocker.mock(pipelineStep.PipelineStep)
        self.mock_pipeline_step2 = self.mocker.mock(pipelineStep.PipelineStep)
        self.mock_pipeline_step3 = self.mocker.mock(pipelineStep.PipelineStep)
        
        # create a couple of tags
        self.mock_tag1 = self.mocker.mock( tag.Tag )
        self.mock_tag2 = self.mocker.mock( tag.Tag )
        
        self.mocker.replay()
        
        self.pipelineStep_list = [ self.mock_pipeline_step1,
                                   self.mock_pipeline_step2,
                                   self.mock_pipeline_step3 ]
        
        self.tag_list = [ self.mock_tag1,
                          self.mock_tag2 ]
        
        # create a proper assetType object
        self.name = "An AssetType"
        self.description = "This is an test asset type"
        
        self.kwargs = {
            "name": self.name,
            "description": self.description,
            "tags": self.tag_list,
            "steps": self.pipelineStep_list
        }
        
        self.an_assetType_obj = types.AssetType(**self.kwargs)
        
        # create a couple of different object
        # a string
        self.test_attr_1 = "a test object"
        
        # an integer
        self.test_attr_2 = 134
        
        # a dict obj
        self.test_attr_3 = {"a key":"a Value"}
        
        # a list of different objects than a pipelineStep objects
        self.test_attr_4 = [
            self.test_attr_1,
            self.test_attr_2,
            self.test_attr_3
        ]
    
    
    
    #----------------------------------------------------------------------
    def test_steps_argument_accepts_pipelineStep_objects_only(self):
        """testing if steps argument accepts just PipelineStep objects
        """
        
        # lets try to assign them to a newly created AssetType object
        # this should raise a ValueError
        
        test_values = [self.test_attr_1,
                       self.test_attr_2,
                       self.test_attr_3,
                       self.test_attr_4]
        
        for test_value in test_values:
            self.kwargs["steps"] = test_value
            
            self.assertRaises(
                ValueError,
                types.AssetType,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_steps_property_for_being_pipelineStep_objects(self):
        """testing if steps `property` accepts just PipelineStep objects
        """
        
        # lets try to assign them to a newly created AssetType object
        # this should raise a ValueError
        
        test_values = [self.test_attr_1,
                       self.test_attr_2,
                       self.test_attr_3,
                       self.test_attr_4]
        
        for test_value in test_values:
        
            self.assertRaises(
                ValueError,
                setattr,
                self.an_assetType_obj,
                "steps",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_steps_property_working_properly(self):
        """testing if steps `property` is working properly
        """
        
        # lets create a new list of pipelineStep objects
        a_new_list_of_pipelineStep_objs = [
            self.mock_pipeline_step1,
            self.mock_pipeline_step2
        ]
        
        # lets assign it to the assetType and check if they are same
        self.an_assetType_obj.steps = a_new_list_of_pipelineStep_objs
        
        self.assertEquals(self.an_assetType_obj.steps,
                          a_new_list_of_pipelineStep_objs
                          )






########################################################################
class TypeTemplateTester(mocker.MockerTestCase):
    """tests the TypeTemplate class
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setups the tests
        """
        
        # create a mock TypeEntity object
        self.mock_type_entity1 = self.mocker.mock(entity.TypeEntity)
        self.mock_type_entity2 = self.mocker.mock(entity.TypeEntity)
        
        self.mock_type_entity1.__eq__(self.mock_type_entity2)
        self.mocker.result(False)
        self.mocker.count(0, None)
        
        self.mock_type_entity1.__ne__(self.mock_type_entity2)
        self.mocker.result(True)
        self.mocker.count(0, None)
        
        self.mocker.replay()
        
        # create a mock TypeTemplate object
        self.kwargs = {
            "name": "Test Template",
            "description": "This is a test template",
            "path_code": "{{project.name}}/SEQUENCES/{{sequence.name}}/SHOTS/\
            {{shot.code}}/{{pipeline_step.code}}/",
            "file_code": "{{shot.code}}_{{take.name}}\
            v{{version.version_number}}",
            "type":self.mock_type_entity1
        }
        
        self.template_obj = types.TypeTemplate(**self.kwargs)
        
        temp_kwargs = self.kwargs.copy()
        temp_kwargs.update({
            "type": self.mock_type_entity2
        })
        
        self.template_obj2 = types.TypeTemplate(**temp_kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_equality_operator(self):
        """testing the equality operator
        """
        
        self.assertFalse(self.template_obj==self.template_obj2)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality_operator(self):
        """testing the inequality operator
        """
        
        self.assertTrue(self.template_obj!=self.template_obj2)
    
    
    
    #----------------------------------------------------------------------
    def test_if_path_code_argument_not_accepting_empty_strings(self):
        """testing if assigning an empty string to path_code argument will
        raise a ValueError
        """
        
        # try to create a new template object with wrong values
        self.kwargs["path_code"] = ""
        self.assertRaises(ValueError, types.TypeTemplate, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_if_path_code_property_not_accepting_empty_strings(self):
        """testing if assigning an empty string to path_code argument will
        raise a ValueError
        """
        
        # try to assign "" to the path_code property
        self.assertRaises(
            ValueError,
            setattr,
            self.template_obj,
            "path_code",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_if_path_code_argument_not_accepting_None(self):
        """testing if assigning None to path_code raises a ValueError
        """
        # try to create a new TypeTemplate object with wrong values
        self.kwargs["path_code"] = None
        self.assertRaises(ValueError, types.TypeTemplate, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_if_path_code_property_not_accepting_None(self):
        """testing if assigning None to path_code raises a ValueError
        """
        # try to assign "" to the path_code property
        self.assertRaises(
            ValueError,
            setattr,
            self.template_obj,
            "path_code",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_if_path_code_argument_accepts_only_strings(self):
        """testing if path_code argument is only accepting string or unicode
        values
        """
        
        test_values = [1, 1.2, ["path_code"], {'path': 'code'}]
        
        for test_value in test_values:
            self.kwargs["path_code"] = test_value
            # an integer value
            self.assertRaises(ValueError, types.TypeTemplate,
                              **self.kwargs)
        
        # this should work without errors
        self.kwargs["path_code"] = "{{project.name}}/SEQs/{{sequence.name}}/\
        SHOTS/{{shot.code}}/{{assetType.code}}"
        a_new_type_template = types.TypeTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_if_path_code_property_accepts_only_strings(self):
        """testing if path_code property is only accepting string or
        unicode values
        """
        
        test_values = [1, 1.2, ["path_code"], {'path': 'code'}]
        
        for test_value in test_values:
            # an integer value
            self.assertRaises(
                ValueError,
                setattr,
                self.template_obj,
                "path_code",
                test_value
            )
        
        # this should work without errors
        self.template_obj.path_template = "{{project.name}}/SEQs/\
        {{sequence.name}}/SHOTS/{{shot.code}}/{{assetType.code}}"
    
    
    
    #----------------------------------------------------------------------
    def test_if_path_code_property_works(self):
        """testing if path_code property works correctly
        """
        
        test_value = "{{project.name}}/SEQs/{{sequence.name}}/SHOTS/ \
        {{shot.code}}/{{assetType.code}}"
        
        # lets assign it and check if it is working
        
        self.template_obj.path_code = test_value
        
        self.assertEquals(self.template_obj.path_code, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_if_file_code_argument_not_accepting_empty_strings(self):
        """testing if assigning an empty string to file_code argument will
        raise a ValueError
        """
        
        # try to create a new template object with wrong values
        self.kwargs["file_code"] = ""
        self.assertRaises(ValueError, types.TypeTemplate, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_if_file_code_property_not_accepting_empty_strings(self):
        """testing if assigning an empty string to file_code argument will
        raise a ValueError
        """
        
        # try to assign "" to the file_code property
        self.assertRaises(
            ValueError,
            setattr,
            self.template_obj,
            "file_code",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_if_file_code_argument_not_accepting_None(self):
        """testing if assigning None to file_code raises a ValueError
        """
        # try to create a new TypeTemplate object with wrong values
        self.kwargs["file_code"] = None
        self.assertRaises(ValueError, types.TypeTemplate, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_if_file_code_property_not_accepting_None(self):
        """testing if assigning None to file_code raises a ValueError
        """
        # try to assign "" to the file_code property
        self.assertRaises(
            ValueError,
            setattr,
            self.template_obj,
            "file_code",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_if_file_code_argument_accepts_only_strings(self):
        """testing if file_code argument is only accepting string or unicode
        values
        """
        
        test_values = [1, 1.2, ["file_code"], {'path': 'code'}]
        
        for test_value in test_values:
            self.kwargs["file_code"] = test_value
            # an integer value
            self.assertRaises(ValueError, types.TypeTemplate,
                              **self.kwargs)
        
        # this should work without errors
        self.kwargs["file_code"] = "{{project.name}}/SEQs/{{sequence.name}}/\
        SHOTS/{{shot.code}}/{{assetType.code}}"
        a_new_type_template = types.TypeTemplate(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_if_file_code_property_accepts_only_strings(self):
        """testing if file_code property is only accepting string or
        unicode values
        """
        
        test_values = [1, 1.2, ["file_code"], {'path': 'code'}]
        
        for test_value in test_values:
            # an integer value
            self.assertRaises(
                ValueError,
                setattr,
                self.template_obj,
                "file_code",
                test_value
            )
        
        # this should work without errors
        self.template_obj.path_template = "{{project.name}}/SEQs/\
        {{sequence.name}}/SHOTS/{{shot.code}}/{{assetType.code}}"
    
    
    
    #----------------------------------------------------------------------
    def test_if_file_code_property_works(self):
        """testing if file_code property works correctly
        """
        
        test_value = "{{project.name}}/SEQs/{{sequence.name}}/SHOTS/ \
        {{shot.code}}/{{assetType.code}}"
        
        # lets assign it and check if it is working
        
        self.template_obj.file_code = test_value
        
        self.assertEquals(self.template_obj.file_code, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_if_type_argument_only_accepts_TypeEntity_objects(self):
        """testing if type argument accepts only TypeEntity objects and raises
        ValueError otherwise
        """
        
        test_values = [1, 1.2, "", [""], {"a": "type entity"}]
        
        for test_value in test_values:
            self.kwargs["type"] = test_value
            self.assertRaises(ValueError, types.TypeTemplate,
                              **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_if_type_property_only_accepts_TypeEntity_objects(self):
        """testing if type property accepts only TypeEntity objects and raises
        ValueError otherwise
        """
        test_values = [1, 1.2, "", [""], {"a": "type entity"}]
        
        for test_value in test_values:
            self.kwargs["type"] = test_value
            self.assertRaises(
                ValueError,
                setattr,
                self.template_obj,
                "type",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_if_type_argument_not_accepting_None(self):
        """testing if type argument doesn't accept None and raises ValueError
        """
        
        self.kwargs["type"] = None
        self.assertRaises(ValueError, types.TypeTemplate, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_if_type_property_not_accepting_None(self):
        """testing if type property doesn't accept None and raises ValueError
        """
        self.assertRaises(ValueError, setattr, self.template_obj, "type", None)
    
    
    
    