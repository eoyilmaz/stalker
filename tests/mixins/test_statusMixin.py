# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import unittest
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import orm

from stalker import db
from stalker.db.session import DBSession
from stalker.models.mixins import StatusMixin
from stalker.models.status import Status, StatusList
from stalker.models.entity import SimpleEntity


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

    #def tearDown(self):
    #    """clean up the test
    #    """
    #    DBSession.remove()

    def test_status_list_argument_is_None(self):
        """testing if TypeError is going to be raised when trying to initialize
        status_list with None
        """
        self.kwargs["status_list"] = None
        self.assertRaises(TypeError, StatMixClass, **self.kwargs)

    def test_status_list_argument_is_not_a_StatusList_instance(self):
        """testing if TypeError is going to be raised when trying to initialize
        status_list with something other than a StatusList
        """
        testValues = [100, "", 100.2]
        for testValue in testValues:
            self.kwargs["status_list"] = testValue
            self.assertRaises(TypeError, StatMixClass, **self.kwargs)

    def test_status_list_attribute_set_to_something_other_than_StatusList(
            self):
        """testing if TypeError is going to be raised when trying to set the
        status_list to something else than a StatusList object
        """
        test_values = ["a string", 1.0, 1, {"a": "statusList"}]

        for test_value in test_values:
            # now try to set it
            self.assertRaises(
                TypeError,
                setattr,
                self.test_mixed_obj,
                "status_list",
                test_value
            )

    def test_status_list_attribute_set_to_None(self):
        """testing if TypeError is going to be raised when trying to set the
        status_list to None
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_mixed_obj,
            "status_list",
            None
        )

    def test_status_list_argument_skipped(self):
        """testing if a TypeError going to be raised when status_list argument
        is skipped
        """
        self.kwargs.pop("status_list")
        self.assertRaises(TypeError, StatMixClass, **self.kwargs)

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

        self.assertRaises(
            TypeError,
            setattr,
            self.test_mixed_obj,
            "status_list",
            new_status_list
        )

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

    def test_status_argument_set_to_None(self):
        """testing if the first Status in the status_list attribute will be
        used when the status argument is None
        """
        self.kwargs["status"] = None
        new_obj = StatMixClass(**self.kwargs)
        self.assertEqual(new_obj.status, new_obj.status_list[0])

    def test_status_attribute_set_to_None(self):
        """testing if the first Status in the status_list attribute will be
        used when setting the status attribute to None
        """
        self.test_mixed_obj.status = None
        self.assertEqual(
            self.test_mixed_obj.status,
            self.test_mixed_obj.status_list[0]
        )

    def test_status_argument_is_not_a_Status_instance_or_integer(self):
        """testing if a TypeError is going to be raised if status argument is
        not a Status instance or an integer
        """
        test_values = ["0", 1.2, [0]]

        for test_value in test_values:
            self.kwargs["status"] = test_value
            self.assertRaises(TypeError, StatMixClass, **self.kwargs)

    def test_status_attribute_set_to_a_value_other_than_a_Status_or_integer(
            self):
        """testing if a TypeError will be raised when trying to set the current
        status to something other than a Status instance or an integer
        """
        test_values = ["a string", 1.2, [1], {"a": "status"}]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_mixed_obj,
                "status",
                test_value
            )

    def test_status_attribute_is_set_to_a_Status_which_is_not_in_the_StatusList(
            self):
        """testing if a ValueError will be raised when the given Status is not
        in the related StatusList
        """
        self.assertRaises(
            ValueError,
            setattr,
            self.test_mixed_obj,
            'status',
            self.test_status8
        )

    def test_status_argument_is_working_properly_with_Status_instances(self):
        """testing if the status attribute is set correctly with the given
        value of status argument when the status argument value is a Status
        instance
        """
        test_value = self.kwargs['status_list'][1]
        self.kwargs['status'] = test_value
        new_obj = StatMixClass(**self.kwargs)
        self.assertEqual(
            new_obj.status,
            test_value
        )

    def test_status_attribute_is_working_properly_with_Status_instances(self):
        """testing if the status attribute is working properly with Status
        instances
        """
        test_value = self.test_mixed_obj.status_list[1]
        self.test_mixed_obj.status = test_value
        self.assertEqual(
            self.test_mixed_obj.status,
            test_value
        )

    def test_status_argument_is_working_properly_with_integers(self):
        """testing if the status attribute value is set correctly with the
        given status argument when the status argument value is an integer
        """
        self.kwargs['status'] = 1
        test_value = self.kwargs['status_list'][1]
        new_obj = StatMixClass(**self.kwargs)
        self.assertEqual(
            new_obj.status,
            test_value
        )

    def test_status_attribute_is_working_properly_with_integers(self):
        """testing if the status attribute is working properly with integers
        """
        test_value = 1
        self.test_mixed_obj.status = test_value
        self.assertEqual(
            self.test_mixed_obj.status,
            self.test_mixed_obj.status_list[test_value]
        )

    def test_status_argument_is_an_integer_but_out_of_range(self):
        """testing if a ValueError will be raised if the status argument is an
        integer but it is way out of range
        """
        test_value = 10
        self.kwargs['status'] = test_value
        self.assertRaises(ValueError, StatMixClass, **self.kwargs)

    def test_status_attribute_set_to_an_integer_but_out_of_range(self):
        """testing if a ValueError will be raised if the status attribute is
        set to an integer which is out of range
        """
        test_value = 10
        self.assertRaises(
            ValueError,
            setattr,
            self.test_mixed_obj,
            'status',
            test_value
        )

    def test_status_argument_is_a_negative_integer(self):
        """testing if a ValueError will be raised if the status argument is a
        negative integer
        """
        test_value = -10
        self.kwargs['status'] = test_value
        self.assertRaises(ValueError, StatMixClass, **self.kwargs)

    def test_status_attribute_set_to_an_negative_integer(self):
        """testing if a ValueError will be raised if the status attribute is
        set to an negative integer
        """
        test_value = -10
        self.assertRaises(
            ValueError,
            setattr,
            self.test_mixed_obj,
            'status',
            test_value
        )


class StatusListAutoAddClass(SimpleEntity, StatusMixin):
    """It is a class derived from stalker.core.models.SimpleEntity for testing
    purposes.
    """

    __tablename__ = "StatusListAutoAddClass"
    __mapper_args__ = {"polymorphic_identity": "StatusListAutoAddClass"}
    statusListAutoAddClass_id = Column("id", Integer,
                                       ForeignKey("SimpleEntities.id"),
                                       primary_key=True)

    def __init__(self, **kwargs):
        super(SimpleEntity, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)

    @orm.reconstructor
    def __init_on_load__(self):
        """the init function for instances loaded from the db
        """
        super(StatusListAutoAddClass, self).__init_on_load__()


class StatusListNoAutoAddClass(SimpleEntity, StatusMixin):
    """It is a class derived from stalker.core.models.SimpleEntity for testing
    purposes.
    """

    __tablename__ = "StatusListNoAutoAddClass"
    __mapper_args__ = {"polymorphic_identity": "StatusListNoAutoAddClass"}
    statusListNoAutoAddClass_id = Column("id", Integer,
                                         ForeignKey("SimpleEntities.id"),
                                         primary_key=True)

    def __init__(self, **kwargs):
        super(SimpleEntity, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)

    @orm.reconstructor
    def __init_on_load__(self):
        """the init function for instances loaded from the db
        """
        super(StatusListAutoAddClass, self).__init_on_load__()


class StatusMixinDBTester(unittest.TestCase):
    """tests the StatusMixin with a DB is already setup
    """

    @classmethod
    def setUpClass(cls):
        """setup test in class level
        """
        DBSession.remove()

    @classmethod
    def tearDownClass(cls):
        """clear test in class level
        """
        DBSession.remove()

    def setUp(self):
        """setup the test
        """
        # create a database
        db.setup()

    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()

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
        DBSession.add(test_status_list)
        DBSession.commit()

        # now try to create a StatusListAutoAddClass without a status_list 
        # argument
        test_StatusListAutoAddClass = StatusListAutoAddClass(
            name="Test StatusListAutoAddClass",
        )

        # now check if the status_list is equal to test_status_list
        self.assertEqual(
            test_StatusListAutoAddClass.status_list,
            test_status_list
        )

    def test_status_list_attribute_is_skipped_and_there_is_a_db_setup_but_no_suitable_StatusList(
            self):
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
        DBSession.add(test_status_list)
        DBSession.commit()

        # now try to create a StatusListAutoAddClass without a status_list 
        # argument

        self.assertRaises(
            TypeError,
            StatusListNoAutoAddClass,
            **{"name": "Test StatusListNoAutoAddClass"}
        )
