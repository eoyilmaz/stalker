# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2018 Erkan Ozgur Yilmaz
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

import unittest
from stalker import Entity, Status


class StatusTest(unittest.TestCase):
    """tests the stalker.models.status.Status class
    """

    def setUp(self):
        """setup the test
        """
        super(StatusTest, self).setUp()

        self.kwargs = {
            'name': 'Complete',
            'description': 'use this when the object is complete',
            'code': 'CMPLT',
        }

        # create an entity object with same kwargs for __eq__ and __ne__ tests
        # (it should return False for __eq__ and True for __ne__ for same
        # kwargs)
        self.entity1 = Entity(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Status class
        """
        assert Status.__auto_name__ is False

    def test_equality(self):
        """testing equality of two statuses
        """
        status1 = Status(**self.kwargs)
        status2 = Status(**self.kwargs)

        self.kwargs["name"] = "Work In Progress"
        self.kwargs["description"] = "use this when the object is still in \
        progress"
        self.kwargs["code"] = "WIP"

        status3 = Status(**self.kwargs)

        assert status1 == status2
        assert not status1 == status3
        assert not status1 == self.entity1

    def test_status_and_string_equality_in_status_name(self):
        """testing a status can be compared with a string and returns True if
        the string matches the name and vice versa
        """
        a_status = Status(**self.kwargs)
        assert a_status == self.kwargs["name"]
        assert a_status == self.kwargs["name"].lower()
        assert a_status == self.kwargs["name"].upper()
        assert a_status != "another name"

    def test_status_and_string_equality_in_status_code(self):
        """testing a status can be compared with a string and returns True if
        the string matches the code and vice versa
        """
        a_status = Status(**self.kwargs)
        assert a_status == self.kwargs["code"]
        assert a_status == self.kwargs["code"].lower()
        assert a_status == self.kwargs["code"].upper()

    def test_inequality(self):
        """testing inequality of two statuses
        """
        status1 = Status(**self.kwargs)
        status2 = Status(**self.kwargs)

        self.kwargs["name"] = "Work In Progress"
        self.kwargs["description"] = "use this when the object is still in \
        progress"
        self.kwargs["code"] = "WIP"

        status3 = Status(**self.kwargs)

        assert not status1 != status2
        assert status1 != status3
        assert status1 != self.entity1

    def test_status_and_string_inequality_in_status_name(self):
        """testing a status can be compared with a string and returns False if
        the string matches the name and vice versa
        """
        a_status = Status(**self.kwargs)
        assert not a_status != self.kwargs["name"]
        assert not a_status != self.kwargs["name"].lower()
        assert not a_status != self.kwargs["name"].upper()
        assert a_status != "another name"

    def test_status_and_string_inequality_in_status_code(self):
        """testing a status can be compared with a string and returns False if
        the string matches the code and vice versa
        """
        a_status = Status(**self.kwargs)
        assert not a_status != self.kwargs["code"]
        assert not a_status != self.kwargs["code"].lower()
        assert not a_status != self.kwargs["code"].upper()
