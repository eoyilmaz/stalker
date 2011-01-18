#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import pipelineStep






########################################################################
class PipelineStepTester(mocker.MockerTestCase):
    """tests pipelineStep
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.kwargs = {
            "name": "Model",
            "description": "the modeling pipelinestep"
        }
    
    
        self.pipeline_step1 = pipelineStep.PipelineStep(**self.kwargs)
        self.pipeline_step2 = pipelineStep.PipelineStep(**self.kwargs)
        
        self.kwargs["name"] = "Lighting"
        self.kwargs["description"] = "the ligthing pipelinestep"
        
        self.pipeline_step3 = pipelineStep.PipelineStep(**self.kwargs)
        
        # create another entity with the same kwargs for the __eq__ and __ne__
        # tests
        from stalker.core.models import entity
        self.entity = entity.Entity(**self.kwargs)

    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality of two PipelineStep objects
        """
        
        self.assertTrue(self.pipeline_step1==self.pipeline_step2)
        self.assertFalse(self.pipeline_step1==self.pipeline_step3)
        self.assertFalse(self.pipeline_step1==self.entity)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality of two PipelineStep objects
        """
        
        self.assertFalse(self.pipeline_step1!=self.pipeline_step2)
        self.assertTrue(self.pipeline_step1!=self.pipeline_step3)
        self.assertTrue(self.pipeline_step1!=self.entity)
    
    
    
    