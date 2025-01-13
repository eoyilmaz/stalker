# -*- coding: utf-8 -*-
"""Type related functions and classes are situated here."""

from typing import Any, Dict, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from stalker.db.declarative import Base
from stalker.log import get_logger
from stalker.models.entity import Entity
from stalker.models.mixins import CodeMixin, TargetEntityTypeMixin

logger = get_logger(__name__)


class Type(Entity, TargetEntityTypeMixin, CodeMixin):
    """Everything can have a type.

    .. versionadded:: 0.1.1
      Types

    Type is a generalized version of the previous design that defines types for
    specific classes.

    The purpose of the :class:`.Type` class is just to define a new type for a
    specific :class:`.Entity`. For example, you can have a ``Character``
    :class:`.Asset` or you can have a ``Commercial`` :class:`.Project` or you
    can define a :class:`.File` as an ``Image`` etc., to create a new
    :class:`.Type` for various classes:

    ..code-block: Python

        Type(name="Character", target_entity_type="Asset")
        Type(name="Commercial", target_entity_type="Project")
        Type(name="Image", target_entity_type="File")

    or:

    ..code-block: Python

        Type(name="Character", target_entity_type=Asset.entity_type)
        Type(name="Commercial", target_entity_type=Project.entity_type)
        Type(name="Image", target_entity_type=File.entity_type)

    or even better:

    ..code-block: Python

        Type(name="Character", target_entity_type=Asset)
        Type(name="Commercial", target_entity_type=Project)
        Type(name="Image", target_entity_type=File)

    By using :class:`.Type` s, one can able to sort and group same type of
    entities.

    :class:`.Type` s are generally used in :class:`.Structure` s.

    Args:
        target_entity_type (str): The string defining the target type of this
            :class:`.Type`.
    """

    __auto_name__ = False
    __tablename__ = "Types"
    __mapper_args__ = {"polymorphic_identity": "Type"}
    type_id_local: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    def __init__(
        self,
        name: Optional[str] = None,
        code: Optional[str] = None,
        target_entity_type: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        kwargs["name"] = name
        kwargs["target_entity_type"] = target_entity_type
        super(Type, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, **kwargs)
        # CodeMixin.__init__(self, **kwargs)
        self.code = code

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is equal to this Type instance as an Entity
                and has the same target_entity_type.
        """
        return (
            super(Type, self).__eq__(other)
            and isinstance(other, Type)
            and self.target_entity_type == other.target_entity_type
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Type, self).__hash__()


class EntityType(Base):
    """A simple class just to hold the registered class names in Stalker."""

    __tablename__ = "EntityTypes"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column("id", primary_key=True)
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True,
    )
    statusable: Mapped[Optional[bool]] = mapped_column(default=False)
    dateable: Mapped[Optional[bool]] = mapped_column(default=False)
    schedulable: Mapped[Optional[bool]] = mapped_column(default=False)
    accepts_references: Mapped[Optional[bool]] = mapped_column(default=False)

    def __init__(
        self,
        name: str,
        statusable: bool = False,
        schedulable: bool = False,
        accepts_references: bool = False,
    ) -> None:
        self.name = name
        self.statusable = statusable
        self.schedulable = schedulable
        self.accepts_references = accepts_references

        # TODO: add tests for the name attribute
