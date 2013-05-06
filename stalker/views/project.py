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
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError

import transaction
from stalker.db import DBSession
from stalker import (User, ImageFormat, Repository, Structure, Status,
                     StatusList, Project, Entity)

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='create_project',
    renderer='templates/project/dialog_create_project.jinja2',
    permission='Create_Project'
)
def create_project(request):
    """called when adding a project
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'create':
            # TODO: remove this later
            for param in ['name',
                          'code',
                          'image_format',
                          'repository',
                          'structure',
                          'lead',
                          'status']:
                if param not in request.params:
                    logger.debug('%s is not in parameters' % param)
 
            if 'name' in request.params and \
                'code' in request.params and \
                'image_format' in request.params and \
                'repository' in request.params and \
                'structure' in request.params and \
                'lead' in request.params and \
                'status' in request.params:
                #login = request.params['login']
                # so create the project
                
                
                # get the image format
                imf_id = int(request.params['image_format'])
                imf = ImageFormat.query.filter_by(id=imf_id).one()
                
                # get repository
                repo_id = int(request.params['repository'])
                repo = Repository.query.filter_by(id=repo_id).one()
                
                # get structure
                structure_id = int(request.params['structure'])
                structure = Structure.query.filter_by(id=structure_id).one()
                
                # get lead
                lead_id = int(request.params['lead'])
                lead = User.query.filter_by(id=lead_id).first()
                
                logger.debug('project.lead = %s' % lead)

                # status
                status_id = int(request.params['status'])
                status = Status.query.filter_by(id=status_id).first()

                # status list
                status_list = StatusList.query\
                    .filter_by(target_entity_type='Project').first()

                # get the dates
                # TODO: no time zone info here, please add time zone
                start = datetime.datetime.strptime(
                    request.params['start'][:-6],
                    "%Y-%m-%dT%H:%M:%S"
                )
                end = datetime.datetime.strptime(
                    request.params['end'][:-6],
                    "%Y-%m-%dT%H:%M:%S"
                )

                logger.debug('start : %s' % start)
                logger.debug('end : %s' % end)

                try:
                    new_project = Project(
                        name=request.params['name'],
                        code=request.params['code'],
                        image_format=imf,
                        repository=repo,
                        created_by=user,
                        fps=request.params['fps'],
                        structure=structure,
                        lead=lead,
                        status_list=status_list,
                        status=status,
                        start=start,
                        end=end
                    )
                except (AttributeError, TypeError, ValueError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_project)
                    try:
                        transaction.commit()
                    except (IntegrityError, AssertionError) as e:
                        logger.debug(e.message)
                        transaction.abort()
                    else:
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding Project')
            else:
                logger.debug('there are missing parameters')
            # do not return anything
            # or maybe we should return to where we came from
    
    # just one wants to see the add project form
    return {
        'user': user,
        'users': User.query.all(),
        'image_formats': ImageFormat.query.all(),
        'repositories': Repository.query.all(),
        'structures': Structure.query.all(),
        'status_lists': StatusList.query\
                            .filter_by(target_entity_type='Project')\
                            .all(),
    }


@view_config(
    route_name='list_projects',
    renderer='templates/project/content_list_projects.jinja2',
    permission='Read_Project'
)
def view_projects(request):
    """runs when viewing all projects
    """

    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    # just return all the projects
    return {
        'entity': entity
    }

@view_config(
    route_name='get_projects_byEntity',
    renderer='json',
    permission='Read_Project'
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
            }
        for project in entity.projects
    ]



@view_config(
    route_name='update_project',
    renderer='templates/project/dialog_update_project.jinja2',
    permission='Update_Project'
)
def update_project(request):
    """runs when updateing a project
    """
    # referrer = request.url
    # came_from = request.params.get('came_from', referrer)
    
    project_id = request.matchdict['project_id']
    project = Project.query.filter_by(id=project_id).first()
    
    # if request.params['submitted'] == 'update':
    #     #return HTTPFound(location=came_from)
    #     login = authenticated_userid(request)
    #     authenticated_user = User.query.filter_by(login=login).first()
    #
    #     # get the project and update it
    #     # TODO: add this part
    #
    #     # return where we came from
    #     # return HTTPFound(location=came_from)
    #
    # # just give the info enough to fill the form
    return {
        'project': project
    }


@view_config(
    route_name='get_projects',
    renderer='json',
    permission='Read_Project'
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
    renderer='templates/project/page_view_project_overview.jinja2',
    permission='Read_Project'
)
@view_config(
    route_name='view_project',
    renderer='templates/project/page_view_project.jinja2',
    permission='Read_Project'
)
@view_config(
    route_name='list_assets',
    renderer='templates/asset/content_list_assets.jinja2',
    permission='Read_Asset'
)
@view_config(
    route_name='list_shots',
    renderer='templates/shot/content_list_shots.jinja2',
    permission='Read_Shot'
)
@view_config(
    route_name='list_sequences',
    renderer='templates/sequence/content_list_sequences.jinja2',
    permission='Read_Sequence'
)
@view_config(
    route_name='summarize_project',
    renderer='templates/project/content_summarize_project.jinja2',
    permission='Read_Project'
)
def view_project_related_data(request):
    """runs when viewing project related data
    """
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    project_id = request.matchdict['project_id']
    project = Project.query.filter_by(id=project_id).first()
    
    return {
        'user': user,
        'project': project
    }

@view_config(
    route_name='view_entity_nav_bar',
    renderer='templates/content_nav_bar.jinja2',
    permission='Read_Project'
)
def view_entity_nav_bar(request):
    """runs when viewing all projects
    """

    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()



    # just return all the projects
    return {
        'entity': entity

    }
