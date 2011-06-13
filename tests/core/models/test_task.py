#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import Entity, Type






########################################################################
class TaskTester(mocker.MockerTestCase):
    """Tests the stalker.core.models.Task class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        #self.fail("test is not implemented yet")
        pass
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_skipped_defaults_to_500(self):
        """testing if skipping the priority argument will default the priority
        attribute to 500.
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_given_as_None_will_default_to_500(self):
        """testing if the priority argument is given as None will default the
        priority attribute to 500.
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_any_given_other_value_then_integer_will_default_to_500(self):
        """testing if any other value then an positif integer for priority
        argument will default thepriority attribute to 500.
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_any_given_other_value_then_integer_will_default_to_500(self):
        """testing if any other value then an positif integer for priority
        attribute will default it to 500.
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_negative(self):
        """testing if the priority argument is given as a negative value will
        set the priority attribute to zero.
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_is_negative(self):
        """testing if the priority attribute is given as a negative value will
        set the priority attribute to zero.
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_too_big(self):
        """testing if the priority argument is given bigger then 1000 will
        clamp the priority attribute value to 1000
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_is_too_big(self):
        """testing if the priority attribute is set to a value bigger than 1000
        will clamp the value to 1000
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_float(self):
        """testing if float numbers for prority argument will be converted to
        integer
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_is_float(self):
        """testing if float numbers for priority attribute will be converted to
        integer
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_is_working_properly(self):
        """testing if the priority attribute is working properly
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_argument_is_skipped(self):
        """testing if a TypeError will be raised when the resources argument is
        skipped
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_argument_is_None(self):
        """testing if a TypeError will be raised when the resources argument is
        given as None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_None(self):
        """testing if a TypeError will be raised when the resources attribute
        is set to None
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_argument_is_not_list(self):
        """testing if a TypeError will be raised when the resources argument is
        not a list
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_not_list(self):
        """testing if a TypeError will be raised when the resources attribute
        is set to any other value then a list
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_argument_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the resources argument is
        set to a list of other values then a User
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the resources attribute is
        set to a list of other values then a User
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_instance_of_ValidatedList(self):
        """testing if the resources attribute is an instance of ValidatedList
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_working_properly(self):
        """testing if the resources attribute is working properly
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_effort_and_duration_argument_is_skipped(self):
        """testing if the effort attribute is set to the default value of
        duration divided by the number of resources
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_effort_argument_skipped_but_duration_is_present(self):
        """testing if the effort argument is skipped but the duration is
        present the effort attribute is calculated from the
        duration * len(resources) formula
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_effort_argument_is_None_defaults_to_1_day(self):
        """testing if the effort argument is given as None will set the effort
        attribute to 1 day
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_effort_attribute_is_None_defaults_to_1_day(self):
        """testing if the effort attribute is given as None will set it to 1
        day.
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_effort_argument_is_not_an_instance_of_timedelta(self):
        """testing if a TypeError will be raised when the effort argument is
        not given as timedelta instance.
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_effort_attribute_is_not_an_instance_of_timedelta(self):
        """testing if a TypeError will be raised when the effort attribute is
        not given as timedelta instance.
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_effort_attribute_is_working_properly(self):
        """testing if the effort attribute is working properly
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_effort_argument_preceds_duration_argument(self):
        """testing if the effort argument preceeds duration argument 
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_effort_attribute_changes_duration(self):
        """testing if the effort attribute changes the duration
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_duration_attribute_changes_effort(self):
        """testing if the duration attribute changes the effort attribute value
        by the effort = duration / len(resources) formula
        """
        
        self.fail("test is not implemented yet")
    
    
    
    