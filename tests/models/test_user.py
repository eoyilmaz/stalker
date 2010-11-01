#-*- coding: utf-8 -*-



import mocker
from stalker.models import user, department, group, task, project, sequence






########################################################################
class UserTest(mocker.MockerTestCase):
    """Testing the user class and attributes
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # need to have some mock object for
        assert(isinstance(self.mocker, mocker.Mocker))
        
        # a department
        self.mock_department = self.mocker.mock(department.Department)
        
        # a group
        self.mock_group = self.mocker.mock(group.Group)
        
        # a task
        self.mock_task = self.mocker.mock(task.Task)
        
        # a project
        self.mock_project = self.mocker.mock(project.Project)
        
        # a sequence
        self.mock_sequence = self.mocker.mock(sequence.Sequence)
        
        self.mocker.replay()
    
    
    
    
    
    