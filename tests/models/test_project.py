# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime
import unittest

from stalker import (Asset, Entity, ImageFormat, Link, Project, Repository,
                     Sequence, Shot, Status, StatusList, Structure, Task, Type,
                     User, db)
from stalker.db.session import DBSession, ZopeTransactionExtension

import logging
from stalker import log
logger = logging.getLogger('stalker.models.project')
logger.setLevel(log.logging_level)

class ProjectTester(unittest.TestCase):
    """tests the Project class
    """
    
    @classmethod
    def setUpClass(cls):
        """set up the test for class
        """
        DBSession.remove()
        DBSession.configure(extension=None)
    
    @classmethod
    def tearDownClass(cls):
        """clean up the test
        """
        DBSession.configure(extension=ZopeTransactionExtension())
    
    def tearDown(self):
        """tearDown the tests
        """
        DBSession.remove()
    
    def setUp(self):
        """setup the test
        """

        DBSession.remove()
        DBSession.configure(extension=None)
        self.TEST_DATABASE_URI = "sqlite:///:memory:"
        
        db.setup({
            "sqlalchemy.url": self.TEST_DATABASE_URI,
            "sqlalchemy.echo": False,
        })
        
        # create test objects
        self.start_date = datetime.date.today()
        self.end_date = self.start_date + datetime.timedelta(days=20)

        self.test_lead = User(
            name="lead",
            login="lead",
            email="lead@lead.com",
            password="lead"
        )

        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@users.com",
            password="123456"
        )

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@users.com",
            password="123456"
        )

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@users.com",
            password="123456"
        )

        self.test_user4 = User(
            name="User4",
            login="user4",
            email="user4@users.com",
            password="123456"
        )

        self.test_user5 = User(
            name="User5",
            login="user5",
            email="user5@users.com",
            password="123456"
        )

        self.test_user6 = User(
            name="User6",
            login="user6",
            email="user6@users.com",
            password="123456"
        )

        self.test_user7 = User(
            name="User7",
            login="user7",
            email="user7@users.com",
            password="123456"
        )

        self.test_user8 = User(
            name="User8",
            login="user8",
            email="user8@users.com",
            password="123456"
        )

        self.test_user9 = User(
            name="user9",
            login="user9",
            email="user9@users.com",
            password="123456"
        )

        self.test_user10 = User(
            name="User10",
            login="user10",
            email="user10@users.com",
            password="123456"
        )

        # statuses
        self.test_status1 = Status(name="Status1", code="S1")
        self.test_status2 = Status(name="Status2", code="S2")
        self.test_status3 = Status(name="Status3", code="S3")
        self.test_status4 = Status(name="Status4", code="S4")
        self.test_status5 = Status(name="Status5", code="S5")

        # status list for project
        self.project_status_list = StatusList(
            name="Project Statuses",
            target_entity_type=Project,
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
        )

        self.test_imageFormat = ImageFormat(
            name="HD",
            width=1920,
            height=1080,
        )

        # type for project
        self.test_project_type = Type(
            name="Project Type 1",
            code='projt1',
            target_entity_type=Project
        )

        self.test_project_type2 = Type(
            name="Project Type 2",
            code='projt2',
            target_entity_type=Project
        )

        # type for structure
        self.test_structure_type1 = Type(
            name="Structure Type 1",
            code='struct1',
            target_entity_type=Structure
        )

        self.test_structure_type2 = Type(
            name="Structure Type 2",
            code='struct2',
            target_entity_type=Structure
        )

        self.test_project_structure = Structure(
            name="Project Structure 1",
            type=self.test_structure_type1,
        )

        self.test_project_structure2 = Structure(
            name="Project Structure 2",
            type=self.test_structure_type2,
        )

        self.test_repo = Repository(
            name="Commercials Repository",
        )

        # create a project object
        self.kwargs = {
            "name": "Test Project",
            'code': 'tp',
            "description": "This is a project object for testing purposes",
            "lead": self.test_lead,
            "image_format": self.test_imageFormat,
            "fps": 25,
            "type": self.test_project_type,
            "structure": self.test_project_structure,
            "repository": self.test_repo,
            "is_stereoscopic": False,
            "display_width": 15,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status_list": self.project_status_list,
            #"tasks": [self.test_task1, self.test_task2, self.test_task3]
        }

        self.test_project = Project(**self.kwargs)

        # status list for sequence
        self.sequence_status_list = StatusList(
            name="Sequence Statuses",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
                ],
            target_entity_type=Sequence
        )

        # sequences without tasks
        self.test_seq1 = Sequence(
            name="Seq1",
            code='Seq1',
            project=self.test_project,
            status_list=self.sequence_status_list,
        )

        self.test_seq2 = Sequence(
            name="Seq2",
            code='Seq2',
            project=self.test_project,
            status_list=self.sequence_status_list,
        )

        self.test_seq3 = Sequence(
            name="Seq3",
            code='Seq3',
            project=self.test_project,
            status_list=self.sequence_status_list,
        )

        # sequences with tasks
        self.test_seq4 = Sequence(
            name="Seq4",
            code='Seq4',
            project=self.test_project,
            status_list=self.sequence_status_list,
        )

        self.test_seq5 = Sequence(
            name="Seq5",
            code='Seq5',
            project=self.test_project,
            status_list=self.sequence_status_list,
        )

        # sequences without tasks but with shots
        self.test_seq6 = Sequence(
            name="Seq6",
            code='Seq6',
            project=self.test_project,
            status_list=self.sequence_status_list,
        )

        self.test_seq7 = Sequence(
            name="Seq7",
            code='Seq7',
            project=self.test_project,
            status_list=self.sequence_status_list,
        )

        # shot status list
        self.shot_status_list = StatusList(
            name="Shot Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
                ],
            target_entity_type=Shot,
        )

        # shots
        self.test_shot1 = Shot(
            code="SH001",
            sequence=self.test_seq6,
            status_list=self.shot_status_list,
        )

        self.test_shot2 = Shot(
            code="SH002",
            sequence=self.test_seq6,
            status_list=self.shot_status_list,
        )

        self.test_shot3 = Shot(
            code="SH003",
            sequence=self.test_seq7,
            status_list=self.shot_status_list,
        )

        self.test_shot4 = Shot(
            code="SH004",
            sequence=self.test_seq7,
            status_list=self.shot_status_list,
        )

        # asset status list
        self.asset_status_list = StatusList(
            name="Asset Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
                ],
            target_entity_type=Asset,
        )

        # asset types
        self.asset_type = Type(
            name="Character",
            code='char',
            target_entity_type=Asset,
        )

        # assets without tasks
        self.test_asset1 = Asset(
            name="Test Asset 1",
            code='ta1',
            type=self.asset_type,
            project=self.test_project,
            status_list=self.asset_status_list,
        )

        self.test_asset2 = Asset(
            name="Test Asset 2",
            code='ta2',
            type=self.asset_type,
            project=self.test_project,
            status_list=self.asset_status_list,
        )

        self.test_asset3 = Asset(
            name="Test Asset 3",
            code='ta3',
            type=self.asset_type,
            project=self.test_project,
            status_list=self.asset_status_list,
        )

        # assets with tasks
        self.test_asset4 = Asset(
            name="Test Asset 4",
            code='ta4',
            type=self.asset_type,
            project=self.test_project,
            status_list=self.asset_status_list,
        )

        self.test_asset5 = Asset(
            name="Test Asset 5",
            code='ta5',
            type=self.asset_type,
            project=self.test_project,
            status_list=self.asset_status_list,
        )

        # task status list
        self.task_status_list = StatusList(
            name="Task Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Task,
        )

        # the tasks

        # for project
        self.test_task1 = Task(
            name="Test Task 1",
            task_of=self.test_project,
            resources=[self.test_user1],
            status_list=self.task_status_list,
        )

        self.test_task2 = Task(
            name="Test Task 2",
            task_of=self.test_project,
            resources=[self.test_user2],
            status_list=self.task_status_list,
            )

        self.test_task3 = Task(
            name="Test Task 3",
            task_of=self.test_project,
            resources=[self.test_user3],
            status_list=self.task_status_list,
        )

        # for sequence4
        self.test_task4 = Task(
            name="Test Task 4",
            task_of=self.test_seq4,
            resources=[self.test_user4],
            status_list=self.task_status_list,
        )

        self.test_task5 = Task(
            name="Test Task 5",
            task_of=self.test_seq4,
            resources=[self.test_user5],
            status_list=self.task_status_list,
        )

        self.test_task6 = Task(
            name="Test Task 6",
            task_of=self.test_seq4,
            resources=[self.test_user6],
            status_list=self.task_status_list,
        )

        # for sequence5
        self.test_task7 = Task(
            name="Test Task 7",
            task_of=self.test_seq5,
            resources=[self.test_user7],
            status_list=self.task_status_list,
        )

        self.test_task8 = Task(
            name="Test Task 8",
            task_of=self.test_seq5,
            resources=[self.test_user8],
            status_list=self.task_status_list,
        )

        self.test_task9 = Task(
            name="Test Task 9",
            task_of=self.test_seq5,
            resources=[self.test_user9],
            status_list=self.task_status_list,
        )

        # for shot1 of seuqence6
        self.test_task10 = Task(
            name="Test Task 10",
            task_of=self.test_shot1,
            resources=[self.test_user10],
            status_list=self.task_status_list,
        )

        self.test_task11 = Task(
            name="Test Task 11",
            task_of=self.test_shot1,
            resources=[self.test_user1, self.test_user2],
            status_list=self.task_status_list,
        )

        self.test_task12 = Task(
            name="Test Task 12",
            task_of=self.test_shot1,
            resources=[self.test_user3, self.test_user4],
            status_list=self.task_status_list,
        )

        # for shot2 of seuqence6
        self.test_task13 = Task(
            name="Test Task 13",
            task_of=self.test_shot2,
            resources=[self.test_user5, self.test_user6],
            status_list=self.task_status_list,
        )

        self.test_task14 = Task(
            name="Test Task 14",
            task_of=self.test_shot2,
            resources=[self.test_user7, self.test_user8],
            status_list=self.task_status_list,
        )

        self.test_task15 = Task(
            name="Test Task 15",
            task_of=self.test_shot2,
            resources=[self.test_user9, self.test_user10],
            status_list=self.task_status_list,
            )

        # for shot3 of seuqence7
        self.test_task16 = Task(
            name="Test Task 16",
            task_of=self.test_shot3,
            resources=[self.test_user1, self.test_user2, self.test_user3],
            status_list=self.task_status_list,
        )

        self.test_task17 = Task(
            name="Test Task 17",
            task_of=self.test_shot3,
            resources=[self.test_user4, self.test_user5, self.test_user6],
            status_list=self.task_status_list,
        )

        self.test_task18 = Task(
            name="Test Task 18",
            task_of=self.test_shot3,
            resources=[self.test_user7, self.test_user8, self.test_user9],
            status_list=self.task_status_list,
        )

        # for shot4 of seuqence7
        self.test_task19 = Task(
            name="Test Task 19",
            task_of=self.test_shot4,
            resources=[self.test_user10, self.test_user1, self.test_user2],
            status_list=self.task_status_list,
        )

        self.test_task20 = Task(
            name="Test Task 20",
            task_of=self.test_shot4,
            resources=[self.test_user3, self.test_user4, self.test_user5],
            status_list=self.task_status_list,
        )

        self.test_task21 = Task(
            name="Test Task 21",
            task_of=self.test_shot4,
            resources=[self.test_user6, self.test_user7, self.test_user8],
            status_list=self.task_status_list,
        )

        # for asset4
        self.test_task22 = Task(
            name="Test Task 22",
            task_of=self.test_asset4,
            resources=[self.test_user9, self.test_user10, self.test_user1],
            status_list=self.task_status_list,
        )

        self.test_task23 = Task(
            name="Test Task 23",
            task_of=self.test_asset4,
            resources=[self.test_user2, self.test_user3],
            status_list=self.task_status_list,
        )

        self.test_task24 = Task(
            name="Test Task 24",
            task_of=self.test_asset4,
            resources=[self.test_user4, self.test_user5],
            status_list=self.task_status_list,
        )

        # for asset5
        self.test_task25 = Task(
            name="Test Task 25",
            task_of=self.test_asset5,
            resources=[self.test_user6, self.test_user7],
            status_list=self.task_status_list,
        )

        self.test_task26 = Task(
            name="Test Task 26",
            task_of=self.test_asset5,
            resources=[self.test_user8, self.test_user9],
            status_list=self.task_status_list,
        )

        self.test_task27 = Task(
            name="Test Task 27",
            task_of=self.test_asset5,
            resources=[self.test_user10, self.test_user1],
            status_list=self.task_status_list,
        )
    
        DBSession.add(self.test_project)
        DBSession.commit()
    
    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Project class
        """
        self.assertFalse(Project.__auto_name__)
    
    def test_setup_is_working_correctly(self):
        """testing if the setup is done correctly
        """
        self.assertIsInstance(self.test_project_type, Type)
        self.assertIsInstance(self.test_project_type2, Type)

    def test_lead_argument_is_given_as_None(self):
        """testing if no error will be raised when the lead arguments is given
        as None
        """
        self.kwargs["lead"] = None
        new_project = Project(**self.kwargs)

    def test_lead_attribute_is_set_to_None(self):
        """testing if no error will be raised when the lead attribute is set to
        None
        """
        self.test_project.lead = None

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

    def test_lead_attribute_is_set_to_something_other_than_a_user(self):
        """testing if a TypeError will be raised when the lead attribute is set
        to something other than a User object
        """
        test_values = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_project,
                "lead",
                test_value
            )

    def test_lead_attribute_works_properly(self):
        """testing if the lead attribute works properly
        """
        self.test_project.lead = self.test_user1
        self.assertEqual(self.test_project.lead, self.test_user1)

    def test_users_attribute_is_read_only(self):
        """testing if the users attribute is read-only
        """
        self.assertRaises(AttributeError, setattr, self.test_project, "users",
            [self.test_user1, self.test_user2, self.test_user3])

        # UPDATE THIS: This test needs to be in the tests.db
        # because the property it is testing is using DBSession.query
        #
        #def test_users_attribute_is_calculated_from_project_tasks(self):
        #"""testing if the users attribute is calculated from the tasks of the
        #project it self
        #"""

        #self.kwargs["sequences"] = []
        #self.kwargs["assets"] = []
        #new_project = Project(**self.kwargs)

        ## Users
        #new_user1 = User(
        #login_name="user1",
        #email="user1@test.com",
        #password="user1",
        #first_name="user1",
        #last_name="user1"
        #)

        #new_user2 = User(
        #login_name="user2",
        #email="user2@test.com",
        #password="user2",
        #first_name="user2",
        #last_name="user2"
        #)

        #status_complete = Status(name="Complete", code="CMPLT")
        #status_wip = Status(name="Work In Progress", code="WIP")

        #task_status_list = StatusList(
        #name="Task Status List",
        #statuses=[status_complete, status_wip],
        #target_entity_type=Task,
        #)

        ## create new tasks
        #new_task1 = Task(
        #name="Task1",
        #status_list=task_status_list,
        #project=new_project,
        #task_of=new_project,
        #resources= [new_user1],
        #)

        #new_task2 = Task(
        #name="Task2",
        #status_list=task_status_list,
        #project=new_project,
        #task_of=new_project,
        #resources= [new_user1],
        #)

        #new_task3 = Task(
        #name="Task3",
        #status_list=task_status_list,
        #project=new_project,
        #task_of=new_project,
        #resources= [new_user2],
        #)

        ## task1, task2, task3
        #expected_users = [new_user1, new_user2]

        #self.assertItemsEqual(new_project.users, expected_users)



        # UPDATE THIS: This test needs to be in the tests.db
        # because the property it is testing is using DBSession.query
        #
        #def test_users_attribute_is_calculated_from_sequence_tasks(self):
        #"""testing if the users attribute is calculated from the tasks of the
        #sequences
        #"""

        #self.kwargs["tasks"] = []
        ##self.kwargs["assets"] = []
        ##self.kwargs["sequences"] = [self.test_seq4, self.test_seq5]

        #new_project = Project(**self.kwargs)


        ## sequences with tasks
        #self.test_seq4 = Sequence(
        #name="Seq4",
        #project=new_project,
        #status_list=self.sequence_status_list,
        #)

        #self.test_seq5 = Sequence(
        #name="Seq5",
        #project=new_project,
        #status_list=self.sequence_status_list,
        #)


        ## for sequence4
        #self.test_task4 = Task(
        #name="Test Task 4",
        #task_of=self.test_seq4,
        #resources=[self.test_user4],
        #status_list=self.task_status_list,
        #)

        #self.test_task5 = Task(
        #name="Test Task 5",
        #task_of=self.test_seq4,
        #resources=[self.test_user5],
        #status_list=self.task_status_list,
        #)

        #self.test_task6 = Task(
        #name="Test Task 6",
        #task_of=self.test_seq4,
        #resources=[self.test_user6],
        #status_list=self.task_status_list,
        #)

        ## for sequence5
        #self.test_task7 = Task(
        #name="Test Task 7",
        #task_of=self.test_seq5,
        #resources=[self.test_user7],
        #status_list=self.task_status_list,
        #)

        #self.test_task8 = Task(
        #name="Test Task 8",
        #task_of=self.test_seq5,
        #resources=[self.test_user8],
        #status_list=self.task_status_list,
        #)

        #self.test_task9 = Task(
        #name="Test Task 9",
        #task_of=self.test_seq5,
        #resources=[self.test_user9],
        #status_list=self.task_status_list,
        #)


        ## task4, task5, task6
        ## task7, task8, task9

        #expected_users = [self.test_user4, self.test_user5, self.test_user6,
        #self.test_user7, self.test_user8, self.test_user9]

        #self.assertItemsEqual(new_project.users, expected_users)



        # UPDATE THIS: this test should be in tests.db
        # because the property it is testing is using DBSession.query
        #
        #def test_users_attribute_is_calculated_from_asset_tasks(self):
        #"""testing if the users attribute is calculated from the tasks of the
        #assets
        #"""

        #self.kwargs["tasks"] = []
        ##self.kwargs["sequences"] = []
        ##self.kwargs["assets"] = [self.test_asset4, self.test_asset5]

        #new_project = Project(**self.kwargs)


        ## assets with tasks
        #self.test_asset4 = Asset(
        #name="Test Asset 4",
        #type=self.asset_type,
        #project=new_project,
        #status_list=self.asset_status_list,
        #)

        #self.test_asset5 = Asset(
        #name="Test Asset 5",
        #type=self.asset_type,
        #project=new_project,
        #status_list=self.asset_status_list,
        #)


        ## for asset4
        #self.test_task22 = Task(
        #name="Test Task 22",
        #task_of=self.test_asset4,
        #resources=[self.test_user9, self.test_user10, self.test_user1],
        #status_list=self.task_status_list,
        #)

        #self.test_task23 = Task(
        #name="Test Task 23",
        #task_of=self.test_asset4,
        #resources=[self.test_user2, self.test_user3],
        #status_list=self.task_status_list,
        #)

        #self.test_task24 = Task(
        #name="Test Task 24",
        #task_of=self.test_asset4,
        #resources=[self.test_user4, self.test_user5],
        #status_list=self.task_status_list,
        #)

        ## for asset5
        #self.test_task25 = Task(
        #name="Test Task 25",
        #task_of=self.test_asset5,
        #resources=[self.test_user6, self.test_user7],
        #status_list=self.task_status_list,
        #)

        #self.test_task26 = Task(
        #name="Test Task 26",
        #task_of=self.test_asset5,
        #resources=[self.test_user8, self.test_user9],
        #status_list=self.task_status_list,
        #)

        #self.test_task27 = Task(
        #name="Test Task 27",
        #task_of=self.test_asset5,
        #resources=[self.test_user10, self.test_user1],
        #status_list=self.task_status_list,
        #)

        #expected_users = [self.test_user1, self.test_user2, self.test_user3,
        #self.test_user4, self.test_user5, self.test_user6,
        #self.test_user7, self.test_user8, self.test_user9,
        #self.test_user10]

        #self.assertItemsEqual(new_project.users, expected_users)


        # UPDATE THIS: This test needs to be in tests.db
        # because the property it is testing is using DBSession.query
        #
        #def test_users_attribute_is_calculated_from_sequence_shots(self):
        #"""testing if the users attribute is calculated from the tasks of the
        #tasks of the sequence shots
        #"""

        #self.kwargs["tasks"] = []
        ##self.kwargs["assets"] = []
        ##self.kwargs["sequences"] = [self.test_seq6, self.test_seq7]

        #new_project = Project(**self.kwargs)

        ## sequences without tasks but with shots
        #self.test_seq6 = Sequence(
        #name="Seq6",
        #project=new_project,
        #status_list=self.sequence_status_list,
        #)

        #self.test_seq7 = Sequence(
        #name="Seq7",
        #project=new_project,
        #status_list=self.sequence_status_list,
        #)

        ## shots
        #self.test_shot1 = Shot(
        #code="SH001",
        #sequence=self.test_seq6,
        #status_list=self.shot_status_list,
        #)

        #self.test_shot2 = Shot(
        #code="SH002",
        #sequence=self.test_seq6,
        #status_list=self.shot_status_list,
        #)

        #self.test_shot3 = Shot(
        #code="SH003",
        #sequence=self.test_seq7,
        #status_list=self.shot_status_list,
        #)

        #self.test_shot4 = Shot(
        #code="SH004",
        #sequence=self.test_seq7,
        #status_list=self.shot_status_list,
        #)


        ## for shot1 of seuqence6
        #self.test_task10 = Task(
        #name="Test Task 10",
        #task_of=self.test_shot1,
        #resources=[self.test_user10],
        #status_list=self.task_status_list,
        #)

        #self.test_task11 = Task(
        #name="Test Task 11",
        #task_of=self.test_shot1,
        #resources=[self.test_user1, self.test_user2],
        #status_list=self.task_status_list,
        #)

        #self.test_task12 = Task(
        #name="Test Task 12",
        #task_of=self.test_shot1,
        #resources=[self.test_user3, self.test_user4],
        #status_list=self.task_status_list,
        #)

        ## for shot2 of seuqence6
        #self.test_task13 = Task(
        #name="Test Task 13",
        #task_of=self.test_shot2,
        #resources=[self.test_user5, self.test_user6],
        #status_list=self.task_status_list,
        #)

        #self.test_task14 = Task(
        #name="Test Task 14",
        #task_of=self.test_shot2,
        #resources=[self.test_user7, self.test_user8],
        #status_list=self.task_status_list,
        #)

        #self.test_task15 = Task(
        #name="Test Task 15",
        #task_of=self.test_shot2,
        #resources=[self.test_user9, self.test_user10],
        #status_list=self.task_status_list,
        #)

        ## for shot3 of seuqence7
        #self.test_task16 = Task(
        #name="Test Task 16",
        #task_of=self.test_shot3,
        #resources=[self.test_user1, self.test_user2, self.test_user3],
        #status_list=self.task_status_list,
        #)

        #self.test_task17 = Task(
        #name="Test Task 17",
        #task_of=self.test_shot3,
        #resources=[self.test_user4, self.test_user5, self.test_user6],
        #status_list=self.task_status_list,
        #)

        #self.test_task18 = Task(
        #name="Test Task 18",
        #task_of=self.test_shot3,
        #resources=[self.test_user7, self.test_user8, self.test_user9],
        #status_list=self.task_status_list,
        #)

        ## for shot4 of seuqence7
        #self.test_task19 = Task(
        #name="Test Task 19",
        #task_of=self.test_shot4,
        #resources=[self.test_user10, self.test_user1, self.test_user2],
        #status_list=self.task_status_list,
        #)

        #self.test_task20 = Task(
        #name="Test Task 20",
        #task_of=self.test_shot4,
        #resources=[self.test_user3, self.test_user4, self.test_user5],
        #status_list=self.task_status_list,
        #)

        #self.test_task21 = Task(
        #name="Test Task 21",
        #task_of=self.test_shot4,
        #resources=[self.test_user6, self.test_user7, self.test_user8],
        #status_list=self.task_status_list,
        #)

        ## tasks
        ## self.test_task10, self.test_task11, self.test_task12
        ## self.test_task13, self.test_task14, self.test_task15
        ## self.test_task16, self.test_task17, self.test_task18
        ## self.test_task19, self.test_task20, self.test_task21

        #expected_users = [self.test_user1, self.test_user2, self.test_user3,
        #self.test_user4, self.test_user5, self.test_user6,
        #self.test_user7, self.test_user8, self.test_user9,
        #self.test_user10]

        ## users
        #self.assertItemsEqual(new_project.users, expected_users)

    def test_sequences_attribute_is_read_only(self):
        """testing if the sequence attribute is read-only
        """
        self.assertRaises(AttributeError, setattr, self.test_project,
                          "sequences", ["some non sequence related data"])

        # UPDATE THIS: This test should be in the tests.db
        # because it useses an active database
    
    #def test_sequences_attribute_is_updated_with_new_sequences(self):
        #"""testing if the sequences attribute is updated with the newly created
        #sequences
        #"""

        ## first get the current sequences of the test_project
        #import copy
        #prev_sequences = copy.copy(self.test_project.sequences)

        ## create a new sequence and assign it to the given project
        #new_sequence = Sequence(
        #name="Test Sequence New",
        #project=self.test_project,
        #status_list=self.sequence_status_list,
        #)

        #self.assertIn(new_sequence, self.test_project.sequences)

        ## and verify that the sequence list is changed
        #self.assertNotEqual(prev_sequences, self.test_project.sequences)

    def test_assets_attribute_is_read_only(self):
        """testing if the assets attribute is read only
        """
        self.assertRaises(AttributeError, setattr, self.test_project, "assets",
            ["some list"])
        # UPDATE THIS: This test should be in the test.db
        # because it needs a db
        #
        #def test_assets_attribute_is_updated(self):
        #"""testing if the assets attribute is updated with the newlly created
        #assets
        #"""

        ## first get the current assets of the test_project
        #import copy
        #prev_assets = copy.copy(self.test_project.assets)

        ## create a new asset and assign it to the given project
        #new_asset = Asset(
        #name="Test Asset New",
        #type=self.asset_type,
        #project=self.test_project,
        #status_list=self.asset_status_list,
        #)

        #self.assertIn(new_asset, self.test_project.assets)

        ## and verify that the assets list is changed
        #self.assertNotEqual(prev_assets, self.test_project.assets)

    def test_image_format_argument_is_None(self):
        """testing if nothing is going to happen when the image_format is set
        to None
        """
        self.kwargs["image_format"] = None
        new_project = Project(**self.kwargs)

    def test_image_format_attribute_is_set_to_None(self):
        """testing if nothing will happen when the image_format attribute is
        set to None
        """
        self.test_project.image_format = None

    def test_image_format_argument_accepts_ImageFormat_only(self):
        """testing if a TypeError will be raised when the image_format
        argument is given as another type then ImageFormat
        """
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        for test_value in test_values:
            self.kwargs["image_format"] = test_value
            self.assertRaises(TypeError, Project, **self.kwargs)

        # and a proper image format
        self.kwargs["image_format"] = self.test_imageFormat
        new_project = Project(**self.kwargs)

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
                self.test_project,
                "image_format",
                test_value
            )

        # and a proper image format
        self.test_project.image_format = self.test_imageFormat

    def test_image_format_attribute_works_properly(self):
        """testing if the image_format attribute is working properly
        """
        new_image_format = ImageFormat(
            name="Foo Image Format",
            width=10,
            height=10
        )
        self.test_project.image_format = new_image_format
        self.assertEqual(self.test_project.image_format, new_image_format)

    def test_fps_argument_is_skipped(self):
        """testing if the default value will be used when fps is skipped
        """
        self.kwargs.pop("fps")
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.fps, 25.0)

    def test_fps_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the fps attribute is set
        to None
        """
        self.kwargs["fps"] = None
        self.assertRaises(TypeError, Project, **self.kwargs)

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

    def test_fps_attribute_is_given_as_non_float_or_integer(self):
        """testing if a TypeError will be raised when the fps attribute is
        set to a value other than a float, integer or valid string literals
        """
        test_values = ["a str"]
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.test_project,
                "fps",
                test_value
            )

        test_values = [["a", "list"], {"a": "list"}]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_project,
                "fps",
                test_value
            )

    def test_fps_argument_string_to_float_conversion(self):
        """testing if valid string literals of fps argument will be converted
        to float correctly
        """
        test_values = [("1", 1.0), ("2.3", 2.3)]
        for test_value in test_values:
            self.kwargs["fps"] = test_value[0]
            new_project = Project(**self.kwargs)
            self.assertAlmostEquals(new_project.fps, test_value[1])


    def test_fps_attribute_string_to_float_conversion(self):
        """testing if valid string literals of fps attribute will be converted
        to float correctly
        """
        test_values = [("1", 1.0), ("2.3", 2.3)]
        for test_value in test_values:
            self.test_project.fps = test_value[0]
            self.assertAlmostEquals(self.test_project.fps, test_value[1])

    def test_fps_attribute_float_conversion(self):
        """testing if the fps attribute is converted to float when the float
        argument is given as an integer
        """
        test_value = 1
        self.kwargs["fps"] = test_value
        new_project = Project(**self.kwargs)
        self.assertIsInstance(new_project.fps, float)
        self.assertEqual(new_project.fps, float(test_value))

    def test_fps_attribute_float_conversion_2(self):
        """testing if the fps attribute is converted to float when it is set to
        an integer value
        """
        test_value = 1
        self.test_project.fps = test_value
        self.assertIsInstance(self.test_project.fps, float)
        self.assertEqual(self.test_project.fps, float(test_value))

    def test_repository_argument_is_skipped(self):
        """testing if a TypeError will be raised when the repository argument
        is skipped
        """
        self.kwargs.pop("repository")
        self.assertRaises(TypeError, Project, **self.kwargs)

    def test_repository_argument_is_None(self):
        """testing if a TypeError will be raised when the repository argument
        is given as None.
        """
        self.kwargs["repository"] = None
        self.assertRaises(TypeError, Project, **self.kwargs)

        #def test_repository_attribute_is_set_to_None(self):
        #"""testing if nothing happens when setting the repository attribute to
        #None
        #"""
        #self.test_project.repository = None

    def test_repository_argument_is_non_Repository_object(self):
        """testing if a TypeError will be raised when the repository argument
        is given as something other than a Repository object
        """
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        for test_value in test_values:
            self.kwargs["repository"] = test_value
            self.assertRaises(TypeError, Project, **self.kwargs)

            #def test_repository_attribute_is_set_to_non_Repository_object(self):
            #"""testing if a TypeErorr will be raised when the repository attribute
            #is tried to be set to something other than a Repository object
            #"""

            #test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
            #for test_value in test_values:
            #self.assertRaises(
            #TypeError,
            #setattr,
            #self.test_project,
            #"repository",
            #test_value
            #)

    def test_repository_attribute_is_working_properly(self):
        """testing if the repository attribute is working properly
        """
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.repository, self.kwargs["repository"])

    def test_is_stereoscopic_argument_skipped(self):
        """testing if is_stereoscopic will set the is_stereoscopic attribute to
        False
        """
        self.kwargs.pop("is_stereoscopic")
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.is_stereoscopic, False)

    def test_is_stereoscopic_argument_bool_conversion(self):
        """testing if all the given values for is_stereoscopic argument will be
        converted to a bool value correctly
        """
        test_values = [0, 1, 1.2, "", "str", ["a", "list"]]
        for test_value in test_values:
            self.kwargs["is_stereoscopic"] = test_value
            new_project = Project(**self.kwargs)
            self.assertEqual(new_project.is_stereoscopic, bool(test_value))

    def test_is_stereoscopic_attribute_bool_conversion(self):
        """testing if all the given values for is_stereoscopic attribute will
        be converted to a bool value correctly
        """
        test_values = [0, 1, 1.2, "", "str", ["a", "list"]]
        for test_value in test_values:
            self.test_project.is_stereoscopic = test_value
            self.assertEqual(
                self.test_project.is_stereoscopic,
                bool(test_value)
            )

            #def test_display_width_argument_is_skipped(self):
            #"""testing if the display_width attribute will be set to the default
            #value when the display_width argument is skipped
            #"""
            #self.kwargs.pop("display_width")
            #new_project = Project(**self.kwargs)
            #self.assertEqual(new_project.display_width, 1.0)

            #def test_display_width_argument_float_conversion(self):
            #"""testing if the display_width attribute is converted to float
            #correctly for various display_width arguments
            #"""
            #test_values = [1, 2, 3, 4]
            #for test_value in test_values:
            #self.kwargs["display_width"] = test_value
            #new_project = Project(**self.kwargs)
            #self.assertIsInstance(new_project.display_width, float)
            #self.assertEqual(new_project.display_width, float(test_value))

            #def test_display_width_attribute_float_conversion(self):
            #"""testing if the display_width attribute is converted to float
            #correctly
            #"""
            #test_values = [1, 2, 3, 4]
            #for test_value in test_values:
            #self.test_project.display_width = test_value
            #self.assertIsInstance(self.test_project.display_width, float)
            #self.assertEqual(self.test_project.display_width,
            #float(test_value))

            #def test_display_width_argument_is_given_as_a_negative_value(self):
            #"""testing if the display_width attribute is set to the absolute value
            #of the given negative display_width argument
            #"""
            #test_value = -1.0
            #self.kwargs["display_width"] = test_value
            #new_project = Project(**self.kwargs)
            #self.assertEqual(new_project.display_width, abs(test_value))

            #def test_display_width_attribute_is_set_to_a_negative_value(self):
            #"""testing if the display_width attribute is set to default value when
            #it is set to a negative value
            #"""
            #test_value = -1.0
            #self.test_project.display_width = test_value
            #self.assertEqual(self.test_project.display_width, abs(test_value))

    def test_structure_argument_is_None(self):
        """testing if nothing happens when the structure argument is None
        """
        self.kwargs["structure"] = None
        new_project = Project(**self.kwargs)

    def test_structure_attribute_is_None(self):
        """testing if nothing happens when the structure attribute is set to
        None
        """
        self.test_project.structure = None

    def test_structure_argument_not_instance_of_Structure(self):
        """testing if a TypeError will be raised when the structure argument
        is not an instance of Structure
        """
        test_values = [1, 1.2, "a str", ["a", "list"]]
        for test_value in test_values:
            self.kwargs["structure"] = test_value
            self.assertRaises(TypeError, Project, **self.kwargs)

    def test_structure_attribute_not_instance_of_Structure(self):
        """testing if a TypeError will be raised when the structure attribute
        is not an instance of Structure
        """
        test_values = [1, 1.2, "a str", ["a", "list"]]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_project,
                "structure",
                test_value
            )

    def test_structure_attribute_is_working_properly(self):
        """testing if the structure attribute is working properly
        """
        self.test_project.structure = self.test_project_structure2
        self.assertEqual(self.test_project.structure,
                         self.test_project_structure2)

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

        self.assertTrue(self.test_project == new_project1)
        self.assertFalse(self.test_project == new_project2)
        self.assertFalse(self.test_project == new_entity)

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

        self.assertFalse(self.test_project != new_project1)
        self.assertTrue(self.test_project != new_project2)
        self.assertTrue(self.test_project != new_entity)

    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """
        link_type_1 = Type(
            name="Image",
            code='image',
            target_entity_type="Link"
        )

        link1 = Link(name="Artwork 1", path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="a.jpg", type=link_type_1)

        link2 = Link(name="Artwork 2", path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="b.jbg", type=link_type_1)

        references = [link1, link2]

        self.kwargs["references"] = references
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.references, references)

    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Complete", code="CMPLT")

        status_list = StatusList(name="Project Statuses",
                                 statuses=[status1, status2],
                                 target_entity_type=Project)
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list
        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.status_list, status_list)

    def test_ScheduleMixin_initialization(self):
        """testing if the ScheduleMixin part is initialized correctly
        """
        start_date = datetime.date.today() + datetime.timedelta(days=25)
        end_date = start_date + datetime.timedelta(days=12)

        self.kwargs["start_date"] = start_date
        self.kwargs["end_date"] = end_date

        new_project = Project(**self.kwargs)
        self.assertEqual(new_project.start_date, start_date)
        self.assertEqual(new_project.end_date, end_date)
        self.assertEqual(new_project.duration, end_date - start_date)

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ is True for Project class
        """
        self.assertEqual(Project.__strictly_typed__, False)

    def test___strictly_typed___not_forces_type_initialization(self):
        """testing if Project can not be created without defining a type for it
        """
        self.kwargs.pop("type")
        new_project = Project(**self.kwargs) # should be possible

    def test_project_attribute_equals_to_self(self):
        """testing if the Project.project equals to self
        """
        self.assertEqual(self.test_project.project, self.test_project)
    
    def test_project_tasks_attribute_returns_the_Tasks_instances_related_to_this_project(self):
        """testing if the tasks attribute returns a list of Task instances
        related to this Project instance.
        """
        # test if we are going to get all the Tasks for project.tasks
        self.assertEqual(len(self.test_project.project_tasks), 27)
        self.assertIn(self.test_task1, self.test_project.project_tasks)
        self.assertIn(self.test_task2, self.test_project.project_tasks)
        self.assertIn(self.test_task3, self.test_project.project_tasks)
        self.assertIn(self.test_task4, self.test_project.project_tasks)
        self.assertIn(self.test_task5, self.test_project.project_tasks)
        self.assertIn(self.test_task6, self.test_project.project_tasks)
        self.assertIn(self.test_task7, self.test_project.project_tasks)
        self.assertIn(self.test_task8, self.test_project.project_tasks)
        self.assertIn(self.test_task9, self.test_project.project_tasks)
        self.assertIn(self.test_task10, self.test_project.project_tasks)
        self.assertIn(self.test_task11, self.test_project.project_tasks)
        self.assertIn(self.test_task12, self.test_project.project_tasks)
        self.assertIn(self.test_task13, self.test_project.project_tasks)
        self.assertIn(self.test_task14, self.test_project.project_tasks)
        self.assertIn(self.test_task15, self.test_project.project_tasks)
        self.assertIn(self.test_task16, self.test_project.project_tasks)
        self.assertIn(self.test_task17, self.test_project.project_tasks)
        self.assertIn(self.test_task18, self.test_project.project_tasks)
        self.assertIn(self.test_task19, self.test_project.project_tasks)
        self.assertIn(self.test_task20, self.test_project.project_tasks)
        self.assertIn(self.test_task21, self.test_project.project_tasks)
        self.assertIn(self.test_task22, self.test_project.project_tasks)
        self.assertIn(self.test_task23, self.test_project.project_tasks)
        self.assertIn(self.test_task24, self.test_project.project_tasks)
        self.assertIn(self.test_task25, self.test_project.project_tasks)
        self.assertIn(self.test_task26, self.test_project.project_tasks)
        self.assertIn(self.test_task27, self.test_project.project_tasks)
        
