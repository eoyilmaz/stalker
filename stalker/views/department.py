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
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from stalker.db import DBSession
from stalker import User, Department, Entity, Tag

import logging
from stalker import log
from stalker.views import PermissionChecker, get_logged_in_user, log_param, get_multi_integer, get_tags

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='dialog_create_department',
    renderer='templates/department/dialog_create_department.jinja2'
)
def create_department_dialog(request):
    """fills the create department dialog
    """

    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request),
        # 'users': User.query.all()
    }


@view_config(
    route_name='dialog_update_department',
    renderer='templates/department/dialog_create_department.jinja2'
)
def update_department_dialog(request):
    """fills the update department dialog
    """
    department_id = request.matchdict['department_id']
    department = Department.query.filter_by(id=department_id).first()

    logger.debug('called update_department_dialog %s' % department_id)
    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'department': department
    }


@view_config(
    route_name='create_department'
)
def create_department(request):
    """creates a new Department
    """
    logged_in_user = get_logged_in_user(request)
    
    logger.debug('called new_department')

    # get params

    name =  request.params.get('name')

    if name:
        description =  request.params.get('description')

        lead_id = request.params.get('lead_id', -1)
        lead = User.query.filter_by(id=lead_id).first()

        # Tags
        tags = get_tags(request)

        logger.debug('creating new department')
        new_department = Department(
           name = name,
           description = description,
           lead = lead,
           created_by=logged_in_user,
           tags = tags
        )
        DBSession.add(new_department)
        logger.debug('created new department')
    else:
        logger.debug('not all parameters are in request.params')
        log_param(request, 'name')
        HTTPServerError()

    return HTTPOk()

@view_config(
    route_name='update_department'
)
def update_department(request):
    """updates an Department
    """
    logged_in_user = get_logged_in_user(request)

    logger.debug('called update_department')
    # get params
    department_id = request.params.get('department_id')
    department = Department.query.filter_by(id=department_id).first()

    name = request.params.get('name')


    if department and name:
        # get the type
        description =  request.params.get('description')

        lead_id = request.params.get('lead_id', -1)
        lead = User.query.filter_by(id=lead_id).first()

        # Tags
        tags = get_tags(request)

        # update the department
        department.name = name
        department.description = description
        logger.debug('request.description: %s' % description)
        logger.debug('department.description  : %s' % department.description)
        department.lead = lead
        department.tags = tags
        department.updated_by = logged_in_user
        department.date_updated = datetime.datetime.now()

        logger.debug('updating department')
        DBSession.add(department)
        logger.debug('updated department successfully')
    else:
        logger.debug('not all parameters are in request.params')
        log_param(request, 'department_id')
        log_param(request, 'name')
        HTTPServerError()

    return HTTPOk()



@view_config(
    route_name='get_departments',
    renderer='json'
)
def get_departments(request):
    """returns all the departments in the database
    """
    return [
        {
            'id': dep.id,
            'name': dep.name
        }
        for dep in Department.query.order_by(Department.name.asc()).all()
    ]

@view_config(
    route_name='view_department',
    renderer='templates/department/page_view_department.jinja2'
)
def view_department(request):
    """runs when viewing a department
    """

    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()


    department_id = request.matchdict['department_id']
    department = Department.query.filter_by(id=department_id).first()

    return {
        'has_permission': PermissionChecker(request),
        'user': logged_in_user,
        'department': department
    }

@view_config(
    route_name='summarize_department',
    renderer='templates/department/content_summarize_department.jinja2'
)
def summarize_department(request):
    """runs when getting general User info
    """
    # get the user id
    department_id = request.matchdict['department_id']
    department = Department.query.filter_by(id=department_id).first()

    return {
        'has_permission': PermissionChecker(request),
        'department': department
    }

@view_config(
    route_name='list_departments',
    renderer='templates/department/content_list_departments.jinja2'
)
def list_departments(request):
    """
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()

    return {
        'has_permission': PermissionChecker(request),
        'entity': entity
    }

@view_config(
    route_name='get_departments_byEntity',
    renderer='json'
)
def get_departments_byEntity(request):
    """
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()


    return [
            {
             'name': department.name,
             'id': department.id,
            'thumbnail_path': department.thumbnail.full_path if department.thumbnail else None

            }
            for department in entity.departments
        ]


@view_config(
    route_name='dialog_append_departments',
    renderer='templates/department/dialog_append_departments.jinja2'
)
def append_departments_dialog(request):
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
    route_name='append_departments'
)
def append_departments(request):
    """appends the given department to the given User
    """
    # departments
    department_ids = get_multi_integer(request, 'department_ids')
    departments = Department.query.filter(Department.id.in_(department_ids)).all()

    # user
    user_id = request.params.get('user_id', None)
    user = Entity.query.filter(User.id==user_id).first()

    logger.debug('user : %s' % user)
    logger.debug('departments  : %s' % departments)

    if departments and user:
        user.departments = departments
        DBSession.add(user)
        DBSession.add_all(departments)

    return HTTPOk()





