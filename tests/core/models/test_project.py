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
    def test_start_property_is_not_a_date_object(self):
        """testing if a ValueError will be raised when trying to set the
        start property to something other than a datetime.date object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_start_argument_is_given_as_None(self):
        """testing if nothing will happen when trying to set the start argument
        to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_start_property_is_set_to_None(self):
        """testing if no error will be raised when trying to set the start
        property to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_start_property_works_properly(self):
        """testing if the start propertly is working properly
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_argument_is_not_a_date_object(self):
        """testing if a ValueError will be raised when trying to set the due
        date something other than a datetime.date object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_property_is_not_a_date_object(self):
        """testing if a ValueError will be raised when trying to set the due
        property is to something other than a datetime.date object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_argument_is_set_to_None(self):
        """testing if no error will be raised when trying to set the due
        argument to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_property_is_set_to_None(self):
        """testing if no error will be raised when trying to set the due
        property to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_argument_is_given_as_timedelta_converted_to_datetime(self):
        """testing if due date attribute is converted to a proper
        datetime.date object when due argument is given as a datetime.timedelta
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_property_is_given_as_timedelta_converted_to_datetime(self):
        """testing if due date attribute is converted to a proper datetime.date
        object when the due property is set to datetime.timedelta
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_argument_is_given_as_timedelta_and_start_as_None(self):
        """testing if the due date attribute is kept as timedelta when the
        start attribute is None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_property_is_given_as_timedelta_and_start_as_None(self):
        """testing if the due date attribute is kept as timedelta when the
        start attribute is None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_attribute_is_converted_to_timedelta_when_start_set_to_None(self):
        """testing if the due date attribute is converted to timedelta when the
        start attribute is set to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_argument_is_tried_to_set_to_a_time_before_start(self):
        """testing if a ValueError will be raised when the due argument is
        given as a value which is a date before start
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_property_is_tried_to_set_to_a_time_before_start(self):
        """testing if a ValueError will be raised when the due property is
        tried to be set to a date before start
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_argument_is_date_and_start_is_None_converted_to_timedelta(self):
        """testing if the due is converted to timedelta when the start is given
        as None, and the timedelta value is calculated from now
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_due_property_is_date_and_start_is_None_converted_to_timedelta(self):
        """testing if the due attribute is converted to timedelta when the
        start is given as None, and the timedelta value is calculated from now
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_given_as_None(self):
        """testing if no error will be raised when the lead arguments is given
        as None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_lead_property_is_given_as_None(self):
        """testing if no error will be raised when the lead property is set to
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
    def test_lead_property_is_set_to_something_other_than_a_user(self):
        """testing if a ValueError will be raised when the lead property is
        set to something other than a user.User object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_users_is_set_to_None(self):
        """testing if no error will be raised when the 
        """
        





