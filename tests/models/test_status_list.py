# -*- coding: utf-8 -*-

import unittest

import pytest

from stalker import Status, StatusList


class StatusListTest(unittest.TestCase):
    """testing the StatusList class
    """

    def setUp(self):
        """let's create proper values for the tests
        """
        super(StatusListTest, self).setUp()

        self.kwargs = {
            "name": "a status list",
            "description": "this is a status list for testing purposes",
            "statuses": [
                Status(name='Waiting For Dependency', code="WFD"),
                Status(name='Ready To Start', code="RTS"),
                Status(name='Work In Progress', code="WIP"),
                Status(name='Pending Review', code="PREV"),
                Status(name='Has Revision', code="HREV"),
                Status(name='Completed', code="CMPL"),
                Status(name='On Hold', code="OH"),
            ],
            "target_entity_type": "Project",
        }

        self.test_status_list = StatusList(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for
        StatusList class
        """
        assert StatusList.__auto_name__ is True

    def test_statuses_argument_accepts_statuses_only(self):
        """testing if statuses list argument accepts list of statuses only
        """
        # the statuses argument should be a list of statuses
        # can be empty?

        test_value = "a str"
        # it should only accept lists of statuses
        self.kwargs["statuses"] = test_value
        with pytest.raises(TypeError) as cm:
            StatusList(**self.kwargs)

        assert str(cm.value) == \
            'Incompatible collection type: str is not list-like'

    def test_statuses_attribute_accepting_only_statuses(self):
        """testing the status_list attribute accepting Status objects only
        """
        test_value = "1"

        # check the attribute
        with pytest.raises(TypeError) as cm:
            self.test_status_list.statuses = test_value

        assert str(cm.value) == \
            'Incompatible collection type: str is not list-like'

    def test_statuses_argument_elements_being_status_objects(self):
        """testing status_list elements against not being derived from Status
        class
        """
        # every element should be an object derived from Status
        a_fake_status_list = [1, 2, "a string", 4.5]

        self.kwargs["statuses"] = a_fake_status_list

        with pytest.raises(TypeError) as cm:
            StatusList(**self.kwargs)

        assert str(cm.value) == \
            'All of the elements in StatusList.statuses must be an instance ' \
            'of stalker.models.status.Status, and not int'

    def test_statuses_attribute_works_properly(self):
        """testing if status_list attribute is working properly
        """
        new_list_of_statutes = [
            Status(name="New Status", code="NSTS")
        ]

        self.test_status_list.statuses = new_list_of_statutes
        assert self.test_status_list.statuses == new_list_of_statutes

    def test_statuses_attributes_elements_changed_to_none_status_objects(self):
        """testing if a TypeError will be raised when trying to set an
        individual element in the statuses list to an object which is not a
        Status instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_status_list.statuses[0] = 0

        assert str(cm.value) == \
            'All of the elements in StatusList.statuses must be an instance ' \
            'of stalker.models.status.Status, and not int'

    def test_equality_operator(self):
        """testing equality of two status list object
        """
        status_list1 = StatusList(**self.kwargs)
        status_list2 = StatusList(**self.kwargs)

        self.kwargs["target_entity_type"] = "SomeOtherClass"

        status_list3 = StatusList(**self.kwargs)

        self.kwargs["statuses"] = [
            Status(name="Started", code="STRT"),
            Status(name="Waiting For Approve", code="WAPPR"),
            Status(name="Approved", code="APPR"),
            Status(name="Finished", code="FNSH"),
        ]

        status_list4 = StatusList(**self.kwargs)

        assert status_list1 == status_list2
        assert not status_list1 == status_list3
        assert not status_list1 == status_list4

    def test_inequality_operator(self):
        """testing equality of two status list object
        """
        status_list1 = StatusList(**self.kwargs)
        status_list2 = StatusList(**self.kwargs)

        self.kwargs["target_entity_type"] = "SomeOtherClass"

        status_list3 = StatusList(**self.kwargs)

        self.kwargs["statuses"] = [
            Status(name="Started", code="STRT"),
            Status(name="Waiting For Approve", code="WAPPR"),
            Status(name="Approved", code="APPR"),
            Status(name="Finished", code="FNSH"),
        ]

        status_list4 = StatusList(**self.kwargs)

        assert not status_list1 != status_list2
        assert status_list1 != status_list3
        assert status_list1 != status_list4

    def test_indexing_get(self):
        """testing indexing of statuses in the statusList, get
        """
        # first try indexing

        # this shouldn't raise a TypeError
        status1 = self.test_status_list[0]

        # check the equality
        assert self.test_status_list.statuses[0] == status1

    def test_indexing_get_string_indexes(self):
        """testing indexing of statuses in the statusList, get with string
        """

        status1 = Status(name="Complete", code="CMPLT")
        status2 = Status(name="Work in Progress", code="WIP")
        status3 = Status(name="Pending Review", code="PRev")

        a_status_list = StatusList(name="Asset Status List",
                                   statuses=[status1, status2, status3],
                                   target_entity_type="Asset")

        assert a_status_list[0] == a_status_list["complete"]
        assert a_status_list[1] == a_status_list["wip"]

    def test_indexing_set(self):
        """testing indexing of statuses in the statusList, set
        """
        # first try indexing

        # this shouldn't raise a TypeError
        status = Status(name="Pending Review", code="PRev")

        self.test_status_list[0] = status

        # check the equality
        assert self.test_status_list.statuses[0] == status

    def test_indexing_del(self):
        """testing indexing of statuses in the statusList, del
        """
        # first get the length
        len_statuses = len(self.test_status_list.statuses)

        del self.test_status_list[-1]

        assert len(self.test_status_list.statuses) == len_statuses - 1

    def test_indexing_len(self):
        """testing indexing of statuses in the statusList, len
        """
        # get the len and compare it wiht len(statuses)
        assert len(self.test_status_list.statuses) == \
            len(self.test_status_list)
