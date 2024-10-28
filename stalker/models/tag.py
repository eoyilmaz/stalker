# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey

from stalker.models.entity import SimpleEntity

from stalker.log import get_logger

logger = get_logger(__name__)


class Tag(SimpleEntity):
    """Use it to create tags for any object available in SOM.

    Doesn't have any other attribute than what is inherited from
    :class:`.SimpleEntity`
    """

    __auto_name__ = False
    __tablename__ = "Tags"
    __mapper_args__ = {"polymorphic_identity": "Tag"}
    tag_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)

    def __eq__(self, other):
        """Check the equality.

        Args:
            other (object): The other object.

        Returns:
            bool: True if the other object is a Tag instance and has the same
                attributes.
        """
        return super(Tag, self).__eq__(other) and isinstance(other, Tag)

    def __hash__(self):
        """the overridden __hash__ method"""
        return super(Tag, self).__hash__()
