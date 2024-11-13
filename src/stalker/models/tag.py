# -*- coding: utf-8 -*-
"""Tag related functions and classes are situated here."""
from typing import Any, Dict

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from stalker.log import get_logger
from stalker.models.entity import SimpleEntity

logger = get_logger(__name__)


class Tag(SimpleEntity):
    """Use it to create tags for any object available in SOM.

    Doesn't have any other attribute than what is inherited from
    :class:`.SimpleEntity`
    """

    __auto_name__ = False
    __tablename__ = "Tags"
    __mapper_args__ = {"polymorphic_identity": "Tag"}
    tag_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super(Tag, self).__init__(**kwargs)

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a Tag instance and has the same
                attributes.
        """
        return super(Tag, self).__eq__(other) and isinstance(other, Tag)

    def __hash__(self) -> int:
        """Return the hash value for this Tag instance.

        Returns:
            int: The hash of this Tag.
        """
        return super(Tag, self).__hash__()
