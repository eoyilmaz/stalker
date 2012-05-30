# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
from sqlalchemy import or_
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config, forbidden_view_config
import stalker


from stalker.models.auth import User
from stalker.models.formats import ImageFormat
from stalker.models.project import Project
from stalker.models.repository import Repository
from stalker.models.structure import Structure


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_stalker_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='home', renderer='templates/home.jinja2',
             permission='View_Project')
def home(request):
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    projects = Project.query().all()
    
    return {
        'stalker': stalker,
        'user': user,
        'projects': projects,
    }

@view_config(route_name='login', renderer='templates/login.jinja2')
@forbidden_view_config(renderer='templates/login.jinja2')
def login(request):
    """the login view
    """
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'
    
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        
        # need to find the user
        # check with the login_name or email attribute
        user_obj = User.query()\
            .filter(or_(User.login_name==login, User.email==login)).first()
        
        if user_obj:
            login = 'User:' + user_obj.login_name
        
        if user_obj and user_obj.check_password(password):
            headers = remember(request, login)
            return HTTPFound(
                location=came_from,
                headers=headers,
            )
        
        message = 'Wrong username or password!!!'
    
    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
        stalker=stalker
    )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(
        location=request.route_url('login'),
        headers=headers
    )

@view_config(route_name='create_project',
             renderer='templates/create_project.jinja2',
             permission='Add_Project')
def create_project(request):
    """called when creating a project
    """
    
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    
#    logger.debug('*******************************************')
#    logger.debug(request.params)
    
    if 'form.submitted' in request.params:
        if request.params['form.submitted'] == 'create':
            #login = request.params['login']
            # so create the project
            logger.debug('create clicked with this request: ' % request)
            
            return HTTPFound(location=came_from)
        else:
            return HTTPFound(location=came_from)
    
    return {
        'user': user,
        'users': User.query().all(),
        'image_formats': ImageFormat.query().all(),
        'repositories': Repository.query().all(),
        'structures': Structure.query().all(),
        'stalker': stalker,
    }

@view_config(route_name='create_image_format',
             renderer='templates/create_image_format.jinja2',
             permission='Add_ImageFormat')
def create_image_format(request):
    """called when creating an image format
    """
    
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'form.submitted' in request.params:
        if request.params['form.submitted'] == 'create':
            #login = request.params['login']
            # so create the project
            logger.debug('create clicked with this request: ' % request)
            
            return HTTPFound(location=came_from)
        else:
            return HTTPFound(location=came_from)
    
    return {
        'user': user,
        'users': User.query().all(),
        'stalker': stalker,
    }
