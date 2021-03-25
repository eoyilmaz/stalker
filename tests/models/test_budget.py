# -*- coding: utf-8 -*-

import unittest

import pytest

from stalker import Budget, BudgetEntry, Good


class BudgetTestBase(unittest.TestCase):
    """the base for this test
    """

    def setUp(self):
        """run once
        """
        super(BudgetTestBase, self).setUp()

        from stalker import Status
        self.status_wfd = Status(name='Waiting For Dependency', code="WFD")
        self.status_rts = Status(name='Ready To Start', code="RTS")
        self.status_wip = Status(name='Work In Progress', code="WIP")
        self.status_prev = Status(name='Pending Review', code="PREV")
        self.status_hrev = Status(name='Has Revision', code="HREV")
        self.status_drev = Status(name='Dependency Has Revision', code="DREV")
        self.status_oh = Status(name='On Hold', code="OH")
        self.status_stop = Status(name='Stopped', code="STOP")
        self.status_cmpl = Status(name='Completed', code="CMPL")

        self.status_new = Status(name='New', code='NEW')
        self.status_app = Status(name='Approved', code='APP')

        from stalker import StatusList
        self.budget_status_list = StatusList(
            name='Budget Statuses',
            target_entity_type='Budget',
            statuses=[self.status_new, self.status_prev, self.status_app]
        )

        self.task_status_list = StatusList(
            statuses=[
                self.status_wfd,
                self.status_rts,
                self.status_wip,
                self.status_prev,
                self.status_hrev,
                self.status_drev,
                self.status_cmpl
            ],
            target_entity_type='Task'
        )

        self.test_project_status_list = StatusList(
            name="Project Statuses",
            statuses=[self.status_wip,
                      self.status_prev,
                      self.status_cmpl],
            target_entity_type='Project',
        )

        from stalker import Type
        self.test_movie_project_type = Type(
            name="Movie Project",
            code='movie',
            target_entity_type='Project',
        )

        self.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type='Repository',
        )

        from stalker import Repository
        self.test_repository = Repository(
            name="Test Repository",
            code='TR',
            type=self.test_repository_type,
            linux_path='/mnt/T/',
            windows_path='T:/',
            osx_path='/Volumes/T/'
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

        from stalker import Project
        self.test_project = Project(
            name="Test Project1",
            code='tp1',
            type=self.test_movie_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repository,
        )

        self.kwargs = {
            'project': self.test_project,
            'name': 'Test Budget 1',
            'status_list': self.budget_status_list
        }

        self.test_budget = Budget(**self.kwargs)

        from stalker import Good
        self.test_good = Good(
            name='Some Good',
            cost=100,
            msrp=120,
            unit='$'
        )


class BudgetTestCase(BudgetTestBase):
    """tests the stalker.models.budget.Budget class
    """

    def test_entries_attribute_is_set_to_a_list_of_other_instances_than_a_budget_entry(self):
        """testing if a TypeError will be raised when the entries attribute is
        set to something other than a list of BugdgetEntries.
        """
        with pytest.raises(TypeError) as cm:
            self.test_budget.entries = ['some', 'string', 1, 2]

        assert str(cm.value) == \
            'Budget.entries should be a list of BudgetEntry instances, not str'

    def test_entries_attribute_is_working_properly(self):
        """testing if the entries attribute is working properly
        """
        from stalker import BudgetEntry
        some_other_budget = Budget(
            name='Test Budget',
            project=self.test_project,
            status_list=self.budget_status_list
        )
        entry1 = BudgetEntry(
            budget=some_other_budget,
            good=self.test_good,
        )
        entry2 = BudgetEntry(
            budget=some_other_budget,
            good=self.test_good,
        )

        self.test_budget.entries = [entry1, entry2]

        assert self.test_budget.entries == [entry1, entry2]

    def test_statuses_is_working_properly(self):
        """testing if Budget accepts statuses
        """
        self.test_budget.status = self.status_new
        assert self.test_budget.status == self.status_new

        self.test_budget.status = self.status_prev
        assert self.test_budget.status == self.status_prev

        self.test_budget.status = self.status_app
        assert self.test_budget.status == self.status_app


class BudgetEntryTestCase(BudgetTestBase):
    """tests the stalker.models.budget.BudgetEntry class
    """

    def test_budget_argument_is_skipped(self):
        """testing if a TypeError will be raised if the budget argument is
        skipped
        """
        with pytest.raises(TypeError) as cm:
            BudgetEntry(amount=10.0)

        assert str(cm.value) == \
            'BudgetEntry.budget should be a Budget instance, not NoneType'

    def test_budget_argument_is_none(self):
        """testing if a TypeError will be raised if the budget argument is
        None
        """
        with pytest.raises(TypeError) as cm:
            BudgetEntry(budget=None, amount=10.0)

        assert str(cm.value) == \
            'BudgetEntry.budget should be a Budget instance, not NoneType'

    def test_budget_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised if the budget attribute is
        set to None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
        )
        with pytest.raises(TypeError) as cm:
            entry.budget = None

        assert str(cm.value) == \
            'BudgetEntry.budget should be a Budget instance, not NoneType'

    def test_budget_argument_is_not_a_budget_instance(self):
        """testing if a TypeError will be raised if the budget argument is not
        a Budget instance
        """
        with pytest.raises(TypeError) as cm:
            BudgetEntry(
                budget='not a budget',
                amount=10.0
            )

        assert str(cm.value) == \
            'BudgetEntry.budget should be a Budget instance, not str'

    def test_budget_attribute_is_not_a_budget_instance(self):
        """testing if a TypeError will be raised if the budget attribute is not
        set to a something that is a Budget instance
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=10.0
        )
        with pytest.raises(TypeError) as cm:
            entry.budget = 'not a budget instance'

        assert str(cm.value) == \
            'BudgetEntry.budget should be a Budget instance, not str'

    def test_budget_argument_is_working_properly(self):
        """testing if the budget argument value is correctly passed to the
        budget attribute
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=10.0
        )
        assert entry.budget == self.test_budget

    def test_budget_attribute_is_working_properly(self):
        """testing if the budget attribute value can correctly be changed
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=10.0
        )
        new_budget = Budget(
            name='Test Budget',
            project=self.test_project,
            status_list=self.budget_status_list
        )
        assert entry.budget != new_budget
        entry.budget = new_budget
        assert entry.budget == new_budget

    def test_cost_attribute_value_will_be_copied_from_the_supplied_good_argument(self):
        """testing if the cost attribute value will be copied from the supplied
        good argument value
        """
        good = Good(name='Some Good', cost=10, msrp=20, unit='$/hour')
        entry = BudgetEntry(budget=self.test_budget, good=good)
        assert entry.cost == good.cost

    def test_cost_attribute_is_set_to_None(self):
        """testing if the cost attribute will be set to 0 if it is set to None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
        )
        assert entry.cost == self.test_good.cost
        entry.cost = None
        assert entry.cost == 0.0

    def test_cost_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if cost attribute is set to
        something other than a number
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
        )
        with pytest.raises(TypeError) as cm:
            entry.cost = 'some string'

        assert str(cm.value) == 'BudgetEntry.cost should be a number, not str'

    def test_cost_attribute_is_working_properly(self):
        """testing if the cost attribute is working properly
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
        )
        test_value = 5.0
        assert entry.cost != test_value
        entry.cost = test_value
        assert entry.cost == test_value

    def test_msrp_attribute_is_set_to_None(self):
        """testing if the msrp attribute will be set to 0 if msrp attribute is
        set to None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
        )
        assert entry.msrp == self.test_good.msrp
        entry.msrp = None
        assert entry.msrp == 0.0

    def test_msrp_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if msrp attribute is set to
        something other than a number
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
        )
        with pytest.raises(TypeError) as cm:
            entry.msrp = 'some string'

        assert str(cm.value) == 'BudgetEntry.msrp should be a number, not str'

    def test_msrp_attribute_is_working_properly(self):
        """testing if the msrp attribute is working properly
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
        )
        test_value = 5.0
        assert entry.msrp != test_value
        entry.msrp = test_value
        assert entry.msrp == test_value

    def test_msrp_attribute_value_will_be_copied_from_the_supplied_good_argument(self):
        """testing if the msrp attribute value will be copied from the supplied
        good argument value
        """
        entry = BudgetEntry(budget=self.test_budget, good=self.test_good)
        assert entry.msrp == self.test_good.msrp

    def test_price_argument_is_skipped(self):
        """testing if the price attribute will be 0 if the price argument is
        skipped
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
        )
        assert entry.price == 0.0

    def test_price_argument_is_set_to_None(self):
        """testing if the price attribute will be set to 0 if the price
        argument is set to None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            price=None
        )
        assert entry.price == 0.0

    def test_price_attribute_is_set_to_None(self):
        """testing if the price attribute will be set to 0 if price attribute
        is set to None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            price=10.0
        )
        assert entry.price == 10.0
        entry.price = None
        assert entry.price == 0.0

    def test_price_argument_is_not_a_number(self):
        """testing if a TypeError will be raised if the price argument is set
        to something other than a number
        """
        with pytest.raises(TypeError) as cm:
            BudgetEntry(
                budget=self.test_budget,
                good=self.test_good,
                price='some string'
            )

        assert str(cm.value) == 'BudgetEntry.price should be a number, not str'

    def test_price_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if price attribute is set to
        something other than a number
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            price=10
        )
        with pytest.raises(TypeError) as cm:
            entry.price = 'some string'

        assert str(cm.value) == 'BudgetEntry.price should be a number, not str'

    def test_price_argument_is_working_properly(self):
        """testing if the price argument value is correctly passed to the price
        attribute
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            price=10
        )
        assert entry.price == 10.0

    def test_price_attribute_is_working_properly(self):
        """testing if the price attribute is working properly
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            price=10
        )
        test_value = 5.0
        assert entry.price != test_value
        entry.price = test_value
        assert entry.price == test_value

    def test_realized_total_argument_is_skipped(self):
        """testing if the realized_total attribute will be 0 if the
        realized_total argument is skipped
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good
        )
        assert entry.realized_total == 0.0

    def test_realized_total_argument_is_set_to_None(self):
        """testing if the realized_total attribute will be set to 0 if the
        realized_total argument is set to None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            realized_total=None
        )
        assert entry.realized_total == 0.0

    def test_realized_total_attribute_is_set_to_None(self):
        """testing if the realized_total attribute will be set to 0 if it is
        set to None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            realized_total=10.0
        )
        assert entry.realized_total == 10.0
        entry.realized_total = None
        assert entry.realized_total == 0.0

    def test_realized_total_argument_is_not_a_number(self):
        """testing if a TypeError will be raised if the realized_total argument
        is set to something other than a number
        """
        with pytest.raises(TypeError) as cm:
            BudgetEntry(
                budget=self.test_budget,
                good=self.test_good,
                realized_total='some string'
            )

        assert str(cm.value) == \
            'BudgetEntry.realized_total should be a number, not str'

    def test_realized_total_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if realized_total attribute is
        set to something other than a number
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            realized_total=10
        )
        with pytest.raises(TypeError) as cm:
            entry.realized_total = 'some string'

        assert str(cm.value) == \
            'BudgetEntry.realized_total should be a number, not str'

    def test_realized_total_argument_is_working_properly(self):
        """testing if the realized_total argument value is correctly passed to
        the realized_total attribute
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            realized_total=10
        )
        assert entry.realized_total == 10.0

    def test_realized_total_attribute_is_working_properly(self):
        """testing if the realized_total attribute is working properly
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            realized_total=10
        )
        test_value = 5.0
        assert entry.realized_total != test_value
        entry.realized_total = test_value
        assert entry.realized_total == test_value

    def test_unit_attribute_is_set_to_None(self):
        """testing if the unit attribute will be set to an empty if it is set
        to None
        """
        entry = BudgetEntry(budget=self.test_budget, good=self.test_good)
        assert entry.unit == self.test_good.unit
        entry.unit = None
        assert entry.unit == ''

    def test_unit_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised if the unit attribute is set
        to something other than a string
        """
        entry = BudgetEntry(budget=self.test_budget, good=self.test_good)
        with pytest.raises(TypeError) as cm:
            entry.unit = 100.212

        assert str(cm.value) == \
            'BudgetEntry.unit should be a string, not float'

    def test_unit_attribute_is_working_properly(self):
        """testing if the unit attribute is working properly
        """
        entry = BudgetEntry(budget=self.test_budget, good=self.test_good)
        test_value = 'TL/hour'
        assert entry.unit != test_value
        entry.unit = test_value
        assert entry.unit == test_value

    def test_unit_attribute_value_will_be_copied_from_the_supplied_good(self):
        """testing if the unit attribute value will be copied from the good
        argument value
        """
        entry = BudgetEntry(budget=self.test_budget, good=self.test_good,)
        assert entry.unit == self.test_good.unit

    def test_amount_argument_is_skipped(self):
        """testing if the amount attribute will be 0 if the amount argument is
        skipped
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good
        )
        assert entry.amount == 0.0

    def test_amount_argument_is_set_to_None(self):
        """testing if the amount attribute will be set to 0 if the amount
        argument is set to None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=None
        )
        assert entry.amount == 0.0

    def test_amount_attribute_is_set_to_None(self):
        """testing if the amount attribute will be set to 0 if it is set to
        None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=10.0
        )
        assert entry.amount == 10.0
        entry.amount = None
        assert entry.amount == 0.0

    def test_amount_argument_is_not_a_number(self):
        """testing if a TypeError will be raised if the amount argument is set
        to something other than a number
        """
        with pytest.raises(TypeError) as cm:
            BudgetEntry(
                budget=self.test_budget,
                good=self.test_good,
                amount='some string'
            )

        assert str(cm.value) == \
            'BudgetEntry.amount should be a number, not str'

    def test_amount_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if amount attribute is set to
        something other than a number
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=10
        )
        with pytest.raises(TypeError) as cm:
            entry.amount = 'some string'

        assert str(cm.value) == \
            'BudgetEntry.amount should be a number, not str'

    def test_amount_argument_is_working_properly(self):
        """testing if the amount argument value is correctly passed to the
        amount attribute
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=10
        )
        assert entry.amount == 10.0

    def test_amount_attribute_is_working_properly(self):
        """testing if the amount attribute is working properly
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=10
        )
        test_value = 5.0
        assert entry.amount != test_value
        entry.amount = test_value
        assert entry.amount == test_value

    def test_good_argument_is_skipped(self):
        """testing if a TypeError will be raised when the good argument is
        skipped
        """
        with pytest.raises(TypeError) as cm:
            BudgetEntry(budget=self.test_budget)

        assert str(cm.value) == \
            'BudgetEntry.good should be a stalker.models.budget.Good ' \
            'instance, not NoneType'

    def test_good_argument_is_None(self):
        """testing if a TypeError will be raised when the good argument is None
        """
        with pytest.raises(TypeError) as cm:
            BudgetEntry(
                budget=self.test_budget,
                good=None,
                amount=53,
            )

        assert str(cm.value) == \
            'BudgetEntry.good should be a stalker.models.budget.Good ' \
            'instance, not NoneType'

    def test_good_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised if the good attribute is set
        to None
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=Good(name='Some Good'),
            amount=53
        )
        with pytest.raises(TypeError) as cm:
            entry.good = None

        assert str(cm.value) == \
            'BudgetEntry.good should be a stalker.models.budget.Good ' \
            'instance, not NoneType'

    def test_good_argument_is_not_a_good_instance(self):
        """testing if a TypeError will be raised when the good argument is not
        a Good instance
        """
        with pytest.raises(TypeError) as cm:
            entry = BudgetEntry(
                budget=self.test_budget,
                good='this is not a Good instance',
                amount=53,
            )

        assert str(cm.value) == \
            'BudgetEntry.good should be a stalker.models.budget.Good ' \
            'instance, not str'

    def test_good_attribute_is_not_a_good_instance(self):
        """testing if a TypeError will be raised when the good attribute is set
        to a value other than a Good instance
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=53,
        )
        with pytest.raises(TypeError) as cm:
            entry.good = 'this is not a Good instance'

        assert str(cm.value) == \
            'BudgetEntry.good should be a stalker.models.budget.Good ' \
            'instance, not str'

    def test_good_argument_is_working_properly(self):
        """testing if the good argument value is correctly passed to the good
        attribute
        """
        test_value = Good(name='Some Good')
        entry = BudgetEntry(
            budget=self.test_budget,
            good=test_value,
            amount=53,
        )
        assert entry.good == test_value

    def test_good_attribute_is_working_properly(self):
        """testing if the good attribute can be correctly set
        """
        test_value = Good(name='Some Other Good')
        entry = BudgetEntry(
            budget=self.test_budget,
            good=self.test_good,
            amount=53
        )
        assert entry.good != test_value
        entry.good = test_value
        assert entry.good == test_value


class BudgetDAGMixinTestCase(BudgetTestBase):
    """tests the parent/child relation of budgets
    """

    def test_parent_child_relation(self):
        """testing the parent/child relation of Budgets
        """
        b1 = Budget(**self.kwargs)
        b2 = Budget(**self.kwargs)

        b2.parent = b1
        assert b1.children == [b2]
