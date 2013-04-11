# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
# 
# This file is part of Stalker.
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
"""
Stalker is a Production Asset Management System (ProdAM) designed for animation
and vfx studios. See docs for more information.
"""

__version__ = '0.2.0.a10'

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
    config.add_route('create_project', 'create/project')
    config.add_route('update_project', 'update/project/{project_id}')
    config.add_route('view_project', 'view/project/{project_id}')
    config.add_route('list_projects', 'list/projects')
    config.add_route('summarize_project', 'summarize/project/{project_id}')
    config.add_route('get_projects', 'get/projects')
    
    # *************************************************************************
    # ImageFormat
    config.add_route('create_image_format', 'create/image_format')
    config.add_route('update_image_format', 'update/image_format/{imf_id}')
    config.add_route('get_image_formats', 'get/image_formats')
    
    # *************************************************************************
    # Repository
    config.add_route('create_repository', 'create/repository')
    config.add_route('update_repository', 'update/repository/{repository_id}')
    config.add_route('get_repositories', 'get/repositories')
    
    # ************************************************************************* 
    # Structure
    config.add_route('create_structure', 'create/structure')
    config.add_route('update_structure', 'update/structure/{structure_id}')
    config.add_route('get_structures', 'get/structures')
    
    # ************************************************************************* 
    # User
    config.add_route('create_user', 'create/user/{department_id}')
    config.add_route('update_user', 'update/user/{user_id}')
    config.add_route('view_user', 'view/user/{user_id}')
    config.add_route('list_users', 'list/users/{entity_id}')
    config.add_route('get_users', 'get/users')
    config.add_route('get_users_byEntity', 'get/users_byEntity/{entity_id}')
    config.add_route('append_user', 'append/user/{project_id}')
    
    config.add_route('summarize_user', 'summarize/user/{user_id}')
    config.add_route('view_user_tasks', 'view/user/tasks/{user_id}')
    config.add_route('view_user_versions', 'view/user/versions/{user_id}')
    config.add_route('view_user_tickets', 'view/user/tickets/{user_id}')
    
    # *************************************************************************
    # FilenameTemplate
    config.add_route('create_filename_template', 'create/filename_template')
    config.add_route('update_filename_template',
                     'update/filename_template/{filename_template_id}')
    config.add_route('get_filename_templates', 'get/filename_templates')
    
    # ************************************************************************* 
    # StatusList
    config.add_route('create_status_list', 'create/status_list')
    config.add_route('create_status_list_for',
                     'create/status_list/{target_entity_type}')
    config.add_route('update_status_list', 'update/status_list/{target_entity_type}')
    config.add_route('get_status_lists', 'get/status_lists')
    config.add_route('get_status_lists_for',
                     'get/status_lists_for/{target_entity_type}')
    
    # *************************************************************************
    # Status
    config.add_route('create_status', 'create/status')
    config.add_route('update_status', 'update/status')
    config.add_route('get_statuses', 'get/statuses')
    config.add_route('get_statuses_for', 'get/statuses_for/{target_entity_type}')
    config.add_route('get_statuses_of', 'get/statuses_of/{status_list_id}')
    
    # *************************************************************************
    # Assets
    config.add_route('create_asset', 'create/asset/{project_id}')
    config.add_route('view_asset', 'view/asset/{asset_id}')
    config.add_route('summarize_asset', 'summarize/asset/{asset_id}')
    config.add_route('update_asset', 'update/asset/{asset_id}')
    config.add_route('list_assets', 'list/assets/{project_id}')
    config.add_route('get_assets', 'get/assets/{project_id}')
    
    # *************************************************************************
    # Shots
    config.add_route('create_shot', 'create/shot/{project_id}')
    config.add_route('view_shot', 'view/shot/{shot_id}')
    config.add_route('summarize_shot', 'summarize/shot/{shot_id}')
    config.add_route('update_shot', 'update/shot/{shot_id}')
    config.add_route('list_shots', 'list/shots/{project_id}')
    config.add_route('get_shots', 'get/shots/{project_id}')
    
    # *************************************************************************
    # Sequence
    config.add_route('create_sequence', 'create/sequence/{project_id}')
    config.add_route('view_sequence', 'view/sequence/{sequence_id}')
    config.add_route('summarize_sequence', 'summarize/sequence/{sequence_id}')
    config.add_route('update_sequence', 'update/sequence/{sequence_id}')
    config.add_route('list_sequences', 'list/sequences/{project_id}')
    config.add_route('get_sequences',
                     'get/sequences/{project_id}')
    
    # *************************************************************************
    # Task
    
    # Dialogs
    config.add_route('create_task_dialog', 'dialog/create/task/{project_id}')
    config.add_route('create_child_task_dialog', 'dialog/create/child_task/{task_id}')
    config.add_route('create_dependent_task_dialog', 'dialog/create/dependent_task/{task_id}')
    config.add_route('update_task_dialog', 'dialog/update/task/{task_id}')
    
    config.add_route('create_task', 'create/task')

    config.add_route('view_task', 'view/task/{task_id}')
    config.add_route('update_task', 'update/task/{task_id}')
    config.add_route('list_tasks', 'list/tasks/{entity_id}')
    
    config.add_route('get_entity_tasks',  'get/entity/tasks/{entity_id}')
    config.add_route('get_user_tasks',    'get/user/tasks/{user_id}')
    config.add_route('get_project_tasks', 'get/project/tasks/{project_id}')
    config.add_route('get_root_tasks',    'get/root/tasks/{project_id}') # TODO: fix this

    config.add_route('get_gantt_tasks', 'get/gantt/tasks/{entity_id}')
    config.add_route('update_gantt_tasks', 'update/gantt/tasks')
    
    # *************************************************************************
    # Booking
    config.add_route('create_booking_dialog', 'dialog/create/booking/{task_id}')
    config.add_route('update_booking_dialog', 'dialog/update/booking/{booking_id}')
    
    config.add_route('create_booking', 'create/booking/{task_id}')
    
    config.add_route('get_bookings', 'get/bookings/{task_id}') # returns json
    config.add_route('list_bookings', 'list/bookings/{task_id}')      # returns response
    
    # *************************************************************************
    # Department
    config.add_route('create_department', 'create/department')
    config.add_route('update_department', 'update/department/{department_id}')
    config.add_route('summarize_department', 'summarize/department/{department_id}')
    config.add_route('view_department', 'view/department/{department_id}')
    config.add_route('get_departments', 'get/departments')
    
    # *************************************************************************
    # Group
    config.add_route('create_group', 'create/group')
    config.add_route('update_group', 'update/group/{group_id}')
    config.add_route('view_group', 'view/group/{group_id}')
    config.add_route('get_groups', 'get/groups')
    
    
    
    config.scan()
    return config.make_wsgi_app()

