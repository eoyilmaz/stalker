# -*- coding: utf-8 -*-
"""Asset related classes."""

import logging
from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from stalker import log
from stalker.models.mixins import CodeMixin, ReferenceMixin
from stalker.models.task import Task

logger: logging.Logger = log.get_logger(__name__)
log.set_level(log.logging_level)


class Asset(Task, CodeMixin):
    """The Asset class is the whole idea behind Stalker.

    *Assets* are containers of :class:`.Task` s. And :class:`.Task` s are the
    smallest meaningful part that should be accomplished to complete the
    :class:`.Project`.

    An example could be given as follows; you can create an asset for one of
    the characters in your project. Than you can divide this character asset in
    to :class:`.Task` s. These :class:`.Task` s can be defined by the type of
    the :class:`.Asset`, which is a :class:`.Type` object created specifically
    for :class:`.Asset` (ie. has its :attr:`.Type.target_entity_type` set to
    "Asset"),

    An :class:`.Asset` instance should be initialized with a :class:`.Project`
    instance (as the other classes which are mixed with the
    :class:`.TaskMixin`). And when a :class:`.Project` instance is given then
    the asset will append itself to the :attr:`.Project.assets` list.

    ..versionadded: 0.2.0:
        No more Asset to Shot connection:

        Assets now are not directly related to Shots. Instead a
        :class:`.Version` will reference the Asset and then it is easy to track
        which shots are referencing this Asset by querying with a join of Shot
        Versions referencing this Asset.
    """

    __auto_name__ = False
    __strictly_typed__ = True
    __tablename__ = "Assets"
    __mapper_args__ = {"polymorphic_identity": "Asset"}

    asset_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Tasks.id"), primary_key=True
    )

    def __init__(self, code, **kwargs) -> None:
        kwargs["code"] = code

        super(Asset, self).__init__(**kwargs)
        CodeMixin.__init__(self, **kwargs)
        ReferenceMixin.__init__(self, **kwargs)

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object equals to this asset.
        """
        return (
            super(Asset, self).__eq__(other)
            and isinstance(other, Asset)
            and self.type == other.type
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Asset, self).__hash__()
