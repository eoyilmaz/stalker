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
        
        self.name = "a test tag"
        self.description = "this is a test tag"
    
    
    
    #----------------------------------------------------------------------
    def test_tag_init(self):
        """testing if tag inits properly
        """
        
        # this should work without any error
        a_tag_object = tag.Tag(
            name=self.name,
            description=self.description
        )
