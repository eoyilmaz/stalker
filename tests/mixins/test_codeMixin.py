# -*- coding: utf-8 -*-

import unittest
import pytest
from sqlalchemy import Column, Integer, ForeignKey
from stalker import CodeMixin, SimpleEntity


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

    def test_code_argument_is_skipped(self):
        """testing if a TypeError will be raised when the code argument is
        skipped
        """
        self.kwargs.pop('code')
        with pytest.raises(TypeError) as cm:
            CodeMixFooMixedInClass(**self.kwargs)

        assert str(cm.value) == 'CodeMixFooMixedInClass.code cannot be None'

    def test_code_argument_is_None(self):
        """testing if a TypeError will be raised when the code argument is None
        """
        self.kwargs['code'] = None
        with pytest.raises(TypeError) as cm:
            CodeMixFooMixedInClass(**self.kwargs)

        assert str(cm.value) == 'CodeMixFooMixedInClass.code cannot be None'

    def test_code_attribute_is_None(self):
        """testing if a TypeError will be raised when teh code attribute is set
        to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_foo_obj.code = None

        assert str(cm.value) == 'CodeMixFooMixedInClass.code cannot be None'

    def test_code_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the code argument is not
        a string
        """
        self.kwargs['code'] = 123
        with pytest.raises(TypeError) as cm:
            CodeMixFooMixedInClass(**self.kwargs)

        assert str(cm.value) == \
            'CodeMixFooMixedInClass.code should be a string not int'

    def test_code_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the code attribute is set
        to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_foo_obj.code = 2342

        assert str(cm.value) == \
            'CodeMixFooMixedInClass.code should be a string not int'

    def test_code_argument_is_an_empty_string(self):
        """testing if a ValueError will be raised when the code attribute is an
        empty string
        """
        self.kwargs['code'] = ''
        with pytest.raises(ValueError) as cm:
            CodeMixFooMixedInClass(**self.kwargs)

        assert str(cm.value) == \
            'CodeMixFooMixedInClass.code can not be an empty string'

    def test_code_attribute_is_set_to_an_empty_string(self):
        """testing if a ValueError will be raised when the code attribute is
        set to an empty string
        """
        with pytest.raises(ValueError) as cm:
            self.test_foo_obj.code = ''

        assert str(cm.value) == \
            'CodeMixFooMixedInClass.code can not be an empty string'

    def test_code_argument_is_working_properly(self):
        """testing if the code argument value is passed to the code attribute
        properly
        """
        assert self.test_foo_obj.code == self.kwargs['code']

    def test_code_attribute_is_working_properly(self):
        """testing if the code attribute is working properly
        """
        test_value = 'new code'
        self.test_foo_obj.code = test_value
        assert self.test_foo_obj.code == test_value
