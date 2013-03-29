# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from pyramid.httpexceptions import HTTPServerError
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from stalker.db import DBSession
from stalker import User, Department

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




