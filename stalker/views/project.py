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
from pyramid.httpexceptions import HTTPOk, HTTPServerError
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from stalker.db import DBSession
from stalker.views import get_date, get_logged_in_user, PermissionChecker
from stalker import (User, ImageFormat, Repository, Structure, Status,
                     StatusList, Project, Entity)

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='dialog_create_project',
    renderer='templates/project/dialog_create_project.jinja2',
)
def create_project_dialog(request):
    """called when the create project dialog is requested
    """
    logged_in_user = get_logged_in_user(request)
    
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request),
        'logged_in_user': logged_in_user
    }


@view_config(
    route_name='dialog_update_project',
    renderer='templates/project/dialog_create_project.jinja2'
)
def update_project_dialog(request):
    """runs when updating a project
    """
    logged_in_user = get_logged_in_user(request)
    
    project_id = request.matchdict['project_id']
    project = Project.query.filter_by(id=project_id).first()
    
    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'project': project,
        'logged_in_user': logged_in_user
    }


@view_config(
    route_name='create_project'
)
def create_project(request):
    """called when adding a new Project
    """
    logged_in_user = get_logged_in_user(request)
    
    # parameters
    name = request.params.get('name')
    code = request.params.get('code')
    fps = int(request.params.get('fps'))
    
    imf_id = request.params.get('image_format', -1)
    imf = ImageFormat.query.filter_by(id=imf_id).first()
    
    repo_id = request.params.get('repository_id', -1)
    repo = Repository.query.filter_by(id=repo_id).first()
    
    structure_id = request.params.get('structure_id', -1)
    structure = Structure.query.filter_by(id=structure_id).first()
    
    lead_id = request.params.get('lead_id', -1)
    lead = User.query.filter_by(id=lead_id).first()
    
    status_id = request.params.get('status_id', -1)
    status = Status.query.filter_by(id=status_id).first()
    
    # get the dates
    start = get_date(request, 'start')
    end = get_date(request, 'end')
    
    if name and code and imf and repo and structure and lead_id and status:
        # lets create the project
        
        # status list
        status_list = StatusList.query\
            .filter_by(target_entity_type='Project').first()
        
        new_project = Project(
            name=name,
            code=code,
            image_format=imf,
            repository=repo,
            created_by=logged_in_user,
            fps=fps,
            structure=structure,
            lead=lead,
            status_list=status_list,
            status=status,
            start=start,
            end=end
        )
        
        DBSession.add(new_project)
        
    else:
        logger.debug('there are missing parameters')
        HTTPServerError()
    
    return HTTPOk()


@view_config(
    route_name='update_project'
)
def update_project(request):
    """called when updating a Project
    """
    logged_in_user = get_logged_in_user(request)
    
    # parameters
    project_id = request.params.get('project_id', -1)
    project = Project.query.filter_by(id=project_id).first()
    
    name = request.params.get('name')
    
    fps = int(request.params.get('fps'))
    
    imf_id = request.params.get('image_format', -1)
    imf = ImageFormat.query.filter_by(id=imf_id).first()
    
    repo_id = request.params.get('repository_id', -1)
    repo = Repository.query.filter_by(id=repo_id).first()
    
    structure_id = request.params.get('structure_id', -1)
    structure = Structure.query.filter_by(id=structure_id).first()
    
    lead_id = request.params.get('lead_id', -1)
    lead = User.query.filter_by(id=lead_id).first()
    
    status_id = request.params.get('status_id', -1)
    status = Status.query.filter_by(id=status_id).first()
    
    # get the dates
    start = get_date(request, 'start')
    end = get_date(request, 'end')
    
    if project and name and imf and repo and structure and lead and \
            status:
        
        project.name = name
        project.image_format = imf
        project.repository = repo
        project.updated_by = logged_in_user
        project.date_updated = datetime.datetime.now()
        project.fps = fps
        project.structure = structure
        project.lead = lead
        project.status = status
        project.start = start
        project.end = end
    
        DBSession.add(project)
    
    else:
        logger.debug('there are missing parameters')
        HTTPServerError()
    
    return HTTPOk()



@view_config(
    route_name='list_projects',
    renderer='templates/project/content_list_projects.jinja2'
)
def view_projects(request):
    """runs when viewing all projects
    """

    logged_in_user = get_logged_in_user(request)

    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    # just return all the projects
    return {
        'entity': entity,
        'logged_in_user': logged_in_user,
        'has_permission': PermissionChecker(request)
    }

@view_config(
    route_name='get_projects_byEntity',
    renderer='json'
)
def get_projects_byEntity(request):
    """
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    return [
        {
            'id': project.id,
            'name': project.name,
            'thumbnail_path': project.thumbnail.full_path
                                            if project.thumbnail else None
        }
        for project in entity.projects
    ]


@view_config(
    route_name='get_projects',
    renderer='json'
)
def get_projects(request):
    """returns all the Project instances in the database
    """
    return [
        {
            'id': proj.id,
            'name': proj.name
        }
        for proj in Project.query.all()
    ]


@view_config(
    route_name='overview_project',
    renderer='templates/project/page_view_project_overview.jinja2'
)
@view_config(
    route_name='view_project',
    renderer='templates/project/page_view_project.jinja2'
)
@view_config(
    route_name='list_assets',
    renderer='templates/asset/content_list_assets.jinja2'
)
@view_config(
    route_name='list_shots',
    renderer='templates/shot/content_list_shots.jinja2'
)
@view_config(
    route_name='list_sequences',
    renderer='templates/sequence/content_list_sequences.jinja2'
)
@view_config(
    route_name='summarize_project',
    renderer='templates/project/content_summarize_project.jinja2'
)
def view_project_related_data(request):
    """runs when viewing project related data
    """
    logged_in_user = get_logged_in_user(request)
    
    project_id = request.matchdict['project_id']
    project = Project.query.filter_by(id=project_id).first()
    
    return {
        'user': logged_in_user,
        'project': project,
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='view_task_nav_bar',
    renderer='templates/task/content_task_nav_bar.jinja2',
)
@view_config(
    route_name='view_entity_nav_bar',
    renderer='templates/content_nav_bar.jinja2',
)
def view_entity_nav_bar(request):
    """runs when viewing all projects
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    # just return all the projects
    return {
        'entity': entity,
        'has_permission': PermissionChecker(request)
    }
