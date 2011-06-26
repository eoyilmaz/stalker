#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import (Asset, Task, Entity, Project, Link, Status,
                                 StatusList, Shot, Type)
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
        
        self.mock_type1 = self.mocker.mock(Type)
        self.mock_type2 = self.mocker.mock(Type)
        
        self.expect(self.mock_type1.__eq__(self.mock_type2)).result(False).\
            count(0, None)
        
        self.expect(self.mock_type2.__eq__(self.mock_type1)).result(False).\
            count(0, None)
        
        self.expect(self.mock_type1.__ne__(self.mock_type2)).result(True).\
            count(0, None)
        
        self.expect(self.mock_type2.__ne__(self.mock_type1)).result(True).\
            count(0, None)
        
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
    def test_test_setup(self):
        """testing if the test setup is correct
        """
        self.assertFalse(self.mock_type1==self.mock_type2)
        self.assertTrue(self.mock_type1!=self.mock_type2)
    
    
    
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
        
        link_type_1 = Type(name="Image", target_entity_type="Link")
        
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
        
        project_status_list = StatusList(
            name="Project Statuses", statuses=[status1],
            target_entity_type=Project.entity_type
        )
        
        project_type = Type(name="Commercial", target_entity_type=Project)
        
        new_project = Project(name="Commercial",
                              status_list=project_status_list,
                              type=project_type)
        
        task1 = Task(name="Modeling", status=0, status_list=task_status_list,
                     project=new_project)
        task2 = Task(name="Lighting", status=0, status_list=task_status_list,
                     project=new_project)
        
        tasks = [task1, task2]
        
        self.kwargs["code"] = "SH12314"
        self.kwargs["tasks"] = tasks
        
        new_asset = Asset(**self.kwargs)
        
        self.assertEqual(new_asset.tasks, tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_ProjectMixin_initialization(self):
        """testing if the ProjectMixin part is initialized correctly
        """
        
        status1 = Status(name="On Hold", code="OH")
        
        project_status_list = StatusList(
            name="Project Statuses", statuses=[status1],
            target_entity_type=Project.entity_type
        )
        
        project_type = Type(name="Commercial", target_entity_type=Project)
        
        new_project = Project(name="Test Project", status=0,
                              status_list=project_status_list,
                              type=project_type)
        
        self.kwargs["project"] = new_project
        
        new_asset = Asset(**self.kwargs)
        
        self.assertEqual(new_asset.project, new_project)
    
    
    
    #----------------------------------------------------------------------
    def test_plural_name(self):
        """testing the default plural name of the Asset class
        """
        
        self.assertEqual(Asset.plural_name, "Assets")
    
    
    
    #----------------------------------------------------------------------
    def test___strictly_typed___is_True(self):
        """testing if the __strictly_typed__ class attribute is True
        """
        
        self.assertEqual(Asset.__strictly_typed__, True)
    
    