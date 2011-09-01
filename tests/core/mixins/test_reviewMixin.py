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
        
        self.kwargs = {}
        
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
        self.test_foo_obj.reviews = []
        self.assertIsInstance(self.test_foo_obj.reviews, ValidatedList)
        
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_not_set_to_a_list(self):
        """testing if a TypeError will be raised when the reviews attribute is
        not set to a list instance
        """
        
        self.assertRaises(TypeError, setattr, self.test_foo_obj, "reviews",
                          123)
    
    
    
    def test_reviews_attribute_is_not_accepting_anything_other_than_list_of_Reviews(self):
        """testing if a TypeError will be raised when the elements of the
        reivews attribute is set to something other than a Review
        """
        
        self.assertRaises(TypeError, setattr, self.test_foo_obj, "reviews",
                          [123])
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_working_properly(self):
        """testing if the reviews attribute is working properly
        """
        
        # create a couple of Reviews
        rev1 = Review(name="Test Rev 1", to=self.test_foo_obj)
        rev2 = Review(name="Test Rev 2", to=self.test_foo_obj)
        rev3 = Review(name="Test Rev 3", to=self.test_foo_obj)
        
        # create a new FooMixedInClass with no previews
        new_foo_obj = self.FooMixedInClass()
        
        # now try to assign all thre rev1 to the new object
        # this should work fine
        test_reviews = [rev1, rev2, rev3]
        new_foo_obj.reviews = test_reviews
        
        self.assertEqual(new_foo_obj.reviews, test_reviews)
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_updates_the_to_attribute_in_the_Review_instance(self):
        """testing if the "to" attribute is updated with the current object
        when it is set
        """
        
        # create a couple of Reviews
        rev1 = Review(name="Test Rev 1", to=self.test_foo_obj)
        rev2 = Review(name="Test Rev 2", to=self.test_foo_obj)
        rev3 = Review(name="Test Rev 3", to=self.test_foo_obj)
        
        # create a new FooMixedInClass with no reviews
        new_foo_obj = self.FooMixedInClass()
        
        #print self.test_foo_obj
        #print new_foo_obj
        
        # now try to assign all the reviews to the new object
        new_foo_obj.reviews = [rev1, rev2, rev3]
        
        # now check if the reviews "to" attribute is pointing to the correct
        # object
        self.assertEqual(rev1.to, new_foo_obj)
        self.assertEqual(rev2.to, new_foo_obj)
        self.assertEqual(rev3.to, new_foo_obj)
        
        # check the reviews are in the reviews list
        self.assertIn(rev1, new_foo_obj.reviews)
        self.assertIn(rev2, new_foo_obj.reviews)
        self.assertIn(rev3, new_foo_obj.reviews)
        
        # now try to remove the review from the reviews list and expect a
        # TypeError
        #print "trying to remove"
        #print "new_foo_obj.reviews : %s" % new_foo_obj.reviews
        #print rev1
        
        self.assertRaises(RuntimeError, new_foo_obj.reviews.remove, rev1)
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_handles_assigning_the_same_review_twice(self):
        """testing if assigning the same review twice or more will not breake
        anything or raise any exception
        """
        
        # create a couple of Reviews
        rev1 = Review(name="Test Rev 1", to=self.test_foo_obj)
        rev2 = Review(name="Test Rev 2", to=self.test_foo_obj)
        rev3 = Review(name="Test Rev 3", to=self.test_foo_obj)
        
        # now try to assign the same review again to the same object
        self.test_foo_obj.reviews.append(rev1)
        
        # now try the reverse
        rev1.to = self.test_foo_obj
        
        
