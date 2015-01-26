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

import unittest
from stalker.models.budget import Good


class GoodTestCase(unittest.TestCase):
    """tests the stalker.models.budget.Good class
    """

    def setUp(self):
        """set up the test
        """
        self.kwargs = {
            'name': 'Comp',
            'cost': 10,
            'msrp': 12,
            'unit': 'TL/hour'
        }

    def test_cost_argument_is_skipped(self):
        """testing if the cost attribute value will be 0.0 if the cost argument
        is skipped
        """
        self.kwargs.pop('cost')
        g = Good(**self.kwargs)
        self.assertEqual(g.cost, 0)

    def test_cost_argument_is_None(self):
        """testing if the cost attribute value will be 0.0 if the cost argument
        is None
        """
        self.kwargs['cost'] = None
        g = Good(**self.kwargs)
        self.assertEqual(g.cost, 0)

    def test_cost_attribute_is_None(self):
        """testing if the cost attribute will be 0.0 if it is set to None
        """
        g = Good(**self.kwargs)
        self.assertNotEqual(g.cost, 0)
        g.cost = None
        self.assertEqual(g.cost, 0)

    def test_cost_argument_is_not_a_number(self):
        """testing if a TypeError will be raised if cost argument is not a
        number
        """
        self.kwargs['cost'] = 'not a number'
        with self.assertRaises(TypeError) as cm:
            g = Good(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Good.cost should be a non-negative number, not str'
        )

    def test_cost_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if the cost attribute is set
        to something other than a number
        """
        g = Good(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            g.cost = 'not a number'

        self.assertEqual(
            str(cm.exception),
            'Good.cost should be a non-negative number, not str'
        )

    def test_cost_argument_is_zero(self):
        """testing if it is totally ok to set the cost to 0
        """
        self.kwargs['cost'] = 0
        g = Good(**self.kwargs)
        self.assertEqual(
            g.cost,
            0.0
        )

    def test_cost_attribute_is_zero(self):
        """testing if it is totally ok to test the cost attribute to 0
        """
        g = Good(**self.kwargs)
        self.assertNotEqual(g.cost, 0.0)
        g.cost = 0.0
        self.assertEqual(
            g.cost,
            0.0
        )

    def test_cost_argument_is_negative(self):
        """testing if a ValueError will be raised if the cost argument is a
        negative number
        """
        self.kwargs['cost'] = -10
        with self.assertRaises(ValueError) as cm:
            g = Good(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Good.cost should be a non-negative number'
        )

    def test_cost_attribute_is_negative(self):
        """testing if ValueError will be raised if the cost attribute is set to
        a negative number
        """
        g = Good(**self.kwargs)
        with self.assertRaises(ValueError) as cm:
            g.cost = -10

        self.assertEqual(
            str(cm.exception),
            'Good.cost should be a non-negative number'
        )

    def test_cost_argument_is_working_properly(self):
        """testing if the cost argument value is properly passed to the cost
        attribute
        """
        test_value = 113
        self.kwargs['cost'] = test_value
        g = Good(**self.kwargs)
        self.assertEqual(
            g.cost,
            test_value
        )

    def test_cost_attribute_is_working_properly(self):
        """testing if the cost attribute value can be properly changed
        """
        test_value = 145
        g = Good(**self.kwargs)
        self.assertNotEqual(
            g.cost,
            test_value
        )
        g.cost = test_value
        self.assertEqual(
            g.cost,
            test_value
        )

    def test_msrp_argument_is_skipped(self):
        """testing if the msrp attribute value will be 0.0 if the msrp argument
        is skipped
        """
        self.kwargs.pop('msrp')
        g = Good(**self.kwargs)
        self.assertEqual(g.msrp, 0)

    def test_msrp_argument_is_None(self):
        """testing if the msrp attribute value will be 0.0 if the msrp argument
        is None
        """
        self.kwargs['msrp'] = None
        g = Good(**self.kwargs)
        self.assertEqual(g.msrp, 0)

    def test_msrp_attribute_is_None(self):
        """testing if the msrp attribute will be 0.0 if it is set to None
        """
        g = Good(**self.kwargs)
        self.assertNotEqual(g.msrp, 0)
        g.msrp = None
        self.assertEqual(g.msrp, 0)

    def test_msrp_argument_is_not_a_number(self):
        """testing if a TypeError will be raised if msrp argument is not a
        number
        """
        self.kwargs['msrp'] = 'not a number'
        with self.assertRaises(TypeError) as cm:
            g = Good(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Good.msrp should be a non-negative number, not str'
        )

    def test_msrp_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if the msrp attribute is set
        to something other than a number
        """
        g = Good(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            g.msrp = 'not a number'

        self.assertEqual(
            str(cm.exception),
            'Good.msrp should be a non-negative number, not str'
        )

    def test_msrp_argument_is_zero(self):
        """testing if it is totally ok to set the msrp to 0
        """
        self.kwargs['msrp'] = 0
        g = Good(**self.kwargs)
        self.assertEqual(
            g.msrp,
            0.0
        )

    def test_msrp_attribute_is_zero(self):
        """testing if it is totally ok to test the msrp attribute to 0
        """
        g = Good(**self.kwargs)
        self.assertNotEqual(g.msrp, 0.0)
        g.msrp = 0.0
        self.assertEqual(
            g.msrp,
            0.0
        )

    def test_msrp_argument_is_negative(self):
        """testing if a ValueError will be raised if the msrp argument is a
        negative number
        """
        self.kwargs['msrp'] = -10
        with self.assertRaises(ValueError) as cm:
            g = Good(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Good.msrp should be a non-negative number'
        )

    def test_msrp_attribute_is_negative(self):
        """testing if ValueError will be raised if the msrp attribute is set to
        a negative number
        """
        g = Good(**self.kwargs)
        with self.assertRaises(ValueError) as cm:
            g.msrp = -10

        self.assertEqual(
            str(cm.exception),
            'Good.msrp should be a non-negative number'
        )

    def test_msrp_argument_is_working_properly(self):
        """testing if the msrp argument value is properly passed to the msrp
        attribute
        """
        test_value = 113
        self.kwargs['msrp'] = test_value
        g = Good(**self.kwargs)
        self.assertEqual(
            g.msrp,
            test_value
        )

    def test_msrp_attribute_is_working_properly(self):
        """testing if the msrp attribute value can be properly changed
        """
        test_value = 145
        g = Good(**self.kwargs)
        self.assertNotEqual(
            g.msrp,
            test_value
        )
        g.msrp = test_value
        self.assertEqual(
            g.msrp,
            test_value
        )

    def test_unit_argument_is_skipped(self):
        """testing if the unit attribute will be an empty string if the unit
        argument is skipped
        """
        self.kwargs.pop('unit')
        g = Good(**self.kwargs)
        self.assertEqual(g.unit, '')

    def test_unit_argument_is_None(self):
        """testing if the unit attribute will be an empty string if the unit
        argument is None
        """
        self.kwargs['unit'] = None
        g = Good(**self.kwargs)
        self.assertEqual(g.unit, '')

    def test_unit_attribute_is_set_to_None(self):
        """testing if the unit attribute will be an empty string if it is set
        to None
        """
        g = Good(**self.kwargs)
        self.assertNotEqual(g.unit, '')
        g.unit = None
        self.assertEqual(g.unit, '')

    def test_unit_argument_is_not_a_string(self):
        """testing if a TypeError will be raised if the unit argument is not a
        string
        """
        self.kwargs['unit'] = 12312
        with self.assertRaises(TypeError) as cm:
            g = Good(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Good.unit should be a str, not int'
        )

    def test_unit_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised if the unit attribute is set
        to a value which is not a string
        """
        g = Good(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            g.unit = 2342

        self.assertEqual(
            str(cm.exception),
            'Good.unit should be a str, not int'
        )

    def test_unit_argument_is_working_properly(self):
        """testing if the unit argument value is properly passed to the unit
        attribute
        """
        test_value = 'this is my unit'
        self.kwargs['unit'] = test_value
        g = Good(**self.kwargs)
        self.assertEqual(g.unit, test_value)

    def test_unit_attribute_is_working_properly(self):
        """testing if the unit attribute value can be changed properly
        """
        test_value = 'this is my unit'
        g = Good(**self.kwargs)
        self.assertNotEqual(g.unit, test_value)
        g.unit = test_value
        self.assertEqual(g.unit, test_value)
