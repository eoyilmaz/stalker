# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, validates
from stalker.db.declarative import Base

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

    .. note::
       .. versionadded 0.2.20: Client Specific Goods

       Clients now can own a list of :class:`.Good` s attached to them.
       So one can define a list of class:`.Good` s with special prices
       adjusted for a particular ``Client``, then get them back from the db by
       querying the :class:`.Good` s those have their ``client`` attribute set
       to that particular ``Client`` instance. Removing a ``Good`` from a
       :class:`.Client` will not delete it from the database, but deleting a
       :class:`.Client` will also delete the ``Good`` s attached to that
       particular :class:`.Client`.

    .. ::
       don't forget to update the Good documentation, which also has the same
       text.

    Two Client object considered the same if they have the same name.

    So creating a client object needs the following parameters:

    :param users: It can be an empty list, so one client can be created
      without any user in it. But this parameter should be a list of User
      objects.

    :type users: list of :class:`.User` s

    :param projects: it can be an empty list, so one client can be created
      without any project in it. But this parameter should be a list of Project
      objects.

    :type projects: :param type: list of :class:`.Project` s

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

    projects = association_proxy(
        'project_role',
        'project',
        creator=lambda p: create_project_client(p)
    )

    project_role = relationship(
        'ProjectClient',
        back_populates='client',
        cascade='all, delete-orphan',
        primaryjoin='Clients.c.id==Project_Clients.c.client_id'
    )

    goods = relationship(
        'Good',
        back_populates='client',
        cascade='all',  # do not include "delete-orphan" we want to keep goods
                        # if they are detached on purpose
        primaryjoin='Clients.c.id==Goods.c.client_id'
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

    def to_tjp(self):
        return ''

    @validates('goods')
    def _validate_good(self, key, good):
        """validates the given good value
        """
        from stalker.models.budget import Good
        if not isinstance(good, Good):
            raise TypeError(
                "%s.goods attribute should be all stalker.models.budget.Good "
                "instances, not %s" % (
                    self.__class__.__name__, good.__class__.__name__
                )
            )

        return good


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
                    '%s.role should be a '
                    'stalker.models.auth.Role instance, not %s' %
                    (self.__class__.__name__, role.__class__.__name__)
                )
        return role


def create_project_client(project):
    """helper function to create ProjectClient instance on association proxy
    """
    from stalker.models.project import ProjectClient
    return ProjectClient(project=project)
