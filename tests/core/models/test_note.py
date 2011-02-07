#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import note






########################################################################
class NoteTester(mocker.MockerTestCase):
    """tests  the Note class
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        
        self.kwargs={
            "name": "Note to something",
            "description": "this is a simple note",
            "content": "this is a note content",
        }
        
        # create a Note object
        self.mock_note = note.Note(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_content_argument_is_missing(self):
        """testing if nothing is going to happen when no content argument is
        given
        """
        
        self.kwargs.pop("content")
        new_note = note.Note(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_content_argument_is_set_to_None(self):
        """testing if nothing is going to happen when content argument is given
        as None
        """
        
        self.kwargs["content"] = None
        new_note = note.Note(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_content_attribute_is_set_to_None(self):
        """testing if nothing is going to happen when content attribute is set
        to None
        """
        
        # nothing should happen
        self.mock_note.content = None
    
    
    
    #----------------------------------------------------------------------
    def test_content_argument_is_set_to_empty_string(self):
        """testing if nothing is going to happen when content argument is given
        as an empty string
        """
        
        self.kwargs["content"] = ""
        new_note = note.Note(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_content_attribute_is_set_to_empty_string(self):
        """testing if nothing is goin to happen when content argument is set to
        an empty string
        """
        
        # nothing should happen
        self.mock_note.content = ""
    
    
    
    #----------------------------------------------------------------------
    def test_content_argument_is_set_to_something_other_than_a_string(self):
        """testing if a ValueEror will be raised when trying to set the content
        argument to something other than a string or unicode
        """
        
        test_values = [1, 1.24, ["content"], {"a": "Content"}]
        
        for test_value in test_values:
            self.kwargs["content"] = test_value
            self.assertRaises(ValueError, note.Note, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_content_attribute_is_set_to_something_other_than_a_string(self):
        """testing if a ValueError will be raised when trying to set the
        content attribute to something other than a string or unicode
        """
        
        test_values = [1, 1.24, ["content"], {"a": "Content"}]
        
        for test_value in test_values:
            
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_note,
                "content",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_content_attribute_is_working_properly(self):
        """testing if the content attribute is working properly
        """
        
        new_content = "This is my new content for the note, and I expect it to\
        work fine when I assign it to a Note object"
        
        self.mock_note.content = new_content
        
        self.assertEquals(self.mock_note.content, new_content)
    
    
    
    #----------------------------------------------------------------------
    def test_equality_operator(self):
        """testing equality operator
        """
        
        note1 = note.Note(**self.kwargs)
        note2 = note.Note(**self.kwargs)
        
        self.kwargs["content"] = "this is a different content"
        note3 = note.Note(**self.kwargs)
        
        self.assertTrue(note1==note2)
        self.assertFalse(note1==note3)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality_operator(self):
        """testing inequality operator
        """
        
        note1 = note.Note(**self.kwargs)
        note2 = note.Note(**self.kwargs)
        
        self.kwargs["content"] = "this is a different content"
        note3 = note.Note(**self.kwargs)
        
        self.assertFalse(note1!=note2)
        self.assertTrue(note1!=note3)
    
    
    