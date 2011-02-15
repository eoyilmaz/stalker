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
        
        full_path = "stalker.core.models.Asset"
        
        expected_result = ("from stalker.core.models import Asset",
                           "stalker.core.models",
                           "Asset")
        
        self.assertEquals(
            utils.path_to_exec(full_path),
            expected_result
        )
    