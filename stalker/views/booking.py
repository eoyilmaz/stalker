# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
from pyramid.view import view_config
from stalker import Task

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
    task_id = request.matchdict['task_id']
    task = Task.query.filter(Task.task_id==task_id).first()
    
    return {
        'task': task
    }
