#-*- coding: utf-8 -*-



import mocker
from stalker.models import pipelineStep






########################################################################
class PipelineStepTester(mocker.MockerTestCase):
    """tests pipelineStep
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        
        # create a proper pipelineStep object
        self.name= 'Testing'
        self.description = 'This is a pipelineStep for testing things'
        self.code = 'TESTING'
        
        self.pStepObj = pipelineStep.PipelineStep(
            name=self.name,
            description=self.description,
            code=self.code
        )
    
    
    
    #----------------------------------------------------------------------
    def test_code_attribute_being_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to the code attribute
        """
        
        self.assertRaises(
            ValueError,
            pipelineStep.PipelineStep,
            name=self.name,
            description=self.description,
            code='',
        )
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_being_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to the code property 
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.pStepObj,
            "code",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_code_attribute_accepts_string_only(self):
        """testing if the code attribute accepts just strings
        """
        
        # try to create a new pipeline step with wrong code
        # attirbute and watch if a ValueError will be raised
        
        # an integer
        self.assertRaises(
            ValueError,
            pipelineStep.PipelineStep,
            name=self.name,
            description=self.description,
            code=1
        )
        
        # a list
        self.assertRaises(
            ValueError,
            pipelineStep.PipelineStep,
            name=self.name,
            description=self.description,
            code=["TT"]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_accepts_string_only(self):
        """testing if the code property accepts just strings
        """
        
        # try to assign something other than a string
        
        # an integer
        self.assertRaises(
            ValueError,
            setattr,
            self.pStepObj,
            "code",
            1
        )
        
        # a list
        self.assertRaises(
            ValueError,
            setattr,
            self.pStepObj,
            "code",
            ["TT"]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_working_properly(self):
        """testing if the code property is working properly
        """
        
        test_value = 'MM'
        
        # just assign it and check if they are equal
        self.pStepObj.code = test_value
        
        self.assertEquals(self.pStepObj.code, test_value)
    
    
    