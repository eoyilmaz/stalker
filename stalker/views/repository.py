# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from pyramid.security import authenticated_userid
from pyramid.view import view_config

from stalker.db import DBSession
from stalker import User, Repository

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='add_repository',
    renderer='templates/repository/add_repository.jinja2',
    permission='Add_Repository'
)
def add_repository(request):
    """called when adding a repository
    """
    referrer = request.url
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'name' in request.params and \
       'windows_path' in request.params and \
       'linux_path' in request.params and \
       'osx_path' in request.params:
        
        # create a new Repository and save it to the database
         new_repository = Repository(
             name=request.params['name'],
             windows_path=request.params['windows_path'],
             linux_path=request.params['linux_path'],
             osx_path=request.params['osx_path'],
             created_by=user
         )
         DBSession.add(new_repository)
    
    return {}


@view_config(
    route_name='edit_repository',
    renderer='templates/repository/edit_repository.jinja2',
    permission='Edit_Repository'
)
def edit_repository(request):
    """called when editing a repository
    """
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    repo_id = request.matchdict['repository_id']
    repo = Repository.query.filter_by(id=repo_id).first()
    
    logger.debug('repo_id: %s' % repo_id)
    logger.debug('repo   : %s' % repo)
    if 'submitted' in request.params:
        logger.debug('submitted in request.params')
        logger.debug('submitted: %s ' % request.params['submitted'])
        if request.params['submitted'] == 'edit':
            if 'name' in request.params and \
               'windows_path' in request.params and \
               'linux_path' in request.params and \
               'osx_path' in request.params:
                
                logger.debug('we have all parameters')
                repo.name=request.params['name']
                repo.windows_path=request.params['windows_path']
                repo.linux_path=request.params['linux_path']
                repo.osx_path=request.params['osx_path']
                repo.updated_by=user
                
                DBSession.add(repo)
            else:
                logger.debug('there are missing parameters')
                log_param(request, 'name')
                log_param(request, 'windows_path')
                log_param(request, 'linux_path')
                log_param(request, 'osx_path')
    else:
        logger.debug('submitted NOT in request.params')
    
    return {
        'repository': repo
    }


@view_config(
    route_name='get_repositories',
    renderer='json',
    permission='View_Repository'
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
