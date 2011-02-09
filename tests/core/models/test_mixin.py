#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import entity, mixin, link, status
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
    def test_references_attribute_accepting_empty_list(self):
        """testing if references attribute accepting empty lists
        """
        
        self.mock_foo_obj.references = []
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_accepting_only_lists_with_link_instances(self):
        """testing if references attribute accepting only lists with Link
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
    def test_references_attribute_working_properly(self):
        """testing if references attribute working properly
        """
        
        self.mock_foo_obj.references = self.mock_links
        
        self.assertEquals(self.mock_foo_obj.references, self.mock_links)
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_is_a_ValidatedList_instance(self):
        """testing if the references attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_foo_obj.references, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_elements_accepts_Link_only(self):
        """testing if a ValueError will be raised when trying to assign
        something other than a Link object to the references list
        """
        
        # append
        self.assertRaises(
            ValueError,
            self.mock_foo_obj.references.append,
            0
        )
        
        # __setitem__
        self.assertRaises(
            ValueError,
            self.mock_foo_obj.references.__setitem__,
            0,
            0
        )
    
    
    
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
        new_link = link.Link(name="NewTestLink", path="nopath",
                             filename="nofilename", type=image_link_type)
        
        test_value = [new_link]
        
        myGreatEntity.references = test_value
        
        self.assertEquals(myGreatEntity.references, test_value)






########################################################################
class StatusMixinTester(mocker.MockerTestCase):
    """tests the StatusMixin class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        assert(isinstance(self.mocker, mocker.Mocker))
        
        # a mock StatusList object
        self.mock_status_list1 = self.mocker.mock(status.StatusList)
        self.expect(len(self.mock_status_list1.statuses)).result(5).\
            count(0, None)
        
        self.expect(self.mock_status_list1.target_entity_type).\
            result("Dummy").count(0, None)
        
        # another mock StatusList object
        self.mock_status_list2 = self.mocker.mock(status.StatusList)
        self.expect(len(self.mock_status_list2.statuses)).result(5)\
            .count(0, None)
        
        self.expect(self.mock_status_list2.target_entity_type).\
            result("Dummy").count(0, None)
        
        #self.mock_status_list1.__eq__(self.mock_status_list2)
        #self.mocker.result(False)
        #self.mocker.count(0, None)
        
        #self.mock_status_list1.__ne__(self.mock_status_list2)
        #self.mocker.result(True)
        #self.mocker.count(0, None)
        
        self.mocker.replay()
        
        
        
        self.kwargs = {
            "status_list": self.mock_status_list1,
            "status": 0,
        }
        
        # create a dummy class
        class Dummy(object):
            entity_type = "Dummy"
            def __init__(self):
                pass
        
        # create another dummy to test the mixin init method
        class DummyWithoutInit(object):
            entity_type = "Dummy"
            pass
        
        
        class MixedClass(Dummy, mixin.StatusMixin):
            pass
        
        class MixedClass_with_MixinInit(DummyWithoutInit, mixin.StatusMixin):
            pass
        
        self.mock_class_for_init_test = MixedClass_with_MixinInit
        
        self.mock_mixed_obj = MixedClass()
        self.mock_mixed_obj.status_list = self.mock_status_list1
        
        # create another one without status_list set to something
        self.mock_mixed_obj2 = MixedClass()
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_1(self):
        """testing if ValueError is going to be raised when trying to
        initialize status_list with something other than a StatusList
        """
        
        testValues = [100, "", 100.2]
        
        for testValue in testValues:
            self.kwargs["status_list"] = testValue
            self.assertRaises(ValueError, self.mock_class_for_init_test,
                              **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_2(self):
        """testing if ValueError is going to be raised when trying to
        initialize status_list with None
        """
        self.kwargs["status_list"] = None
        self.assertRaises(ValueError, self.mock_class_for_init_test,
                          **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_attribute_set_to_something_other_than_StatusList(self):
        """testing if ValueError is going to be raised when trying to set the
        status_list to something else than a StatusList object
        """
        
        test_values = [ "a string", 1.0, 1, {"a": "statusList"}]
        
        for test_value in test_values:
            # now try to set it
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_mixed_obj,
                "status_list",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_attribute_set_to_None(self):
        """testing if ValueError is going to be raised when trying to set the
        status_list to None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_mixed_obj,
            "status_list",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_being_omited(self):
        """testing if a ValueError going to be raised when omiting the
        status_list argument
        """
        self.kwargs.pop("status_list")
        self.assertRaises(ValueError, self.mock_class_for_init_test,
                          **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_suitable_for_the_current_class(self):
        """testing if a TypeError will be raised when the
        Status.target_entity_class is not compatible with the current
        class
        """
        
        # create a new status list suitable for another class with different
        # entity_type
        
        
        new_status_list = status.StatusList(
            name="Sequence Statuses",
            statuses=[
                status.Status(name="On Hold", code="OH"),
                status.Status(name="Complete", code="CMPLT"),
            ],
            target_entity_type="Sequence"
        )
        
        self.assertRaises(
            TypeError,
            setattr,
            self.mock_mixed_obj,
            "status_list",
            new_status_list
        )
        
        new_suitable_list = status.StatusList(
            name="Suitable Statuses",
            statuses=[
                status.Status(name="On Hold", code="OH"),
                status.Status(name="Complete", code="CMPLT"),
            ],
            target_entity_type="Dummy"
        )
        
        # this shouldn't raise any error
        self.mock_mixed_obj.status_list = new_suitable_list
    
    
    
    #----------------------------------------------------------------------
    def test_status_argument_set_to_None(self):
        """testing if a ValueError will be raised when setting the status
        argument to None
        """
        self.kwargs["status"] = None
        self.assertRaises(ValueError, self.mock_class_for_init_test,
                          **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_attribute_set_to_None(self):
        """testing if a ValueError will be raised when setting the status
        attribute to None
        """
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_mixed_obj,
            "status",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_argument_different_than_an_int(self):
        """testing if a ValueError is going to be raised if trying to
        initialize status with something else than an integer
        """
        
        # with a string
        test_values = ["0", 1.2, [0]]
        
        for test_value in test_values:
            self.kwargs["status"] = test_value
            self.assertRaises(ValueError, self.mock_class_for_init_test,
                              **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_attribute_set_to_other_than_int(self):
        """testing if ValueError going to be raised when trying to set the
        current status to something other than an integer
        """
        
        test_values = ["a string", 1.2, [1], {"a": "status"}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_mixed_obj,
                "status",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_status_attribute_set_to_too_high(self):
        """testing if a ValueError is going to be raised when trying to set the
        current status to something higher than it is allowd to, that is it
        couldn't be set a value higher than len(statusList.statuses - 1)
        """
        
        test_value = len(self.mock_status_list1.statuses)
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_mixed_obj,
            "status",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_attribute_set_before_status_list(self):
        """testing if a ValueError will be raised when trying to set the status
        attribute to some value before having a StatusList object in
        status_list attribute
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_mixed_obj2,
            "status",
            0,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_attribute_set_to_too_low(self):
        """testing if a ValueError is going to be raised when trying to set the
        current status to something lower than it is allowed to, that is it
        couldn't be set to value lower than 0
        """
        
        test_value = -1
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_mixed_obj,
            "status",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_attribute_works_properly(self):
        """testing if the status attribute works properly
        """
        
        test_value = 1
        
        self.mock_mixed_obj.status = test_value
        self.assertEquals(self.mock_mixed_obj.status, test_value)


