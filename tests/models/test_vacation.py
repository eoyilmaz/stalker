# -*- coding: utf-8 -*-

import unittest

import pytest

from stalker.models.studio import Vacation


class VacationTestCase(unittest.TestCase):
    """tests the stalker.models.studio.Vacation class
    """

    def setUp(self):
        """setup the test
        """
        super(VacationTestCase, self).setUp()

        # create a user
        from stalker import User
        self.test_user = User(
            name='Test User',
            login='testuser',
            email='testuser@test.com',
            password='secret',
        )

        # vacation type
        from stalker import Type
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

        import datetime
        import pytz
        self.kwargs = {
            'user': self.test_user,
            'type': self.personal_vacation,
            'start': datetime.datetime(2013, 6, 6, 10, 0, tzinfo=pytz.utc),
            'end': datetime.datetime(2013, 6, 10, 19, 0, tzinfo=pytz.utc)
        }

        self.test_vacation = Vacation(**self.kwargs)

    def test_strictly_typed_is_False(self):
        """testing if the __strictly_typed_ attribute is False for Vacation
        class
        """
        assert Vacation.__strictly_typed__ is False

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
        with pytest.raises(TypeError) as cm:
            Vacation(**self.kwargs)

        assert str(cm.value) == \
            'Vacation.user should be an instance of ' \
            'stalker.models.auth.User, not str'

    def test_user_attribute_is_not_a_User_instance(self):
        """testing if a TypeError will be raised when the user attribute is set
        to a value which is not a stalker.models.auth.User instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_vacation.user = 'not a user instance'

        assert str(cm.value) == \
            'Vacation.user should be an instance of ' \
            'stalker.models.auth.User, not str'

    def test_user_argument_is_working_properly(self):
        """testing if the user argument value is correctly passed to the user
        attribute
        """
        assert self.test_vacation.user == self.kwargs['user']

    def test_user_attribute_is_working_properly(self):
        """testing if the user attribute is working properly
        """
        from stalker import User
        new_user = User(
            name='test user 2',
            login='testuser2',
            email='test@user.com',
            password='secret'
        )

        assert self.test_vacation.user != new_user
        self.test_vacation.user = new_user
        assert self.test_vacation.user == new_user

    def test_user_argument_back_populates_vacations_attribute(self):
        """testing if the user argument back populates vacations attribute of
        the User instance
        """
        assert self.test_vacation in self.kwargs['user'].vacations

    def test_user_attribute_back_populates_vacations_attribute(self):
        """testing if the user attribute back populates vacations attribute of
        the User instance
        """
        from stalker import User
        new_user = User(
            name='test user 2',
            login='testuser2',
            email='test@user.com',
            password='secret'
        )

        self.test_vacation.user = new_user
        assert self.test_vacation in new_user.vacations

    def test_to_tjp_attribute_is_a_read_only_property(self):
        """testing if the to_tjp is a read-only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_vacation.to_tjp = 'some value'

        assert str(cm.value) == "can't set attribute"

    def test_to_tjp_attribute_is_working_properly(self):
        """testing if the to_tjp attribute is working properly
        """
        # TODO: Vacation should also use time zone info
        expected_tjp = "vacation 2013-06-06-10:00:00 - 2013-06-10-19:00:00"
        assert self.test_vacation.to_tjp == expected_tjp
