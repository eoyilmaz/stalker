#-*- coding: utf-8 -*-



import unittest
from stalker.ext import auth
import os
import tempfile
from beaker import session as beakerSession
from stalker import db
from stalker.core.models import User 





#########################################################################
class AuthTester(unittest.TestCase):
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
    
    #----------------------------------------------------------------------
    def test_create_session(self):
        """tests create_session function
        """
	
	auth.create_session()
	self.assertTrue(auth.SESSION != {})
    
    
    #----------------------------------------------------------------------
    def test_logout_function(self):
        """tests logout function
        """
    
        auth.create_session()
        auth.logout()
        self.assertEquals(len(auth.SESSION), 0)

    #-----------------------------------------------------------------------
    def test_autenticate_user_exist(self):
        """Tests the authenticate function when user exists in db
        """
	tempdir = tempfile.gettempdir()
	dbFileAddr = tempdir + "/studio.db"	
	
	# remove db file 
	if os.path.exists(dbFileAddr):
		os.remove(  dbFileAddr) 
	
	# setup a new db 
	db.setup( "sqlite:///" + dbFileAddr )

        testUser = User(first_name="tu",
			last_name="tu",
			login_name="testuser", 
			email="testuser@gmail.com",
			password="test",
			description="This is for test porpose")

        # if user exist does not add him
	user_obj = db.session.query(User).filter_by(name="testuser").first()
	if user_obj == None:
            db.session.add(testUser)
            db.session.commit()
       
        # now the test user is in db and we can authenticate it
        self.assertTrue(auth.authenticate("testuser","test") != None)
	
   #-----------------------------------------------------------------------
    def test_autenticate_user_not_exist(self):
        """tests the authenticate function when there isn't proper user
        """
	tempdir = tempfile.gettempdir()
	dbFileAddr = tempdir + "/studio1.db"	
	
	# remove db file 
	if os.path.exists(dbFileAddr):
		os.remove(  dbFileAddr) 

        
	# create a fresh db
	db.setup("sqlite:///" + dbFileAddr)
        self.assertTrue(auth.authenticate("testuser",auth.set_password("test")) == None)
        
   #-----------------------------------------------------------------------
    def test_autenticate_password_isnot_correct(self):
        """tests the authenticate function when the user's password
        is incorrect
        """
	tempdir = tempfile.gettempdir()
	dbFileAddr = tempdir + "/studio2.db"	
	
	# remove db file 
	if os.path.exists(dbFileAddr):
		os.remove(  dbFileAddr) 

        
	# create a fresh db
	db.setup("sqlite:///" + dbFileAddr)
        
	testUser = User(first_name="tu",
			last_name="tu",
			login_name="testuser", 
			email="testuser@gmail.com",
			password="test",
			description="This is for test porpose")

        # if user exist does not add him
	user_obj = db.session.query(User).filter_by(name="testuser").first()
	if user_obj == None:
            db.session.add(testUser)
            db.session.commit()
       
	
	# use incorrect password 
	self.assertTrue(auth.authenticate("testuser","tes") == None)
        
   
   #-----------------------------------------------------------------------
    def test_login_without_params(self):
        """tests the login function when there is a cookie file
        """

	tempdir = tempfile.gettempdir()

	self.SESSION['user_id'] = "testuser"
        self.SESSION['password'] =  "test"
        self.SESSION.save()
        
	dbFileAddr = tempdir + "/studio3.db"	
	
	# remove db file 
	if os.path.exists(dbFileAddr):
		os.remove(  dbFileAddr) 
	
	# setup a new db 
	db.setup( "sqlite:///" + dbFileAddr )

        testUser = User(first_name="tu",
			last_name="tu",
			login_name="testuser", 
			email="testuser@gmail.com",
			password="test",
			description="This is for test porpose")

        # if user exist does not add him
	user_obj = db.session.query(User).filter_by(name="testuser").first()
	if user_obj == None:
            db.session.add(testUser)
            db.session.commit()

	# now the test user exist in cookie and db so the login method should work
	# without any error
        
	self.assertTrue(auth.login())
       
    #-----------------------------------------------------------------------
    def test_login_with_params_login_result(self):
        """tests the login function when there is not any cookie file
        """

	tempdir = tempfile.gettempdir()

	dbFileAddr = tempdir + "/studio4.db"	
	
	# remove db file 
	if os.path.exists(dbFileAddr):
		os.remove(  dbFileAddr) 
	
	# setup a new db 
	db.setup( "sqlite:///" + dbFileAddr )

        testUser = User(first_name="tu",
			last_name="tu",
			login_name="testuser", 
			email="testuser@gmail.com",
			password="test",
			description="This is for test porpose")

        # if user exist does not add him
	user_obj = db.session.query(User).filter_by(name="testuser").first()
	if user_obj == None:
            db.session.add(testUser)
            db.session.commit()

	# now the test user exist in db so the login method should work
	# without any error. Also the user data should be written in cookie
        
        auth.login("testuser","test")
        self.assertTrue(user_obj != None )
	
	
	
     #-----------------------------------------------------------------------
    def test_login_with_params_cookie_register(self):
        """tests the login function to see the ability of writing user
        data in the cookie file for further use
        """
	
        tempdir = tempfile.gettempdir()

	
        dbFileAddr = tempdir + "/studio5.db"	
	
	# remove db file 
        if os.path.exists(dbFileAddr):
		os.remove(  dbFileAddr) 
	
	# setup a new db 
        db.setup( "sqlite:///" + dbFileAddr )

        testUser = User(first_name="tu",
			last_name="tu",
			login_name="testuser", 
			email="testuser@gmail.com",
			password="test",
			description="This is for test porpose")

        # if user exist does not add him
        user_obj = db.session.query(User).filter_by(name="testuser").first()
        if user_obj == None:
            db.session.add(testUser)
            db.session.commit()

	auth.login("testuser","test")

	session_options = {
        "id":"stalker",
        "key":auth.SESSION_KEY,
        "type":"file",
        "cookie_expires": False,
        "data_dir": os.path.sep.join([tempdir, "stalker_cache", "data"]),
        "lock_dir": os.path.sep.join([tempdir, "stalker_cache", "lock"]),}

        newSession = beakerSession.Session({},**session_options) 
          
       	self.assertTrue('user_id' in newSession and  
			newSession['user_id'] == 'testuser' and 
			'password' in newSession #and 
                        #newSession['password'] == auth.set_password('test')
	                #check_password('test', newSession['password'])
			)
        

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
    
    
    