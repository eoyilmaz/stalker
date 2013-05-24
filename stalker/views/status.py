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
import datetime

from pyramid.httpexceptions import HTTPServerError, HTTPOk
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError
import transaction

from stalker.db import DBSession
from stalker import User, Status, StatusList, EntityType

import logging
from stalker import log
from stalker.views import PermissionChecker, get_logged_in_user, get_multi_integer, get_color_as_int

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


# *******************
#
# Status Dialogs
#
# *******************

@view_config(
    route_name='dialog_create_status',
    renderer='templates/status/dialog_create_status.jinja2'
)
def dialog_create_status(request):
    """fills the create status dialog
    """
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='dialog_update_status',
    renderer='templates/status/dialog_create_status.jinja2'
)
def dialog_update_status(request):
    """fills update status dialog
    """
    status_id = request.matchdict['status_id']
    status = Status.query.filter_by(id=status_id).first()
    
    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'status': status
    }


@view_config(
    route_name='create_status',
)
def create_status(request):
    """creates a new Status
    """
    logged_in_user = get_logged_in_user(request)
    
    # get parameters
    name = request.params.get('name')
    code = request.params.get('code')
    bg_color = get_color_as_int(request, 'bg_color')
    fg_color = get_color_as_int(request, 'fg_color')
    
    if name and code:
        new_status = Status(
            name=name,
            code=code,
            fg_color=fg_color,
            bg_color=bg_color,
            created_by=logged_in_user,
        )
        DBSession.add(new_status)
    
    return HTTPOk()


@view_config(
    route_name='update_status'
)
def update_status(request):
    """updates a status
    """
    logged_in_user = get_logged_in_user(request)
    
    # get parameters
    name = request.params.get('name')
    code = request.params.get('code')
    bg_color = get_color_as_int(request, 'bg_color')
    fg_color = get_color_as_int(request, 'fg_color')
    
    # just update the given Status
    st_id = request.matchdict['status_id']
    status = Status.query.filter_by(id=st_id).first()
    
    if status and name and code:
        status.name = name
        status.code = code
        status.fg_color = fg_color
        status.bg_color = bg_color
        status.updated_by = logged_in_user
        status.date_updated = datetime.datetime.now()
        DBSession.add(status)
    
    return HTTPOk()


# *******************
#
# Status List Dialogs
#
# *******************
 
@view_config(
    route_name='dialog_create_status_list',
    renderer='templates/status/dialog_create_status_list.jinja2'
)
@view_config(
    route_name='dialog_create_status_list_for',
    renderer='templates/status/dialog_create_status_list.jinja2'
)
def dialog_create_status_list(request):
    """fills the create status_list dialog
    """
    target_entity_type = request.matchdict.get('target_entity_type')
    
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request),
        'target_entity_type': target_entity_type,
        'entity_types': EntityType.query.filter_by(statusable=True).all(),
        'statuses': Status.query.all()
    }


@view_config(
    route_name='dialog_update_status_list',
    renderer='templates/status/dialog_create_status_list.jinja2'
)
def dialog_update_status_list(request):
    
    target_entity_type = request.matchdict.get('target_entity_type')
    status_list = StatusList.query\
        .filter_by(target_entity_type=target_entity_type).first()
    
    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'entity_types': EntityType.query.filter_by(statusable=True).all(),
        'statuses': Status.query.all(),
        'status_list': status_list,
    }


# *******************
#
# Status List Actions
#
# *******************

@view_config(
    route_name='create_status_list'
)
def create_status_list(request):
    """creates a StatusList
    """
    logged_in_user = get_logged_in_user(request)
    
    # get parameters
    name = request.params.get('name')
    target_entity_type = request.params.get('target_entity_type')
    
    # get statuses
    st_ids = get_multi_integer(request, 'status_ids')
    statuses = Status.query.filter(Status.id.in_(st_ids)).all()
    
    if name and target_entity_type:
        new_status_list = StatusList(
            name=name,
            target_entity_type=target_entity_type,
            statuses=statuses,
            created_by=logged_in_user
        )
        DBSession.add(new_status_list)  
    
    return HTTPOk()

@view_config(
    route_name='update_status_list'
)
def update_status_list(request):
    """called when updating a StatusList
    """
    logged_in_user = get_logged_in_user(request)
    
    name = request.params.get('name')
    
    status_list_id = request.params.get('status_list_id')
    status_list = StatusList.query.filter_by(id=status_list_id).first()
    
    st_ids = get_multi_integer(request, 'status_ids')
    statuses = Status.query.filter(Status.id.in_(st_ids)).all()
    
    logger.debug('st_ids   : %s' % st_ids)
    logger.debug('statuses : %s' % statuses)
    
    if status_list and name:
        status_list.name = name
        status_list.statuses = statuses
        
        logger.debug('status_list.statuses : %s' % status_list.statuses)
        
        status_list.updated_by = logged_in_user
        status_list.date_updated = datetime.datetime.now()
        
        DBSession.add(status_list)
    
    return HTTPOk()


@view_config(
    route_name='get_statuses',
    renderer='json'
)
def get_statuses(request):
    """returns all the Statuses in the database
    """
    return [
        {
            'id': status.id,
            'name': status.name,
            'code': status.code
        }
        for status in Status.query.all()
    ]


@view_config(
    route_name='get_statuses_of',
    renderer='json'
)
def get_statuses_of(request):
    """returns the Statuses of given StatusList
    """
    status_list_id = request.matchdict['status_list_id']
    status_list = StatusList.query.filter_by(id=status_list_id).first()
    return [
        {
            'id': status.id,
            'name': status.name + " (" + status.code+ ")"
        }
        for status in status_list.statuses
    ]

@view_config(
    route_name='get_statuses_for',
    renderer='json'
)
def get_statuses_for(request):
    """returns the Statuses of given StatusList
    """
    status_list_type = request.matchdict['target_entity_type']
    status_list = StatusList.query.filter_by(target_entity_type=status_list_type).first()

    return [
        {
            'id': status.id,
            'name': status.name + " (" + status.code+ ")"
        }
        for status in status_list.statuses
    ] if status_list else []

@view_config(
    route_name='get_status_lists',
    renderer='json'
)
def get_status_lists(request):
    """returns all the StatusList instances in the databases
    """
    return [
        {
            'id': status_list.id,
            'name': status_list.name,
        }
        for status_list in StatusList.query.all()
    ]


@view_config(
    route_name='get_status_lists_for',
    renderer='json'
)
def get_status_lists_for(request):
    """returns all the StatusList for a specific target_entity_type
    """
    return [
        {
            'id': status_list.id,
            'name': status_list.name,
        }
        for status_list in StatusList.query
            .filter_by(target_entity_type=request.matchdict['target_entity_type'])
            .all()
    ]
