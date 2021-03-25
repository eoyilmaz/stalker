# -*- coding: utf-8 -*-
"""Errors for the system.

This module contains the Errors in Stalker.
"""


class LoginError(Exception):
    """Raised when the login information is not correct or not correlate with
    the data in the database.
    """

    def __init__(self, value=""):
        super(LoginError, self).__init__(value)
        self.value = value

    def __str__(self):
        return self.value


class CircularDependencyError(Exception):
    """Raised when there is circular dependencies within Tasks
    """
    def __init__(self, value=""):
        super(CircularDependencyError, self).__init__(value)
        self.value = value

    def __str__(self):
        return self.value


class OverBookedError(Exception):
    """Raised when a resource is booked more than once for the same time period
    """

    def __init__(self, value=""):
        super(OverBookedError, self).__init__(value)
        self.value = value

    def __str__(self):
        return self.value


class StatusError(Exception):
    """Raised when the status of an entity is not suitable for the desired
    action
    """

    def __init__(self, value=""):
        super(StatusError, self).__init__(value)
        self.value = value

    def __str__(self):
        return self.value


class DependencyViolationError(Exception):
    """Raised when a TimeLog violates the dependency relation between tasks
    """

    def __init__(self, value=""):
        super(DependencyViolationError, self).__init__(value)
        self.value = value

    def __str__(self):
        return self.value
