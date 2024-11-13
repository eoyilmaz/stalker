# -*- coding: utf-8 -*-
"""Errors for the system.

This module contains the Errors in Stalker.
"""


class LoginError(Exception):
    """Raised when the login information is not correct."""

    def __init__(self, value="") -> None:
        super(LoginError, self).__init__(value)
        self.value = value

    def __str__(self) -> str:
        """Return the string representation of this exception.

        Returns:
            str: The string representation of this exception.
        """
        return self.value


class CircularDependencyError(Exception):
    """Raised when there is circular dependencies within Tasks."""

    def __init__(self, value="") -> None:
        super(CircularDependencyError, self).__init__(value)
        self.value = value

    def __str__(self) -> str:
        """Return the string representation of this exception.

        Returns:
            str: The string representation of this exception.
        """
        return self.value


class OverBookedError(Exception):
    """Raised when a resource is booked more than once for the same time period."""

    def __init__(self, value="") -> None:
        super(OverBookedError, self).__init__(value)
        self.value = value

    def __str__(self) -> str:
        """Return the string representation of this exception.

        Returns:
            str: The string representation of this exception.
        """
        return self.value


class StatusError(Exception):
    """Raised when the status of an entity is not suitable for the desired action."""

    def __init__(self, value="") -> None:
        super(StatusError, self).__init__(value)
        self.value = value

    def __str__(self) -> str:
        """Return the string representation of this exception.

        Returns:
            str: The string representation of this exception.
        """
        return self.value


class DependencyViolationError(Exception):
    """Raised when a TimeLog violates the dependency relation between tasks."""

    def __init__(self, value="") -> None:
        super(DependencyViolationError, self).__init__(value)
        self.value = value

    def __str__(self) -> str:
        """Return the string representation of this exception.

        Returns:
            str: The string representation of this exception.
        """
        return self.value
