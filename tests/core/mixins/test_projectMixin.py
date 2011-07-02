#-*- coding: utf-8 -*-



import datetime
import mocker

from stalker.core.mixins import ProjectMixin
from stalker.core.models import Project






########################################################################
class ProjectMixinTester(mocker.MockerTestCase):
    """tests the ProjectMixin
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.mock_project1 = self.mocker.mock(Project)
        self.mock_project2 = self.mocker.mock(Project)
        
        self.mocker.replay()
        
        self.kwargs = {
            "project": self.mock_project1,
        }
        
        class BarClass(object):
            def __init__(self, **kwargs):
                pass
        
        class FooMixedInClass(BarClass, ProjectMixin):
            def __init__(self, **kwargs):
                super(FooMixedInClass, self).__init__(**kwargs)
                ProjectMixin.__init__(self, **kwargs)
        
        self.FooMixedInClass = FooMixedInClass
        
        self.mock_foo_obj = FooMixedInClass(**self.kwargs)
    
    
    
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
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_None(self):
        """testing if a TypeError will be raised when the project attribute is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.mock_foo_obj, "project",
                          None)
    
    
    
    #----------------------------------------------------------------------
    def test_project_argument_is_not_a_Project_instance(self):
        """testing if a TypeError will be raised when the project argument is
        not a stalker.core.models.Project instance
        """
        self.kwargs["project"] = "a project"
        self.assertRaises(TypeError, self.FooMixedInClass, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_not_a_Project_instance(self):
        """testing if a TypeError will be raised when the project attribute is
        set to something other than a stalker.core.models.Project instance
        """
        self.assertRaises(TypeError, setattr, self.mock_foo_obj, "project",
                          "a project")
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_working_properly(self):
        """testing if the project attribute is working properly
        """
        self.mock_foo_obj.project = self.mock_project2
        self.assertEqual(self.mock_foo_obj.project, self.mock_project2)
    
    
    
    