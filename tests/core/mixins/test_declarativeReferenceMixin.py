# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause


import unittest

from stalker.core.models import SimpleEntity, Link, ReferenceMixin
from sqlalchemy import Column, Integer, ForeignKey


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

        new_link1 = Link(name="test link 1", path="none")
        new_link2 = Link(name="test link 2", path="no path")

        a_ins.references.append(new_link1)
        b_ins.references.append(new_link2)

        self.assertIn(new_link1, a_ins.references)
        self.assertIn(new_link2, b_ins.references)



