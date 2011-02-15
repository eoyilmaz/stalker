#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import AssetBase, AssetType, Task, Entity
from stalker.ext.validatedList import ValidatedList






########################################################################
class AssetBaseTester(mocker.MockerTestCase):
    """tests AssetBase class
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
            "name": "Test AssetBase",
            "description": "This is a test AssetBase object",
            "type": self.mock_type1,
            "tasks": [self.mock_task1, self.mock_task2, self.mock_task3],
        }
        
        self.mock_asset_base = AssetBase(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_None(self):
        """testing if nothing happens when the type argument is given as None
        """
        
        self.kwargs["type"] = None
        new_assetBase = AssetBase(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_set_to_None(self):
        """testing if nothing happens when the type attribute is set to None
        """
        
        self.mock_asset_base.type = None
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_not_AssetType_instance(self):
        """testing if a ValueError will be raised when the type argument is not
        an instance of AssetType
        """
        
        test_values = [1, 1.2, "a str", ["a", "str"]]
        
        for test_value in test_values:
            self.kwargs["type"] = test_value
            self.assertRaises(ValueError, AssetBase, **self.kwargs)
    
    
    
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
                self.mock_asset_base,
                "type",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_working_properly(self):
        """testing if the type attribute is working properly
        """
        
        self.mock_asset_base.type = self.mock_type2
        self.assertEquals(self.mock_asset_base.type, self.mock_type2)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_argument_is_None(self):
        """testing if the tasks attribute will be set to empty list if tasks
        argument is given as None
        """
        
        self.kwargs["tasks"] = None
        new_assetBase = AssetBase(**self.kwargs)
        self.assertEquals(new_assetBase.tasks, [])
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_None(self):
        """testing if the tasks attribute will be set to empty list when it is set
        to None
        """
        
        self.mock_asset_base.tasks = None
        self.assertEquals(self.mock_asset_base.tasks, [])
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_argument_is_not_a_list(self):
        """testing if a ValueError will be raised when the tasks argument is not
        a list
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.kwargs["tasks"] = test_value
            self.assertRaises(ValueError, AssetBase, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_not_a_list(self):
        """testing if a ValueError will be raised when the tasks attribute is
        tried to set to a non list object
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_asset_base,
                "tasks",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_argument_is_a_list_of_other_objects_than_Task(self):
        """testing if a ValueError will be raised when the items in the tasks
        argument is not Task instance
        """
        
        test_value = [1, 1.2, "a str", ["a", "list"]]
        self.kwargs["tasks"] = test_value
        self.assertRaises(ValueError, AssetBase, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_set_to_a_list_of_other_objects_than_Task(self):
        """testing if a ValueError will be raised when the items in the tasks
        attribute is not Task instance
        """
        
        test_value = [1, 1.2, "a str", ["a", "list"]]
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_asset_base,
            "tasks",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_element_attributes_are_set_to_other_object_than_Task(self):
        """testing if a ValueError will be raised when trying to set the
        individual elements in the tasks attribute to other objects than a
        Task instance
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                self.mock_asset_base.tasks.__setitem__,
                "0",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_instance_of_ValidatedList(self):
        """testing if the tasks attribute is a ValidatedList instance
        """
        
        self.assertIsInstance(self.mock_asset_base.tasks, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality of two AssetBase objects
        """
        
        new_assetBase1 = AssetBase(**self.kwargs)
        new_assetBase2 = AssetBase(**self.kwargs)
        
        new_entity1 = Entity(**self.kwargs)
        
        self.kwargs["type"] = self.mock_type2
        new_assetBase3 = AssetBase(**self.kwargs)
        
        self.kwargs["name"] = "another name"
        new_assetBase4 = AssetBase(**self.kwargs)
        
        self.assertTrue(new_assetBase1==new_assetBase2)
        self.assertFalse(new_assetBase1==new_assetBase3)
        self.assertFalse(new_assetBase1==new_assetBase4)
        self.assertFalse(new_assetBase3==new_assetBase4)
        self.assertFalse(new_assetBase1==new_entity1)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality of two AssetBase objects
        """
        
        new_assetBase1 = AssetBase(**self.kwargs)
        new_assetBase2 = AssetBase(**self.kwargs)
        
        new_entity1 = Entity(**self.kwargs)
        
        self.kwargs["type"] = self.mock_type2
        new_assetBase3 = AssetBase(**self.kwargs)
        
        self.kwargs["name"] = "another name"
        new_assetBase4 = AssetBase(**self.kwargs)
        
        self.assertFalse(new_assetBase1!=new_assetBase2)
        self.assertTrue(new_assetBase1!=new_assetBase3)
        self.assertTrue(new_assetBase1!=new_assetBase4)
        self.assertTrue(new_assetBase3!=new_assetBase4)
        self.assertTrue(new_assetBase1!=new_entity1)
    
    
    