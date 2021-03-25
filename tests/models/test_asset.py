# -*- coding: utf-8 -*-

from stalker.testing import UnitTestDBBase


class AssetTester(UnitTestDBBase):
    """tests Asset class
    """

    def setUp(self):
        """setup the test
        """
        super(AssetTester, self).setUp()

        # users
        from stalker import User
        from stalker.db.session import DBSession
        self.test_user1 = User(
            name='User1',
            login='user1',
            password='12345',
            email='user1@user1.com'
        )
        DBSession.add(self.test_user1)

        self.test_user2 = User(
            name='User2',
            login='user2',
            password='12345',
            email='user2@user2.com'
        )
        DBSession.add(self.test_user2)
        DBSession.commit()

        # statuses
        from stalker import Status, Project
        self.status_wip = Status.query.filter_by(code='WIP').first()
        self.status_cmpl = Status.query.filter_by(code='CMPL').first()

        # types
        from stalker import Type
        self.commercial_project_type = Type(
            name="Commercial Project",
            code='commproj',
            target_entity_type='Project',
        )
        DBSession.add(self.commercial_project_type)

        self.asset_type1 = Type(
            name="Character",
            code='char',
            target_entity_type='Asset'
        )
        DBSession.add(self.asset_type1)

        self.asset_type2 = Type(
            name="Environment",
            code='env',
            target_entity_type='Asset'
        )
        DBSession.add(self.asset_type2)

        self.repository_type = Type(
            name="Test Repository Type",
            code='testrepo',
            target_entity_type='Repository',
        )
        DBSession.add(self.repository_type)

        # repository
        from stalker import Repository
        self.repository = Repository(
            name="Test Repository",
            code='TR',
            type=self.repository_type,
        )
        DBSession.add(self.repository)

        # project
        self.project1 = Project(
            name="Test Project1",
            code='tp1',
            type=self.commercial_project_type,
            repositories=[self.repository],
        )
        DBSession.add(self.project1)
        DBSession.commit()

        # sequence
        from stalker import Sequence
        self.seq1 = Sequence(
            name="Test Sequence",
            code='tseq',
            project=self.project1,
            responsible=[self.test_user1]
        )
        DBSession.add(self.seq1)

        # shots
        from stalker import Shot
        self.shot1 = Shot(
            code="TestSH001",
            project=self.project1,
            sequences=[self.seq1],
            responsible=[self.test_user1]
        )
        DBSession.add(self.shot1)

        self.shot2 = Shot(
            code="TestSH002",
            project=self.project1,
            sequences=[self.seq1],
            responsible=[self.test_user1]
        )
        DBSession.add(self.shot2)

        self.shot3 = Shot(
            code="TestSH003",
            project=self.project1,
            sequences=[self.seq1],
            responsible=[self.test_user1]
        )
        DBSession.add(self.shot3)

        self.shot4 = Shot(
            code="TestSH004",
            project=self.project1,
            sequences=[self.seq1],
            responsible=[self.test_user1]
        )
        DBSession.add(self.shot4)

        self.kwargs = {
            "name": "Test Asset",
            'code': 'ta',
            "description": "This is a test Asset object",
            "project": self.project1,
            "type": self.asset_type1,
            "status": 0,
            'responsible': [self.test_user1]
        }

        from stalker import Asset, Task
        self.asset1 = Asset(**self.kwargs)
        DBSession.add(self.asset1)

        # tasks
        self.task1 = Task(
            name="Task1",
            parent=self.asset1,
        )
        DBSession.add(self.task1)

        self.task2 = Task(
            name="Task2",
            parent=self.asset1,
        )
        DBSession.add(self.task2)

        self.task3 = Task(
            name="Task3",
            parent=self.asset1,
        )
        DBSession.add(self.task3)
        DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Asset class
        """
        from stalker import Asset
        assert Asset.__auto_name__ is False

    def test_equality(self):
        """testing equality of two Asset objects
        """
        from stalker import Asset, Entity
        new_asset1 = Asset(**self.kwargs)
        new_asset2 = Asset(**self.kwargs)

        new_entity1 = Entity(**self.kwargs)

        self.kwargs["type"] = self.asset_type2
        new_asset3 = Asset(**self.kwargs)

        self.kwargs["name"] = "another name"
        new_asset4 = Asset(**self.kwargs)

        assert new_asset1 == new_asset2
        assert not new_asset1 == new_asset3
        assert not new_asset1 == new_asset4
        assert not new_asset3 == new_asset4
        assert not new_asset1 == new_entity1

    def test_inequality(self):
        """testing inequality of two Asset objects
        """
        from stalker import Asset, Entity
        new_asset1 = Asset(**self.kwargs)
        new_asset2 = Asset(**self.kwargs)

        new_entity1 = Entity(**self.kwargs)

        self.kwargs["type"] = self.asset_type2
        new_asset3 = Asset(**self.kwargs)

        self.kwargs["name"] = "another name"
        new_asset4 = Asset(**self.kwargs)

        assert not new_asset1 != new_asset2
        assert new_asset1 != new_asset3
        assert new_asset1 != new_asset4
        assert new_asset3 != new_asset4
        assert new_asset1 != new_entity1

    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """
        from stalker import Link, Type
        link_type_1 = Type(
            name="Image",
            code='image',
            target_entity_type="Link"
        )

        link1 = Link(
            name="Artwork 1",
            full_path="/mnt/M/JOBs/TEST_PROJECT",
            filename="a.jpg",
            type=link_type_1
        )

        link2 = Link(
            name="Artwork 2",
            full_path="/mnt/M/JOBs/TEST_PROJECT",
            filename="b.jbg",
            type=link_type_1
        )

        references = [link1, link2]

        self.kwargs["code"] = "SH12314"
        self.kwargs["references"] = references

        from stalker import Asset
        new_asset = Asset(**self.kwargs)

        assert new_asset.references == references

    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """
        from stalker import StatusList, Asset
        status_list = \
            StatusList.query.filter_by(target_entity_type='Asset').first()

        self.kwargs["code"] = "SH12314"
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list

        new_asset = Asset(**self.kwargs)

        assert new_asset.status_list == status_list

    def test_TaskMixin_initialization(self):
        """testing if the TaskMixin part is initialized correctly
        """
        from stalker import Type, Project, Asset, Task
        commercial_project_type = Type(
            name="Commercial",
            code='comm',
            target_entity_type='Project',
        )

        new_project = Project(
            name="Commercial",
            code='COM',
            type=commercial_project_type,
            repository=self.repository,
        )

        character_asset_type = Type(
            name="Character",
            code='char',
            target_entity_type='Asset'
        )

        new_asset = Asset(
            name="test asset",
            type=character_asset_type,
            code="tstasset",
            project=new_project,
            responsible=[self.test_user1]
        )

        task1 = Task(
            name="Modeling",
            parent=new_asset
        )

        task2 = Task(
            name="Lighting",
            parent=new_asset
        )

        tasks = [task1, task2]

        assert \
            sorted(new_asset.tasks, key=lambda x: x.name) == \
            sorted(tasks, key=lambda x: x.name)

    def test_plural_class_name(self):
        """testing the default plural name of the Asset class
        """
        assert self.asset1.plural_class_name == "Assets"

    def test___strictly_typed___is_True(self):
        """testing if the __strictly_typed__ class attribute is True
        """
        from stalker import Asset
        assert Asset.__strictly_typed__ is True
