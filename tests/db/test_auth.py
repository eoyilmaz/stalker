



import unittest
import os
import tempfile
import datetime
import functools
from beaker import session as beakerSession
import auth


class Auth_TestCase(unittest.TestCase):
    
	

	
	def setUp(self):
		
		
		tempdir = tempfile.gettempdir()
		
		session_options = {"id":"stalker",
				"key":"stalker",
				"type":"file",
				"cookie_expires": False,
				"data_dir": os.path.sep.join([tempdir, "stalker_cache", "data"]),
				"lock_dir": os.path.sep.join([tempdir, "stalker_cache", "lock"]),
				}

		self.SESSION = beakerSession.Session({},**session_options) 
		#self.SESSION.save()
		
	def test_session_function_True(self):

		self.SESSION['user_id'] = "name"
		self.SESSION['password'] =  "pass"
		self.SESSION.save()

		self.failUnless(auth.session() == True)

	def test_session_function_False(self):

		del self.SESSION['user_id']
		del self.SESSION['password']
		self.SESSION.save()

		self.failUnless(auth.session() == False)
	
	def test_logout_function(self):

		auth.session()
		auth.logout()
		self.failUnless(len(auth.SESSION) == 0 )


