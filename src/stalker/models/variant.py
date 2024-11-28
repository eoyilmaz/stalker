# -*- coding: utf-8 -*-
"""Variant related functions and classes are situated here."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from stalker.models.task import Task


class Variant(Task):
    """A Task derivative to keep track of Variants in a Task hierarchy.

    The basic reason to have the Variant class is to upgrade the variants,
    into a Task derivative so that it is possible to create dependencies
    between different variants and being able to review them individually.

    You see, in previous versions of Stalker, the variants were handled as a
    part of the Version instances with a str attribute. The down side of that
    design was not being able to distinguish any reviews per variant.

    So, when a Model task is approved, all its variant approved all together,
    even if one of the variants were still getting worked on.

    The new design prevents that and gives the variant the level of attention
    they deserved.

    Variants doesn't introduce any new arguments or attributes. They are just
    initialized like any other Tasks.
    """

    __tablename__ = "Variants"
    __mapper_args__ = {"polymorphic_identity": "Variant"}
    variant_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Tasks.id"),
        primary_key=True,
    )
