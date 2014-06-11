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

    users = relationship(
        "User",
        primaryjoin='Users.c.company_id==Clients.c.id',
        back_populates="company",
        doc="""List of users representing the employees of this client.""",
    )

    projects = relationship(
        "Project",
        primaryjoin='Projects.c.client_id==Clients.c.id',
        back_populates="client",
        doc="""List of projects affiliated with this client.""",
    )

    members = synonym('users')

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

    @validates("users")
    def _validate_users(self, key, user):
        """validates the given user value
        """
        from stalker.models.auth import User

        if not isinstance(user, User):
            raise TypeError(
                "Every element in the %s.users list should be an instance "
                "of stalker.models.auth.User not %s" %
                (self.__class__.__name__, user.__class__.__name__)
            )
        return user

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
