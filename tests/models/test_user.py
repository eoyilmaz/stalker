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
        # create the default values for parameters
        
        self.name = 'ozgur'
        self.first_name = 'Erkan Ozgur'
        self.last_name = 'Yilmaz'
        self.login_name = 'eoyilmaz'
        self.password = 'hidden'
        self.email = 'eoyilmaz@fake.com'
        self.description = 'this is a test user'
        
        # need to have some mock object for
        assert(isinstance(self.mocker, mocker.Mocker))
        
        # a department
        self.mock_department = self.mocker.mock(department.Department)
        
        # a couple of permission groups
        self.mock_permission_group1 = self.mocker.mock(group.Group)
        self.mock_permission_group2 = self.mocker.mock(group.Group)
        
        # a couple of tasks
        self.mock_task1 = self.mocker.mock(task.Task)
        self.mock_task2 = self.mocker.mock(task.Task)
        self.mock_task3 = self.mocker.mock(task.Task)
        self.mock_task4 = self.mocker.mock(task.Task)
        
        # a couple of projects
        self.mock_project1 = self.mocker.mock(project.Project)
        self.mock_project2 = self.mocker.mock(project.Project)
        self.mock_project3 = self.mocker.mock(project.Project)
        
        # a couple of sequences
        self.mock_sequence1 = self.mocker.mock(sequence.Sequence)
        self.mock_sequence2 = self.mocker.mock(sequence.Sequence)
        self.mock_sequence3 = self.mocker.mock(sequence.Sequence)
        self.mock_sequence4 = self.mocker.mock(sequence.Sequence)
        
        self.mocker.replay()
        
        # create a proper user object
        self.mock_user = user.User(
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            leader_of_sequences=[self.mock_sequence1,
                                 self.mock_sequence2,
                                 self.mock_sequence3,
                                 self.mock_sequence4]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_email_attribute_accepting_only_string_or_unicode(self):
        """testing if the email attribute accepting only string or unicode
        values
        """
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_email_property_accepting_only_string_or_unicode(self):
        """testing if the email property accepting only string or unicode
        values
        """
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_email_attribute_format(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        
        test_values = ['an email in no format',
                       'an_email_with_no_part2',
                       '@an_email_with_only_part2',
                       '@',
                       ]
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_email_property_format(self):
        """testing if given an email in wrong format will raise a ValueError 
        """
        
        test_values = ['an email in no format',
                       'an_email_with_no_part2',
                       '@an_email_with_only_part2',
                       '@',
                       ]
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_attribute_accepts_only_strings(self):
        """testing if login_name attribute accepts only strings or unicode
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_accepts_only_strings(self):
        """testing if login_name property accepts only strings or unicode
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_attribute_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login_name attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login_name property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_attribute_for_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to login_name attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_for_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to login_name property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_attribute_formatted_correctly(self):
        """testing if the login_name attribute formatted correctly
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_formatted_correctly(self):
        """testing if the loing_name property formatted correctly
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_attribute_None(self):
        """testing if a ValuError will be raised when trying to assing None to
        first_name attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        first_name property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_attribute_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to first_name attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to first_name property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_attribute_formatted_correctly(self):
        """testing if the first_name attribute is formatted correctly
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_formatted_correctly(self):
        """testing if the first_name property is formatted correctly
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_attribute_accepts_only_strings(self):
        """testing if the first_name attribute accepts only strings or unicode
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_accepts_only_strings(self):
        """testing if the first_name property accepts only strings or unicode
        """
        
        self.fail('test not implemented yet')
    
        
        
        
        
        
    
    
    #----------------------------------------------------------------------
    def test_last_name_attribute_None(self):
        """testing if a ValuError will be raised when trying to assing None to
        last_name attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        last_name property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_attribute_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to last_name attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to last_name property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_attribute_formatted_correctly(self):
        """testing if the last_name attribute is formatted correctly
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_formatted_correctly(self):
        """testing if the last_name property is formatted correctly
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_attribute_accepts_only_strings(self):
        """testing if the last_name attribute accepts only strings or unicode
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_accepts_only_strings(self):
        """testing if the last_name property accepts only strings or unicode
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_department_attribute_None(self):
        """testing if a ValueError will be raised when trying to assign None
        for the department attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_department_property_None(self):
        """testing if a ValueError will be raised when trying to assign None
        for the department property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_department_attribute_only_accepts_department_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a Department object to department attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_department_property_only_accepts_department_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a Department object to department property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_password_attribute_being_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the password attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_password_property_being_None(self):
        """testing if a ValueError will be raised when tyring to assign None
        to the password property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_password_attribute_being_mangled(self):
        """testing if the password is mangled when trying to store it
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_password_property_being_mangled(self):
        """testing if the password is mangled when trying to store it
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_password_attribute_retrieved_back_correctly(self):
        """testing if the password attribute decoded and retrieved correctly
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_password_property_retrieved_back_correctly(self):
        """testing if the password property decoded and retrieved correctly
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_attribute_for_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        permission_groups attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_property_for_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        permission_groups property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_attribute_for_empty_list(self):
        """testing if a ValueError will be raised when trying to assign an
        empty list to the permission_groups attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_property_for_empty_list(self):
        """testing if a ValueError will be raised when trying to assign an
        empty list to the permission_groups property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_perimssion_groups_attribute_accepts_only_group_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other then a Group object to the permission_group attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_perimssion_groups_property_accepts_only_group_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other then a Group object to the permission_group property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the tasks attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_property_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the tasks attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_accepts_only_list_of_task_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a list of task objects to the tasks attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_property_accepts_only_list_of_task_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a list of task objects to the tasks attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_accepts_an_empty_list(self):
        """testing if nothing happens when trying to assing an empty list to
        tasks attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_property_accepts_an_empty_list(self):
        """testing if nothing happends when trying to assign an empty list to
        tasks property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_projects_attribute_accepts_an_empty_list(self):
        """testing if the projects attribute accepts an empty list
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_projects_property_accepts_an_empty_list(self):
        """testing if the projects property accepts an empty list
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_projects_attribute_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the projects attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_projects_property_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the projects property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_projects_attribute_accepts_only_a_list_of_project_objs(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects project attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_projects_property_accepts_only_a_list_of_project_objs(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects to projects property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_projects_attribute_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the leader_of_projects attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_projects_property_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the leader_of_projects property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_projects_attribute_accepts_empty_list(self):
        """testing if the leader_of_projects attribute accepts an empty list
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_projects_property_accepts_empty_list(self):
        """testing if the leader_of_projects property accepts an empty list
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_projects_attr_accepts_only_lits_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        leader_of_projects attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_projects_prop_accepts_only_list_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assing a list
        of other object than a list of Project objects to the
        leader_of_projects property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_sequences_attribute_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the leader_of_sequences attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_sequences_property_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the leader_of_sequences property
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_sequences_attribute_accepts_empty_list(self):
        """testing if the leader_of_sequences attribute accepts an empty list
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_sequences_property_accepts_empty_list(self):
        """testing if the leader_of_sequences property accepts an empty list
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_sequences_attr_accepts_only_lits_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        leader_of_sequences attribute
        """
        
        self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_leader_of_sequences_prop_accepts_only_list_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assing a list
        of other object than a list of Project objects to the
        leader_of_sequences property
        """
        
        self.fail('test not implemented yet')
    
    
    