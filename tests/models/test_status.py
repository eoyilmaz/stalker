#-*- coding: utf-8 -*-



import unittest
from stalker.models import status



########################################################################
class TestStatus(unittest.TestCase):
    """testing the status class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_short_name_str_or_unicode(self):
        """testing the short_name attribute against not being a string or
        unicode
        """
        
        #----------------------------------------------------------------------
        # the short_name should be a str or unicode
        self.assertRaises(
            ValueError,
            status.Status,
            name='Complete',
            short_name=1
        )
        
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
    def test_short_name_empty_string(self):
        """testing the short_name attribute against being an empty string
        """
        
        #----------------------------------------------------------------------
        # the short_name can not be an empty string
        self.assertRaises(ValueError, status.Status, 'Complete', '')
        
        # check the property
        a_status = status.Status(name='Complete', short_name='Cmlt')
        self.assertRaises(ValueError, setattr, a_status, 'short_name', '')
        
        #----------------------------------------------------------------------
        # check if the short_name is get correctly
        name = 'Complete'
        abbr = 'Cmplt'
        a_status = status.Status(name=name, short_name=abbr)
        self.assertEquals( a_status.short_name, abbr)






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
    
    
    
    ##----------------------------------------------------------------------
    #def test_name_empty(self):
        #"""testing the name attribute against  being empty
        #"""
        
        ##----------------------------------------------------------------------
        ## the name couldn't be empty
        #self.assertRaises(ValueError, status.StatusList, '', self.a_status_list)
        
        ## test the name property
        #a_status_list_obj = status.StatusList(self.list_name, self.a_status_list)
        #self.assertRaises(ValueError, setattr, a_status_list_obj, 'name', '')
    
    
    
    ##----------------------------------------------------------------------
    #def test_name_for_str_or_unicode(self):
        #"""testing the name against not being a string or unicode
        #"""
        
        ##----------------------------------------------------------------------
        ## the name should be a string or unicode
        #self.assertRaises(ValueError, status.StatusList, 1, self.a_status_list)
        
        #a_status_list_obj = status.StatusList(self.list_name, self.a_status_list)
        #self.assertRaises(ValueError, setattr, a_status_list_obj, 'name', 1)
        #self.assertRaises(ValueError, setattr, a_status_list_obj, 'name', [])
        #self.assertRaises(ValueError, setattr, a_status_list_obj, 'name', {})
    
    
    
    ##----------------------------------------------------------------------
    #def test_name_property(self):
        #"""testing the name attribute property
        #"""
        
        ##----------------------------------------------------------------------
        ## it should be property
        #new_list_name = 'new status list name'
        
        ## check if we can properly assign new values to name property
        #a_status_list_obj = status.StatusList(self.list_name, self.a_status_list)
        #a_status_list_obj.name = new_list_name
        #self.assertEquals(a_status_list_obj.name, new_list_name)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_accepting_statuses(self):
        """testing the statuses list attribute
        """
        
        # the statuses attribute should be a list of statuses
        # can be empty?
        #
        
        #----------------------------------------------------------------------
        # it should only accept lists of statuses
        self.assertRaises(
            ValueError,
            status.StatusList,
            name=self.list_name,
            statuses='a str'
        )
        
        self.assertRaises(
            ValueError,
            status.StatusList,
            name=self.list_name,
            statuses={}
        )
        
        self.assertRaises(
            ValueError,
            status.StatusList,
            name=self.list_name,
            statuses=1
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_property_accepting_only_statuses(self):
        """testing the status_list attribute as a property and accepting
        Status objects only
        """
        new_status_list = status.StatusList(
            name=self.list_name,
            statuses=self.a_status_list
        )
        
        # check the property
        self.assertRaises(ValueError,
                          setattr,new_status_list, 'statuses', '1')
        
        self.assertRaises(ValueError,
                          setattr, new_status_list, 'statuses', ['1'])
        
        self.assertRaises(ValueError,
                          setattr, new_status_list, 'statuses', 1)
        
        self.assertRaises(ValueError,
                          setattr, new_status_list, 'statuses', [1, 'w'])
    
    
    
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
        
        