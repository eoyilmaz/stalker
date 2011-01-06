#-*- coding: utf-8 -*-



import mocker
import datetime
from stalker.core.models import department, user






########################################################################
class DepartmentTester(mocker.MockerTestCase):
    """tests the Department class
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """lets setup the tests
        """
        
        # create a couple of mock users
        self.mock_user1 = self.mocker.mock(user.User)
        self.mock_user2 = self.mocker.mock(user.User)
        self.mock_user3 = self.mocker.mock(user.User)
        self.mock_user4 = self.mocker.mock(user.User)
        
        self.members_list = [ self.mock_user1,
                              self.mock_user2,
                              self.mock_user3,
                              self.mock_user4,
                            ]
        
        self.mock_admin = self.mocker.mock(user.User)
        
        self.mocker.replay()
        
        self.name = 'Test Department'
        self.description = 'This is a department for testing purposes'
        self.date_created = self.date_updated = datetime.datetime.now()
        
        
        # create a default department object
        self.mock_department = department.Department(
            name=self.name,
            description=self.description,
            created_by=self.mock_admin,
            updated_by=self.mock_admin,
            date_created=self.date_created,
            date_updated=self.date_updated,
            members=self.members_list,
            lead=self.mock_user1
        )
    
    
    
    #----------------------------------------------------------------------
    def test_members_argument_accepts_an_empy_list(self):
        """testing if members argument accepts an empty list
        """
        
        # this should work without raising any error
        aNewDepartment = department.Department(
            name=self.name,
            description=self.description,
            created_by=self.mock_admin,
            updated_by=self.mock_admin,
            date_created=self.date_created,
            date_updated=self.date_updated,
            members=[],
            lead=self.mock_user1
        )
    
    
    
    #----------------------------------------------------------------------
    def test_members_property_accepts_an_empy_list(self):
        """testing if members property accepts an empty list
        """
        
        # this should work without raising any error
        self.mock_department.members = []
    
    
    
    #----------------------------------------------------------------------
    def test_members_argument_accepts_only_a_list_of_user_objects(self):
        """testing if members argument accepts only a list of user objects
        """
        
        test_value = [1, 2.3, [], {}]
        
        # this should raise a ValueError
        self.assertRaises(
            ValueError,
            department.Department,
            name=self.name,
            description=self.description,
            created_by=self.mock_admin,
            updated_by=self.mock_admin,
            date_created=self.date_created,
            date_updated=self.date_updated,
            members=test_value,
            lead=self.mock_user1
        )
    
    
    
    #----------------------------------------------------------------------
    def test_members_property_accepts_only_a_list_of_user_objects(self):
        """testing if members property accepts only a list of user objects
        """
        
        test_value = [1, 2.3, [], {}]
        
        # this should raise a ValueError
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_department,
            "members",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_accepts_only_user_objects(self):
        """testing if lead argument accepts only user objects
        """
        
        test_values = [ "", 1, 2.3, [], {} ]
        
        # all of the above values should raise an ValueError
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                department.Department,
                name=self.name,
                description=self.description,
                created_by=self.mock_admin,
                updated_by=self.mock_admin,
                date_created=self.date_created,
                date_updated=self.date_updated,
                members=self.members_list,
                lead=test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_lead_property_accepts_only_user_objects(self):
        """testing if lead property accepts only user objects
        """
        
        test_values = [ "", 1, 2.3, [], {} ]
        
        # all of the above values should raise an ValueError
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_department,
                "lead",
                test_value
            )
    
    
    
    ##----------------------------------------------------------------------
    #def test_lead_argument_being_None(self):
        #"""testing if a ValueError will be raised when trying to assing None to
        #the lead argument
        #"""
        
        #self.assertRaises(
            #ValueError,
            #department.Department,
            #name=self.name,
            #description=self.description,
            #created_by=self.mock_admin,
            #updated_by=self.mock_admin,
            #date_created=self.date_created,
            #date_updated=self.date_updated,
            #members=self.members_list,
            #lead=None
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_lead_property_being_None(self):
        #"""testing if a ValueError will be raised when trying to assing None to
        #lead property
        #"""
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.mock_department,
            #"lead",
            #None
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_member_remove_also_removes_department_from_user(self):
        #"""testing if removing an user from the members list also removes the
        #department from the users department argument
        #"""
        
        #self.fail('test is not implemented yet')
    
    
    