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

import unittest

from sqlalchemy import Column, Integer, ForeignKey

from stalker import db
from stalker.models.mixins import CodeMixin
from stalker.db.session import DBSession
from stalker.models.entity import SimpleEntity


class CodeMixFooMixedInClass(SimpleEntity, CodeMixin):
    """a class which derives from another which has and __init__ already
    """
    __tablename__ = "CodeMixFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "CodeMixFooMixedInClass"}
    codeMixFooMixedInClass_id = Column(
        "id", Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )

    def __init__(self, **kwargs):
        super(CodeMixFooMixedInClass, self).__init__(**kwargs)
        CodeMixin.__init__(self, **kwargs)


class CodeMixinTester(unittest.TestCase):
    """Tests the CodeMixin
    """

    def setUp(self):
        """setup the test
        """
        self.kwargs = {
            'name': 'Test Code Mixin',
            'code': 'this_is_a_test_code',
            'description': 'This is a simple entity object for testing '
                           'DateRangeMixin',
        }

        self.test_foo_obj = CodeMixFooMixedInClass(**self.kwargs)

    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()

    def test_code_argument_is_skipped(self):
        """testing if a TypeError will be raised when the code argument is
        skipped
        """
        self.kwargs.pop('code')
        self.assertRaises(TypeError, CodeMixFooMixedInClass, **self.kwargs)

    def test_code_argument_is_None(self):
        """testing if a TypeError will be raised when the code argument is None
        """
        self.kwargs['code'] = None
        self.assertRaises(TypeError, CodeMixFooMixedInClass, **self.kwargs)

    def test_code_attribute_is_None(self):
        """testing if a TypeError will be raised when teh code attribute is set
        to None
        """
        self.assertRaises(TypeError, setattr, self.test_foo_obj, 'code', None)

    def test_code_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the code argument is not
        a string
        """
        self.kwargs['code'] = 123
        self.assertRaises(TypeError, CodeMixFooMixedInClass, **self.kwargs)

    def test_code_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the code attribute is set
        to None
        """
        self.assertRaises(TypeError, setattr, self.test_foo_obj, 'code', 2342)

    def test_code_argument_is_an_empty_string(self):
        """testing if a ValueError will be raised when the code attribute is an
        empty string
        """
        self.kwargs['code'] = ''
        self.assertRaises(ValueError, CodeMixFooMixedInClass, **self.kwargs)

    def test_code_attribute_is_set_to_an_empty_string(self):
        """testing if a ValueError will be raised when the code attribute is
        set to an empty string
        """
        self.assertRaises(ValueError, setattr, self.test_foo_obj, 'code', '')

    def test_code_argument_is_working_properly(self):
        """testing if the code argument value is passed to the code attribute
        properly
        """
        self.assertEqual(self.test_foo_obj.code, self.kwargs['code'])

    def test_code_attribute_is_working_properly(self):
        """testing if the code attribute is working properly
        """
        test_value = 'new code'
        self.test_foo_obj.code = test_value
        self.assertEqual(self.test_foo_obj.code, test_value)
