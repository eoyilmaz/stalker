# -*- coding: utf-8 -*-
"""Tests for the stalker.models.template.FilenameTemplate class."""

import sys
import pytest

from stalker import (
    Entity,
    FilenameTemplate,
    Project,
    Sequence,
    Shot,
    Structure,
    Task,
    Type,
    Version,
)
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_filename_template_tests():
    """Set up tests for the FilenameTemplate class."""
    data = dict()
    data["kwargs"] = {
        "name": "Test FilenameTemplate",
        "type": Type(
            name="Test Type", code="tt", target_entity_type="FilenameTemplate"
        ),
        "path": "ASSETS/{{asset.code}}/{{task.type.code}}/",
        "filename": "{{asset.code}}_{{version.variant_name}}_{{task.type.code}}_"
        "{{version.version}}_{{user.initials}}",
        "output_path": "",
        "target_entity_type": "Asset",
    }
    data["filename_template"] = FilenameTemplate(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Asset class."""
    assert FilenameTemplate.__auto_name__ is False


def test_filename_template_is_not_strictly_typed(setup_filename_template_tests):
    """FilenameTemplate class is not strictly typed."""
    data = setup_filename_template_tests
    data["kwargs"].pop("type")
    # no errors
    ft = FilenameTemplate(**data["kwargs"])
    assert isinstance(ft, FilenameTemplate)


def test_target_entity_type_argument_is_skipped(setup_filename_template_tests):
    """TypeError is raised if the target_entity_type argument is skipped."""
    data = setup_filename_template_tests
    data["kwargs"].pop("target_entity_type")
    with pytest.raises(TypeError) as cm:
        FilenameTemplate(**data["kwargs"])

    assert str(cm.value) == "FilenameTemplate.target_entity_type cannot be None"


def test_target_entity_type_argument_is_none(setup_filename_template_tests):
    """TypeError is raised if the target_entity_type argument is given as None."""
    data = setup_filename_template_tests
    data["kwargs"]["target_entity_type"] = None
    with pytest.raises(TypeError) as cm:
        FilenameTemplate(**data["kwargs"])

    assert str(cm.value) == "FilenameTemplate.target_entity_type cannot be None"


def test_target_entity_type_attribute_is_read_only(setup_filename_template_tests):
    """AttributeError is raised if the target_entity_type attribute is set."""
    data = setup_filename_template_tests
    with pytest.raises(AttributeError) as cm:
        data["filename_template"].target_entity_type = "Asset"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute",
        11: "property of 'FilenameTemplate' object has no setter",
        12: "property of 'FilenameTemplate' object has no setter",
    }.get(
        sys.version_info.minor,
        "property '_target_entity_type_getter' of 'FilenameTemplate' "
        "object has no setter"
    )

    assert str(cm.value) == error_message


def test_target_entity_type_argument_accepts_classes(setup_filename_template_tests):
    """target_entity_type can be set to a class directly."""
    data = setup_filename_template_tests
    data["kwargs"]["target_entity_type"] = "Asset"
    _ = FilenameTemplate(**data["kwargs"])


def test_target_entity_type_attribute_is_converted_to_a_string_if_given_as_a_class(
    setup_filename_template_tests,
):
    """target_entity_type attr is converted if the target_entity_type is a class."""
    data = setup_filename_template_tests
    data["kwargs"]["target_entity_type"] = "Asset"
    ft = FilenameTemplate(**data["kwargs"])
    assert ft.target_entity_type == "Asset"


def test_path_argument_is_skipped(setup_filename_template_tests):
    """Nothing happens if the path argument is skipped."""
    data = setup_filename_template_tests
    data["kwargs"].pop("path")
    ft = FilenameTemplate(**data["kwargs"])
    assert isinstance(ft, FilenameTemplate)


def test_path_argument_skipped_path_attribute_is_empty_string(
    setup_filename_template_tests,
):
    """path attribute is an empty string if the path argument is skipped."""
    data = setup_filename_template_tests
    data["kwargs"].pop("path")
    ft = FilenameTemplate(**data["kwargs"])
    assert ft.path == ""


def test_path_argument_is_none_path_attribute_is_empty_string(
    setup_filename_template_tests,
):
    """path attribute is an empty string if the path argument is None."""
    data = setup_filename_template_tests
    data["kwargs"]["path"] = None
    ft = FilenameTemplate(**data["kwargs"])
    assert ft.path == ""


def test_path_argument_is_empty_string(setup_filename_template_tests):
    """Nothing happens if the path argument is empty string."""
    data = setup_filename_template_tests
    data["kwargs"]["path"] = ""
    ft = FilenameTemplate(**data["kwargs"])
    assert isinstance(ft, FilenameTemplate)


def test_path_attribute_is_empty_string(setup_filename_template_tests):
    """Nothing happens if the path attribute is set to empty string."""
    data = setup_filename_template_tests
    data["filename_template"].path = ""


def test_path_argument_is_not_string(setup_filename_template_tests):
    """TypeError is raised if the path argument is not a string."""
    data = setup_filename_template_tests
    test_value = list("a list from a string")
    data["kwargs"]["path"] = test_value
    with pytest.raises(TypeError) as cm:
        FilenameTemplate(**data["kwargs"])

    assert str(cm.value) == (
        "FilenameTemplate.path attribute should be string, not list: '['a', ' ', 'l', "
        "'i', 's', 't', ' ', 'f', 'r', 'o', 'm', ' ', 'a', ' ', 's', 't', 'r', 'i', "
        "'n', 'g']'"
    )


def test_path_attribute_is_not_string(setup_filename_template_tests):
    """TypeError is raised if the path attribute is not set to a string."""
    data = setup_filename_template_tests
    test_value = list("a list from a string")
    with pytest.raises(TypeError) as cm:
        data["filename_template"].path = test_value

    assert str(cm.value) == (
        "FilenameTemplate.path attribute should be string, not list: '['a', ' ', 'l', "
        "'i', 's', 't', ' ', 'f', 'r', 'o', 'm', ' ', 'a', ' ', 's', 't', 'r', 'i', "
        "'n', 'g']'"
    )


def test_filename_argument_is_skipped(setup_filename_template_tests):
    """Nothing happens if the filename argument is skipped."""
    data = setup_filename_template_tests
    data["kwargs"].pop("filename")
    ft = FilenameTemplate(**data["kwargs"])
    assert isinstance(ft, FilenameTemplate)


def test_filename_argument_skipped_filename_attribute_is_empty_string(
    setup_filename_template_tests,
):
    """filename attribute is an empty string if the filename argument is skipped."""
    data = setup_filename_template_tests
    data["kwargs"].pop("filename")
    ft = FilenameTemplate(**data["kwargs"])
    assert ft.filename == ""


def test_filename_argument_is_none_filename_attribute_is_empty_string(
    setup_filename_template_tests,
):
    """filename attribute is an empty string if the filename argument is None."""
    data = setup_filename_template_tests
    data["kwargs"]["filename"] = None
    ft = FilenameTemplate(**data["kwargs"])
    assert ft.filename == ""


def test_filename_argument_is_empty_string(setup_filename_template_tests):
    """Nothing happens if the filename argument is empty string."""
    data = setup_filename_template_tests
    data["kwargs"]["filename"] = ""
    ft = FilenameTemplate(**data["kwargs"])
    assert isinstance(ft, FilenameTemplate)


def test_filename_attribute_is_empty_string(setup_filename_template_tests):
    """Nothing happens if the filename attribute is set to empty string."""
    data = setup_filename_template_tests
    data["filename_template"].filename = ""


def test_filename_argument_is_not_string(setup_filename_template_tests):
    """TypeError is raised if filename argument is not string."""
    data = setup_filename_template_tests
    test_value = list("a list from a string")
    data["kwargs"]["filename"] = test_value
    with pytest.raises(TypeError) as cm:
        FilenameTemplate(**data["kwargs"])

    assert str(cm.value) == (
        "FilenameTemplate.filename attribute should be string, not list: '['a', ' ', "
        "'l', 'i', 's', 't', ' ', 'f', 'r', 'o', 'm', ' ', 'a', ' ', 's', 't', 'r', "
        "'i', 'n', 'g']'"
    )


def test_filename_attribute_is_not_string(setup_filename_template_tests):
    """Given value converted to string for the filename attribute."""
    data = setup_filename_template_tests
    test_value = list("a list from a string")
    with pytest.raises(TypeError) as cm:
        data["filename_template"].filename = test_value

    assert str(cm.value) == (
        "FilenameTemplate.filename attribute should be string, not list: "
        "'['a', ' ', 'l', 'i', 's', 't', ' ', 'f', 'r', 'o', 'm', ' ', 'a', ' ', "
        "'s', 't', 'r', 'i', 'n', 'g']'"
    )


def test_equality(setup_filename_template_tests):
    """Equality of FilenameTemplate objects."""
    data = setup_filename_template_tests
    ft1 = FilenameTemplate(**data["kwargs"])

    new_entity = Entity(**data["kwargs"])

    data["kwargs"]["target_entity_type"] = "Entity"
    ft2 = FilenameTemplate(**data["kwargs"])

    data["kwargs"]["path"] = "different path"
    ft3 = FilenameTemplate(**data["kwargs"])

    data["kwargs"]["filename"] = "different filename"
    ft4 = FilenameTemplate(**data["kwargs"])

    assert data["filename_template"] == ft1
    assert not data["filename_template"] == new_entity
    assert not ft1 == ft2
    assert not ft2 == ft3
    assert not ft3 == ft4


def test_inequality(setup_filename_template_tests):
    """Inequality of FilenameTemplate objects."""
    data = setup_filename_template_tests
    ft1 = FilenameTemplate(**data["kwargs"])

    new_entity = Entity(**data["kwargs"])

    data["kwargs"]["target_entity_type"] = "Entity"
    ft2 = FilenameTemplate(**data["kwargs"])

    data["kwargs"]["path"] = "different path"
    ft3 = FilenameTemplate(**data["kwargs"])

    data["kwargs"]["filename"] = "different filename"
    ft4 = FilenameTemplate(**data["kwargs"])

    assert not data["filename_template"] != ft1
    assert data["filename_template"] != new_entity
    assert ft1 != ft2
    assert ft2 != ft3
    assert ft3 != ft4


def test_naming_case(setup_postgresql_db):
    """Naming should contain both Sequence Shot and other stuff.

    (this is based on https://github.com/eoyilmaz/anima/issues/23)
    """
    ft = FilenameTemplate(
        name="Normal Naming Convention",
        target_entity_type="Task",
        path="$REPO{{project.repository.id}}/{{project.code}}/{%- for parent_task in "
        "parent_tasks -%}{{parent_task.nice_name}}/{%- endfor -%}",
        filename="""{%- for p in parent_tasks -%}
            {%- if p.entity_type == 'Sequence' -%}
                {{p.name}}
            {%- elif p.entity_type == 'Shot' -%}
                _{{p.name}}{{p.children[0].name}}
            {%- endif -%}
        {%- endfor -%}
        {%- set fx = parent_tasks[-2] -%}
        _{{fx.name}}_{{version.variant_name}}_v{{"%02d"|format(version.version_number)}}""",
    )
    DBSession.add(ft)

    st = Structure(name="Normal Project Structure", templates=[ft])
    DBSession.add(st)

    test_project = Project(name="test001", code="test001", structure=st)
    DBSession.add(test_project)
    DBSession.commit()

    seq_task = Task(name="seq", project=test_project)
    DBSession.add(seq_task)

    ep101 = Sequence(name="ep101", code="ep101", parent=seq_task)
    DBSession.add(ep101)

    shot_task = Task(name="shot", parent=ep101)
    DBSession.add(shot_task)

    s001 = Shot(name="s001", code="s001", parent=shot_task)
    DBSession.add(s001)

    c001 = Task(name="c001", parent=s001)
    DBSession.add(c001)

    effects_scene = Task(name="effectScenes", parent=c001)
    DBSession.add(effects_scene)

    fxA = Task(name="fxA", parent=effects_scene)
    DBSession.add(fxA)

    maya = Task(name="maya", parent=fxA)
    DBSession.add(maya)
    DBSession.commit()

    v = Version(task=maya)
    v.update_paths()
    v.extension = ".ma"
    DBSession.add(v)
    DBSession.commit()

    assert v.filename == "ep101_s001c001_fxA_Main_v01.ma"
