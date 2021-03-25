# -*- coding: utf-8 -*-

import unittest
import pytest


class AuthenticationLogTestCase(unittest.TestCase):
    """tests AuthenticationLog class
    """

    def setUp(self):
        """set the test up
        """
        super(AuthenticationLogTestCase, self).setUp()

        from stalker import User
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )

        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )

    def test_user_argument_is_skipped(self):
        """testing if a TypeError will be raised when the user argument is
        skipped
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN
        import datetime
        import pytz
        with pytest.raises(TypeError) as cm:
            AuthenticationLog(
                action=LOGIN,
                date=datetime.datetime.now(pytz.utc)
            )

        assert str(cm.value) == \
            'AuthenticationLog.user should be a User instance, not NoneType'

    def test_user_argument_is_None(self):
        """testing if a TypeError will be raised when the user argument is None
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN
        import datetime
        import pytz
        with pytest.raises(TypeError) as cm:
            AuthenticationLog(
                user=None,
                action=LOGIN,
                date=datetime.datetime.now(pytz.utc)
            )

        assert str(cm.value) == \
            'AuthenticationLog.user should be a User instance, not NoneType'

    def test_user_argument_is_not_a_user_instance(self):
        """testing if a TypeError will be raised when the user argument value
        is not a User instance
        """
        from stalker import AuthenticationLog
        from stalker.models.auth import LOGIN
        import datetime
        import pytz
        with pytest.raises(TypeError) as cm:
            AuthenticationLog(
                user='not a user instance',
                action=LOGIN,
                date=datetime.datetime.now(pytz.utc)
            )

        assert str(cm.value) == \
            'AuthenticationLog.user should be a User instance, not str'

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
        with pytest.raises(TypeError) as cm:
            uli.user = 'not a user instance'

        assert str(cm.value) == \
            'AuthenticationLog.user should be a User instance, not str'

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
        assert uli.user == self.test_user1

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
        assert uli.user != self.test_user2
        uli.user = self.test_user2
        assert uli.user == self.test_user2

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
        assert uli.action == LOGIN

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
        assert uli.action == LOGIN

    def test_action_argument_value_is_not_login_or_logout(self):
        """testing if a ValueError will be raised when the action attribute
        value is not one of "login" or "login"
        """
        from stalker import AuthenticationLog
        import datetime
        import pytz
        with pytest.raises(ValueError) as cm:
            AuthenticationLog(
                user=self.test_user1,
                action='not login',
                date=datetime.datetime.now(pytz.utc)
            )

        assert str(cm.value) == \
            'AuthenticationLog.action should be one of "login" or "logout", ' \
            'not "not login"'

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
        with pytest.raises(ValueError) as cm:
            uli.action = 'not login'

        assert str(cm.value) == \
            'AuthenticationLog.action should be one of "login" or "logout", ' \
            'not "not login"'

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
        assert uli.action == LOGIN

        uli = AuthenticationLog(
            user=self.test_user1,
            action=LOGOUT,
            date=datetime.datetime.now(pytz.utc)
        )
        assert uli.action == LOGOUT

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
        assert uli.action != LOGOUT
        uli.action = LOGOUT
        assert uli.action == LOGOUT

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
        assert diff.microseconds < 5000

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
        assert diff < datetime.timedelta(seconds=1)

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
        assert diff > one_second

        uli.date = None
        diff = datetime.datetime.now(pytz.utc) - uli.date
        assert diff < one_second

    def test_date_argument_is_not_a_datetime_instance(self):
        """testing if a TypeError will be raised when the date argument value
        is not a ``datetime.datetime`` instance
        """
        from stalker.models.auth import AuthenticationLog, LOGIN
        with pytest.raises(TypeError) as cm:
            AuthenticationLog(
                user=self.test_user1,
                action=LOGIN,
                date='not a datetime instance'
            )

        assert str(cm.value) == \
            'AuthenticationLog.date should be a "datetime.datetime" ' \
            'instance, not str'

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
        with pytest.raises(TypeError) as cm:
            uli.date = 'not a datetime instance'

        assert str(cm.value) == \
            'AuthenticationLog.date should be a "datetime.datetime" ' \
            'instance, not str'

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

        assert uli.date == date

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
        assert uli.date != date2
        uli.date = date2
        assert uli.date == date2

    def test_date_argument_is_working_properly2(self):
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
        assert uli.date == date1
