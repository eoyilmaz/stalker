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
from stalker.models.entity import SimpleEntity
from stalker.models.mixins import ReferenceMixin
from stalker.models.link import Link


class DeclRefMixA(SimpleEntity, ReferenceMixin):
    """A test class for ReferenceMixin
    """

    __tablename__ = "DeclRefMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclRefMixA"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)

    def __init__(self, **kwargs):
        super(DeclRefMixA, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)


class DeclRefMixB(SimpleEntity, ReferenceMixin):
    """A test class for ReferenceMixin
    """

    __tablename__ = "RefMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclRefMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)

    def __init__(self, **kwargs):
        super(DeclRefMixB, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)


class ReferenceMixinTester(unittest.TestCase):
    """Tests ReferenceMixin
    """


    def test_ReferenceMixin_setup(self):
        """
        """
        a_ins = DeclRefMixA(name="ozgur")
        b_ins = DeclRefMixB(name="bozgur")

        new_link1 = Link(name="test link 1", full_path="none")
        new_link2 = Link(name="test link 2", full_path="no path")

        a_ins.references.append(new_link1)
        b_ins.references.append(new_link2)

        self.assertTrue(new_link1 in a_ins.references)
        self.assertTrue(new_link2 in b_ins.references)

    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()
        # DBSession.close()




