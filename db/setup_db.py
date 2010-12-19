#-*- coding: utf-8 -*-
"""
The mapper is a utility to help do the mapping. It first reads the
config.defaults and uses the OBJECT_TO_TABLE list to import the objects and
tables and then map them together.
"""


from sqlalchemy.orm import mapper, sessionmaker
from stalker.conf import defaults
from stalker.db import tables



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
    
    
    engine = create_engine('sqlite:///:memory:')
    session.configure(bind=engine)
    # You probably need to create some tables and 
    # load some test data, do so here.
    
    # To create tables, you typically do:
    model.metadata.create_all(engine)



#----------------------------------------------------------------------
def get_db_address():
    """reads the database address from the config
    """
    
    pass





#----------------------------------------------------------------------
def create_mappers():
    ## tags
    #mapper(stalker.models.tag.Tag, stalker.db.tables.tags_table)
    
    ## simple entity
    #mapper(entity.SimpleEntity, tables.simpleEntity_table)
    
    # there should be a concept that holds all these objects to table
    # connections in this config file and it should be in the default config
    # file and it should be read by the system, then overriddin by the user
    # this can also lead us to the solution of the user configuration part of
    # the system
    
    for obj_table in defaults.OBJECT_TO_TABLE:
        
        # get object info
        obj_path = obj_table[0]
        obj_module = get_module_path(obj_path)
        obj_name = get_obj_name(obj_path)
        
        # get table info
        table_path = obj_table[1]
        table_module = get_module_path(table_path)
        table_name = get_obj_name(table_path)
        
        exec("import "+obj_module)
        exec("import "+table_module)
        
        # create the mapper
        exec "mapper(" + obj_path + "," + table_path + ")"
    
    # create the engine
    
    # create a session
    #Session = sessionmaker(bind=engine)



#----------------------------------------------------------------------
def get_module_path(import_string):
    """returns the module path of the given absolute import_string
    
    returns stalker.models.tag for stalker.models.tag.Tag
    """
    
    return '.'.join(import_string.split('.')[:-1])



#----------------------------------------------------------------------
def get_obj_name(import_string):
    """returns the object name for the given absolute import string
    
    returns Tag for stalker.models.tag.Tag
    """
    
    return import_string.split('.')[-1]
    




