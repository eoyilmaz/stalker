# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
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
