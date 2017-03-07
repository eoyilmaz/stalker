# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

from stalker.testing import UnitTestBase


class PaymentTestCase(UnitTestBase):
    """tests for Payment class
    """

    def setUp(self):
        """run once
        """
        super(PaymentTestCase, self).setUp()
        from stalker import db, Status
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
        db.DBSession.add(self.test_project_status_list)

        from stalker import Type
        self.test_movie_project_type = Type(
            name="Movie Project",
            code='movie',
            target_entity_type=Project,
        )
        db.DBSession.add(self.test_movie_project_type)

        from stalker import Repository
        self.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type=Repository,
        )
        db.DBSession.add(self.test_repository_type)

        self.test_repository = Repository(
            name="Test Repository",
            type=self.test_repository_type,
        )
        db.DBSession.add(self.test_repository)

        from stalker import User
        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@user1.com",
            password="1234"
        )
        db.DBSession.add(self.test_user1)

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@user2.com",
            password="1234"
        )
        db.DBSession.add(self.test_user2)

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@user3.com",
            password="1234"
        )
        db.DBSession.add(self.test_user3)

        self.test_user4 = User(
            name="User4",
            login="user4",
            email="user4@user4.com",
            password="1234"
        )
        db.DBSession.add(self.test_user4)

        self.test_user5 = User(
            name="User5",
            login="user5",
            email="user5@user5.com",
            password="1234"
        )
        db.DBSession.add(self.test_user5)

        from stalker import Client
        self.test_client = Client(
            name='Test Client',
        )
        db.DBSession.add(self.test_client)

        self.test_project = Project(
            name="Test Project1",
            code='tp1',
            type=self.test_movie_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repository,
            clients=[self.test_client]
        )
        db.DBSession.add(self.test_project)

        from stalker import Budget
        self.test_budget = Budget(
            project=self.test_project,
            name='Test Budget 1',
        )
        db.DBSession.add(self.test_budget)

        from stalker import Invoice
        self.test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=1500,
            unit='TRY'
        )
        db.DBSession.add(self.test_invoice)
        db.DBSession.commit()

    def test_creating_a_payment_instance(self):
        """testing if it is possible to create a Payment instance
        """
        from stalker import Payment
        payment = Payment(
            invoice=self.test_invoice,
            amount=1000,
            unit='TRY'
        )
        self.assertIsInstance(payment, Payment)

    def test_invoice_argument_is_skipped(self):
        """testing if a TypeError will be raised when the invoice argument is
        skipped
        """
        from stalker import Payment
        with self.assertRaises(TypeError) as cm:
            p = Payment(amount=1499, unit='TRY')

        self.assertEqual(
            str(cm.exception),
            'Payment.invoice should be an Invoice instance, not NoneType'
        )

    def test_invoice_argument_is_None(self):
        """testing if a TypeError will be raised when the invoice argument is
        None
        """
        from stalker import Payment
        with self.assertRaises(TypeError) as cm:
            p = Payment(invoice=None, amount=1499, unit='TRY')

        self.assertEqual(
            str(cm.exception),
            'Payment.invoice should be an Invoice instance, not NoneType'
        )

    def test_invoice_attribute_is_None(self):
        """testing if a TypeError will be raised when the invoice attribute is
        set to None
        """
        from stalker import Payment
        p = Payment(invoice=self.test_invoice, amount=1499, unit='TRY')

        with self.assertRaises(TypeError) as cm:
            p.invoice = None

        self.assertEqual(
            str(cm.exception),
            'Payment.invoice should be an Invoice instance, not NoneType'
        )

    def test_invoice_argument_is_not_an_invoice_instance(self):
        """testing if a TypeError will be raised when the invoice argument is
        not an Invoice instance
        """
        from stalker import Payment
        with self.assertRaises(TypeError) as cm:
            p = Payment(
                invoice='not an invoice instance',
                amount=1499,
                unit='TRY'
            )

        self.assertEqual(
            str(cm.exception),
            'Payment.invoice should be an Invoice instance, not str'
        )

    def test_invoice_attribute_is_set_to_a_value_other_than_an_invoice_instance(self):
        """testing if a TypeError will be raised when the invoice attribute is
        set to a value other than an Invoice instance
        """
        from stalker import Payment
        p = Payment(invoice=self.test_invoice, amount=1499, unit='TRY')

        with self.assertRaises(TypeError) as cm:
            p.invoice = 'not an invoice instance'

        self.assertEqual(
            str(cm.exception),
            'Payment.invoice should be an Invoice instance, not str'
        )

    def test_invoice_argument_is_working_properly(self):
        """testing if the invoice argument value is correctly passed to the
        invoice attribute
        """
        from stalker import Payment
        p = Payment(invoice=self.test_invoice, amount=1499, unit='TRY')
        self.assertEqual(p.invoice, self.test_invoice)

    def test_invoice_attribute_is_working_properly(self):
        """testing if the invoice attribute value can be correctly changed
        """
        from stalker import Payment, Invoice
        p = Payment(invoice=self.test_invoice, amount=1499, unit='TRY')
        new_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=2500,
            unit='TRY'
        )
        self.assertNotEqual(p.invoice, new_invoice)
        p.invoice = new_invoice
        self.assertEqual(p.invoice, new_invoice)
