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
from pyramid.security import authenticated_userid, has_permission
from pyramid.view import view_config
from stalker import Task, User, Studio, TimeLog

from stalker import defaults

import logging
from stalker import log
from stalker.db import DBSession
from stalker.views import get_datetime

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)

@view_config(
    route_name='dialog_create_time_log',
    renderer='templates/time_log/dialog_create_time_log.jinja2',
)
def create_time_log_dialog(request):
    """creates a create_time_log_dialog by using the given task
    """
    logger.debug('inside create_time_log_dialog')
    
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
    route_name='create_time_log'
)
def create_time_log(request):
    """runs when creating a time_log
    """
    task_id = request.matchdict['task_id']
    task = Task.query.filter(Task.id==task_id).first()
    
    #**************************************************************************
    # collect data
    resource_id = request.params.get('resource_id', None)
    resource = User.query.filter(User.id==resource_id).first()
    
    start_date = get_datetime(request, 'start_date', 'start_time')
    end_date = get_datetime(request, 'end_date', 'end_time')
    
    logger.debug('task_id     : %s' % task_id)
    logger.debug('task        : %s' % task)
    logger.debug('resource_id : %s' % resource_id)
    logger.debug('start_date  : %s' % start_date)
    logger.debug('end_date    : %s' % end_date)
    
    if task and resource and start_date and end_date:
        # we are ready to create the time log
        # TimeLog should handle the extension of the effort
        time_log = TimeLog(
            task=task,
            resource=resource,
            start=start_date,
            end=end_date
        )
        DBSession.add(time_log)
    
    return HTTPOk()


@view_config(
    route_name='list_time_logs',
    renderer='templates/time_log/content_list_time_logs.jinja2'
)
def list_time_logs(request):
    """lists the time logs of the given task
    """
    task_id = request.matchdict['task_id']
    task = Task.query.filter_by(id=task_id).first()
    
    time_logs = []
    if task:
        time_logs = task.time_logs
    
    return {
        'task': task,
        'time_logs': time_logs,
        'has_permission': has_permission
    }
