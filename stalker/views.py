# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime

from sqlalchemy import or_
from pyramid.httpexceptions import HTTPFound, HTTPServerError
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config, forbidden_view_config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import DetachedInstanceError

import transaction

import stalker
from stalker.db.session import DBSession
from stalker import (User, ImageFormat, Project, Repository, Structure,
                     FilenameTemplate, EntityType, Type, StatusList, Status,
                     Asset, Shot, Sequence, Department, Group,
                     Tag, Task)

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

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


def log_param(request, param):
    if param in request.params:
        logger.debug('%s: %s' % (param, request.params[param]))
    else:
        logger.debug('%s not in params' % param)


@view_config(route_name='home',
            renderer='templates/base.jinja2')
@view_config(route_name='me_menu',
             renderer='templates/me_menu.jinja2')
@view_config(route_name='user_home',
             renderer='templates/user_home.jinja2')
def home(request):
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    projects = Project.query.all()
    return {
        'stalker': stalker,
        'user': user,
        'projects': projects,
    }

@forbidden_view_config(
    renderer='templates/no_permission.jinja2'
)
def forbidden(request):
    """runs when user has no permission for the requested page
    """
    return {}

@view_config(
    route_name='user_menu',
    renderer='templates/user_menu.jinja2'
)
def user_menu(request):
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    return {
        'stalker': stalker,
        'user': user,
    }

@view_config(route_name='create_menu',
             renderer='templates/create_menu.jinja2')
def create_menu(request):
    return {}

@view_config(
    route_name='login',
    renderer='templates/login.jinja2'
)
def login(request):
    """the login view
    """
    logger.debug('login start')
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
        # check with the login or email attribute
        user_obj = User.query\
            .filter(or_(User.login==login, User.email==login)).first()

        if user_obj:
            login = user_obj.login

        if user_obj and user_obj.check_password(password):
            headers = remember(request, login)
            return HTTPFound(
                location=came_from,
                headers=headers,
            )

        message = 'Wrong username or password!!!'

    logger.debug('login end')
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
    renderer='templates/view_projects.jinja2',
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
    renderer='templates/edit_project.jinja2',
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
    route_name='add_image_format',
    renderer='templates/add_image_format.jinja2',
    permission='Add_ImageFormat'
)
def add_image_format(request):
    """called when adding or editing an image format
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
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
    """called when editing an image format
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    imf_id = request.matchdict['imf_id']
    imf = ImageFormat.query\
            .filter(ImageFormat.id==imf_id)\
            .first()
    
    if 'submitted' in request.params:
        if 'name' in request.params and \
            'width' in request.params and \
            'height' in request.params and \
            'pixel_aspect' in request.params and \
            'submitted' in request.params:
            if request.params['submitted'] == 'edit':
                imf.name = request.params['name']
                imf.width = int(request.params['width'])
                imf.height = int(request.params['height'])
                imf.pixel_aspect = float(request.params['pixel_aspect'])
                imf.updated_by = user
                DBSession.add(imf)
                #try:
                #    transaction.commit()
                #except (IntegrityError, DetachedInstanceError) as e:
                #    logging.debug(e)
                #    transaction.abort()
                #else:
                #    DBSession.flush()
    
    return {'image_format': imf}

@view_config(
    route_name='edit_structure',
    renderer='templates/edit_structure.jinja2',
    permission='Edit_Structure'
)
def edit_structure(request):
    """called when editing a structure
    """
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    structure_id = request.matchdict['structure_id']
    structure = Structure.query.filter_by(id=structure_id).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'edit':
            if 'name' in request.params and \
                'custom_template' in request.params and \
                'filename_templates' in request.params:
                    
                    # get all FilenameTemplates
                    ft_ids = [
                        int(ft_id)
                        for ft_id in request.POST.getall('filename_templates')
                    ]
                    
                    fts = [
                        FilenameTemplate.query.filter_by(id=ft_id).first()
                        for ft_id in ft_ids
                    ]
                    
                    # edit structure
                    structure.name = request.params['name']
                    structure.templates = fts
                    structure.custom_template = \
                        request.params['custom_template']
                    structure.updated_by = user
                    
                    DBSession.add(structure)
                    # TODO: update date_updated
                        
    return {'structure': structure}


@view_config(
    route_name='add_repository',
    renderer='templates/add_repository.jinja2',
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
    renderer='templates/edit_repository.jinja2',
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
    route_name='add_structure',
    renderer='templates/add_structure.jinja2',
    permission='Add_Structure'
)
def add_structure(request):
    """called when adding a structure
    """
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
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
                    # get all FilenameTemplates
                    ft_ids = [
                        int(ft_id)
                        for ft_id in request.POST.getall('filename_templates')
                    ]
                    
                    fts = [
                        FilenameTemplate.query.filter_by(id=ft_id).first()
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
    else:
        logger.debug('submitted is not in request.params')
    
    return {
        'filename_templates': FilenameTemplate.query.all()
    }

@view_config(
    route_name='add_user',
    renderer='templates/add_user.jinja2',
    permission='Add_User'
)
def add_user(request):
    """called when adding a User
    """
    login = authenticated_userid(request)
    logged_user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        logger.debug('submitted in params')
        if request.params['submitted'] == 'add':
            logger.debug('submitted value is: add')
            # create and add a new user
            if 'name' in request.params and \
               'login' in request.params and \
               'email' in request.params and \
               'password' in request.params:
                
                # Departments
                departments = []
                if 'department_ids' in request.params:
                    dep_ids = [
                        int(dep_id)
                        for dep_id in request.POST.getall('department_ids')
                    ]
                    departments = Department.query.filter(
                                    Department.id.in_(dep_ids)).all()
                
                # Groups
                groups = []
                if 'group_ids' in request.params:
                    grp_ids = [
                        int(grp_id)
                        for grp_id in request.POST.getall('group_ids')
                    ]
                    groups = Group.query.filter(
                                    Group.id.in_(grp_ids)).all()
                
                # Tags
                tags = []
                if 'tag_ids' in request.params:
                    tag_ids = [
                        int(tag_id)
                        for tag_id in request.POST.getall('tag_ids')
                    ]
                    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
                
                logger.debug('creating new user')
                new_user = User(
                    name=request.params['name'],
                    login=request.params['login'],
                    email=request.params['email'],
                    password=request.params['password'],
                    created_by=logged_user,
                    departments=departments,
                    groups=groups,
                    tags=tags
                )
                
                logger.debug('adding new user to db')
                DBSession.add(new_user)
                logger.debug('added new user successfully')
            else:
                logger.debug('not all parameters are in request.params')
                log_param(request, 'name')
                log_param(request, 'login')
                log_param(request, 'email')
                log_param(request, 'password')
                
        #elif request.params['submitted'] == 'edit':
        #    # just edit the given user
        #    user_id = request.matchdict['user_id']
        #    user = User.query.filter_by(id=user_id).one()
        #    
        #    with transaction.manager:
        #        user.name = request.params['name']
        #        user.email = request.params['email']
        #        user.password = request.params['password']
        #        user.updated_by = logged_user
        #        # TODO: update the rest later
        #        DBSession.add(user)
        else:
            logger.debug('submitted value is not add but: %s' %
                         request.params['submitted'])
    else:
        logger.debug('submitted is not among parameters')
        for key in request.params.keys():
            logger.debug('request.params[%s]: %s' % (key, request.params[key]))
    
    return {
        'user': logged_user,
    }

@view_config(
    route_name='edit_user',
    renderer='templates/edit_user.jinja2',
    permission='Edit_User'
)
def edit_user(request):
    """called when editing a user
    """
    pass

@view_config(
    route_name='add_filename_template',
    renderer='templates/add_filename_template.jinja2',
    permission='Add_FilenameTemplate'
)
def add_filename_template(request):
    """called when adding a FilenameTemplate instance
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'add':
            logger.debug('adding a new FilenameTemplate')
            # create and add a new FilenameTemplate
            
            # TODO: remove this later
            for param in ['name',
                          'target_entity_type',
                          'type_id',
                          'path',
                          'filename',
                          'output_path']:
                if param not in request.params:
                    logger.debug('%s is not in parameters' % param)
            
            if 'name' in request.params and \
                'target_entity_type' in request.params and \
                'type_id' in request.params and\
                'path' in request.params and \
                'filename' in request.params and \
                'output_path' in request.params:
                
                logger.debug('we got all the parameters')
                
                # get the typ
                type_ = Type.query\
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
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding FilenameTemplate')
            else:
                logger.debug('there are missing parameters')
    return {
        'entity_types': EntityType.query.all(),
        'filename_template_types': 
            Type.query
                .filter_by(target_entity_type="FilenameTemplate")
                .all()
    }

@view_config(
    route_name='edit_filename_template',
    renderer='templates/edit_filename_template.jinja2',
    permission='Edit_FilenameTemplate'
)
def edit_filename_template(request):
    """called when editing a FilenameTemplate instance
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'edit':
            logger.debug('editing a Filename Template')
            # just edit the given filename_template
            ft_id = request.matchdict['filename_template_id']
            ft = FilenameTemplate.query.filter_by(id=ft_id).first()
            
            ft.name = request.params['name']
            ft.path = request.params['path']
            ft.filename = request.params['filename']
            ft.output_path = request.params['output_path']
            ft.updated_by = user
            
            DBSession.add(ft)
            try:
                transaction.commit()
            except (IntegrityError, DetachedInstanceError) as e:
                logging.debug(e)
                transaction.abort()
            else:
                DBSession.flush()
        
        logger.debug('finished editing FilenameTemplate')
 
     
    return {}

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
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'add':
            logger.debug('adding a new Status')
            # create and add a new Status
            
            if 'name' in request.params and \
                'code' in request.params and \
                'bg_color' in request.params and \
                'fg_color' in request.params:
                
                logger.debug('we got all the parameters')
                
                try:
                    # get colors
                    bg_color = int(request.params['bg_color'][1:], 16)
                    fg_color = int(request.params['fg_color'][1:], 16)
                    new_status = Status(
                        name=request.params['name'],
                        code=request.params['code'],
                        fg_color=fg_color,
                        bg_color=bg_color,
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
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding Status')
            else:
                logger.debug('there are missing parameters')
                logger.debug(request.params)
            
            # TODO: place a return statement here
        elif request.params['submitted'] == 'edit':
            logger.debug('editing a Status')
            # just edit the given Status
            st_id = request.matchdict['status_id']
            status = Status.query.filter_by(id=st_id).first()
            
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
    route_name='add_status_list_for',
    renderer='templates/add_status_list.jinja2',
    permission='Add_StatusList'
)
def add_status_list(request):
    """called when adding or editing a StatusList
    """
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
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
                    int(st_id)
                    for st_id in request.POST.getall('statuses')
                ]
                
                statuses = Status.query.filter(Status.id.in_(st_ids)).all()
                
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
                    # TODO: This is just a test for HTTPExceptions, do it properly later!
                    DBSession.add(new_status_list)  
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                        http_error = HTTPServerError()
                        http_error.explanation = e.message
                        return(http_error)
                    else:
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding StatusList')
            else:
                logger.debug('there are missing parameters')
    
    target_entity_type = request.matchdict.get('target_entity_type')
    
    return {
        'target_entity_type': target_entity_type,
        'entity_types': EntityType.query.filter_by(statusable=True).all(),
        'statuses': Status.query.all()
    }


@view_config(
    route_name='edit_status_list',
    renderer='templates/edit_status_list.jinja2',
    permission='Edit_StatusList'
)
def edit_status_list(request):
    """called when editing a StatusList
    """
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    status_list_id = request.matchdict['status_list_id']
    status_list = StatusList.query.filter_by(id=status_list_id).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'edit':
            logger.debug('editing a StatusList')
            # just edit the given StatusList
            
            # get statuses
            logger.debug("request.params['statuses']: %s" % 
                                                request.params['statuses'])
            st_ids = [
                int(st_id)
                for st_id in request.POST.getall('statuses')
            ]
            
            statuses = Status.query.filter(Status.id.in_(st_ids)).all()
            
            logger.debug("statuses: %s" % statuses)
            
            status_list.name = request.params['name']
            status_list.statuses = statuses
            status_list.updated_by = user
            
            DBSession.add(status_list)
    
    return {
        'status_list': status_list,
    }

@view_config(
    route_name='add_asset',
    renderer='add_asset.jinja2',
    permission='Add_Asset'
)
def add_asset(request):
    """runs when adding a new Asset instance
    """
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        logger.debug('request.params["submitted"]: %s' % request.params['submitted'])
        
        if request.params['submitted'] == 'add':
            
            if 'name' in request.params and \
               'code' in request.params and \
               'description' in request.params and \
               'type_name' in request.params and \
               'status_list_id' in request.params and \
               'status_id' in request.params:
                
                logger.debug('request.params["name"]: %s' %
                             request.params['name'])
                logger.debug('request.params["code"]: %s' %
                             request.params['name'])
                logger.debug('request.params["description"]: %s' %
                             request.params['description'])
                # logger.debug('request.params["project_id"]: %s' %
                #              request.params['project_id'])
                logger.debug('request.params["type_name"]: %s' %
                             request.params['type_name'])
                logger.debug('request.params["status_list_id"]: %s' %
                             request.params['status_list_id'])
                logger.debug('request.params["status_id"]: %s' %
                             request.params['status_id'])
                
                project_id = request.matchdict['project_id']
                
                # type will always return with a type name
                type_name = request.params['type_name']
                
                project = Project.query.filter_by(id=project_id).first()
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
                
                # get the status_list
                status_list = StatusList.query.filter_by(
                    target_entity_type='Asset'
                ).first()
                
                logger.debug('status_list: %s' % status_list)
                
                # there should be a status_list
                if status_list is None:
                    return HTTPServerError(
                        detail='No StatusList found'
                    )
                
                status_id = int(request.params['status_id'])
                logger.debug('status_id: %s' % status_id)
                status = Status.query.filter_by(id=status_id).first()
                logger.debug('status: %s' % status)
                
#                logger.debug('status: %s' % status)
#                logger.debug('status_list: %s' % status_list)
#                logger.debug('status in status_list: %s' % status in status_list)
                
                # get the info
                try:
                    logger.debug('*****************************')
                    logger.debug('code: %s' % request.params['code'])
                    new_asset = Asset(
                        name=request.params['name'],
                        code=request.params['code'],
                        description=request.params['description'],
                        project=project,
                        type=type_,
                        status_list=status_list,
                        status=status,
                        created_by=logged_in_user
                    )
                    
                    logger.debug('new_asset.status: ' % new_asset.status)
                    
                    #DBSession.add(new_asset)
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_asset)
                    #try:
                    #    transaction.commit()
                    #except IntegrityError as e:
                    #    logger.debug(e.message)
                    #    transaction.abort()
                    #else:
                    #    logger.debug('flushing the DBSession, no problem here!')
                    #    DBSession.flush()
                    #    logger.debug('finished adding Asset')
            else:
                logger.debug('there are missing parameters')
                def get_param(param):
                    if param in request.params:
                        logger.debug('%s: %s' % (param, request.params[param]))
                    else:
                        logger.debug('%s not in params' % param)
                get_param('name')
                get_param('code')
                get_param('description')
                get_param('project_id')
                get_param('type_name')
                get_param('status_list_id')
                get_param('status_id')

    project = Project.query.filter_by(id=request.matchdict['project_id']).first()

    return {
        'project': project,
        'projects': Project.query.all(),
        'types': Type.query.filter_by(target_entity_type='Asset').all(),
        'status_list':
            StatusList.query.filter_by(target_entity_type='Asset').first()
    }

@view_config(
    route_name='view_asset',
    renderer='view_asset.jinja2'
)
def view_asset(request):
    """runs when viewing an asset
    """

    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()

    asset_id = request.matchdict['asset_id']
    asset = Asset.query.filter_by(id=asset_id).first()

    return {
        'user': logged_in_user,
        'asset': asset
    }

@view_config(
    route_name='add_sequence',
    renderer='add_sequence.jinja2',
    permission='Add_Sequence'
)
def add_sequence(request):
    """runs when adding a new sequence
    """
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        logger.debug('request.params["submitted"]: %s' % request.params['submitted'])
        
        if request.params['submitted'] == 'add':
            
            if 'name' in request.params and \
               'code' in request.params and \
               'description' in request.params and \
               'project_id' in request.params and \
               'status_list_id' in request.params and \
               'status_id' in request.params:
                
                project_id = request.params['project_id']
                project = Project.query.filter_by(id=project_id).first()
                
                # get the status_list
                status_list = StatusList.query.filter_by(
                    id=int(request.params['status_list_id'])
                ).first()
                
                # there should be a status_list
                if status_list is None:
                    return HTTPServerError(
                        detail='No StatusList found'
                    )
                
                status_id = int(request.params['status_id'])
                status = Status.query.filter_by(id=status_id).first()
                
                try:
                    new_sequence = Sequence(
                        name=request.params['name'],
                        code=request.params['code'],
                        description=request.params['description'],
                        project=project,
                        status_list=status_list,
                        status=status,
                        created_by=logged_in_user,
                    )
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_sequence)
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                    else:
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding Sequence')
            else:
                logger.debug('there are missing parameters')
    
    return {
        'projects': Project.query.all(),
        'types': Type.query.filter_by(target_entity_type='Sequence').all(),
        'status_list':
            StatusList.query.filter_by(target_entity_type='Sequence').first()
    }


@view_config(
    route_name='edit_sequence',
    renderer='templates/edit_sequence.jinja2',
    permission='Edit_Sequence'
)
def edit_sequence(request):
    """runs when editing a sequence
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    sequence_id = request.matchdict['sequence_id']
    sequence = Sequence.query.filter_by(id=sequence_id).first()
    
    if request.params['submitted'] == 'edit':
        login = authenticated_userid(request)
        authenticated_user = User.query.filter_by(login=login).first()
        
        # get the sequence and update it
        # TODO: add this part
        
        # return where we came from
        return HTTPFound(location=came_from)
    
    # just give the info enough to fill the form
    return {
        'sequence': sequence,
        'users': User.query.all(),
        'status_lists': StatusList.query\
                            .filter_by(target_entity_type='Sequence')\
                            .all(),
    }


@view_config(
    route_name='add_shot',
    renderer='add_shot.jinja2',
    permission='Add_Shot'
)
def add_shot(request):
    """runs when adding a new shot
    """
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        logger.debug('request.params["submitted"]: %s' % request.params['submitted'])
        
        if request.params['submitted'] == 'add':
            if 'name' in request.params and \
               'code' in request.params and  \
               'sequence_id' in request.params and \
               'status_list_id' in request.params and \
               'status_id' in request.params:
                
                sequence_id = request.params['sequence_id']
                sequence = Sequence.query.filter_by(id=sequence_id).first()
                
                # get the status_list
                status_list = StatusList.query.filter_by(
                    id=request.params["status_list_id"]
                ).first()
                
                # there should be a status_list
                if status_list is None:
                    return HTTPServerError(
                        detail='No StatusList found'
                    )
                
                status_id = int(request.params['status_id'])
                status = Status.query.filter_by(id=status_id).first()
                
                # get the info
                try:
                    new_shot = Shot(
                        name=request.params['name'],
                        code=request.params['code'],
                        sequence=sequence,
                        status_list=status_list,
                        status=status,
                        created_by=logged_in_user
                    )
                    
                    DBSession.add(new_shot)
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_shot)
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                    else:
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding Shot')
            else:
                logger.debug('there are missing parameters')
                def get_param(param):
                    if param in request.params:
                        logger.debug('%s: %s' % (param, request.params[param]))
                    else:
                        logger.debug('%s not in params' % param)
                get_param('project_id')

    project = Project.query.filter_by(id=request.matchdict['project_id']).first()

    return {
        'project': project,
        'projects': Project.query.all(),
        'status_list':
            StatusList.query.filter_by(target_entity_type='Shot').first()
    }

@view_config(
    route_name='get_assets',
    renderer='json',
    permission='View_Asset'
)
def get_assets(request):
    """returns all the Assets of a given Project
    """
    proj_id = request.matchdict['project_id']
    return [
        {
            'id': asset.id,
            'name': asset.name,
            'type': asset.type.name,
            'status': asset.status.name,
            'user_id': asset.created_by.id,
            'user_link': '<a href="%s">%s</a>' %
                         ('view/user/%i' % asset.created_by.id,
                          asset.created_by.name),
            'user_name': asset.created_by.name,
            'description': asset.description
        }
        for asset in Asset.query.filter_by(project_id=proj_id).all()
    ]

@view_config(
    route_name='get_filename_templates',
    renderer='json',
    permission='View_FilenameTemplate'
)
def get_filename_templates(request):
    """returns all the FilenameTemplates in the database
    """
    return [
        {
            'id': ft.id,
            'name': ft.name,
            'target_entity_type': ft.target_entity_type,
            'type': ft.type.name
        }
        for ft in FilenameTemplate.query.all()
    ]

@view_config(
    route_name='get_image_formats',
    renderer='json',
    permission='View_ImageFormat'
)
def get_image_formats(request):
    """returns all the image formats in the database
    """
    return [
        {
            'id': imf.id,
            'name': imf.name,
            'width': imf.width,
            'height': imf.height,
            'pixel_aspect': imf.pixel_aspect
        }
        for imf in ImageFormat.query.all()
    ]

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

@view_config(
    route_name='get_sequences',
    renderer='json',
    permission='View_Sequence'
)
def get_sequences(request):
    """returns the related sequences of the given project as a json data
    """
    project_id = request.matchdict['project_id']
    project = Project.query.filter_by(id=project_id).first()
    return [
            {'id': sequence.id, 'name': sequence.name}
            for sequence in project.sequences
    ]

@view_config(
    route_name='get_shots',
    renderer='json',
    permission='View_Shot'
)
def get_shots(request):
    """returns all the Shots of the given Project
    """
    project_id = request.matchdict['project_id']
#    project = Project.query.filter_by(id=project_id).first()
    return [
        {
            'id': shot.id,
            'name': shot.name,
            'sequence': shot.sequence.name,
            'status': shot.status.name,
            'user_name': shot.created_by.name
        }
        for shot in Shot.query\
            .join(Sequence, Shot.sequence_id==Sequence.id)
            .join(Project, Sequence.project_id==Project.id)
            .filter(Project.id==project_id)
            .all()
    ]

@view_config(
    route_name='get_statuses',
    renderer='json',
    permission='View_Status'
)
def get_statuses(request):
    """returns all the Statuses in the database
    """
    return [
        {
            'id': status.id,
            'name': status.name,
            'code': status.code
        }
        for status in Status.query.all()
    ]

@view_config(
    route_name='get_statuses_of',
    renderer='json',
    permission='View_Status'
)
def get_statuses_of(request):
    """returns the Statuses of given StatusList
    """
    status_list_id = request.matchdict['status_list_id']
    status_list = StatusList.query.filter_by(id=status_list_id).first()
    return [
        {
            'id': status.id,
            'name': status.name + " (" + status.code+ ")"
        }
        for status in status_list.statuses
    ]

@view_config(
    route_name='get_status_lists',
    renderer='json',
    permission='View_StatusList'
)
def get_status_lists(request):
    """returns all the StatusList instances in the databases
    """
    return [
        {
            'id': status_list.id,
            'name': status_list.name,
        }
        for status_list in StatusList.query.all()
    ]

@view_config(
    route_name='get_status_lists_for',
    renderer='json',
    permission='View_StatusList'
)
def get_status_lists_for(request):
    """returns all the StatusList for a specific target_entity_type
    """
    return [
        {
            'id': status_list.id,
            'name': status_list.name,
        }
        for status_list in StatusList.query
            .filter_by(target_entity_type=request.matchdict['target_entity_type'])
            .all()
    ]

@view_config(
    route_name='get_structures',
    renderer='json',
    permission='View_Structure'
)
def get_structures(request):
    """returns all the structures in the database
    """
    return [
        {
            'id': structure.id,
            'name': structure.name
        }
        for structure in Structure.query.all()
    ]

def convert_to_depend_index(task, tasks):
    """converts the given task and its dependencies to the format suitable
    for jQueryGantt's depends input
    
    :param task: A Stalker Task
    
    :param [] tasks: A list of Stalker Tasks
    """
    depends = ''
    for dependent_task in task.depends:
        # find the index of the task in the given tasks
        try:
            i = tasks.index(dependent_task)
        except ValueError:
            pass
        else:
            depends += ", %i" % i
    if depends.startswith(','):
        logger.debug('converted to depends: %s' % depends[1:])
        return depends[1:]
    else:
        return ''

def convert_to_jquery_gantt_task_format(tasks):
    """Converts the given tasks to the jQuery Gantt compatible json format.
    
    :param tasks: List of Stalker Tasks.
    :return: json compatible dictionary
    """
    return {
        'tasks' : [
            {
                'id': task.id,
                'name': '%s' % task.name,
                'code': task.id,
                'level': 0,
                'status': 'STATUS_ACTIVE',
                'start': int(task.start.strftime('%s')) * 1000,
                'duration': task.duration.days,
                'end': int(task.end.strftime('%s')) * 1000,
                'depends': convert_to_depend_index(task, tasks),
                'description': task.description,
                'assigs': [
                    {
                        'resourceId': resource.id,
                        'id': resource.id
                    } for resource in task.resources
                ]
            }
            for task in tasks
        ],
        'resources' : [{
            'id': resource.id,
            'name': resource.name
        } for resource in User.query.all()],
        "canWrite": 1,
        "canWriteOnParent": 1
    }

def update_with_jquery_gantt_task_data(json_data):
    """updates the given tasks in database
    
    :param data: jQueryGantt produced json string
    """
    
    logger.debug(json_data)
    import json
    data = json.loads(json_data)
    
    # Updated Tasks
    for task_data in data['tasks']:
        task_id = task_data['id']
        task_name = task_data['name']
        task_start = task_data['start']
        task_duration = task_data.get('duration', 0)
        task_resource_ids = [resource_data['resourceId']
                             for resource_data in task_data['assigs']]
        task_description = task_data.get('description', '')
        
        # task_depend_ids : " 2, 3, 5, 6:3, 12" these are the index numbers of
        # the task in the Gantt chart, be carefull it is not the id of the task
        task_depend_ids = []
        if len(task_data.get('depends', [])):
            for index_str in task_data['depends'].split(','):
                index = int(index_str.split(':')[0])
                dependent_task_id = data['tasks'][index]['id']
                task_depend_ids.append(dependent_task_id)
        
        # get the task itself
        if not isinstance(task_id, basestring): 
            # update task
            task = Task.query.filter(Task.id==task_id).first()
        elif task_id.startswith('tmp_'):
            # create a new Task
            task = Task()
        
        # update it
        if task:
            task.name = task_name
            task.start = datetime.date.fromtimestamp(task_start/1000)
            task.duration = datetime.timedelta(task_duration)
            
            resources = User.query.filter(User.id.in_(task_resource_ids)).all()
            task.resources = resources
            
            task.description = task_description
            
            task_depends = Task.query.filter(Task.id.in_(task_depend_ids)).all()
            task.depends = task_depends
            DBSession.add(task)
    
    # Deleted tasks
    deleted_tasks = Task.query.filter(Task.id.in_(data['deletedTaskIds'])).all()
    for task in deleted_tasks:
        DBSession.delete(task)
    
    # create new tasks
    
    
    # transaction will handle the commit don't bother doing anything
 
@view_config(
    route_name='edit_tasks',
    renderer='json'
)
def edit_tasks(request):
    """edits the given tasks with the given JSON data
    """
    
    # get the data
    data = request.params['prj']
    if data:
        update_with_jquery_gantt_task_data(data)
    
    return {}

@view_config(
    route_name='get_tasks',
    renderer='json',
    permission='View_Task'
)
def get_tasks(request):
    """returns all the tasks in database related to the given taskable_entity
    """
    taskable_entity_id = request.matchdict.get('taskable_entity_id')
    taskable_entity = TaskableEntity.query\
                        .filter_by(id=taskable_entity_id).first()
    tasks = None
    if taskable_entity:
        tasks = taskable_entity.tasks
    
    for task in tasks:
        logger.debug('------------------------------')
        logger.debug('task name: %s' % task.name)
        logger.debug('start date: %s' % task.start)
        logger.debug('end date: %s' % task.end)
    
    return convert_to_jquery_gantt_task_format(tasks)

@view_config(
    route_name='get_project_tasks',
    renderer='json',
    permission='View_Task'
)
def get_project_tasks(request):
    """returns all the tasks of the given Project instance
    """
    project_id = request.matchdict.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    tasks = None
    if project:
        tasks = project.project_tasks
    
    return [
        {
            'id': task.id,
            'name': '%s (%s in %s)' % (task.name,
                                       task.task_of.name,
                                       task.task_of.project.name),
        }
        for task in tasks
    ]

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
    route_name='get_users',
    renderer='json',
    permission='View_User'
)
def get_users(request):
    """returns all the users in database
    """
    return [
        {'id': user.id, 'name': user.name}
        for user in User.query.all()
    ]

@view_config(
    route_name='view_project',
    renderer='templates/view_project.jinja2',
    permission='View_Project'
)
@view_config(
    route_name='view_assets',
    renderer='view_assets.jinja2',
    permission='View_Asset'
)
@view_config(
    route_name='view_shots',
    renderer='view_shots.jinja2',
    permission='View_Shot'
)
@view_config(
    route_name='overview_project',
    renderer='templates/overview_project.jinja2',
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

@view_config(
    route_name='view_tasks',
    renderer='view_tasks.jinja2',
    permission='View_Task'
)
def view_tasks(request):
    """runs when viewing tasks of a TaskableEntity
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    taskable_entity_id = request.matchdict['taskable_entity_id']
    taskable_entity = TaskableEntity.query\
        .filter_by(id=taskable_entity_id)\
        .first()
    
    tasks = sorted(taskable_entity.tasks, key=lambda x: x.project.id)
    
    # get distinct projects
    # TODO: again, please update it with a proper database query
    projects = list(set([task.project for task in tasks]))
    
    return {
        'taskable_entity': taskable_entity,
        'tasks': tasks,
        'projects': projects
    }

@view_config(
    route_name='add_task',
    renderer='add_task.jinja2',
    permission='Add_Task'
)
def add_task(request):
    """runs when adding a new task
    """
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        logger.debug('request.params["submitted"]: %s' % request.params['submitted'])
        
        if request.params['submitted'] == 'add':
            
            if 'task_of_id' in request.params and \
                'name' in request.params and \
                'description' in request.params and \
                'is_milestone' in request.params and \
                'resource_ids' in request.params and \
                'status_id' in request.params:
                
                # get the taskable entity
                task_of_id = request.params['task_of_id']
                taskable_entity = TaskableEntity.query.filter_by(id=task_of_id).first()
                
                # get the status_list
                status_list = StatusList.query.filter_by(
                    target_entity_type='Task'
                ).first()
                
                logger.debug('status_list: %s' % status_list)
                
                # there should be a status_list
                if status_list is None:
                    return HTTPServerError(
                        detail='No StatusList found'
                    )
                
                status_id = int(request.params['status_id'])
                logger.debug('status_id: %s' % status_id)
                status = Status.query.filter_by(id=status_id).first()
                logger.debug('status: %s' % status)
                
                # get the resources
                resource_ids = [
                    int(r_id)
                    for r_id in request.POST.getall('resource_ids')
                ]
                resources = User.query.filter(User.id.in_(resource_ids)).all()
                
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
                
                # get the dependencies
                depend_ids = [
                    int(d_id)
                    for d_id in request.POST.getall('depend_ids')
                ]
                depends = Task.query.filter(Task.id.in_(depend_ids)).all()
                logger.debug('depends: %s' % depends)
                
                try:
                    new_task = Task(
                        name=request.params['name'],
                        task_of=taskable_entity,
                        status_list=status_list,
                        status=status,
                        created_by=logged_in_user,
                        start=start,
                        end=end,
                        resources=resources,
                        depends=depends
                    )
                    
                    logger.debug('new_task.status: ' % new_task.status)
                    
                    DBSession.add(new_task)
                except (AttributeError, TypeError) as e:
                    logger.debug(e.message)
                else:
                    DBSession.add(new_task)
                    try:
                        transaction.commit()
                    except IntegrityError as e:
                        logger.debug(e.message)
                        transaction.abort()
                    else:
                        logger.debug('flushing the DBSession, no problem here!')
                        DBSession.flush()
                        logger.debug('finished adding Task')
                        #return {}
            else:
                logger.debug('there are missing parameters')
                def get_param(param):
                    if param in request.params:
                        logger.debug('%s: %s' % (param, request.params[param]))
                    else:
                        logger.debug('%s not in params' % param)
                get_param('task_of_id')
                get_param('name')
                get_param('description')
                get_param('is_milestone')
                get_param('resource_ids')
                get_param('status_id')
    
    # return the necessary values to prepare the form
    # get the taskable entity
    te_id = request.matchdict['taskable_entity_id']
    te = TaskableEntity.query.filter_by(id=te_id).first()
    
    return {
        'taskable_entity': te,
        'types': Type.query.filter_by(target_entity_type='Task').all(),
        'users': User.query.all(),
        'status_list':
            StatusList.query.filter_by(target_entity_type='Task').first()
    }

@view_config(
    route_name='add_department',
    renderer='add_department.jinja2',
    permission='Add_Department'
)
def add_department(request):
    """called when adding a new Department
    """
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    logger.debug('called add_department')
    
    try:
        logger.debug('submitted: %s' % request.params['submitted'])
        if request.params['submitted'] == 'add':
            # get the params and create the Department
            try:
                name = request.params['name']
            except KeyError:
                message = 'The name parameter is missing'
                logger.debug(message)
                return HTTPServerError(detail=message)
            
            try:
                lead_id = request.params['lead_id']
                lead = User.query.filter_by(id=lead_id).first()
            except KeyError:
                lead = None
            
            logger.debug('creating new department')
            new_department = Department(
                name=name,
                lead=lead,
                created_by=logged_in_user
            )
            DBSession.add(new_department)
            logger.debug('created new department')
    except KeyError:
        logger.debug('submitted is not in params')
    
    return {
        'users': User.query.all()
    }

@view_config(
    route_name='get_departments',
    renderer='json',
    permission='View_Department'
)
def get_departments(request):
    """returns all the departments in the database
    """
    return [
        {
            'id': dep.id,
            'name': dep.name
        }
        for dep in Department.query.all()
    ]


@view_config(
    route_name='add_group',
    renderer='add_groups.jinja2',
    permission='Add_Group'
)
def add_group(request):
    """runs when adding a new Group
    """
    return {}

@view_config(
    route_name='overview_user',
    renderer='overview_user.jinja2'
)
@view_config(
    route_name='view_user_tasks',
    renderer='view_tasks.jinja2'
)
def overview_user(request):
    """runs when over viewing general User info
    """
    # get the user id
    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()
    
    return {
        'user': user
    }

@view_config(
    route_name='get_user_tasks',
    renderer='json'
)
def get_user_tasks(request):
    """returns the user tasks as jQueryGantt json
    """
    # get user id
    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()
    
    # get tasks
    tasks = []
    if user is not None:
        tasks = sorted(user.tasks, key=lambda x: x.project.id)
    
    return convert_to_jquery_gantt_task_format(tasks)
