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
def setup(database=None, mappers=[], engine_settings=None):
    
    from stalker.db import __setup__
    __setup__.__setup__(database, mappers, engine_settings)


