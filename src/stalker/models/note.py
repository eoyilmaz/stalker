# -*- coding: utf-8 -*-
"""Note class lies here."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import synonym

from stalker.log import get_logger
from stalker.models.entity import SimpleEntity

logger = get_logger(__name__)


class Note(SimpleEntity):
    """Notes for any of the SOM objects.

    To leave notes in Stalker use the Note class.

    Args:
        content (str): The content of the note.
        attached_to (Entity): The object that this note is attached to.
    """

    __auto_name__ = True
    __tablename__ = "Notes"
    __mapper_args__ = {"polymorphic_identity": "Note"}

    note_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    content = synonym(
        "description",
        doc="""The content of this :class:`.Note` instance.

        Content is a string representing the content of this Note, can be an
        empty.
        """,
    )

    def __init__(self, content="", **kwargs):
        super(Note, self).__init__(**kwargs)
        self.content = content

    def __eq__(self, other):
        """Check the equality.

        Args:
            other (object): The other object.

        Returns:
            bool: True if the other object is a Note instance and has the same content.
        """
        return (
            super(Note, self).__eq__(other)
            and isinstance(other, Note)
            and self.content == other.content
        )

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Note, self).__hash__()