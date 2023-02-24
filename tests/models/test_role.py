# -*- coding: utf-8 -*-
"""Tests for the Role class."""

from stalker import Role


def test_role_class_generic():
    """creation of a Role instance."""
    r = Role(name="Lead")
    assert isinstance(r, Role)
    assert r.name == "Lead"
