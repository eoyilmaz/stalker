#-*- coding: utf-8 -*-



import unittest
import datetime

from stalker.core.mixins import ProjectMixin
from stalker.core.models import (Status, StatusList, Type, Project, Repository)
from stalker.ext.validatedList import ValidatedList






########################################################################
class ProjectMixinTester(unittest.TestCase):
    """Tests the ProjectMixin
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
            "project": self.test_project1,
        }
        
        class BarClass(object):
            def __init__(self, **kwargs):
                pass
        
        class FooMixedInClass(BarClass, ProjectMixin):
            def __init__(self, **kwargs):
                super(FooMixedInClass, self).__init__(**kwargs)
                ProjectMixin.__init__(self, **kwargs)
        
        self.FooMixedInClass = FooMixedInClass
        
        self.test_foo_obj = FooMixedInClass(**self.kwargs)
    
    
    
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
        #self.assertRaises(TypeError, setattr, self.test_foo_obj, "project",
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
        #self.assertRaises(TypeError, setattr, self.test_foo_obj, "project",
                          #"a project")
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_attribute_is_working_properly(self):
        #"""testing if the project attribute is working properly
        #"""
        #self.test_foo_obj.project = self.test_project2
        #self.assertEqual(self.test_foo_obj.project, self.test_project2)
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_read_only(self):
        """testing if the project attribute is read only
        """
        
        self.assertRaises(AttributeError, setattr, self.test_foo_obj,
                          "project", self.test_project2)
    
    
    