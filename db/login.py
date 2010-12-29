#-*- coding: utf-8 -*-
"""This utility module helps to create a session
"""


from stalker import db


#----------------------------------------------------------------------
def login(user_name, password, db_uri=None, db_mappers=[]):
    """a login helper for the system
    """
    
    # setup the database
    db.setup(database=db_uri, mappers=db_mappers)
    
    

