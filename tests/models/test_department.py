#-*- coding: utf-8 -*-



import mocker
import datetime
from stalker.models import department, user






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
        self.mock_department(
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
    def test_members_attribute_accepts_an_empy_list(self):
        """testing if the members attribute accepts an empty list
        """
        
        self.fail('test not implemented yet')
    
    
    
    