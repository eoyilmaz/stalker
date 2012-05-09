# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime
import unittest

from sqlalchemy import Column, Integer, ForeignKey
from stalker.conf import defaults
from stalker.models import SimpleEntity, ScheduleMixin, DBSession


class SchedMixFooMixedInClass(SimpleEntity, ScheduleMixin):
    """a class which derives from another which has and __init__ already
    """

    __tablename__ = "SchedMixFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "SchedMixFooMixedInClass"}
    schedMixFooMixedInClass_id = Column("id", Integer,
                                        ForeignKey("SimpleEntities.id"),
                                        primary_key=True)

    def __init__(self, **kwargs):
        super(SchedMixFooMixedInClass, self).__init__(**kwargs)
        ScheduleMixin.__init__(self, **kwargs)

class ScheduleMixinTester(unittest.TestCase):
    """Tests the ScheduleMixin
    """

    def setUp(self):
        """setup the test
        """

        # create mock objects

        self.start_date = datetime.date.today()
        self.due_date = self.start_date + datetime.timedelta(days=20)
        self.duration = datetime.timedelta(days=10)

        self.kwargs = {
            "name": "Test Schedule Mixin",
            "description": "This is a simple entity object for testing " +
                           "ScheduleMixin",
            "start_date": self.start_date,
            "due_date": self.due_date,
            "duration": self.duration,
            }

        self.mock_foo_obj = SchedMixFooMixedInClass(**self.kwargs)
    
    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()

    def test_start_date_argument_is_not_a_date_object(self):
        """testing if defaults will be used for the start_date attribute when
        the start_date is given as something other than a datetime.date object
        """

        test_values = [1, 1.2, "str", ["a", "date"]]

        for test_value in test_values:
            self.kwargs["start_date"] = test_value

            new_foo_obj = SchedMixFooMixedInClass(**self.kwargs)

            self.assertEqual(new_foo_obj.start_date,
                             new_foo_obj.due_date - new_foo_obj.duration)

            self.assertEqual(new_foo_obj.due_date, self.kwargs["due_date"])
            self.assertEqual(new_foo_obj.duration, self.kwargs["duration"])

    def test_start_date_attribute_is_not_a_date_object(self):
        """testing if the defaults will be used when trying to set the
        start_date attribute to something other than a datetime.date object
        """

        test_values = [1, 1.2, "str", ["a", "date"]]

        for test_value in test_values:
            due_date = self.mock_foo_obj.due_date
            duration = self.mock_foo_obj.duration

            self.mock_foo_obj.start_date = test_value

            self.assertEqual(
                self.mock_foo_obj.start_date,
                self.mock_foo_obj.due_date - self.mock_foo_obj.duration
            )

            # check if we still have the same due_date
            self.assertEqual(self.mock_foo_obj.due_date, due_date)

            # check if we still have the same duration
            self.assertEqual(self.mock_foo_obj.duration, duration)

    def test_start_date_attribute_is_set_to_None_use_the_default_value(self):
        """testing if setting the start_date attribute to None will update the
        start_date to today
        """

        self.mock_foo_obj.start_date = None
        self.assertEqual(self.mock_foo_obj.start_date, datetime.date.today())

    def test_start_date_attribute_works_properly(self):
        """testing if the start propertly is working properly
        """

        test_value = datetime.date(year=2011, month=1, day=1)
        self.mock_foo_obj.start_date = test_value
        self.assertEqual(self.mock_foo_obj.start_date, test_value)

    def test_due_date_argument_is_not_a_date_object(self):
        """testing if default values will be for the due_date attribute used
        when trying to set the due date something other than a datetime.date
        object
        """

        test_values = [1, 1.2, "str", ["a", "date"],
                       datetime.timedelta(days=100)]

        for test_value in test_values:
            self.kwargs["due_date"] = test_value
            new_foo_obj = SchedMixFooMixedInClass(**self.kwargs)

            self.assertEqual(new_foo_obj.due_date,
                             new_foo_obj.start_date + new_foo_obj.duration)

    def test_due_date_attribute_is_not_a_date_object(self):
        """testing if default values will be used for the due_date attribute
        when trying to set the due_date attribute to something other than a
        datetime.date object
        """

        test_values = [1, 1.2, "str", ["a", "date"],
                       datetime.timedelta(days=100)]

        for test_value in test_values:
            self.mock_foo_obj.due_date = test_value

            self.assertEqual(self.mock_foo_obj.due_date,
                             self.mock_foo_obj.start_date +\
                             self.mock_foo_obj.duration)

    def test_due_date_argument_is_tried_to_set_to_a_time_before_start_date(
    self):
        """testing if due_date attribute will be updated to
        start_date + duration when the due_date argument is given as a value
        which is a date before start
        """

        self.kwargs["due_date"] = self.kwargs["start_date"] -\
                                  datetime.timedelta(days=10)

        new_foo_obj = SchedMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_obj.due_date,
                         new_foo_obj.start_date + new_foo_obj.duration)


    def test_due_date_attribute_is_tried_to_set_to_a_time_before_start_date(
    self):
        """testing if a the due attribute is re calculated from the start_date
        and duration attributes when the due_date is tried to be set to a date
        before start
        """

        new_due_date = self.mock_foo_obj.start_date -\
                       datetime.timedelta(days=10)

        self.mock_foo_obj.due_date = new_due_date

        self.assertEqual(self.mock_foo_obj.due_date,
                         self.mock_foo_obj.start_date +\
                         self.mock_foo_obj.duration)

    def test_due_date_attribute_is_shifted_when_start_date_passes_it(self):
        """testing if due_date attribute will be shifted when the start_date
        attribute passes it
        """

        time_delta = self.mock_foo_obj.due_date - self.mock_foo_obj.start_date
        self.mock_foo_obj.start_date += 2 * time_delta

        self.assertEqual(
            self.mock_foo_obj.due_date - self.mock_foo_obj.start_date,
            time_delta
        )

    def test_duration_argument_is_not_an_instance_of_timedelta_no_problem_if_start_date_and_due_date_is_present(
    self):
        """testing if no error will be raised when the duration argument is not
        an instance of datetime.date class when both of the start_date and
        due_date arguments are present.
        """

        test_values = [1, 1.2, "10", "10 days"]

        # no problem if there are start_date and due_date arguments
        for test_value in test_values:
            self.kwargs["duration"] = test_value
            new_foo_obj = SchedMixFooMixedInClass(**self.kwargs)

            # check the value
            self.assertEqual(new_foo_obj.duration,
                             new_foo_obj.due_date - new_foo_obj.start_date)

    def test_duration_argument_is_not_an_instance_of_date_when_start_date_argument_is_missing(
    self):
        """testing if defaults for the duration attribute will be used  when
        the duration argument is not an instance of datetime.date class when
        start_date argument is also missing
        """

        test_values = [1, 1.2, "10", "10 days"]

        self.kwargs.pop("start_date")

        for test_value in test_values:
            self.kwargs["duration"] = test_value
            new_foo_obj = SchedMixFooMixedInClass(**self.kwargs)

            self.assertEqual(new_foo_obj.duration,
                             defaults.DEFAULT_TASK_DURATION)

    def test_duration_argument_is_not_an_instance_of_date_when_due_date_argument_is_missing(
    self):
        """testing if the defaults for the duration attribute will be used when
        the duration argument is not an instance of datetime.date class and
        when due_date argument is also missing
        """

        test_values = [1, 1.2, "10", "10 days"]

        self.kwargs.pop("due_date")

        for test_value in test_values:
            self.kwargs["duration"] = test_value
            new_foo_obj = SchedMixFooMixedInClass(**self.kwargs)
            self.assertEqual(new_foo_obj.duration,
                             defaults.DEFAULT_TASK_DURATION)

    def test_duration_attribute_is_calculated_correctly(self):
        """testing if the duration attribute is calculated correctly
        """

        new_foo_entity = SchedMixFooMixedInClass(**self.kwargs)
        new_foo_entity.start_date = datetime.date.today()
        new_foo_entity.due_date = new_foo_entity.start_date +\
                                  datetime.timedelta(201)

        self.assertEqual(new_foo_entity.duration, datetime.timedelta(201))

    def test_duration_attribute_is_set_to_not_an_instance_of_timedelta(self):
        """testing if duration attribute reset to a calculated value when it is
        set to something other than a datetime.timedelta instance
        """

        test_values = [1, 1.2, "10", "10 days"]

        # no problem if there are start_date and due_date arguments
        for test_value in test_values:
            self.mock_foo_obj.duration = test_value

            # check the value
            self.assertEqual(self.mock_foo_obj.duration,
                             self.mock_foo_obj.due_date -\
                             self.mock_foo_obj.start_date)

    def test_duration_attribute_expands_then_due_date_shifts(self):
        """testing if duration attribute is expanded then the due_date
        attribute is shifted
        """

        due_date = self.mock_foo_obj.due_date
        start_date = self.mock_foo_obj.start_date
        duration = self.mock_foo_obj.duration

        # change the duration
        new_duration = duration * 10
        self.mock_foo_obj.duration = new_duration

        # duration expanded
        self.assertEqual(self.mock_foo_obj.duration, new_duration)

        # start_date is not changed
        self.assertEqual(self.mock_foo_obj.start_date, start_date)

        # due_date is postponed
        self.assertEqual(self.mock_foo_obj.due_date, start_date + new_duration)

    def test_duration_attribute_contracts_then_due_date_shifts_back(self):
        """testing if duration attribute is contracted then the due_date
        attribute is shifted back
        """

        due_date = self.mock_foo_obj.due_date
        start_date = self.mock_foo_obj.start_date
        duration = self.mock_foo_obj.duration

        # change the duration
        new_duration = duration / 2
        self.mock_foo_obj.duration = new_duration

        # duration expanded
        self.assertEqual(self.mock_foo_obj.duration, new_duration)

        # start_date is not changed
        self.assertEqual(self.mock_foo_obj.start_date, start_date)

        # due_date is postponed
        self.assertEqual(self.mock_foo_obj.due_date, start_date + new_duration)

    def test_duration_is_a_negative_timedelta(self):
        """testing if the duration is a negative timedelta will set the
        duration to 1 days
        """

        start_date = self.mock_foo_obj.start_date

        self.mock_foo_obj.duration = datetime.timedelta(-10)

        self.assertEqual(self.mock_foo_obj.duration, datetime.timedelta(1))
        self.assertEqual(self.mock_foo_obj.start_date, start_date)

    def test_init_all_parameters_skipped(self):
        """testing if the attributes are initialized to:
        
        start_date = datetime.date.today()
        duration = stalker.conf.defaults.DEFAULT_TASK_DURATION
        due_date = start_date + duration
        """

        #self.fail("test is not implemented yet")
        self.kwargs.pop("start_date")
        self.kwargs.pop("due_date")
        self.kwargs.pop("duration")

        new_foo_entity = SchedMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.start_date, datetime.date.today())
        self.assertEqual(new_foo_entity.duration,
                         defaults.DEFAULT_TASK_DURATION)
        self.assertEqual(new_foo_entity.due_date,
                         new_foo_entity.start_date + new_foo_entity.duration)

    def test_init_only_start_date_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        duration = stalker.conf.defaults.DEFAULT_TASK_DURATION
        due_date = start_date + duration
        """

        self.kwargs.pop("due_date")
        self.kwargs.pop("duration")

        new_foo_entity = SchedMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.duration,
                         defaults.DEFAULT_TASK_DURATION)
        self.assertEqual(new_foo_entity.due_date,
                         new_foo_entity.start_date + new_foo_entity.duration)

    def test_init_start_date_and_due_date_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        duration = due_date - start_date
        """

        self.kwargs.pop("duration")

        new_foo_entity = SchedMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.duration,
                         new_foo_entity.due_date - new_foo_entity.start_date)

    def test_init_start_date_and_duration_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        due_date = start_date + duration
        """

        self.kwargs.pop("due_date")

        new_foo_entity = SchedMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.due_date,
                         new_foo_entity.start_date + new_foo_entity.duration)

    def test_init_all_arguments_are_given(self):
        """testing if the attributes are initialized to:
        
        duration = due_date - start_date
        """

        new_foo_entity = SchedMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.duration,
                         new_foo_entity.due_date - new_foo_entity.start_date)

    def test_init_due_date_and_duration_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        start_date = due_date - duration
        """

        self.kwargs.pop("start_date")

        new_foo_entity = SchedMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.start_date,
                         new_foo_entity.due_date - new_foo_entity.duration)

    def test_init_only_due_date_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        duration = stalker.conf.defaults.DEFAFULT_TASK_DURATION
        start_date = due_date - duration
        """

        self.kwargs.pop("duration")
        self.kwargs.pop("start_date")

        new_foo_entity = SchedMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.duration,
                         defaults.DEFAULT_TASK_DURATION)
        self.assertEqual(new_foo_entity.start_date,
                         new_foo_entity.due_date - new_foo_entity.duration)

    def test_init_only_duration_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        start_date = datetime.date.today()
        due_date = start_date + duration
        """

        self.kwargs.pop("due_date")
        self.kwargs.pop("start_date")

        new_foo_entity = SchedMixFooMixedInClass(**self.kwargs)

        self.assertEqual(new_foo_entity.start_date, datetime.date.today())
        self.assertEqual(new_foo_entity.due_date,
                         new_foo_entity.start_date + new_foo_entity.duration)







