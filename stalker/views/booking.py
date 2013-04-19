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
from pyramid.httpexceptions import HTTPOk
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from stalker import Task, User, Studio

from stalker import defaults

import logging
from stalker import log
from stalker.views import get_datetime

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)

@view_config(
    route_name='create_booking_dialog',
    renderer='templates/booking/dialog_create_booking.jinja2',
    permission='Create_Booking'
)
def create_booking_dialog(request):
    """creates a create_booking_dialog by using the given task
    """
    logger.debug('inside create_booking_dialog')
    
    # get logged in user
    logged_in_user_id = authenticated_userid(request)
    logged_in_user = User.query.filter(User.id==logged_in_user_id).first()
    
    task_id = request.matchdict['task_id']
    task = Task.query.filter(Task.task_id==task_id).first()
    
    studio = Studio.query.first()
    if not studio:
        studio = defaults
    
    return {
        'studio': studio,
        'logged_in_user': logged_in_user,
        'task': task
    }

@view_config(
    route_name='create_booking',
    permission='Create_Booking'
)
def create_booking(request):
    """runs when creating a booking
    """
    task_id = request.matchdict['task_id']
    task = Task.query.filter(Task.id==task_id).first()
    
    #**************************************************************************
    # collect data
    resource_id = request.get('resource_id')
    start_date = get_datetime(request, 'start_date', 'start_time')
    end_date = get_datetime(request, 'end_date', 'end_time')
    
    
    return HTTPOk()
