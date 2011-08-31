#-*- coding: utf-8 -*-



import unittest
import datetime
from stalker.core.models import Review, Entity, User, Tag






########################################################################
class ReviewTest(unittest.TestCase):
    """testing the Review class
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setting up the test
        """
        
        # will need:
        # a couple of test tag objects
        
        # a couple of test tags
        self.test_tag1 = Tag(name="Test Tag 1")
        self.test_tag2 = Tag(name="Test Tag 2")
        
        ## a test entity object
        #self.test_entity = Entity(name="Test Entity 1")
        #self.test_entity2 = Entity(name="Test Entity 2")
        
        class AnObjectWithReviews(object):
            def __init__(self):
                self.reviews = []
        
        self.test_to_object = AnObjectWithReviews()
        self.test_to_object2 = AnObjectWithReviews()
        
        # creation and update dates
        self.date_created = datetime.datetime.now()
        self.date_updated = self.date_created
        
        # a test user object
        self.test_user = User(
            login_name="user1",
            first_name="user1",
            last_name="user1",
            email="user1@users.com",
            password="1234",
        )
        
        self.kwargs = {
            "name": "Test Review",
            "description": "this is a test object",
            "body": "This is the content of the review",
            "to": self.test_to_object
        }
        
        self.test_review = Review(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_body_argument_accepts_string_or_unicode_only(self):
        """testing if a TypeError raised if the body argument is set to
        anything other than a string or unicode
        """
        
        # create a new review with false values
        
        test_values = [1, 1.0, ["this is the bodybody"],
                       {"this": "is the body"}]
        
        for test_value in test_values:
            self.kwargs["body"] = test_value
            self.assertRaises(
                TypeError,
                Review,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_body_attribute_being_string_or_unicode(self):
        """testing if a TypeError raised if the body attribute is set to
        anything other than a string or unicode
        """
        
        test_values = [1, 1.0, ["this is the bodybody"],
                       {"this": "is the body"}]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_review,
                "body",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_body_attribute_is_set_properly(self):
        """testing if body attribute is set properly
        """
        
        new_body = "This is a new review body"
        self.test_review.body = new_body
        self.assertEqual(new_body, self.test_review.body)
    
    
    
    #----------------------------------------------------------------------
    def test_body_argument_being_empty(self):
        """testing if everythings will be ok if body argument is set to
        nothing
        """
        
        # creating a new review and skipping the body should work fine
        self.kwargs.pop("body")
        a_new_review =  Review(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_being_none(self):
        """testing if a TypeError will be raised if to argment is tried to be
        set to None
        """
        
        # create a new review with no "to" argument
        self.kwargs["to"] = None
        self.assertRaises(TypeError, Review, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_being_none(self):
        """testing if a TypeError will be raised if the to attribute tried to
        be set to a None value
        """
        
        # try to set the to attribute to none
        
        self.assertRaises(
            TypeError,
            setattr,
            self.test_review,
            "to",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_accepts_anything_that_has_list_like_reviews_attribute(self):
        """testing if an AttributeError will be raised if **to** argument tried
        to be set to something that has no "reviews" attribute
        """
        
        test_values = [1, 1.2, "an Entity"]
        
        for test_value in test_values:
            self.kwargs["to"] = test_value
            
            self.assertRaises(
                TypeError,
                Review,
                **self.kwargs
            )
        
        # lets check with something that has `reviews` attribute
        #class AnObjectWithReviews(object):
            #def __init__(self):
                #self.reviews = []
        
        #an_object = AnObjectWithReviews()
        
        # this should work
        self.kwargs["to"] = self.test_to_object2
        new_review = Review(**self.kwargs)
        
        # check if it is related to the object
        self.assertEqual(new_review.to, self.test_to_object2)
        
        # check if the back reference is updated
        self.assertIn(new_review, self.test_to_object2.reviews)
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_accepts_anything_that_has_list_like_reviews_attribute(self):
        """testing if an AttributeError will be raised if the to attribute
        tried to be set to something that has no "reveiews" attribute
        """
        
        # try to set the to attribute to something other than an entity object
        self.assertRaises(
            TypeError,
            setattr,
            self.test_review,
            "to",
            "an Entity"
        )
        
        
        # lets check with something that has `reviews` attribute
        #class AnObjectWithReviews(object):
            #def __init__(self):
                #self.reviews = []
        
        #an_object = AnObjectWithReviews()
        
        prev_owner = self.test_review.to
        
        # this should work
        self.test_review.to = self.test_to_object2
        
        # check if it is related to the object
        self.assertEqual(self.test_review.to, self.test_to_object2)
        
        # check if the back reference is updated
        self.assertIn(self.test_review, self.test_to_object2.reviews)
        
        # check if the review is removed from the previous owner
        self.assertNotIn(self.test_review, prev_owner.reviews)
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_has_reviews_attribute_but_not_list_like(self):
        """testing if an AttributeError will be raised when the object given
        with the `to` argument has an "review" attribute but it is not
        list-like
        """
        
        # lets check with something that has `reviews` attribute
        class AnObjectWithReviews(object):
            def __init__(self):
                self.reviews = "" # not list
        
        an_object = AnObjectWithReviews()
        
        self.kwargs["to"] = an_object
        
        self.assertRaises(TypeError, Review, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_has_reviews_attribute_but_not_list_like(self):
        """testing if an AttributeError will be raised when the object given
        with the `to` attribute has an "review" attribute but it is not
        list-like
        """
        
        # lets check with something that has `reviews` attribute
        class AnObjectWithReviews(object):
            def __init__(self):
                self.reviews = "" # not list
        
        an_object = AnObjectWithReviews()
        
        self.assertRaises(TypeError, setattr, self.test_review, "to",
                          an_object)
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_being_skipped(self):
        """testing if a TypeError will be raised if **to** argument is skipped
        """
        
        # this should raise a TypeError
        self.kwargs.pop("to")
        
        self.assertRaises(
            TypeError,
            Review,
            **self.kwargs
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_is_set_properly(self):
        """testing if to attribute is set properly
        """
        
        new_to = self.test_to_object2
        self.test_review.to = new_to
        self.assertEqual(new_to, self.test_review.to)
    
    
    
    #----------------------------------------------------------------------
    def test_plural_name(self):
        """testing the plural name of Review class
        """
        
        self.assertTrue(Review.plural_name, "Reviews")
    
    
    