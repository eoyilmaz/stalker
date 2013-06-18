# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
from pyramid.httpexceptions import HTTPOk, HTTPServerError
from pyramid.security import authenticated_userid, has_permission
from pyramid.view import view_config
from stalker import Task, User, Studio, Ticket, Entity, Project, Status

from stalker import defaults

import logging
from stalker import log
from stalker.db import DBSession
from stalker.exceptions import OverBookedError
from stalker.views import get_datetime, get_logged_in_user, PermissionChecker, seconds_since_epoch, microseconds_since_epoch

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)

@view_config(
    route_name='dialog_create_ticket',
    renderer='templates/ticket/dialog_create_ticket.jinja2',
)
def create_ticket_dialog(request):
    """creates a create_ticket_dialog by using the given task
    """
    logger.debug('inside create_ticket_dialog')

    # get logged in user
    logged_in_user = get_logged_in_user(request)


    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter(Entity.entity_id==entity_id).first()

    logger.debug('entity_type : %s' % entity.entity_type)

    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request),
        'logged_in_user': logged_in_user,
        'entity': entity,
        'microseconds_since_epoch': microseconds_since_epoch
    }

@view_config(
    route_name='dialog_update_ticket',
    renderer='templates/ticket/dialog_create_ticket.jinja2',
)
def update_ticket_dialog(request):
    """updates a create_ticket_dialog by using the given task
    """
    logger.debug('inside updates_ticket_dialog')

    # get logged in user
    logged_in_user = get_logged_in_user(request)

    ticket_id = request.matchdict['ticket_id']
    ticket = Ticket.query.filter_by(id=ticket_id).first()


    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'logged_in_user': logged_in_user,
        'ticket': ticket,
        'entity': ticket.project,
        'microseconds_since_epoch': microseconds_since_epoch
    }


@view_config(
    route_name='create_ticket'
)
def create_ticket(request):
    """runs when creating a ticket
    """
    #**************************************************************************
    # collect data

    description = request.params.get('description')

    project_id = request.params.get('project_id', None)
    project = Project.query.filter(Project.id==project_id).first()

    owner_id = request.params.get('owner_id', None)
    owner = User.query.filter(User.id==owner_id).first()

    status_id = request.params.get('status_id')
    status = Status.query.filter_by(id=status_id).first()


    logger.debug('*******************************')

    logger.debug('create_ticket is running')

    logger.debug('project_id : %s' % project_id)
    logger.debug('owner_id : %s' % owner_id)


    logger.debug('owner: %s' % owner)

    if description and project and  owner :
        # we are ready to create the time log
        # Ticket should handle the extension of the effort
        ticket = Ticket(
            status = status,
            description=description,
            owner=owner,
            project=project,
            created_by=get_logged_in_user(request)
        )
        DBSession.add(ticket)

    return HTTPOk()


@view_config(
    route_name='update_ticket'
)
def update_ticket(request):
    """runs when updating a ticket
    """

    ticket_id = request.params.get('ticket_id')
    ticket = Ticket.query.filter_by(id=ticket_id).first()

    #**************************************************************************
    # collect data
    description = request.params.get('description')

    project_id = request.params.get('project_id', None)
    project = Project.query.filter(Project.id==project_id).first()

    owner_id = request.params.get('owner_id', None)
    owner = User.query.filter(User.id==owner_id).first()

    status_id = request.params.get('status_id')
    status = Status.query.filter_by(id=status_id).first()

    logger.debug('*******************************')

    logger.debug('update_ticket is running')

    logger.debug('project_id : %s' % project_id)
    logger.debug('owner_id : %s' % owner_id)


    logger.debug('ticket: %s' % ticket)
    logger.debug('owner: %s' % owner)
    logger.debug('project: %s' % project)


    if  ticket and description and project and  owner :
        # we are ready to create the time log
        # Ticket should handle the extension of the effort
        ticket.status=status
        ticket.description=description
        ticket.owner=owner
        ticket.updated_by=get_logged_in_user(request)

        DBSession.add(ticket)

    return HTTPOk()

@view_config(
    route_name='view_ticket',
    renderer='templates/ticket/page_view_ticket.jinja2'
)
def view_ticket(request):
    """runs when viewing an ticket
    """
    logged_in_user = get_logged_in_user(request)

    ticket_id = request.matchdict['ticket_id']
    ticket = Ticket.query.filter_by(id=ticket_id).first()

    return {
        'user': logged_in_user,
        'has_permission': PermissionChecker(request),
        'ticket': ticket
    }


@view_config(
    route_name='summarize_ticket',
    renderer='templates/ticket/content_summarize_ticket.jinja2'
)
def summarize_ticket(request):
    """runs when viewing an ticket
    """
    logged_in_user = get_logged_in_user(request)

    ticket_id = request.matchdict['ticket_id']
    ticket = Ticket.query.filter_by(id=ticket_id).first()

    return {
        'user': logged_in_user,
        'has_permission': PermissionChecker(request),
        'ticket': ticket
    }


@view_config(
    route_name='list_tickets',
    renderer='templates/ticket/content_list_tickets.jinja2'
)
def list_tickets(request):
    """lists the time logs of the given task
    """

    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    logger.debug('*******************************')
    logger.debug('list_tickets is running')

    logger.debug('entity_id : %s' % entity_id)

    return {
        'entity': entity,
        'has_permission': PermissionChecker(request)
    }

@view_config(
    route_name='get_tickets',
    renderer='json'
)
def get_tickets(request):
    """returns all the Shots of the given Project
    """

    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    logger.debug('*******************************')
    logger.debug('get_tickets is running')

    logger.debug('entity_id : %s' % entity_id)

    logger.debug('entity : %s' % entity)
    logger.debug('entity_tickets : %s' %  len(entity.tickets))

    ticket_data = []

    # if entity.tickets:
    for ticket in entity.tickets:

        assert isinstance(ticket, Ticket)
        ticket_data.append({
            'id': ticket.id,
            'name': ticket.name,
            'project_id': ticket.project_id,
            'project_name': ticket.project.name,
            'owner_id': ticket.owner_id,
            'owner_name': 'owner',
            'created_by_id': ticket.created_by_id,
            'created_by_name': ticket.created_by.name
        })

    return ticket_data

