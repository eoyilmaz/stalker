#-*- coding: utf-8 -*-



import mocker
from stalker.models import typeEntity, pipelineStep, tag






########################################################################
class AssetTypeTester(mocker.MockerTestCase):
    """tests AssetType class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """lets setup the test
        """
        
        # we need a couple of mocke PipelineStep objects
        self.mock_pipeline_step1 = self.mocker.mock( pipelineStep.PipelineStep )
        self.mock_pipeline_step2 = self.mocker.mock( pipelineStep.PipelineStep )
        self.mock_pipeline_step3 = self.mocker.mock( pipelineStep.PipelineStep )
        
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
        self.name = 'An AssetType'
        self.description = 'This is an test asset type'
        
        self.an_assetType_obj = typeEntity.AssetType(name=self.name,
                                             description=self.description,
                                             tags=self.tag_list,
                                             steps=self.pipelineStep_list
                                             )
        
        # create a couple of different object
        # a string
        self.test_attr_1 = "a test object"
        
        # an integer
        self.test_attr_2 = 134
        
        # a dict obj
        self.test_attr_3 = {'a key':'a Value'}
        
        # a list of different objects than a pipelineStep objects
        self.test_attr_4 = [
            self.test_attr_1,
            self.test_attr_2,
            self.test_attr_3
        ]
    
    
    
    #----------------------------------------------------------------------
    def test_steps_attribute_for_being_pipelineStep_objects(self):
        """testing if the steps `attribute` accepts just PipelineStep objects
        """
        
        # lets try to assign them to a newly created AssetType object
        # this should raise a ValueError
        self.assertRaises(
            ValueError,
            typeEntity.AssetType,
            name=self.name,
            description=self.description,
            tags=self.tag_list,
            steps=self.test_attr_1
        )
        
        self.assertRaises(
            ValueError,
            typeEntity.AssetType,
            name=self.name,
            description=self.description,
            tags=self.tag_list,
            steps=self.test_attr_2
        )
        
        self.assertRaises(
            ValueError,
            typeEntity.AssetType,
            name=self.name,
            description=self.description,
            tags=self.tag_list,
            steps=self.test_attr_3
        )
    
        self.assertRaises(
            ValueError,
            typeEntity.AssetType,
            name=self.name,
            description=self.description,
            tags=self.tag_list,
            steps=self.test_attr_4
        )
    
    
    
    #----------------------------------------------------------------------
    def test_steps_property_for_being_pipelineStep_objects(self):
        """testing if the steps `property` accepts just PipelineStep objects
        """
        
        # lets try to assign them to a newly created AssetType object
        # this should raise a ValueError
        self.assertRaises(
            ValueError,
            setattr,
            self.an_assetType_obj,
            'steps',
            self.test_attr_1
        )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.an_assetType_obj,
            'steps',
            self.test_attr_2
        )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.an_assetType_obj,
            'steps',
            self.test_attr_3
        )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.an_assetType_obj,
            'steps',
            self.test_attr_4
        )
    
    
    
    #----------------------------------------------------------------------
    def test_steps_property_working_properly(self):
        """testing if the steps `property` is working properly
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
    
    
