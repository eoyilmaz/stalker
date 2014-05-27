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
from sqlalchemy.orm import relationship, validates, synonym

from stalker import defaults
from stalker.models.auth import User
from stalker.models.entity import Entity

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Client(Entity):
    """The Client (company) which users may be part of.

    The information that a Client object holds is like:

      * The members of the client
      * and all the other things those are inherited from the AuditEntity class

    Two Client object considered the same if they have the same name.

    so creating a client object needs the following parameters:

    :param members: it can be an empty list, so one client can be created
      without any member in it. But this parameter should be a list of User
      objects.
    """
    __auto_name__ = False
    __tablename__ = "Clients"
    __mapper_args__ = {"polymorphic_identity": "Client"}
    client_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    )

    members = relationship(
        "User",
        secondary='User_Clients',
        back_populates="clients",
        doc="""List of users representing the members of this client.""",
    )

    users = synonym('members')

    def __init__(self, members=None, **kwargs):
        super(Client, self).__init__(**kwargs)

        if members is None:
            members = []

        self.members = members

    def __eq__(self, other):
        """the equality operator
        """
        return super(Client, self).__eq__(other) and \
            isinstance(other, Client)

    @validates("members")
    def _validate_members(self, key, member):
        """validates the given member attribute
        """
        if not isinstance(member, User):
            raise TypeError(
                "Every element in the %s.members list should be an instance "
                "of stalker.models.auth.User not %s" %
                (self.__class__.__name__, member.__class__.__name__)
            )
        return member

