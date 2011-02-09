#-*- coding: utf-8 -*-
"""This is the authentication system of Stalker. Uses Beaker for the session
management.

This helper module is written to help users to persist their login information
in their system. The aim of this function is not security. So one can quickly
by-pass this system and get himself/herself logged in or query information from
the database without login.

The user information is going to be used in the database to store who created,
updated, read or delete the data.

There are two functions to log a user in, first one is
:func:`~stalker.db.auth.authenticate`, which accepts username and password and
returns a :class:`~stalker.core.models.user.User` object::
    
    from stalker.db import auth
    userObj = auth.authenticate("username", "password")

The second one is the :func:`~stalker.db.auth.login` which uses a given
:class:`~stalker.core.models.user.User` object and creates a Beaker Session and
stores the logged in user id in that session.

The :func:`~stalker.db.auth.get_user` can be used to get the authenticated and
logged in :class:`~stalker.core.models.user.User` object.

The basic usage of the system is as follows::
    
    from stalker import db
    from stalker.db import auth
    from stalker.core.models import user
    
    # directly get the user from the database if there is a user_id
    # in the current auth.SESSION
    # 
    # in this way we prevent asking the user for login information all the time
    if "user_id" in auth.SESSION:
        userObj = auth.get_user()
    else:
        # ask the username and password of the user
        # then authenticate the given user
        username, password = the_interface_for_login()
        userObj = auth.authenticate(username, password)
    
    # login with the given user.User object, this will also create the session
    # if there is no one defined
    auth.login(userObj)

The module also introduces a decorator called
:func:`~stalker.db.auth.login_required` to help adding the authentication
functionality to any function or method. There is also another decorator called
:func:`~stalker.db.auth.premission_required` to check if the logged in user is
in the given permission group.
"""

import os
import tempfile
import datetime
import functools
from beaker import session as beakerSession
from stalker import db
from stalker.core.models import error, user



SESSION = {}
SESSION_KEY = "stalker_key"
SESSION_VALIDATE_KEY = "stalker_validate_key"



#----------------------------------------------------------------------
def create_session():
    """creates the session
    """
    
    tempdir = tempfile.gettempdir()
    
    session_options = {
        "id": "0",
        "type": "file",
        "cookie_expires": False,
        "data_dir": os.path.sep.join([tempdir, "stalker_cache", "data"]),
        "lock_dir": os.path.sep.join([tempdir, "stalker_cache", "lock"]),
        "key": SESSION_KEY,
        "validate_key": SESSION_VALIDATE_KEY,
    }
    
    SESSION = beakerSession.Session({}, **session_options)
    SESSION.save()



#----------------------------------------------------------------------
def authenticate(username="", password=""):
    """Authenticates the given username and password, returns a
    stalker.core.models.user.User object
    
    There needs to be a already setup database for the authentication to hapen.
    """
    
    # check if the database is setup
    if db.session == None:
        raise error.LoginError("stalker is not connected to any db right now, "
                               "use stalker.db.setup(), to setup the default "
                               "db")
    
    # try to get the given user
    userObj = db.session.query(user.User).filter_by(name=username).first()
    
    error_msg = "user name and login don't match, %s - %s" % \
              (username, password)
    
    if userObj is None:
        raise error.LoginError(error_msg)
    
    if userObj.password != password:
        raise error.LoginError(error_msg)
    
    return userObj



#----------------------------------------------------------------------
def login(user_obj):
    """Persist a user id in the session. This way a user doesn't have to
    reauthenticate on every request
    """
    
    user_obj.last_login = datetime.datetime.now()
    db.session.commit()
    
    if "user_id" not in SESSION:
        # create the session first
        create_session()
    
    SESSION.update({"user_id": user_obj.id})
    SESSION.save()



#----------------------------------------------------------------------
def logout():
    """removes the current session
    """
    
    try:
        SESSION.delete()
        SESSION = {}
    except AttributeError:
        return



#----------------------------------------------------------------------
def get_user():
    """returns the user from stored session
    """
    
    # check if the database is setup
    if db.session == None:
        raise error.LoginError("stalker is not connected to any db right now, "
                               "use stalker.db.setup(), to setup the default "
                               "db")
    
    # create the session dictionary
    create_session()
    
    if "user_id" in SESSION:
        # create the session
        return db.session.query(user.User).\
               filter_by(id=SESSION["user_id"]).first()
    else:
        return None



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


