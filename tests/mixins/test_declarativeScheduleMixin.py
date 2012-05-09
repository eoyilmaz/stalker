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
            "start_date": datetime.date.today(),
            "due_date": datetime.date.today() + datetime.timedelta(10),
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
        self.assertEqual(new_A.start_date, self.kwargs["start_date"])
        self.assertEqual(new_A.due_date, self.kwargs["due_date"])
        self.assertEqual(new_A.duration, self.kwargs["duration"])

        #print "----------------------------"
        #print new_A.start_date
        #print new_A.due_date
        #print new_A.duration

        # try to change the start_date and check if the duration is also
        # updated
        new_A.start_date = datetime.date.today() + datetime.timedelta(20)

        self.assertEqual(new_A.start_date, datetime.date.today() +
                                           datetime.timedelta(20))
        self.assertEqual(new_A.due_date, self.kwargs["due_date"] +
                                         datetime.timedelta(20))
        self.assertEqual(new_A.duration, datetime.timedelta(10))

        a_start_date = new_A.start_date
        a_due_date = new_A.due_date
        a_duration = new_A.duration

        # now check the start_date, due_date and duration
        #print "----------------------------"
        #print new_A.start_date
        #print new_A.due_date
        #print new_A.duration

        # create a new class
        new_B = DeclSchedMixB(**self.kwargs)
        # now check the start_date, due_date and duration
        self.assertEqual(new_B.start_date, self.kwargs["start_date"])
        self.assertEqual(new_B.due_date, self.kwargs["due_date"])
        self.assertEqual(new_B.duration, self.kwargs["duration"])

        #print "----------------------------"
        #print new_B.start_date
        #print new_B.due_date
        #print new_B.duration

        # now check the start_date, due_date and duration of A
        #print "----------------------------"
        #print new_A.start_date
        #print new_A.due_date
        #print new_A.duration
        self.assertEqual(new_A.start_date, a_start_date)
        self.assertEqual(new_A.due_date, a_due_date)
        self.assertEqual(new_A.duration, a_duration)
        
        
    
    
    
    
    
    
