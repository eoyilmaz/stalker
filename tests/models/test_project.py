# -*- coding: utf-8 -*-

import logging
import pytest
from stalker import log
from stalker.testing import UnitTestDBBase
logger = logging.getLogger('stalker.models.project')
logger.setLevel(log.logging_level)


class ProjectTestDBCase(UnitTestDBBase):
    """tests the Project class
    """

    def setUp(self):
        """setup the test
        """
        super(ProjectTestDBCase, self).setUp()

        # create test objects
        import datetime
        import pytz
        self.start = datetime.datetime(2016, 11, 17, tzinfo=pytz.utc)
        self.end = self.start + datetime.timedelta(days=20)

        from stalker import User
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

        self.test_user_client = User(
            name="User Client",
            login="userClient",
            email="user@client.com",
            password="123456"
        )
        from stalker.db.session import DBSession
        DBSession.save([
            self.test_lead, self.test_user1, self.test_user2, self.test_user3,
            self.test_user4, self.test_user5, self.test_user6, self.test_user7,
            self.test_user8, self.test_user9, self.test_user10,
            self.test_user_client
        ])

        from stalker import ImageFormat
        self.test_image_format = ImageFormat(
            name="HD",
            width=1920,
            height=1080,
        )

        # type for project
        from stalker import Type
        self.test_project_type = Type(
            name="Project Type 1",
            code='projt1',
            target_entity_type='Project'
        )

        self.test_project_type2 = Type(
            name="Project Type 2",
            code='projt2',
            target_entity_type='Project'
        )

        # type for structure
        self.test_structure_type1 = Type(
            name="Structure Type 1",
            code='struct1',
            target_entity_type='Structure'
        )

        self.test_structure_type2 = Type(
            name="Structure Type 2",
            code='struct2',
            target_entity_type='Structure'
        )

        from stalker import Structure
        self.test_project_structure = Structure(
            name="Project Structure 1",
            type=self.test_structure_type1,
        )

        self.test_project_structure2 = Structure(
            name="Project Structure 2",
            type=self.test_structure_type2,
        )

        from stalker import Repository
        self.test_repo1 = Repository(
            name="Commercials Repository 1",
            code="CR1",
        )

        self.test_repo2 = Repository(
            name="Commercials Repository 2",
            code="CR2"
        )

        from stalker import Client
        self.test_client = Client(
            name='Test Company',
            users=[self.test_user_client]
        )
        DBSession.save([
            self.test_image_format, self.test_project_type, self.test_project_type2,
            self.test_structure_type1, self.test_structure_type2, self.test_project_structure,
            self.test_project_structure2, self.test_repo1, self.test_repo2, self.test_client
        ])

        # create a project object
        self.kwargs = {
            "name": "Test Project",
            'code': 'tp',
            "description": "This is a project object for testing purposes",
            "image_format": self.test_image_format,
            "fps": 25,
            "type": self.test_project_type,
            "structure": self.test_project_structure,
            "repositories": [self.test_repo1, self.test_repo2],
            "is_stereoscopic": False,
            "display_width": 15,
            "start": self.start,
            "end": self.end,
            "clients": [self.test_client]
        }

        from stalker import Project
        self.test_project = Project(**self.kwargs)
        DBSession.add(self.test_project)
        DBSession.commit()

        # sequences without tasks
        from stalker import Sequence
        self.test_seq1 = Sequence(
            name="Seq1",
            code='Seq1',
            project=self.test_project,
            resources=[self.test_user1],
            responsible=[self.test_user1]
        )

        self.test_seq2 = Sequence(
            name="Seq2",
            code='Seq2',
            project=self.test_project,
            resources=[self.test_user2],
            responsible=[self.test_user2]
        )

        self.test_seq3 = Sequence(
            name="Seq3",
            code='Seq3',
            project=self.test_project,
            resources=[self.test_user3],
            responsible=[self.test_user1]
        )

        # sequences with tasks
        self.test_seq4 = Sequence(
            name="Seq4",
            code='Seq4',
            project=self.test_project,
            responsible=[self.test_user1]
        )

        self.test_seq5 = Sequence(
            name="Seq5",
            code='Seq5',
            project=self.test_project,
            responsible=[self.test_user1]
        )

        # sequences without tasks but with shots
        self.test_seq6 = Sequence(
            name="Seq6",
            code='Seq6',
            project=self.test_project,
            responsible=[self.test_user1]
        )

        self.test_seq7 = Sequence(
            name="Seq7",
            code='Seq7',
            project=self.test_project,
            responsible=[self.test_user1]
        )

        # shots
        from stalker import Shot
        self.test_shot1 = Shot(
            code="SH001",
            project=self.test_project,
            sequences=[self.test_seq6],
            responsible=[self.test_lead],
        )

        self.test_shot2 = Shot(
            code="SH002",
            project=self.test_project,
            sequences=[self.test_seq6],
            responsible=[self.test_lead],
        )

        self.test_shot3 = Shot(
            code="SH003",
            project=self.test_project,
            sequences=[self.test_seq7],
            responsible=[self.test_lead],
        )

        self.test_shot4 = Shot(
            code="SH004",
            project=self.test_project,
            sequences=[self.test_seq7],
            responsible=[self.test_lead],
        )

        # asset types
        self.asset_type = Type(
            name="Character",
            code='char',
            target_entity_type='Asset',
        )

        # assets without tasks
        from stalker import Asset
        self.test_asset1 = Asset(
            name="Test Asset 1",
            code='ta1',
            type=self.asset_type,
            project=self.test_project,
            resources=[self.test_user2],
            responsible=[self.test_lead],
        )

        self.test_asset2 = Asset(
            name="Test Asset 2",
            code='ta2',
            type=self.asset_type,
            project=self.test_project,
            responsible=[self.test_lead],
        )

        self.test_asset3 = Asset(
            name="Test Asset 3",
            code='ta3',
            type=self.asset_type,
            project=self.test_project,
            responsible=[self.test_lead],
        )

        # assets with tasks
        self.test_asset4 = Asset(
            name="Test Asset 4",
            code='ta4',
            type=self.asset_type,
            project=self.test_project,
            responsible=[self.test_lead],
        )

        self.test_asset5 = Asset(
            name="Test Asset 5",
            code='ta5',
            type=self.asset_type,
            project=self.test_project,
        )

        # for project
        from stalker import Task
        self.test_task1 = Task(
            name="Test Task 1",
            project=self.test_project,
            resources=[self.test_user1],
        )

        self.test_task2 = Task(
            name="Test Task 2",
            project=self.test_project,
            resources=[self.test_user2],
        )

        self.test_task3 = Task(
            name="Test Task 3",
            project=self.test_project,
            resources=[self.test_user3],
        )

        # for sequence4
        self.test_task4 = Task(
            name="Test Task 4",
            parent=self.test_seq4,
            resources=[self.test_user4],
        )

        self.test_task5 = Task(
            name="Test Task 5",
            parent=self.test_seq4,
            resources=[self.test_user5],
        )

        self.test_task6 = Task(
            name="Test Task 6",
            parent=self.test_seq4,
            resources=[self.test_user6],
        )

        # for sequence5
        self.test_task7 = Task(
            name="Test Task 7",
            parent=self.test_seq5,
            resources=[self.test_user7],
        )

        self.test_task8 = Task(
            name="Test Task 8",
            parent=self.test_seq5,
            resources=[self.test_user8],
        )

        self.test_task9 = Task(
            name="Test Task 9",
            parent=self.test_seq5,
            resources=[self.test_user9],
        )

        # for shot1 of sequence6
        self.test_task10 = Task(
            name="Test Task 10",
            parent=self.test_shot1,
            resources=[self.test_user10],
            schedule_timing=10
        )

        self.test_task11 = Task(
            name="Test Task 11",
            parent=self.test_shot1,
            resources=[self.test_user1, self.test_user2],
        )

        self.test_task12 = Task(
            name="Test Task 12",
            parent=self.test_shot1,
            resources=[self.test_user3, self.test_user4],
        )

        # for shot2 of sequence6
        self.test_task13 = Task(
            name="Test Task 13",
            parent=self.test_shot2,
            resources=[self.test_user5, self.test_user6],
        )

        self.test_task14 = Task(
            name="Test Task 14",
            parent=self.test_shot2,
            resources=[self.test_user7, self.test_user8],
        )

        self.test_task15 = Task(
            name="Test Task 15",
            parent=self.test_shot2,
            resources=[self.test_user9, self.test_user10],
        )

        # for shot3 of sequence7
        self.test_task16 = Task(
            name="Test Task 16",
            parent=self.test_shot3,
            resources=[self.test_user1, self.test_user2, self.test_user3],
        )

        self.test_task17 = Task(
            name="Test Task 17",
            parent=self.test_shot3,
            resources=[self.test_user4, self.test_user5, self.test_user6],
        )

        self.test_task18 = Task(
            name="Test Task 18",
            parent=self.test_shot3,
            resources=[self.test_user7, self.test_user8, self.test_user9],
        )

        # for shot4 of sequence7
        self.test_task19 = Task(
            name="Test Task 19",
            parent=self.test_shot4,
            resources=[self.test_user10, self.test_user1, self.test_user2],
        )

        self.test_task20 = Task(
            name="Test Task 20",
            parent=self.test_shot4,
            resources=[self.test_user3, self.test_user4, self.test_user5],
        )

        self.test_task21 = Task(
            name="Test Task 21",
            parent=self.test_shot4,
            resources=[self.test_user6, self.test_user7, self.test_user8],
        )

        # for asset4
        self.test_task22 = Task(
            name="Test Task 22",
            parent=self.test_asset4,
            resources=[self.test_user9, self.test_user10, self.test_user1],
        )

        self.test_task23 = Task(
            name="Test Task 23",
            parent=self.test_asset4,
            resources=[self.test_user2, self.test_user3],
        )

        self.test_task24 = Task(
            name="Test Task 24",
            parent=self.test_asset4,
            resources=[self.test_user4, self.test_user5],
        )

        # for asset5
        self.test_task25 = Task(
            name="Test Task 25",
            parent=self.test_asset5,
            resources=[self.test_user6, self.test_user7],
        )

        self.test_task26 = Task(
            name="Test Task 26",
            parent=self.test_asset5,
            resources=[self.test_user8, self.test_user9],
        )

        self.test_task27 = Task(
            name="Test Task 27",
            parent=self.test_asset5,
            resources=[self.test_user10, self.test_user1],
        )

        # final task hierarchy
        # test_seq1
        # test_seq2
        # test_seq3
        #
        # test_seq4
        #     test_task4
        #     test_task5
        #     test_task6
        # test_seq5
        #     test_task7
        #     test_task8
        #     test_task9
        # test_seq6
        # test_seq7
        #
        # test_shot1
        #     test_task10
        #     test_task11
        #     test_task12
        # test_shot2
        #     test_task13
        #     test_task14
        #     test_task15
        # test_shot3
        #     test_task16
        #     test_task17
        #     test_task18
        # test_shot4
        #     test_task19
        #     test_task20
        #     test_task21
        #
        # test_asset1
        # test_asset2
        # test_asset3
        # test_asset4
        #     test_task22
        #     test_task23
        #     test_task24
        # test_asset5
        #     test_task25
        #     test_task26
        #     test_task27
        #
        # test_task1
        # test_task2
        # test_task3

        DBSession.add(self.test_project)
        DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Project class
        """
        from stalker import Project
        assert Project.__auto_name__ is False

    def test_setup_is_working_correctly(self):
        """testing if the setup is done correctly
        """
        from stalker import Type
        assert isinstance(self.test_project_type, Type)
        assert isinstance(self.test_project_type2, Type)

    def test_sequences_attribute_is_read_only(self):
        """testing if the sequence attribute is read-only
        """
        with pytest.raises(AttributeError) as cm:
            self.test_project.sequences = ["some non sequence related data"]

        assert str(cm.value) == "can't set attribute"

    def test_assets_attribute_is_read_only(self):
        """testing if the assets attribute is read only
        """
        with pytest.raises(AttributeError) as cm:
            self.test_project.assets = ["some list"]

    def test_image_format_argument_is_skipped(self):
        """testing if image_format attribute will be None when the image_format
        argument is skipped
        """
        self.kwargs.pop("image_format")
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.image_format is None

    def test_image_format_argument_is_None(self):
        """testing if nothing is going to happen when the image_format is set
        to None
        """
        self.kwargs["image_format"] = None
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.image_format is None

    def test_image_format_attribute_is_set_to_None(self):
        """testing if nothing will happen when the image_format attribute is
        set to None
        """
        self.test_project.image_format = None

    def test_image_format_argument_accepts_ImageFormat_only(self):
        """testing if a TypeError will be raised when the image_format
        argument is given as another type then ImageFormat
        """
        from stalker import Project
        self.kwargs["image_format"] = "a str"
        with pytest.raises(TypeError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'Project.image_format should be an instance of ' \
            'stalker.models.format.ImageFormat, not str'

    def test_image_format_argument_is_working_properly(self):
        """testing if the image_format argument value is correctly passed to
        the image_format attribute
        """
        # and a proper image format
        from stalker import Project
        self.kwargs["image_format"] = self.test_image_format
        new_project = Project(**self.kwargs)
        assert new_project.image_format == self.test_image_format

    def test_image_format_attribute_accepts_ImageFormat_only(self):
        """testing if a TypeError will be raised when the image_format
        attribute is tried to be set to something other than a ImageFormat
        instance
        """
        test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
        for test_value in test_values:
            with pytest.raises(TypeError) as cm:
                self.test_project.image_format = test_value

        # and a proper image format
        self.test_project.image_format = self.test_image_format

    def test_image_format_attribute_works_properly(self):
        """testing if the image_format attribute is working properly
        """
        from stalker import ImageFormat
        new_image_format = ImageFormat(
            name="Foo Image Format",
            width=10,
            height=10
        )
        self.test_project.image_format = new_image_format
        assert self.test_project.image_format == new_image_format

    def test_fps_argument_is_skipped(self):
        """testing if the default value will be used when fps is skipped
        """
        self.kwargs.pop("fps")
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.fps == 25.0

    def test_fps_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the fps attribute is set
        to None
        """
        self.kwargs["fps"] = None
        from stalker import Project
        with pytest.raises(TypeError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not NoneType'

    def test_fps_argument_is_given_as_non_float_or_integer_1(self):
        """testing if a TypeError will be raised when the fps argument is
        given as a value other than a float or integer, or a string which is
        convertible to float.
        """
        from stalker import Project
        self.kwargs["fps"] = "a str"
        with pytest.raises(TypeError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not str'

    def test_fps_argument_is_given_as_non_float_or_integer_2(self):
        """testing if a TypeError will be raised when the fps argument is
        given as a value other than a float or integer, or a string which is
        convertible to float.
        """
        from stalker import Project
        self.kwargs["fps"] = ["a", "list"]
        with pytest.raises(TypeError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not list'

    def test_fps_attribute_is_given_as_non_float_or_integer_1(self):
        """testing if a TypeError will be raised when the fps attribute is
        set to a value other than a float, integer or valid string literals
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.fps = "a str"

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not str'

    def test_fps_attribute_is_given_as_non_float_or_integer_2(self):
        """testing if a TypeError will be raised when the fps attribute is
        set to a value other than a float, integer or valid string literals
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.fps = ["a", "list"]

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not list'

    def test_fps_argument_string_to_float_conversion(self):
        """testing if a TypeError will be raised when a string containing a
        float has been passed
        """
        from stalker import Project
        self.kwargs["fps"] = "2.3"
        with pytest.raises(TypeError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not str'

    def test_fps_attribute_string_to_float_conversion(self):
        """testing if a TypeError will be raised if a the fps attribute is set
        to a string containing a float
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.fps = "2.3"

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not str'

    def test_fps_attribute_float_conversion(self):
        """testing if the fps attribute is converted to float when the float
        argument is given as an integer
        """
        test_value = 1
        self.kwargs["fps"] = test_value
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert isinstance(new_project.fps, float)
        assert new_project.fps == float(test_value)

    def test_fps_attribute_float_conversion_2(self):
        """testing if the fps attribute is converted to float when it is set to
        an integer value
        """
        test_value = 1
        self.test_project.fps = test_value
        assert isinstance(self.test_project.fps, float)
        assert self.test_project.fps == float(test_value)

    def test_fps_argument_is_zero(self):
        """testing if a ValueError will be raised when the fps is 0
        """
        self.kwargs['fps'] = 0
        from stalker import Project

        with pytest.raises(ValueError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not 0.0'

    def test_fps_attribute_is_set_to_zero(self):
        """testing if a value error will be raised when the fps attribute is
        set to zero
        """
        with pytest.raises(ValueError) as cm:
            self.test_project.fps = 0

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not 0.0'

    def test_fps_argument_is_negative(self):
        """testing if a ValueError will be raised when the fps argument is
        negative
        """
        self.kwargs['fps'] = -1.0
        from stalker import Project
        with pytest.raises(ValueError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not -1.0'

    def test_fps_attribute_is_negative(self):
        """testing if a ValueError will be raised when the fps attribute is
        set to a negative value
        """
        with pytest.raises(ValueError) as cm:
            self.test_project.fps = -1

        assert str(cm.value) == \
            'Project.fps should be a positive float or int, not -1.0'

    def test_repositories_argument_is_skipped(self):
        """testing if the repositories attribute will be an empty list if the
        repositories argument is skipped
        """
        self.kwargs.pop("repositories")
        from stalker import Project
        p = Project(**self.kwargs)
        assert p.repositories == []

    def test_repositories_argument_is_None(self):
        """testing if a the repositories attribute will be an empty list if the
        repositories argument is None.
        """
        self.kwargs["repositories"] = None
        from stalker import Project
        p = Project(**self.kwargs)
        assert p.repositories == []

    def test_repositories_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the repositories
        attribute is set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.repositories = None

        assert str(cm.value) == \
            "'NoneType' object is not iterable"

    def test_repositories_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the repositories argument
        value is not a list
        """
        self.kwargs['repositories'] = 'not a list'
        with pytest.raises(TypeError) as cm:
            from stalker import Project
            Project(**self.kwargs)

        assert str(cm.value) == \
            'ProjectRepository.repositories should be a list of ' \
            'stalker.models.repository.Repository instances or derivatives, ' \
            'not str'

    def test_repositories_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the repositories
        attribute is set to a value other than a list
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.repositories = 'not a list'

        assert str(cm.value) == \
            'ProjectRepository.repositories should be a list of ' \
            'stalker.models.repository.Repository instances or derivatives, ' \
            'not str'

    def test_repositories_argument_is_not_a_list_of_repository_instances(self):
        """testing if a TypeError will be raised if the repositories argument
        value is a list of objects which are not Repository instances
        """
        from stalker import Repository, Project
        self.kwargs['repositories'] = ['not', 1, 'list', 'of', Repository,
                                       'instances']
        with pytest.raises(TypeError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'ProjectRepository.repositories should be a list of ' \
            'stalker.models.repository.Repository instances or derivatives, ' \
            'not str'

    def test_repositories_attribute_is_not_a_list_of_repository_instances(self):
        """testing if a TypeError will be raised if the repositories attribute
        is set to a list that contains objects other than Repository instances
        """
        with pytest.raises(TypeError) as cm:
            from stalker import Repository
            self.test_project.repositories = ['not', 1, 'list', 'of',
                                              Repository, 'instances']

        assert str(cm.value) == \
            'ProjectRepository.repositories should be a list of ' \
            'stalker.models.repository.Repository instances or derivatives, ' \
            'not str'

    def test_repositories_argument_is_working_properly(self):
        """testing if the repositories argument value is properly passed to the
        repositories attribute value
        """
        assert self.test_project.repositories == self.kwargs['repositories']

    def test_repositories_attribute_is_working_properly(self):
        """testing if the repository attribute is working properly
        """
        from stalker import Repository
        new_repo1 = Repository(
            name='Some Random Repo',
            code='SRP',
            linux_path='/mnt/S/random/repo',
            windows_path='S:/random/repo',
            osx_path='/Volumes/S/random/repo'
        )

        assert self.test_project.repositories != [new_repo1]
        self.test_project.repositories = [new_repo1]
        assert self.test_project.repositories == [new_repo1]

    def test_repositories_attribute_value_order_is_not_changing(self):
        """testing if the order of the repositories attribute is not changing
        """
        from stalker import Repository, Project
        repo1 = Repository(name='Repo1', code='R1')
        repo2 = Repository(name='Repo2', code='R1')
        repo3 = Repository(name='Repo3', code='R1')

        from stalker.db.session import DBSession
        DBSession.add_all([repo1, repo2, repo3])
        DBSession.commit()

        test_value = [repo3, repo1, repo2]
        self.test_project.repositories = test_value
        DBSession.commit()

        for i in range(10):
            db_proj = Project.query.first()
            assert db_proj.repositories == test_value
            DBSession.commit()

    def test_is_stereoscopic_argument_skipped(self):
        """testing if is_stereoscopic will set the is_stereoscopic attribute to
        False
        """
        self.kwargs.pop("is_stereoscopic")
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.is_stereoscopic is False

    def test_is_stereoscopic_argument_bool_conversion(self):
        """testing if all the given values for is_stereoscopic argument will be
        converted to a bool value correctly
        """
        from stalker import Project
        test_values = [0, 1, 1.2, "", "str", ["a", "list"]]
        for test_value in test_values:
            self.kwargs["is_stereoscopic"] = test_value
            new_project = Project(**self.kwargs)
            assert new_project.is_stereoscopic == bool(test_value)

    def test_is_stereoscopic_attribute_bool_conversion(self):
        """testing if all the given values for is_stereoscopic attribute will
        be converted to a bool value correctly
        """
        test_values = [0, 1, 1.2, "", "str", ["a", "list"]]
        for test_value in test_values:
            self.test_project.is_stereoscopic = test_value
            assert self.test_project.is_stereoscopic == bool(test_value)

    def test_structure_argument_is_None(self):
        """testing if nothing happens when the structure argument is None
        """
        self.kwargs["structure"] = None
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert isinstance(new_project, Project)

    def test_structure_attribute_is_None(self):
        """testing if nothing happens when the structure attribute is set to
        None
        """
        self.test_project.structure = None

    def test_structure_argument_not_instance_of_Structure(self):
        """testing if a TypeError will be raised when the structure argument
        is not an instance of Structure
        """
        from stalker import Project
        self.kwargs["structure"] = 1.215
        with pytest.raises(TypeError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'Project.structure should be an instance of ' \
            'stalker.models.structure.Structure, not float'

    def test_structure_attribute_not_instance_of_Structure(self):
        """testing if a TypeError will be raised when the structure attribute
        is not an instance of Structure
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.structure = 1.2

        assert str(cm.value) == \
            'Project.structure should be an instance of ' \
            'stalker.models.structure.Structure, not float'

    def test_structure_attribute_is_working_properly(self):
        """testing if the structure attribute is working properly
        """
        self.test_project.structure = self.test_project_structure2
        assert self.test_project.structure == self.test_project_structure2

    def test_equality(self):
        """testing the equality of two projects
        """
        # create a new project with the same arguments
        from stalker import Entity, Project
        new_project1 = Project(**self.kwargs)

        # create a new entity with the same arguments
        new_entity = Entity(**self.kwargs)

        # create another project with different name
        self.kwargs["name"] = "a different project"
        new_project2 = Project(**self.kwargs)

        assert not self.test_project != new_project1
        assert self.test_project != new_project2
        assert self.test_project != new_entity

    def test_inequality(self):
        """testing the inequality of two projects
        """
        # create a new project with the same arguments
        from stalker import Entity, Project
        new_project1 = Project(**self.kwargs)

        # create a new entity with the same arguments
        new_entity = Entity(**self.kwargs)

        # create another project with different name
        self.kwargs["name"] = "a different project"
        new_project2 = Project(**self.kwargs)

        assert not self.test_project != new_project1
        assert self.test_project != new_project2
        assert self.test_project != new_entity

    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """
        from stalker import Type, Link, Project
        link_type_1 = Type(
            name="Image",
            code='image',
            target_entity_type="Link"
        )

        link1 = Link(name="Artwork 1", full_path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="a.jpg", type=link_type_1)

        link2 = Link(name="Artwork 2", full_path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="b.jbg", type=link_type_1)

        references = [link1, link2]

        self.kwargs["references"] = references
        new_project = Project(**self.kwargs)
        assert new_project.references == references

    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """
        from stalker import StatusList
        status_list = StatusList\
            .query.filter_by(target_entity_type='Project').first()
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.status_list == status_list

    def test_ScheduleMixin_initialization(self):
        """testing if the DateRangeMixin part is initialized correctly
        """
        import datetime
        import pytz
        start = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) \
            + datetime.timedelta(days=25)
        end = start + datetime.timedelta(days=12)

        self.kwargs["start"] = start
        self.kwargs["end"] = end

        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.start == start
        assert new_project.end == end
        assert new_project.duration == end - start

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ is True for Project class
        """
        from stalker import Project
        assert Project.__strictly_typed__ is False

    def test___strictly_typed___not_forces_type_initialization(self):
        """testing if Project can not be created without defining a type for it
        """
        self.kwargs.pop("type")
        from stalker import Project
        Project(**self.kwargs)  # should be possible

    def test_tasks_attribute_returns_the_Tasks_instances_related_to_this_project(self):
        """testing if the tasks attribute returns a list of Task instances
        related to this Project instance.
        """
        # test if we are going to get all the Tasks for project.tasks
        assert len(self.test_project.tasks) == 43
        assert self.test_task1 in self.test_project.tasks
        assert self.test_task2 in self.test_project.tasks
        assert self.test_task3 in self.test_project.tasks
        assert self.test_task4 in self.test_project.tasks
        assert self.test_task5 in self.test_project.tasks
        assert self.test_task6 in self.test_project.tasks
        assert self.test_task7 in self.test_project.tasks
        assert self.test_task8 in self.test_project.tasks
        assert self.test_task9 in self.test_project.tasks
        assert self.test_task10 in self.test_project.tasks
        assert self.test_task11 in self.test_project.tasks
        assert self.test_task12 in self.test_project.tasks
        assert self.test_task13 in self.test_project.tasks
        assert self.test_task14 in self.test_project.tasks
        assert self.test_task15 in self.test_project.tasks
        assert self.test_task16 in self.test_project.tasks
        assert self.test_task17 in self.test_project.tasks
        assert self.test_task18 in self.test_project.tasks
        assert self.test_task19 in self.test_project.tasks
        assert self.test_task20 in self.test_project.tasks
        assert self.test_task21 in self.test_project.tasks
        assert self.test_task22 in self.test_project.tasks
        assert self.test_task23 in self.test_project.tasks
        assert self.test_task24 in self.test_project.tasks
        assert self.test_task25 in self.test_project.tasks
        assert self.test_task26 in self.test_project.tasks
        assert self.test_task27 in self.test_project.tasks

        # assets, sequences and shots are also Tasks
        assert self.test_seq1 in self.test_project.tasks
        assert self.test_seq2 in self.test_project.tasks
        assert self.test_seq3 in self.test_project.tasks
        assert self.test_seq4 in self.test_project.tasks
        assert self.test_seq5 in self.test_project.tasks
        assert self.test_seq6 in self.test_project.tasks
        assert self.test_seq7 in self.test_project.tasks
 
        assert self.test_asset1 in self.test_project.tasks
        assert self.test_asset2 in self.test_project.tasks
        assert self.test_asset3 in self.test_project.tasks
        assert self.test_asset4 in self.test_project.tasks
        assert self.test_asset5 in self.test_project.tasks
 
        assert self.test_shot1 in self.test_project.tasks
        assert self.test_shot2 in self.test_project.tasks
        assert self.test_shot3 in self.test_project.tasks
        assert self.test_shot4 in self.test_project.tasks

    def test_root_tasks_attribute_returns_the_Tasks_instances_with_no_parent_in_this_project(self):
        """testing if the root_tasks attribute returns a list of Task instances
        related to this Project instance and has no parent.
        """
        # test if we are going to get all the Tasks for project.tasks
        root_tasks = self.test_project.root_tasks
        assert len(root_tasks) == 19
        assert self.test_task1 in root_tasks
        assert self.test_task2 in root_tasks
        assert self.test_task3 in root_tasks

        # assets, sequences and shots are also Tasks
        assert self.test_seq1 in root_tasks
        assert self.test_seq2 in root_tasks
        assert self.test_seq3 in root_tasks
        assert self.test_seq4 in root_tasks
        assert self.test_seq5 in root_tasks
        assert self.test_seq6 in root_tasks
        assert self.test_seq7 in root_tasks

        assert self.test_asset1 in root_tasks
        assert self.test_asset2 in root_tasks
        assert self.test_asset3 in root_tasks
        assert self.test_asset4 in root_tasks
        assert self.test_asset5 in root_tasks

        assert self.test_shot1 in root_tasks
        assert self.test_shot2 in root_tasks
        assert self.test_shot3 in root_tasks
        assert self.test_shot4 in root_tasks

    def test_users_argument_is_skipped(self):
        """testing if the users attribute will be an empty list when the users
        argument is skipped
        """
        self.kwargs['name'] = 'New Project Name'
        try:
            self.kwargs.pop('users')
        except KeyError:
            pass
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.users == []

    def test_users_argument_is_None(self):
        """testing if a the users attribute will be an empty list when the
        users argument is set to None
        """
        self.kwargs['name'] = 'New Project Name'
        self.kwargs['users'] = None
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.users == []

    def test_users_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the users attribute is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.users = None

        assert str(cm.value) == "'NoneType' object is not iterable"

    def test_users_argument_is_not_a_list_of_User_instances(self):
        """testing if a TypeError will be raised when the users argument is not
        a list of Users
        """
        self.kwargs['name'] = 'New Project Name'
        self.kwargs['users'] = ['not a list of User instances']
        from stalker import Project
        with pytest.raises(TypeError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'ProjectUser.user should be a stalker.models.auth.User ' \
            'instance, not str'

    def test_users_attribute_is_set_to_a_value_which_is_not_a_list_of_User_instances(self):
        """testing if a TypeError will be raised when the user attribute is set
        to a value which is not a list of User instances
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.users = ['not a list of Users']

        assert str(cm.value) == \
            'ProjectUser.user should be a stalker.models.auth.User ' \
            'instance, not str'

    def test_users_argument_is_working_properly(self):
        """testing if the users argument value is passed to the users attribute
        properly
        """
        self.kwargs['users'] = [self.test_user1, self.test_user2, self.test_user3]
        from stalker import Project
        new_proj = Project(**self.kwargs)
        assert sorted(self.kwargs['users'], key=lambda x: x.name) == sorted(new_proj.users, key=lambda x: x.name)

    def test_users_attribute_is_working_properly(self):
        """testing if the users attribute is working properly
        """
        users = [self.test_user1, self.test_user2, self.test_user3]
        self.test_project.users = users
        assert sorted(users, key=lambda x: x.name) == sorted(self.test_project.users, key=lambda x: x.name)

    def test_tjp_id_is_working_properly(self):
        """testing if the tjp_id attribute is working properly
        """
        self.test_project.id = 654654
        assert self.test_project.tjp_id == 'Project_654654'

    def test_to_tjp_is_working_properly(self):
        """testing if the to_tjp attribute is working properly
        """
        from jinja2 import Template

        expected_tjp_temp = Template("""
task Project_{{project.id}} "Project_{{project.id}}" {
        
task Sequence_{{sequence1.id}} "Sequence_{{sequence1.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user1.id}}             
}        
task Sequence_{{sequence2.id}} "Sequence_{{sequence2.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user2.id}}             
}        
task Sequence_{{sequence3.id}} "Sequence_{{sequence3.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user3.id}}             
}        
task Sequence_{{sequence4.id}} "Sequence_{{sequence4.id}}" {

    
    
task Task_{{task4.id}} "Task_{{task4.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user4.id}}             
}
task Task_{{task5.id}} "Task_{{task5.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user5.id}}             
}
task Task_{{task6.id}} "Task_{{task6.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user6.id}}             
}
}        
task Sequence_{{sequence5.id}} "Sequence_{{sequence5.id}}" {

    
    
task Task_{{task7.id}} "Task_{{task7.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user7.id}}             
}
task Task_{{task8.id}} "Task_{{task8.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user8.id}}             
}
task Task_{{task9.id}} "Task_{{task9.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user9.id}}             
}
}        
task Sequence_{{sequence6.id}} "Sequence_{{sequence6.id}}" {

    
                        
}        
task Sequence_{{sequence7.id}} "Sequence_{{sequence7.id}}" {

    
                        
}        
task Shot_{{shot1.id}} "Shot_{{shot1.id}}" {

    
    
task Task_{{task10.id}} "Task_{{task10.id}}" {

    
            
            
            effort 10.0h
            allocate User_{{user10.id}}             
}
task Task_{{task11.id}} "Task_{{task11.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user1.id}} , User_{{user2.id}}             
}
task Task_{{task12.id}} "Task_{{task12.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user3.id}} , User_{{user4.id}}             
}
}        
task Shot_{{shot2.id}} "Shot_{{shot2.id}}" {

    
    
task Task_{{task13.id}} "Task_{{task13.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user5.id}} , User_{{user6.id}}             
}
task Task_{{task14.id}} "Task_{{task14.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user7.id}} , User_{{user8.id}}             
}
task Task_{{task15.id}} "Task_{{task15.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user9.id}} , User_{{user10.id}}             
}
}        
task Shot_{{shot3.id}} "Shot_{{shot3.id}}" {

    
    
task Task_{{task16.id}} "Task_{{task16.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user1.id}} , User_{{user2.id}} , User_{{user3.id}}             
}
task Task_{{task17.id}} "Task_{{task17.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user4.id}} , User_{{user5.id}} , User_{{user6.id}}             
}
task Task_{{task18.id}} "Task_{{task18.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user7.id}} , User_{{user8.id}} , User_{{user9.id}}             
}
}        
task Shot_{{shot4.id}} "Shot_{{shot4.id}}" {

    
    
task Task_{{task19.id}} "Task_{{task19.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user1.id}} , User_{{user2.id}} , User_{{user10.id}}             
}
task Task_{{task20.id}} "Task_{{task20.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user3.id}} , User_{{user4.id}} , User_{{user5.id}}             
}
task Task_{{task21.id}} "Task_{{task21.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user6.id}} , User_{{user7.id}} , User_{{user8.id}}             
}
}        
task Asset_{{asset1.id}} "Asset_{{asset1.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user2.id}}             
}        
task Asset_{{asset2.id}} "Asset_{{asset2.id}}" {

    
                        
}        
task Asset_{{asset3.id}} "Asset_{{asset3.id}}" {

    
                        
}        
task Asset_{{asset4.id}} "Asset_{{asset4.id}}" {

    
    
task Task_{{task22.id}} "Task_{{task22.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user1.id}} , User_{{user9.id}} , User_{{user10.id}}             
}
task Task_{{task23.id}} "Task_{{task23.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user2.id}} , User_{{user3.id}}             
}
task Task_{{task24.id}} "Task_{{task24.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user4.id}} , User_{{user5.id}}             
}
}        
task Asset_{{asset5.id}} "Asset_{{asset5.id}}" {

    
    
task Task_{{task25.id}} "Task_{{task25.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user6.id}} , User_{{user7.id}}             
}
task Task_{{task26.id}} "Task_{{task26.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user8.id}} , User_{{user9.id}}             
}
task Task_{{task27.id}} "Task_{{task27.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user1.id}} , User_{{user10.id}}             
}
}        
task Task_{{task1.id}} "Task_{{task1.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user1.id}}             
}        
task Task_{{task2.id}} "Task_{{task2.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user2.id}}             
}        
task Task_{{task3.id}} "Task_{{task3.id}}" {

    
            
            
            effort 1.0h
            allocate User_{{user3.id}}             
}}""")
        expected_tjp = expected_tjp_temp.render({
            'project': self.test_project,

            'task1': self.test_task1,
            'task2': self.test_task2,
            'task3': self.test_task3,
            'task4': self.test_task4,
            'task5': self.test_task5,
            'task6': self.test_task6,
            'task7': self.test_task7,
            'task8': self.test_task8,
            'task9': self.test_task9,
            'task10': self.test_task10,
            'task11': self.test_task11,
            'task12': self.test_task12,
            'task13': self.test_task13,
            'task14': self.test_task14,
            'task15': self.test_task15,
            'task16': self.test_task16,
            'task17': self.test_task17,
            'task18': self.test_task18,
            'task19': self.test_task19,
            'task20': self.test_task20,
            'task21': self.test_task21,
            'task22': self.test_task22,
            'task23': self.test_task23,
            'task24': self.test_task24,
            'task25': self.test_task25,
            'task26': self.test_task26,
            'task27': self.test_task27,

            'asset1': self.test_asset1,
            'asset2': self.test_asset2,
            'asset3': self.test_asset3,
            'asset4': self.test_asset4,
            'asset5': self.test_asset5,

            'shot1': self.test_shot1,
            'shot2': self.test_shot2,
            'shot3': self.test_shot3,
            'shot4': self.test_shot4,

            'sequence1': self.test_seq1,
            'sequence2': self.test_seq2,
            'sequence3': self.test_seq3,
            'sequence4': self.test_seq4,
            'sequence5': self.test_seq5,
            'sequence6': self.test_seq6,
            'sequence7': self.test_seq7,

            'user1': self.test_user1,
            'user2': self.test_user2,
            'user3': self.test_user3,
            'user4': self.test_user4,
            'user5': self.test_user5,
            'user6': self.test_user6,
            'user7': self.test_user7,
            'user8': self.test_user8,
            'user9': self.test_user9,
            'user10': self.test_user10,
        })

        # print expected_tjp
        # print "-----------------"
        # print self.test_project.to_tjp
        # self.maxDiff = None

        assert self.test_project.to_tjp == expected_tjp

    def test_active_attribute_is_True_by_default(self):
        """testing if the active attribute is True by default
        """
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.active == True

    def test_is_active_is_read_only(self):
        """testing if the is_active is a read only property
        """
        with pytest.raises(AttributeError) as cm:
            self.test_project.is_active = True

        assert str(cm.value) == "can't set attribute"

    def test_is_active_is_working_properly(self):
        """testing if is_active is working properly
        """
        self.test_project.active = True
        assert self.test_project.is_active is True

        self.test_project.active = False
        assert self.test_project.is_active is False

    def test_total_logged_seconds_attribute_is_read_only(self):
        """testing if the total_logged_seconds attribute is a read-only
        attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_project.total_logged_seconds = 32.3

        assert str(cm.value) == "can't set attribute"

    def test_total_logged_seconds_is_0_for_a_project_with_no_child_tasks(self):
        """testing if the total_logged_seconds
        """
        from stalker import Project
        from stalker.db.session import DBSession
        new_project = Project(**self.kwargs)
        DBSession.add(new_project)
        DBSession.commit()
        assert new_project.total_logged_seconds == 0

    def test_total_logged_seconds_attribute_is_working_properly(self):
        """testing if the total_logged_seconds attribute is working properly
        """
        # create some time logs
        import datetime
        import pytz
        from stalker import TimeLog
        TimeLog(
            task=self.test_task1,
            resource=self.test_task1.resources[0],
            start=datetime.datetime(2013, 8, 1, 1, 0, tzinfo=pytz.utc),
            duration=datetime.timedelta(hours=1)
        )
        from stalker.db.session import DBSession
        DBSession.commit()
        assert self.test_project.total_logged_seconds == 3600

        # add more time logs
        TimeLog(
            task=self.test_seq1,
            resource=self.test_seq1.resources[0],
            start=datetime.datetime(2013, 8, 1, 2, 0, tzinfo=pytz.utc),
            duration=datetime.timedelta(hours=1)
        )
        DBSession.commit()
        assert self.test_project.total_logged_seconds == 7200

        # create more deeper time logs
        TimeLog(
            task=self.test_task10,
            resource=self.test_task10.resources[0],
            start=datetime.datetime(2013, 8, 1, 3, 0, tzinfo=pytz.utc),
            duration=datetime.timedelta(hours=3)
        )
        DBSession.commit()
        assert self.test_project.total_logged_seconds == 18000

        # create a time log for one asset
        TimeLog(
            task=self.test_asset1,
            resource=self.test_asset1.resources[0],
            start=datetime.datetime(2013, 8, 1, 6, 0, tzinfo=pytz.utc),
            duration=datetime.timedelta(hours=10)
        )
        DBSession.commit()
        assert self.test_project.total_logged_seconds == 15 * 3600

    def test_schedule_seconds_attribute_is_read_only(self):
        """testing if the schedule_seconds is a read-only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_project.schedule_seconds = 3

        assert str(cm.value) == "can't set attribute"

    def test_schedule_seconds_attribute_value_is_0_for_a_project_with_no_tasks(self):
        """testing if the schedule_seconds attribute value is 0 for a project
        with no tasks
        """
        from stalker import Project
        from stalker.db.session import DBSession
        new_project = Project(**self.kwargs)
        DBSession.add(new_project)
        DBSession.commit()
        assert new_project.schedule_seconds == 0

    def test_schedule_seconds_attribute_is_working_properly(self):
        """testing if the schedule_seconds attribute value is gathered from the
        child tasks
        """
        assert self.test_shot1.is_container
        assert self.test_task10.parent == self.test_shot1

        assert self.test_seq1.schedule_seconds == 3600
        assert self.test_seq2.schedule_seconds == 3600
        assert self.test_seq3.schedule_seconds == 3600
        assert self.test_seq4.schedule_seconds == 3 * 3600
        assert self.test_seq5.schedule_seconds == 3 * 3600
        assert self.test_seq6.schedule_seconds == 3600
        assert self.test_seq7.schedule_seconds == 3600

        assert self.test_shot1.schedule_seconds == 12 * 3600
        assert self.test_shot2.schedule_seconds == 3 * 3600
        assert self.test_shot3.schedule_seconds == 3 * 3600
        assert self.test_shot4.schedule_seconds == 3 * 3600

        assert self.test_asset1.schedule_seconds == 3600
        assert self.test_asset2.schedule_seconds == 3600
        assert self.test_asset3.schedule_seconds == 3600
        assert self.test_asset4.schedule_seconds == 3 * 3600
        assert self.test_asset5.schedule_seconds == 3 * 3600

        assert self.test_task1.schedule_seconds == 3600
        assert self.test_task2.schedule_seconds == 3600
        assert self.test_task3.schedule_seconds == 3600
        assert self.test_task4.schedule_seconds == 3600
        assert self.test_task5.schedule_seconds == 3600
        assert self.test_task6.schedule_seconds == 3600
        assert self.test_task7.schedule_seconds == 3600
        assert self.test_task8.schedule_seconds == 3600
        assert self.test_task9.schedule_seconds == 3600
        assert self.test_task10.schedule_seconds == 10 * 3600
        assert self.test_task11.schedule_seconds == 3600
        assert self.test_task12.schedule_seconds == 3600
        assert self.test_task13.schedule_seconds == 3600
        assert self.test_task14.schedule_seconds == 3600
        assert self.test_task15.schedule_seconds == 3600
        assert self.test_task16.schedule_seconds == 3600
        assert self.test_task17.schedule_seconds == 3600
        assert self.test_task18.schedule_seconds == 3600
        assert self.test_task19.schedule_seconds == 3600
        assert self.test_task20.schedule_seconds == 3600
        assert self.test_task21.schedule_seconds == 3600
        assert self.test_task22.schedule_seconds == 3600
        assert self.test_task23.schedule_seconds == 3600
        assert self.test_task24.schedule_seconds == 3600
        assert self.test_task25.schedule_seconds == 3600
        assert self.test_task26.schedule_seconds == 3600
        assert self.test_task27.schedule_seconds == 3600

        assert self.test_project.schedule_seconds == 44 * 3600

    def test_percent_complete_attribute_is_read_only(self):
        """testing if the percent_complete is a read-only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_project.percent_complete = 32.3

        assert str(cm.value) == "can't set attribute"

    def test_percent_complete_is_0_for_a_project_with_no_tasks(self):
        """testing if the percent_complete attribute value is 0 for a project
        with no tasks
        """
        from stalker import Project
        from stalker.db.session import DBSession
        new_project = Project(**self.kwargs)
        DBSession.add(new_project)
        DBSession.commit()
        assert new_project.percent_complete == 0

    def test_percent_complete_attribute_is_working_properly(self):
        """testing if the percent_complete attribute is working properly
        """
        assert self.test_project.percent_complete == 0

        assert self.test_shot1.is_container is True
        assert self.test_task10.parent == self.test_shot1
        assert self.test_task10.schedule_seconds == 36000
        assert self.test_task11.schedule_seconds == 3600
        assert self.test_task12.schedule_seconds == 3600
        assert self.test_shot1.schedule_seconds == 12 * 3600

        # create some time logs
        from stalker import TimeLog

        import datetime
        import pytz
        t = TimeLog(
            task=self.test_task1,
            resource=self.test_task1.resources[0],
            start=datetime.datetime(2013, 8, 1, 1, 0, tzinfo=pytz.utc),
            duration=datetime.timedelta(hours=1)
        )
        from stalker.db.session import DBSession
        DBSession.add(t)
        DBSession.commit()

        assert self.test_project.percent_complete == (1.0 / 44.0 * 100)

    def test_clients_argument_is_skipped(self):
        """testing if the clients attribute will be set to None when the
        clients argument is skipped
        """
        self.kwargs['name'] = 'New Project Name'
        try:
            self.kwargs.pop('clients')
        except KeyError:
            pass
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.clients == []

    def test_clients_argument_is_None(self):
        """testing if the clients argument can be None
        """
        self.kwargs['clients'] = None
        from stalker import Project
        new_project = Project(**self.kwargs)
        assert new_project.clients == []

    def test_clients_attribute_is_set_to_None(self):
        """testing if it a TypeError will be raised when the clients attribute
        is set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.clients = None

        assert str(cm.value) == "'NoneType' object is not iterable"

    def test_clients_argument_is_given_as_something_other_than_a_client(self):
        """testing if a TypeError will be raised when the client argument is
        given as something other than a Client object
        """
        self.kwargs["clients"] = "a user"
        from stalker import Project
        with pytest.raises(TypeError) as cm:
            Project(**self.kwargs)

        assert str(cm.value) == \
            'ProjectClient.client should be an instance of ' \
            'stalker.models.auth.Client not str'

    def test_clients_attribute_is_not_a_client_instance(self):
        """testing if a TypeError will be raised when the client attribute is
        set to a value other than a Client instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_project.clients = "a user"

        assert str(cm.value) == \
            'ProjectClient.client should be an instance of ' \
            'stalker.models.auth.Client not str'

    # def test_client_argument_is_working_properly(self):
    #     """testing if the client argument value is correctly passed to the
    #     client attribute
    #     """
    #     assert self.test_project.client == self.kwargs['client']

    def test_clients_attribute_is_working_properly(self):
        """testing if the clients attribute value can be updated correctly
        """
        from stalker import Client
        new_client = Client(name='New Client')
        assert self.test_project.clients != [new_client]
        self.test_project.clients = [new_client]
        assert self.test_project.clients == [new_client]


class ProjectTicketsTestDBCase(UnitTestDBBase):
    """tests the Project <-> Ticket relation
    """

    def setUp(self):
        """setup the test
        """
        super(ProjectTicketsTestDBCase, self).setUp()

        # create test objects
        import datetime
        import pytz
        self.start = datetime.datetime(2016, 11, 17, tzinfo=pytz.utc)
        self.end = self.start + datetime.timedelta(days=20)

        from stalker import User
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

        from stalker import ImageFormat
        self.test_image_format = ImageFormat(
            name="HD",
            width=1920,
            height=1080,
        )

        # type for project
        from stalker import Type
        self.test_project_type = Type(
            name="Project Type 1",
            code='projt1',
            target_entity_type='Project'
        )

        self.test_project_type2 = Type(
            name="Project Type 2",
            code='projt2',
            target_entity_type='Project'
        )

        # type for structure
        self.test_structure_type1 = Type(
            name="Structure Type 1",
            code='struct1',
            target_entity_type='Structure'
        )

        self.test_structure_type2 = Type(
            name="Structure Type 2",
            code='struct2',
            target_entity_type='Structure'
        )

        from stalker import Structure
        self.test_project_structure = Structure(
            name="Project Structure 1",
            type=self.test_structure_type1,
        )

        self.test_project_structure2 = Structure(
            name="Project Structure 2",
            type=self.test_structure_type2,
        )

        from stalker import Repository
        self.test_repo = Repository(
            name="Commercials Repository",
            code="CR",
        )

        # create a project object
        self.kwargs = {
            "name": "Test Project",
            'code': 'tp',
            "description": "This is a project object for testing purposes",
            "image_format": self.test_image_format,
            "fps": 25,
            "type": self.test_project_type,
            "structure": self.test_project_structure,
            "repository": self.test_repo,
            "is_stereoscopic": False,
            "display_width": 15,
            "start": self.start,
            "end": self.end,
        }

        from stalker import Project
        self.test_project = Project(**self.kwargs)

        # *********************************************************************
        # Tickets
        # *********************************************************************

        # no need to create status list for tickets cause we have a database
        # set up an running so it will be automatically linked

        # tickets for version1
        from stalker import Ticket
        self.test_ticket1 = Ticket(
            project=self.test_project
        )
        from stalker.db.session import DBSession
        DBSession.add(self.test_ticket1)
        # set it to closed
        self.test_ticket1.resolve()
        DBSession.commit()

        # create a new ticket and leave it open
        self.test_ticket2 = Ticket(
            project=self.test_project
        )
        DBSession.add(self.test_ticket2)
        DBSession.commit()

        # create a new ticket and close and then reopen it
        self.test_ticket3 = Ticket(
            project=self.test_project
        )
        DBSession.add(self.test_ticket3)
        self.test_ticket3.resolve()
        self.test_ticket3.reopen()
        DBSession.commit()

        # *********************************************************************
        # tickets for version2
        # create a new ticket and leave it open
        self.test_ticket4 = Ticket(
            project=self.test_project
        )
        DBSession.add(self.test_ticket4)
        DBSession.commit()

        # create a new Ticket and close it
        self.test_ticket5 = Ticket(
            project=self.test_project
        )
        DBSession.add(self.test_ticket5)
        self.test_ticket5.resolve()
        DBSession.commit()

        # create a new Ticket and close it
        self.test_ticket6 = Ticket(
            project=self.test_project
        )
        DBSession.add(self.test_ticket6)
        self.test_ticket6.resolve()
        DBSession.commit()

        # *********************************************************************
        # tickets for version3
        # create a new ticket and close it
        self.test_ticket7 = Ticket(
            project=self.test_project
        )
        DBSession.add(self.test_ticket7)
        self.test_ticket7.resolve()
        DBSession.commit()

        # create a new ticket and close it
        self.test_ticket8 = Ticket(
            project=self.test_project
        )
        DBSession.add(self.test_ticket8)
        self.test_ticket8.resolve()
        DBSession.commit()

        # *********************************************************************
        # tickets for version4
        # create a new ticket and close it
        self.test_ticket9 = Ticket(
            project=self.test_project
        )
        DBSession.add(self.test_ticket9)

        self.test_ticket9.resolve()
        DBSession.commit()

        # *********************************************************************

        DBSession.add(self.test_project)
        DBSession.commit()

    def test_tickets_attribute_is_an_empty_list_by_default(self):
        """testing if the Project.tickets is an empty list by default
        """
        from stalker import Project
        project1 = Project(**self.kwargs)
        assert project1.tickets == []

    def test_open_tickets_attribute_is_an_empty_list_by_default(self):
        """testing if the Project.open_tickets is an empty list by default
        """
        from stalker import Project
        project1 = Project(**self.kwargs)
        from stalker.db.session import DBSession
        DBSession.add(project1)
        DBSession.commit()
        assert project1.open_tickets == []

    def test_open_tickets_attribute_is_read_only(self):
        """testing if the Project.open_tickets attribute is a read only
        attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_project.open_tickets = []
        assert str(cm.value) == "can't set attribute"

    def test_tickets_attribute_returns_all_tickets_in_this_project(self):
        """testing if Project.tickets returns all the tickets in this project
        """
        # there should be tickets in this project already
        assert self.test_project.tickets != []

        # now we should have some tickets
        assert len(self.test_project.tickets) > 0

        # now check for exact items
        assert \
            sorted(self.test_project.tickets, key=lambda x: x.name) == \
            sorted([
                self.test_ticket1, self.test_ticket2, self.test_ticket3,
                self.test_ticket4, self.test_ticket5, self.test_ticket6,
                self.test_ticket7, self.test_ticket8, self.test_ticket9
            ], key=lambda x: x.name)

    def test_open_tickets_attribute_returns_all_open_tickets_owned_by_this_user(self):
        """testing if User.open_tickets returns all the open tickets owned by
        this user
        """
        # there should be tickets in this project already
        assert self.test_project.open_tickets != []

        # assign the user to some tickets
        self.test_ticket1.reopen(self.test_user1)
        self.test_ticket2.reopen(self.test_user1)
        self.test_ticket3.reopen(self.test_user1)
        self.test_ticket4.reopen(self.test_user1)
        self.test_ticket5.reopen(self.test_user1)
        self.test_ticket6.reopen(self.test_user1)
        self.test_ticket7.reopen(self.test_user1)
        self.test_ticket8.reopen(self.test_user1)

        # be careful not all of these are open tickets
        self.test_ticket1.reassign(self.test_user1, self.test_user1)
        self.test_ticket2.reassign(self.test_user1, self.test_user1)
        self.test_ticket3.reassign(self.test_user1, self.test_user1)
        self.test_ticket4.reassign(self.test_user1, self.test_user1)
        self.test_ticket5.reassign(self.test_user1, self.test_user1)
        self.test_ticket6.reassign(self.test_user1, self.test_user1)
        self.test_ticket7.reassign(self.test_user1, self.test_user1)
        self.test_ticket8.reassign(self.test_user1, self.test_user1)

        # now we should have some open tickets
        assert len(self.test_project.open_tickets) > 0

        # now check for exact items
        assert \
            sorted(self.test_project.open_tickets, key=lambda x: x.name) == \
            sorted([
                self.test_ticket1,
                self.test_ticket2,
                self.test_ticket3,
                self.test_ticket4,
                self.test_ticket5,
                self.test_ticket6,
                self.test_ticket7,
                self.test_ticket8
            ], key=lambda x: x.name)

        # close a couple of them
        from stalker.models.ticket import (FIXED, CANTFIX, INVALID)

        self.test_ticket1.resolve(self.test_user1, FIXED)
        self.test_ticket2.resolve(self.test_user1, INVALID)
        self.test_ticket3.resolve(self.test_user1, CANTFIX)

        # new check again
        assert \
            sorted(self.test_project.open_tickets, key=lambda x: x.name) ==\
            sorted([
                self.test_ticket4,
                self.test_ticket5,
                self.test_ticket6,
                self.test_ticket7,
                self.test_ticket8
            ], key=lambda x: x.name)
