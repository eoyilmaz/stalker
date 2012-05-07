# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
"""Database module of Stalker.

Whenever stalker.db or something under it imported, the
:func:`stalker.db.setup` becomes available to let one setup the database.
"""

from sqlalchemy import engine_from_config
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

from stalker.conf import defaults
from stalker.db.declarative import Base 

# SQLAlchemy database engine
engine = None

# SQLAlchemy session manager
DBSession = None

def setup(settings=None):
    """Utility function that helps to connect the system to the given database.
    
    if the database is None then the it setups using the default database in
    the settings file.
    
    :param settings: This is a dictionary which has keys prefixed with
        "sqlalchemy" and shows the settings. The most important one is the
        engine. The default is None, and in this case it uses the settings from
        stalker.conf.defaults.DATABASE_ENGINE_SETTINGS
   """

    global engine
    global DBSession

    if settings is None:
        settings = defaults.DATABASE_ENGINE_SETTINGS

    # create engine
    engine = engine_from_config(settings, 'sqlalchemy.')

    # create the Session class
    DBSession = scoped_session(
        sessionmaker(
            bind=engine,
            **defaults.DATABASE_SESSION_SETTINGS,
            extension=ZopeTransactionExtension()
        )
    )
    
    # create the database
    Base.metadata.create_all(engine)
    
    # init database
    __init_db__()

def __init_db__():
    """fills the database with default values
    """

    if defaults.AUTO_CREATE_ADMIN:
        __create_admin__()

def __create_admin__():
    """creates the admin
    """
    global DBSession
    
    from stalker.models import User, Department
    
    # check if there is already an admin in the database
    if len(DBsession.query(User).\
    filter_by(name=defaults.ADMIN_NAME).all()) > 0:
        #there should be an admin user do nothing
        #print "there is an admin already"
        return
    
    # create the admin department
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
    
    admin_department.created_by = admin
    admin_department.updated_by = admin
    
    DBSession.add(admin)
