# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
"""
Stalker is a Production Asset Management System (ProdAM) designed for animation
and vfx studios. See docs for more information.
"""


from pyramid.config import Configurator

from stalker import db

__version__ = '0.2.0.a1'

#from stalker.db.declarative import Base
#from stalker.db.session import DBSession
from stalker.models.asset import Asset
from stalker.models.auth import Group, User
from stalker.models.department import Department
from stalker.models.entity import SimpleEntity, Entity, TaskableEntity
from stalker.models.formats import ImageFormat
from stalker.models.link import Link
from stalker.models.message import Message
from stalker.models.mixins import (ProjectMixin, ReferenceMixin, ScheduleMixin,
                                   StatusMixin, TargetEntityTypeMixin)
from stalker.models.note import Note
from stalker.models.project import Project
from stalker.models.repository import Repository
from stalker.models.sequence import Sequence
from stalker.models.shot import Shot
from stalker.models.status import Status, StatusList
from stalker.models.structure import Structure
from stalker.models.tag import Tag
from stalker.models.task import Booking
from stalker.models.task import Task
from stalker.models.templates import FilenameTemplate
from stalker.models.type import Type
from stalker.models.version import Version


from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from stalker.models.auth import group_finder

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    # setup the database to the given settings
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
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()

