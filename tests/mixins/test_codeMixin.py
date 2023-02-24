# -*- coding: utf-8 -*-
"""CodeMixin related tests."""
import pytest

from sqlalchemy import Column, ForeignKey, Integer

from stalker import CodeMixin, SimpleEntity


class CodeMixFooMixedInClass(SimpleEntity, CodeMixin):
    """A class which derives from another which has and __init__ already."""

    __tablename__ = "CodeMixFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "CodeMixFooMixedInClass"}
    codeMixFooMixedInClass_id = Column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(CodeMixFooMixedInClass, self).__init__(**kwargs)
        CodeMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def code_mixin_tester_setup():
    """Set up the test.

    Returns:
        dict: Test data.
    """
    data = {
        "kwargs": {
            "name": "Test Code Mixin",
            "code": "this_is_a_test_code",
            "description": "This is a simple entity object for testing "
            "DateRangeMixin",
        },
    }
    data["test_foo_obj"] = CodeMixFooMixedInClass(**data["kwargs"])
    return data


def test_code_argument_is_skipped(code_mixin_tester_setup):
    """TypeError is raised if the code argument is skipped."""
    data = code_mixin_tester_setup
    data["kwargs"].pop("code")
    with pytest.raises(TypeError) as cm:
        CodeMixFooMixedInClass(**data["kwargs"])

    assert str(cm.value) == "CodeMixFooMixedInClass.code cannot be None"


def test_code_argument_is_none(code_mixin_tester_setup):
    """TypeError is raised if the code argument is None."""
    data = code_mixin_tester_setup
    data["kwargs"]["code"] = None
    with pytest.raises(TypeError) as cm:
        CodeMixFooMixedInClass(**data["kwargs"])

    assert str(cm.value) == "CodeMixFooMixedInClass.code cannot be None"


def test_code_attribute_is_none(code_mixin_tester_setup):
    """TypeError is raised if teh code attribute is set to None."""
    data = code_mixin_tester_setup
    with pytest.raises(TypeError) as cm:
        data["test_foo_obj"].code = None

    assert str(cm.value) == "CodeMixFooMixedInClass.code cannot be None"


def test_code_argument_is_not_a_string(code_mixin_tester_setup):
    """TypeError is raised if the code argument is not a string."""
    data = code_mixin_tester_setup
    data["kwargs"]["code"] = 123
    with pytest.raises(TypeError) as cm:
        CodeMixFooMixedInClass(**data["kwargs"])

    assert str(cm.value) == "CodeMixFooMixedInClass.code should be a string not int"


def test_code_attribute_is_not_a_string(code_mixin_tester_setup):
    """TypeError is raised if the code attribute is set to None."""
    data = code_mixin_tester_setup
    with pytest.raises(TypeError) as cm:
        data["test_foo_obj"].code = 2342

    assert str(cm.value) == "CodeMixFooMixedInClass.code should be a string not int"


def test_code_argument_is_an_empty_string(code_mixin_tester_setup):
    """ValueError is raised if the code attribute is an empty string."""
    data = code_mixin_tester_setup
    data["kwargs"]["code"] = ""
    with pytest.raises(ValueError) as cm:
        CodeMixFooMixedInClass(**data["kwargs"])

    assert str(cm.value) == "CodeMixFooMixedInClass.code can not be an empty string"


def test_code_attribute_is_set_to_an_empty_string(code_mixin_tester_setup):
    """ValueError is raised if the code attribute is set to an empty string."""
    data = code_mixin_tester_setup
    with pytest.raises(ValueError) as cm:
        data["test_foo_obj"].code = ""

    assert str(cm.value) == "CodeMixFooMixedInClass.code can not be an empty string"


def test_code_argument_is_working_properly(code_mixin_tester_setup):
    """code argument value is passed to the code attribute properly."""
    data = code_mixin_tester_setup
    assert data["test_foo_obj"].code == data["kwargs"]["code"]


def test_code_attribute_is_working_properly(code_mixin_tester_setup):
    """code attribute is working properly."""
    data = code_mixin_tester_setup
    test_value = "new code"
    data["test_foo_obj"].code = test_value
    assert data["test_foo_obj"].code == test_value
