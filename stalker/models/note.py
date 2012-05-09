# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import validates
from stalker.models.entity import SimpleEntity

class Note(SimpleEntity):
    """Notes for any of the SOM objects.
    
    To leave notes in Stalker use the Note class.
    
    :param content: the content of the note
    
    :param attached_to: The object that this note is attached to.
    """

    __tablename__ = "Notes"
    __mapper_args__ = {"polymorphic_identity": "Note"}

    note_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )

    entity_id = Column(
        "entity_id",
        Integer,
        ForeignKey("Entities.id")
    )

    content = Column(
        String,
        doc="""The content of this :class:`~stalker.core.models.Note` instance.
        
        Content is a string representing the content of this Note, can be given
        as an empty string or can be even None, but anything other than None or
        string or unicode will raise a TypeError.
        """
    )

    def __init__(self, content="", **kwargs):
        super(Note, self).__init__(**kwargs)
        self.content = content

    @validates("content")
    def _validate_content(self, key, content_in):
        """validates the given content
        """

        if content_in is not None and\
           not isinstance(content_in, (str, unicode)):
            raise TypeError("%s.content should be an instance of string or "
                            "unicode not %s" %
                            (self.__class__.__name__,
                             content_in.__class__.__name__))

        return content_in

    def __eq__(self, other):
        """the equality operator
        """

        return super(Note, self).__eq__(other) and\
               isinstance(other, Note) and\
               self.content == other.content
