# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime

from sqlalchemy import or_
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config, forbidden_view_config

import transaction

import stalker
from stalker.db.session import DBSession
from stalker.models.auth import User
from stalker.models.format import ImageFormat
from stalker.models.project import Project
from stalker.models.repository import Repository
from stalker.models.structure import Structure
from stalker.models.template import FilenameTemplate
from stalker.models.type import EntityType, Type

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

@view_config(
    route_name='add_project',
    renderer='templates/add_project.jinja2',
    permission='Add_Project'
)
@view_config(
    route_name='edit_project',
    renderer='templates/add_project.jinja2',
    permission='Edit_Project'
)
def add_project(request):
    """called when creating a project
    """
    
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    
#    logger.debug('*******************************************')
#    logger.debug(request.params)
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'add':
            #login = request.params['login']
            # so create the project
            logger.debug('create clicked with this request: ' % request)
            
            # get the image format
            imf_id = int(request.params['image_format'])
            imf = ImageFormat.query().filter_by(id=imf_id).one()
            
            # get repository
            repo_id = int(request.params['repository'])
            repo = Repository.query().filter_by(id=repo_id).one()
            
            # get structure
            structure_id = int(request.params['structure_id'])
            structure = Structure.query().filter_by(id=structure_id).one()
            
            new_project = Project(
                name=request.params['name'],
                image_format=imf,
                repository=repo,
                created_by=user,
                fps=request.params['fps'],
                structure=structure,
            )
            
            return HTTPFound(location=came_from)
        elif request.params['params']:
            return HTTPFound(location=came_from)
    
    return {
        'user': user,
        'users': User.query().all(),
        'image_formats': ImageFormat.query().all(),
        'repositories': Repository.query().all(),
        'structures': Structure.query().all(),
        'stalker': stalker,
    }

@view_config(
    route_name='add_image_format',
    renderer='templates/add_image_format.jinja2',
    permission='Add_ImageFormat'
)
def add_image_format(request):
    """called when adding or editing an image format
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    
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
    
    return {
        'user': user,
        'users': User.query().all(),
        'stalker': stalker,
    }



@view_config(
    route_name='edit_image_format',
    renderer='templates/edit_image_format.jinja2',
    permission='Edit_ImageFormat'
)

def edit_image_format(request):
    """called when adding or editing an image format
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    
    imf_id = request.matchdict['imf_id']
    imf = ImageFormat.query()\
            .filter(ImageFormat.id==imf_id)\
            .one()
    
    if 'name' in request.params and \
        'width' in request.params and \
        'height' in request.params and \
        'pixel_aspect' in request.params and \
        'submitted' in request.params:
        if request.params['submitted'] == 'edit':
            with transaction.manager:
                imf.name = request.params['name']
                imf.width = int(request.params['width'])
                imf.height = int(request.params['height'])
                imf.pixel_aspect = float(request.params['pixel_aspect'])
                DBSession.add(imf)
    
    return {
        'user': user,
        'users': User.query().all(),
        'stalker': stalker,
        'image_format': imf
    }

@view_config(
    route_name='add_repository',
    renderer='templates/add_repository.jinja2',
    permission='Add_Repository'
)
@view_config(
    route_name='edit_repository',
    renderer='templates/add_repository.jinja2',
    permission='Edit_Repository'
)
def add_repository(request):
    """called when adding or editing a repository
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'name' in request.params and \
       'windows_path' in request.params and \
       'linux_path' in request.params and \
       'osx_path' in request.params:
        
        # create a new Repository and save it to the database
        with transaction.manager:
            new_repository = Repository(
                name=request.params['name'],
                windows_path=request.params['windows_path'],
                linux_path=request.params['linux_path'],
                osx_path=request.params['osx_path']
            )
            DBSession.add(new_repository)
    
    return {
        'user': user,
        'users': User.query().all(),
        'stalker': stalker,
    }

@view_config(
    route_name='add_structure',
    renderer='templates/add_structure.jinja2',
    permission='Add_Structure'
)
@view_config(
    route_name='edit_structure',
    renderer='templates/edit_structure.jinja2',
    permission='Edit_Structure'
)
def add_edit_structure(request):
    """called when adding or editing a structure
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'submit' in request.params:
        if request.params['submit'] == 'add':
            # create and add a new structure
            if 'name' in request.params and \
                'custom_template' in request.params:
                with transaction.manager:
                    # TODO: add FilenameTemplate objects later
                    new_structure = Structure(
                        name=request.params['name'],
                        custom_template=request.params['custom_template']
                    )
                    DBSession.add(new_structure)
        elif request.params['submit'] == 'edit':
            # just edit the given structure
            structure_id = request.matchdict['structure_id']
            structure = Structure.query().filter_by(id=structure_id).one()
            
            with transaction.manager:
                structure.name = request.params['name']
                structure.custom_template = request.params['custom_template']
                # TODO: update the FilenameTemplates later
                DBSession.add(structure)
    
    return {
        'user': user,
        'users': User.query().all(),
        'stalker': stalker,
        'filename_templates': FilenameTemplate.query().all()
    }

@view_config(
    route_name='add_user',
    renderer='templates/add_user.jinja2',
    permission='Add_User'
)
@view_config(
    route_name='edit_user',
    renderer='templates/edit_user.jinja2',
    permission='Edit_User'
)
def add_edit_user(request):
    """called when adding or editing a user
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'submit' in request.params:
        if request.params['submit'] == 'add':
            # create and add a new user
            if 'first_name' in request.params and \
                'last_name' in request.params and \
                'email' in request.params and \
                'password' in request.params:
                with transaction.manager:
                    new_user = User(
                        first_name=request.params['first_name'],
                        last_name=request.params['last_name'],
                        email=request.params['email'],
                        password=request.params['password']
                    )
                    DBSession.add(new_user)
        elif request.params['submit'] == 'edit':
            # just edit the given user
            user_id = request.matchdict['user_id']
            user = User.query().filter_by(id=user_id).one()
            
            with transaction.manager:
                user.first_name = request.params['first_name']
                user.last_name = request.params['last_name']
                user.email = request.params['email']
                user.password = request.params['password']
                # TODO: update the rest later
                DBSession.add(user)
    
    return {
        'user': user,
        'users': User.query().all(),
        'stalker': stalker
    }

@view_config(
    route_name='add_filename_template',
    renderer='templates/add_filename_template.jinja2',
    permission='Add_FilenameTemplate'
)
@view_config(
    route_name='edit_filename_template',
    renderer='templates/edit_filename_template.jinja2',
    permission='Edit_FilenameTemplate'
)
def add_edit_filename_template(request):
    """called when adding or editing a FilenameTemplate instance
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request).split(':')[1]
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'submit' in request.params:
        if request.params['submit'] == 'add':
            # create and add a new FilenameTemplate
            if 'name' in request.params and \
                'target_entity_type' in request.params and \
                'path' in request.params and \
                'filename' in request.params and \
                'output_path' in request.params:
                with transaction.manager:
                    new_ft = FilenameTemplate(
                        name=request.params['name'],
                        target_entity_type=\
                            request.params['target_entity_type'],
                        path=request.params['path'],
                        filename=request.params['filename']
                    )
                    DBSession.add(new_ft)
        elif request.params['submit'] == 'edit':
            # just edit the given filename_template
            ft_id = request.matchdict['filename_template_id']
            ft = FilenameTemplate.query().filter_by(id=ft_id).one()
            
            with transaction.manager:
                ft.name = request.params['name']
                ft.path = request.params['path']
                ft.filename = request.params['filename']
                ft.output_path = request.params['output_path']
                DBSession.add(ft)
    
    return {
        'user': user,
        'users': User.query().all(),
        'stalker': stalker,
        'entity_types': EntityType.query().all(),
        'filename_template_types': 
            Type.query()
                .filter_by(target_entity_type="FilenameTemplate")
                .all()
    }

