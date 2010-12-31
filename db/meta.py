#-*- coding: utf-8 -*-
"""This module exists to have a singleton metadata. The best way is to hold the
metadata variable in a seperate module (as Guido van Rossum suggested, if I
remember correctly)

"""

from sqlalchemy import MetaData
#from beaker import session as beakerSession


# SQLAlchemy database engine
engine = None

# SQLAlchemy session manager
session = None

# the singleton metadata
metadata = MetaData()

# a couple off helper attributes
__mappers__ = []


## a sessionData for current user session
#beakerSession = session.Session(
    #{},
    #key='stalker',
    #type='file',
    #cookie_expires=True,
    #data_dir='/tmp/cache/data',
    #lock_dir='/tmp/cache/lock'
#)
logged_user = None
