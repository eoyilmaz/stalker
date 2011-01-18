#-*- coding: utf-8 -*-



import unittest
from stalker.core.models import tag






########################################################################
class TagTest(unittest.TestCase):
    """testing the Tag class
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.kwargs = {
            "name": "a test tag",
            "description": "this is a test tag",
        }
        
        # create another SimpleEntity with kwargs for __eq__ and __ne__ tests
        from stalker.core.models import entity
        self.simple_entity = entity.SimpleEntity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tag_init(self):
        """testing if tag inits properly
        """
        
        # this should work without any error
        a_tag_object = tag.Tag(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality of two Tags
        """
        
        a_tag_object1 = tag.Tag(**self.kwargs)
        a_tag_object2 = tag.Tag(**self.kwargs)
        
        self.kwargs["name"] = "a new test Tag"
        self.kwargs["description"] = "this is a new test Tag"
        
        a_tag_object3 = tag.Tag(**self.kwargs)
        
        
        self.assertTrue(a_tag_object1==a_tag_object2)
        self.assertFalse(a_tag_object1==a_tag_object3)
        self.assertFalse(a_tag_object1==self.simple_entity)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality of two Tags
        """
        
        a_tag_object1 = tag.Tag(**self.kwargs)
        a_tag_object2 = tag.Tag(**self.kwargs)
        
        self.kwargs["name"] = "a new test Tag"
        self.kwargs["description"] = "this is a new test Tag"
        
        a_tag_object3 = tag.Tag(**self.kwargs)
        
        self.assertFalse(a_tag_object1!=a_tag_object2)
        self.assertTrue(a_tag_object1!=a_tag_object3)
        self.assertTrue(a_tag_object1!=self.simple_entity)


