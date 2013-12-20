# -*- coding: utf-8 -*-
# stalker_pyramid
# Copyright (C) 2013 Erkan Ozgur Yilmaz
#
# This file is part of stalker_pyramid.
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

import unittest2
from sqlalchemy import Column, Integer, ForeignKey
from stalker import SimpleEntity, ScheduleMixin, defaults


class MixedInClass(SimpleEntity, ScheduleMixin):
    """A simple class derived from SimpleEntity and mixed in with ScheduleMixin
    used for tests
    """

    __tablename__ = "ScheduleMixFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "ScheduleMixFooMixedInClass"}
    schedMixFooMixedInClass_id = Column(
        "id", Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )

    def __init__(self, **kwargs):
        SimpleEntity.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)


class ScheduleMixinTestCase(unittest2.TestCase):
    """tests the ScheduleMixin
    """

    def setUp(self):
        """set up the test
        """
        self.kwargs = {
            'name': 'Test Object',
            'schedule_timing': 1,
            'schedule_unit': 'h',
            'schedule_model': 'effort',
            'schedule_constraint': 0
        }
        self.test_obj = MixedInClass(**self.kwargs)

    def tearDown(self):
        from stalker import db
        db.DBSession.remove()

    def test_schedule_model_attribute_is_effort_by_default(self):
        """testing if the schedule_model is effort by default
        """
        self.assertEqual(self.test_obj.schedule_model, 'effort')

    def test_schedule_model_argument_is_None(self):
        """testing if the schedule model attribute will be 'effort' if the
        schedule_model argument is set to None
        """
        self.kwargs['schedule_model'] = None
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(
            new_task.schedule_model,
            'effort'
        )

    def test_schedule_model_attribute_is_set_to_None(self):
        """testing if the schedule_model will be 'effort' if it is set to None
        """
        self.test_obj.schedule_model = None
        self.assertEqual(
            self.test_obj.schedule_model,
            'effort'
        )

    def test_schedule_model_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the schedule_model
        argument is not a string
        """
        self.kwargs['schedule_model'] = 234
        self.assertRaises(TypeError, MixedInClass, **self.kwargs)

    def test_schedule_model_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the schedule_model
        attribute is set to a value other than a string
        """
        self.assertRaises(
            TypeError, setattr, self.test_obj, 'schedule_model', 2343
        )

    def test_schedule_model_argument_is_not_in_correct_value(self):
        """testing if a ValueError will be raised when the schedule_model
        argument is not in correct value
        """
        self.kwargs['schedule_model'] = 'not in the list'
        self.assertRaises(ValueError, MixedInClass, **self.kwargs)

    def test_schedule_model_attribute_is_not_in_correct_value(self):
        """testing if a ValueError will be raised when the schedule_model
        attribute is not set to a correct value
        """
        self.assertRaises(
            ValueError, setattr, self.test_obj, 'schedule_model',
            'not in the list'
        )

    def test_schedule_model_argument_is_working_properly(self):
        """testing if the schedule_model argument value is correctly passed to
        the schedule_model attribute
        """
        test_value = 'duration'
        self.kwargs['schedule_model'] = test_value
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(new_task.schedule_model, test_value)

    def test_schedule_model_attribute_is_working_properly(self):
        """testing if the schedule_model attribute is working properly
        """
        test_value = 'duration'
        self.assertNotEqual(
            self.test_obj.schedule_model, test_value
        )
        self.test_obj.schedule_model = test_value
        self.assertEqual(
            self.test_obj.schedule_model, test_value
        )

    def test_schedule_constraint_is_0_by_default(self):
        """testing if the schedule_constraint attribute is None by default
        """
        self.assertEqual(self.test_obj.schedule_constraint, 0)

    def test_schedule_constraint_argument_is_skipped(self):
        """testing if the schedule_constraint attribute will be 0 if
        schedule_constraint is skipped
        """
        try:
            self.kwargs.pop('schedule_constraint')
        except KeyError:
            pass
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, 0)

    def test_schedule_constraint_argument_is_None(self):
        """testing if the schedule_constraint attribute will be 0 if
        schedule_constraint is None
        """
        self.kwargs['schedule_constraint'] = None
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, 0)

    def test_schedule_constraint_attribute_is_set_to_None(self):
        """testing if the schedule_constraint attribute will be 0 if
        it is set to None
        """
        self.test_obj.schedule_constraint = None
        self.assertEqual(self.test_obj.schedule_constraint, 0)

    def test_schedule_constraint_argument_is_not_an_integer(self):
        """testing if a TypeError will be raised when the schedule_constraint
        argument is not an integer
        """
        self.kwargs['schedule_constraint'] = 'not an integer'
        self.assertRaises(TypeError, MixedInClass, **self.kwargs)

    def test_schedule_constraint_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the schedule_constraint
        attribute is set to a value other than an integer
        """
        self.assertRaises(TypeError, setattr, self.test_obj,
                          'schedule_constraint', 'not an integer')

    def test_schedule_constraint_argument_is_working_properly(self):
        """testing if the schedule_constraint argument value is correctly
        passed to schedule_constraint attribute
        """
        test_value = 2
        self.kwargs['schedule_constraint'] = test_value
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, test_value)

    def test_schedule_constraint_attribute_is_working_properly(self):
        """testing if the schedule_constraint attribute value is correctly
        changed
        """
        test_value = 3
        self.test_obj.schedule_constraint = test_value
        self.assertEqual(self.test_obj.schedule_constraint, test_value)

    def test_schedule_constraint_argument_value_is_out_of_range(self):
        """testing if the value of schedule_constraint argument value will be
        clamped to the [0-3] range if it is out of range
        """
        self.kwargs['schedule_constraint'] = -1
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, 0)

        self.kwargs['schedule_constraint'] = 4
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(new_task.schedule_constraint, 3)

    def test_schedule_constraint_attribute_value_is_out_of_range(self):
        """testing if the value of schedule_constraint attribute value will be
        clamped to the [0-3] range if it is out of range
        """
        self.test_obj.schedule_constraint = -1
        self.assertEqual(self.test_obj.schedule_constraint, 0)

        self.test_obj.schedule_constraint = 4
        self.assertEqual(self.test_obj.schedule_constraint, 3)

    def test_schedule_timing_argument_skipped(self):
        """testing if the schedule_timing attribute will be equal to 1 hour if
        the schedule_timing argument is skipped
        """
        self.kwargs.pop("schedule_timing")
        new_task = MixedInClass(**self.kwargs)

        self.assertEqual(new_task.schedule_timing, 1)

    def test_schedule_timing_argument_is_None(self):
        """testing if the schedule_timing attribute will be equal to the
        stalker.config.Config.timing_resolutio.seconds/3600 if the
        schedule_timing argument is None
        """
        self.kwargs["schedule_timing"] = None
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(
            new_task.schedule_timing,
            defaults.timing_resolution.seconds / 60.0
        )

    def test_schedule_timing_attribute_is_set_to_None(self):
        """testing if the schedule_timing attribute will be equal to the
        stalker.config.Config.timing_resolution.seconds/3600 if it is set to
        None
        """
        self.test_obj.schedule_timing = None
        self.assertEqual(
            self.test_obj.schedule_timing,
            defaults.timing_resolution.seconds / 60.0
        )

    def test_schedule_timing_argument_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised when the schedule_timing
        is not an integer or float
        """
        self.kwargs["schedule_timing"] = '10d'
        self.assertRaises(TypeError, MixedInClass, **self.kwargs)

    def test_schedule_timing_attribute_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised when the schedule_timing
        attribute is not set to an integer or float
        """
        self.assertRaises(TypeError, setattr, self.test_obj,
                          'schedule_timing', '10d')

    def test_schedule_timing_attribute_is_working_properly(self):
        """testing if the schedule_timing attribute is working properly
        """
        test_value = 18
        self.test_obj.schedule_timing = test_value
        self.assertEqual(self.test_obj.schedule_timing, test_value)

    def test_schedule_unit_argument_skipped(self):
        """testing if the schedule_unit attribute will be 'h' if the
        schedule_unit argument is skipped
        """
        self.kwargs.pop("schedule_unit")
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(new_task.schedule_unit, 'h')

    def test_schedule_unit_argument_is_None(self):
        """testing if the schedule_unit attribute will be 'h' if the
        schedule_unit argument is None
        """
        self.kwargs["schedule_unit"] = None
        new_task = MixedInClass(**self.kwargs)
        self.assertEqual(new_task.schedule_unit, 'h')

    def test_schedule_unit_attribute_is_set_to_None(self):
        """testing if the schedule_unit attribute will be 'h' if it is set to
        None
        """
        self.test_obj.schedule_unit = None
        self.assertEqual(self.test_obj.schedule_unit, 'h')

    def test_schedule_unit_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the schedule_unit is not
        an integer
        """
        self.kwargs["schedule_unit"] = 10
        self.assertRaises(TypeError, MixedInClass, **self.kwargs)

    def test_schedule_unit_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the schedule_unit
        attribute is not set to a string
        """
        self.assertRaises(TypeError, setattr, self.test_obj, 'schedule_unit',
                          23)

    def test_schedule_unit_attribute_is_working_properly(self):
        """testing if the schedule_unit attribute is working properly
        """
        test_value = 'w'
        self.test_obj.schedule_unit = test_value
        self.assertEqual(self.test_obj.schedule_unit, test_value)

    def test_schedule_unit_argument_value_is_not_in_defaults_datetime_units(self):
        """testing if a ValueError will be raised when the schedule_unit value
        is not in stalker.config.Config.datetime_units list
        """
        self.kwargs['schedule_unit'] = 'os'
        self.assertRaises(ValueError, MixedInClass, **self.kwargs)

    def test_schedule_unit_attribute_value_is_not_in_defaults_datetime_units(self):
        """testing if a ValueError will be raised when it is set to a value
        which is not in stalker.config.Config.datetime_units list
        """
        self.assertRaises(ValueError, setattr, self.test_obj, 'schedule_unit',
                          'so')

