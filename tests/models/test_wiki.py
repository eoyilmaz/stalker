# -*- coding: utf-8 -*-
"""Tests related to the Wiki class."""

import pytest

from stalker import Page, Project, Repository, Status, StatusList, Type


@pytest.fixture(scope="function")
def setup_page_tests():
    """Set up tests for the Page class."""
    data = dict()
    # create a repository
    data["repository_type"] = Type(
        name="Test Repository Type", code="test_repo", target_entity_type="Repository"
    )

    data["test_repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["repository_type"],
    )

    # statuses
    data["status1"] = Status(name="Status1", code="STS1")
    data["status2"] = Status(name="Status2", code="STS2")
    data["status3"] = Status(name="Status3", code="STS3")

    # project status list
    data["project_status_list"] = StatusList(
        name="Project Status List",
        statuses=[
            data["status1"],
            data["status2"],
            data["status3"],
        ],
        target_entity_type="Project",
    )

    # project type
    data["test_project_type"] = Type(
        name="Test Project Type",
        code="testproj",
        target_entity_type="Project",
    )

    # create projects
    data["test_project1"] = Project(
        name="Test Project 1",
        code="tp1",
        type=data["test_project_type"],
        status_list=data["project_status_list"],
        repository=data["test_repository"],
    )

    data["kwargs"] = {
        "title": "Test Page Title",
        "content": "Test content",
        "project": data["test_project1"],
    }

    data["test_page"] = Page(**data["kwargs"])
    return data


def test_title_argument_is_skipped(setup_page_tests):
    """ValueError is raised if the title argument is skipped."""
    data = setup_page_tests
    data["kwargs"].pop("title")
    with pytest.raises(ValueError) as cm:
        Page(**data["kwargs"])
    assert str(cm.value) == "Page.title cannot be empty"


def test_title_argument_is_none(setup_page_tests):
    """TypeError is raised if the title argument is None."""
    data = setup_page_tests
    data["kwargs"]["title"] = None
    with pytest.raises(TypeError) as cm:
        Page(**data["kwargs"])
    assert str(cm.value) == "Page.title should be a string, not NoneType: 'None'"


def test_title_attribute_is_set_to_none(setup_page_tests):
    """TypeError is raised if the title attribute is set to None."""
    data = setup_page_tests
    with pytest.raises(TypeError) as cm:
        data["test_page"].title = None
    assert str(cm.value) == "Page.title should be a string, not NoneType: 'None'"


def test_title_argument_is_an_empty_string(setup_page_tests):
    """ValueError is raised if the title argument is an empty string."""
    data = setup_page_tests
    data["kwargs"]["title"] = ""
    with pytest.raises(ValueError) as cm:
        Page(**data["kwargs"])
    assert str(cm.value) == "Page.title cannot be empty"


def test_title_attribute_is_set_to_empty_string(setup_page_tests):
    """ValueError is raised if the title attribute is set to empty string."""
    data = setup_page_tests
    with pytest.raises(ValueError) as cm:
        data["test_page"].title = ""
    assert str(cm.value) == "Page.title cannot be empty"


def test_title_argument_is_not_a_string(setup_page_tests):
    """TypeError is raised if the title argument is not a string."""
    data = setup_page_tests
    data["kwargs"]["title"] = 2165
    with pytest.raises(TypeError) as cm:
        Page(**data["kwargs"])
    assert str(cm.value) == "Page.title should be a string, not int: '2165'"


def test_title_attribute_is_not_a_string(setup_page_tests):
    """TypeError is raised if the title is set to a value other than a string."""
    data = setup_page_tests
    with pytest.raises(TypeError) as cm:
        data["test_page"].title = 2135
    assert str(cm.value) == "Page.title should be a string, not int: '2135'"


def test_title_argument_is_working_as_expected(setup_page_tests):
    """title argument value is correctly passed to title attribute."""
    data = setup_page_tests
    assert data["test_page"].title == data["kwargs"]["title"]


def test_title_attribute_is_working_as_expected(setup_page_tests):
    """title attribute is working as expected."""
    data = setup_page_tests
    test_value = "Test Title 2"
    data["test_page"].title = test_value
    assert data["test_page"].title == test_value


def test_content_argument_skipped(setup_page_tests):
    """content attr value is an empty str if the content argument is skipped."""
    data = setup_page_tests
    data["kwargs"].pop("content")
    new_page = Page(**data["kwargs"])
    assert new_page.content == ""


def test_content_argument_is_None(setup_page_tests):
    """content attribute value is an empty string if the content argument is None."""
    data = setup_page_tests
    data["kwargs"]["content"] = None
    new_page = Page(**data["kwargs"])
    assert new_page.content == ""


def test_content_attribute_is_set_to_None(setup_page_tests):
    """content attr value is an empty string if the content attribute is set to None."""
    data = setup_page_tests
    assert data["test_page"].content != ""
    data["test_page"].content = None
    assert data["test_page"].content == ""


def test_content_argument_is_empty_string(setup_page_tests):
    """content attr value is an empty string if the content arg is an empty string."""
    data = setup_page_tests
    data["kwargs"]["content"] = ""
    new_page = Page(**data["kwargs"])
    assert new_page.content == ""


def test_content_attribute_is_set_to_an_empty_string(setup_page_tests):
    """content attribute can be set to an empty string."""
    data = setup_page_tests
    data["test_page"].content = ""
    assert data["test_page"].content == ""


def test_content_argument_is_not_a_string(setup_page_tests):
    """TypeError is raised if the content argument is not a str."""
    data = setup_page_tests
    data["kwargs"]["content"] = 1234
    with pytest.raises(TypeError) as cm:
        Page(**data["kwargs"])
    assert str(cm.value) == "Page.content should be a string, not int: '1234'"


def test_content_attribute_is_set_to_a_value_other_than_a_string(setup_page_tests):
    """TypeError is raised if the content attr is not a str."""
    data = setup_page_tests
    with pytest.raises(TypeError) as cm:
        data["test_page"].content = ["not", "a", "string"]
    assert str(cm.value) == (
        "Page.content should be a string, not list: '['not', 'a', 'string']'"
    )


def test_content_argument_is_working_as_expected(setup_page_tests):
    """content argument value is correctly passed to the content attribute."""
    data = setup_page_tests
    assert data["test_page"].content == data["kwargs"]["content"]


def test_content_attribute_is_working_as_expected(setup_page_tests):
    """content attribute value can be correctly set."""
    data = setup_page_tests
    test_value = "This is a test content"
    assert data["test_page"].content != test_value
    data["test_page"].content = test_value
    assert data["test_page"].content == test_value
