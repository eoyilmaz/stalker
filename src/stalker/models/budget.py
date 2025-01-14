# -*- coding: utf-8 -*-
"""Budget related classes and functions are situated here."""
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import (
    AmountMixin,
    DAGMixin,
    ProjectMixin,
    StatusMixin,
    UnitMixin,
)

if TYPE_CHECKING:  # pragma: no cover
    from stalker.models.client import Client


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

    Args:
        cost (Union[int, float]): The cost of this item to the Studio, so
            generally it is better to keep price of the related BudgetEntry
            bigger than this value to get profit by selling this item.
        msrp (Union[int, float]): The suggested retail price for this item.
        unit (str): The unit of this item.
    """

    __auto_name__ = False
    __tablename__ = "Goods"
    __mapper_args__ = {"polymorphic_identity": "Good"}

    good_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    price_lists: Mapped["PriceList"] = relationship(
        secondary="PriceList_Goods",
        primaryjoin="Goods.c.id==PriceList_Goods.c.good_id",
        secondaryjoin="PriceList_Goods.c.price_list_id==PriceLists.c.id",
        back_populates="goods",
        doc="PriceLists that this good is related to.",
    )

    cost: Mapped[Optional[float]] = mapped_column(default=0.0)
    msrp: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    unit: Mapped[Optional[str]] = mapped_column(String(64))

    client_id: Mapped[Optional[int]] = mapped_column(
        "client_id", ForeignKey("Clients.id")
    )
    client: Mapped["Client"] = relationship(
        primaryjoin="Goods.c.client_id==Clients.c.id",
        back_populates="goods",
        uselist=False,
    )

    def __init__(
        self,
        cost: Union[int, float] = 0.0,
        msrp: Union[int, float] = 0.0,
        unit: str = "",
        client: Optional["Client"] = None,
        **kwargs,
    ) -> None:
        super(Good, self).__init__(**kwargs)
        UnitMixin.__init__(self, unit=unit)
        self.cost = cost
        self.msrp = msrp
        self.client = client

    @validates("cost")
    def _validate_cost(self, key: str, cost: Union[int, float]) -> Union[int, float]:
        """Validate the given cost value.

        Args:
            key (str): The name of the validated column.
            cost (Union[int, float]): The cost value to be validated.

        Raises:
            TypeError: If the given cost value is not an int or float.
            ValueError: If the given cost is a negative value.

        Returns:
            float: The validated cost value.
        """
        if cost is None:
            cost = 0.0

        if not isinstance(cost, (float, int)):
            raise TypeError(
                f"{self.__class__.__name__}.cost should be a non-negative number, "
                f"not {cost.__class__.__name__}: '{cost}'"
            )

        if cost < 0.0:
            raise ValueError(
                f"{self.__class__.__name__}.cost should be a non-negative number"
            )

        return cost

    @validates("msrp")
    def _validate_msrp(self, key: str, msrp: Union[int, float]) -> Union[int, float]:
        """Validate the given msrp value.

        Args:
            key (str): The name of the validated column.
            msrp (Union[int, float]): The msrp value to be validated.

        Raises:
            TypeError: If the given msrp value is not an int or float.
            ValueError: If the msrp is a negative value.

        Returns:
            float: The validated msrp value.
        """
        if msrp is None:
            msrp = 0.0

        if not isinstance(msrp, (float, int)):
            raise TypeError(
                f"{self.__class__.__name__}.msrp should be a non-negative number, "
                f"not {msrp.__class__.__name__}: '{msrp}'"
            )

        if msrp < 0.0:
            raise ValueError(
                f"{self.__class__.__name__}.msrp should be a non-negative number"
            )

        return msrp

    @validates("client")
    def _validate_client(self, key: str, client: "Client") -> "Client":
        """Validate the given client value.

        Args:
            key (str): The name of the validated column.
            client (Client): The client value to be validated.

        Raises:
            TypeError: If the given client arg value is not a
                :class:`stalker.models.client.Client` instance.

        Returns:
            Client: The validated :class:`stalker.models.client.Client` instance.
        """
        if client is not None:
            from stalker.models.client import Client

            if not isinstance(client, Client):
                raise TypeError(
                    f"{self.__class__.__name__}.client attribute should be a "
                    "stalker.models.client.Client instance, "
                    f"not {client.__class__.__name__}: '{client}'"
                )
        return client


class PriceList(Entity):
    """Contains CommercialItems to create a list of items that is sold by the Studio.

    You can create different lists for items sold in this studio.

    Args:
        goods (List[Good]): A list of :class:`.Good` instances to be put into this
            :class:`.PriceList` instance.
    """

    __auto_name__ = False
    __tablename__ = "PriceLists"
    __mapper_args__ = {"polymorphic_identity": "PriceList"}

    price_list_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    goods: Mapped[Optional[List["Good"]]] = relationship(
        secondary="PriceList_Goods",
        primaryjoin="PriceLists.c.id==PriceList_Goods.c.price_list_id",
        secondaryjoin="PriceList_Goods.c.good_id==Goods.c.id",
        back_populates="price_lists",
        doc="Goods in this list.",
    )

    def __init__(
        self,
        goods: Optional[List["Good"]] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super(PriceList, self).__init__(**kwargs)
        if goods is None:
            goods = []
        self.goods = goods

    @validates("goods")
    def _validate_goods(self, key: str, good: "Good") -> "Good":
        """Validate the given good value.

        Args:
            key (str): The name of the validated column.
            good (Good): The good value to be validated.

        Raises:
            TypeError: If the given good arg value is not a :class:`.Good` instance.

        Returns:
            Good: The validated :class:`.Good` instance.
        """
        if not isinstance(good, Good):
            raise TypeError(
                f"{self.__class__.__name__}.goods should only contain "
                "instances of stalker.model.budget.Good, "
                f"not {good.__class__.__name__}: '{good}'"
            )
        return good


PriceList_Goods = Table(
    "PriceList_Goods",
    Base.metadata,
    Column("price_list_id", Integer, ForeignKey("PriceLists.id"), primary_key=True),
    Column("good_id", Integer, ForeignKey("Goods.id"), primary_key=True),
)


class Budget(Entity, ProjectMixin, DAGMixin, StatusMixin):
    """Manages project budgets.

    Budgets manager :class:`.Project` budgets. You can create entries as
    instances of :class:`.BudgetEntry` class.
    """

    __auto_name__ = False
    __tablename__ = "Budgets"
    __mapper_args__ = {"polymorphic_identity": "Budget"}

    budget_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    __id_column__ = "budget_id"

    entries: Mapped[Optional[List["BudgetEntry"]]] = relationship(
        primaryjoin="BudgetEntries.c.budget_id==Budgets.c.id",
        cascade="all, delete-orphan",
    )

    invoices: Mapped[Optional[List["Invoice"]]] = relationship(
        primaryjoin="Invoices.c.budget_id==Budgets.c.id",
        cascade="all, delete-orphan",
    )

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super(Budget, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)
        DAGMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)

    @validates("entries")
    def _validate_entry(self, key: str, entry: "BudgetEntry") -> "BudgetEntry":
        """Validate the given entry value.

        Args:
            key (str): The name of the validated column.
            entry (BudgetEntry): The entry value to be validated.

        Raises:
            TypeError: If the given entry value is not a :class:`.BudgetEntry` instance.

        Returns:
            BudgetEntry: The validated BudgetEntry instance.
        """
        if not isinstance(entry, BudgetEntry):
            raise TypeError(
                f"{self.__class__.__name__}.entries should only contain "
                "instances of BudgetEntry, "
                f"not {entry.__class__.__name__}: '{entry}'"
            )
        return entry


class BudgetEntry(Entity, AmountMixin, UnitMixin):
    """Manages entries in a Budget.

    With BudgetEntries one can manage project budget entries one by one. Each
    entry shows one component of a bigger budget. Entries are generally a
    reflection of a :class:`.Good` instance and shows how many of that Good has
    been included in this Budget, and what was the discounted price of that
    Good.

    Args:
        budget (Budget): The :class:`.Budget` that this entry is a part of.
        good (Good): Stores a :class:`.Good` instance to carry all the cost/msrp/unit
            data from.
        price (float): The decided price of this entry. This is generally bigger than
            the :attr:`.cost` and should be also bigger than :attr:`.msrp` but the
            person that is editing the budget which this entry is related to can decide
            to do a discount on this entry and give a different price. This attribute
            holds the proposed final price.
        realized_total (float): This attribute is for holding the realized price of this
            entry. It can be the same number of the :attr:`.price` multiplied by the
            :attr:`.amount` or can be something else that reflects the reality.
            Generally it is for calculating the "service" cost/profit.
        amount (float): Defines the amount of :class:`Good` that is in consideration for
            this entry.
    """

    __auto_name__ = True
    __tablename__ = "BudgetEntries"
    __mapper_args__ = {"polymorphic_identity": "BudgetEntry"}

    entry_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )
    budget_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Budgets.id"))
    budget: Mapped["Budget"] = relationship(
        primaryjoin="BudgetEntries.c.budget_id==Budgets.c.id",
        back_populates="entries",
        uselist=False,
    )

    good_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Goods.id"))

    good: Mapped["Good"] = relationship(
        primaryjoin="BudgetEntries.c.good_id==Goods.c.id", uselist=False
    )

    cost: Mapped[Optional[float]] = mapped_column(default=0.0)
    msrp: Mapped[Optional[float]] = mapped_column(default=0.0)

    price: Mapped[Optional[float]] = mapped_column(default=0.0)
    realized_total: Mapped[Optional[float]] = mapped_column(default=0.0)

    def __init__(
        self,
        budget: Optional[Budget] = None,
        good: Optional[Good] = None,
        price: Union[float, int] = 0,
        realized_total: Union[float, int] = 0,
        amount: Union[float, int] = 0.0,
        **kwargs: Dict[str, Any],
    ) -> None:
        super(BudgetEntry, self).__init__(**kwargs)

        self.budget = budget
        self.good = good
        self.cost = good.cost
        self.msrp = good.msrp

        kwargs["unit"] = good.unit
        kwargs["amount"] = amount

        AmountMixin.__init__(self, **kwargs)
        UnitMixin.__init__(self, **kwargs)

        self.price = price
        self.realized_total = realized_total

    @validates("budget")
    def _validate_budget(self, key: str, budget: "Budget") -> "Budget":
        """Validate the given budget value.

        Args:
            key (str): The name of the validated column.
            budget (Budget): The budget that needs to be validated.

        Raises:
            TypeError: If the given budget is not a :class:`.Budget` instance.

        Returns:
            Budget: The validated :class:`.Budget` instance.
        """
        if not isinstance(budget, Budget):
            raise TypeError(
                f"{self.__class__.__name__}.budget should be a Budget instance, "
                f"not {budget.__class__.__name__}: '{budget}'"
            )
        return budget

    @validates("cost")
    def _validate_cost(self, key: str, cost: Union[float, int]) -> float:
        """Validate the given cost value.

        Args:
            key (str): The name of the validated column.
            cost (Union[int, float]): The cost value to be validated.

        Raises:
            TypeError: If the given cost value is not an int or float.

        Returns:
            float: The validated cost value.
        """
        if cost is None:
            cost = 0.0

        if not isinstance(cost, (int, float)):
            raise TypeError(
                f"{self.__class__.__name__}.cost should be a number, "
                f"not {cost.__class__.__name__}: '{cost}'"
            )

        return float(cost)

    @validates("msrp")
    def _validate_msrp(self, key: str, msrp: Union[float, int]) -> float:
        """Validate the given msrp value.

        Args:
            key (str): The name of the validated column.
            msrp (Union[int, float]): The msrp value to be validated.

        Raises:
            TypeError: If the given msrp value is not an int or float.

        Returns:
            float: The validated msrp value.
        """
        if msrp is None:
            msrp = 0.0

        if not isinstance(msrp, (int, float)):
            raise TypeError(
                f"{self.__class__.__name__}.msrp should be a number, "
                f"not {msrp.__class__.__name__}: '{msrp}'"
            )

        return float(msrp)

    @validates("price")
    def _validate_price(self, key: str, price: Union[float, int]) -> float:
        """Validate the given price value.

        Args:
            key (str): The name of the validated column.
            price (Union[int, float]): The price value to be validated.

        Raises:
            TypeError: If the given price value is not an int or float.

        Returns:
            float: The validated price value.
        """
        if price is None:
            price = 0.0

        if not isinstance(price, (int, float)):
            raise TypeError(
                f"{self.__class__.__name__}.price should be a number, "
                f"not {price.__class__.__name__}: '{price}'"
            )

        return float(price)

    @validates("realized_total")
    def _validate_realized_total(
        self, key: str, realized_total: Union[float, int]
    ) -> float:
        """Validate  the given realized_total value.

        Args:
            key (str): The name of the validated column.
            realized_total (Union[int, float]): The realized_total value to be
                validated.

        Raises:
            TypeError: If the given realized_total value is not an int or float.

        Returns:
            float: The validated realized_total value.
        """
        if realized_total is None:
            realized_total = 0.0

        if not isinstance(realized_total, (int, float)):
            raise TypeError(
                f"{self.__class__.__name__}.realized_total should be a number, "
                f"not {realized_total.__class__.__name__}: '{realized_total}'"
            )

        return float(realized_total)

    @validates("good")
    def _validate_good(self, key: str, good: "Good") -> "Good":
        """Validate the given good value.

        Args:
            key (str): The name of the validated column.
            good (Good): The good to be validated.

        Raises:
            TypeError: If the given good is not a :class:`.Good` instance.

        Returns:
            Good: Returns the validated :class:`.Good` instance.
        """
        if not isinstance(good, Good):
            raise TypeError(
                f"{self.__class__.__name__}.good should be a "
                "stalker.models.budget.Good instance, "
                f"not {good.__class__.__name__}: '{good}'"
            )

        return good


class Invoice(Entity, AmountMixin, UnitMixin):
    """Holds information about invoices.

    Invoices are part of :class:`.Budgets`. The main purpose of invoices are
    to track the :class:`.Payment` s. It is a very primitive entity. It is
    by no means designed to hold real financial information (at least for now).

    Args:
        client (Client): The :class:`.Client` instance that shows the payer for this
            invoice.
        budget (Budget): The :class:`.Budget` instance that owns this invoice.
        amount (Union[int, float]): The amount of this invoice. Without the
            :attr:`.Invoice.unit` attribute it is meaningless. This cannot be skipped.
        unit (str): The unit of the issued amount. This cannot be skipped.
    """

    __auto_name__ = True
    __tablename__ = "Invoices"
    __mapper_args__ = {"polymorphic_identity": "Invoice"}

    invoice_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )
    budget_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Budgets.id"))

    budget: Mapped[Optional["Budget"]] = relationship(
        primaryjoin="Invoices.c.budget_id==Budgets.c.id",
        back_populates="invoices",
        uselist=False,
    )

    client_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Clients.id"))

    client: Mapped[Optional["Client"]] = relationship(
        primaryjoin="Invoices.c.client_id==Clients.c.id", uselist=False
    )

    payments: Mapped[Optional[List["Payment"]]] = relationship(
        primaryjoin="Payments.c.invoice_id==Invoices.c.id",
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        budget: Optional["Budget"] = None,
        client: Optional["Client"] = None,
        amount: Union[float, int] = 0,
        unit: Optional[str] = None,
        **kwargs,
    ) -> None:
        super(Invoice, self).__init__(**kwargs)
        AmountMixin.__init__(self, amount=amount)
        UnitMixin.__init__(self, unit=unit)
        self.budget = budget
        self.client = client

    @validates("budget")
    def _validate_budget(self, key: str, budget: "Budget") -> "Budget":
        """Validate the given budget value.

        Args:
            key (str): The name of the validated column.
            budget (Budget): The :class:`.Budget` instance to be validated.

        Raises:
            TypeError: If the given budget arg value is not a :class:`.Budget` instance.

        Returns:
            Budget: The validated :class:`.Budget` instance.
        """
        if not isinstance(budget, Budget):
            raise TypeError(
                f"{self.__class__.__name__}.budget should be a Budget instance, "
                f"not {budget.__class__.__name__}: '{budget}'"
            )
        return budget

    @validates("client")
    def _validate_client(self, key: str, client: "Client") -> "Client":
        """Validate the given client value.

        Args:
            key (str): The name of the validated column.
            client (Client): The :class:`stalker.models.client.Client` instance to be
                validated.

        Raises:
            TypeError: If the ``client`` is not a :class:`stalker.models.client.Client`
                instance.

        Returns:
            Client: The validated :class:`stalker.models.client.Client` instance.
        """
        from stalker.models.client import Client

        if not isinstance(client, Client):
            raise TypeError(
                f"{self.__class__.__name__}.client should be a Client instance, "
                f"not {client.__class__.__name__}: '{client}'"
            )
        return client


class Payment(Entity, AmountMixin, UnitMixin):
    """Holds information about the payments.

    Each payment should be related with an :class:`.Invoice` instance. Use the
    :attr:`.type` attribute to diversify payments (ex. "Advance").

    Args:
        invoice (Invoice): The :class:`.Invoice` instance that this payment is related
            to. This cannot be skipped.
        amount (Union[int, float]): The amount value.
        unit (Optional[str]): The unit of this mixed in class.
    """

    __auto_name__ = True
    __tablename__ = "Payments"
    __mapper_args__ = {"polymorphic_identity": "Payment"}

    payment_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )
    invoice_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Invoices.id"))
    invoice: Mapped[Optional["Invoice"]] = relationship(
        primaryjoin="Payments.c.invoice_id==Invoices.c.id",
        back_populates="payments",
        uselist=False,
    )

    def __init__(
        self,
        invoice: Optional["Invoice"] = None,
        amount: Union[int, float] = 0,
        unit: Optional[str] = None,
        **kwargs,
    ) -> None:
        super(Payment, self).__init__(**kwargs)
        AmountMixin.__init__(self, amount=amount)
        UnitMixin.__init__(self, unit=unit)
        self.invoice = invoice

    @validates("invoice")
    def _validate_invoice(self, key: str, invoice: "Invoice") -> "Invoice":
        """Validate the invoice value.

        Args:
            key (str): The name of the validated column.
            invoice (Invoice): The :class:`.Invoice` instance to validate.

        Raises:
            TypeError: The :class:`.Invoice` instance to be validated.

        Returns:
            Invoice: The validated :class:`.Invoice` instance.
        """
        if not isinstance(invoice, Invoice):
            raise TypeError(
                f"{self.__class__.__name__}.invoice should be an Invoice instance, "
                f"not {invoice.__class__.__name__}: '{invoice}'"
            )
        return invoice
