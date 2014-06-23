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

import datetime
import unittest

from sqlalchemy import Column, Integer, ForeignKey

from stalker import db
from stalker import defaults
from stalker.db.session import DBSession
from stalker.models.entity import SimpleEntity
from stalker.models.mixins import DateRangeMixin

import logging
logging.getLogger('stalker.models.studio').setLevel(logging.DEBUG)


class DateRangeMixFooMixedInClass(SimpleEntity, DateRangeMixin):
    """a class which derives from another which has and __init__ already
    """
    __tablename__ = "DateRangeMixFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "DateRangeMixFooMixedInClass"}
    schedMixFooMixedInClass_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )

    def __init__(self, **kwargs):
        super(DateRangeMixFooMixedInClass, self).__init__(**kwargs)
        DateRangeMixin.__init__(self, **kwargs)


class DateRangeMixinTester(unittest.TestCase):
    """Tests the DateRangeMixin
    """

    def setUp(self):
        """setup the test
        """
        # create mock objects
        self.start = datetime.datetime(2013, 3, 22, 15, 15)
        self.end = self.start + datetime.timedelta(days=20)
        self.duration = datetime.timedelta(days=10)

        self.kwargs = {
            'name': 'Test Daterange Mixin',
            'description': 'This is a simple entity object for testing '
                           'DateRangeMixin',
            'start': self.start,
            'end': self.end,
            'duration': self.duration
        }
        db.setup({'sqlalchemy.url': 'sqlite:///:memory:'})
        self.test_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)

    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()
        # restore defaults.timing_resolution
        defaults.timing_resolution = datetime.timedelta(hours=1)

    def test_start_argument_is_not_a_date_object(self):
        """testing if defaults will be used for the start attribute when
        the start is given as something other than a datetime.datetime object
        """
        test_values = [1, 1.2, "str", ["a", "date"]]

        for test_value in test_values:
            self.kwargs["start"] = test_value

            new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)

            self.assertEqual(new_foo_obj.start,
                             new_foo_obj.end - new_foo_obj.duration)

            # the values are rounded can not check anymore
            #self.assertEqual(new_foo_obj.end, self.kwargs["end"])
            #self.assertEqual(new_foo_obj.duration, self.kwargs["duration"])

    def test_start_attribute_is_not_a_date_object(self):
        """testing if the defaults will be used when trying to set the
        start attribute to something other than a datetime.datetime object
        """
        test_values = [1, 1.2, "str", ["a", "date"]]

        for test_value in test_values:
            end = self.test_foo_obj.end
            duration = self.test_foo_obj.duration

            self.test_foo_obj.start = test_value

            self.assertEqual(
                self.test_foo_obj.start,
                self.test_foo_obj.end - self.test_foo_obj.duration
            )

            # check if we still have the same end
            self.assertEqual(self.test_foo_obj.end, end)

            # check if we still have the same duration
            self.assertEqual(self.test_foo_obj.duration, duration)

    def test_start_attribute_is_set_to_None_use_the_default_value(self):
        """testing if setting the start attribute to None will update the
        start to today
        """
        self.test_foo_obj.start = None
        self.assertEqual(
            self.test_foo_obj.start,
            datetime.datetime(2013, 3, 22, 15, 00)
        )
        self.assertTrue(isinstance(self.test_foo_obj.start, datetime.datetime))

    def test_start_attribute_works_properly(self):
        """testing if the start properly is working properly
        """
        test_value = datetime.datetime(year=2011, month=1, day=1)
        self.test_foo_obj.start = test_value
        self.assertEqual(self.test_foo_obj.start, test_value)

    def test_end_argument_is_not_a_date_object(self):
        """testing if default values will be for the end attribute used when
        trying to set the due date something other than a datetime.datetime
        object
        """
        test_values = [1, 1.2, "str", ["a", "date"],
                       datetime.timedelta(days=100)]

        for test_value in test_values:
            self.kwargs["end"] = test_value
            new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)

            self.assertEqual(new_foo_obj.end,
                             new_foo_obj.start + new_foo_obj.duration)

    def test_end_attribute_is_not_a_date_object(self):
        """testing if default values will be used for the end attribute
        when trying to set the end attribute to something other than a
        datetime.datetime object
        """
        test_values = [1, 1.2, "str", ["a", "date"],
                       datetime.timedelta(days=100)]

        for test_value in test_values:
            self.test_foo_obj.end = test_value

            self.assertEqual(self.test_foo_obj.end,
                             self.test_foo_obj.start + \
                             self.test_foo_obj.duration)

    def test_end_argument_is_tried_to_set_to_a_time_before_start(self):
        """testing if end attribute will be updated to
        start + duration when the end argument is given as a value
        which is a date before start
        """

        self.kwargs["end"] = self.kwargs["start"] - \
                             datetime.timedelta(days=10)

        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_obj.end,
                         new_foo_obj.start + new_foo_obj.duration)

    def test_end_attribute_is_tried_to_set_to_a_time_before_start(self):
        """testing if a the due attribute is re calculated from the start
        and duration attributes when the end is tried to be set to a date
        before start
        """
        new_end = self.test_foo_obj.start - datetime.timedelta(days=10)
        self.test_foo_obj.end = new_end
        self.assertEqual(self.test_foo_obj.end,
                         self.test_foo_obj.start + \
                         self.test_foo_obj.duration)

    def test_end_attribute_is_shifted_when_start_passes_it(self):
        """testing if end attribute will be shifted when the start
        attribute passes it
        """
        time_delta = self.test_foo_obj.end - self.test_foo_obj.start
        self.test_foo_obj.start += 2 * time_delta

        self.assertEqual(
            self.test_foo_obj.end - self.test_foo_obj.start,
            time_delta
        )

    def test_duration_argument_is_not_an_instance_of_timedelta_no_problem_if_start_and_end_is_present(self):
        """testing if no error will be raised when the duration argument is not
        an instance of datetime.datetime class when both of the start and end
        arguments are present.
        """
        test_values = [1, 1.2, "10", "10 days"]

        # no problem if there are start and end arguments
        for test_value in test_values:
            self.kwargs["duration"] = test_value
            new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)

            # check the value
            self.assertEqual(new_foo_obj.duration,
                             new_foo_obj.end - new_foo_obj.start)

    def test_duration_argument_is_not_an_instance_of_date_when_start_argument_is_missing(self):
        """testing if defaults.timing_resolution will be used when the duration
        argument is not an instance of datetime.datetime class when start
        argument is also missing
        """
        test_values = [1, 1.2, "10", "10 days"]
        self.kwargs.pop("start")
        for test_value in test_values:
            self.kwargs["duration"] = test_value
            new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
            self.assertEqual(
                new_foo_obj.duration,
                defaults.timing_resolution
            )

    def test_duration_argument_is_not_an_instance_of_date_when_end_argument_is_missing(self):
        """testing if the defaults.timing_resolution will be used when the
        duration argument is not an instance of datetime.datetime class and
        when end argument is also missing
        """
        defaults.timing_resolution = datetime.timedelta(hours=1)
        # some wrong values for the duration
        test_values = [1, 1.2, "10", "10 days"]
        self.kwargs.pop("end")

        for test_value in test_values:
            self.kwargs["duration"] = test_value
            new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
            self.assertEqual(
                new_foo_obj.duration,
                defaults.timing_resolution
            )

    def test_duration_argument_is_smaller_than_timing_resolution(self):
        """testing if the defaults.timing_resolution will be used as for the
        duration value when the duration argument is smaller than the
        defaults.timing_resolution
        """
        self.kwargs.pop("end")
        self.kwargs['duration'] = datetime.timedelta(minutes=1)
        obj = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertEqual(
            obj.start,
            datetime.datetime(2013, 3, 22, 15, 0)
        )
        self.assertEqual(
            obj.end,
            datetime.datetime(2013, 3, 22, 16, 0)
        )

    def test_duration_attribute_is_calculated_correctly(self):
        """testing if the duration attribute is calculated correctly
        """
        new_foo_entity = DateRangeMixFooMixedInClass(**self.kwargs)
        new_foo_entity.start = datetime.datetime(2013, 3, 22, 15, 0)
        new_foo_entity.end = new_foo_entity.start + \
                             datetime.timedelta(201)

        self.assertEqual(new_foo_entity.duration, datetime.timedelta(201))

    def test_duration_attribute_is_set_to_not_an_instance_of_timedelta(self):
        """testing if duration attribute reset to a calculated value when it is
        set to something other than a datetime.timedelta instance
        """
        test_values = [1, 1.2, "10", "10 days"]

        # no problem if there are start and end arguments
        for test_value in test_values:
            self.test_foo_obj.duration = test_value

            # check the value
            self.assertEqual(self.test_foo_obj.duration,
                             self.test_foo_obj.end - \
                             self.test_foo_obj.start)

    def test_duration_attribute_expands_then_end_shifts(self):
        """testing if duration attribute is expanded then the end
        attribute is shifted
        """
        end = self.test_foo_obj.end
        start = self.test_foo_obj.start
        duration = self.test_foo_obj.duration

        # change the duration
        new_duration = duration * 10
        self.test_foo_obj.duration = new_duration

        # duration expanded
        self.assertEqual(self.test_foo_obj.duration, new_duration)

        # start is not changed
        self.assertEqual(self.test_foo_obj.start, start)

        # end is postponed
        self.assertEqual(self.test_foo_obj.end, start + new_duration)

    def test_duration_attribute_contracts_then_end_shifts_back(self):
        """testing if duration attribute is contracted then the end
        attribute is shifted back
        """
        end = self.test_foo_obj.end
        start = self.test_foo_obj.start
        duration = self.test_foo_obj.duration

        # change the duration
        new_duration = duration / 2
        self.test_foo_obj.duration = new_duration

        # duration expanded
        self.assertEqual(self.test_foo_obj.duration, new_duration)

        # start is not changed
        self.assertEqual(self.test_foo_obj.start, start)

        # end is postponed
        self.assertEqual(self.test_foo_obj.end, start + new_duration)

    def test_duration_attribute_is_smaller_then_timing_resolution(self):
        """testing if the defaults.timing_resolution will be used as for the
        duration value when the given value for the duration attribute is
        smaller then the defaults.timing_resolution
        """
        self.test_foo_obj.duration = datetime.timedelta(minutes=10)
        self.assertEqual(
            self.test_foo_obj.duration,
            defaults.timing_resolution
        )

    def test_duration_is_a_negative_timedelta(self):
        """testing if the duration is a negative timedelta will set the
        duration to 1 days
        """
        start = self.test_foo_obj.start
        self.test_foo_obj.duration = datetime.timedelta(-10)
        self.assertEqual(self.test_foo_obj.duration, datetime.timedelta(1))
        self.assertEqual(self.test_foo_obj.start, start)

    def test_init_all_parameters_skipped(self):
        """testing if the attributes are initialized to:

        start = datetime.datetime.now()
        duration = stalker.config.Config.timing_resolution
        end = start + duration
        """
        #self.fail("test is not implemented yet")
        self.kwargs.pop("start")
        self.kwargs.pop("end")
        self.kwargs.pop("duration")

        new_foo_entity = DateRangeMixFooMixedInClass(**self.kwargs)

        self.assertTrue(isinstance(new_foo_entity.start, datetime.datetime))
        # can not check for start, just don't want to struggle with the round
        # thing
        #self.assertEqual(new_foo_entity.start,
        #                 datetime.datetime(2013, 3, 22, 15, 30))
        self.assertEqual(new_foo_entity.duration,
                         defaults.timing_resolution)
        self.assertEqual(new_foo_entity.end,
                         new_foo_entity.start + new_foo_entity.duration)

    def test_init_only_start_argument_is_given(self):
        """testing if the attributes are initialized to:

        duration = defaults.timing_resolution
        end = start + duration
        """
        self.kwargs.pop("end")
        self.kwargs.pop("duration")

        new_foo_entity = DateRangeMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.duration, defaults.timing_resolution)
        self.assertEqual(new_foo_entity.end,
                         new_foo_entity.start + new_foo_entity.duration)

    def test_init_start_and_end_argument_is_given(self):
        """testing if the attributes are initialized to:

        duration = end - start
        """
        self.kwargs.pop("duration")
        new_foo_entity = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertEqual(new_foo_entity.duration,
                         new_foo_entity.end - new_foo_entity.start)

    def test_init_start_and_end_argument_is_given_but_duration_is_smaller_than_timing_resolution(self):
        """testing if the start will be anchored and the end will be
        recalculated when the start and end values are given but the calculated
        duration is smaller than timing_resolution

        duration = end - start
        """
        self.kwargs.pop("duration")
        self.kwargs['start'] = datetime.datetime(2013, 12, 22, 23, 8)
        self.kwargs['end'] = datetime.datetime(2013, 12, 22, 23, 15)
        obj = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertEqual(obj.start, datetime.datetime(2013, 12, 22, 23, 0))
        self.assertEqual(obj.end, datetime.datetime(2013, 12, 23, 0, 0))

    def test_init_start_and_duration_argument_is_given(self):
        """testing if the attributes are initialized to:

        end = start + duration
        """

        self.kwargs.pop("end")

        new_foo_entity = DateRangeMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.end,
                         new_foo_entity.start + new_foo_entity.duration)

    def test_init_all_arguments_are_given(self):
        """testing if the attributes are initialized to:

        duration = end - start
        """
        new_foo_entity = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertEqual(new_foo_entity.duration,
                         new_foo_entity.end - new_foo_entity.start)

    def test_init_end_and_duration_argument_is_given(self):
        """testing if the attributes are initialized to:

        start = end - duration
        """
        self.kwargs.pop("start")
        new_foo_entity = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertEqual(new_foo_entity.start,
                         new_foo_entity.end - new_foo_entity.duration)

    def test_init_only_end_argument_is_given(self):
        """testing if the attributes are initialized to:

        duration = defaults.timing_resolution
        start = end - duration
        """
        self.kwargs.pop("duration")
        self.kwargs.pop("start")
        new_foo_entity = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertEqual(new_foo_entity.duration,
                         defaults.timing_resolution)
        self.assertEqual(new_foo_entity.start,
                         new_foo_entity.end - new_foo_entity.duration)

    def test_init_only_duration_argument_is_given(self):
        """testing if the attributes are initialized to:

        start = datetime.date.today()
        end = start + duration
        """
        self.kwargs.pop("end")
        self.kwargs.pop("start")

        new_foo_entity = DateRangeMixFooMixedInClass(**self.kwargs)

        # just check if it is an instance of datetime.datetime
        self.assertTrue(isinstance(new_foo_entity.start, datetime.datetime))
        # can not check for start
        #self.assertEqual(new_foo_entity.start,
        #                 datetime.datetime(2013, 3, 22, 15, 30))
        self.assertEqual(new_foo_entity.end,
                         new_foo_entity.start + new_foo_entity.duration)

    def test_start_end_and_duration_values_are_rounded_to_the_default_timing_resolution(self):
        """testing if the start and end dates are rounded to the default
        timing_resolution (no Studio)
        """
        self.kwargs['start'] = datetime.datetime(2013, 3, 22, 2, 38, 55, 531)
        self.kwargs['end'] = datetime.datetime(2013, 3, 24, 16, 46, 32, 102)
        defaults.timing_resolution = datetime.timedelta(minutes=5)

        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        # check the start
        expected_start = datetime.datetime(2013, 3, 22, 2, 40)
        self.assertEqual(new_foo_obj.start, expected_start)
        # check the end
        expected_end = datetime.datetime(2013, 3, 24, 16, 45)
        self.assertEqual(new_foo_obj.end, expected_end)
        # check the duration
        self.assertEqual(new_foo_obj.duration, expected_end - expected_start)

    def test_start_end_and_duration_values_are_rounded_to_the_Studio_timing_resolution(self):
        """testing if the start and end dates are rounded to the Studio
        timing_resolution
        """
        from stalker.models.studio import Studio
        studio = Studio(
            name='Test Studio',
            timing_resolution=datetime.timedelta(minutes=5)
        )
        DBSession.add(studio)
        DBSession.commit()
        self.kwargs['start'] = datetime.datetime(2013, 3, 22, 2, 38, 55, 531)
        self.kwargs['end'] = datetime.datetime(2013, 3, 24, 16, 46, 32, 102)

        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        # check the start
        expected_start = datetime.datetime(2013, 3, 22, 2, 40)
        self.assertEqual(new_foo_obj.start, expected_start)
        # check the end
        expected_end = datetime.datetime(2013, 3, 24, 16, 45)
        self.assertEqual(new_foo_obj.end, expected_end)
        # check the duration
        self.assertEqual(new_foo_obj.duration, expected_end - expected_start)

    def test_computed_start_is_None_for_a_non_scheduled_class(self):
        """testing if the computed_start attribute is None for a non scheduled
        class
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertTrue(new_foo_obj.computed_start is None)

    def test_computed_end_is_None_for_a_non_scheduled_class(self):
        """testing if the computed_end attribute is None for a non scheduled
        class
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertTrue(new_foo_obj.computed_end is None)

    def test_computed_duration_attribute_is_None_if_there_is_no_computed_start_and_no_computed_end(self):
        """testing if the computed_start attribute is None if there is no
        computed_start and no computed_end
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        new_foo_obj.computed_start = None
        new_foo_obj.computed_end = None
        self.assertTrue(new_foo_obj.computed_duration is None)

    def test_computed_duration_attribute_is_None_if_there_is_computed_start_but_no_computed_end(self):
        """testing if the computed_start attribute is None if there is
        computed_start but no computed_end
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        new_foo_obj.computed_start = datetime.datetime.now()
        new_foo_obj.computed_end = None
        self.assertTrue(new_foo_obj.computed_duration is None)

    def test_computed_duration_attribute_is_None_if_there_is_no_computed_start_but_computed_end(self):
        """testing if the computed_start attribute is None if there is no
        computed_start but computed_end
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        new_foo_obj.computed_start = None
        new_foo_obj.computed_end = datetime.datetime.now()
        self.assertTrue(new_foo_obj.computed_duration is None)

    def test_computed_duration_attribute_is_calculated_correctly_when_there_are_both_computed_start_and_computed_end(self):
        """testing if the computed_duration is calculated correctly when there
        are both computed_start and computed_end values
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        new_foo_obj.computed_start = datetime.datetime.now()
        new_foo_obj.computed_end = \
            new_foo_obj.computed_start + datetime.timedelta(12)
        self.assertEqual(new_foo_obj.computed_duration, datetime.timedelta(12))

    def test_computed_duration_is_read_only(self):
        """testing if the computed_duration attribute is read-only
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertRaises(AttributeError, setattr, new_foo_obj,
                          'computed_duration', datetime.timedelta(10))

    def test_total_seconds_attribute_is_read_only(self):
        """testing if the total_seconds is read only
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertRaises(
            AttributeError,
            setattr,
            new_foo_obj,
            'total_seconds',
            234234
        )

    def test_total_seconds_attribute_is_working_properly(self):
        """testing is the total_seconds is read only
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        new_foo_obj.start = datetime.datetime(2013, 5, 31, 10, 0)
        new_foo_obj.end = datetime.datetime(2013, 5, 31, 18, 0)
        self.assertEqual(
            new_foo_obj.total_seconds,
            8 * 60 * 60
        )

    def test_computed_total_seconds_attribute_is_read_only(self):
        """testing if the computed_total_seconds is read only
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        self.assertRaises(
            AttributeError,
            setattr,
            new_foo_obj,
            'computed_total_seconds',
            234234
        )

    def test_computed_total_seconds_attribute_is_working_properly(self):
        """testing is the computed_total_seconds is read only
        """
        new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
        new_foo_obj.computed_start = datetime.datetime(2013, 5, 31, 10, 0)
        new_foo_obj.computed_end = datetime.datetime(2013, 5, 31, 18, 0)
        self.assertEqual(
            new_foo_obj.computed_total_seconds,
            8 * 60 * 60
        )
