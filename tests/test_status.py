#-*- coding: utf-8 -*-
########################################################################
# 
# Copyright (C) 2010  Erkan Ozgur Yilmaz
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 
########################################################################



import unittest
from stalker.models import status



########################################################################
class TestStatus(unittest.TestCase):
    """testing the status class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_name_str_or_unicode(self):
        """test the name attribute if it is str or unicode
        """
        
        #----------------------------------------------------------------------
        # the name should be a str or unicode
        self.assertRaises(ValueError, status.Status, 1, '1')
        # check the property
        a_status = status.Status('Complete', 'Cmpl')
        self.assertRaises(ValueError, setattr, a_status, 'name', 1)
        
    
    #----------------------------------------------------------------------
    def test_name_for_being_empty(self):
        """testing the name attribute if it is empty
        """
        #----------------------------------------------------------------------
        # the name could not be an empty string
        self.assertRaises(ValueError, status.Status, '', 'Cmp')
        # check the property
        a_status = status.Status('Complete', 'Cmpl')
        self.assertRaises(ValueError, setattr, a_status, 'name', '')
    
    
    
    #----------------------------------------------------------------------
    def test_name_first_letter_lowercase(self):
        """testing the name attributes first letter against being a lowercase
        letter
        """
        
        #----------------------------------------------------------------------
        # the first letter of the name should be in upper case and the other
        # letters should be in lower case
        status_name = 'test'
        a_status = status.Status(status_name, 'tst')
        self.assertEqual(status_name.title(), a_status.name)
        
        # check the property
        a_status = status.Status('Complete', 'Cmpl')
        a_status.name = status_name
        self.assertEqual(status_name.title(), a_status.name)
    
    
    
    #----------------------------------------------------------------------
    def test_name_first_letter_integer(self):
        """testing the name attributes first letter against being an integer
        value
        """
        #----------------------------------------------------------------------
        # the first letter of the name could not be an integer
        status_name = '1test'
        self.assertRaises(ValueError, status.Status, status_name, \
                           status_name)
        
        # check the property
        a_status = status.Status('Complete', 'Cmpl')
        self.assertRaises(ValueError, setattr, a_status, 'name', status_name)
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_str_or_unicode(self):
        """testing the abbreviation attribute against not being a string or
        unicode
        """
        
        #----------------------------------------------------------------------
        # the abbreviation should be a str or unicode
        self.assertRaises(ValueError, status.Status, 'Complete', 1)
        
        # check the property
        a_status = status.Status('Complete', 'Cmlt')
        self.assertRaises(ValueError, setattr, a_status, 'abbreviation', 1)
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_empty_string(self):
        """testing the abbreviation attribute against being an empty string
        """
        
        #----------------------------------------------------------------------
        # the abbreviation can not be an empty string
        self.assertRaises(ValueError, status.Status, 'Complete', '')
        
        # check the property
        a_status = status.Status('Complete', 'Cmlt')
        self.assertRaises(ValueError, setattr, a_status, 'abbreviation', '')
        
        #----------------------------------------------------------------------
        # check if the abbreviation is get correctly
        name = 'Complete'
        abbr = 'Cmplt'
        a_status = status.Status(name, abbr)
        self.assertEquals( a_status.abbreviation, abbr)






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
            status.Status('Not Available', 'N/A'),
            status.Status('Waiting To Start', 'WStrt'),
            status.Status('Started', 'Strt'),
            status.Status('Waiting For Approve', 'WAppr'),
            status.Status('Approved', 'Appr'),
            status.Status('Finished', 'Fnsh'),
            status.Status('On Hold', 'OH'),
            ]
    
    
    
    #----------------------------------------------------------------------
    def test_name_empty(self):
        """testing the name attribute against  being empty
        """
        
        #----------------------------------------------------------------------
        # the name couldn't be empty
        self.assertRaises(ValueError, status.StatusList, '', self.a_status_list)
        
        # test the name property
        a_status_list_obj = status.StatusList(self.list_name, self.a_status_list)
        self.assertRaises(ValueError, setattr, a_status_list_obj, 'name', '')
    
    
    
    #----------------------------------------------------------------------
    def test_name_for_str_or_unicode(self):
        """testing the name against not being a string or unicode
        """
        
        #----------------------------------------------------------------------
        # the name should be a string or unicode
        self.assertRaises(ValueError, status.StatusList, 1, self.a_status_list)
        
        a_status_list_obj = status.StatusList(self.list_name, self.a_status_list)
        self.assertRaises(ValueError, setattr, a_status_list_obj, 'name', 1)
        self.assertRaises(ValueError, setattr, a_status_list_obj, 'name', [])
        self.assertRaises(ValueError, setattr, a_status_list_obj, 'name', {})
    
    
    
    #----------------------------------------------------------------------
    def test_name_property(self):
        """testing the name attribute property
        """
        
        #----------------------------------------------------------------------
        # it should be property
        new_list_name = 'new status list name'
        
        # check if we can properly assign new values to name property
        a_status_list_obj = status.StatusList(self.list_name, self.a_status_list)
        a_status_list_obj.name = new_list_name
        self.assertEquals(a_status_list_obj.name, new_list_name)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_accepting_statuses(self):
        """testing the statuses list attribute
        """
        
        # the statuses attribute should be a list of statuses
        # can be empty?
        #
        
        #----------------------------------------------------------------------
        # it should only accept lists of statuses
        self.assertRaises(ValueError,
                          status.StatusList, self.list_name, 'a str')
        self.assertRaises(ValueError,
                          status.StatusList, self.list_name, {})
        self.assertRaises(ValueError,
                          status.StatusList, self.list_name, 1)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_property_accepting_only_statuses(self):
        """testing the status_list attribute as a property and accepting
        Status objects only
        """
        new_status_list = status.StatusList( self.list_name, self.a_status_list )
        
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
        self.assertRaises(ValueError,
                          status.StatusList, self.list_name, [])
    
    
    
    #----------------------------------------------------------------------
    def test_statusList_list_elements_being_status_objects(self):
        """testing status_list elements against not being derived from Status
        class
        """
        
        #----------------------------------------------------------------------
        # every element should be an object derived from Status
        a_fake_status_list = [1, 2, 'a string', u'a unicode', 4.5]
        
        self.assertRaises(ValueError,
                          status.StatusList, self.list_name, a_fake_status_list)
    
    
    
    #----------------------------------------------------------------------
    def test_statusList_property(self):
        """testing status_list as being property
        """
        
        #----------------------------------------------------------------------
        # it should be a property so check if it sets property correctly
        a_status_list_obj = status.StatusList( self.list_name, self.a_status_list)
        new_list_of_statutes = [ status.Status('New Status', 'abbr') ]
        a_status_list_obj.statuses = new_list_of_statutes
        self.assertEquals( a_status_list_obj.statuses, new_list_of_statutes)
        
        