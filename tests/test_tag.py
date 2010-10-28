#-*- coding: utf-8 -*-



import unittest
from stalker.models import tag






########################################################################
class TagTest(unittest.TestCase):
    """testing the Tag class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_name_str_unicode(self):
        """testing the name attribute being an instance of string or unicode
        """
        
        #----------------------------------------------------------------------
        # the name should be a string or unicode
        new_name = 1
        self.assertRaises(ValueError, tag.Tag, new_name)
        # check the name property
        name = 'a new tag'
        a_tag = tag.Tag(name)
        self.assertRaises(ValueError, setattr, a_tag, 'name', new_name)
    
    
    
    #----------------------------------------------------------------------
    def test_name_empty(self):
        """testing the name attribute being empty
        """
        
        #----------------------------------------------------------------------
        # the name can not be empty
        new_name = ''
        self.assertRaises(ValueError, tag.Tag, new_name)
        # check the name property
        name = 'a new tag'
        a_tag = tag.Tag(name)
        self.assertRaises(ValueError, setattr, a_tag, 'name', new_name)
    
    
    
    #----------------------------------------------------------------------
    def test_name_property(self):
        """testing the name property
        """
        
        #----------------------------------------------------------------------
        # test if we get the name attribute correctly by using the name
        # property
        name = 'a tag'
        a_tag = tag.Tag(name)
        self.assertEquals(a_tag.name, name)
        