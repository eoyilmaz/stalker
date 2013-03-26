# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from pyramid.httpexceptions import HTTPServerError, HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError

import transaction
from stalker.db import DBSession
from stalker import User, Project, StatusList, Status, Sequence, Type

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='add_sequence',
    renderer='templates/sequence/add_sequence.jinja2',
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


    project = Project.query.filter_by(id=request.matchdict['project_id']).first()

    return {
        'project': project,
        'projects': Project.query.all(),
        'types': Type.query.filter_by(target_entity_type='Sequence').all(),
        'status_list':
            StatusList.query.filter_by(target_entity_type='Sequence').first()
    }


@view_config(
    route_name='edit_sequence',
    renderer='templates/sequence/edit_sequence.jinja2',
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
