# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from sqlalchemy import Column, Integer, ForeignKey

from stalker.models.entity import SimpleEntity

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Tag(SimpleEntity):
    """Use it to create tags for any object available in SOM.

    Doesn't have any other attribute than what is inherited from
    :class:`.SimpleEntity`
    """
    __auto_name__ = False
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

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Tag, self).__hash__()
