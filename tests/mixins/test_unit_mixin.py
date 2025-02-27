# -*- coding: utf-8 -*-
"""UnitMixin class related tests."""

import pytest

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from stalker import SimpleEntity, UnitMixin


class UnitMixinFooMixedInClass(SimpleEntity, UnitMixin):
    """A class which derives from another which has and __init__ already."""

    __tablename__ = "UnitMixinFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "UnitMixinFooMixedInClass"}
    unitMixinFooMixedInClass_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )
    __id_column__ = "unitMixinFooMixedInClass_id"

    def __init__(self, **kwargs):
        super(UnitMixinFooMixedInClass, self).__init__(**kwargs)
        UnitMixin.__init__(self, **kwargs)


def test_mixed_in_class_initialization():
    """init is working as expected."""
    a = UnitMixinFooMixedInClass(unit="TRY")
    assert isinstance(a, UnitMixinFooMixedInClass)
    assert a.unit == "TRY"


def test_unit_argument_is_skipped():
    """unit attribute is an empty string if the unit argument is skipped."""
    g = UnitMixinFooMixedInClass()
    assert g.unit == ""


def test_unit_argument_is_none():
    """unit attribute will be an empty string if the unit argument is None."""
    g = UnitMixinFooMixedInClass(unit=None)
    assert g.unit == ""


def test_unit_attribute_is_set_to_none():
    """unit attribute will be an empty string if it is set to None."""
    g = UnitMixinFooMixedInClass(unit="TRY")
    assert g.unit != ""
    g.unit = None
    assert g.unit == ""


def test_unit_argument_is_not_a_string():
    """TypeError is raised if the unit argument is not a str."""
    with pytest.raises(TypeError) as cm:
        UnitMixinFooMixedInClass(unit=1234)

    assert str(cm.value) == (
        "UnitMixinFooMixedInClass.unit should be a string, not int: '1234'"
    )


def test_unit_attribute_is_not_a_string():
    """TypeError is raised if the unit attribute is set to non-str."""
    g = UnitMixinFooMixedInClass(unit="TRY")
    with pytest.raises(TypeError) as cm:
        g.unit = 2342

    assert str(cm.value) == (
        "UnitMixinFooMixedInClass.unit should be a string, not int: '2342'"
    )


def test_unit_argument_is_working_as_expected():
    """unit arg value is passed to the unit attribute."""
    test_value = "this is my unit"
    g = UnitMixinFooMixedInClass(unit=test_value)
    assert g.unit == test_value


def test_unit_attribute_is_working_as_expected():
    """unit attribute value can be changed."""
    test_value = "this is my unit"
    g = UnitMixinFooMixedInClass(unit="TRY")
    assert g.unit != test_value
    g.unit = test_value
    assert g.unit == test_value
