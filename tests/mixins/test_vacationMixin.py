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
import datetime

import unittest2

from sqlalchemy import Column, Integer, ForeignKey

from stalker import SimpleEntity, VacationMixin, Vacation


class VacationMixedClass(SimpleEntity, VacationMixin):
    """A class which derives from another which has and __init__ already
    """
    __tablename__ = "VacationMixedClasses"
    __mapper_args__ = {"polymorphic_identity": "VacationMixedClass"}
    vacationMixedClass_id = Column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(VacationMixedClass, self).__init__(**kwargs)


class VacationMixinTestCase(unittest2.TestCase):
    """tests the stalker.models.mixins.VacationMixin
    """

    def setUp(self):
        """setup the test
        """
        self.test_vac1 = Vacation(
            start=datetime.datetime(2013, 6, 1, 0, 0),
            ennd=datetime.datetime(2013, 6, 10, 0, 0)
        )

        self.test_vac2 = Vacation(
            start=datetime.datetime(2013, 6, 11, 0, 0),
            ennd=datetime.datetime(2013, 6, 20, 0, 0)
        )

        self.test_vac_mix_class = VacationMixedClass()

    def test_vacations_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the vacations attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_vac_mix_class,
                          'vacations', None)

    def test_vacations_attribute_is_set_to_a_value_other_than_list(self):
        """testing if a TypeError will be raised when the vacations attribute
        is set to a value other than a list
        """
        self.assertRaises(TypeError, setattr, self.test_vac_mix_class,
                          'vacations', 'not a list')

    def test_vacations_attribute_is_a_list_of_other_values_than_Vacations(self):
        """testing if a TypeError will be raised when the vacations attribute
        is a list of other values than Vacation instances
        """
        self.assertRaises(TypeError, setattr, self.test_vac_mix_class,
                          'vacations', ['not a list'])

    def test_vacations_attribute_is_working_properly(self):
        """testing if the vacation attribute is working properly
        """
        self.assertEqual(len(self.test_vac_mix_class.vacations), 0)
        self.test_vac_mix_class.vacations = [self.test_vac1, self.test_vac2]
        self.assertEqual(len(self.test_vac_mix_class.vacations), 2)
        self.assertIn(self.test_vac1, self.test_vac_mix_class.vacations)
        self.assertIn(self.test_vac2, self.test_vac_mix_class.vacations)

