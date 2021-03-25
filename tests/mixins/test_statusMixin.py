# -*- coding: utf-8 -*-

import unittest

import pytest

from stalker.testing import UnitTestDBBase
from sqlalchemy import Column, Integer, ForeignKey
from stalker import StatusMixin, Status, StatusList, SimpleEntity


class StatMixClass(SimpleEntity, StatusMixin):
    __tablename__ = "StatMixClasses"
    __mapper_args__ = {"polymorphic_identity": "StatMixClass"}
    StatMixClass_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                             primary_key=True)

    def __init__(self, **kwargs):
        super(StatMixClass, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


class StatusMixinTester(unittest.TestCase):
    """tests the StatusMixin class
    """

    def setUp(self):
        """setup the test
        """
        super(StatusMixinTester, self).setUp()
        self.test_status1 = Status(name="Status1", code="STS1")
        self.test_status2 = Status(name="Status2", code="STS2")
        self.test_status3 = Status(name="Status3", code="STS3")
        self.test_status4 = Status(name="Status4", code="STS4")
        self.test_status5 = Status(name="Status5", code="STS5")

        # statuses which are not going to be used
        self.test_status6 = Status(name="Status6", code="STS6")
        self.test_status7 = Status(name="Status7", code="STS7")
        self.test_status8 = Status(name="Status8", code="STS8")

        # a test StatusList object
        self.test_status_list1 = StatusList(
            name="Test Status List 1",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type="StatMixClass",
        )

        # another test StatusList object
        self.test_status_list2 = StatusList(
            name="Test Status List 2",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type="StatMixClass",
        )

        self.kwargs = {
            "name": "Test Class",
            "status_list": self.test_status_list1,
            "status": self.test_status_list1.statuses[0],
        }

        self.test_mixed_obj = StatMixClass(**self.kwargs)
        self.test_mixed_obj.status_list = self.test_status_list1

        # create another one without status_list set to something
        self.test_mixed_obj2 = StatMixClass(**self.kwargs)

    def test_status_list_argument_is_not_a_StatusList_instance(self):
        """testing if TypeError is going to be raised when trying to initialize
        status_list with something other than a StatusList
        """
        self.kwargs["status_list"] = 100
        with pytest.raises(TypeError) as cm:
            StatMixClass(**self.kwargs)

        assert str(cm.value) == \
            'StatMixClass.status_list should be an instance of ' \
            'stalker.models.status.StatusList not int'

    def test_status_list_attribute_set_to_something_other_than_StatusList(self):
        """testing if TypeError is going to be raised when trying to set the
        status_list to something else than a StatusList object
        """
        with pytest.raises(TypeError) as cm:
            self.test_mixed_obj.status_list = "a string"

        assert str(cm.value) == \
            'StatMixClass.status_list should be an instance of ' \
            'stalker.models.status.StatusList not str'

    def test_status_list_argument_suitable_for_the_current_class(self):
        """testing if a TypeError will be raised when the
        Status.target_entity_type is not compatible with the current class
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

        with pytest.raises(TypeError) as cm:
            self.test_mixed_obj.status_list = new_status_list

        assert str(cm.value) == \
            "The given StatusLists' target_entity_type is Sequence, whereas " \
            "the entity_type of this object is StatMixClass"

    def test_status_list_attribute_is_working_properly(self):
        """testing if the status_list attribute is working properly
        """
        new_suitable_list = StatusList(
            name="Suitable Statuses",
            statuses=[
                Status(name="On Hold", code="OH"),
                Status(name="Complete", code="CMPLT"),
            ],
            target_entity_type="StatMixClass"
        )

        # this shouldn't raise any error
        self.test_mixed_obj.status_list = new_suitable_list

        assert self.test_mixed_obj.status_list == new_suitable_list

    def test_status_argument_set_to_None(self):
        """testing if the first Status in the status_list attribute will be
        used when the status argument is None
        """
        self.kwargs["status"] = None
        new_obj = StatMixClass(**self.kwargs)
        assert new_obj.status == new_obj.status_list[0]

    def test_status_attribute_set_to_None(self):
        """testing if the first Status in the status_list attribute will be
        used when setting the status attribute to None
        """
        self.test_mixed_obj.status = None
        assert self.test_mixed_obj.status == self.test_mixed_obj.status_list[0]

    def test_status_argument_is_not_a_Status_instance_or_integer(self):
        """testing if a TypeError is going to be raised if status argument is
        not a Status instance or an integer
        """
        self.kwargs["status"] = "0"
        with pytest.raises(TypeError) as cm:
            StatMixClass(**self.kwargs)

        assert str(cm.value) == \
            'StatMixClass.status must be an instance of ' \
            'stalker.models.status.Status or an integer showing the index ' \
            'of the Status object in the StatMixClass.status_list, not str'

    def test_status_attribute_set_to_a_value_other_than_a_Status_or_integer(self):
        """testing if a TypeError will be raised when trying to set the current
        status to something other than a Status instance or an integer
        """
        with pytest.raises(TypeError) as cm:
            self.test_mixed_obj.status = "a string"

        assert str(cm.value) == \
            'StatMixClass.status must be an instance of ' \
            'stalker.models.status.Status or an integer showing the index ' \
            'of the Status object in the StatMixClass.status_list, not str'

    def test_status_attribute_is_set_to_a_Status_which_is_not_in_the_StatusList(self):
        """testing if a ValueError will be raised when the given Status is not
        in the related StatusList
        """
        with pytest.raises(ValueError) as cm:
            self.test_mixed_obj.status = self.test_status8

        assert str(cm.value) == \
            'The given Status instance for StatMixClass.status is not in ' \
            'the StatMixClass.status_list, please supply a status from ' \
            'that list.'

    def test_status_argument_is_working_properly_with_Status_instances(self):
        """testing if the status attribute is set correctly with the given
        value of status argument when the status argument value is a Status
        instance
        """
        test_value = self.kwargs['status_list'][1]
        self.kwargs['status'] = test_value
        new_obj = StatMixClass(**self.kwargs)
        assert new_obj.status == test_value

    def test_status_attribute_is_working_properly_with_Status_instances(self):
        """testing if the status attribute is working properly with Status
        instances
        """
        test_value = self.test_mixed_obj.status_list[1]
        self.test_mixed_obj.status = test_value
        assert self.test_mixed_obj.status == test_value

    def test_status_argument_is_working_properly_with_integers(self):
        """testing if the status attribute value is set correctly with the
        given status argument when the status argument value is an integer
        """
        self.kwargs['status'] = 1
        test_value = self.kwargs['status_list'][1]
        new_obj = StatMixClass(**self.kwargs)
        assert new_obj.status == test_value

    def test_status_attribute_is_working_properly_with_integers(self):
        """testing if the status attribute is working properly with integers
        """
        test_value = 1
        self.test_mixed_obj.status = test_value
        assert self.test_mixed_obj.status == \
               self.test_mixed_obj.status_list[test_value]

    def test_status_argument_is_an_integer_but_out_of_range(self):
        """testing if a ValueError will be raised if the status argument is an
        integer but it is way out of range
        """
        self.kwargs['status'] = 10
        with pytest.raises(ValueError) as cm:
            StatMixClass(**self.kwargs)

        assert str(cm.value) == \
            'StatMixClass.status can not be bigger than the length of the ' \
            'status_list'

    def test_status_attribute_set_to_an_integer_but_out_of_range(self):
        """testing if a ValueError will be raised if the status attribute is
        set to an integer which is out of range
        """
        with pytest.raises(ValueError) as cm:
            self.test_mixed_obj.status = 10

        assert str(cm.value) == \
            'StatMixClass.status can not be bigger than the length of the ' \
            'status_list'

    def test_status_argument_is_a_negative_integer(self):
        """testing if a ValueError will be raised if the status argument is a
        negative integer
        """
        self.kwargs['status'] = -10
        with pytest.raises(ValueError) as cm:
            StatMixClass(**self.kwargs)

        assert str(cm.value) == \
               'StatMixClass.status must be a non-negative integer'

    def test_status_attribute_set_to_an_negative_integer(self):
        """testing if a ValueError will be raised if the status attribute is
        set to an negative integer
        """
        with pytest.raises(ValueError) as cm:
            self.test_mixed_obj.status = -10

        assert str(cm.value) == \
               'StatMixClass.status must be a non-negative integer'


class StatusListAutoAddClass(SimpleEntity, StatusMixin):
    """It is a class derived from stalker.core.models.SimpleEntity for testing
    purposes.
    """

    __tablename__ = "StatusListAutoAddClass"
    __mapper_args__ = {"polymorphic_identity": "StatusListAutoAddClass"}
    statusListAutoAddClass_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )

    def __init__(self, **kwargs):
        super(SimpleEntity, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


class StatusListNoAutoAddClass(SimpleEntity, StatusMixin):
    """It is a class derived from stalker.core.models.SimpleEntity for testing
    purposes.
    """

    __tablename__ = "StatusListNoAutoAddClass"
    __mapper_args__ = {"polymorphic_identity": "StatusListNoAutoAddClass"}
    statusListNoAutoAddClass_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )

    def __init__(self, **kwargs):
        super(SimpleEntity, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


class StatusMixinDBTester(UnitTestDBBase):
    """tests the StatusMixin with a DB is already setup
    """

    def setUp(self):
        """setup the test
        """
        super(StatusMixinDBTester, self).setUp()
        self.test_status1 = Status(name="Status1", code="STS1")
        self.test_status2 = Status(name="Status2", code="STS2")
        self.test_status3 = Status(name="Status3", code="STS3")
        self.test_status4 = Status(name="Status4", code="STS4")
        self.test_status5 = Status(name="Status5", code="STS5")

        # statuses which are not going to be used
        self.test_status6 = Status(name="Status6", code="STS6")
        self.test_status7 = Status(name="Status7", code="STS7")
        self.test_status8 = Status(name="Status8", code="STS8")

        # a test StatusList object
        self.test_status_list1 = StatusList(
            name="Test Status List 1",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type="StatMixClass",
        )

        # another test StatusList object
        self.test_status_list2 = StatusList(
            name="Test Status List 2",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type="StatMixClass",
        )

        self.kwargs = {
            "name": "Test Class",
            "status_list": self.test_status_list1,
            "status": self.test_status_list1.statuses[0],
        }

        self.test_mixed_obj = StatMixClass(**self.kwargs)
        self.test_mixed_obj.status_list = self.test_status_list1

        # create another one without status_list set to something
        self.test_mixed_obj2 = StatMixClass(**self.kwargs)

    def test_status_list_attribute_is_skipped_and_there_is_a_db_setup(self):
        """testing if there will be no error and the status_list attribute is
        filled with the correct StatusList instance coming from the database
        if there is already a database setup and there is a StatusList instance
        defined for the StatusListAutoAddClass.
        """
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
        from stalker.db.session import DBSession
        DBSession.add(test_status_list)
        DBSession.commit()

        # now try to create a StatusListAutoAddClass without a status_list 
        # argument
        test_StatusListAutoAddClass = StatusListAutoAddClass(
            name="Test StatusListAutoAddClass",
        )

        # now check if the status_list is equal to test_status_list
        assert test_StatusListAutoAddClass.status_list == test_status_list

    def test_status_list_attribute_is_skipped_and_there_is_a_db_setup_but_no_suitable_StatusList(self):
        """testing if a TypeError will be raised even a database is setup 
        but there is no suitable StatusList for StatusListNoAutoAddClass in 
        the database
        """

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
        from stalker.db.session import DBSession
        DBSession.add(test_status_list)
        DBSession.commit()

        # now try to create a StatusListAutoAddClass without a status_list 
        # argument

        with pytest.raises(TypeError) as cm:
            StatusListNoAutoAddClass(name="Test StatusListNoAutoAddClass")

        assert str(cm.value) == \
            "StatusListNoAutoAddClass instances can not be initialized " \
            "without a stalker.models.status.StatusList instance, please " \
            "pass a suitable StatusList " \
            "(StatusList.target_entity_type=StatusListNoAutoAddClass) with " \
            "the 'status_list' argument"

    def test_status_list_argument_is_None(self):
        """testing if TypeError is going to be raised when trying to initialize
        status_list with None
        """
        self.kwargs["status_list"] = None
        with pytest.raises(TypeError) as cm:
            StatMixClass(**self.kwargs)

        assert str(cm.value) == \
            "StatMixClass instances can not be initialized without a " \
            "stalker.models.status.StatusList instance, please pass a " \
            "suitable StatusList " \
            "(StatusList.target_entity_type=StatMixClass) with the " \
            "'status_list' argument"

    def test_status_list_argument_skipped(self):
        """testing if a TypeError going to be raised when status_list argument
        is skipped
        """
        self.kwargs.pop("status_list")
        with pytest.raises(TypeError) as cm:
            StatMixClass(**self.kwargs)

        assert str(cm.value) == \
            "StatMixClass instances can not be initialized without a " \
            "stalker.models.status.StatusList instance, please pass a " \
            "suitable StatusList " \
            "(StatusList.target_entity_type=StatMixClass) with the " \
            "'status_list' argument"

    def test_status_list_attribute_set_to_None(self):
        """testing if TypeError is going to be raised when trying to set the
        status_list to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_mixed_obj.status_list = None

        assert str(cm.value) == \
            "StatMixClass instances can not be initialized without a " \
            "stalker.models.status.StatusList instance, please pass a " \
            "suitable StatusList " \
            "(StatusList.target_entity_type=StatMixClass) with the " \
            "'status_list' argument"
