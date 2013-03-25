# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from pyramid.security import authenticated_userid
from pyramid.view import view_config
import transaction

from stalker.db import DBSession
from stalker import User, ImageFormat

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='edit_image_format',
    renderer='templates/format/edit_image_format.jinja2',
    permission='Edit_ImageFormat'
)
def edit_image_format(request):
    """called when editing an image format
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    imf_id = request.matchdict['imf_id']
    imf = ImageFormat.query\
            .filter(ImageFormat.id==imf_id)\
            .first()
    
    if 'submitted' in request.params:
        if 'name' in request.params and \
            'width' in request.params and \
            'height' in request.params and \
            'pixel_aspect' in request.params and \
            'submitted' in request.params:
            if request.params['submitted'] == 'edit':
                imf.name = request.params['name']
                imf.width = int(request.params['width'])
                imf.height = int(request.params['height'])
                imf.pixel_aspect = float(request.params['pixel_aspect'])
                imf.updated_by = user
                DBSession.add(imf)
                #try:
                #    transaction.commit()
                #except (IntegrityError, DetachedInstanceError) as e:
                #    logging.debug(e)
                #    transaction.abort()
                #else:
                #    DBSession.flush()
    
    return {'image_format': imf}


@view_config(
    route_name='get_image_formats',
    renderer='json',
    permission='View_ImageFormat'
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


@view_config(
    route_name='add_image_format',
    renderer='templates/format/add_image_format.jinja2',
    permission='Add_ImageFormat'
)
def add_image_format(request):
    """called when adding or editing an image format
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'name' in request.params and \
       'width' in request.params and \
       'height' in request.params and \
       'pixel_aspect' in request.params:
        
        # create a new ImageFormat and save it to the database
        with transaction.manager:
            new_image_format = ImageFormat(
                name=request.params['name'],
                width=int(request.params['width']),
                height=int(request.params['height']),
                pixel_aspect=float(request.params['pixel_aspect']),
                created_by=user
            )
            DBSession.add(new_image_format)
    
    return {}
