# -*- coding: utf-8 -*-

import pytest


def test_role_argument_is_not_a_role_instance():
    """testing if a TypeError will be raised when the role argument is not
    a Role instance
    """
    from stalker import DepartmentUser
    from stalker import Department, User

    with pytest.raises(TypeError) as cm:
        DepartmentUser(
            department=Department(name='Test Department'),
            user=User(
                name='Test User',
                login='tuser',
                email='u@u.com',
                password='secret'
            ),
            role='not a role instance'
        )

    assert str(cm.value) == \
        'DepartmentUser.role should be a stalker.models.auth.Role ' \
        'instance, not str'
