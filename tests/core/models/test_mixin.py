#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import entity, mixin, link





########################################################################
class ReferenceMixinTester(mocker.MockerTestCase):
    """tests the ReferenceMixin
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create a couple of mock Link objects
        self.mock_link1 = self.mocker.mock(link.Link)
        self.mock_link2 = self.mocker.mock(link.Link)
        self.mock_link3 = self.mocker.mock(link.Link)
        self.mock_link4 = self.mocker.mock(link.Link)
        
        self.mocker.replay()
        
        self.mock_links = [
            self.mock_link1,
            self.mock_link2,
            self.mock_link3,
            self.mock_link4,
        ]
        
        # create a SimpleEntitty and mix it with the ReferenceMixin
        class Foo(entity.SimpleEntity, mixin.ReferenceMixin):
            pass
        
        self.mock_foo_obj = Foo(name="Ref Mixin Test")
    
    
    
    #----------------------------------------------------------------------
    def test_references_property_accepting_empty_list(self):
        """testing if references property accepting empty lists
        """
        
        self.mock_foo_obj.references = []
    
    
    
    #----------------------------------------------------------------------
    def test_references_property_accepting_only_lists_with_link_instances(self):
        """testing if references property accepting only lists with Link
        instances
        """
        
        test_value = [1,2.2,["a reference as list"],"some references"]
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_foo_obj,
            "references",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_references_property_working_properly(self):
        """testing if references property working properly
        """
        
        self.mock_foo_obj.references = self.mock_links
        
        self.assertEquals(self.mock_foo_obj.references, self.mock_links)
    
    
    
    #----------------------------------------------------------------------
    def test_references_application_test(self):
        """testing an example of ReferenceMixin usage
        """
        
        from stalker.core.models import mixin, entity, link, types
        
        class GreatEntity(entity.SimpleEntity, mixin.ReferenceMixin):
            pass
        
        myGreatEntity = GreatEntity(name="Test")
        myGreatEntity.references
        
        image_link_type = types.LinkType(name="Image")
        new_link = link.Link(name="NewTestLink", path="nopath", filename="nofilename", type=image_link_type)
        
        test_value = [new_link]
        
        myGreatEntity.references = test_value
        
        self.assertEquals(myGreatEntity.references, test_value)
    
    
    