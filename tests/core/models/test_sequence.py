#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import sequence, project, user, shot, entity, status
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
        
        self.mock_project = self.mocker.mock(project.Project)
        self.mock_project2 = self.mocker.mock(project.Project)
        self.mock_lead = self.mocker.mock(user.User)
        self.mock_lead2 = self.mocker.mock(user.User)
        
        self.mock_shot1 = self.mocker.mock(shot.Shot)
        self.mock_shot2 = self.mocker.mock(shot.Shot)
        self.mock_shot3 = self.mocker.mock(shot.Shot)
        
        self.mock_status1 = self.mocker.mock(status.Status)
        self.mock_status2 = self.mocker.mock(status.Status)
        self.mock_status3 = self.mocker.mock(status.Status)
        
        self.mock_status_list1 = self.mocker.mock(status.StatusList)
        self.expect(self.mock_status_list1.target_entity_type).\
            result(sequence.Sequence.entity_type).count(0, None)
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
        self.mock_sequence = sequence.Sequence(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_default_value_is_None(self):
        """testing if the project attribute defaults to None when no project
        argument is given
        """
        
        self.kwargs.pop("project")
        new_sequence = sequence.Sequence(**self.kwargs)
        self.assertEquals(new_sequence.project, None)
    
    
    
    #----------------------------------------------------------------------
    def test_project_argument_is_None(self):
        """testing if nothing happens when the project argument is None
        """
        
        self.kwargs["project"] = None
        new_sequence = sequence.Sequence(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_set_to_None(self):
        """testing if nothing happends when the project attribute set to None
        """
        
        self.mock_sequence.project = None
    
    
    
    #----------------------------------------------------------------------
    def test_project_argument_other_than_a_Project(self):
        """testing if a ValueError will be raised when the project argument
        is None
        """
        
        test_values = [1, 1.2, "a project", ["a", "list"]]
        
        for test_value in test_values:
            self.kwargs["project"] = test_value
            self.assertRaises(ValueError, sequence.Sequence, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_other_than_a_Project(self):
        """testing if a ValueError will be raised when the project attribute
        is set to None
        """
        
        test_values = [1, 1.2, "project", ["a", "list"]]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_sequence,
                "project",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_working_properly(self):
        """testing if the project attribute is working properly
        """
        
        self.mock_sequence.project = self.mock_project2
        self.assertEquals(self.mock_sequence.project, self.mock_project2)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_defaults_to_None(self):
        """testing if the lead attribute defualts to None when no lead argument
        is given
        """
        
        self.kwargs.pop("lead")
        new_sequence = sequence.Sequence(**self.kwargs)
        self.assertEquals(new_sequence.lead, None)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_None(self):
        """testing if nothing will happen when the lead argument is given as
        None
        """
        
        self.kwargs["lead"] = None
        new_sequence = sequence.Sequence(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_None(self):
        """testing if nothing will happen when the lead attribute is set to
        None
        """
        
        self.mock_sequence.lead = None
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_is_not_User(self):
        """testing if a ValueError will be raised when the lead argument is not
        an instance of user.User
        """
        
        test_values = [1, 1.2, "a user", ["a", "list", "as", "user"]]
        
        for test_value in test_values:
            self.kwargs["lead"] = test_value
            self.assertRaises(ValueError, sequence.Sequence, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_is_not_User(self):
        """testing if a ValueError will be raised when the lead attribute is
        set to something other than a user.User
        """
        
        test_values = [1, 1.2, "a user", ["a", "list", "as", "user"]]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
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
        self.assertEquals(self.mock_sequence.lead, self.mock_lead2)
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_defaults_to_empty_list(self):
        """testing if the shots attribute defaults to an empty list
        """
        
        self.kwargs.pop("shots")
        new_sequence = sequence.Sequence(**self.kwargs)
        self.assertEquals(new_sequence.shots, [])
    
    
    
    #----------------------------------------------------------------------
    def test_shots_argument_is_set_to_None(self):
        """testing if the shots attribute will be set to an empty list when the
        shots argument is given as None
        """
        
        self.kwargs["shots"] = None
        new_sequence = sequence.Sequence(**self.kwargs)
        self.assertEquals(new_sequence.shots, [])
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_is_set_None(self):
        """testing if the shots attribute will be set to an empty list when it
        is set to None
        """
        
        self.mock_sequence.shots = None
        self.assertEquals(self.mock_sequence.shots, [])
    
    
    
    #----------------------------------------------------------------------
    def test_shots_argument_is_set_to_other_than_a_list(self):
        """testing if a ValueError will be raised when the given shots argument
        is not a list
        """
        
        test_values = [1, 1.2, "a string"]
        
        for test_value in test_values:
            self.kwargs["shots"] = test_value
            self.assertRaises(ValueError, sequence.Sequence, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_is_set_to_other_than_a_list(self):
        """testing if a ValueError will be raised when the shots attribute is
        tried to be set to something other than a list
        """
        
        test_values = [1, 1.2, "a string"]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_sequence,
                "shots",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_shots_argument_is_a_list_of_other_objects(self):
        """testing if a ValueError will be raised when the shots argument is a
        list of other type of objects
        """
        
        test_value = [1, 1.2, "a string"]
        self.kwargs["shots"] = test_value
        self.assertRaises(ValueError, sequence.Sequence, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_is_a_list_of_other_objects(self):
        """testing if a ValueError will be raised when the shots argument is a
        list of other type of objects
        """
        
        test_value = [1, 1.2, "a string"]
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_sequence,
            "shots",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_shots_attribute_elements_tried_to_be_set_to_non_Shot_object(self):
        """testing if a ValueError will be raised when the individual elements
        in the shots list tried to be set to something other than a Shot
        instance
        """
        
        test_values = [1, 1.2, "a string", ["a", "list"]]
        
        for test_value in test_values:
            self.assertRaises(ValueError,
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
        
        
        new_seq1 = sequence.Sequence(**self.kwargs)
        new_seq2 = sequence.Sequence(**self.kwargs)
        new_entity = entity.Entity(**self.kwargs)
        
        self.kwargs["name"] = "a different sequence"
        new_seq3 = sequence.Sequence(**self.kwargs)
        
        self.assertTrue(new_seq1==new_seq2)
        self.assertFalse(new_seq1==new_seq3)
        self.assertFalse(new_seq1==new_entity)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality of sequences
        """
        
        
        new_seq1 = sequence.Sequence(**self.kwargs)
        new_seq2 = sequence.Sequence(**self.kwargs)
        new_entity = entity.Entity(**self.kwargs)
        
        self.kwargs["name"] = "a different sequence"
        new_seq3 = sequence.Sequence(**self.kwargs)
        
        self.assertFalse(new_seq1!=new_seq2)
        self.assertTrue(new_seq1!=new_seq3)
        self.assertTrue(new_seq1!=new_entity)
    
    
    