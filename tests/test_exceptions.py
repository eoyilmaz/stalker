# -*- coding: utf-8 -*-
"""Tests for the exceptions module."""
import pytest

from stalker.exceptions import (
    CircularDependencyError,
    DependencyViolationError,
    LoginError,
    OverBookedError,
    StatusError,
)


def test_login_error_is_working_as_expected():
    """LoginError is working as expected."""
    test_message = "testing LoginError"
    with pytest.raises(LoginError) as cm:
        raise LoginError(test_message)

    assert str(cm.value) == test_message


def test_circular_dependency_error_is_working_as_expected():
    """CircularDependencyError is working as expected."""
    test_message = "testing CircularDependencyError"
    with pytest.raises(CircularDependencyError) as cm:
        raise CircularDependencyError(test_message)

    assert str(cm.value) == test_message


def test_over_booked_error_is_working_as_expected():
    """OverBookedError is working as expected."""
    test_message = "testing OverBookedError"
    with pytest.raises(OverBookedError) as cm:
        raise OverBookedError(test_message)

    assert str(cm.value) == test_message


def test_status_error_is_working_as_expected():
    """StatusError is working as expected."""
    test_message = "testing StatusError"
    with pytest.raises(StatusError) as cm:
        raise StatusError(test_message)

    assert str(cm.value) == test_message


def test_dependency_violation_error_is_working_as_expected():
    """DependencyViolationError is working as expected."""
    test_message = "testing DependencyViolationError"
    with pytest.raises(DependencyViolationError) as cm:
        raise DependencyViolationError(test_message)

    assert str(cm.value) == test_message
