# -*- coding: utf-8 -*-
"""Ticket related functions and classes are situated here."""
import uuid
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.exc import OperationalError, UnboundExecutionError
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym
from sqlalchemy.orm.mapper import validates
from sqlalchemy.schema import ForeignKey, Table
from sqlalchemy.types import Enum

from stalker.db.declarative import Base
from stalker.db.session import DBSession
from stalker.exceptions import CircularDependencyError
from stalker.log import get_logger
from stalker.models.auth import User
from stalker.models.entity import Entity, SimpleEntity
from stalker.models.mixins import StatusMixin
from stalker.models.note import Note
from stalker.models.project import Project
from stalker.models.status import Status

logger = get_logger(__name__)

# RESOLUTIONS
FIXED = "fixed"
INVALID = "invalid"
WONTFIX = "wontfix"
DUPLICATE = "duplicate"
WORKSFORME = "worksforme"
CANTFIX = "cantfix"


class Ticket(Entity, StatusMixin):
    """Tickets are the way of reporting errors or asking for changes.

    The Stalker Ticketing system is based on Trac Basic Workflow. For more
    information please visit `Trac Workflow`_

    _`Trac Workflow`:: http://trac.edgewall.org/wiki/TracWorkflow

    Stalker Ticket system is very flexible, to customize the workflow please
    update the :class:`.Config.ticket_workflow` dictionary.

    In the default setup, there are four actions available; ``accept``,
    ``resolve``, ``reopen``, ``reassign``, and five statuses available ``New``,
    ``Assigned``, ``Accepted``, ``Reopened``, ``Closed``.

    Args:
        project (Project): The Project that this Ticket is assigned to. A Ticket in
            Stalker must be assigned to a Project. ``project`` argument cannot be
            skipped or cannot be None.
        summary (str): A string which contains the title or a short
            description of this Ticket.
        priority (str): The priority of the Ticket which is an enum value.
            Possible values are:

            +--------------+-------------------------------------------------+
            | 0 / TRIVIAL  | defect with little or no impact / cosmetic      |
            |              | enhancement                                     |
            +--------------+-------------------------------------------------+
            | 1 / MINOR    | defect with minor impact / small enhancement    |
            +--------------+-------------------------------------------------+
            | 2 / MAJOR    | defect with major impact / big enhancement      |
            +--------------+-------------------------------------------------+
            | 3 / CRITICAL | severe loss of data due to the defect or highly |
            |              | needed enhancement                              |
            +--------------+-------------------------------------------------+
            | 4 / BLOCKER  | basic functionality is not available until this |
            |              | is fixed                                        |
            +--------------+-------------------------------------------------+

        reported_by (User): A :class:`.User` instance who created this Ticket. It is
            basically a synonym for the :attr:`.SimpleEntity.created_by` attribute.

    Changing the :attr`.Ticket.status` will create a new :class:`.TicketLog` instance
    showing the previous operation.

    Even though Tickets needs statuses they don't need to be supplied a
    :class:`.StatusList` nor :class:`.Status` for the Tickets. It will be
    automatically filled accordingly. For newly created Tickets the status of
    the ticket is ``NEW`` and can be changed to other statuses as follows:

        Status   -> Action   -> New Status

        NEW      -> resolve  -> CLOSED
        NEW      -> accept   -> ACCEPTED
        NEW      -> reassign -> ASSIGNED

        ASSIGNED -> resolve  -> CLOSED
        ASSIGNED -> accept   -> ACCEPTED
        ASSIGNED -> reassign -> ASSIGNED

        ACCEPTED -> resolve  -> CLOSED
        ACCEPTED -> accept   -> ACCEPTED
        ACCEPTED -> reassign -> ASSIGNED

        REOPENED -> resolve  -> CLOSED
        REOPENED -> accept   -> ACCEPTED
        REOPENED -> reassign -> ASSIGNED

        CLOSED   -> reopen   -> REOPENED

        actions available:
        resolve
        reassign
        accept
        reopen

    The :attr:`.Ticket.name` is automatically generated by using the
    ``stalker.config.Config.ticket_label`` attribute and
    :attr:`.Ticket.ticket_number` . So if defaults are used the first ticket
    name will be "Ticket#1" and the second "Ticket#2" and so on. For every
    project the number will restart from 1.

    Use the :meth:`.Ticket.resolve`, :meth:`.Ticket.reassign`,
    :meth:`.Ticket.accept`, :meth:`.Ticket.reopen` methods to change the status
    of the current Ticket.

    Changing the status of the Ticket will create :class:`.TicketLog` entries
    reflecting the change made.
    """

    # logs attribute
    __auto_name__ = True
    __tablename__ = "Tickets"
    # __table_args__ = (
    #    UniqueConstraint("project_id", 'number'), {}
    # )
    __mapper_args__ = {"polymorphic_identity": "Ticket"}

    ticket_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    # TODO: use ProjectMixin
    project_id: Mapped[int] = mapped_column("project_id", ForeignKey("Projects.id"))

    _project: Mapped[Project] = relationship(
        primaryjoin="Tickets.c.project_id==Projects.c.id",
        back_populates="tickets",
    )

    _number: Mapped[int] = mapped_column(
        "number",
        autoincrement=True,
        default=1,
        nullable=False,
        unique=True,
    )

    related_tickets: Mapped[Optional[List["Ticket"]]] = relationship(
        secondary="Ticket_Related_Tickets",
        primaryjoin="Tickets.c.id==Ticket_Related_Tickets.c.ticket_id",
        secondaryjoin="Ticket_Related_Tickets.c.related_ticket_id==" "Tickets.c.id",
        doc="""A list of other Ticket instances which are related
        to this one. Can be used to related Tickets to point to a common
        problem. The Ticket itself cannot be assigned to this list
        """,
    )

    summary: Mapped[Optional[str]] = mapped_column(Text)

    logs: Mapped[Optional[List["TicketLog"]]] = relationship(
        primaryjoin="Tickets.c.id==TicketLogs.c.ticket_id",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )

    links: Mapped[Optional[List["SimpleEntity"]]] = relationship(
        secondary="Ticket_SimpleEntities"
    )

    comments: Mapped[Optional[List["Note"]]] = synonym(
        "notes",
        doc="""A list of :class:`.Note` instances showing the comments made for
        this Ticket instance. It is a synonym for the :attr:`.Ticket.notes`
        attribute.
        """,
    )

    reported_by: Mapped[Optional["User"]] = synonym(
        "created_by", doc="Shows who created this Ticket"
    )

    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Users.id"))
    owner: Mapped["User"] = relationship(primaryjoin="Tickets.c.owner_id==Users.c.id")

    resolution: Mapped[Optional[str]] = mapped_column(String(128))

    priority: Mapped[Optional[str]] = mapped_column(
        Enum("TRIVIAL", "MINOR", "MAJOR", "CRITICAL", "BLOCKER", name="PriorityType"),
        default="TRIVIAL",
        doc="""The priority of the Ticket which is an enum value.
        Possible values are:

          +--------------+-------------------------------------------------+
          | 0 / TRIVIAL  | defect with little or no impact / cosmetic      |
          |              | enhancement                                     |
          +--------------+-------------------------------------------------+
          | 1 / MINOR    | defect with minor impact / small enhancement    |
          +--------------+-------------------------------------------------+
          | 2 / MAJOR    | defect with major impact / big enhancement      |
          +--------------+-------------------------------------------------+
          | 3 / CRITICAL | severe loss of data due to the defect or highly |
          |              | needed enhancement                              |
          +--------------+-------------------------------------------------+
          | 4 / BLOCKER  | basic functionality is not available until this |
          |              | is fixed                                        |
          +--------------+-------------------------------------------------+
        """,
    )

    def __init__(
        self,
        project: Optional[Project] = None,
        links: Optional[List[SimpleEntity]] = None,
        priority: str = "TRIVIAL",
        summary: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        # just force auto name generation
        self._number = self._generate_ticket_number()
        from stalker import defaults

        kwargs["name"] = "{:s} #{:d}".format(defaults.ticket_label, self.number)

        super(Ticket, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)

        self._project = project

        self.priority = priority
        if links is None:
            links = []
        self.links = links
        self.summary = summary

    def _number_getter(self) -> int:
        """Return the number attribute value.

        Returns:
            int: The number attribute value.
        """
        return self._number

    number = synonym(
        "_number",
        descriptor=property(_number_getter),
        doc="""The automatically generated number for the tickets.
        """,
    )

    def _project_getter(self) -> Project:
        """Return the project attribute value.

        Returns:
            Project: The project attribute value.
        """
        return self._project

    project = synonym("_project", descriptor=property(_project_getter))

    @classmethod
    def _maximum_number(cls) -> int:
        """Return the maximum available number from the database.

        Returns:
            int: The maximum ticket number.
        """
        try:
            # do your query
            with DBSession.no_autoflush:
                max_ticket = Ticket.query.order_by(Ticket.number.desc()).first()
        except (UnboundExecutionError, OperationalError):
            max_ticket = None

        return max_ticket.number if max_ticket is not None else 0

    def _generate_ticket_number(self) -> int:
        """Auto generate a number for the ticket.

        Returns:
            int: The auto generated ticket number.
        """
        # TODO: try to make it atomic
        return self._maximum_number() + 1

    @validates("related_tickets")
    def _validate_related_tickets(self, key: str, related_ticket: "Ticket") -> "Ticket":
        """Validate the given related_ticket value.

        Args:
            key (str): The name of the validated column.
            related_ticket (Ticket): The related_ticket value to be validated.

        Raises:
            TypeError: If the related_ticket value is not a Ticket instance.
            CircularDependencyError: If the related_ticket value is the same with this
                Ticket.

        Returns:
            Ticket: The validated related_ticket value.
        """
        if not isinstance(related_ticket, Ticket):
            raise TypeError(
                "{}.related_ticket should only contain instances of "
                "stalker.models.ticket.Ticket, not {}: '{}'".format(
                    self.__class__.__name__,
                    related_ticket.__class__.__name__,
                    related_ticket,
                )
            )

        if related_ticket is self:
            raise CircularDependencyError(
                "{}.related_ticket attribute cannot have itself in the list".format(
                    self.__class__.__name__
                )
            )

        return related_ticket

    @validates("_project")
    def _validate_project(
        self, key: str, project: Union[None, Project]
    ) -> Union[None, Project]:
        """Validate the given project value.

        Args:
            key (str): The name of the validated column.
            project (Union[None, Project]): The project value to be validated.

        Raises:
            TypeError: If the given project is not a Project instance.

        Returns:
            Union[None, Project]: The validated project value.
        """
        if project is None or not isinstance(project, Project):
            raise TypeError(
                "{}.project should be an instance of "
                "stalker.models.project.Project, not {}: '{}'".format(
                    self.__class__.__name__, project.__class__.__name__, project
                )
            )

        return project

    @validates("summary")
    def _validate_summary(self, key: str, summary: Union[None, str]) -> str:
        """Validate the given summary value.

        Args:
            key (str): The name of the validated column.
            summary (Union[None, str]): The summary value to be validated.

        Raises:
            TypeError: If the given summary is not None and not a string.

        Returns:
            str: The validated summary value.
        """
        if summary is None:
            summary = ""

        if not isinstance(summary, str):
            raise TypeError(
                "{}.summary should be an instance of str, not {}: '{}'".format(
                    self.__class__.__name__, summary.__class__.__name__, summary
                )
            )
        return summary

    def __action__(
        self, action: str, created_by: User, action_arg: Any = None
    ) -> "TicketLog":
        """Update the ticket status and create a ticket log.

        The log is created according to the Ticket.__available_actions__ dictionary.

        Args:
            action (str): The name of the action.
            created_by (User): The User creating this action.
            action_arg (Any): The argument to pass to the action.

        Returns:
            TicketLog: The TicketLog instance created.
        """
        from stalker import defaults

        statuses = defaults.ticket_workflow[action].keys()
        status = self.status.name
        return_value = None
        if status in statuses:
            action_data = defaults.ticket_workflow[action][status]
            new_status_code = action_data["new_status"]
            action_name = action_data["action"]

            # there is an action defined for this status
            # get the to_status
            from_status = self.status
            to_status = self.status_list[new_status_code]
            self.status = to_status

            # call the action with action_arg
            func = getattr(self, action_name)
            func(action_arg)

            ticket_log = TicketLog(
                self, from_status, to_status, action, created_by=created_by
            )

            # create log entry
            self.logs.append(ticket_log)
            return_value = ticket_log
        return return_value

    def resolve(
        self, created_by: Union[None, User] = None, resolution: str = ""
    ) -> "TicketLog":
        """Resolve the ticket.

        Args:
            created_by (User): The User instance who is taking this action.
            resolution (str): The resolution.

        Returns:
            TicketLog: The newly created TicketLog instance.
        """
        return self.__action__("resolve", created_by, resolution)

    def accept(self, created_by: Union[None, User] = None) -> "TicketLog":
        """Accept the ticket.

        Args:
            created_by (User): The User instance who is taking this action.

        Returns:
            TicketLog: The newly created TicketLog instance.
        """
        return self.__action__("accept", created_by, created_by)

    def reassign(
        self, created_by: Union[None, User] = None, assign_to: Union[None, User] = None
    ) -> "TicketLog":
        """Reassign the ticket to another User.

        Args:
            created_by (User): The User that is doing the action.
            assign_to (User): The new owner of the ticket.

        Returns:
            TicketLog: The newly created TicketLog instance.
        """
        return self.__action__("reassign", created_by, assign_to)

    def reopen(self, created_by: Union[None, User] = None) -> "TicketLog":
        """Reopen the ticket.

        Args:
            created_by (User): The User who is doing the action.

        Returns:
            TicketLog: The newly created TicketLog instance.
        """
        return self.__action__("reopen", created_by)

    # actions
    def set_owner(self, *args) -> None:
        """Set the owner.

        Args:
            args (Any): Set the owner.
        """
        self.owner = args[0]

    def set_resolution(self, *args) -> None:
        """Set the timing_resolution.

        Args:
            args (Any): Any argument passed to this method.
        """
        self.resolution = args[0]

    def del_resolution(self, *args) -> None:
        """Delete the timing_resolution.

        Args:
            args (Any): Any arguments passed to this method.
        """
        self.resolution = ""

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a Ticket instance and has the same name,
                number, status, logs and priority.
        """
        return (
            super(Ticket, self).__eq__(other)
            and isinstance(other, Ticket)
            and other.name == self.name
            and other.number == self.number
            and other.status == self.status
            and other.logs == self.logs
            and other.priority == self.priority
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Ticket, self).__hash__()


class TicketLog(SimpleEntity):
    """Holds :attr:`.Ticket.status` change operations.

    Args:
        ticket (Ticket): A :class:`.Ticket` instance which is the subject of the
            operation.

        from_status (Status): Holds a reference to a :class:`.Status` instance which is
            the previous status of the :class:`.Ticket` .

        to_status (Status): Holds a reference to a :class:`.Status` instance which is
            the new status of the :class;`.Ticket` .

        action (str): An Enumerator holding the type of the operation should be one of
            ["resolve", "accept", "reassign", "reopen"].

      Operations follow the `Track Workflow`_ ,

      .. image:: http://trac.edgewall.org/chrome/common/guide/original-workflow.png
          :width: 787 px
          :height: 509 px
          :align: left

    .. _Track Workflow: http://trac.edgewall.org/wiki/TracWorkflow
    """

    from stalker import defaults  # need to limit it with a scope

    # TODO: there are no tests for the TicketLog class

    __tablename__ = "TicketLogs"
    __mapper_args__ = {"polymorphic_identity": "TicketLog"}

    ticket_log_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )

    from_status_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Statuses.id"))
    to_status_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Statuses.id"))

    from_status: Mapped[Status] = relationship(
        primaryjoin="TicketLogs.c.from_status_id==Statuses.c.id"
    )

    to_status: Mapped[Status] = relationship(
        primaryjoin="TicketLogs.c.to_status_id==Statuses.c.id"
    )

    action: Mapped[Optional[str]] = mapped_column(
        Enum(*defaults.ticket_workflow.keys(), name="TicketActions")
    )

    ticket_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Tickets.id"))
    ticket: Mapped[Optional[Ticket]] = relationship(
        primaryjoin="TicketLogs.c.ticket_id==Tickets.c.id",
        back_populates="logs",
    )

    def __init__(
        self,
        ticket: Optional[Ticket] = None,
        from_status: Optional[Status] = None,
        to_status: Optional[Status] = None,
        action: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        kwargs["name"] = "TicketLog_" + uuid.uuid4().hex
        super(TicketLog, self).__init__(**kwargs)
        self.ticket = ticket
        self.from_status = from_status
        self.to_status = to_status
        self.action = action


# A secondary Table for Ticket to Ticket relations
Ticket_Related_Tickets = Table(
    "Ticket_Related_Tickets",
    Base.metadata,
    Column("ticket_id", Integer, ForeignKey("Tickets.id"), primary_key=True),
    Column("related_ticket_id", Integer, ForeignKey("Tickets.id"), primary_key=True),
    extend_existing=True,
)

# Ticket SimpleEntity Relation, link anything to a ticket
Ticket_SimpleEntities = Table(
    "Ticket_SimpleEntities",
    Base.metadata,
    Column("ticket_id", Integer, ForeignKey("Tickets.id"), primary_key=True),
    Column(
        "simple_entity_id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    ),
)
