#-*- coding: utf-8 -*-



import mocker
from stalker.db import setup_db






########################################################################
class Setup_Db_Tester(mocker.MockerTestCase):
    """tests the stalker.db.setup_db module
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setting up the tests
        """
        
        self.mock_module_path = "stalker.models.tag.Tag"
    
    
    
    #----------------------------------------------------------------------
    def test_get_module_path(self):
        """testing if the get_module_path returns the correct path for a given
        module string
        """
        
        expected_result = "stalker.models.tag"
        
        self.assertEquals(
            setup_db.get_module_path(self.mock_module_path),
            expected_result
        )
    
    
    
    #----------------------------------------------------------------------
    def test_get_obj_name(self):
        """testing if the get_obj_name returns the correct name for a given
        module string
        """
        
        expected_result = "Tag"
        
        self.assertEquals(
            setup_db.get_obj_name(self.mock_module_path),
            expected_result
        )
    
    
    
    #----------------------------------------------------------------------
    def test_module_imports(self):
        """testing if the correct modules and tables are imported
        """
        
        # change the defaults
        assert(isinstance(self.mocker, mocker.Mocker))
        
        # change the import statements
        # try to replace them with test class and a test table later on
        class_path = "stalker.models.tag.Tag"
        table_path = "stalker.db.tables.tags_table"
        
        class_module = "stalker.models.tag"
        table_module = "stalker.db.tables"
        
        mocked_defaults = self.mocker.replace("stalker.conf.defaults")
        import stalker.conf
        
        getattr(
            mocked_defaults,
            'OBJECT_TO_TABLE'
        )
        
        self.mocker.result(
            [(class_path,
             table_path)]
        )
        
        self.mocker.count(0,1000)
        self.mocker.replay()
        
        print stalker.conf.defaults.OBJECT_TO_TABLE
        
        # just call the setup_db.create_mappers and watch for the results
        setup_db.create_mappers()
        
        # check if the class_path and table_path are in sys.modules.keys()
        import sys
        
        module_names = sys.modules.keys()
        self.assertTrue( class_module in module_names )
        self.assertTrue( table_module in module_names )
        
        # delete the imported modules
        exec "del(" + class_module + ")"
        exec "del(" + table_module + ")"
        
        