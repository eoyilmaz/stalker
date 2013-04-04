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

from pyramid.httpexceptions import HTTPServerError
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError
import transaction

from stalker.db import DBSession
from stalker import User, Status, StatusList, EntityType

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='create_status',
    renderer='templates/status/dialog_create_status.jinja2',
    permission='Create_Status'
)
@view_config(
    route_name='update_status',
    renderer='templates/status/update_status.jinja2',
    permission='Update_Status'
)
def create_update_status(request):
    """called when adding or updateing a Status
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'create':
            logger.debug('adding a new Status')
            # create and add a new Status
            
            if 'name' in request.params and \
                'code' in request.params and \
                'bg_color' in request.params and \
                'fg_color' in request.params:
                
                logger.debug('we got all the parameters')
                
                try:
                    # get colors
                    bg_color = int(request.params['bg_color'][1:], 16)
                    fg_color = int(request.params['fg_color'][1:], 16)
                    new_status = Status(
                        name=request.params['name'],
                        code=request.params['code'],
                        fg_color=fg_color,
                        bg_color=bg_color,
                        created_by=user,
                    )
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_status)
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                    else:
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding Status')
            else:
                logger.debug('there are missing parameters')
                logger.debug(request.params)
            
            # TODO: place a return statement here
        elif request.params['submitted'] == 'update':
            logger.debug('updateing a Status')
            # just update the given Status
            st_id = request.matchdict['status_id']
            status = Status.query.filter_by(id=st_id).first()
            
            with transaction.manager:
                status.name = request.params['name']
                status.code = request.params['code']
                status.updated_by = user
                DBSession.add(status)
            
            logger.debug('finished updateing Status')
            
            # TODO: place a return statement here
    
    return {}


@view_config(
    route_name='create_status_list',
    renderer='templates/status/dialog_create_status_list.jinja2',
    permission='Create_StatusList'
)
@view_config(
    route_name='create_status_list_for',
    renderer='templates/status/dialog_create_status_list.jinja2',
    permission='Create_StatusList'
)
def create_status_list(request):
    """called when adding or updateing a StatusList
    """
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'create':
            logger.debug('adding a new StatusList')
            # create and add a new StatusList
            
            if 'name' in request.params and \
                'target_entity_type' in request.params and \
                'statuses' in request.params:
                
                logger.debug('we got all the parameters')
                
                # get statuses
                st_ids = [
                    int(st_id)
                    for st_id in request.POST.getall('statuses')
                ]
                
                statuses = Status.query.filter(Status.id.in_(st_ids)).all()
                
                try:
                    new_status_list = StatusList(
                        name=request.params['name'],
                        target_entity_type=\
                            request.params['target_entity_type'],
                        statuses=statuses,
                        created_by=user,
                    )
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    # TODO: This is just a test for HTTPExceptions, do it properly later!
                    DBSession.add(new_status_list)  
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                        http_error = HTTPServerError()
                        http_error.explanation = e.message
                        return(http_error)
                    else:
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding StatusList')
            else:
                logger.debug('there are missing parameters')
    
    target_entity_type = request.matchdict.get('target_entity_type')
    
    return {
        'target_entity_type': target_entity_type,
        'entity_types': EntityType.query.filter_by(statusable=True).all(),
        'statuses': Status.query.all()
    }


@view_config(
    route_name='update_status_list',
    renderer='templates/status/dialog_update_status_list.jinja2',
    permission='Update_StatusList'
)
def update_status_list(request):
    """called when updating a StatusList
    """
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    status_list_type = request.matchdict['target_entity_type']
    status_list = StatusList.query.filter_by(target_entity_type=status_list_type).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'update':
            logger.debug('updating a StatusList')
            # just update the given StatusList
            
            # get statuses
            logger.debug("request.params['statuses']: %s" % 
                                                request.params['statuses'])
            st_ids = [
                int(st_id)
                for st_id in request.POST.getall('statuses')
            ]
            
            statuses = Status.query.filter(Status.id.in_(st_ids)).all()
            
            logger.debug("statuses: %s" % statuses)
            
            status_list.name = request.params['name']
            status_list.statuses = statuses
            status_list.updated_by = user
            
            DBSession.add(status_list)
    
    return {
        'status_list': status_list
    }


@view_config(
    route_name='get_statuses',
    renderer='json',
    permission='Read_Status'
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
    renderer='json',
    permission='Read_Status'
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
    renderer='json',
    permission='Read_Status'
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
    renderer='json',
    permission='Read_StatusList'
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
    renderer='json',
    permission='Read_StatusList'
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
