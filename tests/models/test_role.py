# -*- coding: utf-8 -*-


def test_role_class_generic():
    """testing of creation of a Role instance
    """
    from stalker import Role
    r = Role(name='Lead')
    assert isinstance(r, Role)
    assert r.name == 'Lead'
