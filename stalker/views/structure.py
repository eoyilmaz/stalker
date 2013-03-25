# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from pyramid.security import authenticated_userid
from pyramid.view import view_config
import transaction

from stalker.db import DBSession
from stalker import User, Structure, FilenameTemplate

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_config(
    route_name='edit_structure',
    renderer='templates/structure/edit_structure.jinja2',
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
    route_name='add_structure',
    renderer='templates/structure/add_structure.jinja2',
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
