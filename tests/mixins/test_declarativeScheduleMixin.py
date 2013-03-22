# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
import datetime

from sqlalchemy import Column, Integer, ForeignKey
from stalker.db.session import DBSession
from stalker.models.mixins import ScheduleMixin
from stalker.models.entity import SimpleEntity

class DeclSchedMixA(SimpleEntity, ScheduleMixin):
    __tablename__ = "DeclSchedMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclSchedMixA"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)


    def __init__(self, **kwargs):
        super(DeclSchedMixA, self).__init__(**kwargs)
        ScheduleMixin.__init__(self, **kwargs)


class DeclSchedMixB(SimpleEntity, ScheduleMixin):
    __tablename__ = "DeclSchedMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclSchedMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)


    def __init__(self, **kwargs):
        super(DeclSchedMixB, self).__init__(**kwargs)
        ScheduleMixin.__init__(self, **kwargs)


class ScheduleMixinTester(unittest.TestCase):
    """tests ScheduleMixin setup
    """


    def setUp(self):
        """setup the test
        """

        self.kwargs = {
            "name": "ozgur",
            "start": datetime.datetime(2013, 3, 22, 4, 0),
            "end": datetime.datetime(2013, 13, 22, 4, 0),
            "duration": datetime.timedelta(10)
        }

    def tearDown(self):
        """clean up the test
        """
        if DBSession:
            DBSession.close()

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
        
        # try to change the start and check if the duration is also
        # updated
        new_A.start = datetime.datetime.today() + datetime.timedelta(20)
        
        self.assertEqual(new_A.start, datetime.date.today() +
                                           datetime.timedelta(20))
        self.assertEqual(new_A.end, self.kwargs["end"] +
                                         datetime.timedelta(20))
        self.assertEqual(new_A.duration, datetime.timedelta(10))

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
    
