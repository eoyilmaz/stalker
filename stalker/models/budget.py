# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey, Float, String, Table
from sqlalchemy.orm import relationship, validates
from stalker.db.declarative import Base

from stalker.models.entity import Entity
from stalker.models.mixins import (ProjectMixin, DAGMixin, StatusMixin,
                                   AmountMixin, UnitMixin)


class Good(Entity, UnitMixin):
    """Manages commercial items that is served by the Studio.

    A Studio can define service prices or items that's been sold by the Studio
    by using a list of commercial items.

    .. note::
       .. versionadded 0.2.20: Client Specific Goods

       Clients now can own a list of :class:`.Good` s attached to them.
       So one can define a list of :class:`.Good` s with special prices
       adjusted for a particular ``Client``, then get them back from the db by
       querying the :class:`.Good` s those have their ``client`` attribute set
       to that particular ``Client`` instance. Removing a ``Good`` from a
       :class:`.Client` will not delete it from the database, but deleting a
       :class:`.Client` will also delete the ``Good`` s attached to that
       particular :class:`.Client`.

    .. ::
       don't forget to update the Client documentation, which also has the same
       text.

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

    client_id = Column('client_id', Integer, ForeignKey('Clients.id'))
    client = relationship(
        'Client',
        primaryjoin='Goods.c.client_id==Clients.c.id',
        back_populates='goods',
        uselist=False
    )

    def __init__(self, cost=0.0, msrp=0.0, unit='', client=None, **kwargs):
        super(Good, self).__init__(**kwargs)
        UnitMixin.__init__(self, unit=unit)
        self.cost = cost
        self.msrp = msrp
        self.client = client

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

    @validates('client')
    def _validate_client(self, key, client):
        """validates the given client value
        """
        if client is not None:
            from stalker import Client
            if not isinstance(client, Client):
                raise TypeError(
                    '%s.client attribute should be a '
                    'stalker.models.client.Client instance, not %s' % (
                        self.__class__.__name__, client.__class__.__name__
                    )
                )
        return client


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


class Budget(Entity, ProjectMixin, DAGMixin, StatusMixin):
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

    invoices = relationship(
        'Invoice',
        primaryjoin='Invoices.c.budget_id==Budgets.c.id',
        uselist=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        super(Budget, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)
        DAGMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)

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


class BudgetEntry(Entity, AmountMixin, UnitMixin):
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
      bigger than the :attr:`.cost` and should be also bigger than
      :attr:`.msrp` but the person that is editing the budget which this entry
      is related to can decide to do a discount on this entry and give a
      different price. This attribute holds the proposed final price.
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

        kwargs['unit'] = good.unit
        kwargs['amount'] = amount

        AmountMixin.__init__(self, **kwargs)
        UnitMixin.__init__(self, **kwargs)

        self.price = price
        self.realized_total = realized_total

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


class Invoice(Entity, AmountMixin, UnitMixin):
    """Holds information about invoices

    Invoices are part of :class:`.Budgets`. The main purpose of invoices are
    to track the :class:`.Payment` s. It is a very primitive entity. It is
    by no means designed to hold real financial information (at least for now).

    :param client: The :class:`.Client` instance that shows the payer for
      this invoice.
    :type client: :class:`.Client`
    :param budget: The :class:`.Budget` instance that owns this invoice.
    :type budget: :class:`.Budget`
    :param int float amount: The amount of this invoice. Without the
      :attr:`.Invoice.unit` attribute it is meaningless. This can not be
      skipped.
    :param str unit: The unit of the issued amount. This can not be skipped.
    """

    __auto_name__ = True
    __tablename__ = "Invoices"
    __mapper_args__ = {"polymorphic_identity": "Invoice"}

    invoice_id = Column(
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
        primaryjoin='Invoices.c.budget_id==Budgets.c.id',
        back_populates='invoices',
        uselist=False
    )

    client_id = Column(
        Integer,
        ForeignKey('Clients.id')
    )

    client = relationship(
        'Client',
        primaryjoin='Invoices.c.client_id==Clients.c.id',
        uselist=False
    )

    payments = relationship(
        'Payment',
        primaryjoin='Payments.c.invoice_id==Invoices.c.id',
        uselist=True,
        cascade="all, delete-orphan"
    )

    def __init__(
            self,
            budget=None,
            client=None,
            amount=0,
            unit=None,
            **kwargs):
        super(Invoice, self).__init__(**kwargs)
        AmountMixin.__init__(self, amount=amount)
        UnitMixin.__init__(self, unit=unit)
        self.budget = budget
        self.client = client

    @validates('budget')
    def _validate_budget(self, key, budget):
        """validates the given budget value
        """
        if not isinstance(budget, Budget):
            raise TypeError(
                '%s.budget should be a Budget instance, not %s' % (
                    self.__class__.__name__,
                    budget.__class__.__name__
                )
            )
        return budget

    @validates('client')
    def _validate_client(self, key, client):
        """validates the given client value
        """
        from stalker import Client
        if not isinstance(client, Client):
            raise TypeError(
                '%s.client should be a Client instance, not %s' % (
                    self.__class__.__name__,
                    client.__class__.__name__
                )
            )
        return client


class Payment(Entity, AmountMixin, UnitMixin):
    """Holds information about the payments.

    Each payment should be related with an :class:`.Invoice` instance. Use the
    :attr:`.type` attribute to diversify payments (ex. "Advance").

    :param invoice: The :class:`.Invoice` instance that this payment is related
      to. This can not be skipped.
    :type invoice: :class:`.Invoice`
    """

    __auto_name__ = True
    __tablename__ = "Payments"
    __mapper_args__ = {"polymorphic_identity": "Payment"}

    payment_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey('Invoices.id')
    )

    invoice = relationship(
        'Invoice',
        primaryjoin='Payments.c.invoice_id==Invoices.c.id',
        back_populates='payments',
        uselist=False
    )

    def __init__(self, invoice=None, amount=0, unit=None, **kwargs):
        super(Payment, self).__init__(**kwargs)
        AmountMixin.__init__(self, amount=amount)
        UnitMixin.__init__(self, unit=unit)
        self.invoice = invoice

    @validates('invoice')
    def _validate_invoice(self, key, invoice):
        """validates the invoice value
        """
        if not isinstance(invoice, Invoice):
            raise TypeError(
                '%s.invoice should be an Invoice instance, not %s' % (
                    self.__class__.__name__,
                    invoice.__class__.__name__
                )
            )
        return invoice
