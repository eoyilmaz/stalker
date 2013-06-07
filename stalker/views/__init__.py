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

import os
import uuid
import logging
import datetime

from pyramid.httpexceptions import HTTPServerError, HTTPOk
from pyramid.view import view_config
from pyramid.response import  Response, FileResponse
from pyramid.security import has_permission, authenticated_userid
import transaction

from stalker import log, User, defaults, Entity, Link, Tag
from stalker.db import DBSession

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


class PermissionChecker(object):
    """Helper class for permission check
    """
    def __init__(self, request):
        self.has_permission = has_permission
        self.request = request
    
    def __call__(self, perm):
        return self.has_permission(perm, self.request.context, self.request)


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


def get_logged_in_user(request):
    """Returns the logged in user
    
    :param request: Request object
    """
    return User.query.filter_by(login=authenticated_userid(request)).first()


def get_multi_integer(request, attr_name):
    """Extracts multi data from request.POST
    
    :param request: Request object
    :param attr_name: Attribute name to extract data from
    :return:
    """
    return [int(attr) for attr in request.POST.getall(attr_name)]


def get_color_as_int(request, attr_name):
    """Extracts a color from request
    """
    return int(request.params.get(attr_name, '#000000')[1:], 16)


def get_tags(request):
    """Extracts Tags from the given request
    
    :param request: Request object
    :return: A list of stalker.models.tag.Tag instances
    """

    # Tags
    tags = []
    tag_names = request.POST.getall('tag_names')
    for tag_name in tag_names:
        logger.debug('tag_name %s' % tag_name)
        tag = Tag.query.filter(Tag.name==tag_name).first()
        if not tag:
            logger.debug('new tag is created %s' % tag_name)
            tag = Tag(name=tag_name)
            DBSession.add(tag)
        tags.append(tag)
        
    return tags


def upload_file_to_server(request, file_param_name):
    """uploads a file from a request.POST to the given path
    
    Uses the hex representation of a uuid4 sequence as the filename.

    The first two digits of the uuid4 is used for the first folder name,
    there are 256 possible variations, then the third and fourth characters
    are used for the second folder name (again 256 other possibilities) and
    then the uuid4 sequence with the original file extension generates the
    filename.

    The extension is used on purpose where OSes like windows can infer the file
    type from the extension.

    {{server_side_storage_path}}/{{uuid4[:2]}}/{{uuid4[2:4]}}//{{uuuid4}}.extension
    
    :param request: The request object.
    :param str file_param_name: The name of the parameter that holds the file.
    :returns (str, str): The original filename and the file path on the server.
    """
    # get the filename
    file_param = request.POST.get(file_param_name)
    filename = file_param.filename
    extension = os.path.splitext(filename)[1]
    input_file = file_param.file
    
    logger.debug('file_param : %s' % file_param)
    logger.debug('filename   : %s' % filename)
    logger.debug('extension  : %s' % extension)
    logger.debug('input_file : %s' % input_file)

    # upload it to the stalker server side storage path

    new_filename = uuid.uuid4().hex + extension

    first_folder = new_filename[:2]
    second_folder = new_filename[2:4]

    file_path = os.path.join(
        defaults.server_side_storage_path,
        first_folder,
        second_folder
    )
    
    file_full_path = os.path.join(
        file_path,
        new_filename
    )

    # write down to a temp file first
    temp_file_path = file_full_path + '~'
    
    # create folders
    os.makedirs(file_path)

    output_file = open(temp_file_path, 'wb') # TODO: guess ascii or binary mode    

    input_file.seek(0)
    while True: # TODO: use 'with'
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)
    output_file.close()

    # data is written completely, rename temp file to original file
    os.rename(temp_file_path, file_full_path)
    
    # create a Link instance and return it
    new_link = Link(
        full_path= file_full_path,
        original_filename=filename,
        created_by=get_logged_in_user(request)
    )
    DBSession.add(new_link)
    transaction.commit()
    
    return new_link

@view_config(
    route_name='dialog_upload_thumbnail',
    renderer='templates/dialog_upload_thumbnail.jinja2'
)
def dialog_upload_thumbnail(request):
    """fills the upload thumbnail dialog
    """
    entity_id = request.matchdict.get('entity_id', -1)
    entity = Entity.query.filter_by(id=entity_id).first()
    
    logger.debug('entity_id : %s' % entity_id)
    logger.debug('entity    : %s' % entity)
    
    return {
        'entity': entity,
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='upload_thumbnail',
    renderer='json'
)
def upload_thumbnail(request):
    """uploads a thumbnail to the server
    """
    # entity_id = request.matchdict.get('entity_id')
    # entity = Entity.query.filter_by(id=entity_id).first()

    try:
        new_link = upload_file_to_server(request, 'uploadedfile')
    except IOError:
        HTTPServerError()
    else:
        # store the link object
        DBSession.add(new_link)
        
        return {
            'file': new_link.full_path,
            'name': new_link.original_filename,
            'width': 320,
            'height': 240,
            'type': os.path.splitext(new_link.original_filename)[1],
            'link_id': new_link.id
        }


@view_config(
    route_name='assign_thumbnail',
)
def assign_thumbnail(request):
    """assigns the thumbnail to the given entity
    """
    link_id = request.params.get('link_id', -1)
    entity_id = request.params.get('entity_id', -1)
    
    link = Link.query.filter_by(id=link_id).first()
    entity = Entity.query.filter_by(id=entity_id).first()
    
    logger.debug('link_id   : %s' % link_id)
    logger.debug('link      : %s' % link)
    logger.debug('entity_id : %s' % entity_id)
    logger.debug('entity    : %s' % entity)
    
    if entity and link:
        entity.thumbnail = link
        DBSession.add(entity)
        DBSession.add(link)
    
    return HTTPOk()



@view_config(
    route_name='serve_files'
)
def serve_files(request):
    """serves files in the stalker server side storage
    """
    partial_file_path = request.matchdict['partial_file_path']
    
    logger.debug('partial_file_path : %s' % partial_file_path)
    
    file_full_path = os.path.join(
        defaults.server_side_storage_path,
        partial_file_path
    )
    
    return FileResponse(file_full_path)
    


def seconds_since_epoch(dt):
    """converts the given datetime.datetime instance to an integer showing the
    seconds from epoch, and does it without using the strftime('%s') which
    uses the time zone info of the system.
    
    :param dt: datetime.datetime instance to be converted
    :returns int: showing the seconds since epoch
    """
    dts = dt - datetime.datetime(1970, 1, 1)
    return dts.days * 86400 + dts.seconds

def microseconds_since_epoch(dt):
    """converts the given datetime.datetime instance to an integer showing the
    microseconds from epoch, and does it without using the strftime('%s') which
    uses the time zone info of the system.
    
    :param dt: datetime.datetime instance to be converted
    :returns int: showing the microseconds since epoch
    """
    dts = dt - datetime.datetime(1970, 1, 1)
    return (dts.days * 86400 + dts.seconds) * 1000 + dts.microseconds
