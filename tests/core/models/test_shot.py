#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import Entity, Shot, Sequence, AssetType, Task






########################################################################
class ShotTester(mocker.MockerTestCase):
    """Tests the Shot class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create a Sequence
        self.mock_sequence = self.mocker.mock(Sequence)
        
        # create an AssetType
        self.assetType = self.mocker.mock(AssetType)
        
        # create mock Tasks
        #self.
    
    