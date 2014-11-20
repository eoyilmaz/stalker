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

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, validates

from stalker.models.entity import Entity
from stalker.models.mixins import ProjectMixin


class Budget(Entity, ProjectMixin):
    """Manages project budgets

    Budgets manager :class:`.Project` budgets. You can create entries as
    instances of :class:`.BudgetEntry` class.
    """

    __auto_name__ = False
    __tablename__ = "Budgets"
    __mapper_args__ = {"polymorphic_identity": "Budget"}

    budget_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    )

    entries = relationship(
        'BudgetEntry',
        primaryjoin='BudgetEntries.c.budget_id==Budgets.c.id',
        uselist=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super(Budget, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)

    @validates('entries')
    def _validate_entry(self, key, entry):
        """validates the given entry value
        """
        if not isinstance(entry, BudgetEntry):
            raise TypeError(
                '%(class)s.entries should be a list of BudgetEntry instances, '
                'not %(entry_class)s' % {
                    'class': self.__class__.__name__,
                    'entry_class': entry.__class__.__name__
                }
            )
        return entry


class BudgetEntry(Entity):
    """Manages budget entries in a budget
    """

    __auto_name__ = True
    __tablename__ = "BudgetEntries"
    __mapper_args__ = {"polymorphic_identity": "BudgetEntry"}

    entry_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    )

    budget_id = Column(
        'budget_id',
        Integer,
        ForeignKey('Budgets.id')
    )

    budget = relationship(
        'Budget',
        primaryjoin='BudgetEntries.c.budget_id==Budgets.c.id',
        back_populates='entries',
        uselist=False
    )

    amount = Column(Float, default=0.0)

    def __init__(self, budget=None, amount=0.0, **kwargs):
        super(BudgetEntry, self).__init__(**kwargs)

        self.budget = budget
        self.amount = amount

    @validates('budget')
    def _validate_budget(self, key, budget):
        """validates the given budget value
        """
        if not isinstance(budget, Budget):
            raise TypeError(
                '%(class)s.budget should be a Budget instance, '
                'not %(budget_class)s' % {
                    'class': self.__class__.__name__,
                    'budget_class': budget.__class__.__name__
                }
            )
        return budget

    @validates('amount')
    def _validate_amount(self, key, amount):
        """validates the given amount value
        """
        if amount is None:
            amount = 0.0

        if not isinstance(amount, (int, float)):
            raise TypeError(
                '%(class)s.amount should be an integer or float, not '
                '%(amount_class)s' % {
                    'class': self.__class__.__name__,
                    'amount_class': amount.__class__.__name__
                }
            )

        return float(amount)
