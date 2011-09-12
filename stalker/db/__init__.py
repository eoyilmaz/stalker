#-*- coding: utf-8 -*-
"""Database module of Stalker.

Whenever stalker.db or something under it imported, the
:func:`stalker.db.setup` becomes available to let one setup the database.
"""



import sqlalchemy
from stalker.conf import defaults
from stalker import utils
from stalker.core.models import User, Department
from stalker.core.models import Base

# SQLAlchemy database engine
engine = None
secondary_engine = None

# SQLAlchemy session manager
session = None
query = None

# SQLAlchemy metadata
#metadata = sqlalchemy.MetaData()
metadata = Base.metadata

# a couple of helper attributes
__mappers__ = []



#----------------------------------------------------------------------
def setup(database=None, mappers=None):
    """Utillty function that helps to connect the system to the given database.
    
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
      customize SOM and database mapping to add your own classes to SOM
    
    :param engine_settings: the settings for the SQLAlchemy engine
    """
    
    if mappers is None:
        mappers = []
    
    from stalker import db
    
    if database is None:
        database = defaults.DATABASE
    
    # create engine
    db.engine = sqlalchemy.create_engine(
        database, **defaults.DATABASE_ENGINE_SETTINGS
    )
    
    # create the database
    db.metadata.create_all(db.engine)
    
    # create the Session class
    Session = sqlalchemy.orm.sessionmaker(bind=db.engine,
                           **defaults.DATABASE_SESSION_SETTINGS)
    
    # create and save session object to db.sessison
    db.session = Session()
    db.query = db.session.query
    
    # init database
    __init_db__()



#----------------------------------------------------------------------
def __init_db__():
    """fills the database with default values
    """
    
    if defaults.AUTO_CREATE_ADMIN:
        __create_admin__()
    
    #__fill_entity_types_table__()



#----------------------------------------------------------------------
def __create_admin__():
    """creates the admin
    """
    from stalker import db
    
    # check if there is already an admin in the database
    if len(db.session.query(User). \
           filter_by(name=defaults.ADMIN_NAME).all()) > 0:
        #there should be an admin user do nothing
        #print "there is an admin already"
        return
    
    # create the admin department
    admin_department = Department(name=defaults.ADMIN_DEPARTMENT_NAME)
    db.session.add(admin_department)
    
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
    
    db.session.add(admin)
    db.session.commit()



#----------------------------------------------------------------------
def __create_mappers__(mappers):
    """imports the given mapper helper modules, refer to :ref:`mappers` for
    more information about how to create your own mapper modules.
    """
    
    from stalker import db
    
    # 
    # just import the given list of mapper modules and run the setup function,
    # if they are in the correct format all the mapping should be done already
    # by just import ing the mapper helper modules
    #
    
    if db.__mappers__ == mappers:
        return
    
    for _mapper in mappers:
        if _mapper not in db.__mappers__:
            exec("import " + _mapper)
            exec(_mapper + ".setup()")
    
    db.__mappers__ = []
    db.__mappers__.extend(mappers)



#----------------------------------------------------------------------
def __fill_entity_types_table__():
    """fills the entity_types table with the entity_types defined in the
    defaults.CORE_MODEL_CLASSES
    """
    
    from stalker import db
    from stalker.db import tables
    
    # insert the values if there is not any
    
    # get the current values in the table
    conn = db.engine.connect()
    select = sqlalchemy.sql.select([tables.EntityTypes.c.entity_type])
    result = conn.execute(select)
    
    entity_types_db = []
    for row in result:
        entity_types_db.append(row[0])
    
    result.close()
    
    # get the defaults
    
    default_entity_types = []
    
    for full_module_path in defaults.CORE_MODEL_CLASSES:
        import_info = utils.path_to_exec(full_module_path)
        
        exec_ = import_info[0]
        module = import_info[1]
        object_ = import_info[2]
        
        # import the modules
        exec(exec_)
        
        # get the entity_type of the object
        default_entity_types.append( eval(object_+".entity_type") )
    
    # now for all the values not in the table insert them
    for entity_type in default_entity_types:
        if entity_type not in entity_types_db:
            db.engine.execute(
                tables.EntityTypes.insert(),
                entity_type=entity_type
            )


