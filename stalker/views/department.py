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

from pyramid.httpexceptions import HTTPServerError
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from stalker.db import DBSession
from stalker import User, Department, Entity

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='create_department',
    renderer='templates/department/dialog_create_department.jinja2',
    permission='Create_Department'
)
def create_department(request):
    """called when creating a new Department
    """
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    logger.debug('called new_department')
    
    try:
        logger.debug('submitted: %s' % request.params['submitted'])
        if request.params['submitted'] == 'create':
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
    permission='Read_Department'
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
    route_name='view_department',
    renderer='templates/department/page_view_department.jinja2',
    permission='Read_Department'
)
def view_department(request):
    """runs when viewing a department
    """

    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()


    department_id = request.matchdict['department_id']
    department = Department.query.filter_by(id=department_id).first()

    return {
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
        'department': department
    }

@view_config(
    route_name='list_departments',
    renderer='templates/department/content_list_departments.jinja2',
    permission='Read_Department'
)
def list_departments(request):
    """
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()



    return {
        'entity': entity

    }

@view_config(
    route_name='get_departments_byEntity',
    renderer='json',
    permission='Read_Department'
)
def get_departments_byEntity(request):
    """
    """
    entity_id = request.matchdict['entity_id']
    entity = Entity.query.filter_by(id=entity_id).first()


    return [
            {
             'name': department.name,
             'id': department.id

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
    login = authenticated_userid(request)
    logged_user = User.query.filter_by(login=login).first()

    user_id = request.matchdict['user_id']
    user = User.query.filter_by(id=user_id).first()

    return {
        'logged_user': logged_user,
        'user': user
    }

@view_config(
    route_name='append_departments'
)
def append_departments(request):
    """appends the given users o the given Project or Department
    # """
    # # users
    # user_ids = [
    #     int(u_id)
    #     for u_id in request.POST.getall('entity_users')
    # ]
    # users = User.query.filter(User.id.in_(user_ids)).all()
    #
    # # entity
    # entity_id = request.params.get('entity_id', None)
    # entity = Entity.query.filter(Entity.id==entity_id).first()
    #
    # logger.debug('entity : %s' % entity)
    # logger.debug('users  : %s' % users)
    #
    # if users and entity:
    #     entity.users = users
    #     DBSession.add(entity)
    #     DBSession.add_all(users)

    return





