# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
from stalker import (TaskableEntity, Project, Repository, Status, StatusList,
                     Task, Type)

class TaskableEntityTester(unittest.TestCase):
    """Tests the TaskableEntity
    """
    
    def setUp(self):
        """setup the test
        """
        # create a repository
        self.repository_type = Type(
            name="Test Repository Type",
            code='test',
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
            code='test',
            target_entity_type=Project,
        )
        
        # create projects
        self.test_project1 = Project(
            name="Test Project 1",
            code='tp1',
            type=self.test_project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )
        
        self.test_project2 = Project(
            name="Test Project 2",
            code='tp2',
            type=self.test_project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )
        
        self.kwargs = {
            "name": "test taskable",
            "project": self.test_project1,
        }
        
        self.test_taskable_entity = TaskableEntity(**self.kwargs)
    
    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for
        TaskableEntity class
        """
        self.assertTrue(TaskableEntity.__auto_name__)
     
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
