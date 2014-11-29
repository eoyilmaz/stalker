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
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, validates
from stalker.db import Base

from stalker.models.entity import Entity

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Client(Entity):
    """The Client (e.g. a company) which users may be part of.

    The information that a Client object holds is like:

      * The users of the client
      * The projects affiliated with the client
      * and all the other things those are inherited from the Entity class

    Two Client object considered the same if they have the same name.

    so creating a client object needs the following parameters:

    :param users: It can be an empty list, so one client can be created
      without any user in it. But this parameter should be a list of User
      objects.

    :type users: list of :class:`.User`\ s

    :param projects: it can be an empty list, so one client can be created
      without any project in it. But this parameter should be a list of Project
      objects.

    :type projects: :param type: list of :class:`.Project`\ s

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

    users = association_proxy(
        'user_role',
        'user',
        creator=lambda n: ClientUser(user=n)
    )

    user_role = relationship(
        "ClientUser",
        back_populates="client",
        cascade='all, delete-orphan',
        primaryjoin='Clients.c.id==Client_Users.c.cid',
        doc="""List of users representing the members of this client."""
    )

    projects = relationship(
        "Project",
        primaryjoin='Projects.c.client_id==Clients.c.id',
        back_populates="client",
        doc="""List of projects affiliated with this client.""",
    )

    def __init__(
            self,
            users=None,
            projects=None,
            **kwargs):
        super(Client, self).__init__(**kwargs)

        if users is None:
            users = []

        if projects is None:
            projects = []

        self.users = users
        self.projects = projects

    def __eq__(self, other):
        """the equality operator
        """
        return super(Client, self).__eq__(other) and \
            isinstance(other, Client)

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Client, self).__hash__()

    @validates("projects")
    def _validate_projects(self, key, project):
        """validates the given project attribute
        """
        from stalker.models.project import Project

        if not isinstance(project, Project):
            raise TypeError(
                "Every element in the %s.projects list should be an instance "
                "of stalker.models.project.Project not %s" %
                (self.__class__.__name__, project.__class__.__name__)
            )
        return project

    def to_tjp(self):
        return ''


class ClientUser(Base):
    """The association object used in Client-to-User relation

    :param client: The client which the user is affiliated with.

    :type client: :class:`.Client`

    :param user: A :class:`.User` instance.

    :type user: :class:`.User`

    """

    __tablename__ = 'Client_Users'

    user_id = Column(
        'uid',
        Integer,
        ForeignKey('Users.id'),
        primary_key=True
    )

    user = relationship(
        'User',
        back_populates='company_role',
        primaryjoin='ClientUser.user_id==User.user_id'
    )

    client_id = Column(
        'cid',
        Integer,
        ForeignKey('Clients.id'),
        primary_key=True
    )

    client = relationship(
        'Client',
        back_populates='user_role',
        primaryjoin='ClientUser.client_id==Client.client_id',
    )

    role_id = Column(
        'rid',
        Integer,
        ForeignKey('Roles.id'),
        nullable=True
    )

    role = relationship(
        'Role',
        primaryjoin='ClientUser.role_id==Role.role_id'
    )

    def __init__(self, client=None, user=None, role=None):
        self.user = user
        self.client = client
        self.role = role

    @validates("client")
    def _validate_client(self, key, client):
        """validates the given client value
        """
        if client is not None:
            if not isinstance(client, Client):
                raise TypeError(
                    "%s.client should be instance of "
                    "stalker.models.client.Client, not %s" %
                    (self.__class__.__name__, client.__class__.__name__)
                )
        return client

    @validates("user")
    def _validate_user(self, key, user):
        """validates the given user value
        """
        if user is not None:
            from stalker.models.auth import User
            if not isinstance(user, User):
                raise TypeError(
                    "%s.user should be an instance of "
                    "stalker.models.auth.User, not %s" %
                    (self.__class__.__name__, user.__class__.__name__)
                )
        return user

    @validates('role')
    def _validate_role(self, key, role):
        """validates the given role instance
        """
        if role is not None:
            from stalker import Role
            if not isinstance(role, Role):
                raise TypeError(
                    '%s.role should be a'
                    'stalker.models.auth.Role instance, not %s' %
                    (self.__class__.__name__, role.__class__.__name__)
                )
        return role
