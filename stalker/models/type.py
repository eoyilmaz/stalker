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

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import TargetEntityTypeMixin, CodeMixin

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Type(Entity, TargetEntityTypeMixin, CodeMixin):
    """Everything can have a type.

    .. versionadded:: 0.1.1
      Types

    Type is a generalized version of the previous design that defines types for
    specific classes.

    The purpose of the :class:`.Type` class is just to define a new type for a
    specific :class:`.Entity`. For example, you can have a ``Character``
    :class:`.Asset` or you can have a ``Commercial`` :class:`.Project` or you
    can define a :class:`.Link` as an ``Image`` etc., to create a new
    :class:`.Type` for various classes::

      Type(name="Character", target_entity_type="Asset")
      Type(name="Commercial", target_entity_type="Project")
      Type(name="Image", target_entity_type="Link")

    or::

      Type(name="Character", target_entity_type=Asset.entity_type)
      Type(name="Commercial", target_entity_type=Project.entity_type)
      Type(name="Image", target_entity_type=Link.entity_type)

    or even better:

      Type(name="Character", target_entity_type=Asset)
      Type(name="Commercial", target_entity_type=Project)
      Type(name="Image", target_entity_type=Link)

    By using :class:`.Type`\ s, one can able to sort and group same type of
    entities.

    :class:`.Type`\ s are generally used in :class:`.Structure`\ s.

    :param string target_entity_type: The string defining the target type of
      this :class:`.Type`.
    """
    __auto_name__ = False
    __tablename__ = "Types"
    __mapper_args__ = {"polymorphic_identity": "Type"}
    type_id_local = Column("id", Integer, ForeignKey("Entities.id"),
                           primary_key=True)

    def __init__(self, name=None, code=None, target_entity_type=None,
                 **kwargs):
        kwargs['name'] = name
        kwargs['target_entity_type'] = target_entity_type
        super(Type, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, **kwargs)
        #CodeMixin.__init__(self, **kwargs)
        self.code = code

    def __eq__(self, other):
        """the equality operator
        """
        return super(Type, self).__eq__(other) and isinstance(other, Type) \
            and self.target_entity_type == other.target_entity_type

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Type, self).__hash__()


class EntityType(Base):
    """A simple class just to hold the registered class names in Stalker
    """
    __tablename__ = 'EntityTypes'
    __table_args__ = ({"extend_existing": True})

    id = Column("id", Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    statusable = Column(Boolean, default=False)
    dateable = Column(Boolean, default=False)
    schedulable = Column(Boolean, default=False)
    accepts_references = Column(Boolean, default=False)

    def __init__(
            self,
            name,
            statusable=False,
            schedulable=False,
            accepts_references=False):
        self.name = name
        self.statusable = statusable
        self.schedulable = schedulable
        self.accepts_references = accepts_references

        # TODO: add tests for the name attribute
