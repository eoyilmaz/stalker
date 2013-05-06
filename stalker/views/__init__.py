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

import logging
import datetime

from pyramid.httpexceptions import HTTPServerError
from pyramid.view import view_config
from pyramid.response import  Response

from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


def log_param(request, param):
    if param in request.params:
        logger.debug('%s: %s' % (param, request.params[param]))
    else:
        logger.debug('%s not in params' % param)


@view_config(
   context=HTTPServerError 
)
def server_error(exc, request):
    msg = exc.args[0] if exc.args else ''
    response = Response('Server Error: %s' % msg)
    response.status_int = 500
    return response


def get_time(request, time_attr):
    """Extracts a time object from the given request
    
    :param request: the request object
    :param time_attr: the attribute name
    :return: datetime.timedelta
    """
    time_part = datetime.datetime.strptime(
        request.params[time_attr][:-6],
        "%Y-%m-%dT%H:%M:%S"
    )
    
    return datetime.timedelta(
        hours=time_part.hour,
        minutes=time_part.minute
    )


def get_date(request, date_attr):
    """Extracts a datetime object from the given request
    
    :param request: the request instance
    :param date_attr: the attribute name
    :return: datetime.datetime
    """
    # TODO: no time zone info here, please add time zone
    return datetime.datetime.strptime(
        request.params[date_attr][:-6],
        "%Y-%m-%dT%H:%M:%S"
    )


def get_datetime(request, date_attr, time_attr):
    """Extracts a datetime object from the given request
    :param request: the request object
    :param date_attr: the attribute name
    :return: datetime.datetime
    """
    # TODO: no time zone info here, please add time zone
    date_part = datetime.datetime.strptime(
        request.params[date_attr][:-6],
        "%Y-%m-%dT%H:%M:%S"
    )
    time_part = datetime.datetime.strptime(
        request.params[time_attr][:-6],
        "%Y-%m-%dT%H:%M:%S"
    )
    # update the time values of date_part with time_part
    return date_part.replace(
        hour=time_part.hour,
        minute=time_part.minute,
        second=time_part.second,
        microsecond=time_part.microsecond
    )


@view_config(
    route_name='busy_dialog',
    renderer='templates/busy_dialog.jinja2'
)
def busy_dialog(request):
    """generates a busy dialog
    """
    return {}
