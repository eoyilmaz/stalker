#-*- coding: utf-8 -*-



import mocker
import datetime
from stalker.core.models import department, user, entity
from stalker.ext.validatedList import ValidatedList






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
        
        self.members_list = [self.mock_user1,
                             self.mock_user2,
                             self.mock_user3,
                             self.mock_user4,
                             ]
        
        self.mock_admin = self.mocker.mock(user.User)
        
        self.mocker.replay()
        
        self.date_created = self.date_updated = datetime.datetime.now()
        
        self.kwargs = {
            "name": "Test Department",
            "description": "This is a department for testing purposes",
            "created_by": self.mock_admin,
            "updated_by": self.mock_admin,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "members": self.members_list,
            "lead": self.mock_user1
        }
        
        # create a default department object
        self.mock_department = department.Department(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_members_argument_accepts_an_empy_list(self):
        """testing if members argument accepts an empty list
        """
        
        # this should work without raising any error
        self.kwargs["members"] = []
        
        aNewDepartment = department.Department(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_members_attribute_accepts_an_empy_list(self):
        """testing if members attribute accepts an empty list
        """
        
        # this should work without raising any error
        self.mock_department.members = []
    
    
    
    #----------------------------------------------------------------------
    def test_members_argument_accepts_only_a_list_of_user_objects(self):
        """testing if members argument accepts only a list of user objects
        """
        
        test_value = [1, 2.3, [], {}]
        
        self.kwargs["members"] = test_value
        # this should raise a ValueError
        self.assertRaises(
            ValueError,
            department.Department,
            **self.kwargs
        )
    
    
    
    #----------------------------------------------------------------------
    def test_members_attribute_accepts_only_a_list_of_user_objects(self):
        """testing if members attribute accepts only a list of user objects
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
    def test_members_attribute_is_a_ValidatedList_instance(self):
        """testing if the members attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_department.members, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_members_attribute_elements_accepts_User_only(self):
        """testing if a ValueError will be raised when trying to assign
        something other than a User object to the members list
        """
        
        # append
        self.assertRaises(
            ValueError,
            self.mock_department.members.append,
            0
        )
        
        # __setitem__
        self.assertRaises(
            ValueError,
            self.mock_department.members.__setitem__,
            0,
            0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_lead_argument_accepts_only_user_objects(self):
        """testing if lead argument accepts only user objects
        """
        
        test_values = [ "", 1, 2.3, [], {} ]
        
        # all of the above values should raise an ValueError
        for test_value in test_values:
            self.kwargs["lead"] = test_value
            self.assertRaises(
                ValueError,
                department.Department,
                **self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_lead_attribute_accepts_only_user_objects(self):
        """testing if lead attribute accepts only user objects
        """
        
        test_values = ["", 1, 2.3, [], {}]
        
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
    #def test_member_remove_also_removes_department_from_user(self):
        #"""testing if removing an user from the members list also removes the
        #department from the users department argument
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality of two Department objects
        """
        
        dep1 = department.Department(**self.kwargs)
        dep2 = department.Department(**self.kwargs)
        
        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("members")
        entity_kwargs.pop("lead")
        entity1 = entity.Entity(**entity_kwargs)
        
        self.kwargs["name"] = "Animation"
        dep3 = department.Department(**self.kwargs)
        
        self.assertTrue(dep1==dep2)
        self.assertFalse(dep1==dep3)
        self.assertFalse(dep1==entity1)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality of two Department objects
        """
        
        dep1 = department.Department(**self.kwargs)
        dep2 = department.Department(**self.kwargs)
        
        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("members")
        entity_kwargs.pop("lead")
        entity1 = entity.Entity(**entity_kwargs)
        
        self.kwargs["name"] = "Animation"
        dep3 = department.Department(**self.kwargs)
        
        self.assertFalse(dep1!=dep2)
        self.assertTrue(dep1!=dep3)
        self.assertTrue(dep1!=entity1)
