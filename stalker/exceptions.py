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
        return repr(self.value)


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
        return repr(self.value)
