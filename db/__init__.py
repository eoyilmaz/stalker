#-*- coding: utf-8 -*-
"""This is the database module of Stalker.

Whenever stalker.db or something under it imported, the
:func:`~stalker.db.setup` becomes available to let one setup the database.
"""



from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import create_engine
from stalker.conf import defaults
from stalker.db import tables, meta
from stalker.models import user, department



#----------------------------------------------------------------------
def setup(database=None, mappers=[], engine_settings=None):
    """
    This is a utillty function that helps to connect the system to the given
    database.
    
    if the database is None then the it setups using the default database in
    the settings file.
    
    These are the steps:
     1. creates the engine, and stores it in stalker.db.meta.engine
     2. creates the mappers, adds the given mappers to the
        stalker.conf.defaults.MAPPERS list
     3. creates the session and binds the engine to it, and stores the session
        in stalker.db.meta.session
    
    :param database: The database address, default is None, and in this case it
      uses the database defined in stalker.conf.defaults.DATABASE
    
    :param mappers: The additional mappers module. Use this parameter to
      customize the whole SOM and database mapping to add your own classes to
      SOM
    """
    
    if database is None:
        database = defaults.DATABASE
    
    #if engine_settings is not None:
        #defaults.DATABASE_ENGINE_SETTINGS.
    
    # create engine
    meta.engine = create_engine(database, **defaults.DATABASE_ENGINE_SETTINGS)
    
    # extend the default mappers with the given mappers list
    defaults.MAPPERS.extend(mappers)
    
    # create mappers
    __create_mappers__(defaults.MAPPERS)
    
    # create the database
    meta.metadata.create_all(meta.engine)
    
    # create the Session class
    Session = sessionmaker(bind=meta.engine)
    
    # create and save session object to stalker.db.meta.sessison
    meta.session = Session()
    
    # init database
    __init_db__()



#----------------------------------------------------------------------
def __init_db__():
    """fills the database with default values
    """
    
    if defaults.AUTO_CREATE_ADMIN:
        __create_admin__()



#----------------------------------------------------------------------
def __create_admin__():
    """creates the admin
    """
    
    # check if there is already an admin in the database
    if len(meta.session.query(user.User). \
           filter_by(name=defaults.ADMIN_NAME).all()) > 0:
        #there should be an admin user do nothing
        #print "there is an admin already"
        return
    
    # create the admin department
    adminDep = department.Department(name=defaults.ADMIN_DEPARTMENT_NAME)
    meta.session.add(adminDep)
    
    # create the admin user
    admin = user.User(
        name=defaults.ADMIN_NAME,
        first_name=defaults.ADMIN_NAME,
        login_name=defaults.ADMIN_NAME,
        password=defaults.ADMIN_PASSWORD,
        email=defaults.ADMIN_EMAIL,
        department=adminDep,
        #created_by=tempUser
    )
    
    admin.created_by = admin
    admin.updated_by = admin
    
    adminDep.created_by = admin
    adminDep.updated_by = admin
    
    meta.session.add(admin)
    #meta.session.delete(tempUser)
    meta.session.commit()



#----------------------------------------------------------------------
def __create_mappers__(mappers):
    """imports the given mapper helper modules, refer to :ref:`mappers` for
    more information about how to create your own mapper modules.
    """
    
    # 
    # just import the given list of mapper modules and run the setup function,
    # if they are in the correct format all the mapping should be done already
    # by just import ing the mapper helper modules
    #
    
    if meta.__mappers__ == mappers:
        print "not creating any new mapper"
        print "current meta.__mappers__ list:"
        print meta.__mappers__
        
        return
    
    
    print "creating mappers"
    
    for _mapper in mappers:
        exec("import " + _mapper)
        exec(_mapper + ".setup()")
    
    meta.__mappers__ = mappers




