# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey
from stalker.models.entity import SimpleEntity

class Tag(SimpleEntity):
    """Use it to create tags for any object available in SOM.
    
    Doesn't have any other attribute than what is inherited from
    :class:`~stalker.core.models.SimpleEntity`
    """

    __tablename__ = "Tags"
    __mapper_args__ = {"polymorphic_identity": "Tag"}
    tag_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                    primary_key=True)

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)

    def __eq__(self, other):
        """the equality operator
        """

        return super(Tag, self).__eq__(other) and isinstance(other, Tag)

    def __ne__(self, other):
        """the inequality operator
        """

        return not self.__eq__(other)
