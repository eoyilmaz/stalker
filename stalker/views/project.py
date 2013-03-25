# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError

import transaction
from stalker.db import DBSession
from stalker import (User, ImageFormat, Repository, Structure, StatusList,
                     Project)

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='add_project',
    renderer='templates/project/add_project.jinja2',
    permission='Add_Project'
)
def add_project(request):
    """called when adding a project
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'add':
            # TODO: remove this later
            for param in ['name',
                          'code',
                          'image_format',
                          'repository',
                          'structure',
                          'lead',
                          'status_list']:
                if param not in request.params:
                    logger.debug('%s is not in parameters' % param)
 
            if 'name' in request.params and \
                'code' in request.params and \
                'image_format' in request.params and \
                'repository' in request.params and \
                'structure' in request.params and \
                'lead' in request.params and \
                'status_list' in request.params:
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
                
                # status list
                status_list_id = int(request.params['status_list'])
                status_list = StatusList.query\
                    .filter_by(id=status_list_id).first()

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
                        status=status_list[0],
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
    route_name='view_projects',
    renderer='templates/project/view_projects.jinja2',
    permission='View_Project'
)
def view_projects(request):
    """runs when viewing all projects
    """
    # just return all the projects
    return {
        'projects': Project.query.all()
    }


@view_config(
    route_name='edit_project',
    renderer='templates/project/edit_project.jinja2',
    permission='Edit_Project'
)
def edit_project(request):
    """runs when editing a project
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    proj_id = request.matchdict['project_id']
    proj = Project.query.filter_by(id=proj_id).first()
    
    if request.params['submitted'] == 'edit':
        #return HTTPFound(location=came_from)
        login = authenticated_userid(request)
        authenticated_user = User.query.filter_by(login=login).first()
        
        # get the project and update it
        # TODO: add this part
        
        # return where we came from
        return HTTPFound(location=came_from)
    
    # just give the info enough to fill the form
    return {
        'project': proj,
        'users': User.query.all(),
        'image_formats': ImageFormat.query.all(),
        'repositories': Repository.query.all(),
        'structures': Structure.query.all(),
        'status_lists': StatusList.query\
                            .filter_by(target_entity_type='Project')\
                            .all(),
    }


@view_config(
    route_name='get_projects',
    renderer='json',
    permission='View_Project'
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
    route_name='view_project',
    renderer='templates/project/view_project.jinja2',
    permission='View_Project'
)
@view_config(
    route_name='view_assets',
    renderer='templates/asset/view_assets.jinja2',
    permission='View_Asset'
)
@view_config(
    route_name='view_shots',
    renderer='templates/shot/view_shots.jinja2',
    permission='View_Shot'
)
@view_config(
    route_name='summarize_project',
    renderer='templates/project/summarize_project.jinja2',
    permission='View_Project'
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
