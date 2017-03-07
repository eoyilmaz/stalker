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

import unittest
import datetime

import pytz
from sqlalchemy import Column, Integer, ForeignKey
from stalker.db.session import DBSession
from stalker.models.mixins import DateRangeMixin
from stalker.models.entity import SimpleEntity
from stalker.testing import UnitTestBase


class DeclSchedMixA(SimpleEntity, DateRangeMixin):
    __tablename__ = "DeclSchedMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclSchedMixA"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)

    def __init__(self, **kwargs):
        super(DeclSchedMixA, self).__init__(**kwargs)
        DateRangeMixin.__init__(self, **kwargs)


class DeclSchedMixB(SimpleEntity, DateRangeMixin):
    __tablename__ = "DeclSchedMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclSchedMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)

    def __init__(self, **kwargs):
        super(DeclSchedMixB, self).__init__(**kwargs)
        DateRangeMixin.__init__(self, **kwargs)


class ScheduleMixinTester(UnitTestBase):
    """tests DateRangeMixin setup
    """

    def setUp(self):
        """setup the test
        """
        super(ScheduleMixinTester, self).setUp()
        self.kwargs = {
            "name": "ozgur",
            "start": datetime.datetime(2013, 3, 20, 4, 0, tzinfo=pytz.utc),
            "end": datetime.datetime(2013, 3, 30, 4, 0, tzinfo=pytz.utc),
            "duration": datetime.timedelta(10)
        }

    def test_mixin_setup_is_working_properly(self):
        """testing if the mixin setup is working properly
        """
        new_A = DeclSchedMixA(**self.kwargs) # should not create any problem
        self.assertEqual(new_A.start, self.kwargs["start"])
        self.assertEqual(new_A.end, self.kwargs["end"])
        self.assertEqual(new_A.duration, self.kwargs["duration"])

        #print "----------------------------"
        #print new_A.start
        #print new_A.end
        #print new_A.duration

        # try to change the start and check if the duration is also updated
        new_A.start = \
            datetime.datetime(2013, 3, 30, 10, 0, tzinfo=pytz.utc)

        self.assertEqual(
            new_A.start,
            datetime.datetime(2013, 3, 30, 10, 0, tzinfo=pytz.utc)
        )
        self.assertEqual(
            new_A.end,
            datetime.datetime(2013, 4, 9, 10, 0, tzinfo=pytz.utc)
        )

        self.assertEqual(
            new_A.duration,
            datetime.timedelta(10)
        )

        a_start = new_A.start
        a_end = new_A.end
        a_duration = new_A.duration

        # now check the start, end and duration
        #print "----------------------------"
        #print new_A.start
        #print new_A.end
        #print new_A.duration

        # create a new class
        new_B = DeclSchedMixB(**self.kwargs)
        # now check the start, end and duration
        self.assertEqual(new_B.start, self.kwargs["start"])
        self.assertEqual(new_B.end, self.kwargs["end"])
        self.assertEqual(new_B.duration, self.kwargs["duration"])

        #print "----------------------------"
        #print new_B.start
        #print new_B.end
        #print new_B.duration

        # now check the start, end and duration of A
        #print "----------------------------"
        #print new_A.start
        #print new_A.end
        #print new_A.duration
        self.assertEqual(new_A.start, a_start)
        self.assertEqual(new_A.end, a_end)
        self.assertEqual(new_A.duration, a_duration)
