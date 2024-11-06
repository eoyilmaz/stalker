# -*- coding: utf-8 -*-
"""Tests for the Structure class."""

import pytest

from stalker import FilenameTemplate, Structure, Type


@pytest.fixture(scope="function")
def setup_structure_tests():
    """stalker.models.structure.Structure class."""
    data = dict()
    vers_type = Type(name="Version", code="vers", target_entity_type="FilenameTemplate")
    ref_type = Type(name="Reference", code="ref", target_entity_type="FilenameTemplate")
    # type templates
    data["asset_template"] = FilenameTemplate(
        name="Test Asset Template", target_entity_type="Asset", type=vers_type
    )
    data["shot_template"] = FilenameTemplate(
        name="Test Shot Template", target_entity_type="Shot", type=vers_type
    )
    data["reference_template"] = FilenameTemplate(
        name="Test Reference Template", target_entity_type="Link", type=ref_type
    )
    data["test_templates"] = [
        data["asset_template"],
        data["shot_template"],
        data["reference_template"],
    ]
    data["test_templates2"] = [data["asset_template"]]
    data["custom_template"] = "a custom template"
    data["test_type"] = Type(
        name="Commercial Structure",
        code="comm",
        target_entity_type="Structure",
    )
    # keyword arguments
    data["kwargs"] = {
        "name": "Test Structure",
        "description": "This is a test structure",
        "templates": data["test_templates"],
        "custom_template": data["custom_template"],
        "type": data["test_type"],
    }
    data["test_structure"] = Structure(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Structure class."""
    assert Structure.__auto_name__ is False


def test_custom_template_argument_can_be_skipped(setup_structure_tests):
    """custom_template argument can be skipped."""
    data = setup_structure_tests
    data["kwargs"].pop("custom_template")
    new_structure = Structure(**data["kwargs"])
    assert new_structure.custom_template == ""


def test_custom_template_argument_is_none(setup_structure_tests):
    """no error raised if the custom_template argument is None."""
    data = setup_structure_tests
    data["kwargs"]["custom_template"] = None
    new_structure = Structure(**data["kwargs"])
    assert new_structure.custom_template == ""


def test_custom_template_argument_is_empty_string(setup_structure_tests):
    """no error raised if the custom_template argument is an empty string."""
    data = setup_structure_tests
    data["kwargs"]["custom_template"] = ""
    new_structure = Structure(**data["kwargs"])
    assert new_structure.custom_template == ""


def test_custom_template_argument_is_not_a_string(setup_structure_tests):
    """TypeError raised if the custom_template argument is not a string."""
    data = setup_structure_tests
    data["kwargs"]["custom_template"] = ["this is not a string"]
    with pytest.raises(TypeError) as cm:
        Structure(**data["kwargs"])

    assert str(cm.value) == (
        "Structure.custom_template should be a string, "
        "not list: '['this is not a string']'"
    )


def test_custom_template_attribute_is_not_a_string(setup_structure_tests):
    """TypeError raised if the custom_template attribute is not a string."""
    data = setup_structure_tests
    with pytest.raises(TypeError) as cm:
        data["test_structure"].custom_template = ["this is not a string"]
    assert str(cm.value) == (
        "Structure.custom_template should be a string, "
        "not list: '['this is not a string']'"
    )


def test_templates_argument_can_be_skipped(setup_structure_tests):
    """no error raised if the templates argument is skipped."""
    data = setup_structure_tests
    data["kwargs"].pop("templates")
    new_structure = Structure(**data["kwargs"])
    assert isinstance(new_structure, Structure)


def test_templates_argument_can_be_none(setup_structure_tests):
    """no error raised if the templates argument is None."""
    data = setup_structure_tests
    data["kwargs"]["templates"] = None
    new_structure = Structure(**data["kwargs"])
    assert isinstance(new_structure, Structure)


def test_templates_attribute_cannot_be_set_to_none(setup_structure_tests):
    """TypeError raised if the templates attribute is set to None."""
    data = setup_structure_tests
    with pytest.raises(TypeError) as cm:
        data["test_structure"].templates = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_templates_argument_only_accepts_list(setup_structure_tests):
    """TypeError raised if the given templates argument is not a list."""
    data = setup_structure_tests
    data["kwargs"]["templates"] = 1
    with pytest.raises(TypeError) as cm:
        Structure(**data["kwargs"])
    assert str(cm.value) == "Incompatible collection type: int is not list-like"


def test_templates_attribute_only_accepts_list_1(setup_structure_tests):
    """TypeError raised if the templates attr is set to none list."""
    data = setup_structure_tests
    with pytest.raises(TypeError) as cm:
        data["test_structure"].templates = 1.121
    assert str(cm.value) == "Incompatible collection type: float is not list-like"


def test_templates_attribute_is_working_as_expected(setup_structure_tests):
    """templates attribute is working as expected."""
    data = setup_structure_tests
    # test the correct value
    data["test_structure"].templates = data["test_templates"]
    assert data["test_structure"].templates == data["test_templates"]


def test_templates_argument_accepts_only_list_of_filename_template_instances(
    setup_structure_tests,
):
    """TypeError raised if the templates arg is a list of none FilenameTemplate."""
    data = setup_structure_tests
    test_value = [1, 1.2, "a string"]
    data["kwargs"]["templates"] = test_value
    with pytest.raises(TypeError) as cm:
        Structure(**data["kwargs"])
    assert str(cm.value) == (
        "All the elements in the Structure.templates should be a "
        "stalker.models.template.FilenameTemplate instance, not int: '1'"
    )


def test_templates_argument_is_working_as_expected(setup_structure_tests):
    """templates argument value is correctly passed to the templates attribute."""
    data = setup_structure_tests
    # test the correct value
    data["kwargs"]["templates"] = data["test_templates"]
    new_structure = Structure(**data["kwargs"])
    assert new_structure.templates == data["test_templates"]


def test_templates_attribute_accpets_only_list_of_filename_template_instances(
    setup_structure_tests,
):
    """TypeError raised if the templates attr is a list of none FilenameTemplate."""
    data = setup_structure_tests
    test_value = [1, 1.2, "a string"]
    with pytest.raises(TypeError) as cm:
        data["test_structure"].templates = test_value

    assert str(cm.value) == (
        "All the elements in the Structure.templates should be a "
        "stalker.models.template.FilenameTemplate instance, not int: '1'"
    )


def test___strictly_typed___is_false():
    """__strictly_typed__ is False."""
    assert Structure.__strictly_typed__ is False


def test_equality_operator(setup_structure_tests):
    """equality of two Structure objects."""
    data = setup_structure_tests
    new_structure2 = Structure(**data["kwargs"])
    data["kwargs"]["custom_template"] = "a test custom template"
    new_structure3 = Structure(**data["kwargs"])
    data["kwargs"]["custom_template"] = data["test_structure"].custom_template
    data["kwargs"]["templates"] = data["test_templates2"]
    new_structure4 = Structure(**data["kwargs"])
    assert data["test_structure"] == new_structure2
    assert not data["test_structure"] == new_structure3
    assert not data["test_structure"] == new_structure4


def test_inequality_operator(setup_structure_tests):
    """inequality of two Structure objects."""
    data = setup_structure_tests
    new_structure2 = Structure(**data["kwargs"])
    data["kwargs"]["custom_template"] = "a test custom template"
    new_structure3 = Structure(**data["kwargs"])
    data["kwargs"]["custom_template"] = data["test_structure"].custom_template
    data["kwargs"]["templates"] = data["test_templates2"]
    new_structure4 = Structure(**data["kwargs"])
    assert not data["test_structure"] != new_structure2
    assert data["test_structure"] != new_structure3
    assert data["test_structure"] != new_structure4


def test_plural_class_name(setup_structure_tests):
    """plural name of Structure class."""
    data = setup_structure_tests
    assert data["test_structure"].plural_class_name == "Structures"
