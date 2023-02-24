# -*- coding: utf-8 -*-
"""ReferenceMixin related tests."""
from sqlalchemy import Column, ForeignKey, Integer

from stalker import Link, SimpleEntity
from stalker.models.mixins import ReferenceMixin


class DeclRefMixA(SimpleEntity, ReferenceMixin):
    """A test class for testing ReferenceMixin."""

    __tablename__ = "DeclRefMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclRefMixA"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    def __init__(self, **kwargs):
        super(DeclRefMixA, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)


class DeclRefMixB(SimpleEntity, ReferenceMixin):
    """A test class for testing ReferenceMixin."""

    __tablename__ = "RefMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclRefMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    def __init__(self, **kwargs):
        super(DeclRefMixB, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)


def test_reference_mixin_setup():
    """ReferenceMixin setup."""
    a_ins = DeclRefMixA(name="ozgur")
    b_ins = DeclRefMixB(name="bozgur")

    new_link1 = Link(name="test link 1", full_path="none")
    new_link2 = Link(name="test link 2", full_path="no path")

    a_ins.references.append(new_link1)
    b_ins.references.append(new_link2)

    assert new_link1 in a_ins.references
    assert new_link2 in b_ins.references
