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

from pyramid.httpexceptions import HTTPOk
from pyramid.view import view_config

from stalker.db import DBSession
from stalker import FilenameTemplate

from stalker import log
from stalker.views import PermissionChecker, get_logged_in_user

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)

@view_config(
    route_name='dialog_create_filename_template',
    renderer='templates/template/dialog_create_filename_template.jinja2'
)
def dialog_create_filename_template(request):
    """fills the create filename template dialog
    """
    # for now prepare the data by hand
    entity_types = ['Asset', 'Shot', 'Sequence', 'Project', 'Task']

    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request),
        'entity_types': entity_types
    }


@view_config(
    route_name='dialog_update_filename_template',
    renderer='templates/template/dialog_create_filename_template.jinja2',
)
def dialog_update_filename_template(request):
    """fills the update filename template dialog
    """
    # get the filename template
    ft_id = request.matchdict['ft_id']
    ft = FilenameTemplate.query.filter_by(id=ft_id).first()

    # for now prepare the data by hand
    entity_types = ['Asset', 'Shot', 'Sequence', 'Project', 'Task']

    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'ft': ft,
        'entity_types': entity_types
    }

@view_config(
    route_name='create_filename_template'
)
def create_filename_template(request):
    """creates a new FilenameTemplate
    """
    logged_in_user = get_logged_in_user(request)

    # get parameters
    name = request.params.get('name')
    target_entity_type = request.params.get('target_entity_type')
    path = request.params.get('path')
    filename = request.params.get('filename')

    if name and target_entity_type and path and filename:
        new_ft = FilenameTemplate(
            name=name,
            target_entity_type=target_entity_type,
            path=path,
            filename=filename,
            created_by=logged_in_user
        )
        DBSession.add(new_ft)

    return HTTPOk()


@view_config(
    route_name='update_filename_template',
)
def update_filename_template(request):
    """updates a FilenameTemplate instance
    """
    logged_in_user = get_logged_in_user(request)

    name = request.params.get('name')
    path = request.params.get('path')
    filename = request.params.get('filename')
    ft_id = request.params.get('ft_id')
    ft = FilenameTemplate.query.filter_by(id=ft_id).first()

    if name and path and filename and ft:
        ft.name = name
        ft.path = path
        ft.filename = filename

        ft.updated_by = logged_in_user
        ft.date_updated = datetime.datetime.now()

        DBSession.add(ft)

    return HTTPOk()


@view_config(
    route_name='get_filename_templates',
    renderer='json'
)
def get_filename_templates(request):
    """returns all the FilenameTemplates in the database
    """
    return [
        {
            'id': ft.id,
            'name': ft.name,
            'target_entity_type': ft.target_entity_type,
        }
        for ft in FilenameTemplate.query.all()
    ]
