# -*- coding: utf-8 -*-

import unittest
import pytest


class InvoiceTestCase(unittest.TestCase):
    """tests for Invoice class
    """

    def setUp(self):
        """run once
        """
        super(InvoiceTestCase, self).setUp()

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
            name='Task Statuses',
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
            target_entity_type='Project',
        )

        from stalker import Repository
        self.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type='Repository',
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

    def test_creating_an_invoice_instance(self):
        """testing creation of an Invoice instance
        """
        from stalker import Invoice
        import datetime
        import pytz
        invoice = Invoice(
            budget=self.test_budget,
            amount=1500,
            unit='TL',
            client=self.test_client,
            date_created=datetime.datetime(2016, 11, 7, tzinfo=pytz.utc),
        )
        assert isinstance(invoice, Invoice)

    def test_budget_argument_is_skipped(self):
        """testing if a TypeError will be raised when the budget argument is
        skipped
        """
        from stalker import Invoice
        with pytest.raises(TypeError) as cm:
            Invoice(
                client=self.test_client,
                amount=1500,
                unit='TRY'
            )

        assert str(cm.value) == \
            'Invoice.budget should be a Budget instance, not NoneType'

    def test_budget_argument_is_None(self):
        """testing if a TypeError will be raised when the budget argument is
        None
        """
        from stalker import Invoice
        with pytest.raises(TypeError) as cm:
            Invoice(
                budget=None,
                client=self.test_client,
                amount=1500,
                unit='TRY'
            )

        assert str(cm.value) == \
            'Invoice.budget should be a Budget instance, not NoneType'

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
        with pytest.raises(TypeError) as cm:
            test_invoice.budget = None

        assert str(cm.value) == \
            'Invoice.budget should be a Budget instance, not NoneType'

    def test_budget_argument_is_not_a_budget_instance(self):
        """testing if a TypeError will be raised when the Budget argument is
        not a Budget instance
        """
        from stalker import Invoice
        with pytest.raises(TypeError) as cm:
            Invoice(
                budget='Not a budget instance',
                client=self.test_client,
                amount=1500,
                unit='TRY'
            )

        assert str(cm.value) == \
            'Invoice.budget should be a Budget instance, not str'

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
        with pytest.raises(TypeError) as cm:
            test_invoice.budget = 'Not a budget instance'

        assert str(cm.value) == \
            'Invoice.budget should be a Budget instance, not str'

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
        assert test_invoice.budget == self.test_budget

    def test_client_argument_is_skipped(self):
        """testing if a TypeError will be raised when the client argument is
        skipped
        """
        from stalker import Invoice
        with pytest.raises(TypeError) as cm:
            Invoice(
                budget=self.test_budget,
                amount=100,
                unit='TRY'
            )

        assert str(cm.value) == \
            'Invoice.client should be a Client instance, not NoneType'

    def test_client_argument_is_None(self):
        """testing if a TypeError will be raised when the client argument is
        None
        """
        from stalker import Invoice
        with pytest.raises(TypeError) as cm:
            Invoice(
                budget=self.test_budget,
                client=None,
                amount=100,
                unit='TRY'
            )

        assert str(cm.value) == \
            'Invoice.client should be a Client instance, not NoneType'

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
        with pytest.raises(TypeError) as cm:
            test_invoice.client = None

        assert str(cm.value) == \
            'Invoice.client should be a Client instance, not NoneType'

    def test_client_argument_is_not_a_client_instance(self):
        """testing if a TypeError will be raised when the client argument is
        not a Client instance
        """
        from stalker import Invoice
        with pytest.raises(TypeError) as cm:
            Invoice(
                budget=self.test_budget,
                client='not a client instance',
                amount=100,
                unit='TRY'
            )

        assert str(cm.value) == \
            'Invoice.client should be a Client instance, not str'

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
        with pytest.raises(TypeError) as cm:
            test_invoice.client = 'not a client instance'

        assert str(cm.value) == \
            'Invoice.client should be a Client instance, not str'

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
        assert test_invoice.client == self.test_client

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
        assert test_invoice.client != test_client
        test_invoice.client = test_client
        assert test_invoice.client == test_client
