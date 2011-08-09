#-*- coding: utf-8 -*-



import unittest
import datetime
from stalker.core.models import Comment, Entity, User, Tag






########################################################################
class CommentTest(unittest.TestCase):
    """testing the Comment class
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setting up the test
        """
        
        # will need:
        # a test entity object
        # a couple of test tag objects
        
        # a couple of test tags
        self.test_tag1 = Tag(name="Test Tag 1")
        self.test_tag2 = Tag(name="Test Tag 2")
        
        # a test entity object
        self.test_entity = Entity(name="Test Entity 1")
        self.test_entity2 = Entity(name="Test Entity 2")
        
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
            "name": "Test Comment",
            "description": "this is a test object",
            "tags": [self.test_tag1, self.test_tag2],
            "created_by": self.test_user,
            "updated_by": self.test_user,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "body": "This is the content of the comment",
            "to": self.test_entity
        }
        
        self.test_comment = Comment(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_body_argument_accepts_string_or_unicode_only(self):
        """testing if a TypeError raised if the body argument is set to
        anything other than a string or unicode
        """
        
        # create a new comment with false values
        
        test_values = [1, 1.0, ["this is the bodybody"],
                       {"this": "is the body"}]
        
        for test_value in test_values:
            self.kwargs["body"] = test_value
            self.assertRaises(
                TypeError,
                Comment,
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
                self.test_comment,
                "body",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_body_attribute_is_set_properly(self):
        """testing if body attribute is set properly
        """
        
        new_body = "This is a new comment body"
        self.test_comment.body = new_body
        self.assertEqual(new_body, self.test_comment.body)
    
    
    
    #----------------------------------------------------------------------
    def test_body_argument_being_empty(self):
        """testing if everythings will be ok if body argument is set to
        nothing
        """
        
        # creating a new comment and skipping the body should work fine
        self.kwargs.pop("body")
        a_new_comment =  Comment(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_being_none(self):
        """testing if a TypeError will be raised if to argment is tried to be
        set to None
        """
        
        # create a new comment with no "to" argument
        self.kwargs["to"] = None
        self.assertRaises(TypeError, Comment, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_being_none(self):
        """testing if a TypeError will be raised if the to attribute tried to
        be set to a None value
        """
        
        # try to set the to attribute to none
        
        self.assertRaises(
            TypeError,
            setattr,
            self.test_comment,
            "to",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_accepts_entity_only(self):
        """testing if a TypeError will be raised if **to** argument tried
        to be set to something other than an entity object
        """
        
        test_values = [1, 1.2, "an Entity"]
        
        for test_value in test_values:
            self.kwargs["to"] = test_value
            
            self.assertRaises(
                TypeError,
                Comment,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_being_set_to_other_than_entity(self):
        """testing if a TypeError will be raised if the to attribute tried to
        be set to a something other than an entity object
        """
        
        # try to set the to attribute to something other than an entity object
        self.assertRaises(
            TypeError,
            setattr,
            self.test_comment,
            "to",
            "an Entity"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_being_skipped(self):
        """testing if a TypeError will be raised if **to** argument is skipped
        """
        
        # this should raise a TypeError
        self.kwargs.pop("to")
        
        self.assertRaises(
            TypeError,
            Comment,
            **self.kwargs
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_is_set_properly(self):
        """testing if to attribute is set properly
        """
        
        new_to = self.test_entity2
        self.test_comment.to = new_to
        self.assertEqual(new_to, self.test_comment.to)
    
    
    
    #----------------------------------------------------------------------
    def test_plural_name(self):
        """testing the plural name of Comment class
        """
        
        self.assertTrue(Comment.plural_name, "Comments")
    
    
    