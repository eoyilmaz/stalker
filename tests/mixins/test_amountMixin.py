# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

from stalker import AmountMixin, SimpleEntity
from sqlalchemy import Column, Integer, ForeignKey
from stalker.testing import UnitTestBase


class AmountMixinFooMixedInClass(SimpleEntity, AmountMixin):
    """a class which derives from another which has and __init__ already
    """
    __tablename__ = "AmountMixinFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "AmountMixinFooMixedInClass"}
    amountMixinFooMixedInClass_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )
    __id_column__ = 'amountMixinFooMixedInClass_id'

    def __init__(self, **kwargs):
        super(AmountMixinFooMixedInClass, self).__init__(**kwargs)
        AmountMixin.__init__(self, **kwargs)


class AmountMixinTestCase(UnitTestBase):
    """tests the AmountMixin
    """

    def test_mixed_in_class_initialization(self):
        """testing if the init is working properly
        """
        a = AmountMixinFooMixedInClass(amount=1500)
        self.assertIsInstance(a, AmountMixinFooMixedInClass)
        self.assertEqual(a.amount, 1500)

    def test_amount_argument_is_skipped(self):
        """testing if the amount attribute will be 0 if the amount argument is
        skipped
        """
        entry = AmountMixinFooMixedInClass()
        self.assertEqual(entry.amount, 0.0)

    def test_amount_argument_is_set_to_None(self):
        """testing if the amount attribute will be set to 0 if the amount
        argument is set to None
        """
        entry = AmountMixinFooMixedInClass(amount=None)
        self.assertEqual(entry.amount, 0.0)

    def test_amount_attribute_is_set_to_None(self):
        """testing if the amount attribute will be set to 0 if it is set to
        None
        """
        entry = AmountMixinFooMixedInClass(amount=10.0)
        self.assertEqual(entry.amount, 10.0)
        entry.amount = None
        self.assertEqual(entry.amount, 0.0)

    def test_amount_argument_is_not_a_number(self):
        """testing if a TypeError will be raised if the amount argument is set
        to something other than a number
        """
        with self.assertRaises(TypeError) as cm:
            AmountMixinFooMixedInClass(amount='some string')

        self.assertEqual(
            str(cm.exception),
            'AmountMixinFooMixedInClass.amount should be a number, not str'
        )

    def test_amount_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if amount attribute is set to
        something other than a number
        """
        entry = AmountMixinFooMixedInClass(amount=10)
        with self.assertRaises(TypeError) as cm:
            entry.amount = 'some string'

        self.assertEqual(
            str(cm.exception),
            'AmountMixinFooMixedInClass.amount should be a number, not str'
        )

    def test_amount_argument_is_working_properly(self):
        """testing if the amount argument value is correctly passed to the
        amount attribute
        """
        entry = AmountMixinFooMixedInClass(amount=10)
        self.assertEqual(entry.amount, 10.0)

    def test_amount_attribute_is_working_properly(self):
        """testing if the amount attribute is working properly
        """
        entry = AmountMixinFooMixedInClass(amount=10)
        test_value = 5.0
        self.assertNotEqual(entry.amount, test_value)
        entry.amount = test_value
        self.assertEqual(entry.amount, test_value)
