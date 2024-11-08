# -*- coding: utf-8 -*-
"""StatusMixin class related tests."""

import pytest

from sqlalchemy import Column, ForeignKey, Integer

from stalker import SimpleEntity, Status, StatusList, StatusMixin
from stalker.db.session import DBSession


class StatMixClass(SimpleEntity, StatusMixin):
    """A class for testing StatusMixin."""

    __tablename__ = "StatMixClasses"
    __mapper_args__ = {"polymorphic_identity": "StatMixClass"}
    StatMixClass_id = Column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(StatMixClass, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def status_mixin_tests():
    """Set up the tests for the StatusMixin class.

    Returns:
        dict: Test data.
    """
    data = dict()
    data["test_status1"] = Status(name="Status1", code="STS1")
    data["test_status2"] = Status(name="Status2", code="STS2")
    data["test_status3"] = Status(name="Status3", code="STS3")
    data["test_status4"] = Status(name="Status4", code="STS4")
    data["test_status5"] = Status(name="Status5", code="STS5")

    # statuses which are not going to be used
    data["test_status6"] = Status(name="Status6", code="STS6")
    data["test_status7"] = Status(name="Status7", code="STS7")
    data["test_status8"] = Status(name="Status8", code="STS8")

    # a test StatusList object
    data["test_status_list1"] = StatusList(
        name="Test Status List 1",
        statuses=[
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ],
        target_entity_type="StatMixClass",
    )

    # another test StatusList object
    data["test_status_list2"] = StatusList(
        name="Test Status List 2",
        statuses=[
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ],
        target_entity_type="StatMixClass",
    )

    data["kwargs"] = {
        "name": "Test Class",
        "status_list": data["test_status_list1"],
        "status": data["test_status_list1"].statuses[0],
    }

    data["test_mixed_obj"] = StatMixClass(**data["kwargs"])
    data["test_mixed_obj"].status_list = data["test_status_list1"]

    # create another one without status_list set to something
    data["test_mixed_obj2"] = StatMixClass(**data["kwargs"])
    return data


def test_status_list_argument_is_not_a_status_list_instance(status_mixin_tests):
    """TypeError is raised if status_list arg is not a StatusList."""
    data = status_mixin_tests
    data["kwargs"]["status_list"] = 100
    with pytest.raises(TypeError) as cm:
        StatMixClass(**data["kwargs"])

    assert str(cm.value) == (
        "StatMixClass.status_list should be an instance of "
        "stalker.models.status.StatusList, not int: '100'"
    )


def test_status_list_attribute_set_to_something_other_than_status_list(
    status_mixin_tests,
):
    """TypeError is raised if status_list is not a StatusList."""
    data = status_mixin_tests
    with pytest.raises(TypeError) as cm:
        data["test_mixed_obj"].status_list = "a string"

    assert str(cm.value) == (
        "StatMixClass.status_list should be an instance of "
        "stalker.models.status.StatusList, not str: 'a string'"
    )


def test_status_list_argument_suitable_for_the_current_class(status_mixin_tests):
    """TypeError is raised if the Status.target_entity_type is not compatible."""
    data = status_mixin_tests
    # create a new status list suitable for another class with different
    # entity_type

    new_status_list = StatusList(
        name="Sequence Statuses",
        statuses=[
            Status(name="On Hold", code="OH"),
            Status(name="Complete", code="CMPLT"),
        ],
        target_entity_type="Sequence",
    )

    with pytest.raises(TypeError) as cm:
        data["test_mixed_obj"].status_list = new_status_list

    assert (
        str(cm.value)
        == "The given StatusLists' target_entity_type is Sequence, whereas "
        "the entity_type of this object is StatMixClass"
    )


def test_status_list_attribute_is_working_as_expected(status_mixin_tests):
    """status_list attribute is working as expected."""
    data = status_mixin_tests
    new_suitable_list = StatusList(
        name="Suitable Statuses",
        statuses=[
            Status(name="On Hold", code="OH"),
            Status(name="Complete", code="CMPLT"),
        ],
        target_entity_type="StatMixClass",
    )

    # this shouldn't raise any error
    data["test_mixed_obj"].status_list = new_suitable_list

    assert data["test_mixed_obj"].status_list == new_suitable_list


def test_status_argument_set_to_none(status_mixin_tests):
    """first in the status_list attribute is used if the status arg is None."""
    data = status_mixin_tests
    data["kwargs"]["status"] = None
    new_obj = StatMixClass(**data["kwargs"])
    assert new_obj.status == new_obj.status_list[0]


def test_status_attribute_set_to_none(status_mixin_tests):
    """first in the status_list is used if status attribute is set to None."""
    data = status_mixin_tests
    data["test_mixed_obj"].status = None
    assert data["test_mixed_obj"].status == data["test_mixed_obj"].status_list[0]


def test_status_argument_is_not_a_status_instance_or_integer(status_mixin_tests):
    """TypeError is raised if status arg is not a Status or int."""
    data = status_mixin_tests
    data["kwargs"]["status"] = "0"
    with pytest.raises(TypeError) as cm:
        StatMixClass(**data["kwargs"])

    assert str(cm.value) == (
        "StatMixClass.status must be an instance of stalker.models.status.Status or "
        "an integer showing the index of the Status object in the "
        "StatMixClass.status_list, not str: '0'"
    )


def test_status_attribute_set_to_a_value_other_than_a_status_or_integer(
    status_mixin_tests,
):
    """TypeError is raised if status attribute is set to not Status nor int."""
    data = status_mixin_tests
    with pytest.raises(TypeError) as cm:
        data["test_mixed_obj"].status = "a string"

    assert str(cm.value) == (
        "StatMixClass.status must be an instance of stalker.models.status.Status "
        "or an integer showing the index of the Status object in the "
        "StatMixClass.status_list, not str: 'a string'"
    )


def test_status_attribute_is_set_to_a_status_which_is_not_in_the_status_list(
    status_mixin_tests,
):
    """ValueError is raised if Status is not in the related StatusList."""
    data = status_mixin_tests
    with pytest.raises(ValueError) as cm:
        data["test_mixed_obj"].status = data["test_status8"]

    assert (
        str(cm.value) == "The given Status instance for StatMixClass.status is not in "
        "the StatMixClass.status_list, please supply a status from "
        "that list."
    )


def test_status_argument_is_working_as_expected_with_status_instances(
    status_mixin_tests,
):
    """status attribute value is set correctly with Status arg value."""
    data = status_mixin_tests
    test_value = data["kwargs"]["status_list"][1]
    data["kwargs"]["status"] = test_value
    new_obj = StatMixClass(**data["kwargs"])
    assert new_obj.status == test_value


def test_status_attribute_is_working_as_expected_with_status_instances(
    status_mixin_tests,
):
    """status attribute is working as expected with Status instances."""
    data = status_mixin_tests
    test_value = data["test_mixed_obj"].status_list[1]
    data["test_mixed_obj"].status = test_value
    assert data["test_mixed_obj"].status == test_value


def test_status_argument_is_working_as_expected_with_integers(status_mixin_tests):
    """status attribute value is set correctly with int arg value."""
    data = status_mixin_tests
    data["kwargs"]["status"] = 1
    test_value = data["kwargs"]["status_list"][1]
    new_obj = StatMixClass(**data["kwargs"])
    assert new_obj.status == test_value


def test_status_attribute_is_working_as_expected_with_integers(status_mixin_tests):
    """status attribute is working as expected with integers."""
    data = status_mixin_tests
    test_value = 1
    data["test_mixed_obj"].status = test_value
    assert (
        data["test_mixed_obj"].status == data["test_mixed_obj"].status_list[test_value]
    )


def test_status_argument_is_an_integer_but_out_of_range(status_mixin_tests):
    """ValueError is raised if the status argument is out of range."""
    data = status_mixin_tests
    data["kwargs"]["status"] = 10
    with pytest.raises(ValueError) as cm:
        StatMixClass(**data["kwargs"])

    assert (
        str(cm.value) == "StatMixClass.status cannot be bigger than the length of the "
        "status_list"
    )


def test_status_attribute_set_to_an_integer_but_out_of_range(status_mixin_tests):
    """ValueError is raised if the status attribute is set to out of range int."""
    data = status_mixin_tests
    with pytest.raises(ValueError) as cm:
        data["test_mixed_obj"].status = 10

    assert (
        str(cm.value) == "StatMixClass.status cannot be bigger than the length of the "
        "status_list"
    )


def test_status_argument_is_a_negative_integer(status_mixin_tests):
    """ValueError will be raised if the status argument is a negative int."""
    data = status_mixin_tests
    data["kwargs"]["status"] = -10
    with pytest.raises(ValueError) as cm:
        StatMixClass(**data["kwargs"])

    assert str(cm.value) == "StatMixClass.status must be a non-negative integer"


def test_status_attribute_set_to_an_negative_integer(status_mixin_tests):
    """ValueError is raised if the status attribute is set to a negative int."""
    data = status_mixin_tests
    with pytest.raises(ValueError) as cm:
        data["test_mixed_obj"].status = -10

    assert str(cm.value) == "StatMixClass.status must be a non-negative integer"


class StatusListAutoAddClass(SimpleEntity, StatusMixin):
    """A class derived from stalker.core.models.SimpleEntity for testing purposes."""

    __tablename__ = "StatusListAutoAddClass"
    __mapper_args__ = {"polymorphic_identity": "StatusListAutoAddClass"}
    statusListAutoAddClass_id = Column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(SimpleEntity, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


class StatusListNoAutoAddClass(SimpleEntity, StatusMixin):
    """A class derived from stalker.core.models.SimpleEntity for testing purposes."""

    __tablename__ = "StatusListNoAutoAddClass"
    __mapper_args__ = {"polymorphic_identity": "StatusListNoAutoAddClass"}
    statusListNoAutoAddClass_id = Column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(SimpleEntity, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def setup_status_mixin_db_tests(setup_postgresql_db):
    """Set up tests for the StatusMixin with a DB.

    Returns:
        dict: Test data.
    """
    data = setup_postgresql_db
    data["test_status1"] = Status(name="Status1", code="STS1")
    data["test_status2"] = Status(name="Status2", code="STS2")
    data["test_status3"] = Status(name="Status3", code="STS3")
    data["test_status4"] = Status(name="Status4", code="STS4")
    data["test_status5"] = Status(name="Status5", code="STS5")

    # statuses which are not going to be used
    data["test_status6"] = Status(name="Status6", code="STS6")
    data["test_status7"] = Status(name="Status7", code="STS7")
    data["test_status8"] = Status(name="Status8", code="STS8")

    # a test StatusList object
    data["test_status_list1"] = StatusList(
        name="Test Status List 1",
        statuses=[
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ],
        target_entity_type="StatMixClass",
    )

    # another test StatusList object
    data["test_status_list2"] = StatusList(
        name="Test Status List 2",
        statuses=[
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ],
        target_entity_type="StatMixClass",
    )

    data["kwargs"] = {
        "name": "Test Class",
        "status_list": data["test_status_list1"],
        "status": data["test_status_list1"].statuses[0],
    }

    data["test_mixed_obj"] = StatMixClass(**data["kwargs"])
    data["test_mixed_obj"].status_list = data["test_status_list1"]

    # create another one without status_list set to something
    data["test_mixed_obj2"] = StatMixClass(**data["kwargs"])
    return data


def test_status_list_attribute_is_skipped_and_there_is_a_db_setup(
    setup_status_mixin_db_tests,
):
    """no error raised, status_list is filled with StatusList instance, with db."""
    # create a StatusList for StatusListAutoAddClass
    test_status_list = StatusList(
        name="StatusListAutoAddClass Statuses",
        statuses=[
            Status(name="Status1", code="Sts1"),
            Status(name="Status2", code="Sts2"),
            Status(name="Status3", code="Sts3"),
        ],
        target_entity_type=StatusListAutoAddClass,
    )

    # add it to the db
    DBSession.add(test_status_list)
    DBSession.commit()

    # now try to create a StatusListAutoAddClass without a status_list
    # argument
    test_status_list_auto_add_class = StatusListAutoAddClass(
        name="Test StatusListAutoAddClass",
    )

    # now check if the status_list is equal to test_status_list
    assert test_status_list_auto_add_class.status_list == test_status_list


def test_status_list_attribute_is_skipped_and_there_is_a_db_setup_but_no_suitable_status_list(
    setup_status_mixin_db_tests,
):
    """TypeError is raised no suitable StatusList in the database."""
    # create a StatusList for StatusListAutoAddClass
    test_status_list = StatusList(
        name="StatusListAutoAddClass Statuses",
        statuses=[
            Status(name="Status1", code="Sts1"),
            Status(name="Status2", code="Sts2"),
            Status(name="Status3", code="Sts3"),
        ],
        target_entity_type=StatusListAutoAddClass,
    )

    # add it to the db
    DBSession.add(test_status_list)
    DBSession.commit()

    # now try to create a StatusListAutoAddClass without a status_list
    # argument

    with pytest.raises(TypeError) as cm:
        StatusListNoAutoAddClass(name="Test StatusListNoAutoAddClass")

    assert (
        str(cm.value) == "StatusListNoAutoAddClass instances cannot be initialized "
        "without a stalker.models.status.StatusList instance, please "
        "pass a suitable StatusList "
        "(StatusList.target_entity_type=StatusListNoAutoAddClass) with "
        "the 'status_list' argument"
    )


def test_status_list_argument_is_none(setup_status_mixin_db_tests):
    """TypeError is raised if trying to initialize status_list with None."""
    data = setup_status_mixin_db_tests
    data["kwargs"]["status_list"] = None
    with pytest.raises(TypeError) as cm:
        StatMixClass(**data["kwargs"])

    assert (
        str(cm.value) == "StatMixClass instances cannot be initialized without a "
        "stalker.models.status.StatusList instance, please pass a "
        "suitable StatusList "
        "(StatusList.target_entity_type=StatMixClass) with the "
        "'status_list' argument"
    )


def test_status_list_argument_skipped(setup_status_mixin_db_tests):
    """TypeError is raised if status_list argument is skipped."""
    data = setup_status_mixin_db_tests
    data["kwargs"].pop("status_list")
    with pytest.raises(TypeError) as cm:
        StatMixClass(**data["kwargs"])

    assert (
        str(cm.value) == "StatMixClass instances cannot be initialized without a "
        "stalker.models.status.StatusList instance, please pass a "
        "suitable StatusList "
        "(StatusList.target_entity_type=StatMixClass) with the "
        "'status_list' argument"
    )


def test_status_list_attribute_set_to_none(setup_status_mixin_db_tests):
    """TypeError is raised if trying to set the status_list to None."""
    data = setup_status_mixin_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_mixed_obj"].status_list = None

    assert (
        str(cm.value) == "StatMixClass instances cannot be initialized without a "
        "stalker.models.status.StatusList instance, please pass a "
        "suitable StatusList "
        "(StatusList.target_entity_type=StatMixClass) with the "
        "'status_list' argument"
    )
