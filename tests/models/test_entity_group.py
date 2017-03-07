# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

import datetime
from stalker.models.entity import EntityGroup
from stalker.testing import UnitTestBase


class EntityGroupTestCase(UnitTestBase):
    """tests EntityGroup class
    """

    def setUp(self):
        """set the test up
        """
        super(EntityGroupTestCase, self).setUp()

        from stalker import (db, defaults, Status, User, StatusList,
                             Repository, Project, Type, Asset, Task)
        # create a couple of task
        self.status_new = Status.query.filter(Status.code == 'NEW').first()
        self.status_wip = Status.query.filter(Status.code == 'WIP').first()
        self.status_cmpl = \
            Status.query.filter(Status.code == 'CMPL').first()

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

        self.asset1 = Asset(
            name='Char1',
            code='char1',
            type=self.char_asset_type,
            project=self.project1,
            responsible=[self.test_user1]
        )

        self.task1 = Task(
            name="Test Task",
            watchers=[self.test_user3],
            parent=self.asset1,
            schedule_timing=5,
            schedule_unit='h',
            bid_timing=52,
            bid_unit='h'
        )

        self.child_task1 = Task(
            name='Child Task 1',
            resources=[self.test_user1, self.test_user2],
            parent=self.task1,
        )

        self.child_task2 = Task(
            name='Child Task 2',
            resources=[self.test_user1, self.test_user2],
            parent=self.task1,
        )

        self.task2 = Task(
            name='Another Task',
            project=self.project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )

        self.entity_group1 = EntityGroup(
            name='My Tasks',
            entities=[
                self.task1, self.child_task2, self.task2
            ]
        )

        db.DBSession.add_all([
            self.task1, self.child_task1, self.child_task2, self.task2,
            self.test_user1, self.test_user2, self.project1, self.status_cmpl,
            self.status_new, self.status_wip, self.asset1
        ])
        db.DBSession.commit()

    def test_entities_argument_is_skipped(self):
        """testing if the entities attribute will be an empty list if the
        entities argument is skipped
        """
        eg = EntityGroup()
        self.assertEqual(eg.entities, [])

    def test_entities_argument_is_None(self):
        """testing if the entities attribute will be an empty list if the
        entities argument is None
        """
        eg = EntityGroup(entities=None)
        self.assertEqual(eg.entities, [])

    def test_entities_argument_is_not_a_list(self):
        """testing if a TypeError will be raised if the entities argument is
        not a list
        """
        with self.assertRaises(TypeError) as cm:
            EntityGroup(entities='not a list of SimpleEntities')

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_entities_argument_is_not_a_list_of_SimpleEntity_instances(self):
        """testing if a TypeError will be raised when the entities argument is
        not a list of SimpleEntity instances
        """
        with self.assertRaises(TypeError) as cm:
            EntityGroup(entities=['not', 1, 'list', 'of', 'SimpleEntities'])

        self.assertEqual(
            str(cm.exception),
            'EntityGroup.entities should be a list of SimpleEntities, not str'
        )

    def test_entities_argument_is_working_properly(self):
        """testing if the entities argument value is correctly passed to the
        entities attribute
        """
        test_value = [self.project1, self.asset1, self.status_cmpl]
        eg = EntityGroup(
            entities=test_value
        )
        self.assertEqual(eg.entities, test_value)
