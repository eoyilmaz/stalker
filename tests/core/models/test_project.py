#-*- coding: utf-8 -*-


import datetime
import mocker
from stalker.core.models import (User, Sequence, Asset, ImageFormat, Project,
                                 Structure, Repository, Entity, Status,
                                 StatusList, Link, Task, Type, Shot)
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
        
        self.mock_lead = self.mocker.mock(User)
        
        self.mock_user1 = self.mocker.mock(User)
        self.mock_user2 = self.mocker.mock(User)
        self.mock_user3 = self.mocker.mock(User)
        self.mock_user4 = self.mocker.mock(User)
        self.mock_user5 = self.mocker.mock(User)
        self.mock_user6 = self.mocker.mock(User)
        self.mock_user7 = self.mocker.mock(User)
        self.mock_user8 = self.mocker.mock(User)
        self.mock_user9 = self.mocker.mock(User)
        self.mock_user10 = self.mocker.mock(User)
        
        # sequences without tasks
        self.mock_seq1 = self.mocker.mock(Sequence)
        self.mock_seq2 = self.mocker.mock(Sequence)
        self.mock_seq3 = self.mocker.mock(Sequence)
        
        # sequences with tasks
        self.mock_seq4 = self.mocker.mock(Sequence)
        self.mock_seq5 = self.mocker.mock(Sequence)
        
        # sequences without tasks but with shots
        self.mock_seq6 = self.mocker.mock(Sequence)
        self.mock_seq7 = self.mocker.mock(Sequence)
        
        # shots
        self.mock_shot1 = self.mocker.mock(Shot)
        self.mock_shot2 = self.mocker.mock(Shot)
        self.mock_shot3 = self.mocker.mock(Shot)
        self.mock_shot4 = self.mocker.mock(Shot)
        
        # assets without tasks
        self.mock_asset1 = self.mocker.mock(Asset)
        self.mock_asset2 = self.mocker.mock(Asset)
        self.mock_asset3 = self.mocker.mock(Asset)
        
        # assets with tasks
        self.mock_asset4 = self.mocker.mock(Asset)
        self.mock_asset5 = self.mocker.mock(Asset)
        
        self.mock_imageFormat = self.mocker.mock(ImageFormat)
        
        self.mock_project_type = self.mocker.mock(Type)
        self.mock_project_type2 = self.mocker.mock(Type)
        
        self.mock_project_structure = self.mocker.mock(Structure)
        self.mock_project_structure2 = self.mocker.mock(Structure)
        
        self.mock_repo = self.mocker.mock(Repository)
        self.mock_repo2 = self.mocker.mock(Repository)
        
        self.mock_status_list = self.mocker.mock(StatusList)
        self.expect(self.mock_status_list.target_entity_type).\
            result(Project.entity_type).count(0, None)
        self.expect(len(self.mock_status_list.statuses)).result(5).count(0,None)
        
        # the tasks
        
        # for project
        self.mock_task1 = self.mocker.mock(Task)
        self.mock_task2 = self.mocker.mock(Task)
        self.mock_task3 = self.mocker.mock(Task)
        
        # for sequence4
        self.mock_task4 = self.mocker.mock(Task)
        self.mock_task5 = self.mocker.mock(Task)
        self.mock_task6 = self.mocker.mock(Task)
        
        # for sequence5
        self.mock_task7 = self.mocker.mock(Task)
        self.mock_task8 = self.mocker.mock(Task)
        self.mock_task9 = self.mocker.mock(Task)
        
        # for shot1 of seuqence6
        self.mock_task10 = self.mocker.mock(Task)
        self.mock_task11 = self.mocker.mock(Task)
        self.mock_task12 = self.mocker.mock(Task)
        
        # for shot2 of seuqence6
        self.mock_task13 = self.mocker.mock(Task)
        self.mock_task14 = self.mocker.mock(Task)
        self.mock_task15 = self.mocker.mock(Task)
        
        # for shot3 of seuqence7
        self.mock_task16 = self.mocker.mock(Task)
        self.mock_task17 = self.mocker.mock(Task)
        self.mock_task18 = self.mocker.mock(Task)
        
        # for shot4 of seuqence7
        self.mock_task19 = self.mocker.mock(Task)
        self.mock_task20 = self.mocker.mock(Task)
        self.mock_task21 = self.mocker.mock(Task)
        
        # for asset4
        self.mock_task22 = self.mocker.mock(Task)
        self.mock_task23 = self.mocker.mock(Task)
        self.mock_task24 = self.mocker.mock(Task)
        
        # for asset5
        self.mock_task25 = self.mocker.mock(Task)
        self.mock_task26 = self.mocker.mock(Task)
        self.mock_task27 = self.mocker.mock(Task)
        
        # the users
        self.expect(self.mock_task1.resources).\
            result([self.mock_user1]).count(0, None)
        self.expect(self.mock_task2.resources).\
            result([self.mock_user2]).count(0, None)
        self.expect(self.mock_task3.resources).\
            result([self.mock_user3]).count(0, None)
        self.expect(self.mock_task4.resources).\
            result([self.mock_user4]).count(0, None)
        self.expect(self.mock_task5.resources).\
            result([self.mock_user5]).count(0, None)
        self.expect(self.mock_task6.resources).\
            result([self.mock_user6]).count(0, None)
        self.expect(self.mock_task7.resources).\
            result([self.mock_user7]).count(0, None)
        self.expect(self.mock_task8.resources).\
            result([self.mock_user8]).count(0, None)
        self.expect(self.mock_task9.resources).\
            result([self.mock_user9]).count(0, None)
        self.expect(self.mock_task10.resources).\
            result([self.mock_user10]).count(0, None)
        self.expect(self.mock_task11.resources).\
            result([self.mock_user1, self.mock_user2]).count(0, None)
        self.expect(self.mock_task12.resources).\
            result([self.mock_user3, self.mock_user4]).count(0, None)
        self.expect(self.mock_task13.resources).\
            result([self.mock_user5, self.mock_user6]).count(0, None)
        self.expect(self.mock_task14.resources).\
            result([self.mock_user7, self.mock_user8]).count(0, None)
        self.expect(self.mock_task15.resources).\
            result([self.mock_user9, self.mock_user10]).count(0, None)
        self.expect(self.mock_task16.resources).\
            result([self.mock_user1, self.mock_user2, self.mock_user3]).\
                count(0, None)
        self.expect(self.mock_task17.resources).\
            result([self.mock_user4, self.mock_user5, self.mock_user6]).\
                count(0, None)
        self.expect(self.mock_task18.resources).\
            result([self.mock_user7, self.mock_user8, self.mock_user9]).\
                count(0, None)
        self.expect(self.mock_task19.resources).\
            result([self.mock_user10, self.mock_user1, self.mock_user2]).\
                count(0, None)
        self.expect(self.mock_task20.resources).\
            result([self.mock_user3, self.mock_user4, self.mock_user5]).\
                count(0, None)
        self.expect(self.mock_task21.resources).\
            result([self.mock_user6, self.mock_user7, self.mock_user8]).\
                count(0, None)
        self.expect(self.mock_task22.resources).\
            result([self.mock_user9, self.mock_user10, self.mock_user1]).\
                count(0, None)
        self.expect(self.mock_task23.resources).\
            result([self.mock_user2, self.mock_user3]).count(0, None)
        self.expect(self.mock_task24.resources).\
            result([self.mock_user4, self.mock_user5]).count(0, None)
        self.expect(self.mock_task25.resources).\
            result([self.mock_user6, self.mock_user7]).count(0, None)
        self.expect(self.mock_task26.resources).\
            result([self.mock_user8, self.mock_user9]).count(0, None)
        self.expect(self.mock_task27.resources).\
            result([self.mock_user10, self.mock_user1]).count(0, None)
        
        # assign tasks for seuqences
        self.expect(self.mock_seq4.tasks).\
            result([self.mock_task4, self.mock_task5, self.mock_task6]).\
                count(0, None)
        
        self.expect(self.mock_seq5.tasks).\
            result([self.mock_task7, self.mock_task8, self.mock_task9]).\
                count(0, None)
        
        # for sequences without shots but with tasks
        self.expect(self.mock_seq4.shots).result([]).count(0, None)
        self.expect(self.mock_seq5.shots).result([]).count(0, None)
        
        # for sequences with shots but without tasks
        self.expect(self.mock_seq6.tasks).result([]).count(0, None)
        self.expect(self.mock_seq7.tasks).result([]).count(0, None)
        
        # assign tasks for shots
        self.expect(self.mock_shot1.tasks).\
            result([self.mock_task10, self.mock_task11, self.mock_task12]).\
                count(0, None)
        
        self.expect(self.mock_shot2.tasks).\
            result([self.mock_task13, self.mock_task14, self.mock_task15]).\
                count(0, None)
        
        self.expect(self.mock_shot3.tasks).\
            result([self.mock_task16, self.mock_task17, self.mock_task18]).\
                count(0, None)
        
        self.expect(self.mock_shot4.tasks).\
            result([self.mock_task19, self.mock_task20, self.mock_task21]).\
                count(0, None)
        
        # assing tasks for assets
        self.expect(self.mock_asset4.tasks).\
            result([self.mock_task22, self.mock_task23, self.mock_task24]).\
                count(0, None)
        
        self.expect(self.mock_asset5.tasks).\
            result([self.mock_task25, self.mock_task26, self.mock_task27]).\
                count(0, None)
        
        # assign shots to sequences
        self.expect(self.mock_seq6.shots).\
            result([self.mock_shot1, self.mock_shot2]).\
                count(0, None)
        
        self.expect(self.mock_seq7.shots).\
            result([self.mock_shot3, self.mock_shot4]).\
                count(0, None)
        
        
        self.mocker.replay()
        
        # create a project object
        self.kwargs = {
            "name": "Test Project",
            "description": "This is a project object for testing purposes",
            "lead": self.mock_lead,
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
            "tasks": [self.mock_task1, self.mock_task2, self.mock_task3]
        }
        
        self.mock_project = Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_setup_is_working_correctly(self):
        """testing if the setup is done correctly
        """
        
        self.assertIsInstance(self.mock_project_type, Type)
        self.assertIsInstance(self.mock_project_type2, Type)
        
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_given_as_None(self):
        """testing if no error will be raised when the lead arguments is given
        as None
        """
        
        self.kwargs["lead"] = None
        new_project = Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_set_to_None(self):
        """testing if no error will be raised when the lead attribute is set to
        None
        """
        
        self.mock_project.lead = None
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_given_as_something_other_than_a_user(self):
        """testing if a TypeError will be raised when the lead argument is
        given as something other than a User object
        """
        
        test_values = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        
        for test_value in test_values:
            self.kwargs["lead"] = test_value
            self.assertRaises(
                TypeError,
                Project,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_set_to_something_other_than_a_user(self):
        """testing if a TypeError will be raised when the lead attribute is set
        to something other than a User object
        """
        
        test_values = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_project,
                "lead",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_works_properly(self):
        """testing if the lead attribute works properly
        """
        
        self.mock_project.lead = self.mock_user1
        self.assertEqual(self.mock_project.lead, self.mock_user1)
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_read_only(self):
        """testing if the users attribute is read-only
        """
        
        self.assertRaises(AttributeError, setattr, self.mock_project, "users",
                          [self.mock_user1, self.mock_user2, self.mock_user3])
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_calculated_from_project_tasks(self):
        """testing if the users attribute is calculated from the tasks of the
        project it self
        """
        
        self.kwargs["sequences"] = []
        self.kwargs["assets"] = []
        new_project = Project(**self.kwargs)
        
        # Users
        new_user1 = User(
            login_name="user1",
            email="user1@test.com",
            password="user1",
            first_name="user1",
            last_name="user1"
        )
        
        new_user2 = User(
            login_name="user2",
            email="user2@test.com",
            password="user2",
            first_name="user2",
            last_name="user2"
        )
        
        status_complete = Status(name="Complete", code="CMPLT")
        status_wip = Status(name="Work In Progress", code="WIP")
        
        task_status_list = StatusList(
            name="Task Status List",
            statuses=[status_complete, status_wip],
            target_entity_type=Task,
        )
        
        # create new tasks
        new_task1 = Task(
            name="Task1",
            status_list=task_status_list,
            project=new_project,
            task_of=new_project,
            resources= [new_user1],
        )
        
        new_task2 = Task(
            name="Task2",
            status_list=task_status_list,
            project=new_project,
            task_of=new_project,
            resources= [new_user1],
        )
        
        new_task3 = Task(
            name="Task3",
            status_list=task_status_list,
            project=new_project,
            task_of=new_project,
            resources= [new_user2],
        )
        
        # task1, task2, task3
        expected_users = [new_user1, new_user2]
        
        self.assertItemsEqual(new_project.users, expected_users)
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_calculated_from_sequence_tasks(self):
        """testing if the users attribute is calculated from the tasks of the
        sequences
        """
        
        self.kwargs["tasks"] = []
        self.kwargs["assets"] = []
        self.kwargs["sequences"] = [self.mock_seq4, self.mock_seq5]
        
        new_project = Project(**self.kwargs)
        
        # task4, task5, task6
        # task7, task8, task9
        
        expected_users = [self.mock_user4, self.mock_user5, self.mock_user6,
                          self.mock_user7, self.mock_user8, self.mock_user9]
        
        self.assertItemsEqual(new_project.users, expected_users)
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_calculated_from_asset_tasks(self):
        """testing if the users attribute is calculated from the tasks of the
        assets
        """
        
        self.kwargs["tasks"] = []
        self.kwargs["sequences"] = []
        self.kwargs["assets"] = [self.mock_asset4, self.mock_asset5]
        
        new_project = Project(**self.kwargs)
        
        # mock_task22, mock_task23, mock_task24
        # mock_task25, mock_task26, mock_task27
        
        expected_users = [self.mock_user1, self.mock_user2, self.mock_user3,
                          self.mock_user4, self.mock_user5, self.mock_user6,
                          self.mock_user7, self.mock_user8, self.mock_user9,
                          self.mock_user10]
        
        #print expected_users
        #print new_project.users
        self.assertItemsEqual(new_project.users, expected_users)
    
    
    
    #----------------------------------------------------------------------
    def test_users_attribute_is_calculated_from_sequence_shots(self):
        """testing if the users attribute is calculated from the tasks of the
        tasks of the sequence shots
        """
        
        self.kwargs["tasks"] = []
        self.kwargs["assets"] = []
        self.kwargs["sequences"] = [self.mock_seq6, self.mock_seq7]
        
        new_project = Project(**self.kwargs)
        
        # tasks
        # self.mock_task10, self.mock_task11, self.mock_task12
        # self.mock_task13, self.mock_task14, self.mock_task15
        # self.mock_task16, self.mock_task17, self.mock_task18
        # self.mock_task19, self.mock_task20, self.mock_task21
        
        expected_users = [self.mock_user1, self.mock_user2, self.mock_user3,
                          self.mock_user4, self.mock_user5, self.mock_user6,
                          self.mock_user7, self.mock_user8, self.mock_user9,
                          self.mock_user10]
        
        # users
        self.assertItemsEqual(new_project.users, expected_users)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_argument_is_given_as_None(self):
        """testing if sequence attribute is set to an empty list when the
        sequences argument is given as None
        """
        
        self.kwargs["sequences"] = None
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.sequences, [])
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_set_to_None_converted_to_empty_list(self):
        """testing if sequence attribute is set to an empty list when it is set
        to None
        """
        
        self.mock_project.sequences = None
        self.assertEqual(self.mock_project.sequences, [])
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_argument_is_given_as_an_empty_list(self):
        """testing if nothing happens when the sequences argument is given as
        an empty list
        """
        
        self.kwargs["sequences"] = []
        new_project = Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_set_to_an_empty_list(self):
        """testing if nothing happens when the seuqences attribute is set to an
        empty list
        """
        
        self.mock_project.sequences = []
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_argument_is_given_as_a_list_containing_non_Sequence_objects(self):
        """testing if a TypeError will be raised when trying the given
        sequences argument is a list containing objects other than Sequence
        instances
        """
        
        test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        self.kwargs["sequences"] = test_value
        self.assertRaises(TypeError, Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_set_to_a_list_containing_non_Sequence_objects(self):
        """testing if a TypeError will be raised when trying to set the
        sequences list to a list containing objects other than Sequence
        instances
        """
        
        test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        self.assertRaises(
            TypeError,
            setattr,
            self.mock_project,
            "sequences",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_argument_is_given_as_non_Sequence_object(self):
        """testing if a TypeError will be raised when trying the given
        sequences argument is an object other than Sequence instance
        """
        
        test_values = [1, 1.2, "a user"]
        
        for test_value in test_values:
            self.kwargs["sequences"] = test_value
            self.assertRaises(TypeError, Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_attribute_is_set_to_a_list_containing_non_Sequence_objects(self):
        """testing if a TypeError will be raised when trying to set the
        sequences list to a list containing objects other than Sequence
        instances
        """
        
        test_values = [1, 1.2, "a user"]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
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
        """testing if a TypeError will be raised when trying to assign
        something other than a Sequence object to the sequences list
        """
        
        # append
        self.assertRaises(
            TypeError,
            self.mock_project.sequences.append,
            0
        )
        
        # __setitem__
        self.assertRaises(
            TypeError,
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
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.assets, [])
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_None_converted_to_empty_list(self):
        """testing if assets attribute is set to an empty list when it is set
        to None
        """
        
        self.mock_project.assets = None
        self.assertEqual(self.mock_project.assets, [])
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_skipped_and_intializied_as_an_empty_list(self):
        """testing if skipping the assets list argument will initialize the
        assets attribute to an empty list
        """
        
        self.kwargs.pop("assets")
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.assets, [])
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_given_as_an_empty_list(self):
        """testing if nothing happens when the assets argument is given as
        an empty list
        """
        
        self.kwargs["assets"] = []
        new_project = Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_an_empty_list(self):
        """testing if nothing happens when the assets attribute is set to an
        empty list
        """
        
        self.mock_project.assets = []
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_a_list_containing_non_Asset_objects(self):
        """testing if a TypeError will be raised when the assets argument is
        given as a list containing objects other than Assets instances
        """
        
        test_value = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        self.kwargs["assets"] = test_value
        self.assertRaises(TypeError, Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_a_list_containing_non_Asset_objects(self):
        """testing if a TypeError will be raised when trying to set the assets
        list to a list containing objects other than Assets instances
        """
        
        test_value = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        
        self.assertRaises(
            TypeError,
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
        """testing if a TypeError will be raised when trying to assign
        something other than a Asset instance to the assets list
        """
        
        # append
        self.assertRaises(
            TypeError,
            self.mock_project.assets.append,
            0
        )
        
        # __setitem__
        self.assertRaises(
            TypeError,
            self.mock_project.assets.__setitem__,
            0,
            0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_not_iterable(self):
        """testing if a TypeError will be raised when the assets argument is
        not iterable
        """
        
        test_values = [1, 1.2, "an asset"]
        
        for test_value in test_values:
            self.kwargs["assets"] = test_value
            self.assertRaises(TypeError, Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_not_iterable(self):
        """testing if a TypeError will be raised when a non-iterable value is
        tried to be assigned to the assets attribute
        """
        
        test_values = [1, 1.2, "an asset"]
        
        for test_value in test_values:
            self.assertRaises(TypeError, setattr, self.mock_project, "assets",
                              test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_argument_is_None(self):
        """testing if nothing is going to happen when the image_format is set
        to None
        """
        
        self.kwargs["image_format"] = None
        new_project = Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_attribute_is_set_to_None(self):
        """testing if nothing will happen when the image_format attribute is
        set to None
        """
        
        self.mock_project.image_format = None
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_argument_accepts_ImageFormat_only(self):
        """testing if a TypeError will be raised when the image_format
        argument is given as another type then ImageFormat
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        
        for test_value in test_values:
            self.kwargs["image_format"] = test_value
            self.assertRaises(TypeError, Project, **self.kwargs)
        
        # and a proper image format
        self.kwargs["image_format"] = self.mock_imageFormat
        new_project = Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_attribute_accepts_ImageFormat_only(self):
        """testing if a TypeError will be raised when the image_format
        attribute is tried to be set to something other than a ImageFormat
        instance
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_project,
                "image_format",
                test_value
            )
        
        # and a proper image format
        self.mock_project.image_format = self.mock_imageFormat
    
    
    
    #----------------------------------------------------------------------
    def test_image_format_attribute_works_properly(self):
        """testing if the image_format attribute is working properly
        """
        
        new_image_format = ImageFormat(
            name="Foo Image Format",
            width=10,
            height=10
        )
        
        self.mock_project.image_format = new_image_format
        self.assertEqual(self.mock_project.image_format, new_image_format)
    
    
    
    #----------------------------------------------------------------------
    def test_fps_argument_is_skipped(self):
        """testing if the default value will be used when fps is skipped
        """
        
        self.kwargs.pop("fps")
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.fps, 25.0)
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the fps attribute is set
        to None
        """
        
        self.kwargs["fps"] = None
        self.assertRaises(TypeError, Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_fps_argument_is_given_as_non_float_or_integer(self):
        """testing if a TypeError will be raised when the fps argument is
        given as a value other than a float or integer, or a string which is
        convertable to float.
        """
        
        test_values = ["a str"]
        for test_value in test_values:
            self.kwargs["fps"] = test_value
            self.assertRaises(
                ValueError,
                Project,
                **self.kwargs
            )
        
        test_values = [["a", "list"], {"a": "list"}]
        for test_value in test_values:
            self.kwargs["fps"] = test_value
            self.assertRaises(
                TypeError,
                Project,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_is_given_as_non_float_or_integer(self):
        """testing if a TypeError will be raised when the fps attribute is
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
            new_project = Project(**self.kwargs)
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
        new_project = Project(**self.kwargs)
        self.assertIsInstance(new_project.fps, float)
        self.assertEqual(new_project.fps, float(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_fps_attribute_float_conversion_2(self):
        """testing if the fps attribute is converted to float when it is set to
        an integer value
        """
        
        test_value = 1
        
        self.mock_project.fps = test_value
        self.assertIsInstance(self.mock_project.fps, float)
        self.assertEqual(self.mock_project.fps, float(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_repository_argument_is_None(self):
        """testing if nothing happens when repository is set to None
        """
        
        self.kwargs["repository"] = None
        new_project = Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_repository_attribute_is_set_to_None(self):
        """testing if nothing happens when setting the repository attribute to
        None
        """
        
        self.mock_project.repository = None
    
    
    
    #----------------------------------------------------------------------
    def test_repository_argument_is_non_Repository_object(self):
        """testing if a TypeError will be raised when the repository argument
        is given as something other than a Repository object
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        for test_value in test_values:
            self.kwargs["repository"] = test_value
            self.assertRaises(TypeError, Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_repository_attribute_is_set_to_non_Repository_object(self):
        """testing if a TypeErorr will be raised when the repository attribute
        is tried to be set to something other than a Repository object
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_project,
                "repository",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_repository_attribute_is_working_properly(self):
        """testin if the repository attribute is working properly
        """
        
        self.mock_project.repository = self.mock_repo2
        self.assertEqual(self.mock_project.repository, self.mock_repo2)
    
    
    
    #----------------------------------------------------------------------
    def test_is_stereoscopic_argument_skipped(self):
        """testing if is_stereoscopic will set the is_stereoscopic attribute to
        False
        """
        
        self.kwargs.pop("is_stereoscopic")
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.is_stereoscopic, False)
    
    
    
    #----------------------------------------------------------------------
    def test_is_stereoscopic_argument_bool_conversion(self):
        """testing if all the given values for is_stereoscopic argument will be
        converted to a bool value correctly
        """
        
        test_values = [0, 1, 1.2, "", "str", ["a", "list"]]
        
        for test_value in test_values:
            self.kwargs["is_stereoscopic"] = test_value
            new_project = Project(**self.kwargs)
            self.assertEqual(new_project.is_stereoscopic, bool(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_is_stereoscopic_attribute_bool_conversion(self):
        """testing if all the given values for is_stereoscopic attribute will
        be converted to a bool value correctly
        """
        
        test_values = [0, 1, 1.2, "", "str", ["a", "list"]]
        
        for test_value in test_values:
            self.mock_project.is_stereoscopic = test_value
            self.assertEqual(
                self.mock_project.is_stereoscopic,
                bool(test_value)
            )
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_argument_is_skipped(self):
        """testing if the display_width attribute will be set to the default
        value when the display_width argument is skipped
        """
        
        self.kwargs.pop("display_width")
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.display_width, 1.0)
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_argument_float_conversion(self):
        """testing if the display_width attribute is converted to float
        correctly for various display_width arguments
        """
        
        test_values = [1, 2, 3, 4]
        for test_value in test_values:
            self.kwargs["display_width"] = test_value
            new_project = Project(**self.kwargs)
            self.assertIsInstance(new_project.display_width, float)
            self.assertEqual(new_project.display_width, float(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_attribute_float_conversion(self):
        """testing if the display_width attribute is converted to float
        correctly
        """
        
        test_values = [1, 2, 3, 4]
        for test_value in test_values:
            self.mock_project.display_width = test_value
            self.assertIsInstance(self.mock_project.display_width, float)
            self.assertEqual(self.mock_project.display_width,
                              float(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_argument_is_given_as_a_negative_value(self):
        """testing if the display_width attribute is set to the absolute value
        of the given negative display_width argument
        """
        
        test_value = -1.0
        self.kwargs["display_width"] = test_value
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.display_width, abs(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_display_width_attribute_is_set_to_a_negative_value(self):
        """testing if the display_width attribute is set to default value when
        it is set to a negative value
        """
        
        test_value = -1.0
        self.mock_project.display_width = test_value
        self.assertEqual(self.mock_project.display_width, abs(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_structure_argument_is_None(self):
        """testing if nothing happens when the structure argument is None
        """
        
        self.kwargs["structure"] = None
        new_project = Project(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_structure_attirbute_is_None(self):
        """testing if nothing happends when the structure attribute is set to
        None
        """
        
        self.mock_project.structure = None
    
    
    
    #----------------------------------------------------------------------
    def test_structure_argument_not_instance_of_Structure(self):
        """testing if a TypeError will be raised when the structure argument
        is not an instance of Structure
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"]]
        
        for test_value in test_values:
            self.kwargs["structure"] = test_value
            self.assertRaises(TypeError, Project, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_structure_attribute_not_instance_of_Structure(self):
        """testing if a TypeError will be raised when the structure attribute
        is not an instance of Structure
        """
        
        test_values = [1, 1.2, "a str", ["a", "list"]]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_project,
                "structure",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_structure_attribute_is_working_properly(self):
        """testing if the structure attribute is working properly
        """
        
        self.mock_project.structure = self.mock_project_structure2
        self.assertEqual(self.mock_project.structure,
                          self.mock_project_structure2)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality of two projects
        """
        
        # create a new project with the same arguments
        new_project1 = Project(**self.kwargs)
        
        # create a new entity with the same arguments
        new_entity = Entity(**self.kwargs)
        
        # create another project with different name
        self.kwargs["name"] = "a different project"
        new_project2 = Project(**self.kwargs)
        
        self.assertTrue(self.mock_project==new_project1)
        self.assertFalse(self.mock_project==new_project2)
        self.assertFalse(self.mock_project==new_entity)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality of two projects
        """
        
        # create a new project with the same arguments
        new_project1 = Project(**self.kwargs)
        
        # create a new entity with the same arguments
        new_entity = Entity(**self.kwargs)
        
        # create another project with different name
        self.kwargs["name"] = "a different project"
        new_project2 = Project(**self.kwargs)
        
        self.assertFalse(self.mock_project!=new_project1)
        self.assertTrue(self.mock_project!=new_project2)
        self.assertTrue(self.mock_project!=new_entity)
    
    
    
    #----------------------------------------------------------------------
    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """
        
        link_type_1 = Type(name="Image", target_entity_type="Link")
        
        link1 = Link(name="Artwork 1", path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="a.jpg", type=link_type_1)
        
        link2 = Link(name="Artwork 2", path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="b.jbg", type=link_type_1)
        
        references = [link1, link2]
        
        self.kwargs["references"] = references
        
        new_project = Project(**self.kwargs)
        
        self.assertEqual(new_project.references, references)
    
    
    
    #----------------------------------------------------------------------
    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """
        
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Complete", code="CMPLT")
        
        status_list = StatusList(name="Project Statuses",
                                 statuses=[status1, status2],
                                 target_entity_type=Project.entity_type)
        
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list
        
        new_project = Project(**self.kwargs)
        
        self.assertEqual(new_project.status_list, status_list)
    
    
    
    #----------------------------------------------------------------------
    def test_ScheduleMixin_initialization(self):
        """testing if the ScheduleMixin part is initialized correctly
        """
        
        start_date = datetime.date.today() + datetime.timedelta(days=25)
        due_date = start_date + datetime.timedelta(days=12)
        
        self.kwargs["start_date"] = start_date
        self.kwargs["due_date"] = due_date
        
        new_project = Project(**self.kwargs)
        
        self.assertEqual(new_project.start_date, start_date)
        self.assertEqual(new_project.due_date, due_date)
        self.assertEqual(new_project.duration, due_date - start_date)
    
    
    
    #----------------------------------------------------------------------
    def test_TaskMixin_initialization(self):
        """testing if the TaskMixin part is initialized correctly
        """
        
        status1 = Status(name="On Hold", code="OH")
        
        project_status_list = StatusList(
            name="Project Status List",
            statuses=[status1],
            target_entity_type=Project
        )
        
        commercial_project_type = Type(
            name="Commercial Project",
            target_entity_type=Project,
        )
        
        new_project = Project(
            name="Test Project",
            type=commercial_project_type,
            status_list=project_status_list
        )
        
        
        task_status_list = StatusList(
            name="Task Statuses",
            statuses=[status1],
            target_entity_type=Task
        )
        
        new_task1 = Task(
            name="Test Task",
            status_list=task_status_list,
            task_of=new_project,
        )
        
        
        self.assertItemsEqual(new_project.tasks, [new_task1])
        self.assertEqual(new_project.project, new_project)
    
    
    
    #----------------------------------------------------------------------
    def test_plural_name(self):
        """testing the plural name of Project class
        """
        
        self.assertTrue(Project.plural_name, "Projects")
    
    
    
    #----------------------------------------------------------------------
    def test___strictly_typed___is_True(self):
        """testing if the __strictly_typed__ is True for Project class
        """
        
        self.assertEqual(Project.__strictly_typed__, True)
        