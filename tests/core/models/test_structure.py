#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import user, structure, types






########################################################################
class StructureTester(mocker.MockerTestCase):
    """tests the stalker.core.models.structure.Structure class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """seting up the tests
        """
        
        # create mocks
        
        # mock_user
        self.mock_user = self.mocker.mock(user.User)
        
        # mock type templates
        self.asset_template1 = self.mocker.mock(types.TypeTemplate)
        self.asset_template2 = self.mocker.mock(types.TypeTemplate)
        
        self.asset_templates = [self.asset_template1, self.asset_template2]
        
        self.reference_template1 = self.mocker.mock(types.TypeTemplate)
        self.reference_template2 = self.mocker.mock(types.TypeTemplate)
        
        self.reference_templates = [self.reference_template1,
                                    self.reference_template2]
        
        self.mocker.replay()
        
        # keyword arguments
        self.kwargs = {
            "name": "Test Structure",
            "description": "This is a tets structure",
            "created_by": self.mock_user,
            "project_template": "some template which is not important",
            "asset_templates": self.asset_templates,
            "reference_templates": self.reference_templates,
        }
        
        self.mock_structure = structure.Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_template_argument_accepts_string_only(self):
        """testing if project_template parameter accepts string or unicodes
        """
        
        test_values = [1, 1.0, ["a string"], {"a": "dictionary"}]
        
        for test_value in test_values:
            
            self.kwargs["project_template"] = test_value
            
            self.assertRaises(ValueError, structure.Structure, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_template_argument_accepts_empty_string(self):
        """testing if project_template parameter accepts None without error
        """
        
        self.kwargs["project_template"] = ""
        
        # should't raise any errors
        new_structure = structure.Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_template_property_accepts_string_only(self):
        """testing if project_template property accepts string or unicodes
        """
        
        test_values = [1, 1.0, ["a string"], {"a": "dictionary"}]
        
        for test_value in test_values:
            
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_structure,
                "project_template",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_asset_templates_argument_accepts_list_of_templates_only(self):
        """testing if asset_templates argument accepts list of
        :class:`~stalker.core.models.types.TypeTemplate` objects only
        """
        
        test_values = [1, 1.0, ["a string"], {"a": "dictionary"}]
        
        # these all should raise ValueErrors
        for test_value in test_values:
            
            self.kwargs["asset_templates"] = test_value
            
            self.assertRaises(ValueError, structure.Structure, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_asset_templates_property_accepts_list_of_templates_only(self):
        """testing if asset_templates argument accepts list of
        :class:`~stalker.core.models.types.TypeTemplate` objects only
        """
        
        test_values = [1, 1.0, ["a string"], {"a": "dictionary"}]
        
        # these all should raise ValueErrors
        for test_value in test_values:
            
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_structure,
                "asset_templates",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_asset_templates_argument_accepts_empty_list(self):
        """testing if asset_templates argument accepts empty lists
        """
        
        # this should work properly wihtou raising an error
        self.kwargs["asset_templates"] = []
        
        a_new_structure = structure.Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_reference_templates_argument_accepts_list_of_templates_only(self):
        """testing if reference_templates argument accepts list of
        :class:`~stalker.core.models.types.TypeTemplate` objects only
        """
        
        test_values = [1, 1.0, ["a string"], {"a": "dictionary"}]
        
        # these all should raise ValueErrors
        for test_value in test_values:
            
            self.kwargs["reference_templates"] = test_value
            
            self.assertRaises(ValueError, structure.Structure, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_reference_templates_property_accepts_list_of_templates_only(self):
        """testing if reference_templates argument accepts list of
        :class:`~stalker.core.models.types.TypeTemplate` objects only
        """
        
        test_values = [1, 1.0, ["a string"], {"a": "dictionary"}]
        
        # these all should raise ValueErrors
        for test_value in test_values:
            
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_structure,
                "reference_templates",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_reference_templates_argument_accepts_empty_list(self):
        """testing if reference_templates argument accepts empty lists
        """
        
        # this should work properly wihtou raising an error
        self.kwargs["reference_templates"] = []
        
        a_new_structure = structure.Structure(**self.kwargs)
    
    
    