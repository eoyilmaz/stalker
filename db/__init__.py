#-*- coding: utf-8 -*-
"""This is the database module of Stalker.

Whenever stalker.db or something under it imported, the
:func:`~stalker.db.setup` becomes available to let one setup the database.
"""



from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import create_engine
from stalker.conf import defaults
from stalker.db import tables, meta



#----------------------------------------------------------------------
def setup(database=None, mappers=[]):
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
    
    # create engine
    meta.engine = create_engine(database, **defaults.DATABASE_ENGINE_SETTINGS)
    
    # extend the default mappers with the given mappers list
    defaults.MAPPERS.extend(mappers)
    
    # create mappers
    create_mappers(defaults.MAPPERS)
    
    # create the database
    meta.metadata.create_all(meta.engine)
    
    # create the Session class
    Session = sessionmaker(bind=meta.engine)
    
    # create and save session object to stalker.db.meta.sessison
    meta.session = Session()
    
    # init database
    #__init_db__()



#----------------------------------------------------------------------
def __init_db__():
    """fills the database with default values
    """
    
    # check the admin setting
    if defaults.AUTO_CREATE_ADMIN:
        # insert a new admin to the USERS table
        from stalker.models import user, department
        
        # create the admin department
        adminDep = department.Department(name='admins')
        meta.session.add(adminDep)
        
        
        tempUser = user.User(
            name='temp',
            first_name='temp',
            login_name='temp',
            password='temp',
            department=adminDep,
            email='temp@temp.com'
        )
        
        admin = user.User(
            name=defaults.ADMIN_NAME,
            first_name=defaults.ADMIN_NAME,
            login_name=defaults.ADMIN_NAME,
            password=defaults.ADMIN_PASSWORD,
            email=defaults.ADMIN_EMAIL,
            department=adminDep,
            created_by=tempUser
        )
        
        admin.created_by = admin
        admin.updated_by = admin
        
        meta.session.add(admin)
        meta.session.commit()



#----------------------------------------------------------------------
def create_mappers(mapper_list):
    """imports the given mapper helper modules, refer to :ref:`mappers` for
    more information about how to create your own mapper modules.
    """
    
    # 
    # just import the given list of mapper modules, if they are in the correct
    # format all the mapping should be done already by just import ing the
    # mapper helper modules
    # 
    
    for _mapper in mapper_list:
        exec("import " + _mapper)
    
    




