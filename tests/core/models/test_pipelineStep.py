#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import pipelineStep






########################################################################
class PipelineStepTester(mocker.MockerTestCase):
    """tests pipelineStep
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        
        # create a proper pipelineStep object
        self.kwargs = {
            "name": "Testing",
            "description": "This is a pipelineStep for testing things",
            "code": "TESTING"
        }
        
        self.pStepObj = pipelineStep.PipelineStep(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_being_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to the code argument
        """
        self.kwargs["code"] = ""
        self.assertRaises(ValueError, pipelineStep.PipelineStep, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_being_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the code argument
        """
        self.kwargs["code"] = None
        self.assertRaises(ValueError, pipelineStep.PipelineStep, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_being_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to the code property 
        """
        self.kwargs["code"] = ""
        self.assertRaises(ValueError, pipelineStep.PipelineStep, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_accepts_string_only(self):
        """testing if code argument accepts just strings
        """
        test_values = [1, ["TT"]]
        
        for test_value in test_values:
            self.kwargs["code"] = test_value
            # an integer
            self.assertRaises(
                ValueError,
                pipelineStep.PipelineStep,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_accepts_string_only(self):
        """testing if code property accepts just strings
        """
        
        test_values = [1, ["TT"]]
        
        for test_value in test_values:
            # an integer
            self.assertRaises(
                ValueError,
                setattr,
                self.pStepObj,
                "code",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_working_properly(self):
        """testing if code property is working properly
        """
        
        test_value = "MM"
        
        # just assign it and check if they are equal
        self.pStepObj.code = test_value
        
        self.assertEquals(self.pStepObj.code, test_value)
    
    
    