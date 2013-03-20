# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import uuid
from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.orm import synonym, relationship
from sqlalchemy.orm.mapper import validates
from sqlalchemy import Column, Integer
from sqlalchemy.schema import ForeignKey, Table
from sqlalchemy.types import Enum
from stalker.conf import defaults
from stalker.db.declarative import Base
from stalker.models.entity import Entity, SimpleEntity
from stalker.models.mixins import StatusMixin

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

class Ticket(Entity, StatusMixin):
    """Tickets are the way of reporting errors or asking for changes in Stalker.
    
    Although the ticketing system is based on Trac Original Workflow, in
    Stalker Tickets are always assigned to the owner of the related
    :class:`~stalker.models.version.Version` files. So there is no need to have
    a status of ``Assigned`` or an action of ``accept`` nor ``reassign``. There
    are only two actions (through Ticket methods); ``resolve`` or ``reopen``,
    and three statuses available ``New``, ``Reopened``, ``Closed``.
    
    :param str summary: A string which contains the title or a short
        description of this Ticket.
    
    :param ticket_for: An instance of :class:`~stalker.models.version.Version`
        instance that this Ticket is created for.
    
    :type ticket_for: :class:`~stalker.models.version.Version`
    
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
    
    :param reported_by: An instance of :class:`~stalker.models.user.User` who
        created this Ticket. It is basically a synonym for the
        :attr:`~stalker.models.entity.SimpleEntity.created_by` attribute.
    
    Changing the :class:`~stalker.models.ticket.Ticket`\ .\ 
    :attr`~stalker.models.ticket.Ticket.status` will create a new
    :class:`~stalker.models.Ticket.TicketLog` instance showing the previous
    operation.
    
     Even though Tickets needs statuses they don't need to be supplied a
    :class:`~stalker.models.status.StatusList` nor
    :class:`~stalker.models.status.Status` for the Tickets. It will be
    automatically filled accordingly. For newly created Tickets the status of
    the ticket is ``NEW`` and can be changed to other statuses as follows:
        
        Status -> Action -> New Status
        
        NEW -> resolve -> CLOSED
        REOPENED -> resolve -> CLOSED
        CLOSED -> reopen -> REOPENED
        
        actions available
        0-NEW      : resolve:CLOSED
        1-REOPENED : resolve:CLOSED
        2-CLOSED   : reopen:REOPENED
    
    The :attr:`~stalker.models.ticket.Ticket.name` is automatically generated
    by using the ``conf.defaults.DEFAULT_TICKET_LABEL`` attribute and
    :attr:`~stalker.models.ticket.Ticket.ticket_number`\ . So if defaults are
    used the first ticket name will be "Ticket#1" and the second "Ticket#2" and
    so on.
    
    Use the :meth:`~stalker.models.ticket.Ticket.resolve`,
    :meth:`~stalker.models.ticket.Ticket.reopen` methods to change the status
    of the current Ticket.
    
    Changing the status of the Ticket will create
    :class:`~stalker.models.ticket.TicketLog` entries reflecting the change
    made.
    """
    
    # logs attribute
    __auto_name__ = True
    __tablename__ = "Tickets"
    __mapper_args__ = {"polymorphic_identity": "Ticket"}
    
    ticket_id = Column(
        "id", Integer, ForeignKey("Entities.id"), primary_key=True
    )
    
    ticket_for_id = Column(Integer, ForeignKey('Versions.id'))
    ticket_for = relationship(
        "Version",
        primaryjoin='Ticket.ticket_for_id==Version.version_id',
        doc="""The :class:`~stalker.models.version.Version` instance that this Ticket is related to
        """
    )
    
    _number = Column(
        Integer,
        unique=True,
        autoincrement=True,
        default=1,
        nullable=False
    )
    
    related_tickets = relationship(
        'Ticket',
        secondary='Ticket_Related_Tickets',
        primaryjoin='Tickets.c.id==Ticket_Related_Tickets.c.ticket_id',
        secondaryjoin='Ticket_Related_Tickets.c.related_ticket_id==Tickets.c.id',
        doc="""A list of other Ticket instances which are related
        to this one. Can be used to related Tickets to point to a common
        problem. The Ticket itself can not be assigned to this list
        """
    )
    
    comments = synonym('notes',
        doc="""A list of :class:`~stalker.models.note.Note` instances showing
        the comments made for this Ticket instance. It is a synonym for the
        :attr:`~stalker.models.ticket.Ticket.notes` attribute.
        """
    )
    
    reported_by = synonym('created_by', doc="Shows who created this Ticket")
    
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
    
    # define the available actions per Status
    __avialable_actions__ = {
        # Current     # Action    # New
        # Status                  # Status
        "NEW"      : {"resolve" : "CLOSED"},
        "REOPENED" : {"resolve" : "CLOSED"},
        "CLOSED"   : {"reopen"  : "REOPENED"}
    }
    
    def __init__(self, ticket_for=None, priority='TRIVIAL', **kwargs):
        # generate a name
        #kwargs['name'] = "Ticket_" + uuid.uuid4().urn.split(':')[2]
        #logger.debug('name of the newly created Ticket is: %s' % 
        #             kwargs['name'])
        
        # just force auto name generation
        self._number = self._generate_ticket_number()
        kwargs['name'] = defaults.TICKET_LABEL + ' #%i' % self.number
        
        super(Ticket, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)
        
        self.ticket_for = ticket_for
        #self._number = self._generate_ticket_number()
        self.priority = priority
      
    def _number_getter(self):
        """returns the number attribute
        """
        return self._number
    
    number = synonym(
        "_number",
        descriptor=property(_number_getter),
        doc="""The automatically generated number for the tickets.
        """
    )
    
    def _maximum_number(self):
        """returns the maximum available number from the database
        
        :return: integer
        """
        try:
            max_ticket = Ticket.query\
                .order_by(Ticket.number.desc())\
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
    
    @validates('ticket_for')
    def _validate_ticket_for(self, key, ticket_for):
        """validates the given ticket_for value
        """
        if ticket_for is None:
            raise TypeError('%s.ticket_for can not be None, please set it '
                            'to a stalker.models.version.Version instance' % 
                            self.__class__.__name__)
        from stalker.models.version import Version
        if not isinstance(ticket_for, Version):
            raise TypeError('%s.ticket_for attribute should be an '
                'instance of stalker.models.version.Version instance not %s' %
                (self.__class__.__name__, ticket_for.__class__.__name__))
        return ticket_for
    
    @validates('related_tickets')
    def _validate_related_tickets(self, key, related_ticket):
        """validates the given related_ticket attribute
        """
        if not isinstance(related_ticket, Ticket):
            raise TypeError('%s.related_ticket attribute should be a list '
                'of other stalker.models.ticket.Ticket instances not %s' %
                (self.__class__.__name__, related_ticket.__class__.__name__))
        
        if related_ticket is self:
            raise ValueError('%s.related_ticket attribute can not have '
            'itself in the list' % self.__class__.__name__)
        
        return related_ticket
    
    def resolve(self, created_by=None):
        """changes the status of the Ticket if it is New or Reopened to Closed
        """
        if self.status.code == 'NEW' or self.status.code == 'REOPENED':
            from_status = self.status
            self.status = 2
            to_status = self.status
            
            # create a log entry
            self.logs.append(
                TicketLog(self, from_status, to_status, 'RESOLVE',
                          created_by=created_by)
            )
    
    def reopen(self, created_by=None):
        """changes the status of the Ticket if it is Closed to Reopened
        """
        if self.status.code == 'CLOSED':
            from_status = self.status
            self.status = 1
            to_status = self.status
            
            # create a log entry
            self.logs.append(
                TicketLog(self, from_status, to_status, 'REOPEN',
                          created_by=created_by)
            )
    
    def __eq__(self, other):
        """the equality operator
        """
        return super(Ticket, self).__eq__(other) and \
               isinstance(other, Ticket) and \
               other.name == self.name and \
               other.number == self.number and \
               other.status == self.status and \
               other.logs == self.logs and \
               other.priority == self.priority and \
               other.ticket_for == self.ticket_for

class TicketLog(SimpleEntity):
    """A class to hold :class:`~stalker.models.ticket.Ticket`\ .\ :attr:`~stalker.models.ticket.Ticket.status` change operations.
    
    :param ticket: An instance of :class:`~stalker.models.ticket.Ticket` which
        the subject to the operation.
    
    :type ticket: :class:`~stalker.models.ticket.Ticket`
    
    :param from_status: Holds a reference to a
        :class:`~stalker.models.status.Status` instance which is the previous
        status of the :class:`~stalker.models.ticket.Ticket`\ .
    
    :param to_status: Holds a reference to a
        :class:`~stalker.models.status.Status` instance which is the new status
        of the :class;`~stalker.models.ticket.Ticket`\ .
    
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
    
    action = Column(Enum('RESOLVE', 'REOPEN', name='TicketActions'))
    
    ticket_id = Column(Integer, ForeignKey('Tickets.id'))
    ticket = relationship(
        'Ticket',
        primaryjoin='TicketLogs.c.ticket_id==Tickets.c.id',
        backref='logs'
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
    Column('related_ticket_id', Integer, ForeignKey('Tickets.id'), primary_key=True),
    extend_existing=True
)
