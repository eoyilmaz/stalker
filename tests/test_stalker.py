#-*- coding: utf-8 -*-
########################################################################
# 
# Copyright (C) 2010  Erkan Ozgur Yilmaz
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 
########################################################################



import unittest
import stalker
import os, shutil



#########################################################################
#class Test_StalkerSettings(unittest.TestCase):
    #"""tests the stalker settings
    #"""
    
    ##----------------------------------------------------------------------
    #def test_serversSettings(self):
        #"""tests if the server paths are existing
        #"""
        #import os
        #from stalker.conf import defaultSettings
        
        ## assert if it is not an instance of tuple
        #assert( isinstance(defaultSettings.PROJECTS_SERVERS, tuple ) )
        
        ## assert if none of the paths are existing
        ## at least one of the project server path should be valid
        ## path[0] the name of the server
        ## path[1] the path of the server
        #self.assertTrue( any( [os.path.exists(path[1]) for path in defaultSettings.PROJECTS_SERVERS] ) )






#########################################################################
#class Test_Stalker(unittest.TestCase):
    #"""tests __init__
    #"""
    
    
    #_testProjectFullPath = None
    
    
    ##----------------------------------------------------------------------
    #def setUp(self):
        #"""prepares the test
        #"""
        ## create a folder in the project server,
        #from stalker.conf import defaultSettings
        
        ## create a dummy project in one of the project path
        #for serverName, serverPath in defaultSettings.PROJECTS_SERVERS:
            #if os.path.exists( serverPath ):
                #self._testProjectFullPath = os.path.join( serverPath, 'STALKER_TEST_PROJECT' )
                #os.mkdir( self._testProjectFullPath )
                #break
    
    
    
    ##----------------------------------------------------------------------
    #def tearDown(self):
        #"""removes the created test elements
        #"""
        ## remove the STALKER_TEST_PROJECT
        #shutil.rmtree( self._testProjectFullPath )
    
    
    
    ###----------------------------------------------------------------------
    ##def test_connectToProject(self):
        ##"""tests stalker.__init__.connectToProject function
        ##"""
        
        ### it should raise an IOError on non existing paths
        ##self.failUnlessRaises( IOError, stalker.connectToProject, '/non-existing-path' )
        
        ### it should raise an IOError for non-existing database for existing paths
        ##self.failUnlessRaises( IOError, stalker.connectToProject, '/home/ozgur' )
        
        ### check if it setted up the settings correctly
        ###from standalone.conf import settings
    
    
    
    ###----------------------------------------------------------------------
    ##def test_createAProject(self):
        ##"""tests stalker.__init__.createAProject function
        ##"""
        
        ### it should connect to the existing databases instead of recreating
        ### them
        ### use the test project
        
        ##stalker.createAProject( self._testProjectFullPath )
        
        ### check if there is a stalker.db file in the full project path
        ##dbFullPath = os.path.join( self._testProjectFullPath,
                                   ##stalker.conf.defaultSettings.DATABASE_NAME
                                   ##)
        ##self.assertTrue( os.path.exists(dbFullPath) )
        
    ##----------------------------------------------------------------------
    #def test_models(self):
        #"""tests the stalker.database.models
        #"""
        
        #from stalker.database import models
        #import elixir
        
        #elixir.setup_all()
        #elixir.create_all()
        
        ## create a user
        #models.User( email=u'eoyilmaz@gmail.com',
                     #first_name=u'Erkan Ozgur',
                     #last_name=u'Yilmaz',
                     #login_name=u'eoyilmaz',
                     #password=u'1234',
                     #task_enabled=True )
        
        #elixir.session.commit()
        