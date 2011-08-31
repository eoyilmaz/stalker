#-*- coding: utf-8 -*-



import unittest
from stalker.core.mixins import ReviewMixin
from stalker.core.models import Review
from stalker.ext.validatedList import ValidatedList






########################################################################
class ReviewMixinTester(unittest.TestCase):
    """Tests the stalker.core.mixins.ReviewMixin
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        class BarClass(object):
            def __init__(self, **kwargs):
                pass
        
        class FooMixedInClass(BarClass, ReviewMixin):
            def __init__(self, **kwargs):
                super(FooMixedInClass, self).__init__(**kwargs)
                ReviewMixin.__init__(self, **kwargs)
        
        self.FooMixedInClass = FooMixedInClass
        
        self.test_foo_obj = FooMixedInClass(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_set_to_None(self):
        """testing if the reviews attribute will be set to an empty list if it
        is set to None
        """
        
        self.test_foo_obj.review = None
        self.assertIsInstance(self.test_foo_obj.reviews, list)
        self.assertEqual(len(self.test_foo_obj.reviews), 0)
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_an_instance_of_ValidatedList(self):
        """testing if the reviews attribute is instance of ValidatedList
        """
        
        self.assertIsInstance(self.test_foo_obj.reviews, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_not_set_to_a_list(self):
        """testing if a TypeError will be raised when the reviews attribute is
        not set to a list instance
        """
        
        self.assertRaises(TypeError, setattr, self.test_foo_obj, "review", 123)
    
    
    
    def test_reviews_attribute_is_not_accepting_anything_other_than_list_of_Reviews(self):
        """testing if a TypeError will be raised when the elements of the
        reivews attribute is set to something other than a Review
        """
        
        self.assertRaises(TypeError, setattr, self.test_foo_obj, "review",
                          [123])
        
        # create a couple of Reviews
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_working_properly(self):
        """testing if the reviews attribute is working properly
        """
        
        
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_updates_the_to_attribute_in_the_Review_instance(self):
        """testing if the "to" attribute is updated with the current object
        when it is set
        """
        
        self.fail("test is not implemented yet")
    
    
    
    