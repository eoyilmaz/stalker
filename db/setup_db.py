#-*- coding: utf-8 -*-
"""
The mapper is a utility to help do the object relational mapping. It first
reads the config.defaults and uses the OBJECT_TO_TABLE list to import the
objects and tables and then map them together.
"""


from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import create_engine
from stalker.conf import defaults
from stalker.db import tables, meta



#----------------------------------------------------------------------
def do_setup():
    """
    This is a utillty function that helps to connect the system to the given
    database in the config file.
    
    These are the steps:
     1. It reads the config.py file to get the database address of the studio 
     2. creates the engine
     3. creates the metadata
     4. reads the database tables
     5. reads the object model of stalker
     6. creates the mapper
     7. creates the session and binds the engine to it
     8. returns the session
    
    """
    
    meta.engine = create_engine(defaults.DATABASE, echo=True)
    
    # create the mappers according to the config
    create_mappers(defaults.MAPPERS)
    
    # To create tables, you typically do:
    meta.metadata.create_all(meta.engine)
    
    # create a session
    Session = sessionmaker(bind=meta.engine)
    
    # save session object
    meta.session = Session()



#----------------------------------------------------------------------
def get_db_address():
    """reads the database address from the config
    """
    
    return defaults.DATABASE





#----------------------------------------------------------------------
def create_mappers(mapper_list):
    # there should be a concept that holds all these objects to table
    # connections in this config file and it should be in the default config
    # file and it should be read by the system, then overriding by the user
    # this can also lead us to the solution of the user configuration part of
    # the system
    
    for _mapper in mapper_list:
        exec("import " + _mapper)





