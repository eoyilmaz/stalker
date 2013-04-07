# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import copy
import unittest
from stalker.conf import defaults
from stalker.models.project import WorkingHours

class WorkingHoursTester(unittest.TestCase):
    """tests the stalker.models.project.WorkingHours class
    """
    
    def test_working_hours_argument_is_skipped(self):
        """testing if a WorkingHours is created with the default settings by
        default.
        """
        wh = WorkingHours()
        self.assertEqual(wh.working_hours, defaults.WORKING_HOURS)
    
    def test_working_hours_argument_is_None(self):
        """testing if a WorkingHours is created with the default settings if
        the working_hours argument is None
        """
        wh = WorkingHours(working_hours=None)
        self.assertEqual(wh.working_hours, defaults.WORKING_HOURS)
    
    def test_working_hours_argument_is_not_a_dictionary(self):
        """testing if a TypeError will be raised when the working_hours
        argument value is not a dictionary
        """
        self.assertRaises(TypeError, WorkingHours,
                          working_hours='not a dictionary of proper values')
    
    def test_working_hours_attribute_is_not_a_dictionary(self):
        """testing if a TypeError will be raised when the working_hours
        attribute is set to a value which is not a dictionary
        """
        wh = WorkingHours()
        self.assertRaises(TypeError, setattr, wh, 'working_hours',
                          'not a dictionary of proper values')
    
    def test_working_hours_argument_value_is_dictionary_of_other_formatted_data(self):
        """testing if a TypeError will be raised when the working_hours
        argument value is a dictionary of some other value than list of list of
        dual integers
        """
        self.assertRaises(TypeError, WorkingHours,
                          working_hours={'not': 'properly valued'})
    
    def test_working_hours_attribute_is_set_to_a_dictionary_of_other_formatted_data(self):
        """testing if a TypeError will be raised when the working hours
        attribute value is a dictionary of some other value
        """
        wh = WorkingHours()
        self.assertRaises(TypeError, setattr, wh, 'working_hours',
                          {'not': 'properly valued'})
    
    def test_working_hours_argument_data_is_not_in_correct_range(self):
        """testing if a ValueError will be raised when the range of the time
        values are not correct in the working_hours argument
        """
        wh = copy.copy(defaults.WORKING_HOURS)
        wh['sun'] = [[-10, 1000]]
        
        self.assertRaises(ValueError, WorkingHours,
                          working_hours=wh)
        
        wh = copy.copy(defaults.WORKING_HOURS)
        wh['sat'] = [[900, 1080], [1090, 1500]]
        self.assertRaises(ValueError, WorkingHours,
                          working_hours=wh)
    
    def test_working_hours_attribute_data_is_not_in_correct_range(self):
        """testing if a ValueError will be raised if the range of the time
        values are not correct when setting the working_hours attr
        """
        wh = copy.copy(defaults.WORKING_HOURS)
        wh['sun'] = [[-10, 1000]]
        
        wh_ins = WorkingHours()
        self.assertRaises(ValueError, setattr, wh_ins, 'working_hours', wh)
        
        wh = copy.copy(defaults.WORKING_HOURS)
        wh['sat'] = [[900, 1080], [1090, 1500]]
        self.assertRaises(ValueError, setattr, wh_ins, 'working_hours', wh)
    
    def test_working_hours_argument_value_is_not_complete(self):
        """testing if the default values are going to be used for missing days
        in the given working_hours argument
        """
        working_hours = {
            'sat': [[900, 1080]],
            'sun': [[900, 1080]]
        }
        wh = WorkingHours(working_hours=working_hours)
        self.assertEqual(wh['mon'], defaults.WORKING_HOURS['mon'])
        self.assertEqual(wh['tue'], defaults.WORKING_HOURS['tue'])
        self.assertEqual(wh['wed'], defaults.WORKING_HOURS['wed'])
        self.assertEqual(wh['thu'], defaults.WORKING_HOURS['thu'])
        self.assertEqual(wh['fri'], defaults.WORKING_HOURS['fri'])
    

    def test_working_hours_attribute_value_is_not_complete(self):
        """testing if the default values are going to be used for missing days
        in the given working_hours attribute
        """
        working_hours = {
            'sat': [[900, 1080]],
            'sun': [[900, 1080]]
        }
        wh = WorkingHours()
        wh.working_hours = working_hours
        self.assertEqual(wh['mon'], defaults.WORKING_HOURS['mon'])
        self.assertEqual(wh['tue'], defaults.WORKING_HOURS['tue'])
        self.assertEqual(wh['wed'], defaults.WORKING_HOURS['wed'])
        self.assertEqual(wh['thu'], defaults.WORKING_HOURS['thu'])
        self.assertEqual(wh['fri'], defaults.WORKING_HOURS['fri'])
         
    def test_working_hours_can_be_indexed_with_day_number(self):
        """testing if the working hours for a day can be reached by an index
        """
        wh = WorkingHours()
        self.assertEqual(wh[0], defaults.WORKING_HOURS['sun'])
        wh[0] = [[540, 1080]]
    
    def test_working_hours_day_0_is_sunday(self):
        """testing if day zero is sunday (I hate this standard)
        """
        wh = WorkingHours()
        wh[0] = [[270, 980]]
        self.assertEqual(wh['sun'], wh[0])
    
    def test_working_hours_can_be_string_indexed_with_the_date_short_name(self):
        """testing if the working hours information can be reached by using
        the short date name as the index
        """
        wh = WorkingHours()
        self.assertEqual(wh['sun'], defaults.WORKING_HOURS['sun'])
        wh['sun'] = [[540, 1080]]
    
    def test___setitem__checks_the_given_data(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()
        self.assertRaises(TypeError, wh.__setitem__, 0, 'not a proper data')
        self.assertRaises(TypeError, wh.__setitem__, 'sun',
                          'not a proper data')
        self.assertRaises(TypeError, wh.__setitem__, 0, ['no proper data'])
        self.assertRaises(TypeError, wh.__setitem__, 'sun', ['no proper data'])
        
        self.assertRaises(RuntimeError, wh.__setitem__, 0,
                          [['no proper data']])
        self.assertRaises(RuntimeError, wh.__setitem__, 'sun',
                          [['no proper data']])
        
        self.assertRaises(RuntimeError, wh.__setitem__, 0, [[3]])
        self.assertRaises(TypeError, wh.__setitem__, 2, [[2, 'a']])
        self.assertRaises(TypeError, wh.__setitem__, 1, [[20, 10], ['a', 300]])
        self.assertRaises(TypeError, wh.__setitem__, 5,
                          [[323, 1344], [2, 'd']])
        self.assertRaises(RuntimeError, wh.__setitem__, 0, [[4, 100, 3]])
    
        self.assertRaises(RuntimeError, wh.__setitem__, 'mon', [[3]])
        self.assertRaises(TypeError, wh.__setitem__, 'mon', [[2, 'a']])
        self.assertRaises(TypeError, wh.__setitem__, 'tue', [[20, 10],
                                                             ['a', 300]])
        self.assertRaises(TypeError, wh.__setitem__, 'fri', [[323, 1344],
                                                              [2, 'd']])
        self.assertRaises(RuntimeError, wh.__setitem__, 'sat', [[4, 100, 3]])
    
    def test___setitem__checks_the_value_ranges(self):
        """testing if a ValueError will be raised if value is not in the
        correct range in __setitem__
        """
        wh = WorkingHours()
        self.assertRaises(ValueError, wh.__setitem__, 'sun', [[-10, 100]])
        self.assertRaises(ValueError, wh.__setitem__, 'sat', [[0, 1800]])
    
    def test___setitem__will_not_accept_any_other_key_or_value(self):
        """testing if it is possible to use the other indexes or keys
        """
        wh = WorkingHours()
        
        # indexing out of interested range
        self.assertRaises(IndexError, wh.__setitem__, 7,
                          [[32, 23], [233, 324]])
        self.assertRaises(KeyError, wh.__setitem__, 'zon',
                          [[32, 23], [233, 324]])
 
    def test_working_hours_argument_is_working_properly(self):
        """testing if the working_hours argument is working properly
        """
        working_hours = copy.copy(defaults.WORKING_HOURS)
        working_hours['sun'] = [[540, 1000]]
        working_hours['sat'] = [[500, 800], [900, 1440]]
        wh = WorkingHours(working_hours=working_hours)
        self.assertEqual(wh.working_hours, working_hours)
        self.assertEqual(wh.working_hours['sun'], working_hours['sun'])
        self.assertEqual(wh.working_hours['sat'], working_hours['sat'])
    
    def test_working_hours_attribute_is_working_properly(self):
        """testing if the working_hours attribute is working properly
        """
        working_hours = copy.copy(defaults.WORKING_HOURS)
        working_hours['sun'] = [[540, 1000]]
        working_hours['sat'] = [[500, 800], [900, 1440]]
        wh = WorkingHours()
        wh.working_hours = working_hours
        self.assertEqual(wh.working_hours, working_hours)
        self.assertEqual(wh.working_hours['sun'], working_hours['sun'])
        self.assertEqual(wh.working_hours['sat'], working_hours['sat'])
    
    def test_to_tjp_attribute_is_read_only(self):
        """testing if the to_tjp attribute is read only
        """
        wh = WorkingHours()
        self.assertRaises(AttributeError, setattr, wh, 'to_tjp', 'some value')
    
    def test_to_tjp_attribute_is_working_properly(self):
        """testing if the to_tjp property is working properly
        """
        wh = WorkingHours()
        wh['mon'] = [[570, 1110]]
        wh['tue'] = [[570, 1110]]
        wh['wed'] = [[570, 1110]]
        wh['thu'] = [[570, 1110]]
        wh['fri'] = [[570, 1110]]
        wh['sat'] = []
        wh['sun'] = []
        
        expected_tjp = """    workinghours mon 09:30 - 18:30
    workinghours tue 09:30 - 18:30
    workinghours wed 09:30 - 18:30
    workinghours thu 09:30 - 18:30
    workinghours fri 09:30 - 18:30
    workinghours sat off
    workinghours sun off"""
        
        self.assertEqual(wh.to_tjp, expected_tjp)
    
    def test_to_tjp_attribute_is_working_properly_for_multiple_work_hour_ranges(self):
        """testing if the to_tjp property is working properly
        """
        wh = WorkingHours()
        wh['mon'] = [[570, 720], [780, 1110]]
        wh['tue'] = [[570, 720], [780, 1110]]
        wh['wed'] = [[570, 720], [780, 1110]]
        wh['thu'] = [[570, 720], [780, 1110]]
        wh['fri'] = [[570, 720], [780, 1110]]
        wh['sat'] = [[570, 720]]
        wh['sun'] = []
        
        expected_tjp = """    workinghours mon 09:30 - 12:00, 13:00 - 18:30
    workinghours tue 09:30 - 12:00, 13:00 - 18:30
    workinghours wed 09:30 - 12:00, 13:00 - 18:30
    workinghours thu 09:30 - 12:00, 13:00 - 18:30
    workinghours fri 09:30 - 12:00, 13:00 - 18:30
    workinghours sat 09:30 - 12:00
    workinghours sun off"""
        
        self.assertEqual(wh.to_tjp, expected_tjp)
 
    def test_weekly_working_hours_attribute_is_read_only(self):
        """testing if the weekly_working_hours is a read-only attribute
        """
        wh = WorkingHours()
        self.assertRaises(AttributeError, setattr, wh, 'weekly_working_hours',
                          232)
    
    def test_weekly_working_hours_attribute_is_working_properly(self):
        """testing if the weekly_working_hours attribute is working properly
        """
        wh = WorkingHours()
        wh['mon'] = [[570, 720], [780, 1110]] # 480
        wh['tue'] = [[570, 720], [780, 1110]] # 480
        wh['wed'] = [[570, 720], [780, 1110]] # 480
        wh['thu'] = [[570, 720], [780, 1110]] # 480
        wh['fri'] = [[570, 720], [780, 1110]] # 480
        wh['sat'] = [[570, 720]]              # 150
        wh['sun'] = []                        # 0
        
        expected_value = 42.5
        self.assertEqual(wh.weekly_working_hours, expected_value)
