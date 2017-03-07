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


from sqlalchemy import Column, Integer, ForeignKey
from stalker import StatusMixin, StatusList, Status
from stalker.testing import UnitTestBase

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


class StatusMixinTester(UnitTestBase):
    """tests StatusMixin
    """

    def setUp(self):
        """setup the test
        """
        super(StatusMixinTester, self).setUp()

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

    def test_status_list_argument_not_set(self):
        """testing if a TypeError will be raised when the status_list argument
        is not set
        """
        self.kwargs.pop("status_list")
        with self.assertRaises(TypeError) as cm:
            DeclStatMixA(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            "DeclStatMixA instances can not be initialized without a "
            "stalker.models.status.StatusList instance, please pass a "
            "suitable StatusList (StatusList.target_entity_type=DeclStatMixA) "
            "with the 'status_list' argument"
        )

    def test_status_list_argument_is_not_correct(self):
        """testing if a TypeError will be raised when the given StatusList
        instance with the status_list argument is not suitable for this class
        """
        self.kwargs["status_list"] = self.test_b_statusList
        with self.assertRaises(TypeError) as cm:
            DeclStatMixA(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            "The given StatusLists' target_entity_type is DeclStatMixB, "
            "whereas the entity_type of this object is DeclStatMixA"
        )

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
