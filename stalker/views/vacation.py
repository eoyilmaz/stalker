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
from stalker import Task, User, Studio, Vacation, Entity, Type

from stalker import defaults

import logging
from stalker import log
from stalker.db import DBSession
from stalker.exceptions import OverBookedError
from stalker.views import get_datetime, get_logged_in_user, PermissionChecker

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)

@view_config(
    route_name='dialog_create_vacation',
    renderer='templates/vacation/dialog_create_vacation.jinja2',
)
def create_vacation_dialog(request):
    """creates a create_vacation_dialog by using the given user
    """
    logger.debug('inside create_vacation_dialog')
    
    # get logged in user
    logged_in_user = get_logged_in_user(request)

    
    user_id = request.matchdict['user_id']
    user = User.query.filter(User.user_id==user_id).first()

    vacation_types = Type.query.filter_by(target_entity_type='Vacation').all()
    
    studio = Studio.query.first()
    if not studio:
        studio = defaults
    
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request),
        'studio': studio,
        'logged_in_user': logged_in_user,
        'user': user,
        'types':vacation_types
    }

@view_config(
    route_name='dialog_update_vacation',
    renderer='templates/vacation/dialog_create_vacation.jinja2',
)
def update_vacation_dialog(request):
    """updates a create_vacation_dialog by using the given user
    """
    logger.debug('inside updates_vacation_dialog')

    # get logged in user
    logged_in_user = get_logged_in_user(request)

    vacation_id = request.matchdict['vacation_id']
    vacation = Vacation.query.filter_by(id=vacation_id).first()


    vacation_types = Type.query.filter_by(target_entity_type='Vacation').all()

    studio = Studio.query.first()
    if not studio:
        studio = defaults

    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'studio': studio,
        'logged_in_user': logged_in_user,
        'user': vacation.user,
        'vacation': vacation,
        'types':vacation_types
    }


@view_config(
    route_name='create_vacation'
)
def create_vacation(request):
    """runs when creating a vacation
    """
    user_id = request.params.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    
    #**************************************************************************
    # collect data
    logged_in_user = get_logged_in_user(request)

    type_name = request.params.get('type_name')
    start_date = get_datetime(request, 'start_date', 'start_time')
    end_date = get_datetime(request, 'end_date', 'end_time')
    
    logger.debug('user_id     : %s' % user_id)
    logger.debug('user        : %s' % user)
    logger.debug('start_date  : %s' % start_date)
    logger.debug('end_date    : %s' % end_date)
    
    if user and start_date and end_date:
        # we are ready to create the time log
        # Vacation should handle the extension of the effort

        type_ = Type.query\
            .filter_by(target_entity_type='Vacation')\
            .filter_by(name=type_name)\
            .first()

        if type_ is None:
            # create a new Type
            # TODO: should we check for permission here or will it be already done in the UI (ex. filteringSelect instead of comboBox)
            type_ = Type(
                name=type_name,
                code=type_name,
                target_entity_type='Vacation'
            )

        vacation = Vacation(
            user=user,
            created_by=logged_in_user,
            type = type_,
            start=start_date,
            end=end_date
        )
        DBSession.add(vacation)
    else:
        HTTPServerError()
    
    return HTTPOk()


@view_config(
    route_name='update_vacation'
)
def update_vacation(request):
    """runs when updating a vacation
    """

    vacation_id = request.params.get('vacation_id')
    vacation = Vacation.query.filter_by(id=vacation_id).first()

    #**************************************************************************
    # collect data
    logged_in_user = get_logged_in_user(request)

    type_name = request.params.get('type_name')
    start_date = get_datetime(request, 'start_date', 'start_time')
    end_date = get_datetime(request, 'end_date', 'end_time')

    logger.debug('start_date  : %s' % start_date)
    logger.debug('end_date    : %s' % end_date)

    if vacation and start_date and end_date:
        # we are ready to create the time log
        # Vacation should handle the extension of the effort
        type_ = Type.query\
            .filter_by(target_entity_type='Vacation')\
            .filter_by(name=type_name)\
            .first()

        if type_ is None:
            # create a new Type
            # TODO: should we check for permission here or will it be already done in the UI (ex. filteringSelect instead of comboBox)
            type_ = Type(
                name=type_name,
                code=type_name,
                target_entity_type='Vacation'
            )

        vacation.updated_by = logged_in_user
        vacation.type = type_
        vacation.start = start_date
        vacation.end = end_date

        DBSession.add(vacation)
    else:
       HTTPServerError()

    return HTTPOk()

@view_config(
    route_name='list_vacations',
    renderer='templates/vacation/content_list_vacations.jinja2'
)
def list_vacations(request):
    """lists the time logs of the given user
    """

    logger.debug('list_vacations is running')

    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()

    logger.debug('user_id : %s' % user_id)
    return {
        'user': user,
        'has_permission': PermissionChecker(request)
    }

@view_config(
    route_name='get_vacations',
    renderer='json'
)
def get_vacations(request):
    """returns all the Shots of the given Project
    """
    logger.debug('get_vacations is running')
    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()

    logger.debug('user_id : %s' % user_id)

    vacation_data = []

    # if user.vacations:
    for vacation in user.vacations:
        logger.debug('vacation.user.id : %s' % vacation.user.id)
        assert isinstance(vacation, Vacation)
        vacation_data.append({
            'id': vacation.id,
            'type': vacation.type.name,
            'created_by_id': vacation.created_by_id,
            'created_by_name': vacation.created_by.name,
            'start_date' : vacation.start.strftime('%s'),
            'end_date':vacation.end.strftime('%s')

            # 'hours_to_complete': vacation.hours_to_complete,
            # 'notes': vacation.notes
        })

    return vacation_data

