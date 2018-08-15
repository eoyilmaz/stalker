# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2018 Erkan Ozgur Yilmaz
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

import unittest
import pytest
from sqlalchemy import Column, Integer, ForeignKey
from stalker import UnitMixin, SimpleEntity


class UnitMixinFooMixedInClass(SimpleEntity, UnitMixin):
    """a class which derives from another which has and __init__ already
    """
    __tablename__ = "UnitMixinFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "UnitMixinFooMixedInClass"}
    unitMixinFooMixedInClass_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )
    __id_column__ = 'unitMixinFooMixedInClass_id'

    def __init__(self, **kwargs):
        super(UnitMixinFooMixedInClass, self).__init__(**kwargs)
        UnitMixin.__init__(self, **kwargs)


class UnitMixinTestCase(unittest.TestCase):
    """tests the UnitMixin
    """

    def test_mixed_in_class_initialization(self):
        """testing if the init is working properly
        """
        a = UnitMixinFooMixedInClass(unit='TRY')
        assert isinstance(a, UnitMixinFooMixedInClass)
        assert a.unit == 'TRY'

    def test_unit_argument_is_skipped(self):
        """testing if the unit attribute will be an empty string if the unit
        argument is skipped
        """
        g = UnitMixinFooMixedInClass()
        assert g.unit == ''

    def test_unit_argument_is_None(self):
        """testing if the unit attribute will be an empty string if the unit
        argument is None
        """
        g = UnitMixinFooMixedInClass(unit=None)
        assert g.unit == ''

    def test_unit_attribute_is_set_to_None(self):
        """testing if the unit attribute will be an empty string if it is set
        to None
        """
        g = UnitMixinFooMixedInClass(unit='TRY')
        assert g.unit != ''
        g.unit = None
        assert g.unit == ''

    def test_unit_argument_is_not_a_string(self):
        """testing if a TypeError will be raised if the unit argument is not a
        string
        """
        with pytest.raises(TypeError) as cm:
            UnitMixinFooMixedInClass(unit=1234)

        assert str(cm.value) == \
            'UnitMixinFooMixedInClass.unit should be a string, not int'

    def test_unit_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised if the unit attribute is set
        to a value which is not a string
        """
        g = UnitMixinFooMixedInClass(unit='TRY')
        with pytest.raises(TypeError) as cm:
            g.unit = 2342

        assert str(cm.value) == \
            'UnitMixinFooMixedInClass.unit should be a string, not int'

    def test_unit_argument_is_working_properly(self):
        """testing if the unit argument value is properly passed to the unit
        attribute
        """
        test_value = 'this is my unit'
        g = UnitMixinFooMixedInClass(unit=test_value)
        assert g.unit == test_value

    def test_unit_attribute_is_working_properly(self):
        """testing if the unit attribute value can be changed properly
        """
        test_value = 'this is my unit'
        g = UnitMixinFooMixedInClass(unit='TRY')
        assert g.unit != test_value
        g.unit = test_value
        assert g.unit == test_value
