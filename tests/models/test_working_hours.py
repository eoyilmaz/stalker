# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
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

from stalker.models.studio import WorkingHours
from stalker.testing import UnitTestBase


class WorkingHoursTester(UnitTestBase):
    """tests the stalker.models.project.WorkingHours class
    """

    def test_working_hours_argument_is_skipped(self):
        """testing if a WorkingHours is created with the default settings by
        default.
        """
        wh = WorkingHours()
        from stalker import defaults
        self.assertEqual(wh.working_hours, defaults.working_hours)

    def test_working_hours_argument_is_None(self):
        """testing if a WorkingHours is created with the default settings if
        the working_hours argument is None
        """
        wh = WorkingHours(working_hours=None)
        from stalker import defaults
        self.assertEqual(wh.working_hours, defaults.working_hours)

    def test_working_hours_argument_is_not_a_dictionary(self):
        """testing if a TypeError will be raised when the working_hours
        argument value is not a dictionary
        """
        with self.assertRaises(TypeError) as cm:
            WorkingHours(working_hours='not a dictionary of proper values')

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours should be a dictionary, not str'
        )

    def test_working_hours_attribute_is_not_a_dictionary(self):
        """testing if a TypeError will be raised when the working_hours
        attribute is set to a value which is not a dictionary
        """
        wh = WorkingHours()
        with self.assertRaises(TypeError) as cm:
            wh.working_hours= 'not a dictionary of proper values'

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours should be a dictionary, not str'
        )

    def test_working_hours_argument_value_is_dictionary_of_other_formatted_data(self):
        """testing if a TypeError will be raised when the working_hours
        argument value is a dictionary of some other value than list of list of
        dual integers
        """
        with self.assertRaises(TypeError) as cm:
            WorkingHours(working_hours={'not': 'properly valued'})

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours should be a dictionary with keys '
            '"mon, tue, wed, thu, fri, sat, sun" and the values should a list '
            'of lists of two integers like [[540, 720], [800, 1080]], not str'
        )

    def test_working_hours_attribute_is_set_to_a_dictionary_of_other_formatted_data(self):
        """testing if a TypeError will be raised when the working hours
        attribute value is a dictionary of some other value
        """
        wh = WorkingHours()
        with self.assertRaises(TypeError) as cm:
            wh.working_hours = {'not': 'properly valued'}

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours should be a dictionary with keys '
            '"mon, tue, wed, thu, fri, sat, sun" and the values should a '
            'list of lists of two integers like [[540, 720], [800, 1080]], '
            'not str'
        )

    def test_working_hours_argument_data_is_not_in_correct_range1(self):
        """testing if a ValueError will be raised when the range of the time
        values are not correct in the working_hours argument
        """
        import copy
        from stalker import defaults
        wh = copy.copy(defaults.working_hours)
        wh['sun'] = [[-10, 1000]]

        with self.assertRaises(ValueError) as cm:
            WorkingHours(working_hours=wh)

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[-10, 1000]]'
        )

    def test_working_hours_argument_data_is_not_in_correct_range2(self):
        """testing if a ValueError will be raised when the range of the time
        values are not correct in the working_hours argument
        """
        import copy
        from stalker import defaults

        wh = copy.copy(defaults.working_hours)
        wh['sat'] = [[900, 1080], [1090, 1500]]
        with self.assertRaises(ValueError) as cm:
            WorkingHours(working_hours=wh)

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[900, 1080], [1090, 1500]]'
        )

    def test_working_hours_attribute_data_is_not_in_correct_range1(self):
        """testing if a ValueError will be raised if the range of the time
        values are not correct when setting the working_hours attr
        """
        import copy
        from stalker import defaults
        wh = copy.copy(defaults.working_hours)
        wh['sun'] = [[-10, 1000]]

        wh_ins = WorkingHours()
        with self.assertRaises(ValueError) as cm:
            wh_ins.working_hours = wh

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[-10, 1000]]'
        )

    def test_working_hours_attribute_data_is_not_in_correct_range2(self):
        """testing if a ValueError will be raised if the range of the time
        values are not correct when setting the working_hours attr
        """
        import copy
        from stalker import defaults

        wh_ins = WorkingHours()
        wh = copy.copy(defaults.working_hours)
        wh['sat'] = [[900, 1080], [1090, 1500]]
        with self.assertRaises(ValueError) as cm:
            wh_ins.working_hours = wh

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[900, 1080], [1090, 1500]]'
        )

    def test_working_hours_argument_value_is_not_complete(self):
        """testing if the default values are going to be used for missing days
        in the given working_hours argument
        """
        working_hours = {
            'sat': [[900, 1080]],
            'sun': [[900, 1080]]
        }
        wh = WorkingHours(working_hours=working_hours)
        from stalker import defaults
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
        from stalker import defaults
        self.assertEqual(wh['mon'], defaults.working_hours['mon'])
        self.assertEqual(wh['tue'], defaults.working_hours['tue'])
        self.assertEqual(wh['wed'], defaults.working_hours['wed'])
        self.assertEqual(wh['thu'], defaults.working_hours['thu'])
        self.assertEqual(wh['fri'], defaults.working_hours['fri'])

    def test_working_hours_can_be_indexed_with_day_number(self):
        """testing if the working hours for a day can be reached by an index
        """
        wh = WorkingHours()
        from stalker import defaults
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
        from stalker import defaults
        self.assertEqual(wh['sun'], defaults.working_hours['sun'])
        wh['sun'] = [[540, 1080]]

    def test___setitem__checks_the_given_data_1(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()
        with self.assertRaises(TypeError) as cm:
            wh[0] = 'not a proper data'

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not str'
        )

    def test___setitem__checks_the_given_data_2(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(TypeError) as cm:
            wh['sun'] = 'not a proper data'

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not str'
        )

    def test___setitem__checks_the_given_data_3(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(TypeError) as cm:
            wh[0] = ['no proper data']

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not str'
        )

    def test___setitem__checks_the_given_data_4(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(TypeError) as cm:
            wh['sun'] = ['no proper data']

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not str'
        )

    def test___setitem__checks_the_given_data_5(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(RuntimeError) as cm:
            wh[0] = [['no proper data']]

        self.assertEqual(
            str(cm.exception),
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers between and the range of integers should be 0-1440, "
            "not [['no proper data']]"
        )

    def test___setitem__checks_the_given_data_6(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(RuntimeError) as cm:
            wh['sun'] = [['no proper data']]

        self.assertEqual(
            str(cm.exception),
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers between and the range of integers should be 0-1440, "
            "not [['no proper data']]"
        )

    def test___setitem__checks_the_given_data_7(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(RuntimeError) as cm:
            wh[0] = [[3]]

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[3]]'
        )

    def test___setitem__checks_the_given_data_8(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(TypeError) as cm:
            wh[2] = [[2, 'a']]

        self.assertEqual(
            str(cm.exception),
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers between and the range of integers should be 0-1440, "
            "not [[2, 'a']]"
        )

    def test___setitem__checks_the_given_data_9(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(TypeError) as cm:
            wh[1] = [[20, 10], ['a', 300]]

        self.assertEqual(
            str(cm.exception),
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers between and the range of integers should be 0-1440, "
            "not [[20, 10], ['a', 300]]"
        )

    def test___setitem__checks_the_given_data_10(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(TypeError) as cm:
            wh[5] = [[323, 1344], [2, 'd']]

        self.assertEqual(
            str(cm.exception),
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers between and the range of integers should be 0-1440, "
            "not [[323, 1344], [2, 'd']]"
        )

    def test___setitem__checks_the_given_data_11(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(RuntimeError) as cm:
            wh[0] = [[4, 100, 3]]

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[4, 100, 3]]'
        )

    def test___setitem__checks_the_given_data_13(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(RuntimeError) as cm:
            wh['mon'] = [[3]]

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[3]]'
        )

    def test___setitem__checks_the_given_data_14(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(TypeError) as cm:
            wh['mon'] = [[2, 'a']]

        self.assertEqual(
            str(cm.exception),
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers between and the range of integers should be 0-1440, "
            "not [[2, 'a']]"
        )

    def test___setitem__checks_the_given_data_15(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(TypeError) as cm:
            wh['tue'] = [[20, 10], ['a', 300]]

        self.assertEqual(
            str(cm.exception),
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers between and the range of integers should be 0-1440, "
            "not [[20, 10], ['a', 300]]"
        )

    def test___setitem__checks_the_given_data_16(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(TypeError) as cm:
            wh['fri'] = [[323, 1344], [2, 'd']]

        self.assertEqual(
            str(cm.exception),
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers between and the range of integers should be 0-1440, "
            "not [[323, 1344], [2, 'd']]"
        )

    def test___setitem__checks_the_given_data_17(self):
        """testing if the __setitem__ checks the given data format
        """
        wh = WorkingHours()

        with self.assertRaises(RuntimeError) as cm:
            wh['sat'] = [[4, 100, 3]]

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[4, 100, 3]]'
        )

    def test___setitem__checks_the_value_ranges_1(self):
        """testing if a ValueError will be raised if value is not in the
        correct range in __setitem__
        """
        wh = WorkingHours()
        with self.assertRaises(ValueError) as cm:
            wh['sun'] = [[-10, 100]]

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[-10, 100]]'
        )

    def test___setitem__checks_the_value_ranges_2(self):
        """testing if a ValueError will be raised if value is not in the
        correct range in __setitem__
        """
        wh = WorkingHours()
        with self.assertRaises(ValueError) as cm:
            wh['sat'] = [[0, 1800]]

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.working_hours value should be a list of lists of '
            'two integers between and the range of integers should be 0-1440, '
            'not [[0, 1800]]'
        )

    def test___setitem__will_not_accept_any_other_key_or_value_1(self):
        """testing if it is possible to use the other indexes or keys
        """
        wh = WorkingHours()

        # indexing out of interested range
        with self.assertRaises(IndexError) as cm:
            wh[7] = [[32, 23], [233, 324]]

        self.assertEqual(
            str(cm.exception),
            'list index out of range'
        )

    def test___setitem__will_not_accept_any_other_key_or_value_2(self):
        """testing if it is possible to use the other indexes or keys
        """
        wh = WorkingHours()
        # indexing non existent day
        with self.assertRaises(KeyError) as cm:
            wh['zon'] = [[32, 23], [233, 324]]

        self.assertEqual(
            str(cm.exception),
            '"WorkingHours accepts only [\'mon\', \'tue\', \'wed\', \'thu\', '
            '\'fri\', \'sat\', \'sun\'] as key, not \'zon\'"'
        )

    def test_working_hours_argument_is_working_properly(self):
        """testing if the working_hours argument is working properly
        """
        import copy
        from stalker import defaults
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
        import copy
        from stalker import defaults
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
        with self.assertRaises(AttributeError) as cm:
            wh.to_tjp = 'some value'

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

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
        with self.assertRaises(AttributeError) as cm:
            wh.weekly_working_hours = 232

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

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
        import datetime
        import pytz
        check_date = datetime.datetime(2013, 4, 8, 13, 55, tzinfo=pytz.utc)
        self.assertTrue(wh.is_working_hour(check_date))

        # sunday
        check_date = datetime.datetime(2013, 4, 14, 13, 55, tzinfo=pytz.utc)
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

        from stalker import defaults
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
        with self.assertRaises(AttributeError) as cm:
            wh.weekly_working_days = 6

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

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
        with self.assertRaises(AttributeError) as cm:
            wh.yearly_working_days = 260.1

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

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
        from stalker import defaults
        self.assertEqual(wh.daily_working_hours, defaults.daily_working_hours)

    def test_daily_working_hours_argument_is_None(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings value when the daily_working_hours argument is None
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = None
        wh = WorkingHours(**kwargs)
        from stalker import defaults
        self.assertEqual(wh.daily_working_hours,
                         defaults.daily_working_hours)

    def test_daily_working_hours_attribute_is_None(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings value when it is set to None
        """
        wh = WorkingHours()
        wh.daily_working_hours = None
        from stalker import defaults
        self.assertEqual(wh.daily_working_hours, defaults.daily_working_hours)

    def test_daily_working_hours_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the daily_working_hours
        argument is not an integer
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = 'not an integer'
        with self.assertRaises(TypeError) as cm:
            WorkingHours(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.daily_working_hours should be an integer, not str'
        )

    def test_daily_working_hours_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the daily_working hours
        attribute is set to a value other than an integer
        """
        wh = WorkingHours()
        with self.assertRaises(TypeError) as cm:
            wh.daily_working_hours = 'not an integer'

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.daily_working_hours should be an integer, not str'
        )

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
        with self.assertRaises(ValueError) as cm:
            WorkingHours(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.daily_working_hours should be a positive integer '
            'value greater than 0 and smaller than or equal to 24'
        )

    def test_daily_working_hours_attribute_is_zero(self):
        """testing if a ValueError will be raised when the daily_working_hours
        attribute is set to zero
        """
        wh = WorkingHours()
        with self.assertRaises(ValueError) as cm:
            wh.daily_working_hours = 0

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.daily_working_hours should be a positive integer '
            'value greater than 0 and smaller than or equal to 24'
        )

    def test_daily_working_hours_argument_is_a_negative_number(self):
        """testing if a ValueError will be raised when the daily_working_hours
        argument value is negative
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = -10
        with self.assertRaises(ValueError) as cm:
            WorkingHours(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.daily_working_hours should be a positive integer '
            'value greater than 0 and smaller than or equal to 24'
        )

    def test_daily_working_hours_attribute_is_a_negative_number(self):
        """testing if a ValueError will be raised when the daily_working_hours
        attribute is set to a negative value
        """
        wh = WorkingHours()
        with self.assertRaises(ValueError) as cm:
            wh.daily_working_hours = -10

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.daily_working_hours should be a positive integer '
            'value greater than 0 and smaller than or equal to 24'
        )

    def test_daily_working_hours_argument_is_set_to_a_number_bigger_than_24(self):
        """testing if a ValueError will be raised when the daily working hours
        argument value is bigger than 24
        """
        kwargs = dict()
        kwargs['daily_working_hours'] = 25
        with self.assertRaises(ValueError) as cm:
            WorkingHours(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.daily_working_hours should be a positive integer '
            'value greater than 0 and smaller than or equal to 24'
        )

    def test_daily_working_hours_attribute_is_set_to_a_number_bigger_than_24(self):
        """testing if a ValueError will be raised when the daily working hours
        attribute value is bigger than 24
        """
        wh = WorkingHours()
        with self.assertRaises(ValueError) as cm:
            wh.daily_working_hours = 25

        self.assertEqual(
            str(cm.exception),
            'WorkingHours.daily_working_hours should be a positive integer '
            'value greater than 0 and smaller than or equal to 24'
        )

    def test_split_in_to_working_hours_is_not_implemented_yet(self):
        """testing if a NotimplementedError will be raised when the
        split_in_to_working_hours() method is called
        """
        with self.assertRaises(NotImplementedError):
            wh = WorkingHours()
            import datetime
            import pytz
            start = datetime.datetime.now(pytz.utc)
            end = start + datetime.timedelta(days=10)
            wh.split_in_to_working_hours(start, end)
