#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import Entity, Shot, Sequence, Asset, AssetType, Task






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
        self.mock_assetType = self.mocker.mock(AssetType)
        
        # create mock Tasks
        self.mock_task1 = self.mocker.mock(Task)
        self.mock_task2 = self.mocker.mock(Task)
        self.mock_task3 = self.mocker.mock(Task)
        
        # create mock Assets
        self.mock_asset1 = self.mocker.mock(Asset)
        self.mock_asset2 = self.mocker.mock(Asset)
        self.mock_asset3 = self.mocker.mock(Asset)
        
        self.kwargs = {
            "type": self.mock_assetType,
            
        }
        
        
    
    
    
    