#-*- coding: utf-8 -*-



import datetime
import mocker

from stalker.core.mixins import ReferenceMixin
from stalker.core.models import (SimpleEntity, Entity, Link, Type)
from stalker.ext.validatedList import ValidatedList






########################################################################
class ReferenceMixinTester(mocker.MockerTestCase):
    """tests the ReferenceMixin
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create a couple of mock Link objects
        self.mock_link1 = self.mocker.mock(Link)
        self.mock_link2 = self.mocker.mock(Link)
        self.mock_link3 = self.mocker.mock(Link)
        self.mock_link4 = self.mocker.mock(Link)
        self.mock_entity1 = self.mocker.mock(Entity)
        self.mock_entity2 = self.mocker.mock(Entity)
        
        self.mocker.replay()
        
        self.mock_links = [
            self.mock_link1,
            self.mock_link2,
            self.mock_link3,
            self.mock_link4,
        ]
        
        # create a SimpleEntitty and mix it with the ReferenceMixin
        class Foo(SimpleEntity, ReferenceMixin):
            pass
        
        self.mock_foo_obj = Foo(name="Ref Mixin Test")
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_accepting_empty_list(self):
        """testing if references attribute accepting empty lists
        """
        
        self.mock_foo_obj.references = []
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_only_accepts_listlike_objects(self):
        """testing if references attribute accepts only list-like objects,
        (objects with __setitem__, __getitem__ methods
        """
        
        test_values = [1, 1.2, "a string"]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_foo_obj,
                "references",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_accepting_only_lists_of_Entity_instances(self):
        """testing if references attribute accepting only lists with Entity
        instances and derivatives
        """
        
        test_value = [1,2.2,["a reference as list"],"some references"]
        
        self.assertRaises(
            TypeError,
            setattr,
            self.mock_foo_obj,
            "references",
            test_value
        )
        
        # and test if it is accepting a proper list
        
        test_value = [self.mock_entity1, self.mock_entity2, self.mock_link1]
        self.mock_foo_obj.references = test_value
        self.assertItemsEqual(test_value, self.mock_foo_obj.references)
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_working_properly(self):
        """testing if references attribute working properly
        """
        
        self.mock_foo_obj.references = self.mock_links
        self.assertEqual(self.mock_foo_obj.references, self.mock_links)
        
        test_value = [self.mock_entity1, self.mock_entity2]
        self.mock_foo_obj.references = test_value
        self.assertItemsEqual(self.mock_foo_obj.references, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_is_a_ValidatedList_instance(self):
        """testing if the references attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_foo_obj.references, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_elements_accepts_Entity_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than an instance of Entity or its derived classes to
        the references list
        """
        
        # append
        self.assertRaises(
            TypeError,
            self.mock_foo_obj.references.append,
            0
        )
        
        # __setitem__
        self.assertRaises(
            TypeError,
            self.mock_foo_obj.references.__setitem__,
            0,
            0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_references_application_test(self):
        """testing an example of ReferenceMixin usage
        """
        
        class GreatEntity(SimpleEntity, ReferenceMixin):
            pass
        
        myGreatEntity = GreatEntity(name="Test")
        # we should have a references attribute right now
        myGreatEntity.references
        
        image_link_type = Type(name="Image", target_entity_type="Link")
        new_link = Link(name="NewTestLink", path="nopath",
                        filename="nofilename", type=image_link_type)
        
        test_value = [new_link]
        
        myGreatEntity.references = test_value
        
        self.assertEqual(myGreatEntity.references, test_value)






