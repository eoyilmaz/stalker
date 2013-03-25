# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
"""
Stalker is a Production Asset Management System (ProdAM) designed for animation
and vfx studios. See docs for more information.
"""

__version__ = '0.2.0.a7'

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from stalker.models.auth import Group, Permission, User
from stalker.models.asset import Asset
from stalker.models.department import Department
from stalker.models.entity import SimpleEntity, Entity
from stalker.models.format import ImageFormat
from stalker.models.link import Link
from stalker.models.message import Message
from stalker.models.mixins import (ProjectMixin, ReferenceMixin, ScheduleMixin,
                                   StatusMixin, TargetEntityTypeMixin,
                                   CodeMixin)
from stalker.models.note import Note
from stalker.models.project import Project
from stalker.models.repository import Repository
from stalker.models.scene import Scene
from stalker.models.sequence import Sequence
from stalker.models.shot import Shot
from stalker.models.status import Status, StatusList
from stalker.models.structure import Structure
from stalker.models.tag import Tag
from stalker.models.task import Booking, Task
from stalker.models.template import FilenameTemplate
from stalker.models.ticket import Ticket, TicketLog
from stalker.models.type import Type, EntityType
from stalker.models.version import Version
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
    
    # *************************************************************************
    # Basics
    config.add_route('home', '/')
    config.add_route('me_menu', '/me_menu')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    
    # *************************************************************************
    # DATA VIEWS
    # *************************************************************************
    
    # *************************************************************************
    # Project
    config.add_route('add_project', 'add/project')
    config.add_route('edit_project', 'edit/project/{project_id}')
    config.add_route('view_project', 'view/project/{project_id}')
    config.add_route('view_projects', 'view/projects')
    config.add_route('summarize_project', 'summarize/project/{project_id}')
    config.add_route('get_projects', 'get/projects')
    
    # *************************************************************************
    # ImageFormat
    config.add_route('add_image_format', 'add/image_format')
    config.add_route('edit_image_format', 'edit/image_format/{imf_id}')
    config.add_route('get_image_formats', 'get/image_formats')
    
    # *************************************************************************
    # Repository
    config.add_route('add_repository', 'add/repository')
    config.add_route('edit_repository', 'edit/repository/{repository_id}')
    config.add_route('get_repositories', 'get/repositories')
    
    # ************************************************************************* 
    # Structure
    config.add_route('add_structure', 'add/structure')
    config.add_route('edit_structure', 'edit/structure/{structure_id}')
    config.add_route('get_structures', 'get/structures')
    
    # ************************************************************************* 
    # User
    config.add_route('add_user', 'add/user')
    config.add_route('edit_user', 'edit/user/{user_id}')
    config.add_route('view_user', 'view/user/{user_id}')
    config.add_route('get_users', 'get/users')
    
    config.add_route('summarize_user', 'summarize/user/{user_id}')
    config.add_route('get_user_tasks', 'get/user/{user_id}/tasks')
    config.add_route('view_user_tasks', 'view/user/tasks/{user_id}')
    config.add_route('view_user_versions', 'view/user/versions/{user_id}')
    config.add_route('view_user_tickets', 'view/user/tickets/{user_id}')
    
    # *************************************************************************
    # FilenameTemplate
    config.add_route('add_filename_template', 'add/filename_template')
    config.add_route('edit_filename_template',
                     'edit/filename_template/{filename_template_id}')
    config.add_route('get_filename_templates', 'get/filename_templates')
    
    # ************************************************************************* 
    # StatusList
    config.add_route('add_status_list', 'add/status_list')
    config.add_route('add_status_list_for',
                     'add/status_list/{target_entity_type}')
    config.add_route('edit_status_list', 'edit/status_list/{status_list_id}')
    config.add_route('get_status_lists', 'get/status_lists')
    config.add_route('get_status_lists_for',
                     'get/status_lists_for/{target_entity_type}')
    
    # *************************************************************************
    # Status
    config.add_route('add_status', 'add/status')
    config.add_route('edit_status', 'edit/status')
    config.add_route('get_statuses', 'get/statuses')
    config.add_route('get_statuses_of', 'get/statuses_of/{status_list_id}')
    
    # *************************************************************************
    # Assets
    config.add_route('add_asset', 'add/asset/{project_id}')
    config.add_route('view_asset', 'view/asset/{asset_id}')
    config.add_route('summarize_asset', 'summarize/asset/{asset_id}')
    config.add_route('edit_asset', 'edit/asset/{asset_id}')
    config.add_route('view_assets', 'view/assets/{project_id}')
    config.add_route('get_assets', 'get/assets/{project_id}')
    
    # *************************************************************************
    # Shots
    config.add_route('add_shot', 'add/shot/{project_id}')
    config.add_route('view_shot', 'view/shot/{shot_id}')
    config.add_route('edit_shot', 'edit/shot/{shot_id}')
    config.add_route('view_shots', 'view/shots/{project_id}')
    config.add_route('get_shots', 'get/shots/{project_id}')
    
    # *************************************************************************
    # Sequence
    config.add_route('add_sequence', 'add/sequence')
    config.add_route('view_sequence', 'view/sequence/{sequence_id}')
    config.add_route('edit_sequence', 'edit/sequence/{sequence_id}')
    config.add_route('view_sequences', 'view/sequences/{project_id}')
    config.add_route('get_sequences',
                     'get/sequences/{project_id}')
    
    # *************************************************************************
    # Task
    config.add_route('add_task', 'add/task/{entity_id}')
    config.add_route('view_task', 'view/task/{task_id}')
    config.add_route('edit_task', 'edit/task/{task_id}')
    config.add_route('edit_tasks', 'edit/tasks')
    config.add_route('view_tasks', 'view/tasks/{entity_id}')
    config.add_route('get_tasks',
                     'get/tasks/{entity_id}')
    config.add_route('get_project_tasks', 'get/project_tasks/{project_id}')
    
    # *************************************************************************
    # Department
    config.add_route('add_department', 'add/department')
    config.add_route('edit_department', 'edit/department/{department_id}')
    config.add_route('view_department', 'view/department/{department_id}')
    config.add_route('get_departments', 'get/departments')
    
    # *************************************************************************
    # Group
    config.add_route('add_group', 'add/group')
    config.add_route('edit_group', 'edit/group/{group_id}')
    config.add_route('view_group', 'view/group/{group_id}')
    config.add_route('get_groups', 'get/groups')
    
    
    
    config.scan()
    return config.make_wsgi_app()

