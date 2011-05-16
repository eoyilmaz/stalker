#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import (Asset, AssetType, Task, Entity, Project, Link,
                                 LinkType, Status, StatusList, Shot)
from stalker.ext.validatedList import ValidatedList






########################################################################
class AssetTester(mocker.MockerTestCase):
    """tests Asset class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.mock_project = self.mocker.mock(Project)
        
        self.mock_type1 = self.mocker.mock(AssetType)
        self.mock_type2 = self.mocker.mock(AssetType)
        
        self.mock_task1 = self.mocker.mock(Task)
        self.mock_task2 = self.mocker.mock(Task)
        self.mock_task3 = self.mocker.mock(Task)
        
        self.mock_status1 = self.mocker.mock(Status)
        self.mock_status2 = self.mocker.mock(Status)
        self.mock_status3 = self.mocker.mock(Status)
        
        self.mock_status_list1 = self.mocker.mock(StatusList)
        
        self.expect(self.mock_status_list1.target_entity_type).\
            result(Asset.entity_type).count(0, None)
        self.expect(self.mock_status_list1.statuses).result(
            [self.mock_status1, self.mock_status2, self.mock_status3]).\
            count(0, None)
        
        self.mock_shot1 = self.mocker.mock(Shot)
        self.mock_shot2 = self.mocker.mock(Shot)
        self.mock_shot3 = self.mocker.mock(Shot)
        
        self.mocker.replay()
        
        self.kwargs = {
            "name": "Test Asset",
            "description": "This is a test Asset object",
            "project": self.mock_project,
            "type": self.mock_type1,
            "tasks": [self.mock_task1, self.mock_task2, self.mock_task3],
            "status": 0,
            "status_list": self.mock_status_list1,
        }
        
        self.mock_asset = Asset(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_argument_is_not_instance_of_Project(self):
        """testing if a ValueError will be raised when the project argument is
        not an instance of Project
        """
        
        test_values = [None, "a project", 1, 1.2, ["a", "project"],
                       {"a": "project"}]
        
        for test_value in test_values:
            self.kwargs["project"] = test_value
            self.assertRaises(ValueError, Asset, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_read_only(self):
        """testing if the project attribute is read-only
        """
        
        self.assertRaises(ValueError, setattr, self.mock_asset, "project",
                          None)
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_working_properly(self):
        """testing if the project attribute is working properly
        """
        
        self.assertIsInstance(self.mock_asset.project, Project)
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_None(self):
        """testing if a ValueError will be raised when the type argument is
        given as None
        """
        
        self.kwargs["type"] = None
        self.assertRaises(ValueError, Asset, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_set_to_None(self):
        """testing a ValueError will be raised when the type attribute is set
        to None
        """
        
        self.assertRaises(ValueError, setattr, self.mock_asset, "type", None)
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_not_AssetType_instance(self):
        """testing if a ValueError will be raised when the type argument is not
        an instance of AssetType
        """
        
        test_values = [1, 1.2, "a str", ["a", "str"]]
        
        for test_value in test_values:
            self.kwargs["type"] = test_value
            self.assertRaises(ValueError, Asset, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_not_AssetType_instance(self):
        """testing if a ValueError will be raised when the type attribute is
        tried to be set to something other than a AssetType instance
        """
        
        test_values = [1, 1.2, "a str", ["a", "str"]]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_asset,
                "type",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_working_properly(self):
        """testing if the type attribute is working properly
        """
        
        self.mock_asset.type = self.mock_type2
        self.assertEqual(self.mock_asset.type, self.mock_type2)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality of two Asset objects
        """
        
        new_asset1 = Asset(**self.kwargs)
        new_asset2 = Asset(**self.kwargs)
        
        new_entity1 = Entity(**self.kwargs)
        
        self.kwargs["type"] = self.mock_type2
        new_asset3 = Asset(**self.kwargs)
        
        self.kwargs["name"] = "another name"
        new_asset4 = Asset(**self.kwargs)
        
        self.assertTrue(new_asset1==new_asset2)
        self.assertFalse(new_asset1==new_asset3)
        self.assertFalse(new_asset1==new_asset4)
        self.assertFalse(new_asset3==new_asset4)
        self.assertFalse(new_asset1==new_entity1)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality of two Asset objects
        """
        
        new_asset1 = Asset(**self.kwargs)
        new_asset2 = Asset(**self.kwargs)
        
        new_entity1 = Entity(**self.kwargs)
        
        self.kwargs["type"] = self.mock_type2
        new_asset3 = Asset(**self.kwargs)
        
        self.kwargs["name"] = "another name"
        new_asset4 = Asset(**self.kwargs)
        
        self.assertFalse(new_asset1!=new_asset2)
        self.assertTrue(new_asset1!=new_asset3)
        self.assertTrue(new_asset1!=new_asset4)
        self.assertTrue(new_asset3!=new_asset4)
        self.assertTrue(new_asset1!=new_entity1)
    
    
    
    #----------------------------------------------------------------------
    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """
        
        link_type_1 = LinkType(name="Image")
        
        link1 = Link(name="Artwork 1", path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="a.jpg", type=link_type_1)
        
        link2 = Link(name="Artwork 2", path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="b.jbg", type=link_type_1)
        
        references = [link1, link2]
        
        self.kwargs["code"] = "SH12314"
        self.kwargs["references"] = references
        
        new_asset = Asset(**self.kwargs)
        
        self.assertEqual(new_asset.references, references)
    
    
    
    #----------------------------------------------------------------------
    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """
        
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Complete", code="CMPLT")
        
        status_list = StatusList(name="Project Statuses",
                                 statuses=[status1, status2],
                                 target_entity_type=Asset.entity_type)
        
        self.kwargs["code"] = "SH12314"
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list
        
        new_asset = Asset(**self.kwargs)
        
        self.assertEqual(new_asset.status_list, status_list)
    
    
     
    #----------------------------------------------------------------------
    def test_TaskMixin_initialization(self):
        """testing if the TaskMixin part is initialized correctly
        """
        
        status1 = Status(name="On Hold", code="OH")
        
        task_status_list = StatusList(name="Task Statuses",
                                      statuses=[status1],
                                      target_entity_type=Task.entity_type)
        
        task1 = Task(name="Modeling", status=0, status_list=task_status_list)
        task2 = Task(name="Lighting", status=0, status_list=task_status_list)
        
        tasks = [task1, task2]
        
        self.kwargs["code"] = "SH12314"
        self.kwargs["tasks"] = tasks
        
        new_asset = Asset(**self.kwargs)
        
        self.assertEqual(new_asset.tasks, tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_is_working_properly(self):
        """testing if the shots attribute is working properly
        """
        
        shots_list = [self.mock_shot1, self.mock_shot2,
                                 self.mock_shot3]
        self.mock_asset.shots = shots_list
        self.assertEqual(self.mock_asset.shots, shots_list)
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_only_accepts_list_of_Shot_instances_list_part(self):
        """testing if the shots attribute accepts only lists of Shot instances
        """
        
        test_values = [1, 1.2, "a shot list"]
        
        for test_value in test_values:
            self.assertRaises(ValueError, setattr, self.mock_asset, "shots",
                              test_value)
        
        # now test with proper values
        shots_list = [self.mock_shot1, self.mock_shot2,
                                 self.mock_shot3]
        
        # should not raise any error
        self.mock_asset.shots = shots_list
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_accepts_only_list_of_Shot_instances(self):
        """testing if the shot attribute accepts only lists of Shot instances
        """
        
        test_value = ["a", "list", "of", "others", 1, 1.2]
        
        self.assertRaises(ValueError, setattr, self.mock_asset, "shots",
                          test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_elements_tried_to_be_changed_to_other_than_Shot(self):
        """testing if a ValueError will be raised when the individual elements
        are tried to be changed
        """
        
        test_values = [1, 1.2, "a shot list", ["a", "list", "of", "others"]]
        
        # test append
        for test_value in test_values:
            self.assertRaises(ValueError, self.mock_asset.shots.append,
                              test_value)
        
        # test setitem
        self.mock_asset.shots = [self.mock_shot1, self.mock_shot2]
        for test_value in test_values:
            self.assertRaises(ValueError, self.mock_asset.shots.__setitem__,
                              0, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_is_instance_of_ValidatedList(self):
        """testing if the shots attribute is instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_asset.shots, ValidatedList)
    