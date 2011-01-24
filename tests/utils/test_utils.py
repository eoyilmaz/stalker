#-*- coding: utf-8 -*-



import unittest
from stalker import utils




########################################################################
class UtilsTester(unittest.TestCase):
    """tests the stalker.utils
    """
    
    
    
    #----------------------------------------------------------------------
    def test_path_to_exec(self):
        """testing if a correct string will be returned with path_to_exec
        """
        
        full_path = "stalker.core.models.asset.Asset"
        
        expected_result = ("from stalker.core.models.asset import Asset",
                           "stalker.core.models.asset",
                           "Asset")
        
        self.assertEquals(
            utils.path_to_exec(full_path),
            expected_result
        )
    