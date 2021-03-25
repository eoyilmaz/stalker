# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import synonym
from stalker.models.entity import SimpleEntity

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Note(SimpleEntity):
    """Notes for any of the SOM objects.

    To leave notes in Stalker use the Note class.

    :param content: the content of the note

    :param attached_to: The object that this note is attached to.
    """
    __auto_name__ = True
    __tablename__ = "Notes"
    __mapper_args__ = {"polymorphic_identity": "Note"}

    note_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )

    content = synonym(
        'description',
        doc="""The content of this :class:`.Note` instance.

        Content is a string representing the content of this Note, can be an
        empty.
        """
    )

    def __init__(self, content="", **kwargs):
        super(Note, self).__init__(**kwargs)
        self.content = content

    def __eq__(self, other):
        """the equality operator
        """
        return super(Note, self).__eq__(other) and \
            isinstance(other, Note) and \
            self.content == other.content

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Note, self).__hash__()
