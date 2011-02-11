#-*- coding: utf-8 -*-
"""This is the authentication system of Stalker. Uses Beaker for the session
management.

This helper module is written to help users to persist their login information
in their system. The aim of this function is not security. So one can quickly
by-pass this system and get himself/herself logged in or query information from
the database without login.

The user information is going to be used in the database to store who created,
updated, read or delete the data.

There are three functions to log a user in, first one is
:func:`~stalker.db.auth.session` that create the session and if there where
user entry in session it return true else return false, the second one is
:func:`~stalker.db.auth.authenticate`, which accepts username and password and
returns a :class:`~stalker.core.models.user.User` object::

    from stalker.db import auth
    user_obj = auth.authenticate("username", "password")

The third one is the :func:`~stalker.db.auth.login` which uses a given
:class:`~stalker.core.models.user.User` object and creates a Beaker Session and
stores the logged in user id in that session.

The :func:`~stalker.db.auth.get_user` can be used to get the authenticated and
logged in :class:`~stalker.core.models.user.User` object.

The basic usage of the system is as follows::
  
  from stalker import db
  from stalker.db import auth
  from stalker.core.models import user
  
  if auth.session():
      # user has login data 
      auth.login()
  else
      #user doesn't have login data get them with login prompt
      get_user_data()
      login(username, password)

The module also introduces a decorator called
:func:`~stalker.db.auth.login_required` to help adding the authentication
functionality to any function or method. There is also another decorator called
:func:`~stalker.db.auth.premission_required` to check if the logged in user is
in the given permission group.
"""


import os
import tempfile
import datetime
from beaker import session as beakerSession
from stalker import db
from stalker.core.models import error, user



SESSION={}
SESSION_KEY = "stalker"



#----------------------------------------------------------------------
def session():
    """create the session and if there was user data entry in the cookie return
    true
    """
    
    from stalker.db import auth
    
    tempdir = tempfile.gettempdir()
    
    # loading session
    session_options = {
        "id":"stalker",
        "key":auth.SESSION_KEY,
        "type":"file",
        "cookie_expires": False,
        "data_dir": os.path.sep.join([tempdir, "stalker_cache", "data"]),
        "lock_dir": os.path.sep.join([tempdir, "stalker_cache", "lock"]),
    }
    
    auth.SESSION = beakerSession.Session({},**session_options)
    
    # checking user data
    return 'user_id' in auth.SESSION and \
           'password' in auth.SESSION



#----------------------------------------------------------------------
def login(username=None, password=None):
    """use this function if session function return true it gets the user data
    and use it to connect to database
    
    use this function if session return false. you should feed this function
    with username and password because it uses them to connect to database. it
    alse write this data to a cookie file for farther use.
    """
    
    from stalker.db import auth
    
    if "user_id" not in auth.SESSION:
        session()
    
    if username and password:
        
        user_obj = authenticate(username, password)
        
        if user_obj is not None:
            
            auth.SESSION['user_id'] = username
            auth.SESSION['password'] =  password
            auth.SESSION.save()
            
            
            user_obj.last_login = datetime.datetime.now()
            db.session.commit()
    
    else:
        if auth.SESSION is not None:
            
            username = auth.SESSION['user_id']
            password = auth.SESSION['password']
            
            user_obj = authenticate(username,password)
            if user_obj is not None:
                auth.SESSION.save()
                user_obj.last_login = datetime.datetime.now()
                db.session.commit()



#----------------------------------------------------------------------
def authenticate(username="", password=""):
    """Authenticates the given username and password, returns a
    stalker.core.models.user.User object

    There needs to be a already setup database for the authentication to hapen.
    """
    
    # check if the database is setup
    if db.session == None:
        raise error.LoginError("stalker is not connected to any db right now, "
                               "use stalker.db.setup(), to setup the default"
                               "db")
    
    # try to get the given user
    user_obj = db.session.query(user.User).filter_by(name=username).first()
    
    error_msg = "user name and login don't match, %s - %s" % \
              (username, password)
    
    if user_obj is None:
        raise(error.LoginError(error_msg))
    
    if user_obj.password != password:
        raise(error.LoginError(error_msg))
    
    return user_obj



#----------------------------------------------------------------------
def logout():
    """removes the current session
    """
    from stalker.db import auth
    
    try:
        auth.SESSION.delete()
        auth.SESSION.clear()
    except AttributeError:
        return



#----------------------------------------------------------------------
def login_required(view, error_message=None):
    """a decorator that implements login functionality to any function or
    method

    :param view: a function returning True or False, thus verifying the entered
      user name and password

    :param error_message: the message to be shown in case a LoginError is
      raised, a default message will be shown when skipped

    :returns: the decorated function
    """

    def wrap(func):
        def wrapped_func(*args, **kwargs):
            if view():
                func(*args, **kwargs)
            else:
                if error_message and isinstance(error_meesage, (str, unicode)):
                    raise error.LoginError(error_message)
                else:
                    raise error.LoginError("You should be logged in before "
                                           "completing your action!")
        return wrapped_func
    return wrap



#----------------------------------------------------------------------
def permission_required(permission_group, error_message=None):
    """a decorator that implements permission checking to any function or
    method

    Checks if the logged in user is in the given permission group and then
    calls the decorated function

    :param permission_group: a :class:`~stalker.coer.models.group.Group` object
      showing the permision group

    :param error_message: the message to be shown in case a LoginError is
      raised, a default message will be shown when skipped

    :returns: the decorated function
    """

    def wrap(func):
        def wrapped_func(*args, **kwargs):
            if get_user() in permission_group:
                func(*args, **kwargs)
            else:
                if error_message and isinstance(error_meesage, (str, unicode)):
                    raise error.LoginError(error_message)
                else:
                    raise error.LoginError("You don't have permission to do "
                                           "complete your action!")
        return wrapped_func
    return wrap