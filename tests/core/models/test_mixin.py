#-*- coding: utf-8 -*-



import datetime
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
    def test_references_attribute_only_accepts_listlike_objects(self):
        """testing if references attribute accepts only list-like objects,
        (objects with __setitem__, __getitem__ methods
        """
        
        test_values = [1, 1.2, "a string"]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_foo_obj,
                "references",
                test_value
            )
    
    
    
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






########################################################################
class ScheduleMixinTester(mocker.MockerTestCase):
    """Tests the ScheduleMixin
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create mock objects
        
        self.start_date = datetime.date.today()
        self.due_date = self.start_date + datetime.timedelta(days=20)
        
        self.kwargs = {
            "name": "Test Schedule Mixin",
            "description": "This is a simple entity object for testing " +
                           "ScheduleMixin",
            "start_date": self.start_date,
            "due_date": self.due_date,
        }
        
        class Bar(object):
            pass
        
        class FooMixedInClass(entity.SimpleEntity, mixin.ScheduleMixin):
            pass
        
        class FooMixedInClass_without_init(Bar, mixin.ScheduleMixin):
            pass
        
        self.FooMixedInClass = FooMixedInClass
        self.FooMixedInClass_without_init = FooMixedInClass_without_init
        
        self.mock_foo_obj = FooMixedInClass(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_start_argument_is_not_a_date_object(self):
        """testing if a ValueError will be raised when the start is given as
        something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            self.kwargs["start_date"] = test_value
            
            self.assertRaises(ValueError, self.FooMixedInClass_without_init,
                              **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_start_attribute_is_not_a_date_object(self):
        """testing if a ValueError will be raised when trying to set the
        start attribute to something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_foo_obj,
                "start_date",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_argument_is_given_as_None_use_the_default_value(self):
        """testing if the start_date argument is given as None, will use the
        today as the start date
        """
        
        self.kwargs["start_date"] = None
        new_foo_obj = self.FooMixedInClass_without_init(**self.kwargs)
        self.assertEquals(new_foo_obj.start_date, datetime.date.today())
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_attribute_is_set_to_None_use_the_default_value(self):
        """testing if setting the start_date attribute to None will update the
        start_date to today
        """
        
        self.mock_foo_obj.start_date = None
        self.assertEquals(self.mock_foo_obj.start_date, datetime.date.today())
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_attribute_works_properly(self):
        """testing if the start propertly is working properly
        """
        
        test_value = datetime.date(year=2011, month=1, day=1)
        self.mock_foo_obj.start_date = test_value
        self.assertEquals(self.mock_foo_obj.start_date, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_not_a_date_or_timedelta_object(self):
        """testing if a ValueError will be raised when trying to set the due
        date something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            self.kwargs["due_date"] = test_value
            self.assertRaises(ValueError, self.FooMixedInClass_without_init,
                              **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_not_a_date_or_timedelta_object(self):
        """testing if a ValueError will be raised when trying to set the due
        attribute is to something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_foo_obj,
                "due_date",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_set_to_None_will_use_the_default_value(self):
        """testing if given the due_date argument given as None will use the
        default value, which is 10 days after the start_date
        """
        
        self.kwargs["due_date"] = None
        new_foo_obj = self.FooMixedInClass_without_init(**self.kwargs)
        self.assertEquals(new_foo_obj.due_date - new_foo_obj.start_date,
                          datetime.timedelta(days=10))
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_set_to_None_will_use_the_default_value(self):
        """testing if setting the due_date attribute to None will use the
        default value, which is 10 days after the start_date
        """
        
        self.mock_foo_obj.due_date = None
        self.assertEquals(
            self.mock_foo_obj.due_date - self.mock_foo_obj.start_date,
            datetime.timedelta(days=10)
        )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_given_as_timedelta_converted_to_datetime(self):
        """testing if due date attribute is converted to a proper
        datetime.date object when due argument is given as a datetime.timedelta
        """
        
        test_value = datetime.timedelta(days=20)
        self.kwargs["due_date"] = test_value
        new_foo_obj = self.FooMixedInClass_without_init(**self.kwargs)
        
        self.assertIsInstance(new_foo_obj.due_date, datetime.date)
        
        self.assertEquals(
            new_foo_obj.due_date - new_foo_obj.start_date,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_set_to_timedelta_converted_to_datetime(self):
        """testing if due date attribute is converted to a proper datetime.date
        object when the due attribute is set to datetime.timedelta
        """
        
        test_value = datetime.timedelta(days=20)
        self.mock_foo_obj.due_date = test_value
        
        self.assertIsInstance(self.mock_foo_obj.due_date, datetime.date)
        
        self.assertEquals(
            self.mock_foo_obj.due_date - self.mock_foo_obj.start_date,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_tried_to_set_to_a_time_before_start_date(self):
        """testing if a ValueError will be raised when the due argument is
        given as a value which is a date before start
        """
        
        self.kwargs["due_date"] = self.kwargs["start_date"] - \
            datetime.timedelta(days=10)
        
        self.assertRaises(ValueError, self.FooMixedInClass_without_init,
                          **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_tried_to_set_to_a_time_before_start_date(self):
        """testing if a ValueError will be raised when the due attribute is
        tried to be set to a date before start
        """
        
        new_due_date = self.mock_foo_obj.start_date - \
                     datetime.timedelta(days=10)
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_foo_obj,
            "due_date",
            new_due_date
        )
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_shifted_when_start_date_passes_it(self):
        """testing if due_date attribute will be shifted when the start_date
        attribute passes it
        """
        
        time_delta = self.mock_foo_obj.due_date - self.mock_foo_obj.start_date
        self.mock_foo_obj.start_date += 2 * time_delta
        
        self.assertEquals(
            self.mock_foo_obj.due_date - self.mock_foo_obj.start_date,
            time_delta
        )
    
    
    
    #----------------------------------------------------------------------
    def test_duration_attribute_is_calculated_correctly(self):
        """testing if the duration attribute is calculated correctly
        """
        
        new_foo_entity = self.FooMixedInClass(self.kwargs)
        new_foo_entity.start_date = datetime.date.today()
        new_foo_entity.due_date = datetime.timedelta(201)
        
        self.assertEquals(new_foo_entity.duration, datetime.timedelta(201))
    
    
    
    #----------------------------------------------------------------------
    def test_duration_attribute_is_read_only(self):
        """testing if the duration attribute is read-only
        """
        
        new_foo_entity = self.FooMixedInClass(self.kwargs)
        self.assertRaises(
            AttributeError, setattr, new_foo_entity, "duration", 10
        )
    
    
    