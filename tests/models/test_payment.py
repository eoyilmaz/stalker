# -*- coding: utf-8 -*-

import unittest
import pytest


class PaymentTestCase(unittest.TestCase):
    """tests for Payment class
    """

    def setUp(self):
        """run once
        """
        super(PaymentTestCase, self).setUp()
        from stalker import Status

        self.status_new = Status(name='Mew', code='NEW')
        self.status_wfd = Status(name='Waiting For Dependency', code='WFD')
        self.status_rts = Status(name='Ready To Start', code='RTS')
        self.status_wip = Status(name='Work In Progress', code='WIP')
        self.status_prev = Status(name='Pending Review', code='PREV')
        self.status_hrev = Status(name='Has Revision', code='HREV')
        self.status_drev = Status(name='Dependency Has Revision', code='DREV')
        self.status_oh = Status(name='On Hold', code='OH')
        self.status_stop = Status(name='Stopped', code='STOP')
        self.status_cmpl = Status(name='Completed', code='CMPL')

        self.status_new = Status(name='New', code='NEW')
        self.status_app = Status(name='Approved', code='APP')

        from stalker import StatusList
        self.budget_status_list = StatusList(
            name='Budget Statuses',
            target_entity_type='Budget',
            statuses=[self.status_new, self.status_prev, self.status_app]
        )

        self.task_status_list = StatusList(
            name='Task Statses',
            statuses=[
                self.status_wfd, self.status_rts, self.status_wip,
                self.status_prev, self.status_hrev, self.status_drev,
                self.status_oh, self.status_stop, self.status_cmpl
            ],
            target_entity_type='Task'
        )

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
            code='TR',
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
            status_list=self.budget_status_list
        )

        from stalker import Invoice
        self.test_invoice = Invoice(
            budget=self.test_budget,
            client=self.test_client,
            amount=1500,
            unit='TRY'
        )

    def test_creating_a_payment_instance(self):
        """testing if it is possible to create a Payment instance
        """
        from stalker import Payment
        payment = Payment(
            invoice=self.test_invoice,
            amount=1000,
            unit='TRY'
        )
        assert isinstance(payment, Payment)

    def test_invoice_argument_is_skipped(self):
        """testing if a TypeError will be raised when the invoice argument is
        skipped
        """
        from stalker import Payment
        with pytest.raises(TypeError) as cm:
            p = Payment(amount=1499, unit='TRY')

        assert str(cm.value) == \
            'Payment.invoice should be an Invoice instance, not NoneType'

    def test_invoice_argument_is_None(self):
        """testing if a TypeError will be raised when the invoice argument is
        None
        """
        from stalker import Payment
        with pytest.raises(TypeError) as cm:
            p = Payment(invoice=None, amount=1499, unit='TRY')

        assert str(cm.value) == \
            'Payment.invoice should be an Invoice instance, not NoneType'

    def test_invoice_attribute_is_None(self):
        """testing if a TypeError will be raised when the invoice attribute is
        set to None
        """
        from stalker import Payment
        p = Payment(invoice=self.test_invoice, amount=1499, unit='TRY')

        with pytest.raises(TypeError) as cm:
            p.invoice = None

        assert str(cm.value) == \
            'Payment.invoice should be an Invoice instance, not NoneType'

    def test_invoice_argument_is_not_an_invoice_instance(self):
        """testing if a TypeError will be raised when the invoice argument is
        not an Invoice instance
        """
        from stalker import Payment
        with pytest.raises(TypeError) as cm:
            p = Payment(
                invoice='not an invoice instance',
                amount=1499,
                unit='TRY'
            )

        assert str(cm.value) == \
            'Payment.invoice should be an Invoice instance, not str'

    def test_invoice_attribute_is_set_to_a_value_other_than_an_invoice_instance(self):
        """testing if a TypeError will be raised when the invoice attribute is
        set to a value other than an Invoice instance
        """
        from stalker import Payment
        p = Payment(invoice=self.test_invoice, amount=1499, unit='TRY')

        with pytest.raises(TypeError) as cm:
            p.invoice = 'not an invoice instance'

        assert str(cm.value) == \
            'Payment.invoice should be an Invoice instance, not str'

    def test_invoice_argument_is_working_properly(self):
        """testing if the invoice argument value is correctly passed to the
        invoice attribute
        """
        from stalker import Payment
        p = Payment(invoice=self.test_invoice, amount=1499, unit='TRY')
        assert p.invoice == self.test_invoice

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
        assert p.invoice != new_invoice
        p.invoice = new_invoice
        assert p.invoice == new_invoice
