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
    """tests Asset class    """    

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


        # TODO: this test should be in tests.db
        # because the property it is testing is using DBSession.query
        #
        #def test_asset_appends_itself_to_the_assets_list_of_project_instance(self):
        #"""testing if the created Asset instance will append itself to the
        #assets list of the given Project instance.
        #"""

        #status1 = Status(name="On Hold", code="OH")

        #task_status_list = StatusList(
        #name="Task Statuses",
        #statuses=[status1],
        #target_entity_type=Task
        #)

        #project_status_list = StatusList(
        #name="Project Statuses",
        #statuses=[status1],
        #target_entity_type=Project
        #)

        #commercial_project_type = Type(
        #name="Commercial",
        #code='comm',
        #target_entity_type=Project,
        #)

        #new_project = Project(
        #name="Commercial",
        #type=commercial_project_type,
        #status_list=project_status_list,
        #repository=self.test_data_repository,
        #)

        #character_asset_type = Type(
        #name="Character",
        #code='char',
        #target_entity_type=Asset
        #)

        #asset_status_list = StatusList(
        #name="Asset Status List",
        #statuses=[status1],
        #target_entity_type=Asset
        #)

        #new_asset = Asset(
        #   name="test asset",
        #   type=character_asset_type,
        #   code="tstasset",
        #   status_list=asset_status_list,
        #   project=new_project,
        #)

        #task1 = Task(
        #   name="Modeling",
        #   status_list=task_status_list,
        #   parent=new_asset
        #)

        #task2 = Task(
        #   name="Lighting",
        #   status_list=task_status_list,
        #   parent=new_asset
        #)

        #self.assertIn(new_asset, new_project.assets)

    def test_plural_class_name(self):
        """testing the default plural name of the Asset class
        """
        self.assertEqual(self.test_data_test_asset.plural_class_name, "Assets")

    def test___strictly_typed___is_True(self):
        """testing if the __strictly_typed__ class attribute is True
        """

        self.assertEqual(Asset.__strictly_typed__, True)

#    def test_shots_argument_is_skipped(self):
#        """testing if the shots attribute will be an empty list when the shots
#        argument is skipped
#        """
#        self.kwargs.pop("shots")
#        new_asset = Asset(**self.kwargs)
#        self.assertEqual(new_asset.shots, [])
#
#    def test_shots_argument_is_None(self):
#        """testing if the shots attribute will be an empty list when the shots
#        argument is None
#        """
#        self.kwargs["shots"] = None
#        new_asset = Asset(**self.kwargs)
#        self.assertEqual(new_asset.shots, [])
#
#    def test_shots_attribute_is_None(self):
#        """testing if a TypeError will be raised when the shots attribute is
#        set to None
#        """
#        self.assertRaises(TypeError, setattr, self.test_data_test_asset,
#                          "shots", None)
#
#    def test_shots_argument_is_not_a_list(self):
#        """testing if a TypeError will be raised when the shots argument is not
#        a list
#        """
#        self.kwargs["shots"] = "1"
#        self.assertRaises(TypeError, Asset, **self.kwargs)
#
#    def test_shots_attribute_is_not_a_list(self):
#        """testing if a TypeError will be raised when the shots attribute is
#        set to a value other than a list
#        """
#        self.assertRaises(TypeError, setattr, self.test_data_test_asset,
#                          "shots", "1")
#
#    def test_shots_argument_is_not_a_list_of_Shots(self):
#        """testing if a TypeError will be raised when the shots argument is not
#        a list of Shot instances
#        """
#        self.kwargs["shots"] = [1, 1.2, "a shot"]
#        self.assertRaises(TypeError, Asset, **self.kwargs)
#
#    def test_shots_attribute_is_not_a_list_of_Shots(self):
#        """testing if a TypeError will be raised when the shots attribute is
#        set to a value other than a list of Shot instances
#        """
#        self.assertRaises(TypeError, setattr, self.test_data_test_asset,
#                          "shots", [1, 1.2, "a shot"])
#
#    def test_shots_argument_is_a_list_of_Shot_instances(self):
#        """testing if the assets attribute of the Shot instances will be
#        updated and have the current asset in their assets list when the shots
#        argument is a list of Shot instances
#        """
#
#        self.kwargs["shots"] = [self.test_data_shot1,
#                                self.test_data_shot2]
#
#        new_asset = Asset(**self.kwargs)
#
#        self.assertIn(new_asset, self.test_data_shot1.assets)
#        self.assertIn(new_asset, self.test_data_shot2.assets)
#
#    def test_shots_attribute_is_a_list_of_Shot_instances(self):
#        """testing if the assets attribute of the Shot instances will be
#        updated and have the current asset in their assets list when the shots
#        attribute is a list of Shot instances
#        """
#
#        self.kwargs["name"] = "New Test Asset"
#        self.kwargs["shots"] = [self.test_data_shot1,
#                                self.test_data_shot2]
#
#        #print "creating new asset"
#        new_asset = Asset(**self.kwargs)
#
#        #print "appending new shots"
#        new_asset.shots = [self.test_data_shot3,
#                           self.test_data_shot4]
#
#        self.assertIn(new_asset, self.test_data_shot3.assets)
#        self.assertIn(new_asset, self.test_data_shot4.assets)
#
#        self.assertNotIn(new_asset, self.test_data_shot1.assets)
#        self.assertNotIn(new_asset, self.test_data_shot2.assets)
#
#    def test_shots_attribute_will_update_the_backreference_value_assets_in_Shot_instances(self):
#        """testing if the shots attribute will update the backreference
#        attribute in Shot instances
#        """
#
#        self.kwargs["name"] = "New Test Asset"
#        self.kwargs["shots"] = [self.test_data_shot1, self.test_data_shot2]
#
#        new_asset = Asset(**self.kwargs)
#
#        # append
#        new_asset.shots.append(self.test_data_shot3)
#        self.assertIn(new_asset, self.test_data_shot3.assets)
#
#        # extend
#        new_asset.shots.extend([self.test_data_shot4])
#        self.assertIn(new_asset, self.test_data_shot4.assets)
#
#        # remove
#        new_asset.shots.remove(self.test_data_shot1)
#        self.assertNotIn(new_asset, self.test_data_shot1.assets)
#
#        # pop
#        new_asset.shots.pop(0)
#        self.assertNotIn(new_asset, self.test_data_shot2.assets)
#
#        # pop again
#        new_asset.shots.pop()
#        self.assertNotIn(new_asset, self.test_data_shot4.assets)
#    
