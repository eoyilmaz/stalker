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
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from stalker import Task, User

import logging
from stalker import log
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
    
    return {
        'logged_in_user': logged_in_user,
        'task': task
    }
