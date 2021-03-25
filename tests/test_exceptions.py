# -*- coding: utf-8 -*-

import unittest
import pytest


class ExceptionTester(unittest.TestCase):
    """testing exceptions
    """

    def test_login_error_is_working_properly(self):
        """testing if LoginError is working properly
        """
        from stalker.exceptions import LoginError
        test_message = 'testing LoginError'
        with pytest.raises(LoginError) as cm:
            raise LoginError(test_message)

        assert str(cm.value) == test_message

    def test_circular_dependency_error_is_working_properly(self):
        """testing if CircularDependencyError is working properly
        """
        from stalker.exceptions import CircularDependencyError
        test_message = 'testing CircularDependencyError'
        with pytest.raises(CircularDependencyError) as cm:
            raise CircularDependencyError(test_message)

        assert str(cm.value) == test_message

    def test_over_booked_error_is_working_properly(self):
        """testing if OverBookedError is working properly
        """
        from stalker.exceptions import OverBookedError
        test_message = 'testing OverBookedError'
        with pytest.raises(OverBookedError) as cm:
            raise OverBookedError(test_message)

        assert str(cm.value) ==test_message

    def test_status_error_is_working_properly(self):
        """testing if StatusError is working properly
        """
        from stalker.exceptions import StatusError
        test_message = 'testing StatusError'
        with pytest.raises(StatusError) as cm:
            raise StatusError(test_message)

        assert str(cm.value) == test_message

    def test_dependency_violation_error_is_working_properly(self):
        """testing if DependencyViolationError is working properly
        """
        from stalker.exceptions import DependencyViolationError
        test_message = 'testing DependencyViolationError'
        with pytest.raises(DependencyViolationError) as cm:
            raise DependencyViolationError(test_message)

        assert str(cm.value) ==test_message
