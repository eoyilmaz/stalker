#-*- coding: utf-8 -*-



import unittest
from stalker.core.models import Version






########################################################################
class VersionTester(unittest.TestCase):
    """tests stalker.core.models.Version class
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        pass
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_skipped_defaults_to_default_value(self):
        """testing if the take argument is skipped the take attribute is going
        to be set to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_None_defaults_to_default_value(self):
        """testing if the take argument is None the take attribute is going to
        be set to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_None_defaults_to_default_value(self):
        """testing if the take attribute is set to None it is going to be set
        to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_empty_string(self):
        """testing if a ValueError will be raised when the take argument is an
        empty string
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_empty_string(self):
        """testing if a ValueError will be raised when the take attribute is
        set to an empty string
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_not_a_string_will_be_converted_to_one(self):
        """testing if the given take argument is not a string will be converted
        to a proper string
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_not_a_string_will_be_converted_to_one(self):
        """testing if the given take attribute is not a string will be
        converted to a proper string
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take argument string
        is formatted to an empty string
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take argument string
        is formatted to an empty string
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_skipped(self):
        """testing if a TypeError will be raised when the version argument is
        skipped
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_None(self):
        """testing if a TypeError will be raised when the version argument is
        None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_version_attribute_is_None(self):
        """testing if a TypeError will be raised when the version attribute is
        set to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_0(self):
        """testing if a ValueError will be raised when the version argument is
        0
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_version_attribute_is_0(self):
        """testing if a ValueError will be raised when the version attribute is
        set to 0
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_negative(self):
        """testing if a ValueError will be raised when the version argument is
        negative
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_version_attribute_is_negative(self):
        """testing if a ValueError will be raised when the version attribute is
        negative
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_set_to_None(self):
        """testing if nothing happens when the reviews attribute is set to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the reviews attribute is
        not a list instance
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_not_a_list_of_Comment_instances(self):
        """testing if a TypeError will be raised when the reviews attribute is
        set to a list of other objects
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_set_to_something_other_than_a_list_of_Comment_instance(self):
        """testing if a TypeError will be raised when the reviews attribute is
        set to something other than a Comment instance
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_working_properly(self):
        """testing if the reviews attribute is working properly
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_a_ValidatedList(self):
        """testinf if the reviews attribute is a ValidatedList instance
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_published_attribute_is_set_to_non_bool_value(self):
        """testing if the published attribute is set to a non bool value will
        be converted to a bool value
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_published_attribute_defaults_to_false(self):
        """testing if the default value of published for newly created Versions
        is False
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_published_attribute_is_working_properly(self):
        """testing if the published attribute is working properly
        """
        
        self.fail("test is not implemented yet")
    
    
    
    