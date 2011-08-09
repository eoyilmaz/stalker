#-*- coding: utf-8 -*-



import datetime
import mocker

from stalker.core.mixins import TaskMixin
from stalker.core.models import (Status, StatusList, Task, Type, Project,
                                 Repository)
from stalker.ext.validatedList import ValidatedList






########################################################################
class TaskMixinTester(mocker.MockerTestCase):
    """Tests the TaskMixin
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create a repository
        self.repository_type = Type(
            name="Test Repository Type",
            target_entity_type=Repository
        )
        
        self.test_repository = Repository(
            name="Test Repository",
            type=self.repository_type,
        )
        
        self.mock_project1 = self.mocker.mock(Project)
        self.mock_project2 = self.mocker.mock(Project)
        
        self.mock_task1 = self.mocker.mock(Task)
        self.mock_task2 = self.mocker.mock(Task)
        self.mock_task3 = self.mocker.mock(Task)
        
        self.mocker.replay()
        
        self.kwargs = {
            "project": self.mock_project1,
        }
        
        class BarClass(object):
            def __init__(self, **kwargs):
                pass
        
        class FooMixedInClass(BarClass, TaskMixin):
            def __init__(self, **kwargs):
                super(FooMixedInClass, self).__init__(**kwargs)
                TaskMixin.__init__(self, **kwargs)
        
        self.FooMixedInClass = FooMixedInClass
        
        self.mock_foo_obj = FooMixedInClass(**self.kwargs)
    
    
    
    ##----------------------------------------------------------------------
    #def test_tasks_attribute_is_None(self):
        #"""testing if the tasks attribute will be set to empty list when it is
        #set to None
        #"""
        
        #self.mock_foo_obj.tasks = None
        #self.assertEqual(self.mock_foo_obj.tasks, [])
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_read_only(self):
        """testing if the tasks attribute is read-only
        """
        
        self.assertRaises(AttributeError, setattr, self.mock_foo_obj, "tasks",
                          [])
    
    
    
    ##----------------------------------------------------------------------
    #def test_tasks_attribute_is_not_a_list(self):
        #"""testing if a TypeError will be raised when the tasks attribute is
        #tried to set to a non list object
        #"""
        
        #test_values = [1, 1.2, "a str"]
        
        #for test_value in test_values:
            #self.assertRaises(
                #TypeError,
                #setattr,
                #self.mock_foo_obj,
                #"tasks",
                #test_value
            #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_tasks_attribute_is_set_to_a_list_of_other_objects_than_Task(self):
        #"""testing if a TypeError will be raised when the items in the tasks
        #attribute is not Task instance
        #"""
        
        #test_value = [1, 1.2, "a str", ["a", "list"]]
        #self.assertRaises(
            #TypeError,
            #setattr,
            #self.mock_foo_obj,
            #"tasks",
            #test_value
        #)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_element_attributes_are_set_to_other_object_than_Task(self):
        """testing if a TypeError will be raised when trying to set the
        individual elements in the tasks attribute to other objects than a
        Task instance
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                self.mock_foo_obj.tasks.__setitem__,
                "0",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_instance_of_ValidatedList(self):
        """testing if the tasks attribute is a ValidatedList instance
        """
        
        self.assertIsInstance(self.mock_foo_obj.tasks, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_updates_the_backreference_attribute_called_task_of(self):
        """testing if the tasks attribute updates the back reference attribute
        on the Task, the task_of attribute with the instance
        """
        
        status_wip = Status(name="Work In Progress", code="WIP")
        status_complete = Status(name="Complete", code="CMPLT")
        
        task_statusList = StatusList(
            name="Task Statuses",
            statuses=[status_wip, status_complete],
            target_entity_type=Task
        )
        
        project_statusList = StatusList(
            name="Project Statuses",
            statuses=[status_wip, status_complete],
            target_entity_type=Project,
        )
        
        commercial_project_type = Type(
            name="Commercial",
            target_entity_type=Project
        )
        
        new_project1 = Project(
            name="Test Project 1",
            status_list=project_statusList,
            type=commercial_project_type,
            repository=self.test_repository,
        )
        
        new_project2 = Project(
            name="Test Project 2",
            status_list=project_statusList,
            type=commercial_project_type,
            repository=self.test_repository,
        )
        
        new_task1 = Task(
            name="Test1",
            status_list=task_statusList,
            task_of=new_project2,
        )
        
        new_task2 = Task(
            name="Test2",
            status_list=task_statusList,
            task_of=new_project2,
        )
        
        new_task3 = Task(
            name="Test3",
            status_list=task_statusList,
            task_of=new_project2,
        )
        
        new_task4 = Task(
            name="Test4",
            status_list=task_statusList,
            task_of=new_project2,
        )
        
        #self.mock_foo_obj.tasks = [new_task1, new_task2]
        
        # now check if the task_of of the tasks are also having a reference
        # to the new_project1
        new_project1.tasks.append(new_task1)
        new_project1.tasks.append(new_task2)
        
        self.assertEqual(new_task1.task_of, new_project1)
        self.assertEqual(new_task2.task_of, new_project1)
        
        # now update the tasks with a new list
        new_project1.tasks.append(new_task3)
        new_project1.tasks.append(new_task4)
        
        new_project2.tasks.append(new_task1)
        new_project2.tasks.append(new_task2)
        
        # and check if the previous tasks are disconnected
        self.assertNotEqual(new_task1.task_of, new_project1)
        self.assertNotEqual(new_task2.task_of, new_project1)
        
        self.assertEqual(new_task1.task_of, new_project2)
        self.assertEqual(new_task2.task_of, new_project2)
        
        # check if the new ones has the connection
        self.assertEqual(new_task3.task_of, new_project1)
        self.assertEqual(new_task4.task_of, new_project1)
        
        # now append one of the old ones
        self.mock_foo_obj.tasks.append(new_task1)
        
        # check it
        self.assertEqual(new_task1.task_of, self.mock_foo_obj)
        
        # poping or removing elements should raise RuntimeError
        self.assertRaises(RuntimeError, self.mock_foo_obj.tasks.pop, 0)
        self.assertRaises(RuntimeError, self.mock_foo_obj.tasks.remove,
                          new_task1)
        
        # extend it
        self.mock_foo_obj.tasks.extend([new_task2, new_task4])
        
        self.assertEqual(new_task2.task_of, self.mock_foo_obj)
        self.assertEqual(new_task4.task_of, self.mock_foo_obj)
    
    
    
    #----------------------------------------------------------------------
    def test_project_argument_is_skipped(self):
        """testing if a TypeError will be raised when the project argument is
        skipped
        """
        self.kwargs.pop("project")
        self.assertRaises(TypeError, self.FooMixedInClass, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_argument_is_None(self):
        """testing if a TypeError will be raised when the project argument is
        None
        """
        self.kwargs["project"] = None
        self.assertRaises(TypeError, self.FooMixedInClass, **self.kwargs)
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_attribute_is_None(self):
        #"""testing if a TypeError will be raised when the project attribute is
        #set to None
        #"""
        #self.assertRaises(TypeError, setattr, self.mock_foo_obj, "project",
                          #None)
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_argument_is_not_a_Project_instance(self):
        #"""testing if a TypeError will be raised when the project argument is
        #not a stalker.core.models.Project instance
        #"""
        #self.kwargs["project"] = "a project"
        #self.assertRaises(TypeError, self.FooMixedInClass, **self.kwargs)
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_attribute_is_not_a_Project_instance(self):
        #"""testing if a TypeError will be raised when the project attribute is
        #set to something other than a stalker.core.models.Project instance
        #"""
        #self.assertRaises(TypeError, setattr, self.mock_foo_obj, "project",
                          #"a project")
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_attribute_is_working_properly(self):
        #"""testing if the project attribute is working properly
        #"""
        #self.mock_foo_obj.project = self.mock_project2
        #self.assertEqual(self.mock_foo_obj.project, self.mock_project2)
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_read_only(self):
        """testing if the project attribute is read only
        """
        
        self.assertRaises(AttributeError, setattr, self.mock_foo_obj,
                          "project", self.mock_project2)
    
    
    