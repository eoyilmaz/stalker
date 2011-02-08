#-*- coding: utf-8 -*-


import datetime
import mocker
from stalker.core.models import (user, sequence, asset, imageFormat, types,
                                 project, structure, repository)






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
    def test_users_attribute_is_a_ValidatedList_instance(self):
        """testing if the users attribute is an instance of ValidatedList
        """
        
        self.assertTrue(isinstance(self.mock_project.users, ValidatedList))
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_elements_accepts_User_only(self):
        """testing if a ValueError will be raised when trying to assign
        something other than a User object to the users list
        """
        
        # append
        self.assertRaises(
            ValueError,
            self.mock_project.users.append,
            0
        )
        
        # __setitem__
        self.assertRaises(
            ValueError,
            self.mock_project.users.__setitem__,
            0,
            0
        )
    
    
    
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
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_set_to_a_list_containing_non_Sequence_objects(self):
        """testing if a ValueError will be raised when trying to set the
        sequences list to a list containing objects other than Sequence
        instances
        """
        
        self.fail("test is not implemented yet")
        
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_a_ValidatedList_instance(self):
        """testing if the sequences attribute is an instance of ValidatedList
        """
        
        self.assertTrue(isinstance(self.mock_project.sequences, ValidatedList))
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_elements_accepts_Sequence_only(self):
        """testing if a ValueError will be raised when trying to assign
        something other than a Sequence object to the sequences list
        """
        
        # append
        self.assertRaises(
            ValueError,
            self.mock_project.sequences.append,
            0
        )
        
        # __setitem__
        self.assertRaises(
            ValueError,
            self.mock_project.sequences.__setitem__,
            0,
            0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_given_as_an_empty_list(self):
        """testing if nothing happens when the assets argument is given as
        an empty list
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_an_empty_list(self):
        """testing if nothing happens when the assets attribute is set to an
        empty list
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_a_list_containing_non_Asset_objects(self):
        """testing if a ValueError will be raised when trying to set the
        assets list to a list containing objects other than Assets instances
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_a_ValidatedList_instance(self):
        """testing if the assets attribute is an instance of ValidatedList
        """
        
        self.assertTrue(isinstance(self.mock_project.assets, ValidatedList))
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_elements_accepts_Asset_only(self):
        """testing if a ValueError will be raised when trying to assign
        something other than a Asset instance to the assets list
        """
        
        # append
        self.assertRaises(
            ValueError,
            self.mock_project.assets.append,
            0
        )
        
        # __setitem__
        self.assertRaises(
            ValueError,
            self.mock_project.assets.__setitem__,
            0,
            0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_argument_is_None(self):
        """testing if a ValueError will be raised when the image_format
        argument is None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_attribute_is_set_to_None(self):
        """testing if a ValueError will be raised when the image_format
        attribute is set to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_argument_accepts_ImageFormat_only(self):
        """testing if a ValueError will be raised when the image_format
        argument is given as another type then ImageFormat
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_attribute_accepts_ImageFormat_only(self):
        """testing if a ValueError will be raised when the image_format
        attribute is tried to be set to something other than a ImageFormat
        instance
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_fps_argument_is_skipped(self):
        """testing if a ValueError will be raised the fps argument is skipped
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_is_set_to_None(self):
        """testing if a ValueError will be raised when the fps attribute is set
        to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_fps_argument_is_given_as_non_float_or_integer(self):
        """testing if a ValueError will be raised when the fps argument is
        given as a value other than a float or integer
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_is_given_as_non_float_or_integer(self):
        """testing if a ValueError will be raised when the fps attribute is
        set to a value other than a float or integer
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_float_conversion(self):
        """testing if the fps attribute is converted to float when the float
        argument is given as an integer
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_float_conversion_2(self):
        """testing if the fps attribute is converted to float when it is set to
        an integer value
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_None(self):
        """testing if a ValueError will be raised when the type argument is set
        to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_set_to_None(self):
        """testing if a ValueError will be raised when the type argument is set
        to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_given_as_non_ProjectType_object(self):
        """testing if a ValueError will be raised when the type argument is
        given as something other than a ProjectType object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_set_to_non_ProjectType_object(self):
        """testing if a ValueError will be raised when the type attribute is
        set to something other than a ProjectType object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_structure_argument_is_None(self):
        """testing if a ValueError will be raised when the structure argument
        is given as None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_structure_attribute_is_set_to_None(self):
        """testing if a ValueError will be raised when the structure argument
        is set to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_repository_argument_is_None(self):
        """testing if a ValueError will be raised when the repository argument
        is None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_repository_attribute_is_set_to_None(self):
        """testing if a ValueError will be raised when the repository argument
        is set to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_repository_argument_is_non_Repository_object(self):
        """testing if a ValueError will be raised when the repository argument
        is given as something other than a Repository object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_repository_attribute_is_set_to_non_Repository_object(self):
        """testing if a ValueErorr will be raised when the repository attribute
        is tried to be set to something other than a Repository object
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_is_stereoscopic_argument_skipped(self):
        """testing if is_stereoscopic will set the is_stereoscopic attribute to
        False
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_is_stereoscopic_argument_bool_conversion(self):
        """testing if all the given values for is_stereoscopic argument will be
        converted to a bool value correctly
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_is_stereoscopic_attribute_bool_conversion(self):
        """testing if all the given values for is_stereoscopic attribute will
        be converted to a bool value correctly
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_argument_is_skipped(self):
        """testing if the display_width attribute will be set to the defualt
        value when the display_width argument is skipped
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_argument_float_conversion(self):
        """tetsing if the display_width attribute is converted to float
        correctly for various display_width arguments
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_attribute_float_conversion(self):
        """testing if the display_width attribute is converted to float
        correctly
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_argument_is_given_as_a_negative_value(self):
        """testing if the display_width attribute is set to default value when
        the display_width argument is given as negative value
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_attribute_is_set_to_a_negative_value(self):
        """testing if the display_width attribute is set to default value when
        it is set to a negative value
        """
        
        self.fail("test is not implemented yet")
    
    
    