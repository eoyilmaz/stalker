# -*- coding: utf-8 -*-
"""StatusMixin class related tests."""
import pytest

from sqlalchemy import Column, ForeignKey, Integer

from stalker import SimpleEntity, Status, StatusList, StatusMixin


class DeclStatMixA(SimpleEntity, StatusMixin):
    """A class for testing StatusMixin."""

    __tablename__ = "DeclStatMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclStatMixA"}
    declStatMixAs_id = Column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(DeclStatMixA, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


class DeclStatMixB(SimpleEntity, StatusMixin):
    """A class for testing StatusMixin."""

    __tablename__ = "DeclStatMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclStatMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    def __init__(self, **kwargs):
        super(DeclStatMixB, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def setup_status_mixin_tester():
    """Set up the tests for StatusMixin.

    Returns:
        dict: Test data.
    """
    data = dict()
    data["test_stat1"] = Status(name="On Hold", code="OH")
    data["test_stat2"] = Status(name="Work In Progress", code="WIP")
    data["test_stat3"] = Status(name="Approved", code="APP")
    data["test_a_statusList"] = StatusList(
        name="A Statuses",
        statuses=[data["test_stat1"], data["test_stat3"]],
        target_entity_type="DeclStatMixA",
    )
    data["test_b_statusList"] = StatusList(
        name="B Statuses",
        statuses=[data["test_stat2"], data["test_stat3"]],
        target_entity_type="DeclStatMixB",
    )
    data["kwargs"] = {"name": "ozgur", "status_list": data["test_a_statusList"]}
    return data


def test_status_list_argument_not_set(setup_status_mixin_tester):
    """TypeError will be raised if the status_list argument is not set."""
    data = setup_status_mixin_tester
    data["kwargs"].pop("status_list")
    with pytest.raises(TypeError) as cm:
        DeclStatMixA(**data["kwargs"])
    assert (
        str(cm.value) == "DeclStatMixA instances cannot be initialized without a "
        "stalker.models.status.StatusList instance, please pass a suitable StatusList "
        "(StatusList.target_entity_type=DeclStatMixA) with the 'status_list' argument"
    )


def test_status_list_argument_is_not_correct(setup_status_mixin_tester):
    """TypeError is raised if status_list argument is not a StatusList."""
    data = setup_status_mixin_tester
    data["kwargs"]["status_list"] = data["test_b_statusList"]
    with pytest.raises(TypeError) as cm:
        DeclStatMixA(**data["kwargs"])
    assert (
        str(cm.value) == "The given StatusLists' target_entity_type is DeclStatMixB, "
        "whereas the entity_type of this object is DeclStatMixA"
    )


def test_status_list_working_properly(setup_status_mixin_tester):
    """status_list attribute is working properly."""
    data = setup_status_mixin_tester
    new_a_ins = DeclStatMixA(name="Ozgur", status_list=data["test_a_statusList"])
    assert data["test_stat1"] in new_a_ins.status_list
    assert data["test_stat2"] not in new_a_ins.status_list
    assert data["test_stat3"] in new_a_ins.status_list
