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
:func:`stalker.ext.auth.session` that create the session and if there where
user entry in session it return true else return false, the second one is
:func:`stalker.ext.auth.authenticate`, which accepts username and password and
returns a :class:`stalker.core.models.User` object::

    from stalker.ext import auth
    user_obj = auth.authenticate("username", "password")

The third one is the :func:`stalker.ext.auth.login` which uses a given
:class:`stalker.core.models.User` object and creates a Beaker Session and
stores the logged in user id in that session.

The :func:`stalker.ext.auth.get_user` can be used to get the authenticated and
logged in :class:`stalker.core.models.User` object.

The basic usage of the system is as follows::

  from stalker import db
  from stalker.ext import auth
  from stalker.core.models import User

  if "user_id" in auth.SESSION:
      # user has login data 
      auth.login()
  else
      #user doesn't have login data get them with login prompt
      get_user_data()
      auth.login(username, password)

The module also introduces a decorator called
:func:`stalker.ext.auth.login_required` to help adding the authentication
functionality to any function or method. There is also another decorator called
:func:`stalker.ext.auth.premission_required` to check if the logged in user is
in the given permission group.

There are also two utility functions two check and set passwords.
:func:`stalker.ext.auth.check_password` and
:func:`stalker.ext.auth.set_password`.
"""



import os
import tempfile
import datetime
import base64

from beaker import session as beakerSession

from stalker import db
from stalker.core.errors import LoginError, DBError
from stalker.core.models import User



SESSION={}
SESSION_ID = "stalker"
SESSION_KEY = "_auth_user_id"



#----------------------------------------------------------------------
def create_session():
    """Creates the beaker.session object.
    
    Stalker creates a session to store currently logged in user data. This
    function creates the session and stores it in the
    :const:`stalker.ext.auth.SESSION` dictionary.
    """
    
    from stalker.ext import auth
    
    tempdir = tempfile.gettempdir()
    
    # loading session
    session_options = {
        "id":auth.SESSION_ID,
        "type":"file",
        "cookie_expires": False,
        "data_dir": os.path.sep.join([tempdir, "stalker_cache", "data"]),
        "lock_dir": os.path.sep.join([tempdir, "stalker_cache", "lock"]),
    }
    
    auth.SESSION = beakerSession.Session({}, **session_options)
    auth.SESSION.save()



#----------------------------------------------------------------------
def login(user=None):
    """Persists the user_id in a session.
    
    The idea behind login is to store the user in a session and retrieve it
    back without asking the credentials over and over again by getting the user
    from the session it self.
    
    The user id is saved in the session.
    
    This should not mixed with the authentication where the user is
    authenticated against the given username and password. This functions
    purpose is to store the user in a session.
    
    :param user: The user object which wanted to be logged in. Can be given as
      None then the user id in the session will be used. And if there are no
      session and thus the user id in the session is None than a loggin error
      will be raised. So by this way the user is logged in only one time.
    
    :type user: :class:`stalker.core.models.User`
    """
    
    from stalker.ext import auth
    
    #if "user_id" not in auth.SESSION:
        #create_session()
    
    #if username and password:
        
        #user_obj = authenticate(username, password)
        
        #if user_obj is not None:
            
            #auth.SESSION['user_id'] = username
            #auth.SESSION['password'] =  password
            #auth.SESSION.save()
            
            #user_obj.last_login = datetime.datetime.now()
            #db.session.commit()
            
            #return True
        #else:
            #return False
        
    ## the username and password should be given from cookie file
    #else:
        #if auth.SESSION is not None:
            
            #username = auth.SESSION['user_id']
            #password = auth.SESSION['password']
            
            #user_obj = authenticate(username, password)
            #if user_obj is not None:
                #auth.SESSION.save()
                #user_obj.last_login = datetime.datetime.now()
                #db.session.commit()
                
                #return True
            #else:
                #return False
        #else:
            #return False
    
    
    # log the user if the current session id matches the given user id
    
    if user is None:
        try:
            logged_user_id = auth.SESSION[auth.SESSION_KEY]
        except KeyError:
            raise LoginError("There is no previous session, please supply a "
                             "user, for the first time.")
        else:
            user = db.query(User).\
                   filter_by(id=SESSION[auth.SESSION_KEY]).\
                   first()
    
    if not isinstance(user, User):
        raise ValueError("user must be a stalker.core.models.User instance")
    
    user.last_login = datetime.datetime.now()
    db.session.commit()
    
    # store the user-id in the SESSION
    if auth.SESSION_KEY in auth.SESSION:
        if auth.SESSION[SESSION_KEY] != user.id:
            auth.SESSION[SESSION_KEY] = user.id
    else:
        # create the session with given session id
        create_session()
        auth.SESSION[SESSION_KEY] = user.id




#----------------------------------------------------------------------
def authenticate(username="", password=""):
    """Authenticates the given username and password, returns a
    stalker.core.models.User object
    
    There needs to be a already setup database for the authentication to hapen.
    """
    
    user_obj = None
    
    # check if the database is setup
    if db.session == None:
        raise DBError("stalker is not connected to any db right now, use "
                      "stalker.db.setup(), to setup the default database")
    
    # try to get the given user
    user_obj = db.session.query(User).filter_by(name=username).first()
    
    error_msg = "user name and login don't match, %s" % username
    
    if user_obj is None:
        raise LoginError(error_msg)
    
    if not check_password(password, user_obj.password):
        print password
        print user_obj.password
        raise LoginError(error_msg)
    
    return user_obj



#----------------------------------------------------------------------
def logout():
    """removes the current session
    """
    from stalker.ext import auth
    
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
                    raise LoginError(error_message)
                else:
                    raise LoginError("You should be logged in before "
                                     "completing your action!")
        return wrapped_func
    return wrap



#----------------------------------------------------------------------
def permission_required(permission_group, error_message=None):
    """a decorator that implements permission checking to any function or
    method
    
    Checks if the logged in user is in the given permission group and then
    calls the decorated function
    
    :param permission_group: a :class:`~stalker.core.models.Group` object
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
                    raise LoginError(error_message)
                else:
                    raise LoginError("You don't have permission to complete "
                                     "your action!")
        return wrapped_func
    return wrap



#----------------------------------------------------------------------
def check_password(raw_password, enc_password):
    """Checks the given raw password.
    
    Checks the given raw password with the given encrypted password. Handles
    the encryption process behind the scene.
    
    :param raw_password: The password.
    
    :param enc_password: The encrypted password.
    
    :returns: bool
    """
    
    return enc_password == base64.encodestring(str(raw_password))



#----------------------------------------------------------------------
def set_password(raw_password):
    """Returns an encrypted version of the given password.
    
    :param string raw_password: The raw password to be encrypted. The
      raw_password attribute can not be None or empty string.
      
    :returns: string
    """
    
    if raw_password is None or raw_password == "":
        raise ValueError("raw_password can not be None or empty string")
    
    return base64.encodestring(raw_password)


