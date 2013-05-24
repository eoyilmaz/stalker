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

from pyramid.view import view_config

from stalker.db import DBSession
from stalker import Structure, FilenameTemplate

import logging
from stalker import log
from stalker.views import PermissionChecker, get_logged_in_user, get_multi_integer

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='dialog_create_structure',
    renderer='templates/structure/dialog_create_structure.jinja2'
)
def dialog_create_structure(request):
    """fills the create structure dialog
    """
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='dialog_update_structure',
    renderer='templates/structure/dialog_create_structure.jinja2'
)
def dialog_update_structure(request):
    """fills the update structure dialog
    """
    structure_id = request.matchdict['structure_id']
    structure = Structure.query.filter_by(id=structure_id).first()
    
    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'structure': structure
    }


@view_config(
    route_name='create_structure'
)
def create_structure(request):
    """creates a structure
    """
    logged_in_user = get_logged_in_user(request)
    
    # get parameters
    name = request.params.get('name')
    custom_template = request.params.get('custom_template')
    ft_ids = get_multi_integer(request, 'filename_templates')
    fts = FilenameTemplate.query.filter(FilenameTemplate.id.in_(ft_ids)).all()

    if name and custom_template:
        # create a new structure
        new_structure = Structure(
            name=name,
            custom_template=custom_template,
            templates=fts,
            created_by=logged_in_user,
        )
        DBSession.add(new_structure)
    
    return HTTPOk()


@view_config(
    route_name='update_structure'
)
def update_structure(request):
    """updates a structure
    """
    
    logged_in_user = get_logged_in_user(request)
    
    # get params
    structure_id = request.params.get('structure_id')
    structure = Structure.query.filter_by(id=structure_id).first()
    
    name = request.params.get('name')
    custom_template = request.params.get('custom_template')
    
    # get all FilenameTemplates
    ft_ids = get_multi_integer(request, 'filename_templates')
    fts = FilenameTemplate.query.filter(FilenameTemplate.id.in_(ft_ids)).all()
    
    if name:
        # update structure
        structure.name = name
        structure.custom_template = custom_template
        structure.templates = fts
        structure.updated_by = logged_in_user
        structure.date_updated = datetime.datetime.now()
        
        DBSession.add(structure)
    
    return HTTPOk()


@view_config(
    route_name='get_structures',
    renderer='json'
)
def get_structures(request):
    """returns all the structures in the database
    """
    return [
        {
            'id': structure.id,
            'name': structure.name
        }
        for structure in Structure.query.all()
    ]
