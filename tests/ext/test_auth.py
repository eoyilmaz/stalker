#-*- coding: utf-8 -*-



import mocker

from stalker.conf import defaults
from stalker import db
from stalker.core.models import User
from stalker.core.errors import LoginError, DBError
from stalker.ext import auth






########################################################################
class AuthTester(mocker.MockerTestCase):
    """Tests the stlaker.ext.auth module
    """
    
    
    
    #----------------------------------------------------------------------
    def test_login_with_user_argument_is_None(self):
        """testing if a LoginError will be raised when the user is None and
        there are no session
        """
        
        auth.SESSION = {}
        
        self.assertRaises(LoginError, auth.login, None)
    
    
    
    #----------------------------------------------------------------------
    def test_login_with_user_argument_is_None_in_the_second_time(self):
        """testing if the user is logged in without any problem if it is logged
        in before
        """
        
        auth.SESSION = {}
        
        # use the admin user for this test
        db.setup()
        admin = db.query(User).filter_by(name=defaults.ADMIN_NAME).first()
        
        # log the user in for the first time
        auth.login(admin)
        
        # log the user in for the second time
        # this should not raise any error
        auth.login(None)
    
    
    
    #----------------------------------------------------------------------
    def test_login_with_user_argument_is_not_User_instance(self):
        """testing if a LoginError will be raised when the user is not a User
        instance
        """
        
        self.assertRaises(ValueError, auth.login, 123)
    
    
    
    #----------------------------------------------------------------------
    def test_login_creates_a_session(self):
        """testing if a proper session with the session key is set to the user
        id
        """
        
        auth.SESSION = {}
        
        # setup the database
        db.setup()
        
        # login with admin
        admin = db.query(User).filter_by(name=defaults.ADMIN_NAME).first()
        
        # log the user in
        auth.login(admin)
        
        # now check if the value for the key session_id is equal to the
        # admin.id
        
        self.assertEquals(auth.SESSION[auth.SESSION_KEY], admin.id)
    
    
    
    #----------------------------------------------------------------------
    def test_login_with_another_user(self):
        """testing if the session will be deleted before login with a different
        user
        """
        
        # clear the session
        auth.SESSION = {}
        
        # setup the database
        db.setup()
        
        # login with admin
        admin = db.query(User).filter_by(name=defaults.ADMIN_NAME).first()
        
        # log the admin in
        auth.login(admin)
        
        admin_session = auth.SESSION.copy()
        
        # now create a different user
        new_user = User(first_name="Erkan Ozgur", last_name="Yilmaz",
                        login_name="eoyilmaz", password="1234",
                        email="ozgur@yilmaz.com")
        
        # get an id for the user
        db.session.add(new_user)
        db.session.commit()
        
        # log in with new user
        auth.login(new_user)
        
        # check if the session is renewed
        self.assertNotEqual(auth.SESSION, admin_session)
        
        # check if the session_id is changed
        self.assertNotEqual(auth.SESSION[auth.SESSION_KEY],
                            admin_session[auth.SESSION_KEY])
        
        # check if the session id matches the user id
        self.assertEquals(auth.SESSION[auth.SESSION_KEY],
                          new_user.id)
    
    
    
    #----------------------------------------------------------------------
    def test_authenticate_without_a_db(self):
        """testing if a ValueError will be raised whne there are no db setup
        yet
        """
        
        # clear the mappers and the database
        db.session = None
        #db.__mappers__ = []
        
        self.assertRaises(DBError, auth.authenticate, defaults.ADMIN_NAME,
                          defaults.ADMIN_PASSWORD)
    
    
    
    #----------------------------------------------------------------------
    def test_authenticate_returns_a_User_instance(self):
        """testing if authenticate returns a stalker.core.models.User instance
        """
        
        # use the default admin user to check
        db.setup()
        
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        self.assertIsInstance(admin, User)
    
    
    
    #----------------------------------------------------------------------
    def test_authenticate_non_existent_user(self):
        """testing if a LoginError will be raised when the given user
        information is not correct
        """
        
        db.setup()
        
        self.assertRaises(LoginError,
                          auth.authenticate,
                          "non_existent", "user")
    
    
    
    #----------------------------------------------------------------------
    def test_logout_deletes_the_content_of_SESSION(self):
        """testing if logout deletes the content of the auth.SESSION
        """
        
        # first login with admin
        db.setup()
        
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        auth.login(admin)
        
        # check if SESSION has SESSION_KEY
        self.assertTrue(auth.SESSION_KEY in auth.SESSION)
        
        # then logout
        auth.logout()
        
        # and check if the SESSION doesn't have SESSION_KEY
        self.assertTrue(auth.SESSION_KEY not in auth.SESSION)
    
    
    
    #----------------------------------------------------------------------
    def test_logout_without_login(self):
        """testing if logout greacefully handles logging out wihtout first
        using login function
        """
        
        auth.SESSION = {}
        
        # now try to logout
        auth.logout()






########################################################################
class PasswordTester(mocker.MockerTestCase):
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
            self.assertEquals(auth.check_password(raw_pass, enc_pass), result)
    
    
    
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
    
    
    