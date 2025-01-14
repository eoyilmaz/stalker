# -*- coding: utf-8 -*-
"""Client related classes and functions are situated here."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from stalker import log
from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.project import create_project_client

if TYPE_CHECKING:  # pragma: no cover
    from stalker.models.auth import Role, User
    from stalker.models.budget import Good
    from stalker.models.project import Project, ProjectClient

logger = log.get_logger(__name__)


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

    Args:
        users (:class:`.User`): It can be an empty list, so one client can be created
            without any user in it. But this parameter should be a list of User objects.

        projects (List[Project]): it can be an empty list, so one client can be created
            without any project in it. But this parameter should be a list of Project
            objects.
    """

    __auto_name__ = False
    __tablename__ = "Clients"
    __mapper_args__ = {"polymorphic_identity": "Client"}
    client_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    users = association_proxy("user_role", "user", creator=lambda n: ClientUser(user=n))

    user_role: Mapped[Optional[List["ClientUser"]]] = relationship(
        back_populates="client",
        cascade="all, delete-orphan",
        primaryjoin="Clients.c.id==Client_Users.c.cid",
        doc="""List of users representing the members of this client.""",
    )

    projects = association_proxy(
        "project_role", "project", creator=lambda p: create_project_client(p)
    )

    project_role: Mapped[Optional[List["ProjectClient"]]] = relationship(
        back_populates="client",
        cascade="all, delete-orphan",
        primaryjoin="Clients.c.id==Project_Clients.c.client_id",
    )

    goods: Mapped[Optional[List["Good"]]] = relationship(
        "Good",
        back_populates="client",
        cascade="all",  # do not include "delete-orphan" we want to keep goods
        # if they are detached on purpose
        primaryjoin="Clients.c.id==Goods.c.client_id",
    )

    def __init__(
        self,
        users: Optional[List["User"]] = None,
        projects: Optional[List["Project"]] = None,
        **kwargs: Optional[Dict[str, Any]],
    ) -> None:
        super(Client, self).__init__(**kwargs)

        if users is None:
            users = []

        if projects is None:
            projects = []

        self.users = users
        self.projects = projects

    def __eq__(self, other: Any) -> bool:
        """Check if the other Client is equal to this once.

        Args:
            other (Any): The other Client instance.

        Returns:
            bool: Returns True, if other object is a Client instance and equal to this
                one.
        """
        return super(Client, self).__eq__(other) and isinstance(other, Client)

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Client, self).__hash__()

    @property
    def to_tjp(self) -> str:
        """Return a TaskJuggler compatible str representation of this Client instance.

        Returns:
            str: The TaskJuggler compatible representation of this Client instance.
        """
        return ""

    @validates("goods")
    def _validate_good(self, key: str, good: "Good") -> "Good":
        """Validate the given good value.

        Args:
            key (str): The name of the validated column.
            good (Good): The good value to be validated.

        Raises:
            TypeError: If the given good is not a :class:`stalker.models.budget.Good`
                instance.

        Returns:
            Good: The validated good value.
        """
        from stalker.models.budget import Good

        if not isinstance(good, Good):
            raise TypeError(
                f"{self.__class__.__name__}.goods should only "
                "contain instances of stalker.models.budget.Good, "
                f"not {good.__class__.__name__}: '{good}'"
            )

        return good


class ClientUser(Base):
    """The association object used in Client-to-User relation.

    Args:
        client (Client): The client which the user is affiliated with.
        user (User): A :class:`.User` instance.
    """

    __tablename__ = "Client_Users"
    user_id: Mapped[int] = mapped_column(
        "uid", ForeignKey("Users.id"), primary_key=True
    )
    user: Mapped["User"] = relationship(
        back_populates="company_role",
        primaryjoin="ClientUser.user_id==User.user_id",
    )
    client_id: Mapped[int] = mapped_column(
        "cid", ForeignKey("Clients.id"), primary_key=True
    )
    client: Mapped["Client"] = relationship(
        back_populates="user_role",
        primaryjoin="ClientUser.client_id==Client.client_id",
    )
    role_id: Mapped[Optional[int]] = mapped_column("rid", ForeignKey("Roles.id"))
    role: Mapped[Optional["Role"]] = relationship(
        primaryjoin="ClientUser.role_id==Role.role_id"
    )

    def __init__(self, client=None, user=None, role=None):
        self.user = user
        self.client = client
        self.role = role

    @validates("client")
    def _validate_client(self, key: str, client: "Client") -> "Client":
        """Validate the given client value.

        Args:
            key (str): The name of the validated column.
            client (Client): The client instance to be validated.

        Raises:
            TypeError: If the given client value is not a :class:`.Client` instance.

        Returns:
            Client: The validated client instance.
        """
        if client is not None:
            if not isinstance(client, Client):
                raise TypeError(
                    f"{self.__class__.__name__}.client should be instance of "
                    "stalker.models.client.Client, "
                    f"not {client.__class__.__name__}: '{client}'"
                )
        return client

    @validates("user")
    def _validate_user(self, key: str, user: "User") -> "User":
        """Validate the given user value.

        Args:
            key (str): The name of the validated column.
            user (User): The user instance to validate.

        Raises:
            TypeError: If the given user value is not a
                :class:`stalker.models.auth.User` instance.

        Returns:
            User: The validated user value.
        """
        if user is not None:
            from stalker.models.auth import User

            if not isinstance(user, User):
                raise TypeError(
                    f"{self.__class__.__name__}.user should be an instance of "
                    "stalker.models.auth.User, "
                    f"not {user.__class__.__name__}: '{user}'"
                )
        return user

    @validates("role")
    def _validate_role(self, key: str, role: "Role") -> "Role":
        """Validate the given role instance.

        Args:
            key (str): The name of the validated column.
            role (Role): The role value to be validated.

        Raises:
            TypeError: If the given role value is not a
                :class:`stalker.models.auth.Role` instance.

        Returns:
            Role: The validated :class:`stalker.models.auth.Role` instance.
        """
        if role is not None:
            from stalker.models.auth import Role

            if not isinstance(role, Role):
                raise TypeError(
                    f"{self.__class__.__name__}.role should be a "
                    "stalker.models.auth.Role instance, "
                    f"not {role.__class__.__name__}: '{role}'"
                )
        return role
