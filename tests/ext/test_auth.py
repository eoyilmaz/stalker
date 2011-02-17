#-*- coding: utf-8 -*-



import unittest
from stalker.ext import auth






#########################################################################
#class AuthTest(unittest.TestCase):
    #"""Tests the stalker.ext.auth module
    #"""
    
    
    ##----------------------------------------------------------------------
    #def setUp(self):
        #"""setup the test
        #"""
        #tempdir = tempfile.gettempdir()
        
        #session_options = {
            #"id":"stalker",
            #"key":"stalker",
            #"type":"file",
            #"cookie_expires": False,
            #"data_dir": os.path.sep.join([tempdir, "stalker_cache", "data"]),
            #"lock_dir": os.path.sep.join([tempdir, "stalker_cache", "lock"]),
        #}
        
        #self.SESSION = beakerSession.Session({},**session_options) 
        ##self.SESSION.save()
    
    
    
    ##----------------------------------------------------------------------
    #def test_session_function_True(self):
        #"""the aim of this test needs to be expalined here
        #"""
        
        #self.SESSION['user_id'] = "name"
        #self.SESSION['password'] =  "pass"
        #self.SESSION.save()
        
        #self.assertTrue(auth.create_session())
    
    
    
    ##----------------------------------------------------------------------
    #def test_session_function_False(self):
        #"""the aim of this test needs to be expalined here
        #"""
        #del self.SESSION['user_id']
        #del self.SESSION['password']
        #self.SESSION.save()
        
        #self.assertFalse(auth.create_session())
    
    
    
    ##----------------------------------------------------------------------
    #def test_logout_function(self):
        #"""the aim of this test needs to be expalined here
        #"""
        
        #auth.create_session()
        #auth.logout()
        #self.assertEquals(len(auth.SESSION), 0)






########################################################################
class PasswordTester(unittest.TestCase):
    """tests stalker.ext.auth.check_password and stalker.ext.auth.set_password
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setUp the test
        """
        
        self.raw_pass = "1234"
        self.enc_pass = "MTIzNA==\n"
    
    
    
    #----------------------------------------------------------------------
    def test_check_password_1(self):
        """testing if False will be returned for variety of situations.
        """
        
        test_values = [(None, None, False),
                       (self.raw_pass, None, False),
                       (None, self.enc_pass, False),
                       ("", "", True),
                       (self.raw_pass, "", False),
                       ("", self.enc_pass, False),
                       (self.raw_pass, "1234", False),
                       (self.raw_pass, 1234, False),
                       (self.raw_pass, self.enc_pass, True),
                       (1234, self.enc_pass, True),
                       ]
        
        for raw_pass, enc_pass, result in test_values:
            #print "r:%s e:%s res:%s" % (raw_pass, enc_pass, result)
            self.assertEquals( auth.check_password(raw_pass, enc_pass), result)
    
    
    
    #----------------------------------------------------------------------
    def test_set_password_working_properly(self):
        """testing if the set_password function is working properly.
        """
        
        enc_password = auth.set_password(self.raw_pass)
        self.assertEquals(enc_password, self.enc_pass)
    
    
    
    #----------------------------------------------------------------------
    def test_set_password_raw_password_None(self):
        """testing if a ValueError will be raised when the raw_password is None
        """
        
        self.assertRaises(ValueError, auth.set_password, None)
    
    
    
    #----------------------------------------------------------------------
    def test_set_password_raw_password_empty_string(self):
        """testing if a ValueError will be raised when the raw_password is
        empty string
        """
        
        self.assertRaises(ValueError, auth.set_password, "")
    
    
    