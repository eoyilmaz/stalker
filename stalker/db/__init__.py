# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
"""Database module of Stalker.

Whenever stalker.db or something under it imported, the
:func:`stalker.db.setup` becomes available to let one setup the database.
"""

import logging

import transaction
from sqlalchemy import engine_from_config

from stalker.conf import defaults
from stalker.db.declarative import Base
from stalker.db.session import DBSession

# create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def setup(settings=None, callback=None):
    """Utility function that helps to connect the system to the given database.
    
    if the database is None then the it setups using the default database in
    the settings file.
    
    :param settings: This is a dictionary which has keys prefixed with
        "sqlalchemy" and shows the settings. The most important one is the
        engine. The default is None, and in this case it uses the settings from
        stalker.conf.defaults.DATABASE_ENGINE_SETTINGS
    
    :param callback: A callback function which is called after database is
        initialized. It is a good place to register your own classes.
   """

    if settings is None:
        settings = defaults.DATABASE_ENGINE_SETTINGS
        logger.debug('no settings given, using the default: %s' % settings)
    
    logger.debug("settings: %s" % settings)
    # create engine
    engine = engine_from_config(settings, 'sqlalchemy.')
    
    logger.debug('engine: %s' % engine)
    
    # create the Session class
    DBSession.remove()
    DBSession.configure(bind=engine)
    
    # create the database
    logger.debug("creating the tables")
    Base.metadata.create_all(engine)
    #Base.metadata.bind = engine
    
    # init database
    __init_db__()
    
    # call callback function
    if callback:
        callback()

def __init_db__():
    """fills the database with default values
    """
    logger.debug("initializing database")
    
    # register all Actions available for all SOM classes
    class_names = [
        'Asset', 'Action', 'Group', 'Permission', 'User', 'Department',
        'Entity', 'SimpleEntity', 'TaskableEntity', 'ImageFormat', 'Link',
        'Message', 'Note', 'Project', 'Repository', 'Sequence', 'Shot',
        'Status', 'StatusList', 'Structure', 'Tag', 'Booking', 'Task',
        'FilenameTemplate', 'Ticket', 'TicketLog', 'Type', 'Version',
    ]
    
    for class_name in class_names:
        register(class_name)
    
    # create the admin if needed
    if defaults.AUTO_CREATE_ADMIN:
        __create_admin__()
    
    logger.debug('finished initializing the database')

def __create_admin__():
    """creates the admin
    """
    
    from stalker.models.auth import User
    from stalker.models.department import Department
    
    # check if there is already an admin in the database
    if len(User.query()
        .filter_by(name=defaults.ADMIN_NAME)
        .all()) > 0:
        #there should be an admin user do nothing
        logger.debug("there is an admin already")
        return

    logger.debug("creating the default administrator user")
    
    # create the admin department
    #with transaction.manager:
    admin_department = Department.query().filter_by(
        name=defaults.ADMIN_DEPARTMENT_NAME
    ).first()
    
    if not admin_department:
        admin_department = Department(name=defaults.ADMIN_DEPARTMENT_NAME)
        DBSession.add(admin_department)
    # create the admins group
    
    from stalker.models.auth import Group
    
    admins_group = Group.query()\
        .filter_by(name=defaults.ADMIN_GROUP_NAME)\
        .first()
    
    if not admins_group:
        admins_group = Group(name=defaults.ADMIN_GROUP_NAME)
        DBSession.add(admins_group)
    
    # create the admin user
    admin = User.query()\
        .filter_by(name=defaults.ADMIN_NAME)\
        .first()
    
    if not admin:
        admin = User(
            name=defaults.ADMIN_NAME,
            first_name=defaults.ADMIN_NAME,
            login_name=defaults.ADMIN_NAME,
            password=defaults.ADMIN_PASSWORD,
            email=defaults.ADMIN_EMAIL,   
            department=admin_department,
            groups=[admins_group]
        )
        
        admin.created_by = admin
        admin.updated_by = admin
    
    # update the department as created and updated by admin user
    admin_department.created_by = admin
    admin_department.updated_by = admin
    
    admins_group.created_by = admin
    admins_group.updated_by = admin
    
    DBSession.add(admin)
    transaction.commit()
    
    # create statuses for Tickets
    from stalker import Status, StatusList
    #with transaction.manager:
    ticket_status1 = Status(name='New', code='NEW')
    ticket_status2 = Status(name='Reopened', code='REOPENED')
    ticket_status3 = Status(name='Closed', code='CLOSED')
    
    ticket_status_list = StatusList(
        name='Ticket Statuses',
        target_entity_type='Ticket',
        statuses=[
            ticket_status1,
            ticket_status2,
            ticket_status3,
        ]
    )
    
    DBSession.add(ticket_status_list)
    transaction.commit()
    
    # create Ticket Types
    from stalker import Type
    #with transaction.manager:
    ticket_type_1 = Type(
        name='Defect',
        target_entity_type='Ticket'
    )
    ticket_type_2 = Type(
        name='Enhancement',
        target_entity_type='Ticket'
    )
    DBSession.add_all([ticket_type_1, ticket_type_2])
    transaction.commit()

def register(class_):
    """Registers the given class to the database.
    
    It is mainly used to create the :class:`~stalker.models.auth.Action`\ s
    needed for the :class:`~stalker.models.auth.User`\ s and
    :class:`~stalker.models.auth.Group`\ s to be able to interact with the
    given class. Whatever class you have created needs to be registered.
    
    Example, lets say that you have a data class which is specific to your
    studio and it is not present in Stalker Object Model (SOM), so you need to
    extend SOM with a new data type. Here is a simple Data class inherited from
    the :class:`~stalker.models.entity.SimpleEntity` class (which is the
    simplest class you should inherit your classes from or use more complex
    classes down to the hierarchy)::
    
      from sqlalchemy import Column, Integer, ForeignKey
      from stalker.models.entity import SimpleEntity
      
      class MyDataClass(SimpleEntity):
        '''This is an example class holding a studio specific data which is not
        present in SOM.
        '''
        
        __tablename__ = 'MyData'
        __mapper_arguments__ = {'polymorphic_identity': 'MyData'}
        
        my_data_id = Column('id', Integer, ForeignKey('SimpleEntities.c.id'),
                            primary_key=True)
    
    Now because Stalker is using Pyramid authorization mechanism it needs to be
    able to have an :class:`~stalker.models.auth.Permission` about your new
    class, so you can assign this :class;`~stalker.models.auth.Permission` to
    your :class:`~stalker.models.auth.User`\ s or
    :class:`~satlker.models.auth.Group`\ s. So you ned to register your new
    class with stalker.db.register like shown below::
    
      from stalker import db
      db.register(MyDataClass)
    
    This will create the necessary Actions in the 'Actions' table on your
    database, then you can create :class:`~stalker.models.auth.Permission`\ s
    and assign these to your :class:`~stalker.models.auth.User`\ s and
    :class:`~stalker.models.auth.Group`\ s so they are Allowed or Denied to do
    the specified Action.
    
    :param class_: The class itself that needs to be registered.
    """
    from pyramid.security import Allow, Deny
    from stalker.models.auth import Permission
    
    # create the Permissions
    permissions_db = Permission.query().all()
    
    if isinstance(class_, type):
        class_name = class_.__class__.__name__
    elif isinstance(class_, (str, unicode)):
        class_name = class_
    else:
        raise TypeError('To register a class please either supply the class '
                        'itself or the name of it')
    
    for action in defaults.DEFAULT_ACTIONS:
        for access in  [Allow, Deny]:
            permission_obj = Permission(access, action, class_name)
            if permission_obj not in permissions_db:
                #logger.debug('adding new permission %s, %s, %s' % 
                #    (permission_obj.access,
                #     permission_obj.action,
                #     permission_obj.class_name)
                #)
                DBSession.add(permission_obj)
            #else:
            #    logger.debug('permission already defined in db:'
            #                 ' %s, %s, %s' %
            #        (permission_obj.access,
            #         permission_obj.action,
            #         permission_obj.class_name)
            #    )
    
    transaction.commit()
