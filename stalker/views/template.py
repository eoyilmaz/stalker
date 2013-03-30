# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause


from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import DetachedInstanceError
import transaction

from stalker.db import DBSession
from stalker import User, FilenameTemplate, Type, EntityType

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='update_filename_template',
    renderer='templates/template/update_filename_template.jinja2',
    permission='Update_FilenameTemplate'
)
def update_filename_template(request):
    """called when updateing a FilenameTemplate instance
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'update':
            logger.debug('updateing a Filename Template')
            # just update the given filename_template
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
        
        logger.debug('finished updateing FilenameTemplate')
 
     
    return {}


@view_config(
    route_name='create_filename_template',
    renderer='templates/template/dialog_create_filename_template.jinja2',
    permission='Create_FilenameTemplate'
)
def create_filename_template(request):
    """called when adding a FilenameTemplate instance
    """
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    
    login = authenticated_userid(request)
    user = User.query.filter_by(login=login).first()
    
    if 'submitted' in request.params:
        if request.params['submitted'] == 'create':
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
    route_name='get_filename_templates',
    renderer='json',
    permission='Read_FilenameTemplate'
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
