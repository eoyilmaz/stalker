# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
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


class InvoiceTestCase(unittest.TestCase):
    """tests for Invoice class
    """

    def setUp(self):
        """run once
        """
        from stalker import defaults
        import datetime
        defaults.timing_resolution = datetime.timedelta(hours=1)

        # create a new session
        from stalker import db
        db.setup({
            'sqlalchemy.url': 'sqlite://',
            'sqlalchemy.echo': False
        })
        db.init()

        from stalker import Status
        self.status_wfd = Status.query.filter_by(code="WFD").first()
        self.status_rts = Status.query.filter_by(code="RTS").first()
        self.status_wip = Status.query.filter_by(code="WIP").first()
        self.status_prev = Status.query.filter_by(code="PREV").first()
        self.status_hrev = Status.query.filter_by(code="HREV").first()
        self.status_drev = Status.query.filter_by(code="DREV").first()
        self.status_oh = Status.query.filter_by(code="OH").first()
        self.status_stop = Status.query.filter_by(code="STOP").first()
        self.status_cmpl = Status.query.filter_by(code="CMPL").first()

        self.status_new = Status.query.filter_by(code='NEW').first()
        self.status_app = Status.query.filter_by(code='APP').first()

        from stalker import StatusList
        self.budget_status_list = StatusList(
            name='Budget Statuses',
            target_entity_type='Budget',
            statuses=[self.status_new, self.status_prev, self.status_app]
        )
        db.DBSession.add(self.budget_status_list)

        self.task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

        from stalker import Project
        self.test_project_status_list = StatusList(
            name="Project Statuses",
            statuses=[self.status_wip,
                      self.status_prev,
                      self.status_cmpl],
            target_entity_type=Project,
        )

        from stalker import Type
        self.test_movie_project_type = Type(
            name="Movie Project",
            code='movie',
            target_entity_type=Project,
        )

        from stalker import Repository
        self.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type=Repository,
        )

        self.test_repository = Repository(
            name="Test Repository",
            type=self.test_repository_type,
        )

        from stalker import User
        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@user1.com",
            password="1234"
        )

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@user2.com",
            password="1234"
        )

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@user3.com",
            password="1234"
        )

        self.test_user4 = User(
            name="User4",
            login="user4",
            email="user4@user4.com",
            password="1234"
        )

        self.test_user5 = User(
            name="User5",
            login="user5",
            email="user5@user5.com",
            password="1234"
        )

        from stalker import Client
        self.test_client = Client(
            name='Test Client',
        )

        self.test_project = Project(
            name="Test Project1",
            code='tp1',
            type=self.test_movie_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repository,
            clients=[self.test_client]
        )

        from stalker import Budget
        self.test_budget = Budget(
            project=self.test_project,
            name='Test Budget 1',
        )

    def test_creating_an_invoice_instance(self):
        """testing creation of an Invoice instance
        """
        from stalker import Invoice
        import datetime
        invoice = Invoice(
            budget=self.test_budget,
            amount=1500,
            unit='TL',
            client=self.test_client,
            date_created=datetime.datetime.today(),
        )
        self.assertIsInstance(invoice, Invoice)

    def test_budget_argument_is_skipped(self):
        """testing if a TypeError will be raised when the budget argument is
        skipped
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                client=self.test_client,
                amount=1500,
                unit='TRY'
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.budget should be a Budget instance, not NoneType'
        )

    def test_budget_argument_is_None(self):
        """testing if a TypeError will be raised when the budget argument is
        None
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget=None,
                client=self.test_client,
                amount=1500,
                unit='TRY'
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.budget should be a Budget instance, not NoneType'
        )

    def test_budget_attribute_is_set_to_None(self):
        """testing if a TypeError will ve raised when the budget attribute is
        set to None
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=1500,
            unit='TRY'
        )
        with self.assertRaises(TypeError) as cm:
            test_invoice.budget = None

        self.assertEqual(
            str(cm.exception),
            'Invoice.budget should be a Budget instance, not NoneType'
        )

    def test_budget_argument_is_not_a_budget_instance(self):
        """testing if a TypeError will be raised when the Budget argument is
        not a Budget instance
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget='Not a budget instance',
                client=self.test_client,
                amount=1500,
                unit='TRY'
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.budget should be a Budget instance, not str'
        )

    def test_budget_attribute_is_set_to_a_value_other_than_a_budget_instance(self):
        """testing if a TypeError will be raised when the Budget attribute is
        set to a value other than a Budget instance
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=1500,
            unit='TRY'
        )
        with self.assertRaises(TypeError) as cm:
            test_invoice.budget = 'Not a budget instance'

        self.assertEqual(
            str(cm.exception),
            'Invoice.budget should be a Budget instance, not str'
        )

    def test_budget_argument_is_working_properly(self):
        """testing if the budget argument value is properly passed to the
        budget attribute
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=1500,
            unit='TRY'
        )
        self.assertEqual(test_invoice.budget, self.test_budget)

    def test_amount_argument_is_skipped(self):
        """testing if a ValueError will be raised when the amount argument is
        skipped
        """
        from stalker import Invoice
        with self.assertRaises(ValueError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client=self.test_client,
                unit='TRY'
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.amount cannot be zero'
        )

    def test_amount_argument_is_None(self):
        """testing if a TypeError will be raised when the amount argument is
        None
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client=self.test_client,
                amount=None,
                unit='TRY',
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.amount should be a non-zero positive integer or float, '
            'not NoneType'
        )

    def test_amount_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the amount attribute is
        set to None
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=14.9,
            unit='TRY',
        )
        with self.assertRaises(TypeError) as cm:
            test_invoice.amount = None

        self.assertEqual(
            str(cm.exception),
            'Invoice.amount should be a non-zero positive integer or float, '
            'not NoneType'
        )

    def test_amount_argument_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised when the amount argument is
        not an Integer or Float
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client=self.test_client,
                amount='not an integer or float',
                unit='TRY',
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.amount should be a non-zero positive integer or float, '
            'not str'
        )

    def test_amount_attribute_is_set_to_a_value_other_than_an_integer_or_float(self):
        """testing if a TypeError will be raised when the amount attribute set
        to a value other than an Integer or Float
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=14.9,
            unit='TRY',
        )
        with self.assertRaises(TypeError) as cm:
            test_invoice.amount = 'not an integer or float'

        self.assertEqual(
            str(cm.exception),
            'Invoice.amount should be a non-zero positive integer or float, '
            'not str'
        )

    def test_amount_argument_is_zero(self):
        """testing if a ValueError will be raised when the amount argument is
        zero
        """
        from stalker import Invoice
        with self.assertRaises(ValueError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client=self.test_client,
                amount=0,
                unit='TRY',
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.amount cannot be zero'
        )

    def test_amount_attribute_is_set_to_zero(self):
        """testing if a ValueError will be raised when the amount attribute is
        set to zero
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=102.0,
            unit='TRY',
        )
        with self.assertRaises(ValueError) as cm:
            test_invoice.amount = 0

        self.assertEqual(
            str(cm.exception),
            'Invoice.amount cannot be zero'
        )

    def test_amount_argument_is_negative(self):
        """testing if a ValueError will be raised when the amount argument is a
        negative value
        """
        from stalker import Invoice
        with self.assertRaises(ValueError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client=self.test_client,
                amount=-1023.9,
                unit='TRY',
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.amount cannot be negative'
        )

    def test_amount_attribute_is_negative(self):
        """testing if a ValueError will be raised when the amount attribute is
        set to a negative value
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=10.4,
            unit='TRY',
        )
        with self.assertRaises(ValueError) as cm:
            test_invoice.amount = -234.3

        self.assertEqual(
            str(cm.exception),
            'Invoice.amount cannot be negative'
        )

    def test_amount_argument_is_working_properly(self):
        """testing if the amount argument value is properly passed to the
        amount attribute
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=1023.9,
            unit='TRY',
        )
        self.assertEqual(test_invoice.amount, 1023.9)

    def test_amount_attribute_is_working_properly(self):
        """testing if the amount attribute value can be changed properly
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=1023.9,
            unit='TRY',
        )
        self.assertNotEqual(test_invoice.amount, 1234.3)
        test_invoice.amount = 1234.3
        self.assertEqual(test_invoice.amount, 1234.3)

    def test_unit_argument_is_skipped(self):
        """testing if a TypeError will be raised when the unit argument is
        skipped
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client=self.test_client,
                amount=100,
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.unit should be a string, not NoneType'
        )

    def test_unit_argument_is_None(self):
        """testing if a TypeError will be raised when the unit argument is None
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client=self.test_client,
                amount=100,
                unit=None,
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.unit should be a string, not NoneType'
        )

    def test_unit_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the unit attribute is set
        to None
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=100,
            unit='TRY',
        )
        with self.assertRaises(TypeError) as cm:
            test_invoice.unit = None

        self.assertEqual(
            str(cm.exception),
            'Invoice.unit should be a string, not NoneType'
        )

    def test_unit_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the unit argument value
        is not a string
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client=self.test_client,
                amount=100,
                unit=123
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.unit should be a string, not int'
        )

    def test_unit_attribute_is_set_to_a_value_other_than_a_string(self):
        """testing if a TypeError will be raised when the unit attribute is set
        to a value other than a string
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=100,
            unit='TRY'
        )
        with self.assertRaises(TypeError) as cm:
            test_invoice.unit = 234.3

        self.assertEqual(
            str(cm.exception),
            'Invoice.unit should be a string, not float'
        )

    def test_unit_argument_is_working_properly(self):
        """testing if the unit argument value is properly passed to the unit
        attribute
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=100,
            unit='TRY'
        )
        self.assertEqual(test_invoice.unit, 'TRY')

    def test_unit_attribute_is_working_properly(self):
        """testing if the unit attribute can be changed properly
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=100,
            unit='USD'
        )
        self.assertNotEqual(test_invoice.unit, 'TRY')
        test_invoice.unit = 'TRY'
        self.assertEqual(test_invoice.unit, 'TRY')

    def test_client_argument_is_skipped(self):
        """testing if a TypeError will be raised when the client argument is
        skipped
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                amount=100,
                unit='TRY'
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.client should be a Client instance, not NoneType'
        )

    def test_client_argument_is_None(self):
        """testing if a TypeError will be raised when the client argument is
        None
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client=None,
                amount=100,
                unit='TRY'
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.client should be a Client instance, not NoneType'
        )

    def test_client_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the client attribute is
        set to None
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=100,
            unit='TRY'
        )
        with self.assertRaises(TypeError) as cm:
            test_invoice.client = None

        self.assertEqual(
            str(cm.exception),
            'Invoice.client should be a Client instance, not NoneType'
        )

    def test_client_argument_is_not_a_client_instance(self):
        """testing if a TypeError will be raised when the client argument is
        not a Client instance
        """
        from stalker import Invoice
        with self.assertRaises(TypeError) as cm:
            test_invoice = Invoice(
                budget=self.test_budget,
                client='not a client instance',
                amount=100,
                unit='TRY'
            )

        self.assertEqual(
            str(cm.exception),
            'Invoice.client should be a Client instance, not str'
        )

    def test_client_attribute_is_set_to_a_value_other_than_a_client_instance(self):
        """testing if a TypeError will be raised when the client attribute is
        set to a value other than a Client instance
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=100,
            unit='TRY'
        )
        with self.assertRaises(TypeError) as cm:
            test_invoice.client = 'not a client instance'

        self.assertEqual(
            str(cm.exception),
            'Invoice.client should be a Client instance, not str'
        )

    def test_client_argument_is_working_properly(self):
        """testing if the client argument value is correctly passed to the
        client attribute
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=100,
            unit='TRY'
        )
        self.assertEqual(test_invoice.client, self.test_client)

    def test_client_attribute_is_working_properly(self):
        """testing if the client attribute value an be changed properly
        """
        from stalker import Invoice
        test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=100,
            unit='TRY'
        )
        from stalker import Client
        test_client = Client(name='Test Client 2')
        self.assertNotEqual(test_invoice.client, test_client)
        test_invoice.client = test_client
        self.assertEqual(test_invoice.client, test_client)
