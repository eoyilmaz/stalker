#-*- coding: utf-8 -*-


import datetime
import mocker
from stalker.core.models import (user, sequence, asset, imageFormat, types,
                                 project, structure, repository, entity,
                                 status)
from stalker.ext.validatedList import ValidatedList





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
        
        
        self.mock_status_list = self.mocker.mock(status.StatusList)
        self.expect(self.mock_status_list.target_entity_type).\
            result(project.Project.entity_type).count(0, None)
        self.expect(len(self.mock_status_list.statuses)).result(5).count(0,None)
        
        self.mocker.replay()
        
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
            "display_width": 15,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "status_list": self.mock_status_list,
        }
        
        self.mock_project = project.Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_start_argument_is_not_a_date_object(self):
        """testing if a ValueError will be raised when the start is given as
        something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            self.kwargs["start_date"] = test_value
            
            self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_start_attribute_is_not_a_date_object(self):
        """testing if a ValueError will be raised when trying to set the
        start attribute to something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_project,
                "start_date",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_argument_is_given_as_None_use_the_default_value(self):
        """testing if the start_date argument is given as None, will use the
        today as the start date
        """
        
        self.kwargs["start_date"] = None
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.start_date, datetime.date.today())
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_attribute_is_set_to_None_use_the_default_value(self):
        """testing if setting the start_date attribute to None will update the
        start_date to today
        """
        
        self.mock_project.start_date = None
        self.assertEquals(self.mock_project.start_date, datetime.date.today())
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_attribute_works_properly(self):
        """testing if the start propertly is working properly
        """
        
        test_value = datetime.date(year=2011, month=1, day=1)
        self.mock_project.start_date = test_value
        self.assertEquals(self.mock_project.start_date, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_not_a_date_or_timedelta_object(self):
        """testing if a ValueError will be raised when trying to set the due
        date something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            self.kwargs["due_date"] = test_value
            self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_not_a_date_or_timedelta_object(self):
        """testing if a ValueError will be raised when trying to set the due
        attribute is to something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_project,
                "due_date",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_set_to_None_will_use_the_default_value(self):
        """testing if given the due_date argument given as None will use the
        default value, which is 10 days after the start_date
        """
        
        self.kwargs["due_date"] = None
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.due_date - new_project.start_date,
                          datetime.timedelta(days=10))
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_set_to_None_will_use_the_default_value(self):
        """testing if setting the due_date attribute to None will use the
        default value, which is 10 days after the start_date
        """
        
        self.mock_project.due_date = None
        self.assertEquals(
            self.mock_project.due_date - self.mock_project.start_date,
            datetime.timedelta(days=10)
        )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_given_as_timedelta_converted_to_datetime(self):
        """testing if due date attribute is converted to a proper
        datetime.date object when due argument is given as a datetime.timedelta
        """
        
        test_value = datetime.timedelta(days=20)
        self.kwargs["due_date"] = test_value
        new_project = project.Project(**self.kwargs)
        
        self.assertIsInstance(new_project.due_date, datetime.date)
        
        self.assertEquals(
            new_project.due_date - new_project.start_date,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_set_to_timedelta_converted_to_datetime(self):
        """testing if due date attribute is converted to a proper datetime.date
        object when the due attribute is set to datetime.timedelta
        """
        
        test_value = datetime.timedelta(days=20)
        self.mock_project.due_date = test_value
        
        self.assertIsInstance(self.mock_project.due_date, datetime.date)
        
        self.assertEquals(
            self.mock_project.due_date - self.mock_project.start_date,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_tried_to_set_to_a_time_before_start_date(self):
        """testing if a ValueError will be raised when the due argument is
        given as a value which is a date before start
        """
        
        self.kwargs["due_date"] = self.kwargs["start_date"] - \
            datetime.timedelta(days=10)
        
        self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_tried_to_set_to_a_time_before_start_date(self):
        """testing if a ValueError will be raised when the due attribute is
        tried to be set to a date before start
        """
        
        new_due_date = self.mock_project.start_date - \
                     datetime.timedelta(days=10)
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_project,
            "due_date",
            new_due_date
        )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_shifted_when_start_date_passes_it(self):
        """testing if due_date attribute will be shifted when the start_date
        attribute passes it
        """
        
        time_delta = self.mock_project.due_date - self.mock_project.start_date
        self.mock_project.start_date += 2 * time_delta
        
        self.assertEquals(
            self.mock_project.due_date - self.mock_project.start_date,
            time_delta
        )
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_given_as_None(self):
        """testing if no error will be raised when the lead arguments is given
        as None
        """
        
        self.kwargs["lead"] = None
        new_project = project.Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_set_to_None(self):
        """testing if no error will be raised when the lead attribute is set to
        None
        """
        
        self.mock_project.lead = None
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_given_as_something_other_than_a_user(self):
        """testing if a ValueError will be raised when the lead argument is
        given as something other than a user.User object
        """
        
        test_values = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        
        for test_value in test_values:
            self.kwargs["lead"] = test_value
            self.assertRaises(
                ValueError,
                project.Project,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_set_to_something_other_than_a_user(self):
        """testing if a ValueError will be raised when the lead attribute is
        set to something other than a user.User object
        """
        
        test_values = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_project,
                "lead",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_users_argument_is_set_to_None(self):
        """testing if no error will be raised when the users argument is given
        as None
        """
        
        self.kwargs["users"] = None
        new_project = project.Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_set_to_None(self):
        """testing if no error will be raised when the users attribute is set
        to None
        """
        
        self.mock_project.users = None
    
    
    
    #----------------------------------------------------------------------
    def test_users_argument_given_as_None_converted_to_empty_list(self):
        """testing if users argument is converted to an empty list when given
        as None
        """
        
        self.kwargs["users"] = None
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.users, [])
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_set_to_None_converted_to_empty_list(self):
        """testing if users attribute is converted to an empty list when set to
        None
        """
        
        self.mock_project.users = None
        self.assertEquals(self.mock_project.users, [])
    
    
    
    #----------------------------------------------------------------------
    def test_users_argument_is_given_as_a_list_of_other_objects_then_user(self):
        """testing if a ValueError will be raised when the users argument is
        given as a list containing objects other than user.User
        """
        
        test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        self.kwargs["users"] = test_value
        self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_given_as_a_list_of_other_objects_then_user(self):
        """testing if a ValueError will be raised when the users attribute is
        given as a list containing objects other than user.User
        """
        
        test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_project,
            "users",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_a_ValidatedList_instance(self):
        """testing if the users attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_project.users, ValidatedList)
    
    
    
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
    def test_sequences_argument_is_given_as_None(self):
        """testing if sequence attribute is set to an empty list when the
        sequences argument is given as None
        """
        
        self.kwargs["sequences"] = None
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.sequences, [])
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_set_to_None_converted_to_empty_list(self):
        """testing if sequence attribute is set to an empty list when it is set
        to None
        """
        
        self.mock_project.sequences = None
        self.assertEquals(self.mock_project.sequences, [])
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_argument_is_given_as_an_empty_list(self):
        """testing if nothing happens when the sequences argument is given as
        an empty list
        """
        
        self.kwargs["sequences"] = []
        new_project = project.Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_set_to_an_empty_list(self):
        """testing if nothing happens when the seuqences attribute is set to an
        empty list
        """
        
        self.mock_project.sequences = []
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_argument_is_given_as_a_list_containing_non_Sequence_objects(self):
        """testing if a ValueError will be raised when trying the given
        sequences argument is a list containing objects other than Sequence
        instances
        """
        
        test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        self.kwargs["sequences"] = test_value
        self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_set_to_a_list_containing_non_Sequence_objects(self):
        """testing if a ValueError will be raised when trying to set the
        sequences list to a list containing objects other than Sequence
        instances
        """
        
        test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_project,
            "sequences",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_a_ValidatedList_instance(self):
        """testing if the sequences attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_project.sequences, ValidatedList)
    
    
    
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
    def test_assets_argument_is_given_as_None(self):
        """testing if assets attribute is set to an empty list when the assets
        argument is given as None
        """
        
        self.kwargs["assets"] = None
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.assets, [])
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_None_converted_to_empty_list(self):
        """testing if assets attribute is set to an empty list when it is set
        to None
        """
        
        self.mock_project.assets = None
        self.assertEquals(self.mock_project.assets, [])
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_skipped_and_intializied_as_an_empty_list(self):
        """testing if skipping the assets list argument will initialize the
        assets attribute to an empty list
        """
        
        self.kwargs.pop("assets")
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.assets, [])
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_given_as_an_empty_list(self):
        """testing if nothing happens when the assets argument is given as
        an empty list
        """
        
        self.kwargs["assets"] = []
        new_project = project.Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_an_empty_list(self):
        """testing if nothing happens when the assets attribute is set to an
        empty list
        """
        
        self.mock_project.assets = []
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_a_list_containing_non_Asset_objects(self):
        """testing if a ValueError will be raised when the assets argument is
        given as a list containing objects other than Assets instances
        """
        
        test_value = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        self.kwargs["assets"] = test_value
        self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_a_list_containing_non_Asset_objects(self):
        """testing if a ValueError will be raised when trying to set the
        assets list to a list containing objects other than Assets instances
        """
        
        test_value = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_project,
            "assets",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_a_ValidatedList_instance(self):
        """testing if the assets attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_project.assets, ValidatedList)
    
    
    
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
        
        self.kwargs["image_format"] = None
        self.assertRaises(ValueError, project.Project, self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_attribute_is_set_to_None(self):
        """testing if a ValueError will be raised when the image_format
        attribute is set to None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_project,
            "image_format",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_argument_accepts_ImageFormat_only(self):
        """testing if a ValueError will be raised when the image_format
        argument is given as another type then ImageFormat
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        
        for test_value in test_values:
            self.kwargs["image_format"] = test_value
            self.assertRaises(ValueError, project.Project, **self.kwargs)
        
        # and a proper image format
        self.kwargs["image_format"] = self.mock_imageFormat
        new_project = project.Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_attribute_accepts_ImageFormat_only(self):
        """testing if a ValueError will be raised when the image_format
        attribute is tried to be set to something other than a ImageFormat
        instance
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_project,
                "image_format",
                test_value
            )
        
        # and a proper image format
        self.mock_project.image_format = self.mock_imageFormat
    
    
    
    #----------------------------------------------------------------------
    def test_fps_argument_is_skipped(self):
        """testing if the default value will be used when fps is skipped
        """
        
        self.kwargs.pop("fps")
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.fps, 25.0)
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the fps attribute is set
        to None
        """
        
        self.kwargs["fps"] = None
        self.assertRaises(TypeError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_fps_argument_is_given_as_non_float_or_integer(self):
        """testing if a ValueError will be raised when the fps argument is
        given as a value other than a float or integer, or a string which is
        convertable to float
        """
        
        test_values = ["a str"]
        for test_value in test_values:
            self.kwargs["fps"] = test_value
            self.assertRaises(
                ValueError,
                project.Project,
                **self.kwargs
            )
        
        test_values = [["a", "list"], {"a": "list"}]
        for test_value in test_values:
            self.kwargs["fps"] = test_value
            self.assertRaises(
                TypeError,
                project.Project,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_is_given_as_non_float_or_integer(self):
        """testing if a ValueError will be raised when the fps attribute is
        set to a value other than a float, integer or valid string literals
        """
        
        test_values = ["a str"]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_project,
                "fps",
                test_value
            )
        
        test_values = [["a", "list"], {"a": "list"}]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_project,
                "fps",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_fps_argument_string_to_float_conversion(self):
        """testing if valid string literals of fps argument will be converted
        to float correctly
        """
        
        test_values = [("1", 1.0), ("2.3", 2.3)]
        
        for test_value in test_values:
            self.kwargs["fps"] = test_value[0]
            new_project = project.Project(**self.kwargs)
            self.assertAlmostEquals(new_project.fps, test_value[1]) 
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_string_to_float_conversion(self):
        """testing if valid string literals of fps attribute will be converted
        to float correctly
        """
        
        test_values = [("1", 1.0), ("2.3", 2.3)]
        
        for test_value in test_values:
            self.mock_project.fps = test_value[0]
            self.assertAlmostEquals(self.mock_project.fps, test_value[1]) 
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_float_conversion(self):
        """testing if the fps attribute is converted to float when the float
        argument is given as an integer
        """
        
        test_value = 1
        
        self.kwargs["fps"] = test_value
        new_project = project.Project(**self.kwargs)
        self.assertIsInstance(new_project.fps, float)
        self.assertEquals(new_project.fps, float(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_float_conversion_2(self):
        """testing if the fps attribute is converted to float when it is set to
        an integer value
        """
        
        test_value = 1
        
        self.mock_project.fps = test_value
        self.assertIsInstance(self.mock_project.fps, float)
        self.assertEquals(self.mock_project.fps, float(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_given_as_non_ProjectType_object(self):
        """testing if a ValueError will be raised when the type argument is
        given as something other than a ProjectType object
        """
        
        test_values = [None, 1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        
        for test_value in test_values:
            self.kwargs["type"] = test_value
            self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_set_to_non_ProjectType_object(self):
        """testing if a ValueError will be raised when the type attribute is
        set to something other than a ProjectType object
        """
        
        test_values = [None, 1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_project,
                "type",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_repository_argument_is_None(self):
        """testing if a ValueError will be raised when the repository argument
        is None
        """
        
        self.kwargs["repository"] = None
        self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_repository_attribute_is_set_to_None(self):
        """testing if a ValueError will be raised when the repository argument
        is set to None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_project,
            "repository",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_repository_argument_is_non_Repository_object(self):
        """testing if a ValueError will be raised when the repository argument
        is given as something other than a Repository object
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        for test_value in test_values:
            self.kwargs["repository"] = test_value
            self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_repository_attribute_is_set_to_non_Repository_object(self):
        """testing if a ValueErorr will be raised when the repository attribute
        is tried to be set to something other than a Repository object
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_project,
                "repository",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_is_stereoscopic_argument_skipped(self):
        """testing if is_stereoscopic will set the is_stereoscopic attribute to
        False
        """
        
        self.kwargs.pop("is_stereoscopic")
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.is_stereoscopic, False)
    
    
    
    #----------------------------------------------------------------------
    def test_is_stereoscopic_argument_bool_conversion(self):
        """testing if all the given values for is_stereoscopic argument will be
        converted to a bool value correctly
        """
        
        test_values = [0, 1, 1.2, "", "str", ["a", "list"]]
        
        for test_value in test_values:
            self.kwargs["is_stereoscopic"] = test_value
            new_project = project.Project(**self.kwargs)
            self.assertEquals(new_project.is_stereoscopic, bool(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_is_stereoscopic_attribute_bool_conversion(self):
        """testing if all the given values for is_stereoscopic attribute will
        be converted to a bool value correctly
        """
        
        test_values = [0, 1, 1.2, "", "str", ["a", "list"]]
        
        for test_value in test_values:
            self.mock_project.is_stereoscopic = test_value
            self.assertEquals(
                self.mock_project.is_stereoscopic,
                bool(test_value)
            )
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_argument_is_skipped(self):
        """testing if the display_width attribute will be set to the default
        value when the display_width argument is skipped
        """
        
        self.kwargs.pop("display_width")
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.display_width, 1.0)
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_argument_float_conversion(self):
        """testing if the display_width attribute is converted to float
        correctly for various display_width arguments
        """
        
        test_values = [1, 2, 3, 4]
        for test_value in test_values:
            self.kwargs["display_width"] = test_value
            new_project = project.Project(**self.kwargs)
            self.assertIsInstance(new_project.display_width, float)
            self.assertEquals(new_project.display_width, float(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_attribute_float_conversion(self):
        """testing if the display_width attribute is converted to float
        correctly
        """
        
        test_values = [1, 2, 3, 4]
        for test_value in test_values:
            self.mock_project.display_width = test_value
            self.assertIsInstance(self.mock_project.display_width, float)
            self.assertEquals(self.mock_project.display_width,
                              float(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_argument_is_given_as_a_negative_value(self):
        """testing if the display_width attribute is set to the absolute value
        of the given negative display_width argument
        """
        
        test_value = -1.0
        self.kwargs["display_width"] = test_value
        new_project = project.Project(**self.kwargs)
        self.assertEquals(new_project.display_width, abs(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_attribute_is_set_to_a_negative_value(self):
        """testing if the display_width attribute is set to default value when
        it is set to a negative value
        """
        
        test_value = -1.0
        self.mock_project.display_width = test_value
        self.assertEquals(self.mock_project.display_width, abs(test_value))
    
    
    
    #----------------------------------------------------------------------
    def tets_structure_argument_not_instance_of_Structure(self):
        """testing if a ValueError will be raised when the structure argument
        is not an instance of Structure
        """
        
        test_values = [None, 1, 1.2, "a str", ["a", "list"]]
        
        for test_value in test_values:
            self.kwargs["structure"] = test_value
            self.assertRaises(ValueError, project.Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_structure_attribute_not_instance_of_Structure(self):
        """testing if a ValueError will be raised when the structure attribute
        is not an instance of Structure
        """
        
        test_values = [None, 1, 1.2, "a str", ["a", "list"]]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_project,
                "structure",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality of two projects
        """
        
        # create a new project with the same arguments
        new_project = project.Project(**self.kwargs)
        
        # create a new entity with the same arguments
        new_entity = entity.Entity(**self.kwargs)
        
        self.assertTrue(self.mock_project==new_project)
        self.assertFalse(self.mock_project==new_entity)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality of two projects
        """
        
        # create a new project with the same arguments
        new_project = project.Project(**self.kwargs)
        
        # create a new entity with the same arguments
        new_entity = entity.Entity(**self.kwargs)
        
        self.assertFalse(self.mock_project!=new_project)
        self.assertTrue(self.mock_project!=new_entity)
    
    
    