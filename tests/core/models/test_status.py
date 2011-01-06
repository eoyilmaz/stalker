#-*- coding: utf-8 -*-



import unittest
from stalker.core.models import status



########################################################################
class TestStatus(unittest.TestCase):
    """testing the status class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_short_name_argument_accepts_str_or_unicode_only(self):
        """testing if a ValueError will be raised when setting the short_name
        argument something other than a string or unicode
        """
        
        test_values = [1, 1.0, ['Cmplt'], {}, ()]
        
        for test_value in test_values:
            #----------------------------------------------------------------------
            # the short_name should be a str or unicode
            self.assertRaises(
                ValueError,
                status.Status,
                name='Complete',
                short_name=test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_short_name_property_accepts_str_or_unicode_only(self):
        """testing if a ValueError will be raised when trying to assign
        something else than a string or unicode to the short_name property
        """
        
        # check the property
        a_status = status.Status(name='Complete', short_name='Cmlt')
        self.assertRaises(
            ValueError,
            setattr,
            a_status,
            'short_name',
            1
        )
    
    
    
    #----------------------------------------------------------------------
    def test_short_name_argument_empty_string(self):
        """testing if a ValueError will be raised when trying to set the
        short_name argument to an empty string
        """
        
        #----------------------------------------------------------------------
        # the short_name can not be an empty string
        self.assertRaises(ValueError, status.Status, 'Complete', '')
    
    
    
    #----------------------------------------------------------------------
    def test_short_name_property_dont_accept_empty_string(self):
        """testing if a ValueError will be raised when trying to assing an
        empty string to short_name property
        """
        
        # check the property
        a_status = status.Status(name='Complete', short_name='Cmlt')
        self.assertRaises(
            ValueError,
            setattr,
            a_status,
            'short_name',
            ''
        )
    
    
    
    #----------------------------------------------------------------------
    def test_short_name_property_works_properly(self):
        """testing if short_name property works properly
        """
        
        #----------------------------------------------------------------------
        # check if the short_name is get correctly
        name = 'Complete'
        abbr = 'Cmplt'
        
        a_status = status.Status(name='Complete', short_name='Cmlt')
        
        a_status = status.Status(name=name, short_name=abbr)
        self.assertEquals(a_status.short_name, abbr)






########################################################################
class StatusListTest(unittest.TestCase):
    """testing the StatusList class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """let's create proper values for the tests
        """
        
        # proper values
        self.list_name = 'a_status_list'
        
        # should use Mocks in the list
        self.a_status_list = [
            status.Status(name='Not Available', short_name='N/A'),
            status.Status(name='Waiting To Start', short_name='WStrt'),
            status.Status(name='Started', short_name='Strt'),
            status.Status(name='Waiting For Approve', short_name='WAppr'),
            status.Status(name='Approved', short_name='Appr'),
            status.Status(name='Finished', short_name='Fnsh'),
            status.Status(name='On Hold', short_name='OH'),
            ]
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_accepts_statuses_only(self):
        """testing if statuses list argument accepts list of statuses only
        """
        
        # the statuses argument should be a list of statuses
        # can be empty?
        #
        
        test_values = ['a str', {}, 1, 1.0]
        
        for test_value in test_values:
            #----------------------------------------------------------------------
            # it should only accept lists of statuses
            self.assertRaises(
                ValueError,
                status.StatusList,
                name=self.list_name,
                statuses=test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_property_accepting_only_statuses(self):
        """testing the status_list property as a property and accepting
        Status objects only
        """
        new_status_list = status.StatusList(
            name=self.list_name,
            statuses=self.a_status_list
        )
        
        test_values = ['1', ['1'], 1, [1, 'w']]
        
        # check the property
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                new_status_list,
                'statuses',
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_being_empty(self):
        """testing status_list against being empty
        """
        
        #----------------------------------------------------------------------
        # the list couldn't be empty
        self.assertRaises(
            ValueError,
            status.StatusList,
            name=self.list_name,
            statuses=[]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_statusList_list_elements_being_status_objects(self):
        """testing status_list elements against not being derived from Status
        class
        """
        
        #----------------------------------------------------------------------
        # every element should be an object derived from Status
        a_fake_status_list = [1, 2, 'a string', u'a unicode', 4.5]
        
        self.assertRaises(
            ValueError,
            status.StatusList,
            name=self.list_name,
            statuses=a_fake_status_list
        )
    
    
    
    #----------------------------------------------------------------------
    def test_statusList_property(self):
        """testing status_list as being property
        """
        
        #----------------------------------------------------------------------
        # it should be a property so check if it sets property correctly
        a_status_list_obj = status.StatusList(
            name=self.list_name,
            statuses=self.a_status_list
        )
        
        new_list_of_statutes = [
            status.Status(name='New Status', short_name='nsts')
        ]
        
        a_status_list_obj.statuses = new_list_of_statutes
        self.assertEquals( a_status_list_obj.statuses, new_list_of_statutes)
        
        