# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import unittest2
from stalker import (Asset, Entity, Project, Repository, Sequence, Status,
                     StatusList, Task, Type, Link, Shot)


class AssetTester(unittest2.TestCase):
    """tests Asset class
    """

    def setUp(self):
        """setup the test
        """
        # statuses
        self.test_data_status_complete = Status(
            name="Complete",
            code="CMPLT",
        )

        self.test_data_status_wip = Status(
            name="Work In Progress",
            code="WIP",
        )

        # status lists
        self.test_data_project_status_list = StatusList(
            name="Project Status List",
            target_entity_type=Project,
            statuses=[
                self.test_data_status_complete,
                self.test_data_status_wip
            ]
        )

        self.test_data_task_status_list = StatusList(
            name="Task Status List",
            target_entity_type=Task,
            statuses=[
                self.test_data_status_complete,
                self.test_data_status_wip
            ]
        )

        self.test_data_asset_status_list = StatusList(
            name="Asset Status List",
            target_entity_type=Asset,
            statuses=[
                self.test_data_status_complete,
                self.test_data_status_wip
            ]
        )

        self.test_data_shot_status_list = StatusList(
            name="Shot Status List",
            target_entity_type=Shot,
            statuses=[
                self.test_data_status_complete,
                self.test_data_status_wip
            ]
        )

        self.test_data_sequence_status_list = StatusList(
            name="Sequence Status List",
            target_entity_type=Sequence,
            statuses=[
                self.test_data_status_complete,
                self.test_data_status_wip
            ]
        )

        # types
        self.test_data_commmercial_project = Type(
            name="Commercial Project",
            code='commproj',
            target_entity_type=Project,
        )

        self.test_data_asset_type1 = Type(
            name="Character",
            code='char',
            target_entity_type=Asset
        )

        self.test_data_asset_type2 = Type(
            name="Environment",
            code='env',
            target_entity_type=Asset
        )

        self.test_data_repository_type = Type(
            name="Test Repository Type",
            code='testrepo',
            target_entity_type=Repository,
        )

        # repository
        self.test_data_repository = Repository(
            name="Test Repository",
            type=self.test_data_repository_type,
        )

        # project
        self.test_data_project1 = Project(
            name="Test Project1",
            code='tp1',
            type=self.test_data_commmercial_project,
            status_list=self.test_data_project_status_list,
            repository=self.test_data_repository,
        )

        # sequence
        self.test_data_sequence = Sequence(
            name="Test Sequence",
            code='tseq',
            project=self.test_data_project1,
            status_list=self.test_data_sequence_status_list,
        )

        # shots
        self.test_data_shot1 = Shot(
            code="TestSH001",
            status_list=self.test_data_shot_status_list,
            project=self.test_data_project1,
            sequences=[self.test_data_sequence],
        )

        self.test_data_shot2 = Shot(
            code="TestSH002",
            status_list=self.test_data_shot_status_list,
            project=self.test_data_project1,
            sequences=[self.test_data_sequence],
        )

        self.test_data_shot3 = Shot(
            code="TestSH003",
            status_list=self.test_data_shot_status_list,
            project=self.test_data_project1,
            sequences=[self.test_data_sequence],
        )

        self.test_data_shot4 = Shot(
            code="TestSH004",
            status_list=self.test_data_shot_status_list,
            project=self.test_data_project1,
            sequences=[self.test_data_sequence],
        )

        self.kwargs = {
            "name": "Test Asset",
            'code': 'ta',
            "description": "This is a test Asset object",
            "project": self.test_data_project1,
            "type": self.test_data_asset_type1,
            "status": 0,
            "status_list": self.test_data_asset_status_list,
        }

        self.test_data_test_asset = Asset(**self.kwargs)

        # tasks
        self.test_data_task1 = Task(
            name="Task1",
            parent=self.test_data_test_asset,
            status_list=self.test_data_task_status_list
        )

        self.test_data_task2 = Task(
            name="Task2",
            parent=self.test_data_test_asset,
            status_list=self.test_data_task_status_list
        )

        self.test_data_task3 = Task(
            name="Task3",
            parent=self.test_data_test_asset,
            status_list=self.test_data_task_status_list
        )

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Asset class
        """
        self.assertFalse(Asset.__auto_name__)

    def test_equality(self):
        """testing equality of two Asset objects
        """

        new_asset1 = Asset(**self.kwargs)
        new_asset2 = Asset(**self.kwargs)

        new_entity1 = Entity(**self.kwargs)

        self.kwargs["type"] = self.test_data_asset_type2
        new_asset3 = Asset(**self.kwargs)

        self.kwargs["name"] = "another name"
        new_asset4 = Asset(**self.kwargs)

        self.assertTrue(new_asset1 == new_asset2)
        self.assertFalse(new_asset1 == new_asset3)
        self.assertFalse(new_asset1 == new_asset4)
        self.assertFalse(new_asset3 == new_asset4)
        self.assertFalse(new_asset1 == new_entity1)

    def test_inequality(self):
        """testing inequality of two Asset objects
        """

        new_asset1 = Asset(**self.kwargs)
        new_asset2 = Asset(**self.kwargs)

        new_entity1 = Entity(**self.kwargs)

        self.kwargs["type"] = self.test_data_asset_type2
        new_asset3 = Asset(**self.kwargs)

        self.kwargs["name"] = "another name"
        new_asset4 = Asset(**self.kwargs)

        self.assertFalse(new_asset1 != new_asset2)
        self.assertTrue(new_asset1 != new_asset3)
        self.assertTrue(new_asset1 != new_asset4)
        self.assertTrue(new_asset3 != new_asset4)
        self.assertTrue(new_asset1 != new_entity1)

    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """

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

        new_asset = Asset(**self.kwargs)

        self.assertEqual(new_asset.references, references)

    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """

        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Complete", code="CMPLT")

        status_list = StatusList(name="Project Statuses",
                                 statuses=[status1, status2],
                                 target_entity_type=Asset)

        self.kwargs["code"] = "SH12314"
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list

        new_asset = Asset(**self.kwargs)

        self.assertEqual(new_asset.status_list, status_list)

    def test_TaskMixin_initialization(self):
        """testing if the TaskMixin part is initialized correctly
        """

        status1 = Status(name="On Hold", code="OH")

        task_status_list = StatusList(
            name="Task Statuses",
            statuses=[status1],
            target_entity_type=Task
        )

        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1],
            target_entity_type=Project,
        )

        commercial_project_type = Type(
            name="Commercial",
            code='comm',
            target_entity_type=Project,
        )

        new_project = Project(
            name="Commercial",
            code='COM',
            type=commercial_project_type,
            status_list=project_status_list,
            repository=self.test_data_repository,
        )

        character_asset_type = Type(
            name="Character",
            code='char',
            target_entity_type=Asset
        )

        asset_status_list = StatusList(
            name="Asset Status List",
            statuses=[status1],
            target_entity_type=Asset
        )

        new_asset = Asset(
            name="test asset",
            type=character_asset_type,
            code="tstasset",
            status_list=asset_status_list,
            project=new_project,
        )

        task1 = Task(
            name="Modeling",
            status_list=task_status_list,
            parent=new_asset
        )

        task2 = Task(
            name="Lighting",
            status_list=task_status_list,
            parent=new_asset
        )

        tasks = [task1, task2]

        self.assertItemsEqual(new_asset.tasks, tasks)

    def test_plural_class_name(self):
        """testing the default plural name of the Asset class
        """
        self.assertEqual(self.test_data_test_asset.plural_class_name, "Assets")

    def test___strictly_typed___is_True(self):
        """testing if the __strictly_typed__ class attribute is True
        """

        self.assertEqual(Asset.__strictly_typed__, True)
