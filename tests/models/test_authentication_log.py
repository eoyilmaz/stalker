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

from stalker.testing import UnitTestBase


class AuthenticationLogTestCase(UnitTestBase):
    """tests AuthenticationLog class
    """

    def setUp(self):
        """set the test up
        """
        super(AuthenticationLogTestCase, self).setUp()

        from stalker import db, User
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user1)
        db.DBSession.commit()

        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user1)
        db.DBSession.commit()

    def test_user_argument_is_skipped(self):
        """testing if a TypeError will be raised when the user argument is
        skipped
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN
        import datetime
        import pytz
        with self.assertRaises(TypeError) as cm:
            AuthenticationLog(
                action=LOGIN,
                date=datetime.datetime.now(pytz.utc)
            )

        self.assertEqual(
            str(cm.exception),
            'AuthenticationLog.user should be a User instance, not NoneType'
        )

    def test_user_argument_is_None(self):
        """testing if a TypeError will be raised when the user argument is None
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN
        import datetime
        import pytz
        with self.assertRaises(TypeError) as cm:
            AuthenticationLog(
                user=None,
                action=LOGIN,
                date=datetime.datetime.now(pytz.utc)
            )

        self.assertEqual(
            str(cm.exception),
            'AuthenticationLog.user should be a User instance, not NoneType'
        )

    def test_user_argument_is_not_a_user_instance(self):
        """testing if a TypeError will be raised when the user argument value
        is not a User instance
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN
        import datetime
        import pytz
        with self.assertRaises(TypeError) as cm:
            AuthenticationLog(
                user='not a user instance',
                action=LOGIN,
                date=datetime.datetime.now(pytz.utc)
            )

        self.assertEqual(
            str(cm.exception),
            'AuthenticationLog.user should be a User instance, not str'
        )

    def test_user_attribute_is_not_a_user_instance(self):
        """testing if a TypeError will be raised when the user attribute is set
        to value other than a User instance
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=datetime.datetime.now(pytz.utc)
        )
        with self.assertRaises(TypeError) as cm:
            uli.user = 'not a user instance'

        self.assertEqual(
            str(cm.exception),
            'AuthenticationLog.user should be a User instance, not str'
        )

    def test_user_argument_is_working_properly(self):
        """testing if the user argument value is correctly passed to the user
        attribute
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGOUT
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGOUT,
            date=datetime.datetime.now(pytz.utc)
        )
        self.assertEqual(uli.user, self.test_user1)

    def test_user_attribute_is_working_properly(self):
        """testing if the user attribute value is correctly passed to the user
        attribute
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGOUT
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGOUT,
            date=datetime.datetime.now(pytz.utc)
        )
        self.assertNotEqual(uli.user, self.test_user2)
        uli.user = self.test_user2
        self.assertEqual(uli.user, self.test_user2)

    def test_action_argument_is_skipped(self):
        """testing if the action attribute value will be set to "login" when
        the action argument is skipped
        """
        from stalker import AuthenticationLog
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            date=datetime.datetime.now(pytz.utc)
        )
        from stalker.models.auth import LOGIN
        self.assertEqual(uli.action, LOGIN)

    def test_action_argument_is_None(self):
        """testing if the action attribute value will be set to "login" when
        the action argument is None
        """
        from stalker import AuthenticationLog
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=None,
            date=datetime.datetime.now(pytz.utc)
        )
        from stalker.models.auth import LOGIN
        self.assertEqual(uli.action, LOGIN)

    def test_action_argument_value_is_not_login_or_logout(self):
        """testing if a ValueError will be raised when the action attribute
        value is not one of "login" or "login"
        """
        from stalker import AuthenticationLog
        import datetime
        import pytz
        with self.assertRaises(ValueError) as cm:
            AuthenticationLog(
                user=self.test_user1,
                action='not login',
                date=datetime.datetime.now(pytz.utc)
            )

        self.assertEqual(
            str(cm.exception),
            'AuthenticationLog.action should be one of "login" or "logout", not '
            '"not login"'
        )

    def test_action_attribute_value_is_not_login_or_logout(self):
        """testing if a ValueError will be raised when the action attribute
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=datetime.datetime.now(pytz.utc)
        )
        with self.assertRaises(ValueError) as cm:
            uli.action = 'not login'

        self.assertEqual(
            str(cm.exception),
            'AuthenticationLog.action should be one of "login" or "logout", not '
            '"not login"'
        )

    def test_action_argument_is_working_properly(self):
        """testing if the action argument value is properly passed to the
        action attribute
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN, LOGOUT
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=datetime.datetime.now(pytz.utc)
        )
        self.assertEqual(uli.action, LOGIN)

        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGOUT,
            date=datetime.datetime.now(pytz.utc)
        )
        self.assertEqual(uli.action, LOGOUT)

    def test_action_attribute_is_working_properly(self):
        """testing if the action attribute is working properly
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN, LOGOUT
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=datetime.datetime.now(pytz.utc)
        )
        self.assertNotEqual(uli.action, LOGOUT)
        uli.action = LOGOUT
        self.assertEqual(uli.action, LOGOUT)

    def test_date_argument_is_skipped(self):
        """testing if the date attribute value will be set to
        datetime.datetime.now(pytz.utc) when the date argument is skipped
        """
        from stalker.models.auth import AuthenticationLog, LOGIN
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN
        )
        diff = datetime.datetime.now(pytz.utc) - uli.date
        self.assertTrue(diff.microseconds < 1000)

    def test_date_argument_is_None(self):
        """testing if the date attribute value will be set to
        datetime.datetime.now(pytz.utc) when the date argument is None
        """
        from stalker.models.auth import AuthenticationLog, LOGIN
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=None
        )
        diff = datetime.datetime.now(pytz.utc) - uli.date
        self.assertTrue(diff < datetime.timedelta(seconds=1))

    def test_date_attribute_is_None(self):
        """testing if the date attribute value is set to
        datetime.datetime.now(pytz.utc) when it is set to None
        """
        from stalker.models.auth import AuthenticationLog, LOGIN
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=datetime.datetime.now(pytz.utc) - datetime.timedelta(days=10)
        )
        diff = datetime.datetime.now(pytz.utc) - uli.date
        one_second = datetime.timedelta(seconds=1)
        self.assertTrue(diff > one_second)

        uli.date = None
        diff = datetime.datetime.now(pytz.utc) - uli.date
        self.assertTrue(diff < one_second)

    def test_date_argument_is_not_a_datetime_instance(self):
        """testing if a TypeError will be raised when the date argument value
        is not a ``datetime.datetime`` instance
        """
        from stalker.models.auth import AuthenticationLog, LOGIN
        with self.assertRaises(TypeError) as cm:
            AuthenticationLog(
                user=self.test_user1,
                action=LOGIN,
                date='not a datetime instance'
            )

        self.assertEqual(
            str(cm.exception),
            'AuthenticationLog.date should be a "datetime.datetime" instance, not '
            'str'
        )

    def test_date_attribute_is_not_a_datetime_instance(self):
        """testing if a TypeError will be raised when the date attribute is set
        to anything other than a ``datetime.datetime`` instance
        """
        from stalker.models.auth import AuthenticationLog, LOGIN
        import datetime
        import pytz
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=datetime.datetime.now(pytz.utc)
        )
        with self.assertRaises(TypeError) as cm:
            uli.date = 'not a datetime instance'

        self.assertEqual(
            str(cm.exception),
            'AuthenticationLog.date should be a "datetime.datetime" instance, not '
            'str'
        )

    def test_date_argument_is_working_properly(self):
        """testing if the date argument value is properly passed to the date
        attribute
        """
        import datetime
        import pytz
        from stalker.models.auth import AuthenticationLog, LOGIN
        date = datetime.datetime(2016, 11, 14, 16, 30, tzinfo=pytz.utc)
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=date
        )

        self.assertEqual(uli.date, date)

    def test_date_attribute_is_working_properly(self):
        """testing if the date attribute value can be properly changed
        """
        import datetime
        import pytz
        from stalker.models.auth import AuthenticationLog, LOGIN
        date1 = datetime.datetime(2016, 11, 4, 6, 30, tzinfo=pytz.utc)
        date2 = datetime.datetime(2016, 11, 14, 16, 30, tzinfo=pytz.utc)
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=date1
        )
        self.assertNotEqual(uli.date, date2)
        uli.date = date2
        self.assertEqual(uli.date, date2)

    def test_date_argument_is_working_properly(self):
        """testing if the date argument value is properly passed to the date
        attribute
        """
        import datetime
        import pytz
        from stalker.models.auth import AuthenticationLog, LOGIN
        date1 = datetime.datetime(2016, 11, 4, 6, 30, tzinfo=pytz.utc)
        date2 = datetime.datetime(2016, 11, 14, 16, 30, tzinfo=pytz.utc)
        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGIN,
            date=date1
        )
        self.assertEqual(uli.date, date1)
