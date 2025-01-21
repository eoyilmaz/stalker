# -*- coding: utf-8 -*-
"""ReferenceMixin related tests."""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from stalker import File, SimpleEntity
from stalker.models.mixins import ReferenceMixin


class DeclRefMixA(SimpleEntity, ReferenceMixin):
    """A test class for testing ReferenceMixin."""

    __tablename__ = "DeclRefMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclRefMixA"}
    a_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(DeclRefMixA, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)


class DeclRefMixB(SimpleEntity, ReferenceMixin):
    """A test class for testing ReferenceMixin."""

    __tablename__ = "RefMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclRefMixB"}
    b_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(DeclRefMixB, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)


def test_reference_mixin_setup():
    """ReferenceMixin setup."""
    a_ins = DeclRefMixA(name="ozgur")
    b_ins = DeclRefMixB(name="bozgur")

    new_file1 = File(name="test file 1", full_path="none")
    new_file2 = File(name="test file 2", full_path="no path")

    a_ins.references.append(new_file1)
    b_ins.references.append(new_file2)

    assert new_file1 in a_ins.references
    assert new_file2 in b_ins.references
