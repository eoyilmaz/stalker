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
from stalker import PriceList, Good


class PriceListTestCase(unittest.TestCase):
    """tests the PriceList class
    """

    def setUp(self):
        """set the test up
        """
        self.kwargs = {
            'name': 'Test Price List',
        }

    def test_goods_argument_is_skipped(self):
        """testing if the goods attribute will be an empty list when the goods
        argument is skipped
        """
        p = PriceList(**self.kwargs)
        self.assertEqual(p.goods, [])

    def test_goods_argument_is_None(self):
        """testing if the goods attribute  will be an empty list when the goods
        argument is None
        """
        self.kwargs['goods'] = None
        p = PriceList(**self.kwargs)
        self.assertEqual(p.goods, [])

    def test_goods_attribute_is_None(self):
        """testing if a TypeError will be raised when the goods attribute 
        is set to None
        """
        g1 = Good(name='Test Good')
        self.kwargs['goods'] = [g1]
        p = PriceList(**self.kwargs)
        self.assertEqual(p.goods, [g1])

        with self.assertRaises(TypeError) as cm:
            p.goods = None

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: None is not list-like'
        )

    def test_goods_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the goods argument value
        is not a list
        """
        self.kwargs['goods'] = 'this is not a list'
        with self.assertRaises(TypeError) as cm:
            PriceList(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_goods_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the goods attribute is
        set to a value other than a list
        """
        g1 = Good(name='Test Good')
        self.kwargs['goods'] = [g1]
        p = PriceList(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            p.goods = 'this is not a list'

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_goods_argument_is_a_list_of_objects_which_are_not_goods(self):
        """testing if a TypeError will be raised when the goods argument is not
        a list of Good instances
        """
        self.kwargs['goods'] = ['not', 1, 'good', 'instances']
        with self.assertRaises(TypeError) as cm:
            PriceList(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'PriceList.goods should be a list of stalker.model.bugdet.Good '
            'instances, not str'
        )

    def test_good_attribute_is_a_list_of_objects_which_are_not_goods(self):
        """testing if a TypeError will be raised when the goods attribute is
        not a list of Good instances
        """
        p = PriceList(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            p.goods = ['not', 1, 'good', 'instances']

        self.assertEqual(
            str(cm.exception),
            'PriceList.goods should be a list of stalker.model.bugdet.Good '
            'instances, not str'
        )

    def test_good_argument_is_working_properly(self):
        """testing if the good argument value is properly passed to the good
        attribute
        """
        g1 = Good(name='Good1')
        g2 = Good(name='Good2')
        g3 = Good(name='Good3')
        test_value = [g1, g2, g3]
        self.kwargs['goods'] = test_value
        p = PriceList(**self.kwargs)
        self.assertEqual(p.goods, test_value)

    def test_good_attribute_is_working_properly(self):
        """testing if the good attribute value can be properly set
        """
        g1 = Good(name='Good1')
        g2 = Good(name='Good2')
        g3 = Good(name='Good3')
        test_value = [g1, g2, g3]
        p = PriceList(**self.kwargs)
        self.assertNotEqual(p.goods, test_value)
        p.goods = test_value
        self.assertEqual(p.goods, test_value)
