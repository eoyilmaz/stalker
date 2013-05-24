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
from pyramid.httpexceptions import HTTPOk

from pyramid.security import authenticated_userid
from pyramid.view import view_config


from stalker.db import DBSession
from stalker import User, ImageFormat
from stalker.views import PermissionChecker, get_logged_in_user

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='dialog_create_image_format',
    renderer='templates/format/dialog_create_image_format.jinja2'
)
def dialog_create_image_format(request):
    """fills create image format dialog
    """
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='dialog_update_image_format',
    renderer='templates/format/dialog_create_image_format.jinja2'
)
def dialog_update_image_format(request):
    """fills update image format dialog
    """
    imf_id = request.matchdict['imf_id']
    imf = ImageFormat.query\
            .filter(ImageFormat.id==imf_id)\
            .first()
    return {
        'mode': 'UPDATE',
        'imf': imf,
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='create_image_format'
)
def create_image_format(request):
    """creates an image format
    """
    logged_in_user = get_logged_in_user(request)
    
    name = request.params.get('name')
    width = int(request.params.get('width', -1))
    height = int(request.params.get('height', -1))
    pixel_aspect = float(request.params.get('pixel_aspect', -1))
    
    if name and width and height and pixel_aspect:
        # create a new ImageFormat and save it to the database
        new_image_format = ImageFormat(
            name=name,
            width=width,
            height=height,
            pixel_aspect=pixel_aspect,
            created_by=logged_in_user
        )
        DBSession.add(new_image_format)
    
    return HTTPOk()


@view_config(
    route_name='update_image_format'
)
def update_image_format(request):
    """updates an image format
    """
    logged_in_user = get_logged_in_user(request)

    # get params
    imf_id = request.params.get('imf_id', -1)
    imf = ImageFormat.query.filter_by(id=imf_id).first()
    
    name = request.params.get('name')
    width = int(request.params.get('width', -1))
    height = int(request.params.get('height', -1))
    pixel_aspect = float(request.params.get('pixel_aspect', -1))
    
    if imf and name and width and height and pixel_aspect:
        imf.name = request.params['name']
        imf.width = int(request.params['width'])
        imf.height = int(request.params['height'])
        imf.pixel_aspect = float(request.params['pixel_aspect'])
        imf.updated_by = logged_in_user
        imf.date_updated = datetime.datetime.now()
        DBSession.add(imf)
    
    return HTTPOk()


@view_config(
    route_name='get_image_formats',
    renderer='json'
)
def get_image_formats(request):
    """returns all the image formats in the database
    """
    return [
        {
            'id': imf.id,
            'name': imf.name,
            'width': imf.width,
            'height': imf.height,
            'pixel_aspect': imf.pixel_aspect
        }
        for imf in ImageFormat.query.all()
    ]


