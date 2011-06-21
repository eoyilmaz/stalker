#-*- coding: utf-8 -*-



import datetime
import mocker
from stalker.conf import defaults
from stalker.core.models import (SimpleEntity, ReferenceMixin, StatusMixin,
                                 ScheduleMixin, Link, Status, StatusList, Task,
                                 TaskMixin, Type)
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
    def test_references_attribute_accepting_only_lists_with_link_instances(self):
        """testing if references attribute accepting only lists with Link
        instances
        """
        
        test_value = [1,2.2,["a reference as list"],"some references"]
        
        self.assertRaises(
            TypeError,
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
        
        self.assertEqual(self.mock_foo_obj.references, self.mock_links)
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_is_a_ValidatedList_instance(self):
        """testing if the references attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_foo_obj.references, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_references_attribute_elements_accepts_Link_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Link object to the references list
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
        myGreatEntity.references
        
        image_link_type = Type(name="Image", target_entity_type="Link")
        new_link = Link(name="NewTestLink", path="nopath",
                        filename="nofilename", type=image_link_type)
        
        test_value = [new_link]
        
        myGreatEntity.references = test_value
        
        self.assertEqual(myGreatEntity.references, test_value)






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
        self.mock_status_list1 = self.mocker.mock(StatusList)
        self.expect(len(self.mock_status_list1.statuses)).result(5).\
            count(0, None)
        
        self.expect(self.mock_status_list1.target_entity_type).\
            result("Dummy").count(0, None)
        
        # another mock StatusList object
        self.mock_status_list2 = self.mocker.mock(StatusList)
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
        
        
        class MixedClass(Dummy, StatusMixin):
            pass
        
        class MixedClass_with_MixinInit(DummyWithoutInit, StatusMixin):
            pass
        
        self.mock_class_for_init_test = MixedClass_with_MixinInit
        
        self.mock_mixed_obj = MixedClass()
        self.mock_mixed_obj.status_list = self.mock_status_list1
        
        # create another one without status_list set to something
        self.mock_mixed_obj2 = MixedClass()
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_1(self):
        """testing if TYpeError is going to be raised when trying to
        initialize status_list with something other than a StatusList
        """
        
        testValues = [100, "", 100.2]
        
        for testValue in testValues:
            self.kwargs["status_list"] = testValue
            self.assertRaises(TypeError, self.mock_class_for_init_test,
                              **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_2(self):
        """testing if TypeError is going to be raised when trying to
        initialize status_list with None
        """
        self.kwargs["status_list"] = None
        self.assertRaises(TypeError, self.mock_class_for_init_test,
                          **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_attribute_set_to_something_other_than_StatusList(self):
        """testing if TypeError is going to be raised when trying to set the
        status_list to something else than a StatusList object
        """
        
        test_values = [ "a string", 1.0, 1, {"a": "statusList"}]
        
        for test_value in test_values:
            # now try to set it
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_mixed_obj,
                "status_list",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_attribute_set_to_None(self):
        """testing if TypeError is going to be raised when trying to set the
        status_list to None
        """
        
        self.assertRaises(
            TypeError,
            setattr,
            self.mock_mixed_obj,
            "status_list",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_being_omited(self):
        """testing if a TypeError going to be raised when omiting the
        status_list argument
        """
        self.kwargs.pop("status_list")
        self.assertRaises(TypeError, self.mock_class_for_init_test,
                          **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_suitable_for_the_current_class(self):
        """testing if a TypeError will be raised when the
        Status.target_entity_class is not compatible with the current
        class
        """
        
        # create a new status list suitable for another class with different
        # entity_type
        
        
        new_status_list = StatusList(
            name="Sequence Statuses",
            statuses=[
                Status(name="On Hold", code="OH"),
                Status(name="Complete", code="CMPLT"),
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
        
        new_suitable_list = StatusList(
            name="Suitable Statuses",
            statuses=[
                Status(name="On Hold", code="OH"),
                Status(name="Complete", code="CMPLT"),
            ],
            target_entity_type="Dummy"
        )
        
        # this shouldn't raise any error
        self.mock_mixed_obj.status_list = new_suitable_list
    
    
    
    #----------------------------------------------------------------------
    def test_status_argument_set_to_None(self):
        """testing if a TypeError will be raised when setting the status
        argument to None
        """
        self.kwargs["status"] = None
        self.assertRaises(TypeError, self.mock_class_for_init_test,
                          **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_attribute_set_to_None(self):
        """testing if a TypeError will be raised when setting the status
        attribute to None
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.mock_mixed_obj,
            "status",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_argument_different_than_an_int(self):
        """testing if a TypeError is going to be raised if trying to
        initialize status with something else than an integer
        """
        
        # with a string
        test_values = ["0", 1.2, [0]]
        
        for test_value in test_values:
            self.kwargs["status"] = test_value
            self.assertRaises(TypeError, self.mock_class_for_init_test,
                              **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_attribute_set_to_other_than_int(self):
        """testing if TypeError going to be raised when trying to set the
        current status to something other than an integer
        """
        
        test_values = ["a string", 1.2, [1], {"a": "status"}]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
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
        """testing if a TypeError will be raised when trying to set the status
        attribute to some value before having a StatusList object in
        status_list attribute
        """
        
        self.assertRaises(
            TypeError,
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
        self.assertEqual(self.mock_mixed_obj.status, test_value)






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
        self.duration = datetime.timedelta(days=10)
        
        self.kwargs = {
            "name": "Test Schedule Mixin",
            "description": "This is a simple entity object for testing " +
                           "ScheduleMixin",
            "start_date": self.start_date,
            "due_date": self.due_date,
            "duration": self.duration,
        }
        
        class Bar(object):
            pass
        
        class Foo(object):
            def __init__(self, **kwargs):
                pass
        
        # a class which derives from another which has and __init__ already
        class FooMixedInClass(Foo, ScheduleMixin):
            def __init__(self, **kwargs):
                super(FooMixedInClass, self).__init__(**kwargs)
                ScheduleMixin.__init__(self, **kwargs)
        
        # another class which doesn't have an __init__
        class FooMixedInClass_without_init(Bar, ScheduleMixin):
            pass
        
        self.FooMixedInClass = FooMixedInClass
        self.FooMixedInClass_without_init = FooMixedInClass_without_init
        
        self.mock_foo_obj = FooMixedInClass(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_argument_is_not_a_date_object(self):
        """testing if defaults will be used for the start_date attribute when
        the start_date is given as something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            self.kwargs["start_date"] = test_value
            
            new_foo_obj = self.FooMixedInClass_without_init(**self.kwargs)
            
            self.assertEqual(new_foo_obj.start_date,
                             new_foo_obj.due_date - new_foo_obj.duration)
            
            self.assertEqual(new_foo_obj.due_date, self.kwargs["due_date"])
            self.assertEqual(new_foo_obj.duration, self.kwargs["duration"])
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_attribute_is_not_a_date_object(self):
        """testing if the defaults will be used when trying to set the
        start_date attribute to something other than a datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"]]
        
        for test_value in test_values:
            
            due_date = self.mock_foo_obj.due_date
            duration = self.mock_foo_obj.duration
            
            self.mock_foo_obj.start_date = test_value
            
            self.assertEqual(
                self.mock_foo_obj.start_date,
                self.mock_foo_obj.due_date - self.mock_foo_obj.duration
            )
            
            # check if we still have the same due_date
            self.assertEqual(self.mock_foo_obj.due_date, due_date)
            
            # check if we still have the same duration
            self.assertEqual(self.mock_foo_obj.duration, duration)
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_attribute_is_set_to_None_use_the_default_value(self):
        """testing if setting the start_date attribute to None will update the
        start_date to today
        """
        
        self.mock_foo_obj.start_date = None
        self.assertEqual(self.mock_foo_obj.start_date, datetime.date.today())
    
    
    
    #----------------------------------------------------------------------
    def test_start_date_attribute_works_properly(self):
        """testing if the start propertly is working properly
        """
        
        test_value = datetime.date(year=2011, month=1, day=1)
        self.mock_foo_obj.start_date = test_value
        self.assertEqual(self.mock_foo_obj.start_date, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_not_a_date_object(self):
        """testing if default values will be for the due_date attribute used
        when trying to set the due date something other than a datetime.date
        object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"],
                       datetime.timedelta(days=100)]
        
        for test_value in test_values:
            self.kwargs["due_date"] = test_value
            new_foo_obj = self.FooMixedInClass_without_init(**self.kwargs)
            
            self.assertEqual(new_foo_obj.due_date,
                             new_foo_obj.start_date + new_foo_obj.duration)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_not_a_date_object(self):
        """testing if default values will be used for the due_date attribute
        when trying to set the due_date attribute to something other than a
        datetime.date object
        """
        
        test_values = [1, 1.2, "str", ["a", "date"],
                       datetime.timedelta(days=100)]
        
        for test_value in test_values:
            self.mock_foo_obj.due_date =test_value
            
            self.assertEqual(self.mock_foo_obj.due_date,
                             self.mock_foo_obj.start_date + \
                             self.mock_foo_obj.duration)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_argument_is_tried_to_set_to_a_time_before_start_date(self):
        """testing if due_date attribute will be updated to
        start_date + duration when the due_date argument is given as a value
        which is a date before start
        """
        
        self.kwargs["due_date"] = self.kwargs["start_date"] - \
            datetime.timedelta(days=10)
        
        new_foo_obj = self.FooMixedInClass_without_init(**self.kwargs)
        
        self.assertEqual(new_foo_obj.due_date,
                         new_foo_obj.start_date + new_foo_obj.duration)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_tried_to_set_to_a_time_before_start_date(self):
        """testing if a the due attribute is re calculated from the start_date
        and duration attributes when the due_date is tried to be set to a date
        before start
        """
        
        new_due_date = self.mock_foo_obj.start_date - \
                     datetime.timedelta(days=10)
        
        self.mock_foo_obj.due_date = new_due_date
        
        self.assertEqual(self.mock_foo_obj.due_date,
                         self.mock_foo_obj.start_date + \
                         self.mock_foo_obj.duration)
    
    
    
    #----------------------------------------------------------------------
    def test_due_date_attribute_is_shifted_when_start_date_passes_it(self):
        """testing if due_date attribute will be shifted when the start_date
        attribute passes it
        """
        
        time_delta = self.mock_foo_obj.due_date - self.mock_foo_obj.start_date
        self.mock_foo_obj.start_date += 2 * time_delta
        
        self.assertEqual(
            self.mock_foo_obj.due_date - self.mock_foo_obj.start_date,
            time_delta
        )
    
    
    
    #----------------------------------------------------------------------
    def test_duration_argument_is_not_an_instance_of_timedelta_no_problem_if_start_date_and_due_date_is_present(self):
        """testing if no error will be raised when the duration argument is not
        an instance of datetime.date class when both of the start_date and
        due_date arguments are present.
        """
        
        test_values = [1, 1.2, "10", "10 days"]
        
        # no problem if there are start_date and due_date arguments
        for test_value in test_values:
            self.kwargs["duration"] = test_value
            new_foo_obj = self.FooMixedInClass(**self.kwargs)
            
            # check the value
            self.assertEqual(new_foo_obj.duration,
                             new_foo_obj.due_date - new_foo_obj.start_date)
    
    
    
    #----------------------------------------------------------------------
    def test_duration_argument_is_not_an_instance_of_date_when_start_date_argument_is_missing(self):
        """testing if defaults for the duration attribute will be used  when
        the duration argument is not an instance of datetime.date class when
        start_date argument is also missing
        """
        
        test_values = [1, 1.2, "10", "10 days"]
        
        self.kwargs.pop("start_date")
        
        for test_value in test_values:
            self.kwargs["duration"] = test_value
            new_foo_obj = self.FooMixedInClass(**self.kwargs)
            
            self.assertEqual(new_foo_obj.duration,
                             defaults.DEFAULT_TASK_DURATION)
    
    
    
    #----------------------------------------------------------------------
    def test_duration_argument_is_not_an_instance_of_date_when_due_date_argument_is_missing(self):
        """testing if the defaults for the duration attribute will be used when
        the duration argument is not an instance of datetime.date class and
        when due_date argument is also missing
        """
        
        test_values = [1, 1.2, "10", "10 days"]
        
        self.kwargs.pop("due_date")
        
        for test_value in test_values:
            self.kwargs["duration"] = test_value
            new_foo_obj = self.FooMixedInClass(**self.kwargs)
            self.assertEqual(new_foo_obj.duration,
                             defaults.DEFAULT_TASK_DURATION)
    
    
    
    #----------------------------------------------------------------------
    def test_duration_attribute_is_calculated_correctly(self):
        """testing if the duration attribute is calculated correctly
        """
        
        new_foo_entity = self.FooMixedInClass(**self.kwargs)
        new_foo_entity.start_date = datetime.date.today()
        new_foo_entity.due_date = new_foo_entity.start_date + \
                      datetime.timedelta(201)
        
        self.assertEqual(new_foo_entity.duration, datetime.timedelta(201))
    
    
    
    #----------------------------------------------------------------------
    def test_duration_attribute_is_set_to_not_an_instance_of_timedelta(self):
        """testing if duration attribute reset to a calculated value when it is
        set to something other than a datetime.timedelta instance
        """
        
        test_values = [1, 1.2, "10", "10 days"]
        
        # no problem if there are start_date and due_date arguments
        for test_value in test_values:
            self.mock_foo_obj.duration = test_value
            
            # check the value
            self.assertEqual(self.mock_foo_obj.duration,
                             self.mock_foo_obj.due_date - \
                             self.mock_foo_obj.start_date)
    
    
    
    #----------------------------------------------------------------------
    def test_duration_attribute_expands_then_due_date_shifts(self):
        """testing if duration attribute is expanded then the due_date
        attribute is shifted
        """
        
        due_date = self.mock_foo_obj.due_date
        start_date = self.mock_foo_obj.start_date
        duration = self.mock_foo_obj.duration
        
        # change the duration
        new_duration = duration * 10
        self.mock_foo_obj.duration = new_duration
        
        # duration expanded
        self.assertEqual(self.mock_foo_obj.duration, new_duration)
        
        # start_date is not changed
        self.assertEqual(self.mock_foo_obj.start_date, start_date)
        
        # due_date is postponed
        self.assertEqual(self.mock_foo_obj.due_date, start_date + new_duration)
    
    
    
    #----------------------------------------------------------------------
    def test_duration_attribute_contracts_then_due_date_shifts_back(self):
        """testing if duration attribute is contracted then the due_date
        attribute is shifted back
        """
        
        due_date = self.mock_foo_obj.due_date
        start_date = self.mock_foo_obj.start_date
        duration = self.mock_foo_obj.duration
        
        # change the duration
        new_duration = duration / 2
        self.mock_foo_obj.duration = new_duration
        
        # duration expanded
        self.assertEqual(self.mock_foo_obj.duration, new_duration)
        
        # start_date is not changed
        self.assertEqual(self.mock_foo_obj.start_date, start_date)
        
        # due_date is postponed
        self.assertEqual(self.mock_foo_obj.due_date, start_date + new_duration)
    
    
    
    #----------------------------------------------------------------------
    def test_duration_is_a_negative_timedelta(self):
        """testing if the duration is a negative timedelta will set the
        duration to 1 days
        """
        
        start_date = self.mock_foo_obj.start_date
        
        self.mock_foo_obj.duration = datetime.timedelta(-10)
        
        self.assertEqual(self.mock_foo_obj.duration, datetime.timedelta(1))
        self.assertEqual(self.mock_foo_obj.start_date, start_date)
    
    
    
    #----------------------------------------------------------------------
    def test_init_all_parameters_skipped(self):
        """testing if the attributes are initialized to:
        
        start_date = datetime.date.today()
        duration = stalker.conf.defaults.DEFAULT_TASK_DURATION
        due_date = start_date + duration
        """
        
        #self.fail("test is not implemented yet")
        self.kwargs.pop("start_date")
        self.kwargs.pop("due_date")
        self.kwargs.pop("duration")
        
        new_foo_entity = self.FooMixedInClass(**self.kwargs)
        
        self.assertEqual(new_foo_entity.start_date, datetime.date.today())
        self.assertEqual(new_foo_entity.duration,
                         defaults.DEFAULT_TASK_DURATION)
        self.assertEqual(new_foo_entity.due_date,
                         new_foo_entity.start_date + new_foo_entity.duration)
    
    
    
    #----------------------------------------------------------------------
    def test_init_only_start_date_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        duration = stalker.conf.defaults.DEFAULT_TASK_DURATION
        due_date = start_date + duration
        """
        
        self.kwargs.pop("due_date")
        self.kwargs.pop("duration")
        
        new_foo_entity = self.FooMixedInClass(**self.kwargs)
        
        self.assertEqual(new_foo_entity.duration,
                         defaults.DEFAULT_TASK_DURATION)
        self.assertEqual(new_foo_entity.due_date,
                         new_foo_entity.start_date + new_foo_entity.duration)
    
    
    
    #----------------------------------------------------------------------
    def test_init_start_date_and_due_date_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        duration = due_date - start_date
        """
        
        self.kwargs.pop("duration")
        
        new_foo_entity = self.FooMixedInClass(**self.kwargs)
        
        self.assertEqual(new_foo_entity.duration,
                         new_foo_entity.due_date - new_foo_entity.start_date)
    
    
    
    #----------------------------------------------------------------------
    def test_init_start_date_and_duration_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        due_date = start_date + duration
        """
        
        self.kwargs.pop("due_date")
        
        new_foo_entity = self.FooMixedInClass(**self.kwargs)
        
        self.assertEqual(new_foo_entity.due_date,
                         new_foo_entity.start_date + new_foo_entity.duration)
    
    
    
    #----------------------------------------------------------------------
    def test_init_all_arguments_are_given(self):
        """testing if the attributes are initialized to:
        
        duration = due_date - start_date
        """
        
        new_foo_entity = self.FooMixedInClass(**self.kwargs)
        
        self.assertEqual(new_foo_entity.duration,
                         new_foo_entity.due_date - new_foo_entity.start_date)
    
    
    
    #----------------------------------------------------------------------
    def test_init_due_date_and_duration_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        start_date = due_date - duration
        """
        
        self.kwargs.pop("start_date")
        
        new_foo_entity = self.FooMixedInClass(**self.kwargs)
        
        self.assertEqual(new_foo_entity.start_date,
                         new_foo_entity.due_date - new_foo_entity.duration)
    
    
    
    #----------------------------------------------------------------------
    def test_init_only_due_date_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        duration = stalker.conf.defaults.DEFAFULT_TASK_DURATION
        start_date = due_date - duration
        """
        
        self.kwargs.pop("duration")
        self.kwargs.pop("start_date")
        
        new_foo_entity = self.FooMixedInClass(**self.kwargs)
        
        self.assertEqual(new_foo_entity.duration,
                         defaults.DEFAULT_TASK_DURATION)
        self.assertEqual(new_foo_entity.start_date,
                         new_foo_entity.due_date - new_foo_entity.duration)

    
    
    
    #----------------------------------------------------------------------
    def test_init_only_duration_argument_is_given(self):
        """testing if the attributes are initialized to:
        
        start_date = datetime.date.today()
        due_date = start_date + duration
        """
        
        self.kwargs.pop("due_date")
        self.kwargs.pop("start_date")
        
        new_foo_entity = self.FooMixedInClass(**self.kwargs)
        
        self.assertEqual(new_foo_entity.start_date, datetime.date.today())
        self.assertEqual(new_foo_entity.due_date,
                         new_foo_entity.start_date + new_foo_entity.duration)







########################################################################
class TaskMixinTester(mocker.MockerTestCase):
    """Tests the TaskMixin
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.mock_task1 = self.mocker.mock(Task)
        self.mock_task2 = self.mocker.mock(Task)
        self.mock_task3 = self.mocker.mock(Task)
        
        self.mocker.replay()
        
        self.kwargs = {
            "tasks": [self.mock_task1, self.mock_task2, self.mock_task3],
        }
        
        class BarClass(object):
            pass
        
        class FooMixedInClass(BarClass, TaskMixin):
            pass
        
        class FooMixedInClassWithInit(BarClass, TaskMixin):
            def __init__(self):
                pass
        
        self.FooMixedInClass = FooMixedInClass
        self.FooMixedInClassWithInit = FooMixedInClassWithInit
        
        self.mock_foo_obj = FooMixedInClass(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_argument_is_None(self):
        """testing if the tasks attribute will be set to empty list if tasks
        argument is given as None
        """
        
        self.kwargs["tasks"] = None
        new_foo_obj = self.FooMixedInClass(**self.kwargs)
        self.assertEqual(new_foo_obj.tasks, [])
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_None(self):
        """testing if the tasks attribute will be set to empty list when it is
        set to None
        """
        
        self.mock_foo_obj.tasks = None
        self.assertEqual(self.mock_foo_obj.tasks, [])
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the tasks argument is
        not a list
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.kwargs["tasks"] = test_value
            self.assertRaises(TypeError, self.FooMixedInClass, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the tasks attribute is
        tried to set to a non list object
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.mock_foo_obj,
                "tasks",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_argument_is_a_list_of_other_objects_than_Task(self):
        """testing if a TypeError will be raised when the items in the tasks
        argument is not Task instance
        """
        
        test_value = [1, 1.2, "a str", ["a", "list"]]
        self.kwargs["tasks"] = test_value
        self.assertRaises(TypeError, self.FooMixedInClass, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_set_to_a_list_of_other_objects_than_Task(self):
        """testing if a TypeError will be raised when the items in the tasks
        attribute is not Task instance
        """
        
        test_value = [1, 1.2, "a str", ["a", "list"]]
        self.assertRaises(
            TypeError,
            setattr,
            self.mock_foo_obj,
            "tasks",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_element_attributes_are_set_to_other_object_than_Task(self):
        """testing if a TypeError will be raised when trying to set the
        individual elements in the tasks attribute to other objects than a
        Task instance
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                self.mock_foo_obj.tasks.__setitem__,
                "0",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_attribute_is_instance_of_ValidatedList(self):
        """testing if the tasks attribute is a ValidatedList instance
        """
        
        self.assertIsInstance(self.mock_foo_obj.tasks, ValidatedList)
    
    
    