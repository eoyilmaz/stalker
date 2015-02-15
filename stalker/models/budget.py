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

from sqlalchemy import Column, Integer, ForeignKey, Float, String, Table
from sqlalchemy.orm import relationship, validates
from stalker.db import Base

from stalker.models.entity import Entity
from stalker.models.mixins import ProjectMixin, DAGMixin


class Good(Entity):
    """Manages commercial items that is served by the Studio.

    A Studio can define service prices or items that's been sold by the Studio
    by using a list of commercial items.

    A Good has the following attributes

    :param msrp: The suggested retail price for this item.

    :param cost: The cost of this item to the Studio, so generally it is better
      to keep price of the related BudgetEntry bigger than this value to get
      profit by selling this item.

    :param unit: The unit of this item.
    """

    __auto_name__ = False
    __tablename__ = 'Goods'
    __mapper_args__ = {'polymorphic_identity': 'Good'}

    good_id = Column(
        'id',
        Integer,
        ForeignKey('Entities.id'),
        primary_key=True
    )

    price_lists = relationship(
        'PriceList',
        secondary='PriceList_Goods',
        primaryjoin='Goods.c.id==PriceList_Goods.c.good_id',
        secondaryjoin='PriceList_Goods.c.price_list_id==PriceLists.c.id',
        back_populates='goods',
        doc='PriceLists that this good is related to.'
    )

    cost = Column(Float, default=0.0)
    msrp = Column(Float, default=0.0)
    unit = Column(String(64))

    def __init__(self, cost=0.0, msrp=0.0, unit='', **kwargs):
        super(Good, self).__init__(**kwargs)
        self.cost = cost
        self.msrp = msrp
        self.unit = unit

    @validates('cost')
    def _validate_cost(self, key, cost):
        """validates the given cost value
        """
        if cost is None:
            cost = 0.0

        if not isinstance(cost, (float, int)):
            raise TypeError(
                '%s.cost should be a non-negative number, not %s' % (
                    self.__class__.__name__,
                    cost.__class__.__name__
                )
            )

        if cost < 0.0:
            raise ValueError(
                '%s.cost should be a non-negative number' %
                self.__class__.__name__
            )

        return cost

    @validates('msrp')
    def _validate_msrp(self, key, msrp):
        """validates the given msrp value
        """
        if msrp is None:
            msrp = 0.0

        if not isinstance(msrp, (float, int)):
            raise TypeError(
                '%s.msrp should be a non-negative number, not %s' % (
                    self.__class__.__name__,
                    msrp.__class__.__name__
                )
            )

        if msrp < 0.0:
            raise ValueError(
                '%s.msrp should be a non-negative number' %
                self.__class__.__name__
            )

        return msrp

    @validates('unit')
    def _validate_unit(self, key, unit):
        """validates the given unit value
        """
        if unit is None:
            unit = ''

        from stalker import __string_types__
        if not isinstance(unit, __string_types__):
            raise TypeError(
                '%s.unit should be a str, not %s' % (
                    self.__class__.__name__,
                    unit.__class__.__name__
                )
            )

        return unit


class PriceList(Entity):
    """Contains CommercialItems to create a list of items that is sold by the
    Studio.

    You can create different lists for items sold in this studio.
    """

    __auto_name__ = False
    __tablename__ = 'PriceLists'
    __mapper_args__ = {'polymorphic_identity': 'PriceList'}

    price_list_id = Column(
        'id',
        Integer,
        ForeignKey('Entities.id'),
        primary_key=True
    )

    goods = relationship(
        'Good',
        secondary='PriceList_Goods',
        primaryjoin='PriceLists.c.id==PriceList_Goods.c.price_list_id',
        secondaryjoin='PriceList_Goods.c.good_id==Goods.c.id',
        back_populates='price_lists',
        doc='Goods in this list.'
    )

    def __init__(self, goods=None, **kwargs):
        super(PriceList, self).__init__(**kwargs)
        if goods is None:
            goods = []
        self.goods = goods

    @validates('goods')
    def _validate_goods(self, key, good):
        """validates the given good value
        """
        from stalker import Good
        if not isinstance(good, Good):
            raise TypeError(
                '%s.goods should be a list of stalker.model.bugdet.Good '
                'instances, not %s' % (
                    self.__class__.__name__,
                    good.__class__.__name__
                )
            )

        return good

PriceList_Goods = Table(
    'PriceList_Goods', Base.metadata,
    Column(
        'price_list_id',
        Integer,
        ForeignKey('PriceLists.id'),
        primary_key=True
    ),
    Column(
        'good_id',
        Integer,
        ForeignKey('Goods.id'),
        primary_key=True
    )
)


class Budget(Entity, ProjectMixin, DAGMixin):
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

    __id_column__ = 'budget_id'

    entries = relationship(
        'BudgetEntry',
        primaryjoin='BudgetEntries.c.budget_id==Budgets.c.id',
        uselist=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super(Budget, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)
        DAGMixin.__init__(self, **kwargs)

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
    """Manages entries in a Budget.

    With BudgetEntries one can manage project budget entries one by one. Each
    entry shows one component of a bigger budget. Entries are generally a
    reflection of a :class:`.Good` instance and shows how many of that Good has
    been included in this Budget, and what was the discounted price of that
    Good.

    :param budget: The :class:`.Budget` that this entry is a part of.
    :param good: Stores a :class:`.Good` instance to carry all the
      cost/msrp/unit data from.
    :param float price: The decided price of this entry. This is generally
      bigger than the cost and should be also bigger than msrp but the person
      that is editing the the budget which this entry is related to can decide
      to do a discount on this entry and give a different price. This attribute
      holds the proposed final price.
    :param float realized_total: This attribute is for holding the realized
      price of this entry. It can be the same number of the :attr:`.price`
      multiplied by the :attr:`.amount` or can be something else that reflects
      the reality. Generally it is for calculating the "service" cost/profit.
    :param float amount: Defines the amount of :class:`Good` that is in
      consideration for this entry.
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
        Integer,
        ForeignKey('Budgets.id')
    )

    budget = relationship(
        'Budget',
        primaryjoin='BudgetEntries.c.budget_id==Budgets.c.id',
        back_populates='entries',
        uselist=False
    )

    good_id = Column(
        Integer,
        ForeignKey('Goods.id')
    )

    good = relationship(
        'Good',
        primaryjoin='BudgetEntries.c.good_id==Goods.c.id',
        uselist=False
    )

    cost = Column(Float, default=0.0)
    msrp = Column(Float, default=0.0)

    price = Column(Float, default=0.0)
    realized_total = Column(Float, default=0.0)

    unit = Column(String(64))
    amount = Column(Float, default=0.0)

    def __init__(self,
                 budget=None,
                 good=None,
                 price=0,
                 realized_total=0,
                 amount=0.0,
                 **kwargs):
        super(BudgetEntry, self).__init__(**kwargs)

        self.budget = budget
        self.good = good
        self.cost = good.cost
        self.msrp = good.msrp
        self.unit = good.unit

        self.price = price
        self.realized_total = realized_total

        self.amount = amount

    @validates('budget')
    def _validate_budget(self, key, budget):
        """validates the given budget value
        """
        if not isinstance(budget, Budget):
            raise TypeError(
                '%s.budget should be a Budget instance, not %s' % (
                    self.__class__.__name__, budget.__class__.__name__
                )
            )
        return budget

    @validates('cost')
    def _validate_cost(self, key, cost):
        """validates the given cost value
        """
        if cost is None:
            cost = 0.0

        if not isinstance(cost, (int, float)):
            raise TypeError(
                '%s.cost should be a number, not %s' % (
                    self.__class__.__name__, cost.__class__.__name__
                )
            )

        return float(cost)

    @validates('msrp')
    def _validate_msrp(self, key, msrp):
        """validates the given msrp value
        """
        if msrp is None:
            msrp = 0.0

        if not isinstance(msrp, (int, float)):
            raise TypeError(
                '%s.msrp should be a number, not %s' % (
                    self.__class__.__name__, msrp.__class__.__name__
                )
            )

        return float(msrp)

    @validates('price')
    def _validate_price(self, key, price):
        """validates the given price value
        """
        if price is None:
            price = 0.0

        if not isinstance(price, (int, float)):
            raise TypeError(
                '%s.price should be a number, not %s' % (
                    self.__class__.__name__, price.__class__.__name__
                )
            )

        return float(price)

    @validates('realized_total')
    def _validate_realized_total(self, key, realized_total):
        """validates the given realized_total value
        """
        if realized_total is None:
            realized_total = 0.0

        if not isinstance(realized_total, (int, float)):
            raise TypeError(
                '%s.realized_total should be a number, not %s' % (
                    self.__class__.__name__,
                    realized_total.__class__.__name__
                )
            )

        return float(realized_total)

    @validates('unit')
    def _validate_unit(self, key, unit):
        """validates the given unit value
        """
        if unit is None:
            unit = ''

        from stalker import __string_types__
        if not isinstance(unit, __string_types__):
            raise TypeError(
                '%s.unit should be a string, not %s' % (
                    self.__class__.__name__, unit.__class__.__name__
                )
            )

        return unit

    @validates('amount')
    def _validate_amount(self, key, amount):
        """validates the given amount value
        """
        if amount is None:
            amount = 0.0

        if not isinstance(amount, (int, float)):
            raise TypeError(
                '%s.amount should be a number, not %s' % (
                    self.__class__.__name__, amount.__class__.__name__
                )
            )

        return float(amount)

    @validates('good')
    def _validate_good(self, key, good):
        """validates the given good value
        """
        if not isinstance(good, Good):
            raise TypeError(
                '%s.good should be a stalker.models.budget.Good instance, '
                'not %s' % (
                    self.__class__.__name__, good.__class__.__name__
                )
            )

        return good
