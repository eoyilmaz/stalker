# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
"""
Stalker is a Production Asset Management System (ProdAM) designed for animation
and vfx studios. See docs for more information.
"""

__version__ = '0.2.0.a4'

from pyramid.config import Configurator

#from stalker.db.declarative import Base
#from stalker.db.session import DBSession
from stalker.models.asset import Asset
from stalker.models.auth import Group, Permission, User
from stalker.models.department import Department
from stalker.models.entity import SimpleEntity, Entity, TaskableEntity
from stalker.models.format import ImageFormat
from stalker.models.link import Link
from stalker.models.message import Message
from stalker.models.mixins import (ProjectMixin, ReferenceMixin, ScheduleMixin,
                                   StatusMixin, TargetEntityTypeMixin)
from stalker.models.note import Note
from stalker.models.project import Project
from stalker.models.repository import Repository
from stalker.models.sequence import Sequence
from stalker.models.shot import Shot
from stalker.models.status import Status, StatusList, Color
from stalker.models.structure import Structure
from stalker.models.tag import Tag
from stalker.models.task import Booking, Task
from stalker.models.template import FilenameTemplate
from stalker.models.ticket import Ticket, TicketLog
from stalker.models.type import Type, EntityType
from stalker.models.version import Version


from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from stalker.models.auth import group_finder

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    # setup the database to the given settings
    from stalker import db
    db.setup(settings)
    
    # setup authorization and authentication
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret',
        callback=group_finder
    )
    authz_policy = ACLAuthorizationPolicy()
    
    config = Configurator(
        settings=settings,
        root_factory='stalker.models.auth.RootFactory'
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy) 
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('user_menu', '/user_menu')
    config.add_route('projects_menu', '/projects_menu')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('add_project', 'add/project')
    config.add_route('edit_project', 'edit/project/{project_id}')
    config.add_route('add_image_format', 'add/image_format')
    config.add_route('edit_image_format', 'edit/image_format/{imf_id}')
    config.add_route('add_repository', 'add/repository')
    config.add_route('edit_repository', 'edit/repository')
    config.add_route('add_structure', 'add/structure')
    config.add_route('edit_structure', 'edit/structure/{structure_id}')
    config.add_route('add_user', 'add/user')
    config.add_route('edit_user', 'edit/user/{user_id}')
    config.add_route('add_filename_template', 'add/filename_template')
    config.add_route('edit_filename_template',
                     'edit/filename_template/{filename_template_id}')
    config.add_route('add_status_list', 'add/status_list')
    config.add_route('edit_status_list', 'edit/status_list/{status_list_id}')
    config.add_route('add_status', 'add/status')
    config.add_route('edit_status', 'edit/status')
    config.scan()
    return config.make_wsgi_app()

