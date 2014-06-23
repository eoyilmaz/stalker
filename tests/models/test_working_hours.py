# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import copy
import unittest
import datetime

from stalker import config
from stalker.models.studio import WorkingHours

defaults = config.Config()


class WorkingHoursTester(unittest.TestCase):
    """tests the stalker.models.project.WorkingHours class
    """

    def test_working_hours_argument_is_skipped(self):
        """testing if a WorkingHours is created with the default settings by
        default.
        """
        wh = WorkingHours()
        self.assertEqual(wh.working_hours, defaults.working_hours)

    def test_working_hours_argument_is_None(self):
        """testing if a WorkingHours is created with the default settings if
        the working_hours argument is None
        """
        wh = WorkingHours(working_hours=None)
        self.assertEqual(wh.working_hours, defaults.working_hours)

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
        wh = copy.copy(defaults.working_hours)
        wh['sun'] = [[-10, 1000]]

        self.assertRaises(ValueError, WorkingHours,
                          working_hours=wh)

        wh = copy.copy(defaults.working_hours)
        wh['sat'] = [[900, 1080], [1090, 1500]]
        self.assertRaises(ValueError, WorkingHours,
                          working_hours=wh)

    def test_working_hours_attribute_data_is_not_in_correct_range(self):
        """testing if a ValueError will be raised if the range of the time
        values are not correct when setting the working_hours attr
        """
        wh = copy.copy(defaults.working_hours)
        wh['sun'] = [[-10, 1000]]

        wh_ins = WorkingHours()
        self.assertRaises(ValueError, setattr, wh_ins, 'working_hours', wh)

        wh = copy.copy(defaults.working_hours)
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
        self.assertEqual(wh['mon'], defaults.working_hours['mon'])
        self.assertEqual(wh['tue'], defaults.working_hours['tue'])
        self.assertEqual(wh['wed'], defaults.working_hours['wed'])
        self.assertEqual(wh['thu'], defaults.working_hours['thu'])
        self.assertEqual(wh['fri'], defaults.working_hours['fri'])

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
        self.assertEqual(wh['mon'], defaults.working_hours['mon'])
        self.assertEqual(wh['tue'], defaults.working_hours['tue'])
        self.assertEqual(wh['wed'], defaults.working_hours['wed'])
        self.assertEqual(wh['thu'], defaults.working_hours['thu'])
        self.assertEqual(wh['fri'], defaults.working_hours['fri'])

    def test_working_hours_can_be_indexed_with_day_number(self):
        """testing if the working hours for a day can be reached by an index
        """
        wh = WorkingHours()
        self.assertEqual(wh[6], defaults.working_hours['sun'])
        wh[6] = [[540, 1080]]

    def test_working_hours_day_0_is_monday(self):
        """testing if day zero is monday
        """
        wh = WorkingHours()
        wh[0] = [[270, 980]]
        self.assertEqual(wh['mon'], wh[0])

    def test_working_hours_can_be_string_indexed_with_the_date_short_name(self):
        """testing if the working hours information can be reached by using
        the short date name as the index
        """
        wh = WorkingHours()
        self.assertEqual(wh['sun'], defaults.working_hours['sun'])
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
        working_hours = copy.copy(defaults.working_hours)
        working_hours['sun'] = [[540, 1000]]
        working_hours['sat'] = [[500, 800], [900, 1440]]
        wh = WorkingHours(working_hours=working_hours)
        self.assertEqual(wh.working_hours, working_hours)
        self.assertEqual(wh.working_hours['sun'], working_hours['sun'])
        self.assertEqual(wh.working_hours['sat'], working_hours['sat'])

    def test_working_hours_attribute_is_working_properly(self):
        """testing if the working_hours attribute is working properly
        """
        working_hours = copy.copy(defaults.working_hours)
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
        wh['mon'] = [[570, 720], [780, 1110]]  # 480
        wh['tue'] = [[570, 720], [780, 1110]]  # 480
        wh['wed'] = [[570, 720], [780, 1110]]  # 480
        wh['thu'] = [[570, 720], [780, 1110]]  # 480
        wh['fri'] = [[570, 720], [780, 1110]]  # 480
        wh['sat'] = [[570, 720]]               # 150
        wh['sun'] = []                         # 0

        expected_value = 42.5
        self.assertEqual(wh.weekly_working_hours, expected_value)

    def test_is_working_hour_is_working_properly(self):
        """testing if the is_working_hour method is working properly
        """
        wh = WorkingHours()

        wh['mon'] = [[570, 720], [780, 1110]]
        wh['tue'] = [[570, 720], [780, 1110]]
        wh['wed'] = [[570, 720], [780, 1110]]
        wh['thu'] = [[570, 720], [780, 1110]]
        wh['fri'] = [[570, 720], [780, 1110]]
        wh['sat'] = [[570, 720]]
        wh['sun'] = []

        # monday
        check_date = datetime.datetime(2013, 4, 8, 13, 55)
        self.assertTrue(wh.is_working_hour(check_date))

        # sunday
        check_date = datetime.datetime(2013, 4, 14, 13, 55)
        self.assertFalse(wh.is_working_hour(check_date))

    def test_day_numbers_are_correct(self):
        """testing if the day numbers are correct
        """
        wh = WorkingHours()
        wh['mon'] = [[1, 2]]
        wh['tue'] = [[3, 4]]
        wh['wed'] = [[5, 6]]
        wh['thu'] = [[7, 8]]
        wh['fri'] = [[9, 10]]
        wh['sat'] = [[11, 12]]
        wh['sun'] = [[13, 14]]

        self.assertEqual(defaults.day_order[0], 'mon')
        self.assertEqual(defaults.day_order[1], 'tue')
        self.assertEqual(defaults.day_order[2], 'wed')
        self.assertEqual(defaults.day_order[3], 'thu')
        self.assertEqual(defaults.day_order[4], 'fri')
        self.assertEqual(defaults.day_order[5], 'sat')
        self.assertEqual(defaults.day_order[6], 'sun')

        self.assertEqual(wh['mon'], wh[0])
        self.assertEqual(wh['tue'], wh[1])
        self.assertEqual(wh['wed'], wh[2])
        self.assertEqual(wh['thu'], wh[3])
        self.assertEqual(wh['fri'], wh[4])
        self.assertEqual(wh['sat'], wh[5])
        self.assertEqual(wh['sun'], wh[6])

    def test_weekly_working_days_is_a_read_only_attribute(self):
        """testing if the weekly working days is a read-only attribute
        """
        wh = WorkingHours()
        self.assertRaises(AttributeError, setattr, wh, 'weekly_working_days',
                          6)

    def test_weekly_working_days_is_calculated_correctly(self):
        """testing if the weekly working days are calculated correctly
        """
        wh = WorkingHours()
        wh['mon'] = [[1, 2]]
        wh['tue'] = [[3, 4]]
        wh['wed'] = [[5, 6]]
        wh['thu'] = [[7, 8]]
        wh['fri'] = [[9, 10]]
        wh['sat'] = []
        wh['sun'] = []
        self.assertEqual(wh.weekly_working_days, 5)

        wh = WorkingHours()
        wh['mon'] = [[1, 2]]
        wh['tue'] = [[3, 4]]
        wh['wed'] = [[5, 6]]
        wh['thu'] = [[7, 8]]
        wh['fri'] = [[9, 10]]
        wh['sat'] = [[11, 12]]
        wh['sun'] = []
        self.assertEqual(wh.weekly_working_days, 6)

        wh = WorkingHours()
        wh['mon'] = [[1, 2]]
        wh['tue'] = [[3, 4]]
        wh['wed'] = [[5, 6]]
        wh['thu'] = [[7, 8]]
        wh['fri'] = [[9, 10]]
        wh['sat'] = [[11, 12]]
        wh['sun'] = [[13, 14]]
        self.assertEqual(wh.weekly_working_days, 7)

    def test_yearly_working_days_is_a_read_only_attribute(self):
        """testing if the yearly_working_days attribute is a read only
        attribute
        """
        wh = WorkingHours()
        self.assertRaises(AttributeError, setattr, wh, 'yearly_working_days',
                          260.1)

    def test_yearly_working_days_is_calculated_correctly(self):
        """testing if the yearly_working_days is calculated correctly
        """

        wh = WorkingHours()
        wh['mon'] = [[1, 2]]
        wh['tue'] = [[3, 4]]
        wh['wed'] = [[5, 6]]
        wh['thu'] = [[7, 8]]
        wh['fri'] = [[9, 10]]
        wh['sat'] = []
        wh['sun'] = []
        self.assertAlmostEqual(wh.yearly_working_days, 261, 3)

        wh = WorkingHours()
        wh['mon'] = [[1, 2]]
        wh['tue'] = [[3, 4]]
        wh['wed'] = [[5, 6]]
        wh['thu'] = [[7, 8]]
        wh['fri'] = [[9, 10]]
        wh['sat'] = [[11, 12]]
        wh['sun'] = []
        self.assertAlmostEqual(wh.yearly_working_days, 313, 4)

        wh = WorkingHours()
        wh['mon'] = [[1, 2]]
        wh['tue'] = [[3, 4]]
        wh['wed'] = [[5, 6]]
        wh['thu'] = [[7, 8]]
        wh['fri'] = [[9, 10]]
        wh['sat'] = [[11, 12]]
        wh['sun'] = [[13, 14]]
        self.assertAlmostEqual(wh.yearly_working_days, 365, 0)

    def test_daily_working_hours_argument_is_skipped(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings when the daily_working_hours argument is skipped
        """
        wh = WorkingHours()
        self.assertEqual(wh.daily_working_hours, defaults.daily_working_hours)

    def test_daily_working_hours_argument_is_None(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings value when the daily_working_hours argument is None
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = None
        wh = WorkingHours(**kwargs)
        self.assertEqual(wh.daily_working_hours,
                         defaults.daily_working_hours)

    def test_daily_working_hours_attribute_is_None(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings value when it is set to None
        """
        wh = WorkingHours()
        wh.daily_working_hours = None
        self.assertEqual(wh.daily_working_hours, defaults.daily_working_hours)

    def test_daily_working_hours_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the daily_working_hours
        argument is not an integer
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = 'not an integer'
        self.assertRaises(TypeError, WorkingHours, **kwargs)

    def test_daily_working_hours_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the daily_working hours
        attribute is set to a value other than an integer
        """
        wh = WorkingHours()
        self.assertRaises(TypeError, setattr, wh, 'daily_working_hours',
                          'not an integer')

    def test_daily_working_hours_argument_is_working_fine(self):
        """testing if the daily working hours argument value is correctly
        passed to daily_working_hours attribute
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = 12
        wh = WorkingHours(**kwargs)
        self.assertEqual(wh.daily_working_hours, 12)

    def test_daily_working_hours_attribute_is_working_properly(self):
        """testing if the daily_working_hours attribute is working properly
        """
        wh = WorkingHours()
        wh.daily_working_hours = 23
        self.assertEqual(wh.daily_working_hours, 23)

    def test_daily_working_hours_argument_is_zero(self):
        """testing if a ValueError will be raised when the daily_working_hours
        argument value is zero
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = 0
        self.assertRaises(ValueError, WorkingHours, **kwargs)

    def test_daily_working_hours_attribute_is_zero(self):
        """testing if a ValueError will be raised when the daily_working_hours
        attribute is set to zero
        """
        wh = WorkingHours()
        self.assertRaises(ValueError, setattr, wh, 'daily_working_hours', 0)

    def test_daily_working_hours_argument_is_a_negative_number(self):
        """testing if a ValueError will be raised when the daily_working_hours
        argument value is negative
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = -10
        self.assertRaises(ValueError, WorkingHours, **kwargs)

    def test_daily_working_hours_attribute_is_a_negative_number(self):
        """testing if a ValueError will be raised when the daily_working_hours
        attribute is set to a negative value
        """
        wh = WorkingHours()
        self.assertRaises(ValueError, setattr, wh, 'daily_working_hours', -10)

    def test_daily_working_hours_argument_is_set_to_a_number_bigger_than_24(self):
        """testing if a ValueError will be raised when the daily working hours
        argument value is bigger than 24
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = 25
        self.assertRaises(ValueError, WorkingHours, **kwargs)

    def test_daily_working_hours_attribute_is_set_to_a_number_bigger_than_24(self):
        """testing if a ValueError will be raised when the daily working hours
        attribute value is bigger than 24
        """
        wh = WorkingHours()
        self.assertRaises(ValueError, setattr, wh, 'daily_working_hours', 25)

    def test_split_in_to_working_hours_is_not_implemented_yet(self):
        """testing if a NotimplementedError will be raised when the
        split_in_to_working_hours() method is called
        """
        with self.assertRaises(NotImplementedError):
            wh = WorkingHours()
            start = datetime.datetime.now()
            end = start + datetime.timedelta(days=10)
            wh.split_in_to_working_hours(start, end)
