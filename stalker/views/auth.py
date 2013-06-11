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

from pyramid.httpexceptions import HTTPFound, HTTPOk, HTTPServerError
from pyramid.security import authenticated_userid, forget, remember
from pyramid.view import view_config, forbidden_view_config
from sqlalchemy import or_

import stalker
from stalker import (defaults, User, Department, Group, Tag, Project, Entity,
                     Studio, Permission, EntityType)
from stalker.db import DBSession
from stalker.views import log_param, get_logged_in_user, PermissionChecker, get_multi_integer, get_tags

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='dialog_create_user',
    renderer='templates/auth/dialog_create_user.jinja2'
)
def dialog_create_user(request):
    """called by create user dialog
    """
    logged_in_user = get_logged_in_user(request)
    
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()
    
    department = None
    group = None
    
    if isinstance(entity, Department):
        department = entity
    elif isinstance(entity, Group):
        group = entity
    
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request),
        'logged_in_user': logged_in_user,
        'department': department,
        'group': group
    }


@view_config(
    route_name='dialog_update_user',
    renderer='templates/auth/dialog_create_user.jinja2'
)
def dialog_update_user(request):
    """called when updating a user
    """
    logged_in_user = get_logged_in_user(request)
    
    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()
    
    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'logged_in_user': logged_in_user,
        'user': user
    }


@view_config(
    route_name='create_user'
)
def create_user(request):
    """called when adding a User
    """
    logged_in_user = get_logged_in_user(request)
    
    name = request.params.get('name', None)
    login = request.params.get('login', None)
    email = request.params.get('email', None)
    password = request.params.get('password', None)
    department_id = request.params.get('department_id', None)

    # create and add a new user
    if name and login and email and password:
        departments = []
        if department_id:
            department = Department.query.filter_by(id=department_id).first()
            departments = [department]
        else:
            # Departments
            if 'department_ids' in request.params:
                dep_ids = get_multi_integer(request, 'department_ids')
                departments = Department.query.filter(
                                Department.id.in_(dep_ids)).all()
    
        # Groups
        groups = []
        if 'group_ids' in request.params:
            grp_ids = get_multi_integer(request, 'group_ids')
            groups = Group.query.filter(
                            Group.id.in_(grp_ids)).all()
        
        # Tags
        tags = get_tags(request)

        logger.debug('creating new user')
        new_user = User(
            name=request.params['name'],
            login=request.params['login'],
            email=request.params['email'],
            password=request.params['password'],
            created_by=logged_in_user,
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
        HTTPServerError()
    
    return HTTPOk()


@view_config(
    route_name='update_user'
)
def update_user(request):
    """called when updating a User
    """
    logged_in_user = get_logged_in_user(request)
    
    user_id = request.params.get('user_id', -1)
    user = User.query.filter(User.id==user_id).first()
    
    name = request.params.get('name')
    login = request.params.get('login')
    email = request.params.get('email')
    password = request.params.get('password')
    
    # create and add a new user
    if user and name and login and email and password:
        departments = []

        # Departments
        if 'department_ids' in request.params:
            dep_ids = get_multi_integer(request,'department_ids')
            departments = Department.query \
                .filter(Department.id.in_(dep_ids)).all()

        # Groups
        groups = []
        if 'group_ids' in request.params:
            grp_ids = get_multi_integer(request, 'group_ids')
            groups = Group.query \
                .filter(Group.id.in_(grp_ids)).all()

        # Tags
        tags = get_tags(request)

        user.name = name
        user.login = login
        user.email = email
        user.updated_by = logged_in_user
        user.date_updated = datetime.datetime.now()
        user.departments = departments
        user.groups = groups
        user.tags = tags

        if password != 'DONTCHANGE':
            user.password = password
        
        logger.debug('updating user')
        DBSession.add(user)
        logger.debug('updated user successfully')
    else:
        logger.debug('not all parameters are in request.params')
        log_param(request, 'user_id')
        log_param(request, 'name')
        log_param(request, 'login')
        log_param(request, 'email')
        log_param(request, 'password')
        HTTPServerError()
    
    return HTTPOk()

@view_config(
    route_name='list_users',
    renderer='templates/auth/content_list_users.jinja2'
)
def view_users(request):
    """
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    return {
        'has_permission': PermissionChecker(request),
        'entity': entity
    }

@view_config(
    route_name='view_user',
    renderer='templates/auth/page_view_user.jinja2'
)
def view_user(request):
    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()
    
    logger.debug('user_id : %s' % user_id)
    logger.debug('user    : %s' % user)
     
    return {
        'user': user,
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='summarize_user',
    renderer='templates/auth/content_summarize_user.jinja2'
)
@view_config(
    route_name='view_user_tasks',
    renderer='templates/task/content_list_tasks.jinja2'
)
def summarize_user(request):
    """runs when getting general User info
    """
    # get logged in user

    logged_in_user = get_logged_in_user(request)

    # get the user id
    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()

    logger.debug('summarize_user is running')

    return {
        'user': user,
        'logged_in_user': logged_in_user,
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='get_users',
    renderer='json'
)
def get_users(request):
    """returns all the users in database
    """
    return [
        {'id': user.id, 'name': user.name}
        for user in User.query.order_by(User.name.asc()).all()
    ]


@view_config(
    route_name='get_users_byEntity',
    renderer='json'
)
def get_users_byEntity(request):
    """returns all the Users of a given Entity
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    users = []

    for user in sorted(entity.users, key=lambda x: x.name.lower()):
        departmentStr = ''
        groupStr = ''
        for department in user.departments:
            departmentStr += '<a href="javascript:redirectLink(%s, %s)">%s</a><br/>' % \
                             ("'central_content'" , ("'view/department/%s'" % department.id) , department.name)
        for group in user.groups:
            groupStr += '<a href="javascript:redirectLink(%s, %s)">%s</a><br/>' % \
                             ("'central_content'" , ("'view/group/%s'" % group.id) , group.name)
        users.append({
            'id': user.id,
            'name': user.name,
            'login': user.login,
            'email': user.email,
            'departments': departmentStr,
            'groups': groupStr,
            'tasksCount': len(user.tasks) ,
            'ticketsCount': len(user.open_tickets),
            'thumbnail_path': user.thumbnail.full_path if user.thumbnail else None
        })

    # works for Departments and Projects or any entity that has users attribute
    return users


@view_config(
    route_name='get_users_not_in_entity',
    renderer='json'
)
def get_users_not_in_entity(request):
    """returns all the Users which are not related with the given Entity
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    entity_class = None
    if entity.entity_type == 'Project':
        entity_class = Project
    elif entity.entity_type == 'Department':
        entity_class = Department

    logger.debug(User.query.filter(User.notin_(entity_class.users)).all())


    # works for Departments and Projects or any entity that has users attribute
    return [
        {
            'id': user.id,
            'name': user.name,
            'login': user.login,
            'tasksCount': len(user.tasks),
            'ticketsCount': len(user.open_tickets),
            'thumbnail_path': user.thumbnail.full_path if user.thumbnail else None
        }
        for user in entity.users
    ]


@view_config(
    route_name='dialog_append_users',
    renderer='templates/auth/dialog_append_users.jinja2'
)
def append_user_dialog(request):
    """runs for append user dialog
    """
    logged_in_user = get_logged_in_user(request)
    
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()
    
    return {
        'user': logged_in_user,
        'has_permission': PermissionChecker(request),
        'entity': entity
    }

@view_config(
    route_name='append_user'
)
def append_user(request):
    """appends the given user to the given Project or Department
    """
    # user
    user_id = request.params.get('user_id', None)
    user = User.query.filter(User.id==user_id).first()
    
    # entity
    entity_id = request.params.get('entity_id', None)
    entity = Entity.query.filter(Entity.id==entity_id).first()
    
    if user and entity:
        entity.users.append(user)
        DBSession.add_all([entity, user])
    
    return HTTPOk()


@view_config(
    route_name='append_users'
)
def append_users(request):
    """appends the given users o the given Project or Department
    """
    # users
    user_ids = get_multi_integer(request, 'user_ids')
    logger.debug('user_ids  : %s' % user_ids)
    users = User.query.filter(User.id.in_(user_ids)).all()
    
    # entity
    entity_id = request.params.get('entity_id', None)
    entity = Entity.query.filter(Entity.id==entity_id).first()
    
    logger.debug('entity : %s' % entity)
    logger.debug('users  : %s' % users)
    
    if users and entity:
        entity.users = users
        DBSession.add(entity)
        DBSession.add_all(users)
    
    return HTTPOk()


def get_permissions_from_multi_dict(multi_dict):
    """returns the permission instances from the given multi_dict
    """
    permissions = []
    for key in multi_dict.keys():
        access = multi_dict[key]
        action_and_class_name = key.split('_')

        try:
            action = action_and_class_name[0]
            class_name = action_and_class_name[1]

            logger.debug('access     : %s' % access)
            logger.debug('action     : %s' % action)
            logger.debug('class_name : %s' % class_name)

        except IndexError:
            continue

        else:
            # get permissions
            permission = Permission.query\
                .filter_by(access=access)\
                .filter_by(action=action)\
                .filter_by(class_name=class_name)\
                .first()

            if permission:
                permissions.append(permission)
    
    logger.debug(permissions)
    return permissions

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(
        location=request.route_url('login'),
        headers=headers
    )


@view_config(
    route_name='login',
    renderer='templates/auth/login.jinja2'
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


@forbidden_view_config(
    renderer='templates/auth/no_permission.jinja2'
)
def forbidden(request):
    """runs when user has no permission for the requested page
    """
    return {}


@view_config(
    route_name='home',
    renderer='templates/base.jinja2'
)
@view_config(
    route_name='me_menu',
    renderer='templates/auth/me_menu.jinja2'
)
def home(request):
    logged_in_user = get_logged_in_user(request)
    studio = Studio.query.first()
    projects = Project.query.all()
    
    logger.debug('logged_in_user     : %s' % logged_in_user)
    logger.debug('studio   : %s' % studio)
    logger.debug('projects : %s' % projects)
    
    if not logged_in_user:
        return logout(request)
    
    return {
        'stalker': stalker,
        'logged_in_user': logged_in_user,
        'projects': projects,
        'studio': studio,
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='check_login_availability',
    renderer='json'
)
def check_login_availability(request):
    """checks it the given login is available
    """
    login = request.matchdict['login']
    logger.debug('checking availability for: %s' % login)

    available = 1
    if login:
        user = User.query.filter(User.login==login).first()
        if user:
            available = 0

    return {
        'available': available
    }


@view_config(
    route_name='check_email_availability',
    renderer='json'
)
def check_email_availability(request):
    """checks it the given email is available
    """
    email = request.matchdict['email']
    logger.debug('checking availability for: %s' % email)

    available = 1
    if email:
        user = User.query.filter(User.email==email).first()
        if user:
            available = 0

    return {
        'available': available
    }

@view_config(
    route_name='dialog_create_group',
    renderer='templates/auth/dialog_create_group.jinja2'
)
def create_group_dialog(request):
    """create group dialog
    """
    logged_in_user = get_logged_in_user(request)

    permissions = Permission.query.all()

    entity_types = EntityType.query.all()

    return {
        'mode': 'CREATE',
        'actions': defaults.actions,
        'permissions': permissions,
        'entity_types': entity_types,
        'logged_in_user': logged_in_user,
        'has_permission': PermissionChecker(request)
    }

@view_config(
    route_name='dialog_update_group',
    renderer='templates/auth/dialog_create_group.jinja2'
)
def update_group_dialog(request):
    """update group dialog
    """
    logged_in_user = get_logged_in_user(request)

    permissions = Permission.query.all()

    entity_types = EntityType.query.all()

    group_id = request.matchdict['group_id']
    group = Group.query.filter_by(id=group_id).first()

    return {
        'mode': 'UPDATE',
        'group': group,
        'actions': defaults.actions,
        'permissions': permissions,
        'entity_types': entity_types,
        'logged_in_user': logged_in_user,
        'has_permission': PermissionChecker(request)
    }

@view_config(
    route_name='create_group'
)
def create_group(request):
    """runs when creating a new Group
    """
    logged_in_user = get_logged_in_user(request)
    
    # get parameters
    post_multi_dict = request.POST
    
    # get name
    name = post_multi_dict['name']

    # get description
    description =  post_multi_dict['description']
    
    # remove name and description to leave only permissions in the dictionary
    post_multi_dict.pop('name')
    post_multi_dict.pop('description')
    
    permissions = get_permissions_from_multi_dict(post_multi_dict)
    
    # create the new group
    new_group = Group(name=name)
    new_group.description = description
    new_group.created_by = logged_in_user
    new_group.permissions = permissions
    
    DBSession.add(new_group)
    
    return HTTPOk()

@view_config(
    route_name='update_group'
)
def update_group(request):
    """updates the group with data from request
    """
    logged_in_user = get_logged_in_user(request)
    
    # get parameters
    post_multi_dict = request.POST
    
    # get group_id
    group_id = post_multi_dict['group_id']
    group = Group.query.filter_by(id=group_id).first()
    
    # get name
    name = post_multi_dict['name']


    # get description
    description =  post_multi_dict['description']

    
    # remove name and description to leave only permission in the dictionary
    post_multi_dict.pop('name')
    post_multi_dict.pop('description')
    permissions = get_permissions_from_multi_dict(post_multi_dict)
    
    if group:
        group.name = name
        group.description = description
        group.permissions = permissions
        group.updated_by = logged_in_user
        group.date_updated = datetime.datetime.now()
        DBSession.add(group)
    
    return HTTPOk()

@view_config(
    route_name='list_groups',
    renderer='templates/auth/content_list_groups.jinja2'
)
def list_groups(request):
    """
    """
    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()

    return {
        'has_permission': PermissionChecker(request),
        'user': user
    }

@view_config(
    route_name='view_group',
    renderer='templates/auth/page_view_group.jinja2',
    permission='Read_Group'
)
def view_group(request):
    """runs when viewing a group
    """
    logged_in_user = get_logged_in_user(request)

    group_id = request.matchdict['group_id']
    group = Group.query.filter_by(id=group_id).first()

    return {
        'user': logged_in_user,
        'has_permission': PermissionChecker(request),
        'group': group
    }

@view_config(
    route_name='summarize_group',
    renderer='templates/auth/content_summarize_group.jinja2'
)
def summarize_group(request):
    """runs when getting general User info
    """
    # get the user id
    group_id = request.matchdict['group_id']
    group = Group.query.filter_by(id=group_id).first()

    return {
        'group': group,
        'has_permission': PermissionChecker(request)
    }

@view_config(
    route_name='get_groups',
    renderer='json',
    permission='List_Group'
)
def get_groups(request):
    """returns all the groups in database
    """
    return [
        {
            'id': group.id,
            'name': group.name,
            'thumbnail_path': group.thumbnail.full_path if group.thumbnail else None
        }
        for group in Group.query.order_by(Group.name.asc()).all()
    ]

@view_config(
    route_name='get_groups_byEntity',
    renderer='json',
    permission='Read_Group'
)
def get_groups_byEntity(request):
    """returns all the Users of a given Entity
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    return [
        {
             'id': group.id,
             'name': group.name,
             'thumbnail_path': group.thumbnail.full_path if group.thumbnail else None
        }
        for group in sorted(entity.groups, key=lambda x: x.name.lower())
    ]

@view_config(
    route_name='dialog_append_groups',
    renderer='templates/auth/dialog_append_groups.jinja2'
)
def append_groups_dialog(request):
    """runs for append user dialog
    """
    logged_in_user = get_logged_in_user(request)

    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()

    return {
        'has_permission': PermissionChecker(request),
        'logged_in_user': logged_in_user,
        'user': user
    }

@view_config(
    route_name='append_groups'
)
def append_groups(request):
    """appends the given groups o the given User
    # """
    # groups
    groups_ids = get_multi_integer(request, 'group_ids')
    logger.debug('groups_ids : %s' % groups_ids)

    groups = Group.query.filter(Group.id.in_(groups_ids)).all()

    # user
    user_id = request.params.get('user_id', None)
    user = User.query.filter(User.id==user_id).first()

    logger.debug('user : %s' % user)
    logger.debug('groups  : %s' % groups)

    if groups and user:
        user.groups = groups
        DBSession.add(user)
        DBSession.add_all(groups)

    return HTTPOk()


@view_config(
    route_name='list_permissions',
    renderer='templates/auth/content_list_permissions.jinja2'
)
def view_permissions(request):
    """create group dialog
    """
    logged_in_user = get_logged_in_user(request)

    permissions = Permission.query.all()

    entity_types = EntityType.query.all()

    group_id = request.matchdict['group_id']
    group = Group.query.filter_by(id=group_id).first()

    return {
        'mode': 'UPDATE',
        'group': group,
        'actions': defaults.actions,
        'permissions': permissions,
        'entity_types': entity_types,
        'logged_in_user': logged_in_user,
        'has_permission': PermissionChecker(request)
    }
