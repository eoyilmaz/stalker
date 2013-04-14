# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
# 
# This file is part of Stalker.
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import unittest
from stalker import Studio, defaults, WorkingHours


class StudioTester(unittest.TestCase):
    """tests the stalker.models.studio.Studio class
    """
    
    def setUp(self):
        """setup the test
        """
        self.kwargs = dict(
            name = 'Studio',
            daily_working_hours = 8,
        )
        
        self.test_studio = Studio(**self.kwargs)
    
    def test_daily_working_hours_argument_is_skipped(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings when the daily_working_hours argument is skipped
        """
        try:
            self.kwargs.pop('daily_working_hours')
        except KeyError:
            pass
        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.daily_working_hours,
                         defaults.daily_working_hours)
    
    def test_daily_working_hours_argument_is_None(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings value when the daily_working_hours argument is None
        """
        self.kwargs['daily_working_hours'] = None
        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.daily_working_hours,
                         defaults.daily_working_hours)
    
    def test_daily_working_hours_attribute_is_None(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings value when it is set to None
        """
        self.test_studio.daily_working_hours = None
        self.assertEqual(self.test_studio.daily_working_hours,
                         defaults.daily_working_hours)
    
    def test_daily_working_hours_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the daily_working_hours
        argument is not an integer
        """
        self.kwargs['daily_working_hours'] = 'not an integer'
        self.assertRaises(TypeError, Studio, **self.kwargs)
    
    def test_daily_working_hours_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the daily_working hours
        attribute is set to a value other than an integer
        """
        self.assertRaises(TypeError, setattr, self.test_studio,
                          'daily_working_hours', 'not an intger')
    
    def test_daily_working_hours_argument_is_working_fine(self):
        """testing if the daily working hours argument value is correctly
        passed to daily_working_hours attribute
        """
        self.kwargs['daily_working_hours'] = 12
        new_project = Studio(**self.kwargs)
        self.assertEqual(new_project.daily_working_hours, 12)
    
    def test_daily_working_hours_attribute_is_working_properly(self):
        """testing if the daily_working_hours attribute is working properly
        """
        self.test_studio.daily_working_hours = 23
        self.assertEqual(self.test_studio.daily_working_hours, 23)
    
    def test_working_hours_argument_is_skipped(self):
        """testing if the default working hours will be used when the
        working_hours argument is skipped
        """
        self.kwargs['name'] = 'New Studio'
        try:
            self.kwargs.pop('working_hours') # pop if there are any
        except KeyError:
            pass
        
        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.working_hours, WorkingHours())
    
    def test_working_hours_argument_is_None(self):
        """testing if the a WorkingHour instance with default settings will be
        used if the working_hours argument is skipped
        """
        self.kwargs['name'] = 'New Studio'
        self.kwargs['working_hours'] = None
        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.working_hours, WorkingHours())
    
    def test_working_hours_attribute_is_None(self):
        """testing if a WorkingHour instance will be created with the default
        values if the working_hours attribute is set to None
        """
        self.test_studio.working_horus = None
        self.assertEqual(self.test_studio.working_hours, WorkingHours())
 
