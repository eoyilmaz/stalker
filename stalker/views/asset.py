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

from pyramid.httpexceptions import HTTPServerError, HTTPOk
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from stalker import User, Project, Type, StatusList, Status, Asset
from stalker.db import DBSession

import logging
from stalker import log
from stalker.views import PermissionChecker, get_logged_in_user

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='dialog_create_asset',
    renderer='templates/asset/dialog_create_asset.jinja2'
)
def create_asset_dialog(request):
    """fills the create asset dialog
    """
    project_id = request.matchdict['project_id']
    project = Project.query.filter_by(id=project_id).first()
    asset_types = Type.query.filter_by(target_entity_type='Asset').all()
    
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request),
        'project': project,
        'types': asset_types
    }

@view_config(
    route_name='dialog_update_asset',
    renderer='templates/asset/dialog_create_asset.jinja2'
)
def update_asset_dialog(request):
    """fills the update asset dialog
    """
    asset_id = request.matchdict['asset_id']
    asset = Asset.query.filter_by(id=asset_id).first()
    asset_types = Type.query.filter_by(target_entity_type='Asset').all()
    
    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'project': asset.project,
        'types': asset_types,
        'asset': asset
    }


@view_config(
    route_name='create_asset'
)
def create_asset(request):
    """creates a new Asset
    """
    logged_in_user = get_logged_in_user(request)
    
    # get params
    name = request.params.get('name')
    code = request.params.get('code')
    description = request.params.get('description')
    type_name = request.params.get('type_name')
    
    status_id = request.params.get('status_id')
    status = Status.query.filter_by(id=status_id).first()
    
    project_id = request.params.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    logger.debug('project_id   : %s' % project_id)
    
    if name and code and type_name and status and  project:
        # get the type
        type_ = Type.query\
            .filter_by(target_entity_type='Asset')\
            .filter_by(name=type_name)\
            .first()
        
        if type_ is None:
            # create a new Type
            # TODO: should we check for permission here or will it be already done in the UI (ex. filteringSelect instead of comboBox)
            type_ = Type(
                name=type_name,
                code=type_name,
                target_entity_type='Asset'
            )
        
        # get the status_list
        status_list = StatusList.query.filter_by(
            target_entity_type='Asset'
        ).first()
        
        # there should be a status_list
        # TODO: you should think about how much possible this is
        if status_list is None:
            return HTTPServerError(detail='No StatusList found')
        
        # create the asset
        new_asset = Asset(
            name=name,
            code=code,
            description=description,
            project=project,
            type=type_,
            status_list=status_list,
            status=status,
            created_by=logged_in_user
        )
        
        DBSession.add(new_asset)
    else:
        logger.debug('there are missing parameters')
        logger.debug('name      : %s' % name)
        logger.debug('code      : %s' % code)
        logger.debug('type_name : %s' % type_name)
        logger.debug('status    : %s' % status)
        logger.debug('project   : %s' % project)
        HTTPServerError()

    return HTTPOk()


@view_config(
    route_name='update_asset'
)
def update_asset(request):
    """updates an Asset
    """
    logged_in_user = get_logged_in_user(request)
    
    # get params
    asset_id = request.params.get('asset_id')
    asset = Asset.query.filter_by(id=asset_id).first()
    
    name = request.params.get('name')
    description = request.params.get('description')
    type_name = request.params.get('type_name')
    
    status_id = request.params.get('status_id')
    status = Status.query.filter_by(id=status_id).first()
    
    if asset and name and type_name and status:
        # get the type
        type_ = Type.query\
            .filter_by(target_entity_type='Asset')\
            .filter_by(name=type_name)\
            .first()
        
        if type_ is None:
            # create a new Type
            type_ = Type(
                name=type_name,
                code=type_name,
                target_entity_type='Asset'
            )
        
        # update the asset
        asset.name = name
        asset.description = description
        asset.type = type_
        asset.status = status
        asset.updated_by = logged_in_user
        asset.date_updated = datetime.datetime.now()
        
        DBSession.add(asset)
    
    return HTTPOk()


@view_config(
    route_name='view_asset',
    renderer='templates/asset/page_view_asset.jinja2'
)
def view_asset(request):
    """runs when viewing an asset
    """
    logged_in_user = get_logged_in_user(request)

    asset_id = request.matchdict['asset_id']
    asset = Asset.query.filter_by(id=asset_id).first()

    return {
        'user': logged_in_user,
        'has_permission': PermissionChecker(request),
        'asset': asset
    }


@view_config(
    route_name='summarize_asset',
    renderer='templates/asset/content_summarize_asset.jinja2'
)
def summarize_asset(request):
    """runs when viewing an asset
    """
    logged_in_user = get_logged_in_user(request)

    asset_id = request.matchdict['asset_id']
    asset = Asset.query.filter_by(id=asset_id).first()

    return {
        'user': logged_in_user,
        'has_permission': PermissionChecker(request),
        'asset': asset
    }


@view_config(
    route_name='get_assets',
    renderer='json'
)
def get_assets(request):
    """returns all the Assets of a given Project
    """
    project_id = request.matchdict['project_id']
    return [
        {
            'id': asset.id,
            'name': asset.name,
            'type': asset.type.name,
            'status': asset.status.name,
            'status_bg_color': asset.status.bg_color,
            'status_fg_color': asset.status.fg_color,
            'user_id': asset.created_by.id,
            'user_name': asset.created_by.name,
            'description': asset.description,
            'thumbnail_path': asset.thumbnail.full_path if asset.thumbnail else None
        }
        for asset in Asset.query.filter_by(project_id=project_id).all()
    ]
