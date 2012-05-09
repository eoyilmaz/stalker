# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest

from stalker.models import (Status, StatusList, Task, TaskableEntity,
                                 Project, Repository, Type)


class TaskableEntityTester(unittest.TestCase):
    """Tests the TaskableEntity
    """
    
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
        
        # statuses
        self.status1 = Status(name="Status1", code="STS1")
        self.status2 = Status(name="Status2", code="STS2")
        self.status3 = Status(name="Status3", code="STS3")
        
        # project status list
        self.project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.status1,
                self.status2,
                self.status3,
                ],
            target_entity_type=Project
        )
        
        # project type
        self.test_project_type = Type(
            name="Test Project Type",
            target_entity_type=Project,
        )
        
        # create projects
        self.test_project1 = Project(
            name="Test Project 1",
            type=self.test_project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )
        
        self.test_project2 = Project(
            name="Test Project 2",
            type=self.test_project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )
        
        self.kwargs = {
            "name": "test taskable",
            "project": self.test_project1,
        }
        
        self.test_taskable_entity = TaskableEntity(**self.kwargs)
    
    def test_tasks_element_attributes_are_set_to_other_object_than_Task(self):
        """testing if a TypeError will be raised when trying to set the
        individual elements in the tasks attribute to other objects than a
        Task instance
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                self.test_taskable_entity.tasks.__setitem__,
                "0",
                test_value
            )
    
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
        
        #self.test_foo_obj.tasks = [new_task1, new_task2]
        
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
        self.test_taskable_entity.tasks.append(new_task1)
        
        # check it
        self.assertEqual(new_task1.task_of, self.test_taskable_entity)
        
        # poping or removing elements should raise RuntimeError
        self.assertRaises(TypeError, self.test_taskable_entity.tasks.pop, 0)
        
        # because the test is recovering from the previous error
        # the remove can not be tested
        
        # extend it
        self.test_taskable_entity.tasks.extend([new_task2, new_task4])
        
        self.assertEqual(new_task2.task_of, self.test_taskable_entity)
        self.assertEqual(new_task4.task_of, self.test_taskable_entity)
    
    def test_project_argument_is_skipped(self):
        """testing if a TypeError will be raised when the project argument is
        skipped
        """
        self.kwargs.pop("project")
        self.assertRaises(TypeError, TaskableEntity, **self.kwargs)
    
    def test_project_argument_is_None(self):
        """testing if a TypeError will be raised when the project argument is
        None
        """
        self.kwargs["project"] = None
        self.assertRaises(TypeError, TaskableEntity, **self.kwargs)
