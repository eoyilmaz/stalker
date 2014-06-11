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

import uuid

from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.orm import synonym, relationship
from sqlalchemy.orm.mapper import validates
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.schema import ForeignKey, Table
from sqlalchemy.types import Enum

from stalker.db.declarative import Base
from stalker.models.entity import Entity, SimpleEntity
from stalker.models.mixins import StatusMixin

from stalker import defaults

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

# RESOLUTIONS
FIXED = 'fixed'
INVALID = 'invalid'
WONTFIX = 'wontfix'
DUPLICATE = 'duplicate'
WORKSFORME = 'worksforme'
CANTFIX = 'cantfix'


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

    :param project: The Project that this Ticket is assigned to. A Ticket in
        Stalker must be assigned to a Project. ``project`` argument can not be
        skipped or can not be None.

    :type project: :class:`.Project`

    :param str summary: A string which contains the title or a short
        description of this Ticket.

    :param enum priority: The priority of the Ticket which is an enum value.
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

    :param reported_by: An instance of :class:`.User` who created this Ticket.
      It is basically a synonym for the :attr:`.SimpleEntity.created_by`
      attribute.

    Changing the :class:`.Ticket`\ .\ :attr`.Ticket.status` will create a new
    :class:`.TicketLog` instance showing the previous operation.

    Even though Tickets needs statuses they don't need to be supplied a
    :class:`.StatusList` nor :class:`.Status` for the Tickets. It will be
    automatically filled accordingly. For newly created Tickets the status of
    the ticket is ``NEW`` and can be changed to other statuses as follows:

        Status -> Action -> New Status

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
    :attr:`.Ticket.ticket_number`\ . So if defaults are used the first ticket
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
    #__table_args__ = (
    #    UniqueConstraint("project_id", 'number'), {}
    #)
    __mapper_args__ = {"polymorphic_identity": "Ticket"}

    ticket_id = Column(
        "id", Integer, ForeignKey("Entities.id"), primary_key=True
    )

    project_id = Column('project_id', Integer, ForeignKey('Projects.id'),
                        nullable=False)

    _project = relationship(
        'Project',
        primaryjoin='Tickets.c.project_id==Projects.c.id',
        back_populates='tickets'
    )

    _number = Column(
        'number',
        Integer,
        autoincrement=True,
        default=1,
        nullable=False,
        unique=True,
    )

    related_tickets = relationship(
        'Ticket',
        secondary='Ticket_Related_Tickets',
        primaryjoin='Tickets.c.id==Ticket_Related_Tickets.c.ticket_id',
        secondaryjoin='Ticket_Related_Tickets.c.related_ticket_id=='
                      'Tickets.c.id',
        doc="""A list of other Ticket instances which are related
        to this one. Can be used to related Tickets to point to a common
        problem. The Ticket itself can not be assigned to this list
        """
    )

    summary = Column(Text)

    logs = relationship(
        'TicketLog',
        primaryjoin='Tickets.c.id==TicketLogs.c.ticket_id',
        back_populates='ticket',
        cascade='all, delete-orphan'
    )

    links = relationship(
        'SimpleEntity',
        secondary='Ticket_SimpleEntities'
    )

    comments = synonym(
        'notes',
        doc="""A list of :class:`.Note` instances showing the comments made for
        this Ticket instance. It is a synonym for the :attr:`.Ticket.notes`
        attribute.
        """
    )

    reported_by = synonym('created_by', doc="Shows who created this Ticket")

    owner_id = Column('owner_id', Integer, ForeignKey('Users.id'))
    owner = relationship(
        'User',
        primaryjoin='Tickets.c.owner_id==Users.c.id'
    )

    resolution = Column(String(128))

    priority = Column(
        Enum('TRIVIAL', 'MINOR', 'MAJOR', 'CRITICAL', 'BLOCKER',
             name='PriorityType'),
        default='TRIVIAL',
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
        """
    )

    def __init__(self, project=None, links=None, priority='TRIVIAL',
                 summary=None, **kwargs):
        # just force auto name generation
        self._number = self._generate_ticket_number()
        kwargs['name'] = defaults.ticket_label + ' #%i' % self.number

        super(Ticket, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)

        self._project = project

        self.priority = priority
        if links is None:
            links = []
        self.links = links
        self.summary = summary

    def _number_getter(self):
        """returns the number attribute
        """
        return self._number

    number = synonym(
        '_number',
        descriptor=property(_number_getter),
        doc="""The automatically generated number for the tickets.
        """
    )

    def _project_getter(self):
        """returns the project attribute
        """
        return self._project

    project = synonym(
        '_project',
        descriptor=property(_project_getter)
    )

    @classmethod
    def _maximum_number(cls):
        """returns the maximum available number from the database

        :return: integer
        """
        try:
            # do your query
            max_ticket = Ticket.query \
                .order_by(Ticket.number.desc()) \
                .first()
        except UnboundExecutionError:
            max_ticket = None

        return max_ticket.number if max_ticket is not None else 0

    def _generate_ticket_number(self):
        """auto generates a number for the ticket

        :return: integer
        """
        # TODO: try to make it atomic
        return self._maximum_number() + 1

    @validates('related_tickets')
    def _validate_related_tickets(self, key, related_ticket):
        """validates the given related_ticket attribute
        """
        if not isinstance(related_ticket, Ticket):
            raise TypeError(
                '%s.related_ticket attribute should be a list of other '
                'stalker.models.ticket.Ticket instances not %s' %
                (self.__class__.__name__, related_ticket.__class__.__name__)
            )

        if related_ticket is self:
            raise ValueError(
                '%s.related_ticket attribute can not have itself in the list' %
                self.__class__.__name__
            )

        return related_ticket

    @validates('_project')
    def _validate_project(self, key, project):
        """validates the given project instance
        """
        from stalker import Project

        if project is None or not isinstance(project, Project):
            raise TypeError(
                '%s.project should be an instance of '
                'stalker.models.project.Project, not %s' %
                (self.__class__.__name__, project.__class__.__name__)
            )

        return project

    @validates('summary')
    def _validate_summary(self, key, summary):
        """validates the given summary value
        """
        if summary is None:
            summary = ''

        from stalker import __string_types__
        if not isinstance(summary, __string_types__):
            raise TypeError(
                '%s.summary should be an instance of str, not %s' %
                (self.__class__.__name__, summary.__class__.__name__)
            )
        return summary

    def __action__(self, action, created_by, action_arg=None):
        """updates the ticket status and creates a ticket log according to the
        Ticket.__available_actions__ dictionary

        :param str action: The name of the action
        :param stalker.models.auth.User created_by: The User creating this
            action
        """
        statuses = defaults.ticket_workflow[action].keys()
        status = self.status.name
        return_value = None
        if status in statuses:
            action_data = defaults.ticket_workflow[action][status]
            new_status_code = action_data['new_status']
            action_name = action_data['action']

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

    def resolve(self, created_by=None, resolution=''):
        """resolves the ticket
        """
        return self.__action__('resolve', created_by, resolution)

    def accept(self, created_by=None):
        """accepts the ticket
        """
        return self.__action__('accept', created_by, created_by)

    def reassign(self, created_by=None, assign_to=None):
        """reassigns the ticket
        """
        return self.__action__('reassign', created_by, assign_to)

    def reopen(self, created_by=None):
        """reopens the ticket
        """
        return self.__action__('reopen', created_by)

    # actions
    def set_owner(self, *args):
        """sets owner to the given owner
        """
        self.owner = args[0]

    def set_resolution(self, *args):
        """sets the timing_resolution
        """
        self.resolution = args[0]

    def del_resolution(self, *args):
        """deletes the timing_resolution
        """
        self.resolution = ''

    def __eq__(self, other):
        """the equality operator
        """
        return super(Ticket, self).__eq__(other) and \
            isinstance(other, Ticket) and \
            other.name == self.name and \
            other.number == self.number and \
            other.status == self.status and \
            other.logs == self.logs and \
            other.priority == self.priority

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Ticket, self).__hash__()


class TicketLog(SimpleEntity):
    """Holds :class:`.Ticket`\ .\ :attr:`.Ticket.status` change operations.

    :param ticket: An instance of :class:`.Ticket` which the subject to the
      operation.

    :type ticket: :class:`.Ticket`

    :param from_status: Holds a reference to a :class:`.Status` instance which
      is the previous status of the :class:`.Ticket`\ .

    :param to_status: Holds a reference to a :class:`.Status` instance which is
      the new status of the :class;`.Ticket`\ .

    :param operation: An Enumerator holding the type of the operation. Possible
      values are: RESOLVE or REOPEN

      Operations follow the `Track Workflow`_\ ,

      .. image:: http://trac.edgewall.org/chrome/common/guide/original-workflow.png
          :width: 787 px
          :height: 509 px
          :align: left

    .. _Track Workflow: http://trac.edgewall.org/wiki/TracWorkflow
    """

    # TODO: there are no tests for the TicketLog class

    __tablename__ = 'TicketLogs'
    __mapper_args__ = {'polymorphic_identity': 'TicketLog'}

    ticket_log_id = Column('id', ForeignKey('SimpleEntities.id'),
                           primary_key=True)

    from_status_id = Column(Integer, ForeignKey('Statuses.id'))
    to_status_id = Column(Integer, ForeignKey('Statuses.id'))

    from_status = relationship(
        'Status',
        primaryjoin='TicketLogs.c.from_status_id==Statuses.c.id'
    )

    to_status = relationship(
        'Status',
        primaryjoin='TicketLogs.c.to_status_id==Statuses.c.id'
    )

    action = Column(
        Enum(*defaults.ticket_workflow.keys(), name='TicketActions')
    )

    ticket_id = Column(Integer, ForeignKey('Tickets.id'))
    ticket = relationship(
        'Ticket',
        primaryjoin='TicketLogs.c.ticket_id==Tickets.c.id',
        back_populates='logs'
    )

    def __init__(self,
                 ticket=None,
                 from_status=None,
                 to_status=None,
                 action=None, **kwargs):
        kwargs['name'] = 'TicketLog_' + uuid.uuid4().hex
        super(TicketLog, self).__init__(**kwargs)
        self.ticket = ticket
        self.from_status = from_status
        self.to_status = to_status
        self.action = action


# A secondary Table for Ticket to Ticket relations
Ticket_Related_Tickets = Table(
    'Ticket_Related_Tickets', Base.metadata,
    Column('ticket_id', Integer, ForeignKey('Tickets.id'), primary_key=True),
    Column('related_ticket_id', Integer, ForeignKey('Tickets.id'),
           primary_key=True),
    extend_existing=True
)

# Ticket SimpleEntity Relation, link anything to a ticket
Ticket_SimpleEntities = Table(
    'Ticket_SimpleEntities', Base.metadata,
    Column('ticket_id', Integer, ForeignKey('Tickets.id'), primary_key=True),
    Column('simple_entity_id', Integer, ForeignKey('SimpleEntities.id'),
           primary_key=True)
)
