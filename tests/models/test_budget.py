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
import tempfile
import unittest
import datetime
from stalker import (db, defaults, Project, Status, StatusList, Type,
                     Repository, User, Budget, BudgetEntry)


class BudgetTestBase(unittest.TestCase):
    """the base for this test
    """

    def setUp(self):
        """run once
        """
        defaults.timing_resolution = datetime.timedelta(hours=1)

        # create a new session
        db.setup({
            'sqlalchemy.url': 'sqlite://',
            'sqlalchemy.echo': False
        })
        db.init()

        self.status_wfd = Status.query.filter_by(code="WFD").first()
        self.status_rts = Status.query.filter_by(code="RTS").first()
        self.status_wip = Status.query.filter_by(code="WIP").first()
        self.status_prev = Status.query.filter_by(code="PREV").first()
        self.status_hrev = Status.query.filter_by(code="HREV").first()
        self.status_drev = Status.query.filter_by(code="DREV").first()
        self.status_oh = Status.query.filter_by(code="OH").first()
        self.status_stop = Status.query.filter_by(code="STOP").first()
        self.status_cmpl = Status.query.filter_by(code="CMPL").first()

        self.task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

        self.test_project_status_list = StatusList(
            name="Project Statuses",
            statuses=[self.status_wip,
                      self.status_prev,
                      self.status_cmpl],
            target_entity_type=Project,
        )

        self.test_movie_project_type = Type(
            name="Movie Project",
            code='movie',
            target_entity_type=Project,
        )

        self.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type=Repository,
        )

        self.test_repository = Repository(
            name="Test Repository",
            type=self.test_repository_type,
            linux_path=tempfile.mkdtemp(),
            windows_path=tempfile.mkdtemp(),
            osx_path=tempfile.mkdtemp()
        )

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

        self.test_project = Project(
            name="Test Project1",
            code='tp1',
            type=self.test_movie_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repository
        )

        self.kwargs = {
            'project': self.test_project,
            'name': 'Test Budget 1'
        }

        self.test_budget = Budget(**self.kwargs)


class BudgetTest(BudgetTestBase):
    """tests the stalker.models.budget.Budget class
    """

    def test_entries_attribute_is_set_to_a_list_of_other_instances_than_a_budget_entry(self):
        """testing if a TypeError will be raised when the entries attribute is
        set to something other than a list of BugdgetEntries.
        """
        with self.assertRaises(TypeError) as cm:
            self.test_budget.entries = ['some', 'string', 1, 2]

        self.assertEqual(
            str(cm.exception),
            'Budget.entries should be a list of BudgetEntry instances, not str'
        )

    def test_entries_attribute_is_working_properly(self):
        """testing if the entries attribute is working properly
        """
        from stalker import BudgetEntry
        some_other_budget = Budget(
            name='Test Budget',
            project=self.test_project
        )
        entry1 = BudgetEntry(budget=some_other_budget)
        entry2 = BudgetEntry(budget=some_other_budget)

        self.test_budget.entries = [entry1, entry2]

        self.assertEqual(
            self.test_budget.entries,
            [entry1, entry2]
        )


class BudgetEntryTestCase(BudgetTestBase):
    """tests the stalker.models.budget.BudgetEntry class
    """

    def test_budget_argument_is_skipped(self):
        """testing if a TypeError will be raised if the budget argument is
        skipped
        """
        with self.assertRaises(TypeError) as cm:
            BudgetEntry(amount=10.0)

        self.assertEqual(
            str(cm.exception),
            'BudgetEntry.budget should be a Budget instance, not NoneType'
        )

    def test_budget_argument_is_none(self):
        """testing if a TypeError will be raised if the budget argument is
        None
        """
        with self.assertRaises(TypeError) as cm:
            BudgetEntry(budget=None, amount=10.0)

        self.assertEqual(
            str(cm.exception),
            'BudgetEntry.budget should be a Budget instance, not NoneType'
        )

    def test_budget_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised if the budget attribute is
        set to None
        """
        entry = BudgetEntry(
            budget=self.test_budget
        )
        with self.assertRaises(TypeError) as cm:
            entry.budget = None

        self.assertEqual(
            str(cm.exception),
            'BudgetEntry.budget should be a Budget instance, not NoneType'
        )

    def test_budget_argument_is_not_a_budget_instance(self):
        """testing if a TypeError will be raised if the budget argument is not
        a Budget instance
        """
        with self.assertRaises(TypeError) as cm:
            BudgetEntry(
                budget='not a budget',
                amount=10.0
            )

        self.assertEqual(
            str(cm.exception),
            'BudgetEntry.budget should be a Budget instance, not str'
        )

    def test_budget_attribute_is_not_a_budget_instance(self):
        """testing if a TypeError will be raised if the budget attribute is not
        set to a something that is a Budget instance
        """
        entry = BudgetEntry(budget=self.test_budget, amount=10.0)
        with self.assertRaises(TypeError) as cm:
            entry.budget = 'not a budget instance'

        self.assertEqual(
            str(cm.exception),
            'BudgetEntry.budget should be a Budget instance, not str'
        )

    def test_budget_argument_is_working_properly(self):
        """testing if the budget argument value is correctly passed to the
        budget attribute
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            amount=10.0
        )
        self.assertEqual(entry.budget, self.test_budget)

    def test_budget_attribute_is_working_properly(self):
        """testing if the budget attribute value can correctly be changed
        """
        entry = BudgetEntry(
            budget=self.test_budget,
            amount=10.0
        )
        new_budget = Budget(name='Test Budget', project=self.test_project)
        self.assertNotEqual(entry.budget, new_budget)
        entry.budget = new_budget
        self.assertEqual(entry.budget, new_budget)

    def test_amount_argument_is_skipped(self):
        """testing if the amount attribute will be 0 if the amount argument is
        skipped
        """
        entry = BudgetEntry(budget=self.test_budget)
        self.assertEqual(entry.amount, 0.0)

    def test_amount_argument_is_set_to_None(self):
        """testing if the amount attribute will be set to 0 if the amount
        argument is set to None
        """
        entry = BudgetEntry(budget=self.test_budget, amount=None)
        self.assertEqual(entry.amount, 0.0)

    def test_amount_attribute_is_set_to_None(self):
        """testing if the amount attribute will be set to 0 if it is set to
        None
        """
        entry = BudgetEntry(budget=self.test_budget, amount=10.0)
        self.assertEqual(entry.amount, 10.0)
        entry.amount = None
        self.assertEqual(entry.amount, 0.0)

    def test_amount_argument_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised if the amount argument is set
        to something other than an integer or float
        """
        with self.assertRaises(TypeError) as cm:
            BudgetEntry(budget=self.test_budget, amount='some string')

        self.assertEqual(
            str(cm.exception),
            'BudgetEntry.amount should be an integer or float, not str'
        )

    def test_amount_attribute_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised if it is set to something
        other than an integer or float
        """
        entry = BudgetEntry(budget=self.test_budget, amount=10)
        with self.assertRaises(TypeError) as cm:
            entry.amount = 'some string'

        self.assertEqual(
            str(cm.exception),
            'BudgetEntry.amount should be an integer or float, not str'
        )

    def test_amount_argument_is_working_properly(self):
        """testing if the amount argument value is correctly passed to the
        amount attribute
        """
        entry = BudgetEntry(budget=self.test_budget, amount=10)
        self.assertEqual(entry.amount, 10.0)

    def test_amount_attribute_is_working_properly(self):
        """testing if the amount attribute is working properly
        """
        entry = BudgetEntry(budget=self.test_budget, amount=10)
        test_value = 5.0
        self.assertNotEqual(entry.amount, test_value)
        entry.amount = test_value
        self.assertEqual(entry.amount, test_value)
