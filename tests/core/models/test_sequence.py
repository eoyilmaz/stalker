#-*- coding: utf-8 -*-



import datetime
import mocker
from stalker.core.models import (Sequence, Project, User, Shot, Entity, Status,
                                 StatusList, Link, Task, Type)
from stalker.ext.validatedList import ValidatedList






########################################################################
class SequenceTester(mocker.MockerTestCase):
    """Tests Sequence class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create a mock project, user and a couple of shots
        
        self.mock_project = self.mocker.mock(Project)
        self.mock_project2 = self.mocker.mock(Project)
        self.mock_lead = self.mocker.mock(User)
        self.mock_lead2 = self.mocker.mock(User)
        
        self.mock_shot1 = self.mocker.mock(Shot)
        self.mock_shot2 = self.mocker.mock(Shot)
        self.mock_shot3 = self.mocker.mock(Shot)
        
        self.mock_status1 = self.mocker.mock(Status)
        self.mock_status2 = self.mocker.mock(Status)
        self.mock_status3 = self.mocker.mock(Status)
        
        self.mock_status_list1 = self.mocker.mock(StatusList)
        self.expect(self.mock_status_list1.target_entity_type).\
            result(Sequence.entity_type).count(0, None)
        self.expect(self.mock_status_list1.statuses).result(
            [self.mock_status1, self.mock_status2, self.mock_status3]).\
            count(0, None)
        
        self.mocker.replay()
        
        # the parameters
        self.kwargs = {
            "name": "Test Sequence",
            "description": "A test sequence",
            "project": self.mock_project,
            "lead": self.mock_lead,
            "shots": [self.mock_shot1, self.mock_shot2, self.mock_shot3],
            "status_list": self.mock_status_list1
        }
        
        # the mock seuqence
        self.mock_sequence = Sequence(**self.kwargs)
        
        # assign the shots
        self.mock_sequence.shots.append(self.mock_shot1)
        self.mock_sequence.shots.append(self.mock_shot2)
        self.mock_sequence.shots.append(self.mock_shot3)

    
    
    
    ##----------------------------------------------------------------------
    #def test_project_attribute_default_value_is_None(self):
        #"""testing if the project attribute defaults to None when no project
        #argument is given
        #"""
        
        #self.kwargs.pop("project")
        #new_sequence = Sequence(**self.kwargs)
        #self.assertEqual(new_sequence.project, None)
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_argument_is_None(self):
        #"""testing if a TypeError will be raised when the project argument is
        #None
        #"""
        
        #self.kwargs["project"] = None
        #self.assertRaises(TypeError, Sequence, **self.kwargs)
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_attribute_is_set_to_None(self):
        #"""testing if a TypeError will be raised when the project attribute set
        #to None
        #"""
        
        ##self.mock_sequence.project = None
        #self.assertRaises(
            #TypeError,
            #setattr,
            #self.mock_sequence,
            #"project",
            #None
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_argument_other_than_a_Project(self):
        #"""testing if a TypeError will be raised when the project argument is
        #None
        #"""
        
        #test_values = [1, 1.2, "a project", ["a", "list"]]
        
        #for test_value in test_values:
            #self.kwargs["project"] = test_value
            #self.assertRaises(TypeError, Sequence, **self.kwargs)
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_attribute_other_than_a_Project(self):
        #"""testing if a TypeError will be raised when the project attribute
        #is set to None
        #"""
        
        #test_values = [1, 1.2, "project", ["a", "list"]]
        
        #for test_value in test_values:
            #self.assertRaises(
                #TypeError,
                #setattr,
                #self.mock_sequence,
                #"project",
                #test_value
            #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_project_attribute_is_working_properly(self):
        #"""testing if the project attribute is working properly
        #"""
        
        #self.mock_sequence.project = self.mock_project2
        #self.assertEqual(self.mock_sequence.project, self.mock_project2)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_defaults_to_None(self):
        """testing if the lead attribute defualts to None when no lead argument
        is given
        """
        
        self.kwargs.pop("lead")
        new_sequence = Sequence(**self.kwargs)
        self.assertEqual(new_sequence.lead, None)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_None(self):
        """testing if nothing will happen when the lead argument is given as
        None
        """
        
        self.kwargs["lead"] = None
        new_sequence = Sequence(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_None(self):
        """testing if nothing will happen when the lead attribute is set to
        None
        """
        
        self.mock_sequence.lead = None
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_not_User(self):
        """testing if a TypeError will be raised when the lead argument is not
        an instance of User
        """
        
        test_values = [1, 1.2, "a user", ["a", "list", "as", "user"]]
        
        for test_value in test_values:
            self.kwargs["lead"] = test_value
            self.assertRaises(TypeError, Sequence, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_not_User(self):
        """testing if a TypeError will be raised when the lead attribute is
        set to something other than a User
        """
        
        test_values = [1, 1.2, "a user", ["a", "list", "as", "user"]]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_sequence,
                "lead",
                test_value
            )
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_works_properly(self):
        """testing if the lead attribute is working properly
        """
        
        self.mock_sequence.lead = self.mock_lead2
        self.assertEqual(self.mock_sequence.lead, self.mock_lead2)
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_defaults_to_empty_list(self):
        """testing if the shots attribute defaults to an empty list
        """
        
        self.kwargs.pop("shots")
        new_sequence = Sequence(**self.kwargs)
        self.assertEqual(new_sequence.shots, [])
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_is_set_None(self):
        """testing if the shots attribute will be set to an empty list when it
        is set to None
        """
        
        self.mock_sequence.shots = None
        self.assertEqual(self.mock_sequence.shots, [])
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_is_set_to_other_than_a_list(self):
        """testing if a TypeError will be raised when the shots attribute is
        tried to be set to something other than a list
        """
        
        test_values = [1, 1.2, "a string"]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_sequence,
                "shots",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_is_a_list_of_other_objects(self):
        """testing if a TypeError will be raised when the shots argument is a
        list of other type of objects
        """
        
        test_value = [1, 1.2, "a string"]
        self.assertRaises(
            TypeError,
            setattr,
            self.mock_sequence,
            "shots",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_elements_tried_to_be_set_to_non_Shot_object(self):
        """testing if a TypeError will be raised when the individual elements
        in the shots list tried to be set to something other than a Shot
        instance
        """
        
        test_values = [1, 1.2, "a string", ["a", "list"]]
        
        for test_value in test_values:
            self.assertRaises(TypeError,
                              self.mock_sequence.shots.__setitem__,
                              0,
                              test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_is_instance_of_ValidatedList(self):
        """testing if the shots attribute holds an instance of ValidateList
        """
        
        self.assertIsInstance(self.mock_sequence.shots, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality of sequences
        """
        
        
        new_seq1 = Sequence(**self.kwargs)
        new_seq2 = Sequence(**self.kwargs)
        new_entity = Entity(**self.kwargs)
        
        self.kwargs["name"] = "a different sequence"
        new_seq3 = Sequence(**self.kwargs)
        
        self.assertTrue(new_seq1==new_seq2)
        self.assertFalse(new_seq1==new_seq3)
        self.assertFalse(new_seq1==new_entity)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality of sequences
        """
        
        
        new_seq1 = Sequence(**self.kwargs)
        new_seq2 = Sequence(**self.kwargs)
        new_entity = Entity(**self.kwargs)
        
        self.kwargs["name"] = "a different sequence"
        new_seq3 = Sequence(**self.kwargs)
        
        self.assertFalse(new_seq1!=new_seq2)
        self.assertTrue(new_seq1!=new_seq3)
        self.assertTrue(new_seq1!=new_entity)
    
    
    
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
        
        self.kwargs["references"] = references
        
        new_sequence = Sequence(**self.kwargs)
        
        self.assertEqual(new_sequence.references, references)
    
    
    
    #----------------------------------------------------------------------
    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """
        
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Complete", code="CMPLT")
        
        status_list = StatusList(name="Project Statuses",
                                 statuses=[status1, status2],
                                 target_entity_type=Sequence.entity_type)
        
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list
        
        new_sequence = Sequence(**self.kwargs)
        
        self.assertEqual(new_sequence.status_list, status_list)
    
    
    
    #----------------------------------------------------------------------
    def test_ScheduleMixin_initialization(self):
        """testing if the ScheduleMixin part is initialized correctly
        """
        
        start_date = datetime.date.today() + datetime.timedelta(days=25)
        due_date = start_date + datetime.timedelta(days=12)
        
        self.kwargs["start_date"] = start_date
        self.kwargs["due_date"] = due_date
        
        new_sequence = Sequence(**self.kwargs)
        
        self.assertEqual(new_sequence.start_date, start_date)
        self.assertEqual(new_sequence.due_date, due_date)
        self.assertEqual(new_sequence.duration, due_date - start_date)
    
    
    
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
        
        self.kwargs["tasks"] = tasks
        
        new_sequence = Sequence(**self.kwargs)
        
        self.assertEqual(new_sequence.tasks, tasks)
    
    
    
    
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
        
        new_sequence = Sequence(**self.kwargs)
        
        self.assertEqual(new_sequence.project, new_project)
    
    
    
    #----------------------------------------------------------------------
    def test_plural_name(self):
        """testing the plural name of Sequence class
        """
        
        self.assertTrue(Sequence.plural_name, "Sequences")
    
    
    
    #----------------------------------------------------------------------
    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ class attribute is False for
        Sequence class.
        """
        
        self.assertEqual(Sequence.__strictly_typed__, False)
    
    
    