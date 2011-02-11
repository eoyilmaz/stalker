#-*- coding: utf-8 -*-



import unittest
import os
import tempfile
from beaker import session as beakerSession
from stalker.db import auth






########################################################################
class AuthTest(unittest.TestCase):
    """Tests the stlaker.db.auth module
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        tempdir = tempfile.gettempdir()
        
        session_options = {
            "id":"stalker",
            "key":"stalker",
            "type":"file",
            "cookie_expires": False,
            "data_dir": os.path.sep.join([tempdir, "stalker_cache", "data"]),
            "lock_dir": os.path.sep.join([tempdir, "stalker_cache", "lock"]),
        }
        
        self.SESSION = beakerSession.Session({},**session_options) 
        #self.SESSION.save()
    
    
    
    #----------------------------------------------------------------------
    def test_session_function_True(self):
        """the aim of this test needs to be expalined here
        """
        
        self.SESSION['user_id'] = "name"
        self.SESSION['password'] =  "pass"
        self.SESSION.save()
        
        self.assertTrue(auth.session())
    
    
    
    #----------------------------------------------------------------------
    def test_session_function_False(self):
        """the aim of this test needs to be expalined here
        """
        del self.SESSION['user_id']
        del self.SESSION['password']
        self.SESSION.save()
        
        self.assertFalse(auth.session())
    
    
    
    #----------------------------------------------------------------------
    def test_logout_function(self):
        """the aim of this test needs to be expalined here
        """
        
        auth.session()
        auth.logout()
        self.assertEquals(len(auth.SESSION), 0)


