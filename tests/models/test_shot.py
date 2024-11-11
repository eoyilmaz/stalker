# -*- coding: utf-8 -*-
"""Tests for the Shot class."""

import sys
import pytest

from stalker import (
    Asset,
    Entity,
    ImageFormat,
    Link,
    Project,
    Repository,
    Scene,
    Sequence,
    Shot,
    Status,
    StatusList,
    Task,
    Type,
)
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_shot_db_tests(setup_postgresql_db):
    """Set up the tests for the Shot class with a DB."""
    data = dict()
    data["database_settings"] = setup_postgresql_db
    # statuses
    # types
    data["test_commercial_project_type"] = Type(
        name="Commercial Project",
        code="comm",
        target_entity_type="Project",
    )
    DBSession.add(data["test_commercial_project_type"])

    data["test_character_asset_type"] = Type(
        name="Character",
        code="char",
        target_entity_type="Asset",
    )
    DBSession.add(data["test_character_asset_type"])

    data["test_repository_type"] = Type(
        name="Test Repository Type", code="test", target_entity_type="Repository"
    )
    DBSession.add(data["test_repository_type"])

    # repository
    data["test_repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["test_repository_type"],
    )
    DBSession.add(data["test_repository"])

    # image format
    data["test_image_format1"] = ImageFormat(
        name="Test Image Format 1", width=1920, height=1080, pixel_aspect=1.0
    )
    DBSession.add(data["test_image_format1"])

    data["test_image_format2"] = ImageFormat(
        name="Test Image Format 2", width=1280, height=720, pixel_aspect=1.0
    )
    DBSession.add(data["test_image_format2"])

    # project and sequences
    data["test_project1"] = Project(
        name="Test Project1",
        code="tp1",
        type=data["test_commercial_project_type"],
        repository=data["test_repository"],
        image_format=data["test_image_format1"],
    )
    DBSession.add(data["test_project1"])
    DBSession.commit()

    data["test_project2"] = Project(
        name="Test Project2",
        code="tp2",
        type=data["test_commercial_project_type"],
        repository=data["test_repository"],
        image_format=data["test_image_format1"],
    )
    DBSession.add(data["test_project2"])
    DBSession.commit()

    data["test_sequence1"] = Sequence(
        name="Test Seq1",
        code="ts1",
        project=data["test_project1"],
    )
    DBSession.add(data["test_sequence1"])
    DBSession.commit()

    data["test_sequence2"] = Sequence(
        name="Test Seq2",
        code="ts2",
        project=data["test_project1"],
    )
    DBSession.add(data["test_sequence2"])
    DBSession.commit()

    data["test_sequence3"] = Sequence(
        name="Test Seq3",
        code="ts3",
        project=data["test_project1"],
    )
    DBSession.add(data["test_sequence3"])
    DBSession.commit()

    data["test_scene1"] = Scene(
        name="Test Sce1",
        code="tsc1",
        project=data["test_project1"],
    )
    DBSession.add(data["test_scene1"])
    DBSession.commit()

    data["test_scene2"] = Scene(
        name="Test Sce2",
        code="tsc2",
        project=data["test_project1"],
    )
    DBSession.add(data["test_scene2"])
    DBSession.commit()

    data["test_scene3"] = Scene(
        name="Test Sce3", code="tsc3", project=data["test_project1"]
    )
    DBSession.add(data["test_scene3"])
    DBSession.commit()

    data["test_asset1"] = Asset(
        name="Test Asset1",
        code="ta1",
        project=data["test_project1"],
        type=data["test_character_asset_type"],
    )
    DBSession.add(data["test_asset1"])
    DBSession.commit()

    data["test_asset2"] = Asset(
        name="Test Asset2",
        code="ta2",
        project=data["test_project1"],
        type=data["test_character_asset_type"],
    )
    DBSession.add(data["test_asset2"])
    DBSession.commit()

    data["test_asset3"] = Asset(
        name="Test Asset3",
        code="ta3",
        project=data["test_project1"],
        type=data["test_character_asset_type"],
    )
    DBSession.add(data["test_asset3"])
    DBSession.commit()

    data["kwargs"] = dict(
        name="SH123",
        code="SH123",
        description="This is a test Shot",
        project=data["test_project1"],
        sequences=[data["test_sequence1"], data["test_sequence2"]],
        scenes=[data["test_scene1"], data["test_scene2"]],
        cut_in=112,
        cut_out=149,
        source_in=120,
        source_out=140,
        record_in=85485,
        status=0,
        image_format=data["test_image_format2"],
    )

    # create a mock shot object
    data["test_shot"] = Shot(**data["kwargs"])
    DBSession.add(data["test_shot"])
    DBSession.commit()
    return data


def test___auto_name__class_attribute_is_set_to_true():
    """__auto_name__ class attribute is set to True for Shot class."""
    assert Shot.__auto_name__ is True


def test___hash___value_is_correctly_calculated(setup_shot_db_tests):
    """__hash__ value is correctly calculated."""
    data = setup_shot_db_tests
    assert data["test_shot"].__hash__() == hash(
        "{}:{}:{}".format(
            data["test_shot"].id, data["test_shot"].name, data["test_shot"].entity_type
        )
    )


def test_project_argument_is_skipped(setup_shot_db_tests):
    """TypeError raised if the project argument is skipped."""
    data = setup_shot_db_tests
    data["kwargs"].pop("project")
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])

    assert (
        str(cm.value) == "Shot.project should be an instance of "
        "stalker.models.project.Project, not NoneType: 'None'.\n\nOr please supply "
        "a stalker.models.task.Task with the parent argument, so "
        "Stalker can use the project of the supplied parent task"
    )


def test_project_argument_is_None(setup_shot_db_tests):
    """TypeError raised if the project argument is None."""
    data = setup_shot_db_tests
    data["kwargs"]["project"] = None

    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])

    assert (
        str(cm.value) == "Shot.project should be an instance of "
        "stalker.models.project.Project, not NoneType: 'None'.\n\nOr please supply "
        "a stalker.models.task.Task with the parent argument, so "
        "Stalker can use the project of the supplied parent task"
    )


@pytest.mark.parametrize("test_value", [1, 1.2, "project", ["a", "project"]])
def test_project_argument_is_not_project_instance(test_value, setup_shot_db_tests):
    """TypeError raised if the given project argument is not a Project instance."""
    data = setup_shot_db_tests
    data["kwargs"]["project"] = test_value
    with pytest.raises(TypeError) as cm:
        Shot(data["kwargs"])

    assert str(cm.value) == (
        "Shot.project should be an instance of stalker.models.project.Project, not "
        "NoneType: 'None'.\n\nOr please supply a stalker.models.task.Task with the parent "
        "argument, so Stalker can use the project of the supplied parent task"
    )


def test_project_already_has_a_shot_with_the_same_code(setup_shot_db_tests):
    """ValueError raised if project argument already has a shot with the same code."""
    data = setup_shot_db_tests
    # let's try to assign the shot to the same sequence2 which has another
    # shot with the same code
    assert data["kwargs"]["code"] == data["test_shot"].code
    with pytest.raises(ValueError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == "There is a Shot with the same code: SH123"

    # this should not raise a ValueError
    data["kwargs"]["code"] = "DifferentCode"
    new_shot2 = Shot(**data["kwargs"])
    assert isinstance(new_shot2, Shot)


def test_code_attribute_is_set_to_the_same_value(setup_shot_db_tests):
    """ValueError will NOT be raised if the shot.code is set to the same value."""
    data = setup_shot_db_tests
    data["test_shot"].code = data["test_shot"].code


def test_project_attribute_is_read_only(setup_shot_db_tests):
    """project attribute is read only."""
    data = setup_shot_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_shot"].project = data["test_project2"]

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute",
        11: "property of 'Shot' object has no setter",
        12: "property of 'Shot' object has no setter",
    }.get(
        sys.version_info.minor,
        "property '_project_getter' of 'Shot' object has no setter",
    )

    assert str(cm.value) == error_message


def test_project_contains_shots(setup_shot_db_tests):
    """shot is added to the Project.shots list."""
    data = setup_shot_db_tests
    assert data["test_shot"] in data["test_shot"].project.shots


def test_project_argument_is_working_as_expected(setup_shot_db_tests):
    """project argument is working as expected."""
    data = setup_shot_db_tests
    assert data["test_shot"].project == data["kwargs"]["project"]


def test_sequences_argument_is_skipped(setup_shot_db_tests):
    """sequences attribute an empty list if the sequences argument is skipped."""
    data = setup_shot_db_tests
    data["kwargs"].pop("sequences")
    data["kwargs"]["code"] = "DifferentCode"
    new_shot = Shot(**data["kwargs"])
    assert new_shot.sequences == []


def test_sequences_argument_is_none(setup_shot_db_tests):
    """sequences attribute an empty list if the sequences argument is set to None."""
    data = setup_shot_db_tests
    data["kwargs"]["sequences"] = None
    data["kwargs"]["code"] = "NewCode"
    new_shot = Shot(**data["kwargs"])
    assert new_shot.sequences == []


def test_sequences_attribute_is_set_to_none(setup_shot_db_tests):
    """TypeError raised if the sequences attribute is set to None."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].sequences = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_sequences_argument_is_not_a_list(setup_shot_db_tests):
    """TypeError raised if the sequences argument is not a list."""
    data = setup_shot_db_tests
    data["kwargs"]["sequences"] = "not a list"
    data["kwargs"]["code"] = "NewCode"
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])
    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_sequences_attribute_is_not_a_list(setup_shot_db_tests):
    """TypeError raised if the sequences attribute is not a list."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].sequences = "not a list"

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_sequences_argument_is_not_a_list_of_Sequence_instances(setup_shot_db_tests):
    """TypeError raised if the sequences argument is not a list of Sequences."""
    data = setup_shot_db_tests
    data["kwargs"]["sequences"] = ["not", 1, "list", "of", "sequences"]
    data["kwargs"]["code"] = "NewShot"
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.sequences should all be stalker.models.sequence.Sequence instances, "
        "not str: 'not'"
    )


def test_sequences_attribute_is_not_a_list_of_Sequence_instances(setup_shot_db_tests):
    """TypeError raised if the sequences attr is not a list of Sequence instances."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].sequences = ["not", 1, "list", "of", "sequences"]

    assert str(cm.value) == (
        "Shot.sequences should all be stalker.models.sequence.Sequence instances, "
        "not str: 'not'"
    )


def test_sequences_argument_is_working_as_expected(setup_shot_db_tests):
    """sequences attribute is working as expected."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "NewShot"
    seq1 = Sequence(
        name="seq1",
        code="seq1",
        project=data["test_project1"],
    )
    seq2 = Sequence(
        name="seq2",
        code="seq2",
        project=data["test_project1"],
    )
    seq3 = Sequence(
        name="seq3",
        code="seq3",
        project=data["test_project1"],
    )

    seqs = [seq1, seq2, seq3]
    data["kwargs"]["sequences"] = seqs
    new_shot = Shot(**data["kwargs"])

    assert sorted(new_shot.sequences, key=lambda x: x.name) == sorted(
        seqs, key=lambda x: x.name
    )


def test_sequences_attribute_is_working_as_expected(setup_shot_db_tests):
    """sequences attribute is working as expected."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "NewShot"
    seq1 = Sequence(
        name="seq1",
        code="seq1",
        project=data["test_project1"],
    )
    seq2 = Sequence(
        name="seq2",
        code="seq2",
        project=data["test_project1"],
    )
    seq3 = Sequence(
        name="seq3",
        code="seq3",
        project=data["test_project1"],
    )

    new_shot = Shot(**data["kwargs"])

    new_shot.sequences = [seq1]
    new_shot.sequences.append(seq2)
    new_shot.sequences.append(seq3)

    seqs = [seq1, seq2, seq3]
    assert sorted(new_shot.sequences, key=lambda x: x.name) == sorted(
        seqs, key=lambda x: x.name
    )


def test_scenes_argument_is_skipped(setup_shot_db_tests):
    """scenes attribute an empty list if the scenes argument is skipped."""
    data = setup_shot_db_tests
    data["kwargs"].pop("scenes")
    data["kwargs"]["code"] = "DifferentCode"
    new_shot = Shot(**data["kwargs"])
    assert new_shot.scenes == []


def test_scenes_argument_is_None(setup_shot_db_tests):
    """scenes attribute an empty list if the scenes argument is set to None."""
    data = setup_shot_db_tests
    data["kwargs"]["scenes"] = None
    data["kwargs"]["code"] = "NewCode"
    new_shot = Shot(**data["kwargs"])
    assert new_shot.scenes == []


def test_scenes_attribute_is_set_to_None(setup_shot_db_tests):
    """TypeError raised if the scenes attribute is set to None."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].scenes = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_scenes_argument_is_not_a_list(setup_shot_db_tests):
    """TypeError raised if the scenes argument is not a list."""
    data = setup_shot_db_tests
    data["kwargs"]["scenes"] = "not a list"
    data["kwargs"]["code"] = "NewCode"
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_scenes_attribute_is_not_a_list(setup_shot_db_tests):
    """TypeError raised if the scenes attribute is not a list."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].scenes = "not a list"

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_scenes_argument_is_not_a_list_of_Scene_instances(setup_shot_db_tests):
    """TypeError raised if the scenes argument is not a list of Scenes."""
    data = setup_shot_db_tests
    data["kwargs"]["scenes"] = ["not", 1, "list", "of", "scenes"]
    data["kwargs"]["code"] = "NewShot"
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.scenes should all be stalker.models.scene.Scene instances, not str: 'not'"
    )


def test_scenes_attribute_is_not_a_list_of_Scene_instances(setup_shot_db_tests):
    """TypeError raised if the scenes attribute is not a list of Scene instances."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].scenes = ["not", 1, "list", "of", "scenes"]

    assert str(cm.value) == (
        "Shot.scenes should all be stalker.models.scene.Scene instances, not str: 'not'"
    )


def test_scenes_argument_is_working_as_expected(setup_shot_db_tests):
    """scenes attribute is working as expected."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "NewShot"
    sce1 = Scene(name="sce1", code="sce1", project=data["test_project1"])
    sce2 = Scene(name="sce2", code="sce2", project=data["test_project1"])
    sce3 = Scene(name="sce3", code="sce3", project=data["test_project1"])

    seqs = [sce1, sce2, sce3]
    data["kwargs"]["scenes"] = seqs
    new_shot = Shot(**data["kwargs"])

    assert sorted(new_shot.scenes, key=lambda x: x.name) == sorted(
        seqs, key=lambda x: x.name
    )


def test_scenes_attribute_is_working_as_expected(setup_shot_db_tests):
    """scenes attribute is working as expected."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "NewShot"

    sce1 = Scene(name="sce1", code="sce1", project=data["test_project1"])
    sce2 = Scene(name="sce2", code="sce2", project=data["test_project1"])
    sce3 = Scene(name="sce3", code="sce3", project=data["test_project1"])

    new_shot = Shot(**data["kwargs"])

    new_shot.scenes = [sce1]
    new_shot.scenes.append(sce2)
    new_shot.scenes.append(sce3)

    seqs = [sce1, sce2, sce3]
    assert sorted(new_shot.scenes, key=lambda x: x.name) == sorted(
        seqs, key=lambda x: x.name
    )


def test_cut_in_argument_is_skipped(setup_shot_db_tests):
    """cut_in arg skipped the cut_in arg is calculated from cut_out arg."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"].pop("cut_in")
    data["kwargs"]["source_in"] = None
    data["kwargs"]["source_out"] = None
    new_shot = Shot(**data["kwargs"])
    assert new_shot.cut_out == data["kwargs"]["cut_out"]
    assert new_shot.cut_in == new_shot.cut_out


def test_cut_in_argument_is_none(setup_shot_db_tests):
    """cut_in attr is calculated from the cut_out attr if the cut_in arg is None."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["cut_in"] = None
    data["kwargs"]["source_in"] = None
    data["kwargs"]["source_out"] = None
    shot = Shot(**data["kwargs"])
    assert shot.cut_out == data["kwargs"]["cut_out"]
    assert shot.cut_in == shot.cut_out


def test_cut_in_attribute_is_set_to_none(setup_shot_db_tests):
    """TypeError raised if the cut_in attribute is set to None."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].cut_in = None
    assert str(cm.value) == "Shot.cut_in should be an int, not NoneType: 'None'"


def test_cut_in_argument_is_not_integer(setup_shot_db_tests):
    """TypeError raised if the cut_in argument is not an instance of int."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["cut_in"] = "a string"
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])
    assert str(cm.value) == "Shot.cut_in should be an int, not str: 'a string'"


def test_cut_in_attribute_is_not_integer(setup_shot_db_tests):
    """TypeError raised if the cut_in attr not an integer."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].cut_in = "a string"
    assert str(cm.value) == "Shot.cut_in should be an int, not str: 'a string'"


def test_cut_in_argument_is_bigger_than_cut_out_argument(setup_shot_db_tests):
    """cut_out offset if the cut_in arg value is bigger than the cut_out arg value."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["cut_in"] = data["kwargs"]["cut_out"] + 10
    data["kwargs"]["source_in"] = None
    data["kwargs"]["source_out"] = None
    shot = Shot(**data["kwargs"])
    assert shot.cut_in == 149
    assert shot.cut_out == 149


def test_cut_in_attribute_is_bigger_than_cut_out_attribute(setup_shot_db_tests):
    """the cut_out attr offset if the cut_in is set bigger than cut_out."""
    data = setup_shot_db_tests
    data["test_shot"].cut_in = data["test_shot"].cut_out + 10
    assert data["test_shot"].cut_in == 159
    assert data["test_shot"].cut_out == data["test_shot"].cut_in


def test_cut_out_argument_is_skipped(setup_shot_db_tests):
    """cut_out attr calculated from cut_in arg value if the cut_out arg is skipped."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"].pop("cut_out")
    data["kwargs"]["source_in"] = None
    data["kwargs"]["source_out"] = None
    new_shot = Shot(**data["kwargs"])
    assert new_shot.cut_in == data["kwargs"]["cut_in"]
    assert new_shot.cut_out == new_shot.cut_in


def test_cut_out_argument_is_set_to_none(setup_shot_db_tests):
    """cut_out arg is set to None the cut_out attr calculated from cut_in arg value."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["cut_out"] = None
    data["kwargs"]["source_in"] = None
    data["kwargs"]["source_out"] = None

    shot = Shot(**data["kwargs"])
    assert shot.cut_in == data["kwargs"]["cut_in"]
    assert shot.cut_out == shot.cut_in


def test_cut_out_attribute_is_set_to_none(setup_shot_db_tests):
    """TypeError raised if the cut_out attribute is set to None."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].cut_out = None
    assert str(cm.value) == "Shot.cut_out should be an int, not NoneType: 'None'"


def test_cut_out_argument_is_not_integer(setup_shot_db_tests):
    """TypeError raised if the cut_out argument is not an integer."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["cut_out"] = "a string"
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])
    assert str(cm.value) == "Shot.cut_out should be an int, not str: 'a string'"


def test_cut_out_attribute_is_not_integer(setup_shot_db_tests):
    """TypeError raised if the cut_out attr is set to a value other than an integer."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].cut_out = "a string"
    assert str(cm.value) == "Shot.cut_out should be an int, not str: 'a string'"


def test_cut_out_argument_is_smaller_than_cut_in_argument(setup_shot_db_tests):
    """cut_out attr is updated if the cut_out arg is smaller than cut_in arg."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["cut_out"] = data["kwargs"]["cut_in"] - 10
    data["kwargs"]["source_in"] = None
    data["kwargs"]["source_out"] = None
    shot = Shot(**data["kwargs"])
    assert shot.cut_in == 102
    assert shot.cut_out == 102


def test_cut_out_attribute_is_smaller_than_cut_in_attribute(setup_shot_db_tests):
    """cut_out attribute is updated if it is smaller than cut_in attribute."""
    data = setup_shot_db_tests
    data["test_shot"].cut_out = data["test_shot"].cut_in - 10
    assert data["test_shot"].cut_in == 102
    assert data["test_shot"].cut_out == 102


def test_cut_duration_attribute_is_not_instance_of_int(setup_shot_db_tests):
    """TypeError raised if the cut_duration attr is set to a value other than an int."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].cut_duration = "a string"
    assert str(cm.value) == (
        "Shot.cut_duration should be a positive integer value, not str: 'a string'"
    )


def test_cut_duration_attribute_will_be_updated_if_cut_in_attribute_changed(
    setup_shot_db_tests,
):
    """cut_duration attribute updated if the cut_in attribute changed."""
    data = setup_shot_db_tests
    data["test_shot"].cut_in = 1
    assert (
        data["test_shot"].cut_duration
        == data["test_shot"].cut_out - data["test_shot"].cut_in + 1
    )


def test_cut_duration_attribute_will_be_updated_if_cut_out_attribute_changed(
    setup_shot_db_tests,
):
    """cut_duration attribute updated if the cut_out attribute changed."""
    data = setup_shot_db_tests
    data["test_shot"].cut_out = 1000
    assert (
        data["test_shot"].cut_duration
        == data["test_shot"].cut_out - data["test_shot"].cut_in + 1
    )


def test_cut_duration_attribute_changes_cut_out_attribute(setup_shot_db_tests):
    """changes in cut_duration attribute will also affect cut_out value."""
    data = setup_shot_db_tests
    first_cut_out = data["test_shot"].cut_out
    data["test_shot"].cut_duration = 245
    assert data["test_shot"].cut_out != first_cut_out
    assert (
        data["test_shot"].cut_out
        == data["test_shot"].cut_in + data["test_shot"].cut_duration - 1
    )


def test_cut_duration_attribute_is_zero(setup_shot_db_tests):
    """ValueError raised if the cut_duration attribute is set to zero."""
    data = setup_shot_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_shot"].cut_duration = 0
    assert str(cm.value) == (
        "Shot.cut_duration cannot be set to zero or a negative value"
    )


def test_cut_duration_attribute_is_negative(setup_shot_db_tests):
    """ValueError raised if the cut_duration attribute is set to a negative value."""
    data = setup_shot_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_shot"].cut_duration = -100

    assert str(cm.value) == (
        "Shot.cut_duration cannot be set to zero or a negative value"
    )


def test_source_in_argument_is_skipped(setup_shot_db_tests):
    """source_in arg is skipped the source_in arg equal to cut_in attr value."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"].pop("source_in")
    shot = Shot(**data["kwargs"])
    assert shot.source_in == shot.cut_in


def test_source_in_argument_is_none(setup_shot_db_tests):
    """source_in attr equal to the cut_in attr if the source_in arg is None."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_in"] = None
    shot = Shot(**data["kwargs"])
    assert shot.source_in == shot.cut_in


def test_source_in_attribute_is_set_to_none(setup_shot_db_tests):
    """TypeError raised if the source_in attribute is set to None."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].source_in = None

    assert str(cm.value) == "Shot.source_in should be an int, not NoneType: 'None'"


def test_source_in_argument_is_not_integer(setup_shot_db_tests):
    """TypeError raised if the source_in argument is not an instance of int."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_in"] = "a string"

    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == "Shot.source_in should be an int, not str: 'a string'"


def test_source_in_attribute_is_not_integer(setup_shot_db_tests):
    """TypeError raised if the source_in attr is set to a value other than an int."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].source_in = "a string"

    assert str(cm.value) == "Shot.source_in should be an int, not str: 'a string'"


def test_source_in_argument_is_bigger_than_source_out_argument(setup_shot_db_tests):
    """ValueError raised if the source_in arg is bigger than source_out arg value."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_out"] = data["kwargs"]["cut_out"] - 10
    data["kwargs"]["source_in"] = data["kwargs"]["source_out"] + 5
    with pytest.raises(ValueError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.source_out cannot be smaller than Shot.source_in, source_in: 144 where "
        "as source_out: 139"
    )


def test_source_in_attribute_is_bigger_than_source_out_attribute(setup_shot_db_tests):
    """ValueError raised if the source_in attr is set to bigger than source out."""
    data = setup_shot_db_tests
    # give it a little bit of room, to be sure that the ValueError is not
    # due to the cut_out
    data["test_shot"].source_out -= 5
    with pytest.raises(ValueError) as cm:
        data["test_shot"].source_in = data["test_shot"].source_out + 1

    assert str(cm.value) == (
        "Shot.source_in cannot be bigger than Shot.source_out, "
        "source_in: 136 where as source_out: 135"
    )


def test_source_in_argument_is_smaller_than_cut_in(setup_shot_db_tests):
    """ValueError raised if the source_in arg is smaller than cut_in attr value."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_in"] = data["kwargs"]["cut_in"] - 10
    with pytest.raises(ValueError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.source_in cannot be smaller than Shot.cut_in, cut_in: "
        "112 where as source_in: 102"
    )


def test_source_in_argument_is_bigger_than_cut_out(setup_shot_db_tests):
    """ValueError raised if the source_in arg is bigger than cut_out attr value."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_in"] = data["kwargs"]["cut_out"] + 10
    with pytest.raises(ValueError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.source_in cannot be bigger than Shot.cut_out, cut_out: "
        "149 where as source_in: 159"
    )


def test_source_out_argument_is_skipped(setup_shot_db_tests):
    """source_out attr equal to cut_out arg value if the source_out arg is skipped."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"].pop("source_out")
    new_shot = Shot(**data["kwargs"])
    assert new_shot.source_out == new_shot.cut_out


def test_source_out_argument_is_none(setup_shot_db_tests):
    """source_out attr value equal to cut_out if the source_out arg value is None."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_out"] = None
    shot = Shot(**data["kwargs"])
    assert shot.source_out == shot.cut_out


def test_source_out_attribute_is_set_to_none(setup_shot_db_tests):
    """TypeError raised if the source_out attribute is set to None."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].source_out = None
    assert str(cm.value) == "Shot.source_out should be an int, not NoneType: 'None'"


def test_source_out_argument_is_not_integer(setup_shot_db_tests):
    """TypeError raised if the source_out argument is not an integer."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_out"] = "a string"
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == "Shot.source_out should be an int, not str: 'a string'"


def test_source_out_attribute_is_not_integer(setup_shot_db_tests):
    """TypeError raised if the source_out attr is set to a value other than an int."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].source_out = "a string"
    assert str(cm.value) == "Shot.source_out should be an int, not str: 'a string'"


def test_source_out_argument_is_smaller_than_source_in_argument(setup_shot_db_tests):
    """ValueError raised if the source_out arg is smaller than the source_in attr."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_in"] = data["kwargs"]["cut_in"] + 15
    data["kwargs"]["source_out"] = data["kwargs"]["source_in"] - 10
    with pytest.raises(ValueError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.source_out cannot be smaller than Shot.source_in, "
        "source_in: 127 where as source_out: 117"
    )


def test_source_out_attribute_is_smaller_than_source_in_attribute(setup_shot_db_tests):
    """ValueError raised if the source_out attr is set to smaller than source_in."""
    data = setup_shot_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_shot"].source_out = data["test_shot"].source_in - 2

    assert str(cm.value) == (
        "Shot.source_out cannot be smaller than Shot.source_in, "
        "source_in: 120 where as source_out: 118"
    )


def test_source_out_argument_is_smaller_than_cut_in_argument(setup_shot_db_tests):
    """ValueError raised if the source_out arg is smaller than the cut_in attr."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_in"] = data["kwargs"]["cut_in"] + 15
    data["kwargs"]["source_out"] = data["kwargs"]["cut_in"] - 10
    with pytest.raises(ValueError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.source_out cannot be smaller than Shot.cut_in, "
        "cut_in: 112 where as source_out: 102"
    )


def test_source_out_attribute_is_smaller_than_cut_in_attribute(setup_shot_db_tests):
    """ValueError raised if the source_out attr is set to smaller than cut_in."""
    data = setup_shot_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_shot"].source_out = data["test_shot"].cut_in - 2

    assert str(cm.value) == (
        "Shot.source_out cannot be smaller than Shot.cut_in, "
        "cut_in: 112 where as source_out: 110"
    )


def test_source_out_argument_is_bigger_than_cut_out_argument(setup_shot_db_tests):
    """ValueError raised if the source_out arg is bigger than the cut_out attr."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    data["kwargs"]["source_in"] = data["kwargs"]["cut_in"] + 2
    data["kwargs"]["source_out"] = data["kwargs"]["cut_out"] + 20
    with pytest.raises(ValueError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.source_out cannot be bigger than Shot.cut_out, "
        "cut_out: 149 where as source_out: 169"
    )


def test_source_out_attribute_is_smaller_than_cut_out_attribute(setup_shot_db_tests):
    """ValueError raised if the source_out attr is set to bigger than cut_out."""
    data = setup_shot_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_shot"].source_out = data["test_shot"].cut_out + 2

    assert str(cm.value) == (
        "Shot.source_out cannot be bigger than Shot.cut_out, "
        "cut_out: 149 where as source_out: 151"
    )


def test_image_format_argument_is_skipped(setup_shot_db_tests):
    """image_format is copied from the Project if the image_format arg is skipped."""
    data = setup_shot_db_tests
    data["kwargs"].pop("image_format")
    data["kwargs"]["code"] = "TestShot"
    new_shot = Shot(**data["kwargs"])
    assert new_shot.image_format == data["kwargs"]["project"].image_format


def test_image_format_argument_is_none(setup_shot_db_tests):
    """image format is copied from the Project if the image_format arg is None."""
    data = setup_shot_db_tests
    data["kwargs"]["image_format"] = None
    data["kwargs"]["code"] = "newShot"
    new_shot = Shot(**data["kwargs"])
    assert new_shot.image_format == data["kwargs"]["project"].image_format


def test_image_format_attribute_is_none(setup_shot_db_tests):
    """image format is copied from the Project if the image_format attr is None."""
    data = setup_shot_db_tests
    # test start conditions
    assert data["test_shot"].image_format != data["test_shot"].project.image_format
    data["test_shot"].image_format = None
    assert data["test_shot"].image_format == data["test_shot"].project.image_format


def test_image_format_argument_is_not_a_image_format_instance_and_not_none(
    setup_shot_db_tests,
):
    """TypeError raised if the image_format arg is not a ImageFormat and not None."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "new_shot"
    data["kwargs"]["image_format"] = "not an image format instance"
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.image_format should be an instance of "
        "stalker.models.format.ImageFormat, not str: 'not an image format instance'"
    )


def test_image_format_attribute_is_not_a_ImageFormat_instance_and_not_none(
    setup_shot_db_tests,
):
    """TypeError raised if the image_format attr is not a ImageFormat and not None."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].image_format = "not an image f"

    assert str(cm.value) == (
        "Shot.image_format should be an instance of "
        "stalker.models.format.ImageFormat, not str: 'not an image f'"
    )


def test_image_format_argument_is_working_as_expected(setup_shot_db_tests):
    """image_format argument value is passed to the image_format attribute correctly."""
    data = setup_shot_db_tests
    assert data["kwargs"]["image_format"] == data["test_shot"].image_format


def test_image_format_attribute_is_working_as_expected(setup_shot_db_tests):
    """image_format attribute is working as expected."""
    data = setup_shot_db_tests
    assert data["test_shot"].image_format != data["test_image_format1"]
    data["test_shot"].image_format = data["test_image_format1"]
    assert data["test_shot"].image_format == data["test_image_format1"]


def test_equality(setup_shot_db_tests):
    """equality of shot objects."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    new_shot1 = Shot(**data["kwargs"])

    data["kwargs"]["project"] = data["test_project2"]
    new_shot2 = Shot(**data["kwargs"])
    # an entity with the same parameters
    # just set the name to the code too
    data["kwargs"]["name"] = data["kwargs"]["code"]
    new_entity = Entity(**data["kwargs"])

    # another shot with different code
    data["kwargs"]["code"] = "SHAnotherShot"
    new_shot3 = Shot(**data["kwargs"])

    assert not new_shot1 == new_shot2
    assert not new_shot1 == new_entity
    assert not new_shot1 == new_shot3


def test_inequality(setup_shot_db_tests):
    """inequality of shot objects."""
    data = setup_shot_db_tests
    data["kwargs"]["code"] = "SH123A"
    new_shot1 = Shot(**data["kwargs"])

    data["kwargs"]["project"] = data["test_project2"]
    new_shot2 = Shot(**data["kwargs"])
    # an entity with the same parameters
    # just set the name to the code too
    data["kwargs"]["name"] = data["kwargs"]["code"]
    new_entity = Entity(**data["kwargs"])

    # another shot with different code
    data["kwargs"]["code"] = "SHAnotherShot"
    new_shot3 = Shot(**data["kwargs"])

    assert new_shot1 != new_shot2
    assert new_shot1 != new_entity
    assert new_shot1 != new_shot3


def test_ReferenceMixin_initialization(setup_shot_db_tests):
    """ReferenceMixin part is initialized correctly."""
    data = setup_shot_db_tests
    link_type_1 = Type(name="Image", code="image", target_entity_type="Link")

    link1 = Link(
        name="Artwork 1",
        full_path="/mnt/M/JOBs/TEST_PROJECT",
        filename="a.jpg",
        type=link_type_1,
    )

    link2 = Link(
        name="Artwork 2",
        full_path="/mnt/M/JOBs/TEST_PROJECT",
        filename="b.jbg",
        type=link_type_1,
    )

    references = [link1, link2]

    data["kwargs"]["code"] = "SH12314"
    data["kwargs"]["references"] = references

    new_shot = Shot(**data["kwargs"])

    assert new_shot.references == references


def test_TaskMixin_initialization(setup_shot_db_tests):
    """TaskMixin part is initialized correctly."""
    data = setup_shot_db_tests
    project_status_list = StatusList.query.filter(
        StatusList.target_entity_type == "Project"
    ).first()

    project_type = Type(name="Commercial", code="comm", target_entity_type="Project")

    new_project = Project(
        name="Commercial1",
        code="comm1",
        status_list=project_status_list,
        type=project_type,
        repository=data["test_repository"],
    )
    DBSession.add(new_project)
    DBSession.commit()

    data["kwargs"]["project"] = new_project
    data["kwargs"]["code"] = "SH12314"

    new_shot = Shot(**data["kwargs"])

    task1 = Task(
        name="Modeling",
        status=0,
        project=new_project,
        parent=new_shot,
    )

    task2 = Task(
        name="Lighting",
        status=0,
        project=new_project,
        parent=new_shot,
    )

    tasks = [task1, task2]

    assert sorted(new_shot.tasks, key=lambda x: x.name) == sorted(
        tasks, key=lambda x: x.name
    )


def test__repr__(setup_shot_db_tests):
    """representation of Shot."""
    data = setup_shot_db_tests
    assert data["test_shot"].__repr__() == "<Shot ({}, {})>".format(
        data["test_shot"].code,
        data["test_shot"].code,
    )


def test_plural_class_name(setup_shot_db_tests):
    """plural name of Shot class."""
    data = setup_shot_db_tests
    assert data["test_shot"].plural_class_name == "Shots"


def test___strictly_typed___is_false():
    """__strictly_typed__ class attribute is False for Shot class."""
    assert Shot.__strictly_typed__ is False


def test_cut_duration_initialization_bug_with_cut_in(setup_shot_db_tests):
    """_cut_duration attribute is initialized correctly for a Shot restored from DB."""
    data = setup_shot_db_tests
    # retrieve the shot back from DB
    test_shot_db = Shot.query.filter_by(name=data["kwargs"]["name"]).first()
    # trying to change the cut_in and cut_out values should not raise any
    # errors
    test_shot_db.cut_in = 1
    DBSession.add(test_shot_db)
    DBSession.commit()


def test_cut_duration_initialization_bug_with_cut_out(setup_shot_db_tests):
    """_cut_duration attribute is initialized correctly for a Shot restored from DB."""
    data = setup_shot_db_tests
    # reconnect to the database
    # retrieve the shot back from DB
    test_shot_db = Shot.query.filter_by(name=data["kwargs"]["name"]).first()
    # trying to change the cut_in and cut_out values should not raise any
    # errors
    test_shot_db.cut_out = 100
    DBSession.add(test_shot_db)
    DBSession.commit()


def test_cut_values_are_set_correctly(setup_shot_db_tests):
    """cut_in attribute is set correctly in db."""
    data = setup_shot_db_tests
    data["test_shot"].cut_in = 100
    assert data["test_shot"].cut_in == 100

    data["test_shot"].cut_out = 153
    assert data["test_shot"].cut_in == 100
    assert data["test_shot"].cut_out == 153

    DBSession.add(data["test_shot"])
    DBSession.commit()

    # retrieve the shot back from DB
    test_shot_db = Shot.query.filter_by(name=data["kwargs"]["name"]).first()

    assert test_shot_db.cut_in == 100
    assert test_shot_db.cut_out == 153


def test_fps_argument_is_skipped(setup_shot_db_tests):
    """default value used if fps is skipped."""
    data = setup_shot_db_tests
    if "fps" in data["kwargs"]:
        data["kwargs"].pop("fps")

    data["kwargs"]["code"] = "SHnew"
    new_shot = Shot(**data["kwargs"])
    assert new_shot.fps == data["test_project1"].fps


def test_fps_attribute_is_set_to_None(setup_shot_db_tests):
    """Project.fps used if the fps argument is None."""
    data = setup_shot_db_tests
    data["kwargs"]["fps"] = None
    data["kwargs"]["code"] = "SHnew"
    new_shot = Shot(**data["kwargs"])
    assert new_shot.fps == data["test_project1"].fps


@pytest.mark.parametrize("test_value", [["a", "list"], {"a": "list"}])
def test_fps_argument_is_given_as_non_float_or_integer(test_value, setup_shot_db_tests):
    """TypeError raised if the fps arg not float or int."""
    data = setup_shot_db_tests
    data["kwargs"]["fps"] = test_value
    data["kwargs"]["code"] = "SH%i"
    with pytest.raises(TypeError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == (
        "Shot.fps should be a positive float or int, not {}: '{}'".format(
            test_value.__class__.__name__, test_value
        )
    )


@pytest.mark.parametrize("test_value", [["a", "list"], {"a": "list"}])
def test_fps_attribute_is_given_as_non_float_or_integer(
    test_value, setup_shot_db_tests
):
    """TypeError raised if the fps attr is not a float or int."""
    data = setup_shot_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_shot"].fps = test_value

    assert str(cm.value) == (
        "Shot.fps should be a positive float or int, not {}: '{}'".format(
            test_value.__class__.__name__, test_value
        )
    )


def test_fps_attribute_float_conversion(setup_shot_db_tests):
    """fps attr is converted to float if the fps argument is given as an int."""
    data = setup_shot_db_tests
    test_value = 1
    data["kwargs"]["fps"] = test_value
    data["kwargs"]["code"] = "SHnew"
    new_shot = Shot(**data["kwargs"])
    assert isinstance(new_shot.fps, float)
    assert new_shot.fps == float(test_value)


def test_fps_attribute_float_conversion_2(setup_shot_db_tests):
    """fps attribute is converted to float if it is set to an int value."""
    data = setup_shot_db_tests
    test_value = 1
    data["test_shot"].fps = test_value
    assert isinstance(data["test_shot"].fps, float)
    assert data["test_shot"].fps == float(test_value)


def test_fps_argument_is_zero(setup_shot_db_tests):
    """ValueError raised if the fps is 0."""
    data = setup_shot_db_tests
    data["kwargs"]["fps"] = 0
    data["kwargs"]["code"] = "SHnew"
    with pytest.raises(ValueError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == "Shot.fps should be a positive float or int, not 0.0"


def test_fps_attribute_is_set_to_zero(setup_shot_db_tests):
    """value error raised if the fps attribute is set to zero."""
    data = setup_shot_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_shot"].fps = 0
    assert str(cm.value) == "Shot.fps should be a positive float or int, not 0.0"


def test_fps_argument_is_negative(setup_shot_db_tests):
    """ValueError raised if the fps argument is negative."""
    data = setup_shot_db_tests
    data["kwargs"]["fps"] = -1.0
    data["kwargs"]["code"] = "SHrandom"
    with pytest.raises(ValueError) as cm:
        Shot(**data["kwargs"])

    assert str(cm.value) == "Shot.fps should be a positive float or int, not -1.0"


def test_fps_attribute_is_negative(setup_shot_db_tests):
    """ValueError raised if the fps attribute is set to a negative value."""
    data = setup_shot_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_shot"].fps = -1

    assert str(cm.value) == "Shot.fps should be a positive float or int, not -1.0"


def test_fps_changes_with_project(setup_shot_db_tests):
    """fps reflects the project.fps unless it is set to a value."""
    data = setup_shot_db_tests
    new_shot = Shot(name="New Shot", code="ns", project=data["test_project1"])
    assert new_shot.fps == data["test_project1"].fps
    data["test_project1"].fps = 335
    assert new_shot.fps == 335
    new_shot.fps = 12
    assert new_shot.fps == 12
    data["test_project1"].fps = 24
    assert new_shot.fps == 12


def test__check_code_availability_code_is_none(setup_shot_db_tests):
    """__check_code_availability() returns True if the code is None."""
    data = setup_shot_db_tests
    assert isinstance(data["test_shot"], Shot)
    result = data["test_shot"]._check_code_availability(None, data["test_project1"])
    assert result is True


def test__check_code_availability_code_is_not_str(setup_shot_db_tests):
    """__check_code_availability() raises TypeError if code is not a str."""
    data = setup_shot_db_tests
    assert isinstance(data["test_shot"], Shot)
    with pytest.raises(TypeError) as cm:
        _ = data["test_shot"]._check_code_availability(1234, data["test_project1"])

    assert str(cm.value) == (
        "code should be a string containing a shot code, not int: '1234'"
    )


def test__check_code_availability_project_is_none(setup_shot_db_tests):
    """__check_code_availability() returns True if project is None"""
    data = setup_shot_db_tests
    assert isinstance(data["test_shot"], Shot)
    result = data["test_shot"]._check_code_availability("SH123", None)
    assert result is True


def test__check_code_availability_project_is_not_a_project_instance(
    setup_shot_db_tests,
):
    """__check_code_availability() raises TypeError if the Project is not a Project instance."""
    data = setup_shot_db_tests
    assert isinstance(data["test_shot"], Shot)
    with pytest.raises(TypeError) as cm:
        _ = data["test_shot"]._check_code_availability("SH123", 1234)

    assert str(cm.value) == ("project should be a Project instance, not int: '1234'")


def test_check_code_availability_fallbacks_to_python_if_db_is_not_available():
    """__check_code_availability() fallbacks to Python if DB is not available."""
    data = dict()
    # statuses
    rts = Status(name="Read To Start", code="RTS")
    wip = Status(name="Work In Progress", code="WIP")
    cmpl = Status(name="Completed", code="CMPL")
    project_status_list = StatusList(
        name="Project Statuses", statuses=[rts, wip, cmpl], target_entity_type="Project"
    )
    shot_status_list = StatusList(
        name="Shot Status List", statuses=[rts, wip, cmpl], target_entity_type="Shot"
    )

    # types
    data["test_commercial_project_type"] = Type(
        name="Commercial Project",
        code="comm",
        target_entity_type="Project",
    )

    data["test_repository_type"] = Type(
        name="Test Repository Type", code="test", target_entity_type="Repository"
    )

    # repository
    data["test_repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["test_repository_type"],
    )

    # image format
    data["test_image_format1"] = ImageFormat(
        name="Test Image Format 1", width=1920, height=1080, pixel_aspect=1.0
    )

    # project and sequences
    data["test_project1"] = Project(
        name="Test Project1",
        code="tp1",
        type=data["test_commercial_project_type"],
        repository=data["test_repository"],
        image_format=data["test_image_format1"],
        status_list=project_status_list,
    )

    data["kwargs"] = dict(
        name="SH123",
        code="SH123",
        description="This is a test Shot",
        project=data["test_project1"],
        status=0,
        status_list=shot_status_list,
    )

    # create a mock shot object
    data["test_shot"] = Shot(**data["kwargs"])

    assert Shot._check_code_availability("SH123", data["test_project1"]) is False


def test__init_on_load__works_as_expected(setup_shot_db_tests):
    """__init_on_load__() works as expected."""
    data = setup_shot_db_tests
    assert data["test_shot"] in DBSession
    DBSession.commit()
    DBSession.flush()
    connection = DBSession.connection()
    connection.close()
    del data["test_shot"]

    from stalker.db.setup import setup

    setup(data["database_settings"]["config"])

    # the following should call Shot.__init_on_load__()
    shot = Shot.query.filter(Shot.name == "SH123").first()
    assert isinstance(shot, Shot)


def test_template_variables_include_scenes_for_shots(setup_shot_db_tests):
    """_template_variables include scenes for shots."""
    data = setup_shot_db_tests
    assert isinstance(data["test_shot"], Shot)
    template_variables = data["test_shot"]._template_variables()
    assert "scenes" in template_variables
    assert data["test_shot"].scenes != []
    assert template_variables["scenes"] == data["test_shot"].scenes


def test_template_variables_include_sequences_for_shots(setup_shot_db_tests):
    """_template_variables include sequences for shots."""
    data = setup_shot_db_tests
    assert isinstance(data["test_shot"], Shot)
    template_variables = data["test_shot"]._template_variables()
    assert "sequences" in template_variables
    assert data["test_shot"].sequences != []
    assert template_variables["sequences"] == data["test_shot"].sequences
