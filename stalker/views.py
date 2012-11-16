# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime
import re

from sqlalchemy import or_
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config, forbidden_view_config
from sqlalchemy.exc import IntegrityError

import transaction

import stalker
from stalker.db.session import DBSession
from stalker import (User, ImageFormat, Project, Repository, Structure,
                     FilenameTemplate, EntityType, Type, StatusList, Status)

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

@view_config(route_name='home',
             renderer='templates/base.jinja2',
             permission='View_Project')
def home(request):
    login_name = authenticated_userid(request)
    user = User.query().filter_by(login_name=login_name).first()
    projects = Project.query().all()
    
    return {
        'stalker': stalker,
        'user': user,
        'projects': projects,
    }


@view_config(route_name='user_menu',
             renderer='templates/user_menu.jinja2')
def user_menu(request):
    login_name = authenticated_userid(request)
    user = User.query().filter_by(login_name=login_name).first()
    return {
        'stalker': stalker,
        'user': user,
    }

@view_config(route_name='projects_menu',
             renderer='templates/projects_menu.jinja2',
             permission='View_Project')
def projects_menu(request):
    return {
        'projects': Project.query().all()
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
#            login = 'User:' + user_obj.login_name
            login = user_obj.login_name
        
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
def add_project(request):
    """called when adding a project
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request)
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'add':
            #login = request.params['login']
            # so create the project
            
            with transaction.manager:
                # get the image format
                imf_id = int(request.params['image_format'])
                imf = ImageFormat.query().filter_by(id=imf_id).one()
                
                # get repository
                repo_id = int(request.params['repository'])
                repo = Repository.query().filter_by(id=repo_id).one()
                
                # get structure
                structure_id = int(request.params['structure'])
                structure = Structure.query().filter_by(id=structure_id).one()
                
                new_project = Project(
                    name=request.params['name'],
                    image_format=imf,
                    repository=repo,
                    created_by=user,
                    fps=request.params['fps'],
                    structure=structure,
                )
                
                DBSession.add(new_project)
        
        # do not return anything
        # or maybe we should return to where we came from
        return HTTPFound(location=came_from)
   
    # just one wants to see the add project form
    return {
        'user': user,
        'users': User.query().all(),
        'image_formats': ImageFormat.query().all(),
        'repositories': Repository.query().all(),
        'structures': Structure.query().all(),
        'status_lists': StatusList.query()\
                            .filter_by(target_entity_type='Project')\
                            .all(),
    }

@view_config(
    route_name='view_project',
    renderer='templates/view_project.jinja2',
    permission='View_Project'
)
def view_project(request):
    """runs when viewing a project
    """
    # just return the project
    proj_id = request.matchdict['project_id']
    proj = Project.query().filter_by(id=proj_id).first()
    return {
        'project': proj
    }

@view_config(
    route_name='view_projects',
    renderer='templates/view_projects.jinja2',
    permission='View_Project'
)
def view_projects(request):
    """runs when viewing all projects
    """
    # just return all the projects
    return {
        'projects': Project.query().all()
    }


@view_config(
    route_name='edit_project',
    renderer='templates/edit_project.jinja2',
    permission='Edit_Project'
)
def edit_project(request):
    """runs when editing a project
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    proj_id = request.matchdict['project_id']
    proj = Project.query().filter_by(id=proj_id).first()
    
    
    
    if request.params['submitted'] == 'edit':
        #return HTTPFound(location=came_from)
        login_name = authenticated_userid(request)
        authenticated_user = User.query().filter_by(login_name=login_name).first()
        
        # get the project and update it
        # TODO: add this part
        
        # return where we came from
        return HTTPFound(location=came_from)
    
    # just give the info enough to fill the form
    return {
        'project': proj,
        'users': User.query().all(),
        'image_formats': ImageFormat.query().all(),
        'repositories': Repository.query().all(),
        'structures': Structure.query().all(),
        'status_lists': StatusList.query()\
                            .filter_by(target_entity_type='Project')\
                            .all(),
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
    
    login_name = authenticated_userid(request)
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
    
    return {}



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
    
    login_name = authenticated_userid(request)
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
                imf.updated_by = user
                DBSession.add(imf)
    
    return {'image_format': imf}

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
def add_edit_repository(request):
    """called when adding or editing a repository
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request)
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
                osx_path=request.params['osx_path'],
                created_by=user
            )
            DBSession.add(new_repository)
    
    return {}

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
    
    login_name = authenticated_userid(request)
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'submitted' in request.params:
        logger.debug('"submitted" in request.params')
        if request.params['submitted'] == 'add':
            logger.debug('Adding a new structure')
            # create and add a new structure
            if 'name' in request.params and \
                'custom_template' in request.params and \
                'filename_templates' in request.params:
                logger.debug('all the parameters are in place')
                with transaction.manager:
                    # get FilenameTemplates
                    ft_ids = [
                        int(re.sub(r"[^0-9]+", "", ft_id))
                            for ft_id in 
                                request.params['filename_templates'].split(',')
                    ]
                    
                    fts = [
                        FilenameTemplate.query().filter_by(id=ft_id).first()
                        for ft_id in ft_ids
                    ]
                    
                    # create structure
                    new_structure = Structure(
                        name=request.params['name'],
                        custom_template=str(request.params['custom_template']),
                        templates=fts,
                        created_by=user,
                    )
                    DBSession.add(new_structure)
            else:
                logger.debug('there are missing parameters in request')
        elif request.params['submitted'] == 'edit':
            # just edit the given structure
            structure_id = request.matchdict['structure_id']
            structure = Structure.query().filter_by(id=structure_id).one()
            
            with transaction.manager:
                structure.name = request.params['name']
                structure.custom_template = request.params['custom_template']
                structure.updated_by = user
                # TODO: update the FilenameTemplates later
                DBSession.add(structure)
    else:
        logger.debug('submitted is not in request.params')
    
    f_templates = FilenameTemplate.query().all()
    logger.debug('we got %i FilenameTemplates' % len(f_templates))
    for f_template in f_templates:
        logger.debug('FilenameTemplate: %s' %f_template.name)
    
    return {
        'filename_templates': f_templates
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
    
    login_name = authenticated_userid(request)
    logged_user = User.query().filter_by(login_name=login_name).first()
    
    if 'submitted' in request.params:
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
                        password=request.params['password'],
                        created_by=logged_user
                    )
                    DBSession.add(new_user)
        elif request.params['submitted'] == 'edit':
            # just edit the given user
            user_id = request.matchdict['user_id']
            user = User.query().filter_by(id=user_id).one()
            
            with transaction.manager:
                user.first_name = request.params['first_name']
                user.last_name = request.params['last_name']
                user.email = request.params['email']
                user.password = request.params['password']
                user.updated_by = logged_user
                # TODO: update the rest later
                DBSession.add(user)
    
    return {
        'user': logged_user,
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
    
    login_name = authenticated_userid(request)
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'add':
            logger.debug('adding a new FilenameTemplate')
            # create and add a new FilenameTemplate
            
            
            # TODO: remove this later
            for param in ['name',
                          'target_entity_type',
                          'type',
                          'path',
                          'filename',
                          'output_path']:
                if param not in request.params:
                    logger.debug('%s is not in parameters' % param)
            
            if 'name' in request.params and \
                'target_entity_type' in request.params and \
                'type' in request.params and\
                'path' in request.params and \
                'filename' in request.params and \
                'output_path' in request.params:
                
                logger.debug('we got all the parameters')
                
                # get the typ
                type_ = Type.query()\
                    .filter_by(id=request.params['type_id'])\
                    .first()
                
                try:
                    new_ft = FilenameTemplate(
                        name=request.params['name'],
                        target_entity_type=\
                            request.params['target_entity_type'],
                        type=type_,
                        path=request.params['path'],
                        filename=request.params['filename'],
                        created_by=user,
                    )
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_ft)
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                    else:
                        logger.debug('flusing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding FilenameTemplate')
            else:
                logger.debug('there are missing parameters')
        elif request.params['submitted'] == 'edit':
            logger.debug('editing a Filename Template')
            # just edit the given filename_template
            ft_id = request.matchdict['filename_template_id']
            ft = FilenameTemplate.query().filter_by(id=ft_id).one()
            
            with transaction.manager:
                ft.name = request.params['name']
                ft.path = request.params['path']
                ft.filename = request.params['filename']
                ft.output_path = request.params['output_path']
                ft.updated_by = user
                DBSession.add(ft)
    
            logger.debug('finished editing FilenameTemplate')
    
    return {
        'entity_types': EntityType.query().all(),
        'filename_template_types': 
            Type.query()
                .filter_by(target_entity_type="FilenameTemplate")
                .all()
    }

@view_config(
    route_name='add_status',
    renderer='templates/add_status.jinja2',
    permission='Add_Status'
)
@view_config(
    route_name='edit_status',
    renderer='templates/edit_status.jinja2',
    permission='Edit_Status'
)
def add_edit_status(request):
    """called when adding or editing a Status
    """
    
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request)
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'add':
            logger.debug('adding a new Status')
            # create and add a new Status
            
            if 'name' in request.params and \
                'code' in request.params:
                
                logger.debug('we got all the parameters')
                
                try:
                    new_status = Status(
                        name=request.params['name'],
                        code=request.params['code'],
                        created_by=user,
                    )
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_status)
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                    else:
                        logger.debug('flusing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding Status')
            else:
                logger.debug('there are missing parameters')
            
            # TODO: place a return statement here
        elif request.params['submitted'] == 'edit':
            logger.debug('editing a Status')
            # just edit the given Status
            st_id = request.matchdict['status_id']
            status = Status.query().filter_by(id=st_id).first()
            
            with transaction.manager:
                status.name = request.params['name']
                status.code = request.params['code']
                status.updated_by = user
                DBSession.add(status)
            
            logger.debug('finished editing Status')
            
            # TODO: place a return statement here
    
    return {}

@view_config(
    route_name='add_status_list',
    renderer='templates/add_status_list.jinja2',
    permission='Add_StatusList'
)
@view_config(
    route_name='edit_status_list',
    renderer='templates/edit_status_list.jinja2',
    permission='Edit_StatusList'
)
def add_edit_status_list(request):
    """called when adding or editing a StatusList
    """
    
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login_name = authenticated_userid(request)
    user = User.query().filter_by(login_name=login_name).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'add':
            logger.debug('adding a new StatusList')
            # create and add a new StatusList
            
            if 'name' in request.params and \
                'target_entity_type' in request.params and \
                'statuses' in request.params:
                
                logger.debug('we got all the parameters')
                
                # get statuses
                st_ids = [
                    int(re.sub(r"[^0-9]+", "", st_id))
                        for st_id in 
                            request.params['statuses'].split(',')
                ]
                
                statuses = [
                    Status.query().filter_by(id=st_id).first()
                    for st_id in st_ids
                ]
                 
                try:
                    new_status_list = StatusList(
                        name=request.params['name'],
                        target_entity_type=\
                            request.params['target_entity_type'],
                        statuses=statuses,
                        created_by=user,
                    )
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_status_list)
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                    else:
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding StatusList')
            else:
                logger.debug('there are missing parameters')
        elif request.params['submitted'] == 'edit':
            logger.debug('editing a StatusList')
            # just edit the given StatusList
            st_id = request.matchdict['status_list_id']
            status_list = StatusList.query().filter_by(id=st_id).first()
            
            # get statuses
            st_ids = [
                int(re.sub(r"[^0-9]+", "", st_id))
                    for st_id in 
                        request.params['statuses'].split(',')
            ]
            
            statuses = [
                Status.query().filter_by(id=st_id).first()
                for st_id in st_ids
            ]
            
            with transaction.manager:
                status_list.name = request.params['name']
                status_list.statuses = statuses
                status_list.updated_by = user
                DBSession.add(status_list)
    
                logger.debug('finished editing StatusList')
    
    return {
        'entity_types': EntityType.query().filter_by(statusable=True).all(),
        'statuses': Status.query().all()
    }
