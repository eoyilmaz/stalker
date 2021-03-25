# -*- coding: utf-8 -*-

import unittest
import datetime

import pytz
from sqlalchemy import Column, Integer, ForeignKey
from stalker.models.mixins import DateRangeMixin
from stalker.models.entity import SimpleEntity


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


class ScheduleMixinTester(unittest.TestCase):
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
        assert new_A.start == self.kwargs["start"]
        assert new_A.end == self.kwargs["end"]
        assert new_A.duration == self.kwargs["duration"]

        # print "----------------------------"
        # print new_A.start
        # print new_A.end
        # print new_A.duration

        # try to change the start and check if the duration is also updated
        new_A.start = \
            datetime.datetime(2013, 3, 30, 10, 0, tzinfo=pytz.utc)

        assert new_A.start == \
               datetime.datetime(2013, 3, 30, 10, 0, tzinfo=pytz.utc)

        assert new_A.end == \
               datetime.datetime(2013, 4, 9, 10, 0, tzinfo=pytz.utc)

        assert new_A.duration == datetime.timedelta(10)

        a_start = new_A.start
        a_end = new_A.end
        a_duration = new_A.duration

        # now check the start, end and duration
        # print "----------------------------"
        # print new_A.start
        # print new_A.end
        # print new_A.duration

        # create a new class
        new_B = DeclSchedMixB(**self.kwargs)
        # now check the start, end and duration
        assert new_B.start == self.kwargs["start"]
        assert new_B.end == self.kwargs["end"]
        assert new_B.duration == self.kwargs["duration"]

        # print "----------------------------"
        # print new_B.start
        # print new_B.end
        # print new_B.duration

        # now check the start, end and duration of A
        # print "----------------------------"
        # print new_A.start
        # print new_A.end
        # print new_A.duration
        assert new_A.start == a_start
        assert new_A.end == a_end
        assert new_A.duration == a_duration
