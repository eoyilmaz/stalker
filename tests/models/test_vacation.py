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

from stalker import User, Type
from stalker.models.studio import Vacation


class VacationTestCase(unittest.TestCase):
    """tests the stalker.models.studio.Vacation class
    """

    def setUp(self):
        """setup the test
        """
        # create a user
        self.test_user = User(
            name='Test User',
            login='testuser',
            email='testuser@test.com',
            password='secret',
        )

        # vacation type
        self.personal_vacation = Type(
            name='Personal',
            code='PERS',
            target_entity_type='Vacation'
        )

        self.studio_vacation = Type(
            name='Studio Wide',
            code='STD',
            target_entity_type='Vacation'
        )

        self.kwargs = {
            'user': self.test_user,
            'type': self.personal_vacation,
            'start': datetime.datetime(2013, 6, 6, 10, 0),
            'end': datetime.datetime(2013, 6, 10, 19, 0)
        }

        self.test_vacation = Vacation(**self.kwargs)

    def test_strictly_typed_is_False(self):
        """testing if the __strictly_typed_ attribute is False for Vacation
        class
        """
        self.assertEqual(Vacation.__strictly_typed__, False)

    def test_user_argument_is_skipped(self):
        """testing if the user argument can be skipped skipped
        """
        self.kwargs.pop('user')
        Vacation(**self.kwargs)

    def test_user_argument_is_None(self):
        """testing if the user argument can be set to None
        """
        self.kwargs['user'] = None
        Vacation(**self.kwargs)

    def test_user_attribute_is_None(self):
        """testing if the user attribute cat be set to None
        """
        self.test_vacation.user = None

    def test_user_argument_is_not_a_User_instance(self):
        """testing if a TypeError will be raised when the user argument is not
        a stalker.models.auth.User instance
        """
        self.kwargs['user'] = 'not a user instance'
        self.assertRaises(TypeError, Vacation, **self.kwargs)

    def test_user_attribute_is_not_a_User_instance(self):
        """testing if a TypeError will be raised when the user attribute is set
        to a value which is not a stalker.models.auth.User instance
        """
        self.assertRaises(TypeError, setattr, self.test_vacation, 'user',
                          'not a user instance')

    def test_user_argument_is_working_properly(self):
        """testing if the user argument value is correctly passed to the user
        attribute
        """
        self.assertEqual(self.kwargs['user'], self.test_vacation.user)

    def test_user_attribute_is_working_properly(self):
        """testing if the user attribute is working properly
        """
        new_user = User(
            name='test user 2',
            login='testuser2',
            email='test@user.com',
            password='secret'
        )

        self.assertNotEqual(self.test_vacation.user, new_user)
        self.test_vacation.user = new_user
        self.assertEqual(self.test_vacation.user, new_user)

    def test_user_argument_back_populates_vacations_attribute(self):
        """testing if the user argument back populates vacations attribute of
        the User instance
        """
        self.assertTrue(
            self.test_vacation in self.kwargs['user'].vacations
        )

    def test_user_attribute_back_populates_vacations_attribute(self):
        """testing if the user attribute back populates vacations attribute of
        the User instance
        """
        new_user = User(
            name='test user 2',
            login='testuser2',
            email='test@user.com',
            password='secret'
        )

        self.test_vacation.user = new_user
        self.assertTrue(self.test_vacation in new_user.vacations)

    def test_to_tjp_attribute_is_a_read_only_property(self):
        """testing if the to_tjp is a read-only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_vacation,
                          'to_tjp', 'some value')

    def test_to_tjp_attribute_is_working_properly(self):
        """testing if the to_tjp attribute is working properly
        """
        expected_tjp = "vacation 2013-06-06-10:00:00 - 2013-06-10-19:00:00"
        self.assertEqual(
            self.test_vacation.to_tjp,
            expected_tjp
        )
