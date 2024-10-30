# -*- coding: utf-8 -*-
"""AmountMixin related tests."""

import pytest

from sqlalchemy import Column, ForeignKey, Integer

from stalker import AmountMixin, SimpleEntity


class AmountMixinFooMixedInClass(SimpleEntity, AmountMixin):
    """A class which derives from another which has and __init__ already."""

    __tablename__ = "AmountMixinFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "AmountMixinFooMixedInClass"}
    amountMixinFooMixedInClass_id = Column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )
    __id_column__ = "amountMixinFooMixedInClass_id"

    def __init__(self, **kwargs):
        super(AmountMixinFooMixedInClass, self).__init__(**kwargs)
        AmountMixin.__init__(self, **kwargs)


def test_mixed_in_class_initialization():
    """init() is working properly."""
    a = AmountMixinFooMixedInClass(amount=1500)
    assert isinstance(a, AmountMixinFooMixedInClass)
    assert a.amount == 1500


def test_amount_argument_is_skipped():
    """amount attribute will be 0 if the amount argument is skipped."""
    entry = AmountMixinFooMixedInClass()
    assert entry.amount == 0.0


def test_amount_argument_is_set_to_none():
    """amount attribute will be 0 if the amount argument is None."""
    entry = AmountMixinFooMixedInClass(amount=None)
    assert entry.amount == 0.0


def test_amount_attribute_is_set_to_none():
    """amount attribute will be set to 0 if it is set to None."""
    entry = AmountMixinFooMixedInClass(amount=10.0)
    assert entry.amount == 10.0
    entry.amount = None
    assert entry.amount == 0.0


def test_amount_argument_is_not_a_number():
    """TypeError will be raised if the amount argument is not a number."""
    with pytest.raises(TypeError) as cm:
        AmountMixinFooMixedInClass(amount="some string")

    assert str(cm.value) == (
        "AmountMixinFooMixedInClass.amount should be a number, not str: 'some string'"
    )


def test_amount_attribute_is_not_a_number():
    """TypeError will be raised if amount attribute is not a number."""
    entry = AmountMixinFooMixedInClass(amount=10)
    with pytest.raises(TypeError) as cm:
        entry.amount = "some string"

    assert str(cm.value) == (
        "AmountMixinFooMixedInClass.amount should be a number, not str: 'some string'"
    )


def test_amount_argument_is_working_properly():
    """amount argument value is correctly passed to the amount attribute."""
    entry = AmountMixinFooMixedInClass(amount=10)
    assert entry.amount == 10.0


def test_amount_attribute_is_working_properly():
    """amount attribute is working properly."""
    entry = AmountMixinFooMixedInClass(amount=10)
    test_value = 5.0
    assert entry.amount != test_value
    entry.amount = test_value
    assert entry.amount == test_value
