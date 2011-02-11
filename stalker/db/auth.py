"""This is the authentication system of Stalker. Uses Beaker for the session
management.

This helper module is written to help users to persist their login information
in their system. The aim of this function is not security. So one can quickly
by-pass this system and get himself/herself logged in or query information from
the database without login.

The user information is going to be used in the database to store who created,
updated, read or delete the data.

There are three functions to log a user in, first one is
:func:`~stalker.db.auth.session` that create the session and if there where user
entry in session it return true else return false
:func:`~stalker.db.auth.authenticate`, which accepts username and password and
returns a :class:`~stalker.core.models.user.User` object::
    
    from stalker.db import auth
    userObj = auth.authenticate("username", "password")

The third one is the :func:`~stalker.db.auth.login` which uses a given
:class:`~stalker.core.models.user.User` object and creates a Beaker Session and
stores the logged in user id in that session.

The :func:`~stalker.db.auth.get_user` can be used to get the authenticated and
logged in :class:`~stalker.core.models.user.User` object.

The basic usage of the system is as follows::
    
    	from stalker import db
	from stalker.db import auth
	from stalker.core.models import user
    	
	if session():
		# user has login data 
		login()
	else
		#user doesn't have login data get them with login prompt
		get_user_data()
		login(username,password)

The module also introduces a decorator called
:func:`~stalker.db.auth.login_required` to help adding the authentication
functionality to any function or method
"""


import os
import tempfile
import datetime
import functools
from beaker import session as beakerSession
from stalker import db
from stalker.core.models import error, user



SESSION={}
SESSION_KEY = "stalker"

#----------------------------------------------------------------------
def session():
	"""create the session and if there was user data entry in the 
	cookie return true
	"""

	tempdir = tempfile.gettempdir()
	
	returnVal = False
	
	# loading session
	session_options = {"id":"stalker",
			"key":SESSION_KEY,
			"type":"file",
			"cookie_expires": False,
			"data_dir": os.path.sep.join([tempdir, "stalker_cache", "data"]),
			"lock_dir": os.path.sep.join([tempdir, "stalker_cache", "lock"]),
			}

	SESSION = beakerSession.Session({},**session_options)
	
	# checking user data
	returnVal = 'user_id' in SESSION and 'password' in SESSION
	return returnVal
	
#----------------------------------------------------------------------
def login():
	"""use this function if session function return true
	it gets the user data and use it to connect to database
	"""

	if SESSION is not None:
		
		username = SESSION['user_id']
		password = SESSION['password']
		
		if authenticate(username,password) :
			SESSION.save()
			user_obj.last_login = datetime.datetime.now()
			db.session.commit()
		
#----------------------------------------------------------------------
def login(username,password):
	"""use this function if session return false. you should
	feed this function with username and password because it uses
	them to connect to database.
	it alse write this data to a cookie file for farther use.
	"""

	if authenticate( username, password):
		
		SESSION['user_id'] = username
		SESSION['password'] =  password
		SESSION.save()
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
        raise(error.LoginError("stalker is not connected to any db right now, \
use stalker.db.setup(), to setup the default db"))
    
    # try to get the given user
    userObj = db.session.query(user.User).filter_by(name=username).first()
    
    error_msg = "user name and login don't match, %s - %s" % \
              (username, password)
    
    if userObj is None:
        raise(error.LoginError(error_msg))
    
    if userObj.password != password:
        raise(error.LoginError(error_msg))
    
    return userObj


#----------------------------------------------------------------------
def logout():
    """removes the current session
    """
    
    try:
        SESSION.delete()
        SESSION.clear()
    except AttributeError:
        return

