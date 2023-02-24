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


def test_login_error_is_working_properly():
    """LoginError is working properly."""
    test_message = "testing LoginError"
    with pytest.raises(LoginError) as cm:
        raise LoginError(test_message)

    assert str(cm.value) == test_message


def test_circular_dependency_error_is_working_properly():
    """CircularDependencyError is working properly."""
    test_message = "testing CircularDependencyError"
    with pytest.raises(CircularDependencyError) as cm:
        raise CircularDependencyError(test_message)

    assert str(cm.value) == test_message


def test_over_booked_error_is_working_properly():
    """OverBookedError is working properly."""
    test_message = "testing OverBookedError"
    with pytest.raises(OverBookedError) as cm:
        raise OverBookedError(test_message)

    assert str(cm.value) == test_message


def test_status_error_is_working_properly():
    """StatusError is working properly."""
    test_message = "testing StatusError"
    with pytest.raises(StatusError) as cm:
        raise StatusError(test_message)

    assert str(cm.value) == test_message


def test_dependency_violation_error_is_working_properly():
    """DependencyViolationError is working properly."""
    test_message = "testing DependencyViolationError"
    with pytest.raises(DependencyViolationError) as cm:
        raise DependencyViolationError(test_message)

    assert str(cm.value) == test_message
