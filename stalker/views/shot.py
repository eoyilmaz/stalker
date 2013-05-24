# -*- coding: utf-8 -*-
# Stalker a Production Shot Management System
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

from pyramid.httpexceptions import HTTPServerError, HTTPOk
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError
import transaction

from stalker.db import DBSession
from stalker import User, Sequence, StatusList, Status, Shot, Project

import logging
from stalker import log
from stalker.views import PermissionChecker, get_logged_in_user

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)

@view_config(
    route_name='dialog_create_shot',
    renderer='templates/shot/dialog_create_shot.jinja2'
)
def create_shot_dialog(request):
    """fills the create shot dialog
    """
    project_id = request.matchdict['project_id']
    project = Project.query.filter_by(id=project_id).first()

    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request),
        'project': project
    }


@view_config(
    route_name='dialog_update_shot',
    renderer='templates/shot/dialog_create_shot.jinja2'
)
def update_shot_dialog(request):
    """fills the create shot dialog
    """
    shot_id = request.matchdict['shot_id']
    shot = Shot.query.filter_by(id=shot_id).first()

    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'shot': shot,
        'project': shot.project
    }

@view_config(
    route_name='create_shot'
)
def create_shot(request):
    """runs when adding a new shot
    """
    logged_in_user = get_logged_in_user(request)

    name = request.params.get('name')
    code = request.params.get('code')

    status_id = request.params.get('status_id')
    status = Status.query.filter_by(id=status_id).first()

    project_id = request.params.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    logger.debug('project_id   : %s' % project_id)

    if name and code  and status and  project:
        # get descriptions
        description = request.params.get('description')

        sequence_id = request.params['sequence_id']
        sequence = Sequence.query.filter_by(id=sequence_id).first()

        # get the status_list
        status_list = StatusList.query.filter_by(
            target_entity_type='Shot'
        ).first()

        # there should be a status_list
        # TODO: you should think about how much possible this is
        if status_list is None:
            return HTTPServerError(detail='No StatusList found')


        new_shot = Shot(
                        name=name,
                        code=code,
                        description=description,
                        sequence=sequence,
                        status_list=status_list,
                        status=status,
                        created_by=logged_in_user,
                        project=project
                    )

        DBSession.add(new_shot)
    
    else:
        logger.debug('there are missing parameters')
        logger.debug('name      : %s' % name)
        logger.debug('code      : %s' % code)
        logger.debug('status    : %s' % status)
        logger.debug('project   : %s' % project)
        HTTPServerError()

    return HTTPOk()

@view_config(
    route_name='update_shot'
)
def update_shot(request):
    """runs when adding a new shot
    """
    logged_in_user = get_logged_in_user(request)

    shot_id = request.params.get('shot_id')
    shot = Shot.query.filter_by(id=shot_id).first()

    name = request.params.get('name')

    status_id = request.params.get('status_id')
    status = Status.query.filter_by(id=status_id).first()


    if shot and name  and status:
        # get descriptions
        description = request.params.get('description')

        sequence_id = request.params['sequence_id']
        sequence = Sequence.query.filter_by(id=sequence_id).first()

        #update the shot

        shot.name = name
        shot.description = description
        shot.sequence = sequence
        shot.status = status
        shot.updated_by = logged_in_user
        shot.date_updated = datetime.datetime.now()

        DBSession.add(shot)

    else:
        logger.debug('there are missing parameters')
        logger.debug('name      : %s' % name)
        logger.debug('status    : %s' % status)
        HTTPServerError()

    return HTTPOk()


@view_config(
    route_name='view_shot',
    renderer='templates/shot/page_view_shot.jinja2'
)
@view_config(
    route_name='summarize_shot',
    renderer='templates/shot/content_summarize_shot.jinja2'
)
def view_shot(request):
    """runs when viewing an shot
    """
    logged_in_user = get_logged_in_user(request)

    shot_id = request.matchdict['shot_id']
    shot = Shot.query.filter_by(id=shot_id).first()

    return {
        'user': logged_in_user,
        'shot': shot,
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='get_shots',
    renderer='json'
)
def get_shots(request):
    """returns all the Shots of the given Project
    """
    project_id = request.matchdict['project_id']
    project = Project.query.filter_by(id=project_id).first()

    shots = []

    for shot in Shot.query.filter_by(project_id=project_id).all():
        sequenceStr = ''

        for sequence in shot.sequences:
            sequenceStr += '<a href="javascript:redirectLink(%s, %s)">%s</a><br/>' % \
                             ("'sequences_content_pane'" , ("'view/sequence/%s'" % sequence.id) , sequence.name)
        shots.append({
            'id': shot.id,
            'name': shot.name,
            'sequences': sequenceStr,
            'status': shot.status.name,
            'status_bg_color': shot.status.bg_color,
            'status_fg_color': shot.status.fg_color,
            'user_id': shot.created_by.id,
            'user_name': shot.created_by.name,
            'description': shot.description
        })


    return shots
