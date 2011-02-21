#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import Asset, AssetType, Task, Entity
from stalker.ext.validatedList import ValidatedList






########################################################################
class AssetTester(mocker.MockerTestCase):
    """tests Asset class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.mock_type1 = self.mocker.mock(AssetType)
        self.mock_type2 = self.mocker.mock(AssetType)
        
        self.mock_task1 = self.mocker.mock(Task)
        self.mock_task2 = self.mocker.mock(Task)
        self.mock_task3 = self.mocker.mock(Task)
        
        self.mocker.replay()
        
        self.kwargs = {
            "name": "Test Asset",
            "description": "This is a test Asset object",
            "type": self.mock_type1,
            "tasks": [self.mock_task1, self.mock_task2, self.mock_task3],
        }
        
        self.mock_asset = Asset(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_None(self):
        """testing if nothing happens when the type argument is given as None
        """
        
        self.kwargs["type"] = None
        new_asset = Asset(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_set_to_None(self):
        """testing if nothing happens when the type attribute is set to None
        """
        
        self.mock_asset.type = None
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_not_AssetType_instance(self):
        """testing if a ValueError will be raised when the type argument is not
        an instance of AssetType
        """
        
        test_values = [1, 1.2, "a str", ["a", "str"]]
        
        for test_value in test_values:
            self.kwargs["type"] = test_value
            self.assertRaises(ValueError, Asset, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_not_AssetType_instance(self):
        """testing if a ValueError will be raised when the type attribute is
        tried to be set to something other than a AssetType instance
        """
        
        test_values = [1, 1.2, "a str", ["a", "str"]]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_asset,
                "type",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_working_properly(self):
        """testing if the type attribute is working properly
        """
        
        self.mock_asset.type = self.mock_type2
        self.assertEquals(self.mock_asset.type, self.mock_type2)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality of two Asset objects
        """
        
        new_asset1 = Asset(**self.kwargs)
        new_asset2 = Asset(**self.kwargs)
        
        new_entity1 = Entity(**self.kwargs)
        
        self.kwargs["type"] = self.mock_type2
        new_asset3 = Asset(**self.kwargs)
        
        self.kwargs["name"] = "another name"
        new_asset4 = Asset(**self.kwargs)
        
        self.assertTrue(new_asset1==new_asset2)
        self.assertFalse(new_asset1==new_asset3)
        self.assertFalse(new_asset1==new_asset4)
        self.assertFalse(new_asset3==new_asset4)
        self.assertFalse(new_asset1==new_entity1)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality of two Asset objects
        """
        
        new_asset1 = Asset(**self.kwargs)
        new_asset2 = Asset(**self.kwargs)
        
        new_entity1 = Entity(**self.kwargs)
        
        self.kwargs["type"] = self.mock_type2
        new_asset3 = Asset(**self.kwargs)
        
        self.kwargs["name"] = "another name"
        new_asset4 = Asset(**self.kwargs)
        
        self.assertFalse(new_asset1!=new_asset2)
        self.assertTrue(new_asset1!=new_asset3)
        self.assertTrue(new_asset1!=new_asset4)
        self.assertTrue(new_asset3!=new_asset4)
        self.assertTrue(new_asset1!=new_entity1)
    
    
    