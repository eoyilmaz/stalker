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
from pyramid.httpexceptions import HTTPOk, HTTPServerError

from pyramid.view import view_config

from stalker.db import DBSession
from stalker import Repository
from stalker import log
from stalker.views import PermissionChecker, get_logged_in_user

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='dialog_create_repository',
    renderer='templates/repository/dialog_create_repository.jinja2',
)
def dialog_create_repository(request):
    """fills the create repository dialog
    """
    # nothing is needed
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='dialog_update_repository',
    renderer='templates/repository/dialog_create_repository.jinja2'
)
def dialog_update_repository(request):
    """fills the update repository dialog
    """
    repo_id = request.matchdict['repo_id']
    repo = Repository.query.filter_by(id=repo_id).first()
    
    return {
        'mode': 'UPDATE',
        'repo': repo,
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='create_repository'
)
def create_repository(request):
    """creates a new repository
    """
    logged_in_user = get_logged_in_user(request)
    
    # get params
    name = request.params.get('name')
    windows_path = request.params.get('windows_path')
    linux_path = request.params.get('linux_path')
    osx_path = request.params.get('osx_path')
    
    if name and windows_path and linux_path and osx_path:
        # create a new Repository and save it to the database
         new_repository = Repository(
             name=name,
             windows_path=windows_path,
             linux_path=linux_path,
             osx_path=osx_path,
             created_by=logged_in_user
         )
         DBSession.add(new_repository)
    
    return HTTPOk()


@view_config(
    route_name='update_repository'
)
def update_repository(request):
    """updates a repository
    """
    logged_in_user = get_logged_in_user(request)
    
    repo_id = request.params.get('repo_id')
    repo = Repository.query.filter_by(id=repo_id).first()
    
    name = request.params.get('name')
    windows_path = request.params.get('windows_path')
    linux_path = request.params.get('linux_path')
    osx_path = request.params.get('osx_path')
    
    if repo and name and windows_path and linux_path and osx_path:
        repo.name = name
        repo.windows_path = windows_path
        repo.linux_path = linux_path
        repo.osx_path = osx_path
        repo.updated_by = logged_in_user
        repo.date_updated = datetime.datetime.now()
        
        DBSession.add(repo)
    
    return HTTPOk()


@view_config(
    route_name='get_repositories',
    renderer='json'
)
def get_repositories(request):
    """returns all the repositories in the database
    """
    return [
        {
            'id': repo.id,
            'name': repo.name,
            'linux_path': repo.linux_path,
            'osx_path': repo.osx_path,
            'windows_path': repo.windows_path
        }
        for repo in Repository.query.all()
    ]
