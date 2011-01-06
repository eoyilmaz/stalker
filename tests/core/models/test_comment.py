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
        
        self.name = 'Test Comment'
        self.description = 'this is a test object'
        
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
        
        # the body of the comment
        self.body = 'This is the content of the comment'
        
        self.mocker.replay()
        
        self.comment = comment.Comment(
            name=self.name,
            description=self.description,
            tags=[self.mock_tag1, self.mock_tag2],
            created_by=self.mock_user,
            updated_by=self.mock_user,
            date_created=self.date_created,
            date_updated=self.date_updated,
            body=self.body,
            to=self.mock_entity
        )
    
    
    
    #----------------------------------------------------------------------
    def test_body_argument_accepts_string_or_unicode_only(self):
        """testing if a ValueError raised if the body argument is set to
        anything other than a string or unicode
        """
        
        # create a new comment with false values
        self.assertRaises(
            ValueError,
            comment.Comment,
            name=self.name,
            description=self.description,
            tags=[self.mock_tag1, self.mock_tag2],
            created_by=self.mock_user,
            updated_by=self.mock_user,
            date_created=self.date_created,
            date_updated=self.date_updated,
            body=1,
            to=self.mock_entity
        )
    
    
    
    #----------------------------------------------------------------------
    def test_body_property_being_string_or_unicode(self):
        """testing if a ValueError raised if the body **property** is set to
        anything other than a string or unicode
        """
        
        new_body = 1
        
        self.assertRaises(
            ValueError,
            setattr,
            self.comment,
            'body',
            new_body
        )
    
    
    
    #----------------------------------------------------------------------
    def test_body_property_is_set_properly(self):
        """testing if the body property is set properly
        """
        
        new_body = 'This is a new comment body'
        self.comment.body = new_body
        self.assertEquals(new_body, self.comment.body)
    
    
    
    #----------------------------------------------------------------------
    def test_body_argument_being_empty(self):
        """testing if everythings will be ok if body argument is set to
        nothing
        """
        
        # creating a new comment and skipping the body should work fine
        a_new_comment =  comment.Comment(
            name=self.name,
            description=self.description,
            tags=[self.mock_tag1, self.mock_tag2],
            created_by=self.mock_user,
            updated_by=self.mock_user,
            date_created=self.date_created,
            date_updated=self.date_updated,
            to=self.mock_entity
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_being_none(self):
        """testing if a ValueError will be raised if to argment is tried to be
        set to None
        """
        
        # create a new comment with no "to" argument
        
        self.assertRaises(
            ValueError,
            comment.Comment,
            name=self.name,
            description=self.description,
            tags=[self.mock_tag1, self.mock_tag2],
            created_by=self.mock_user,
            updated_by=self.mock_user,
            date_created=self.date_created,
            date_updated=self.date_updated,
            body=self.body,
            to=None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_property_being_none(self):
        """testing if a ValueError will be raised if the to **property** tried
        to be set to a None value
        """
        
        # try to set the to property to none
        
        self.assertRaises(
            ValueError,
            setattr,
            self.comment,
            'to',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_accepts_entity_only(self):
        """testing if a ValueError will be raised if **to** argument tried
        to be set to something other than an entity object
        """
        
        self.assertRaises(
            ValueError,
            comment.Comment,
            name=self.name,
            description=self.description,
            tags=[self.mock_tag1, self.mock_tag2],
            created_by=self.mock_user,
            updated_by=self.mock_user,
            date_created=self.date_created,
            date_updated=self.date_updated,
            body=self.body,
            to='an Entity'
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_property_being_set_to_other_than_entity(self):
        """testing if a ValueError will be raised if the **to** **property**
        tried to be set to a something other than an entity object
        """
        
        # try to set the to property to something other than an entity object
        self.assertRaises(
            ValueError,
            setattr,
            self.comment,
            'to',
            'an Entity'
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_argument_being_skipped(self):
        """testing if a ValueError will be raised if **to** argument is skipped
        """
        
        # this should raise a ValueError
        self.assertRaises(
            ValueError,
            comment.Comment,
            name=self.name,
            description=self.description,
            tags=[self.mock_tag1, self.mock_tag2],
            created_by=self.mock_user,
            updated_by=self.mock_user,
            date_created=self.date_created,
            date_updated=self.date_updated,
            body=self.body,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_to_property_is_set_properly(self):
        """testing if the to property is set properly
        """
        
        new_to = self.mock_entity2
        self.comment.to = new_to
        self.assertEquals(new_to, self.comment.to)
    
    
    