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
        self.mock_department1 = self.mocker.mock(department.Department)
        self.mock_department2 = self.mocker.mock(department.Department)
        
        # a couple of permission groups
        self.mock_permission_group1 = self.mocker.mock(group.Group)
        self.mock_permission_group2 = self.mocker.mock(group.Group)
        self.mock_permission_group3 = self.mocker.mock(group.Group)
        
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
        
        # a mock user
        self.mock_admin = self.mocker.mock(user.User)
        
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
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_email_attribute_accepting_only_string_or_unicode(self):
        """testing if the email attribute accepting only string or unicode
        values
        """
        
        # try to create a new user with wrong attribte
        test_value = ['an email']
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=test_value,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_email_property_accepting_only_string_or_unicode(self):
        """testing if the email property accepting only string or unicode
        values
        """
        
        # try to assign something else than a string or unicode
        test_value = 1
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'email',
            test_value
        )
        
        
        
        test_value = ['an email']
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'email',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_email_attribute_format(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        
        test_values = ['an email in no format',
                       'an_email_with_no_part2',
                       '@an_email_with_only_part2',
                       '@',
                       ]
        
        # any of this values should raise a ValueError
        for value in test_values:
            
            self.assertRaises(
                ValueError,
                user.User,
                name=self.name,
                first_name=self.first_name,
                last_name=self.last_name,
                description=self.description,
                email=value,
                password=self.password,
                login_name=self.login_name,
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
    
    
    
    #----------------------------------------------------------------------
    def test_email_property_format(self):
        """testing if given an email in wrong format will raise a ValueError 
        """
        
        test_values = ['an email in no format',
                       'an_email_with_no_part2',
                       '@an_email_with_only_part2',
                       '@',
                       'eoyilmaz@',
                       'eoyilmaz@somecompony@com',
                       ]
        
        # any of these email values should raise a ValueError
        for value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                'email',
                value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_email_property_works_properly(self):
        """testing if the email property works properly
        """
        
        test_email = 'eoyilmaz@somemail.com'
        
        self.mock_user.email = test_email
        
        self.assertEquals( self.mock_user.email, test_email)
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_attribute_accepts_only_strings(self):
        """testing if login_name attribute accepts only strings or unicode
        """
        
        test_values = [23412, ['a_user_login_name'] , [], {}, 3234.12312]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                user.User,
                name=self.name,
                first_name=self.first_name,
                last_name=self.last_name,
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=test_value,
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                projects_lead=[self.mock_project1,
                               self.mock_project2],
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_accepts_only_strings(self):
        """testing if login_name property accepts only strings or unicode
        """
        
        test_values = [12312, 132.123123, ['aloginname'], {}, []]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                'login_name',
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_attribute_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login_name attribute
        """
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name='',
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login_name property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'login_name',
            ''
        )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_attribute_for_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to login_name attribute
        """
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=None,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_for_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to login_name property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'login_name',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_attribute_formatted_correctly(self):
        """testing if the login_name attribute formatted correctly
        """
        
        #                 input       expected
        test_values = [ ('e. ozgur', 'eozgur'),
                        ('erkan', 'erkan'),
                        ('Ozgur', 'ozgur'),
                        ('Erkan ozgur', 'erkanozgur'),
                        ('eRKAN', 'erkan'),
                        ('eRkaN', 'erkan'),
                        (' eRkAn', 'erkan'),
                        (' eRkan ozGur', 'erkanozgur'),
                        ('213 e.ozgur', 'eozgur'),
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            test_user = user.User(
                name=self.name,
                first_name=self.first_name,
                last_name=self.last_name,
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=valuePair[0],
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
            
            self.assertEquals(
                test_user._login_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_formatted_correctly(self):
        """testing if the loing_name property formatted correctly
        """
        
        #                 input       expected
        test_values = [ ('e. ozgur', 'eozgur'),
                        ('erkan', 'erkan'),
                        ('Ozgur', 'ozgur'),
                        ('Erkan ozgur', 'erkanozgur'),
                        ('eRKAN', 'erkan'),
                        ('eRkaN', 'erkan'),
                        (' eRkAn', 'erkan'),
                        (' eRkan ozGur', 'erkanozgur'),
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            self.mock_user.login_name = valuePair[0]
            
            self.assertEquals(
                self.mock_user.login_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_attribute_None(self):
        """testing if a ValuError will be raised when trying to assing None to
        first_name attribute
        """
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=None,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        first_name property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'first_name',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_attribute_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to first_name attribute
        """
        
        # try to assign None to the first_name attribute
        test_value = None
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=test_value,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to first_name property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'first_name',
            ''
        )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_attribute_formatted_correctly(self):
        """testing if the first_name attribute is formatted correctly
        """
        
        #                 input       expected
        test_values = [ ('e. ozgur', 'E. Ozgur'),
                        ('erkan', 'Erkan'),
                        ('ozgur', 'Ozgur'),
                        ('Erkan ozgur', 'Erkan Ozgur'),
                        ('eRKAN', 'Erkan'),
                        ('eRkaN', 'Erkan'),
                        (' eRkAn', 'Erkan'),
                        (' eRkan ozGur', 'Erkan Ozgur'),
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            test_user = user.User(
                name=self.name,
                first_name=valuePair[0],
                last_name=self.last_name,
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=self.login_name,
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
            
            self.assertEquals(
                test_user._first_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_formatted_correctly(self):
        """testing if the first_name property is formatted correctly
        """
        
        #                 input       expected
        test_values = [ ('e. ozgur', 'E. Ozgur'),
                        ('erkan', 'Erkan'),
                        ('ozgur', 'Ozgur'),
                        ('Erkan ozgur', 'Erkan Ozgur'),
                        ('eRKAN', 'Erkan'),
                        ('eRkaN', 'Erkan'),
                        (' eRkAn', 'Erkan'),
                        (' eRkan ozGur', 'Erkan Ozgur'),
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            
            self.mock_user.first_name = valuePair[0]
            
            self.assertEquals(
                self.mock_user.first_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_attribute_accepts_only_strings(self):
        """testing if the first_name attribute accepts only strings or unicode
        """
        
        # try to assign something other than a string or unicode
        
        test_value = 1
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=test_value,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
        
        
        test_value = ['this is my first name']
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=test_value,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_accepts_only_strings(self):
        """testing if the first_name property accepts only strings or unicode
        """
        
        test_values = [12412, ['Erkan Ozgur']]
        
        for value in test_values:
            
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                'first_name',
                value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_attribute_None(self):
        """testing if it will be converted to an empty string if None is
        assigned to last_name attribute
        """
        
        aNewUser = user.User(
            name=self.name,
            first_name=self.first_name,
            last_name=None,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
        
        self.assertEquals(aNewUser.last_name, '')
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_None(self):
        """testing if it will be converted to an empty string if None is
        assigned to last_name property
        """
        
        self.mock_user.last_name = None
        
        self.assertEquals(self.mock_user.last_name, '')
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_attribute_formatted_correctly(self):
        """testing if the last_name attribute is formatted correctly
        """
        
        #                 input       expected
        test_values = [ ('yilmaz', 'Yilmaz'),
                        ('Yilmaz', 'Yilmaz'),
                        ('yILMAZ', 'Yilmaz'),
                        ('yIlmaZ', 'Yilmaz'),
                        (' yIlmAz', 'Yilmaz'),
                        (' yILmAz  ', 'Yilmaz'),
                        ('de niro', 'De Niro')
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            test_user = user.User(
                name=self.name,
                first_name=self.first_name,
                last_name=valuePair[0],
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=self.login_name,
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
            
            self.assertEquals(
                test_user._last_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_formatted_correctly(self):
        """testing if the last_name property is formatted correctly
        """
        
        #                 input       expected
        test_values = [ ('yilmaz', 'Yilmaz'),
                        ('Yilmaz', 'Yilmaz'),
                        ('yILMAZ', 'Yilmaz'),
                        ('yIlmaZ', 'Yilmaz'),
                        (' yIlmAz', 'Yilmaz'),
                        (' yILmAz  ', 'Yilmaz'),
                    ]
        
        for valuePair in test_values:
            self.mock_user.last_name = valuePair[0]
            
            self.assertEquals(
                self.mock_user.last_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_attribute_accepts_only_strings(self):
        """testing if the last_name attribute accepts only strings or unicode
        """
        
        test_values = [123123, ['asdfas'], [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                user.User,
                name=self.name,
                first_name=self.first_name,
                last_name=test_value,
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=self.login_name,
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_accepts_only_strings(self):
        """testing if the last_name property accepts only strings or unicode
        """
        
        test_values = [123123, ['a last name'], {},(), 234.23423]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                'last_name',
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_department_attribute_None(self):
        """testing if a ValueError will be raised when trying to assign None
        for the department attribute
        """
        
        #try to assign None to department
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=None,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_department_property_None(self):
        """testing if a ValueError will be raised when trying to assign None
        for the department property
        """
        
        # try to assign None to the department property
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'department',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_department_attribute_only_accepts_department_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a Department object to department attribute
        """
        
        # try to assign something other than a department object
        test_value = 'A department'
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=test_value,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_department_property_only_accepts_department_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a Department object to department property
        """
        
        # try to assign something other than a department
        test_value = 'a department'
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'department',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_department_property_works_properly(self):
        """testing if the department property works properly
        """
        
        # try to set and get the same value back
        self.mock_user.department = self.mock_department2
        
        self.assertEquals( self.mock_user.department, self.mock_department2)
        
    
    
    
    #----------------------------------------------------------------------
    def test_password_attribute_being_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the password attribute
        """
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=None,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_password_property_being_None(self):
        """testing if a ValueError will be raised when tyring to assign None
        to the password property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'password',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_password_property_works_properly(self):
        """testing if the password property works properly
        """
        
        test_password = 'a new test password'
        
        self.mock_user.password = test_password
        
        self.assertEquals(self.mock_user.password, test_password)
    
    
    
    ##----------------------------------------------------------------------
    #def test_password_attribute_being_mangled(self):
        #"""testing if the password is mangled when trying to store it
        #"""
        
        #self.fail('test not implemented yet')
    
    
    
    ##----------------------------------------------------------------------
    #def test_password_property_being_mangled(self):
        #"""testing if the password is mangled when trying to store it
        #"""
        
        #self.fail('test not implemented yet')
    
    
    
    ##----------------------------------------------------------------------
    #def test_password_attribute_retrieved_back_correctly(self):
        #"""testing if the password attribute decoded and retrieved correctly
        #"""
        
        #self.fail('test not implemented yet')
    
    
    
    ##----------------------------------------------------------------------
    #def test_password_property_retrieved_back_correctly(self):
        #"""testing if the password property decoded and retrieved correctly
        #"""
        
        #self.fail('test not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_attribute_for_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        permission_groups attribute
        """
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=None,
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_property_for_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        permission_groups property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'permission_groups',
            None
        )
    
    
    
    ##----------------------------------------------------------------------
    #def test_permission_groups_attribute_for_empty_list(self):
        #"""testing if a ValueError will be raised when trying to assign an
        #empty list to the permission_groups attribute
        #"""
        
        #test_value = []
        
        #self.assertRaises(
            #ValueError,
            #user.User,
            #name=self.name,
            #first_name=self.first_name,
            #last_name=self.last_name,
            #description=self.description,
            #email=self.email,
            #password=self.password,
            #login_name=self.login_name,
            #department=self.mock_department1,
            #permission_groups=test_value,
            #tasks=[self.mock_task1,
                   #self.mock_task2,
                   #self.mock_task3,
                   #self.mock_task4],
            #projects=[self.mock_project1,
                      #self.mock_project2,
                      #self.mock_project3],
            #projects_lead=[self.mock_project1,
                           #self.mock_project2],
            #sequences_lead=[self.mock_sequence1,
                            #self.mock_sequence2,
                            #self.mock_sequence3,
                            #self.mock_sequence4],
            #created_by=self.mock_admin,
            #updated_by=self.mock_admin
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_permission_groups_property_for_empty_list(self):
        #"""testing if a ValueError will be raised when trying to assign an
        #empty list to the permission_groups property
        #"""
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.mock_user,
            #'permission_groups',
            #[]
        #)
    
    
    
    #----------------------------------------------------------------------
    def test_perimssion_groups_attribute_accepts_only_group_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other then a Group object to the permission_group attribute
        """
        
        test_values = [23123,
                       1231.43122,
                       'a_group',
                       ['group1', 'group2', 234],
                       ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                user.User,
                name=self.name,
                first_name=self.first_name,
                last_name=self.last_name,
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=self.login_name,
                department=self.mock_department1,
                permission_groups=test_value,
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                projects_lead=[self.mock_project1,
                               self.mock_project2],
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
    
    
    
    #----------------------------------------------------------------------
    def test_perimssion_groups_property_accepts_only_group_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other then a Group object to the permission_group property
        """
        
        test_values = [23123,
                       1231.43122,
                       'a_group',
                       ['group1', 'group2', 234],
                       ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                'permission_groups',
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_property_works_properly(self):
        """testing if permission_groups property works properly
        """
        
        test_pg = [self.mock_permission_group3]
        self.mock_user.permission_groups = test_pg
        
        self.assertEquals(self.mock_user.permission_groups, test_pg)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the tasks attribute
        """
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=None,
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_property_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the tasks attribute
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'tasks',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_accepts_only_list_of_task_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a list of task objects to the tasks attribute
        """
        
        test_values = [ 12312, 1233244.2341, ['aTask1', 'aTask2'], 'a_task']
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                user.User,
                name=self.name,
                first_name=self.first_name,
                last_name=self.last_name,
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=self.login_name,
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=test_value,
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                projects_lead=[self.mock_project1,
                               self.mock_project2],
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_property_accepts_only_list_of_task_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a list of task objects to the tasks attribute
        """
        
        test_values = [ 12312, 1233244.2341, ['aTask1', 'aTask2'], 'a_task']
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                'tasks',
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_accepts_an_empty_list(self):
        """testing if nothing happens when trying to assing an empty list to
        tasks attribute
        """
        
        # this should work without any error
        aUserObj = user.User(
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_property_accepts_an_empty_list(self):
        """testing if nothing happends when trying to assign an empty list to
        tasks property
        """
        
        # this should work without any error
        self.mock_user.tasks = []
    
    
    
    #----------------------------------------------------------------------
    def test_projects_attribute_accepts_an_empty_list(self):
        """testing if the projects attribute accepts an empty list
        """
        
        # this should work properly
        user.User(
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_property_accepts_an_empty_list(self):
        """testing if the projects property accepts an empty list
        """
        
        # this should work properly
        self.mock_user.projects = []
    
    
    
    #----------------------------------------------------------------------
    def test_projects_attribute_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the projects attribute
        """
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=None,
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_property_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the projects property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'projects',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_attribute_accepts_only_a_list_of_project_objs(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects project attribute
        """
        
        test_values = [ 123123, 1231.2132, ['a_project1', 'a_project2'] ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                user.User,
                name=self.name,
                first_name=self.first_name,
                last_name=self.last_name,
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=self.login_name,
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=test_value,
                projects_lead=[self.mock_project1,
                               self.mock_project2],
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_property_accepts_only_a_list_of_project_objs(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects to projects property
        """
        
        test_values = [ 123123, 1231.2132, ['a_project1', 'a_project2'] ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                'projects',
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_attribute_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the projects_lead attribute
        """
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin,
            projects_lead=None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_property_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the projects_lead property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'projects_lead',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_attribute_accepts_empty_list(self):
        """testing if the projects_lead attribute accepts an empty list
        """
        
        # this should work without any problems
        self.mock_user = user.User(
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin,
            projects_lead=[]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_property_accepts_empty_list(self):
        """testing if the projects_lead property accepts an empty list
        """
        
        # this should work without any problem
        self.mock_user.projects_lead = []
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_attr_accepts_only_lits(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        projects_lead attribute
        """
        
        test_values = ['a project', 123123, {}, 12.2132 ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                user.User,
                name=self.name,
                first_name=self.first_name,
                last_name=self.last_name,
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=self.login_name,
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                projects_lead=test_value,
                sequences_lead=[self.mock_sequence1,
                                self.mock_sequence2,
                                self.mock_sequence3,
                                self.mock_sequence4],
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_attr_accepts_only_lits_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        projects_lead attribute
        """
        
        test_value = ['a project', 123123, [], {}, 12.2132 ]
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=test_value,
            sequences_lead=[self.mock_sequence1,
                            self.mock_sequence2,
                            self.mock_sequence3,
                            self.mock_sequence4],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_property_accepts_only_lits(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        projects_lead attribute
        """
        
        test_values = ['a project', 123123, {}, 12.2132 ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                'projects',
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_prop_accepts_only_list_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assing a list
        of other object than a list of Project objects to the
        projects_lead property
        """
        
        test_value = ['a project', 123123, [], {}, 12.2132 ]
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'projects_lead',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_attribute_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the sequences_lead attribute
        """
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=None,
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_property_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the sequences_lead property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            'sequences_lead',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_attribute_accepts_empty_list(self):
        """testing if the sequences_lead attribute accepts an empty list
        """
        #this should work
        a_user = user.User(
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=[],
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_property_accepts_empty_list(self):
        """testing if the sequences_lead property accepts an empty list
        """
        
        # this should work without any error
        self.mock_user.leader_of_seuqences = []
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_attr_accepts_only_lits(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        sequences_lead attribute
        """
        
        test_values = ['a sequence', 123123, {}, 12.2132 ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                user.User,
                name=self.name,
                first_name=self.first_name,
                last_name=self.last_name,
                description=self.description,
                email=self.email,
                password=self.password,
                login_name=self.login_name,
                department=self.mock_department1,
                permission_groups=[self.mock_permission_group1,
                                   self.mock_permission_group2],
                tasks=[self.mock_task1,
                       self.mock_task2,
                       self.mock_task3,
                       self.mock_task4],
                projects=[self.mock_project1,
                          self.mock_project2,
                          self.mock_project3],
                projects_lead=[self.mock_project1,
                               self.mock_project2],
                sequences_lead=test_value,
                created_by=self.mock_admin,
                updated_by=self.mock_admin
            )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_attr_accepts_only_lits_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        sequences_lead attribute
        """
        
        test_value = ['a sequence', 123123, [], {}, 12.2132 ]
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2],
            sequences_lead=test_value,
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_prop_accepts_only_list_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assing a list
        of other object than a list of Project objects to the
        sequences_lead property
        """
        
        test_value = ['a sequence', 123123, [], {}, 12.2132 ]
        
        self.assertRaises(
            ValueError,
            user.User,
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            description=self.description,
            email=self.email,
            password=self.password,
            login_name=self.login_name,
            department=self.mock_department1,
            permission_groups=[self.mock_permission_group1,
                               self.mock_permission_group2],
            tasks=[self.mock_task1,
                   self.mock_task2,
                   self.mock_task3,
                   self.mock_task4],
            projects=[self.mock_project1,
                      self.mock_project2,
                      self.mock_project3],
            projects_lead=[self.mock_project1,
                           self.mock_project2,
                           self.mock_project3],
            sequences_lead=test_value,
            created_by=self.mock_admin,
            updated_by=self.mock_admin
        )
    
    
    