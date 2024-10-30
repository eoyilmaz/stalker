# -*- coding: utf-8 -*-
"""Tests for the StatusList class."""

import pytest

from stalker import Status, StatusList


@pytest.fixture(scope="function")
def setup_status_list_tests():
    """Set up tests for the StatusList class."""
    data = dict()
    data["kwargs"] = {
        "name": "a status list",
        "description": "this is a status list for testing purposes",
        "statuses": [
            Status(name="Waiting For Dependency", code="WFD"),
            Status(name="Ready To Start", code="RTS"),
            Status(name="Work In Progress", code="WIP"),
            Status(name="Pending Review", code="PREV"),
            Status(name="Has Revision", code="HREV"),
            Status(name="Completed", code="CMPL"),
            Status(name="On Hold", code="OH"),
        ],
        "target_entity_type": "Project",
    }

    data["test_status_list"] = StatusList(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_true():
    """__auto_name__ class attribute is set to True for StatusList class."""
    assert StatusList.__auto_name__ is True


def test_statuses_argument_accepts_statuses_only(setup_status_list_tests):
    """statuses list argument accepts list of statuses only."""
    data = setup_status_list_tests
    # the statuses argument should be a list of statuses
    # can be empty?
    test_value = "a str"
    # it should only accept lists of statuses
    data["kwargs"]["statuses"] = test_value
    with pytest.raises(TypeError) as cm:
        StatusList(**data["kwargs"])

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_statuses_attribute_accepting_only_statuses(setup_status_list_tests):
    """status_list attribute accepting Status objects only."""
    data = setup_status_list_tests
    test_value = "1"
    # check the attribute
    with pytest.raises(TypeError) as cm:
        data["test_status_list"].statuses = test_value

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_statuses_argument_elements_being_status_objects(setup_status_list_tests):
    """status_list elements against not being derived from Status class."""
    data = setup_status_list_tests
    # every element should be an object derived from Status
    a_fake_status_list = [1, 2, "a string", 4.5]
    data["kwargs"]["statuses"] = a_fake_status_list
    with pytest.raises(TypeError) as cm:
        StatusList(**data["kwargs"])

    assert str(cm.value) == (
        "All of the elements in StatusList.statuses must be an instance "
        "of stalker.models.status.Status, not int: '1'"
    )


def test_statuses_attribute_works_properly(setup_status_list_tests):
    """status_list attribute is working properly."""
    data = setup_status_list_tests
    new_list_of_statutes = [Status(name="New Status", code="NSTS")]
    data["test_status_list"].statuses = new_list_of_statutes
    assert data["test_status_list"].statuses == new_list_of_statutes


def test_statuses_attributes_elements_changed_to_none_status_objects(
    setup_status_list_tests,
):
    """TypeError raised if an item is set to a none Status instance statuses list."""
    data = setup_status_list_tests
    with pytest.raises(TypeError) as cm:
        data["test_status_list"].statuses[0] = 0
    assert str(cm.value) == (
        "All of the elements in StatusList.statuses must be an instance "
        "of stalker.models.status.Status, not int: '0'"
    )


def test_equality_operator(setup_status_list_tests):
    """equality of two status list object."""
    data = setup_status_list_tests
    status_list1 = StatusList(**data["kwargs"])
    status_list2 = StatusList(**data["kwargs"])
    data["kwargs"]["target_entity_type"] = "SomeOtherClass"
    status_list3 = StatusList(**data["kwargs"])
    data["kwargs"]["statuses"] = [
        Status(name="Started", code="STRT"),
        Status(name="Waiting For Approve", code="WAPPR"),
        Status(name="Approved", code="APPR"),
        Status(name="Finished", code="FNSH"),
    ]
    status_list4 = StatusList(**data["kwargs"])
    assert status_list1 == status_list2
    assert not status_list1 == status_list3
    assert not status_list1 == status_list4


def test_inequality_operator(setup_status_list_tests):
    """equality of two status list object."""
    data = setup_status_list_tests
    status_list1 = StatusList(**data["kwargs"])
    status_list2 = StatusList(**data["kwargs"])
    data["kwargs"]["target_entity_type"] = "SomeOtherClass"
    status_list3 = StatusList(**data["kwargs"])
    data["kwargs"]["statuses"] = [
        Status(name="Started", code="STRT"),
        Status(name="Waiting For Approve", code="WAPPR"),
        Status(name="Approved", code="APPR"),
        Status(name="Finished", code="FNSH"),
    ]
    status_list4 = StatusList(**data["kwargs"])
    assert not status_list1 != status_list2
    assert status_list1 != status_list3
    assert status_list1 != status_list4


def test_indexing_get(setup_status_list_tests):
    """indexing of statuses in the statusList, get."""
    data = setup_status_list_tests
    # first try indexing
    # this shouldn't raise a TypeError
    status1 = data["test_status_list"][0]
    # check the equality
    assert data["test_status_list"].statuses[0] == status1


def test_indexing_get_string_indexes(setup_status_list_tests):
    """indexing of statuses in the statusList, get with string."""
    data = setup_status_list_tests
    status1 = Status(name="Complete", code="CMPLT")
    status2 = Status(name="Work in Progress", code="WIP")
    status3 = Status(name="Pending Review", code="PRev")
    a_status_list = StatusList(
        name="Asset Status List",
        statuses=[status1, status2, status3],
        target_entity_type="Asset",
    )

    assert a_status_list[0] == a_status_list["complete"]
    assert a_status_list[1] == a_status_list["wip"]


def test_indexing_setitem_validates_the_given_value(setup_status_list_tests):
    """indexing of statuses in the statusList, set."""
    data = setup_status_list_tests
    # first try indexing
    # this shouldn't raise a TypeError
    with pytest.raises(TypeError) as cm:
        data["test_status_list"][0] = "PRev"

    assert str(cm.value) == (
        "All of the elements in StatusList.statuses must be an instance of "
        "stalker.models.status.Status, not str: 'PRev'"
    )


def test_indexing_setitem(setup_status_list_tests):
    """indexing of statuses in the statusList, set."""
    data = setup_status_list_tests
    # first try indexing
    # this shouldn't raise a TypeError
    status = Status(name="Pending Review", code="PRev")
    data["test_status_list"][0] = status
    # check the equality
    assert data["test_status_list"].statuses[0] == status


def test_indexing_delitem(setup_status_list_tests):
    """indexing of statuses in the statusList, del."""
    data = setup_status_list_tests
    # first get the length
    len_statuses = len(data["test_status_list"].statuses)
    del data["test_status_list"][-1]
    assert len(data["test_status_list"].statuses) == len_statuses - 1


def test_indexing_len(setup_status_list_tests):
    """indexing of statuses in the statusList, len."""
    data = setup_status_list_tests
    # get the len and compare it wiht len(statuses)
    assert len(data["test_status_list"].statuses) == len(data["test_status_list"])
