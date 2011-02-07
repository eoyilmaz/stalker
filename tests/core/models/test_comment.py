#-*- coding: utf-8 -*-



import mocker
import datetime
from stalker.core.models import comment, entity, user, tag






########################################################################
class CommentTest(mocker.MockerTestCase):
    """testing the Comment model
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setting up the test
        """
        
        # will need:
        # a mock entity object
        # a couple of mock tag objects
        
        # a couple of mock tags
        self.mock_tag1 = self.mocker.mock(tag.Tag)
        self.mock_tag2 = self.mocker.mock(tag.Tag)
        
        # a mock entity object
        self.mock_entity = self.mocker.mock(entity.Entity)
        self.mock_entity2 = self.mocker.mock(entity.Entity)
        
        # creation and update dates
        self.date_created = datetime.datetime.now()
        self.date_updated = self.date_created
        
        # a mock user object
        self.mock_user = self.mocker.mock(user.User)
        
        self.mocker.replay()
        
        self.kwargs = {
            "name": "Test Comment",
            "description": "this is a test object",
            "tags": [self.mock_tag1, self.mock_tag2],
            "created_by": self.mock_user,
            "updated_by": self.mock_user,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "body": "This is the content of the comment",
            "to": self.mock_entity
        }
        
        self.comment = comment.Comment(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_body_argument_accepts_string_or_unicode_only(self):
        """testing if a ValueError raised if the body argument is set to
        anything other than a string or unicode
        """
        
        # create a new comment with false values
        
        test_values = [1, 1.0, ["this is the bodybody"],
                       {"this": "is the body"}]
        
        for test_value in test_values:
            self.kwargs["body"] = test_value
            self.assertRaises(
                ValueError,
                comment.Comment,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_body_attribute_being_string_or_unicode(self):
        """testing if a ValueError raised if the body attribute is set to
        anything other than a string or unicode
        """
        
        test_values = [1, 1.0, ["this is the bodybody"],
                       {"this": "is the body"}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.comment,
                "body",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_body_attribute_is_set_properly(self):
        """testing if body attribute is set properly
        """
        
        new_body = "This is a new comment body"
        self.comment.body = new_body
        self.assertEquals(new_body, self.comment.body)
    
    
    
    #----------------------------------------------------------------------
    def test_body_argument_being_empty(self):
        """testing if everythings will be ok if body argument is set to
        nothing
        """
        
        # creating a new comment and skipping the body should work fine
        self.kwargs.pop("body")
        a_new_comment =  comment.Comment(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_being_none(self):
        """testing if a ValueError will be raised if to argment is tried to be
        set to None
        """
        
        # create a new comment with no "to" argument
        self.kwargs["to"] = None
        self.assertRaises(ValueError, comment.Comment, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_being_none(self):
        """testing if a ValueError will be raised if the to attribute tried to
        be set to a None value
        """
        
        # try to set the to attribute to none
        
        self.assertRaises(
            ValueError,
            setattr,
            self.comment,
            "to",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_accepts_entity_only(self):
        """testing if a ValueError will be raised if **to** argument tried
        to be set to something other than an entity object
        """
        
        test_values = [1, 1.2, "an Entity"]
        
        for test_value in test_values:
            self.kwargs["to"] = test_value
            
            self.assertRaises(
                ValueError,
                comment.Comment,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_being_set_to_other_than_entity(self):
        """testing if a ValueError will be raised if the to attribute tried to
        be set to a something other than an entity object
        """
        
        # try to set the to attribute to something other than an entity object
        self.assertRaises(
            ValueError,
            setattr,
            self.comment,
            "to",
            "an Entity"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_being_skipped(self):
        """testing if a ValueError will be raised if **to** argument is skipped
        """
        
        # this should raise a ValueError
        self.kwargs.pop("to")
        
        self.assertRaises(
            ValueError,
            comment.Comment,
            **self.kwargs
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_attribute_is_set_properly(self):
        """testing if to attribute is set properly
        """
        
        new_to = self.mock_entity2
        self.comment.to = new_to
        self.assertEquals(new_to, self.comment.to)
    
    
    