#-*- coding: utf-8 -*-
"""This is the database module of Stalker.

Whenever stalker.db or something under it imported, the
:func:`~stalker.db.setup` becomes available to let one setup the database.
"""

import sqlalchemy

# SQLAlchemy database engine
engine = None

# SQLAlchemy session manager
session = None
query = None

# SQLAlchemy metadata
metadata = sqlalchemy.MetaData()

# a couple of helper attributes
__mappers__ = []



#----------------------------------------------------------------------
def setup(database=None, mappers=[]):
    """
    This is a utillty function that helps to connect the system to the given
    database.
    
    if the database is None then the it setups using the default database in
    the settings file.
    
    These are the steps:
     1. creates the engine, and stores it in stalker.db.engine
     2. creates the mappers, adds the given mappers to the
        stalker.conf.defaults.MAPPERS list
     3. creates the session and binds the engine to it, and stores the session
        in stalker.db.session
    
    :param database: The database address, default is None, and in this case it
      uses the database defined in stalker.conf.defaults.DATABASE
    
    :param mappers: The additional mappers module. Use this parameter to
      customize the whole SOM and database mapping to add your own classes to
      SOM
    
    :param engine_settings: the settings for the SQLAlchemy engine
    """
    
    from stalker.db import __setup__
    __setup__.__setup__(database, mappers)


