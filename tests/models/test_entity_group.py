# -*- coding: utf-8 -*-

import unittest
import pytest
from stalker.models.entity import EntityGroup


class EntityGroupTestCase(unittest.TestCase):
    """tests EntityGroup class
    """

    def setUp(self):
        """set the test up
        """
        super(EntityGroupTestCase, self).setUp()

        from stalker import (Status, User, StatusList, Repository, Project,
                             Type, Asset, Task)
        # create a couple of task
        self.status_new = Status(name='Mew', code='NEW')
        self.status_wfd = Status(name='Waiting For Dependency', code='WFD')
        self.status_rts = Status(name='Ready To Start', code='RTS')
        self.status_wip = Status(name='Work In Progress', code='WIP')
        self.status_prev = Status(name='Pending Review', code='PREV')
        self.status_hrev = Status(name='Has Revision', code='HREV')
        self.status_drev = Status(name='Dependency Has Revision', code='DREV')
        self.status_cmpl = Status(name='Completed', code='CMPL')

        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@user.com",
            password="1234",
        )

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@user.com",
            password="1234",
        )

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@user.com",
            password="1234",
        )

        self.project_status_list = StatusList(
            name="Project Status List",
            statuses=[self.status_new, self.status_wip, self.status_cmpl],
            target_entity_type="Project",
        )

        self.repo = Repository(
            name='Test Repo',
            code='TR',
            linux_path='/mnt/M/JOBs',
            windows_path='M:/JOBs',
            osx_path='/Users/Shared/Servers/M',
        )

        self.project1 = Project(
            name='Tests Project',
            code='tp',
            status_list=self.project_status_list,
            repository=self.repo,
        )

        self.char_asset_type = Type(
            name='Character Asset',
            code='char',
            target_entity_type="Asset"
        )

        self.task_status_list = StatusList(
            name='Task Statuses',
            statuses=[
                self.status_wfd, self.status_rts, self.status_wip,
                self.status_prev, self.status_hrev, self.status_drev,
                self.status_cmpl
            ],
            target_entity_type='Task'
        )

        self.asset_status_list = StatusList(
            name='Asset Statuses',
            statuses=[
                self.status_wfd, self.status_rts, self.status_wip,
                self.status_prev, self.status_hrev, self.status_drev,
                self.status_cmpl
            ],
            target_entity_type='Asset'
        )

        self.asset1 = Asset(
            name='Char1',
            code='char1',
            type=self.char_asset_type,
            project=self.project1,
            responsible=[self.test_user1],
            status_list=self.asset_status_list
        )

        self.task1 = Task(
            name="Test Task",
            watchers=[self.test_user3],
            parent=self.asset1,
            schedule_timing=5,
            schedule_unit='h',
            bid_timing=52,
            bid_unit='h',
            status_list=self.task_status_list
        )

        self.child_task1 = Task(
            name='Child Task 1',
            resources=[self.test_user1, self.test_user2],
            parent=self.task1,
            status_list=self.task_status_list
        )

        self.child_task2 = Task(
            name='Child Task 2',
            resources=[self.test_user1, self.test_user2],
            parent=self.task1,
            status_list=self.task_status_list
        )

        self.task2 = Task(
            name='Another Task',
            project=self.project1,
            resources=[self.test_user1],
            responsible=[self.test_user2],
            status_list=self.task_status_list
        )

        self.entity_group1 = EntityGroup(
            name='My Tasks',
            entities=[
                self.task1, self.child_task2, self.task2
            ]
        )

    def test_entities_argument_is_skipped(self):
        """testing if the entities attribute will be an empty list if the
        entities argument is skipped
        """
        eg = EntityGroup()
        assert eg.entities == []

    def test_entities_argument_is_None(self):
        """testing if the entities attribute will be an empty list if the
        entities argument is None
        """
        eg = EntityGroup(entities=None)
        assert eg.entities == []

    def test_entities_argument_is_not_a_list(self):
        """testing if a TypeError will be raised if the entities argument is
        not a list
        """
        with pytest.raises(TypeError) as cm:
            EntityGroup(entities='not a list of SimpleEntities')

        assert str(cm.value) == \
            'Incompatible collection type: str is not list-like'

    def test_entities_argument_is_not_a_list_of_SimpleEntity_instances(self):
        """testing if a TypeError will be raised when the entities argument is
        not a list of SimpleEntity instances
        """
        with pytest.raises(TypeError) as cm:
            EntityGroup(entities=['not', 1, 'list', 'of', 'SimpleEntities'])

        assert str(cm.value) == \
            'EntityGroup.entities should be a list of SimpleEntities, not str'

    def test_entities_argument_is_working_properly(self):
        """testing if the entities argument value is correctly passed to the
        entities attribute
        """
        test_value = [self.project1, self.asset1, self.status_cmpl]
        eg = EntityGroup(
            entities=test_value
        )
        assert eg.entities == test_value
