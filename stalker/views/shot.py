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
from sqlalchemy.exc import IntegrityError
import transaction

from stalker.db import DBSession
from stalker import User, Sequence, StatusList, Status, Shot, Project

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='create_shot',
    renderer='templates/shot/dialog_create_shot.jinja2',
    permission='Create_Shot'
)
def create_shot(request):
    """runs when adding a new shot
    """
    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        logger.debug('request.params["submitted"]: %s' % request.params['submitted'])
        
        if request.params['submitted'] == 'create':
            if 'name' in request.params and \
               'code' in request.params and  \
               'sequence_id' in request.params and \
               'status_id' in request.params:
                
                sequence_id = request.params['sequence_id']
                sequence = Sequence.query.filter_by(id=sequence_id).first()

                project_id = request.matchdict['project_id']
                project = Project.query.filter_by(id=project_id).first()
                # get the status_list
                status_list = StatusList.query.filter_by(
                    target_entity_type='Shot'
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
                        created_by=logged_in_user,
                        project=project
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
    route_name='view_shot',
    renderer='templates/shot/page_view_shot.jinja2'
)
def view_shot(request):
    """runs when viewing an shot
    """

    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()

    shot_id = request.matchdict['shot_id']
    shot = Shot.query.filter_by(id=shot_id).first()

    return {
        'user': logged_in_user,
        'shot': shot
    }

@view_config(
    route_name='update_shot',
    renderer='templates/shot/dialog_update_shot.jinja2',
    permission='Update_Shot'
)
def update_shot(request):
    """runs when updating a shot
    """

    shot_id = request.matchdict['shot_id']
    shot = Shot.query.filter_by(id=shot_id).first()

    return {
        'shot': shot,
        'projects': Project.query.all()
    }


@view_config(
    route_name='summarize_shot',
    renderer='templates/shot/content_summarize_shot.jinja2'
)
def summarize_shot(request):
    """runs when viewing an shot
    """

    login = authenticated_userid(request)
    logged_in_user = User.query.filter_by(login=login).first()

    shot_id = request.matchdict['shot_id']
    shot = Shot.query.filter_by(id=shot_id).first()

    return {
        'user': logged_in_user,
        'shot': shot
    }

@view_config(
    route_name='get_shots',
    renderer='json',
    permission='Read_Shot'
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
            sequenceStr += '<a class="DataLink" href="#" stalker_target="sequences_content_pane" stalker_href="view/sequence/%s">%s</a><br/> ' % (sequence.id,sequence.name)
        shots.append({
            'id': shot.id,
            'name': shot.name,
            'sequences': sequenceStr,
            'status': shot.status.name,
            'user_id': shot.created_by.id,
            'user_name': shot.created_by.name
        })


    return shots
