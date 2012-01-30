# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
"""Errors for the system.

This module contains the Errors in Stalker.
"""

class LoginError(Exception):
    """Raised when the login information is not correct or not correlate with the data in the database.
    """

    def __init__(self, value=""):
        super(LoginError, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


class DBError(Exception):
    """Raised when there is no database and a database related action has been placed.
    """

    def __init__(self, value=""):
        super(DBError, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


class CircularDependencyError(Exception):
    """Raised when there is cirular dependencies within Tasks
    """

    def __init__(self, value=""):
        super(CircularDependencyError, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


class OverBookedWarning(Warning):
    """Raised when a resource is booked more than once for the same time period
    """

    def __init__(self, value=""):
        super(OverBookedWarning, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)
