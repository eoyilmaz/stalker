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
logger.setLevel(logging.WARNING)

def setup(settings=None):
    """Utility function that helps to connect the system to the given database.
    
    if the database is None then the it setups using the default database in
    the settings file.
    
    :param settings: This is a dictionary which has keys prefixed with
        "sqlalchemy" and shows the settings. The most important one is the
        engine. The default is None, and in this case it uses the settings from
        stalker.conf.defaults.DATABASE_ENGINE_SETTINGS
   """

    if settings is None:
        settings = defaults.DATABASE_ENGINE_SETTINGS
        logger.debug('no settings given, using the default: %s' % settings)
    
    logger.debug("settings: %s" % settings)
    # create engine
    engine = engine_from_config(settings, 'sqlalchemy.')

    # create the Session class
    DBSession.configure(bind=engine)
    
    # create the database
    logger.debug("creating the tables")
    Base.metadata.create_all(engine)
    
   # init database
    __init_db__()

def __init_db__():
    """fills the database with default values
    """
    logger.debug("initializing database")

    if defaults.AUTO_CREATE_ADMIN:
        __create_admin__()

def __create_admin__():
    """creates the admin
    """
    
    from stalker.models.user import User
    from stalker.models.department import Department
    
    # check if there is already an admin in the database
    if len(DBSession.query(User).\
        filter_by(name=defaults.ADMIN_NAME).all()) > 0:
        #there should be an admin user do nothing
        logger.debug("there is an admin already")
        return

    logger.debug("creating the default administrator user")
    
    # create the admin department
    with transaction.manager:
        admin_department = DBSession.query(Department).filter_by(
            name=defaults.ADMIN_DEPARTMENT_NAME
        ).first()
        
        if not admin_department:
            admin_department = Department(name=defaults.ADMIN_DEPARTMENT_NAME)
            DBSession.add(admin_department)

        # create the admin user
        admin = User(
            name=defaults.ADMIN_NAME,
            first_name=defaults.ADMIN_NAME,
            login_name=defaults.ADMIN_NAME,
            password=defaults.ADMIN_PASSWORD,
            email=defaults.ADMIN_EMAIL,   
            department=admin_department,
        )
        
        admin.created_by = admin
        admin.updated_by = admin
        
        # update the department as created and updated by admin user
        admin_department.created_by = admin
        admin_department.updated_by = admin
        
        DBSession.add(admin)
    
    # TODO: create tests for the Ticket Status initialization
    # create statuses for Tickets
    from stalker import Status, StatusList
    with transaction.manager:
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
    
    # create Ticket Types
    from stalker import Type
    with transaction.manager:
        ticket_type_1 = Type(
            name='Defect',
            target_entity_type='Ticket'
        )
        ticket_type_2 = Type(
            name='Enhancement',
            target_entity_type='Ticket'
        )
        DBSession.add_all([ticket_type_1, ticket_type_2])
    
    
