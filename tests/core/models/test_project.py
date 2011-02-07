#-*- coding: utf-8 -*-


import datetime
import mocker
from stalker.core.models import (user, sequence, asset, imageFormat, types,
                                 structure, repository)






########################################################################
class ProjectTester(mocker.MockerTestCase):
    """tests the Project class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create mock objects
        
        self.start_date = datetime.date.today()
        self.due_date = self.start_date + datetime.timedelta(days=20)
        
        self.mock_lead = self.mocker.mock(user.User)
        
        self.mock_user1 = self.mocker.mock(user.User)
        self.mock_user2 = self.mocker.mock(user.User)
        self.mock_user3 = self.mocker.mock(user.User)
        
        self.mock_seq1 = self.mocker.mock(sequence.Sequence)
        self.mock_seq2 = self.mocker.mock(sequence.Sequence)
        self.mock_seq3 = self.mocker.mock(sequence.Sequence)
        
        self.mock_asset1 = self.mocker.mock(asset.Asset)
        self.mock_asset2 = self.mocker.mock(asset.Asset)
        self.mock_asset3 = self.mocker.mock(asset.Asset)
        
        self.mock_imageFormat = self.mocker.mock(imageFormat.ImageFormat)
        
        self.mock_project_type = self.mocker.mock(types.ProjectType)
        
        self.mock_project_structure = self.mocker.mock(structure.Structure)
        
        self.mock_repo = self.mocker.mock(repository.Repository)
        
        # create a project object
        
        self.kwargs = {
            "name": "Test Project",
            "description": "This is a project object for testing purposes",
            "lead": self.mock_lead,
            "users": [self.mock_user1, self.mock_user2, self.mock_user3],
            "sequences": [self.mock_seq1, self.mock_seq2, self.mock_seq3],
            "assets": [self.mock_asset1, self.mock_asset2, self.mock_asset3],
            "image_format": self.mock_imageFormat,
            "fps": 25,
            "type": self.mock_project_type,
            "structure": self.mock_project_structure,
            "repository": self.mock_repo,
            "is_stereoscopic": False,
            "display_width": 15
        }
    
    
    
    #----------------------------------------------------------------------
    def test_start_argument_is_not_a_date_object(self):
        """testing if a ValueError will be raised when the start is given as
        something other than a datetime.date object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_start_attribute_is_not_a_date_object(self):
        """testing if a ValueError will be raised when trying to set the
        start attribute to something other than a datetime.date object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_argument_is_given_as_None_use_the_default_value(self):
        """testing if the start_date argument is given as None, will use the
        today as the start date
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_attribute_is_set_to_None_use_the_default_value(self):
        """testing if setting the start_date attribute to None will update the
        start_date to today
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_attribute_works_properly(self):
        """testing if the start propertly is working properly
        """
        
        self.fail("test is not implemented yet")
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_not_a_date_or_timedelta_object(self):
        """testing if a ValueError will be raised when trying to set the due
        date something other than a datetime.date object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_not_a_date_or_timedelta_object(self):
        """testing if a ValueError will be raised when trying to set the due
        attribute is to something other than a datetime.date object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_set_to_None_will_use_the_default_value(self):
        """testing if given the due_date argument given as None will use the
        default value, which is 10 days after the start_date
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_set_to_None_will_use_the_default_value(self):
        """testing if setting the due_date attribute to None will use the
        default value, which is 10 days after the start_date
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_given_as_timedelta_converted_to_datetime(self):
        """testing if due date attribute is converted to a proper
        datetime.date object when due argument is given as a datetime.timedelta
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_set_to_timedelta_converted_to_datetime(self):
        """testing if due date attribute is converted to a proper datetime.date
        object when the due attribute is set to datetime.timedelta
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_tried_to_set_to_a_time_before_start_date(self):
        """testing if a ValueError will be raised when the due argument is
        given as a value which is a date before start
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_tried_to_set_to_a_time_before_start_date(self):
        """testing if a ValueError will be raised when the due attribute is
        tried to be set to a date before start
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_shifted_when_start_date_passes_it(self):
        """testing if due_date attribute will be shifted when the start_date
        attribute passes it
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_given_as_None(self):
        """testing if no error will be raised when the lead arguments is given
        as None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_given_as_None(self):
        """testing if no error will be raised when the lead attribute is set to
        None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_given_as_something_other_than_a_user(self):
        """testing if a ValueError will be raised when the lead argument is
        given as something other than a user.User object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_set_to_something_other_than_a_user(self):
        """testing if a ValueError will be raised when the lead attribute is
        set to something other than a user.User object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    
    #----------------------------------------------------------------------
    def test_users_argument_is_set_to_None(self):
        """testing if no error will be raised when the users argument is given
        as None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_set_to_None(self):
        """testing if no error will be raised when the users attribute is set
        to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_users_argument_given_as_None_converted_to_empty_list(self):
        """testing if users argument is converted to an empty list when given
        as None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_set_to_None_converted_to_empty_list(self):
        """testing if users attribute is converted to an empty list when set to
        None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_users_argument_is_given_as_a_list_of_other_objects_then_user(self):
        """testing if a ValueError will be raised when the users argument is
        given as a list containing objects other than user.User
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_given_as_a_list_of_other_objects_then_user(self):
        """testing if a ValueError will be raised when the users attribute is
        given as a list containing objects other than user.User
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_seuqences_argument_is_given_as_an_empty_list(self):
        """testing if nothing happens when the sequences argument is given as
        an empty list
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_set_to_an_empty_list(self):
        """testing if nothing happens when the seuqences attribute is set to an
        empty list
        """
        
        self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_(self):
        #"""
        #"""
        



