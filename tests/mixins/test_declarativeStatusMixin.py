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

import unittest

from sqlalchemy import Column, Integer, ForeignKey
from stalker.db.session import DBSession
from stalker.models.mixins import StatusMixin
from stalker.models.status import StatusList, Status

# create a new mixed in SimpleEntity
from stalker.models.entity import SimpleEntity


class DeclStatMixA(SimpleEntity, StatusMixin):
    __tablename__ = "DeclStatMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclStatMixA"}
    declStatMixAs_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                              primary_key=True)

    def __init__(self, **kwargs):
        super(DeclStatMixA, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


class DeclStatMixB(SimpleEntity, StatusMixin):
    __tablename__ = "DeclStatMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclStatMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)

    def __init__(self, **kwargs):
        super(DeclStatMixB, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


class StatusMixinTester(unittest.TestCase):
    """tests StatusMixin
    """

    def setUp(self):
        """setup the test
        """
        self.test_stat1 = Status(name="On Hold", code="OH")
        self.test_stat2 = Status(name="Work In Progress", code="WIP")
        self.test_stat3 = Status(name="Approved", code="APP")

        self.test_a_statusList = StatusList(
            name="A Statuses",
            statuses=[self.test_stat1, self.test_stat3],
            target_entity_type="DeclStatMixA",
            )

        self.test_b_statusList = StatusList(
            name="B Statuses",
            statuses=[self.test_stat2, self.test_stat3],
            target_entity_type="DeclStatMixB"
        )

        self.kwargs = {
            "name": "ozgur",
            "status_list": self.test_a_statusList
        }

    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()

    def test_status_list_argument_not_set(self):
        """testing if a TypeError will be raised when the status_list argument
        is not set
        """
        self.kwargs.pop("status_list")
        self.assertRaises(TypeError, DeclStatMixA, **self.kwargs)

    def test_status_list_argument_is_not_correct(self):
        """testing if a TypeError will be raised when the given StatusList
        instance with the status_list argument is not suitable for this class
        """
        self.kwargs["status_list"] = self.test_b_statusList
        self.assertRaises(TypeError, DeclStatMixA, **self.kwargs)

    def test_status_list_working_properly(self):
        """testing if the status_list attribute is working properly
        """
        new_a_ins = DeclStatMixA(
            name="Ozgur",
            status_list=self.test_a_statusList
        )

        self.assertTrue(self.test_stat1 in new_a_ins.status_list)
        self.assertFalse(self.test_stat2 in new_a_ins.status_list)
        self.assertTrue(self.test_stat3 in new_a_ins.status_list)
