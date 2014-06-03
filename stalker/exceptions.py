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


class DBError(Exception):
    """Raised when there is no database and a database related action has been
    placed.
    """

    def __init__(self, value=""):
        super(DBError, self).__init__(value)
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
        return repr(self.value)


class OverBookedError(Exception):
    """Raised when a resource is booked more than once for the same time period
    """

    def __init__(self, value=""):
        super(OverBookedError, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


class StatusError(Exception):
    """Raised when the status of an entity is not suitable for the desired
    action
    """

    def __init__(self, value=""):
        super(StatusError, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


class DependencyViolationError(Exception):
    """Raised when a TimeLog violates the dependency relation between tasks
    """

    def __init__(self, value=""):
        super(DependencyViolationError, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)
