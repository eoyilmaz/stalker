# -*- coding: utf-8 -*-
"""Tests Client class."""
import datetime

import pytest

import pytz

from stalker import Client, Entity, Good, Project, Repository, Status, StatusList, User


@pytest.fixture(scope="function")
def setup_client_tests():
    """Set up the tests for the Client class."""
    data = dict()

    # create a couple of test users
    data["test_user1"] = User(
        name="User1",
        login="user1",
        email="user1@test.com",
        password="123456",
    )

    data["test_user2"] = User(
        name="User2",
        login="user2",
        email="user2@test.com",
        password="123456",
    )

    data["test_user3"] = User(
        name="User3",
        login="user3",
        email="user3@test.com",
        password="123456",
    )

    data["test_user4"] = User(
        name="User4",
        login="user4",
        email="user4@test.com",
        password="123456",
    )

    data["users_list"] = [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
        data["test_user4"],
    ]

    data["test_admin"] = User(
        name="admin", login="admin", email="admin@admins.com", password="1234"
    )

    data["status_new"] = Status(name="New", code="NEW")
    data["status_wip"] = Status(name="Work In Progress", code="WIP")
    data["status_cmpl"] = Status(name="Completed", code="CMPL")

    data["project_statuses"] = StatusList(
        name="Project Status List",
        statuses=[data["status_new"], data["status_wip"], data["status_cmpl"]],
        target_entity_type="Project",
    )

    data["test_repo"] = Repository(name="Test Repository", code="TR")

    data["test_project1"] = Project(
        name="Test Project 1",
        code="proj1",
        status_list=data["project_statuses"],
        repository=data["test_repo"],
    )

    data["test_project2"] = Project(
        name="Test Project 1",
        code="proj2",
        status_list=data["project_statuses"],
        repository=data["test_repo"],
    )
    data["test_project3"] = Project(
        name="Test Project 1",
        code="proj3",
        status_list=data["project_statuses"],
        repository=data["test_repo"],
    )
    data["projects_list"] = [
        data["test_project1"],
        data["test_project2"],
        data["test_project3"],
    ]
    data["date_created"] = data["date_updated"] = datetime.datetime.now(pytz.utc)
    data["kwargs"] = {
        "name": "Test Client",
        "description": "This is a client for testing purposes",
        "created_by": data["test_admin"],
        "updated_by": data["test_admin"],
        "date_created": data["date_created"],
        "date_updated": data["date_updated"],
        "users": data["users_list"],
        "projects": data["projects_list"],
    }
    # create a default client object
    data["test_client"] = Client(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Department class."""
    assert Client.__auto_name__ is False


def test_users_argument_accepts_an_empty_list(setup_client_tests):
    """users argument accepts an empty list."""
    data = setup_client_tests
    # this should work without raising any error
    data["kwargs"]["users"] = []
    new_dep = Client(**data["kwargs"])
    assert isinstance(new_dep, Client)


def test_users_attribute_accepts_an_empty_list(setup_client_tests):
    """users attribute accepts an empty list."""
    data = setup_client_tests
    # this should work without raising any error
    data["test_client"].users = []


def test_users_argument_accepts_only_a_list_of_user_objects(setup_client_tests):
    """users argument accepts only a list of user objects."""
    data = setup_client_tests
    test_value = [1, 2.3, [], {}]
    data["kwargs"]["users"] = test_value
    # this should raise a TypeError
    with pytest.raises(TypeError) as cm:
        Client(**data["kwargs"])

    assert (
        str(cm.value) == "ClientUser.user should be an instance of "
        "stalker.models.auth.User, not int"
    )


def test_users_attribute_accepts_only_a_list_of_user_objects(setup_client_tests):
    """users attribute accepts only a list of user objects."""
    data = setup_client_tests
    test_value = [1, 2.3, [], {}]
    # this should raise a TypeError
    with pytest.raises(TypeError) as cm:
        data["test_client"].users = test_value

    assert (
        str(cm.value) == "ClientUser.user should be an instance of "
        "stalker.models.auth.User, not int"
    )


def test_users_attribute_elements_accepts_user_only_append(setup_client_tests):
    """TypeError is raised if users list assigned a value other than a User instance."""
    data = setup_client_tests
    # append
    with pytest.raises(TypeError) as cm:
        data["test_client"].users.append(0)

    assert str(cm.value) == (
        "ClientUser.user should be an instance of stalker.models.auth.User, not int"
    )


def test_users_attribute_elements_accepts_user_only_setitem(setup_client_tests):
    """TypeError is raised if users list assigned a value other than a User instance."""
    data = setup_client_tests
    # __setitem__
    with pytest.raises(TypeError) as cm:
        data["test_client"].users[0] = 0

    assert str(cm.value) == (
        "ClientUser.user should be an instance of stalker.models.auth.User, not int"
    )


def test_users_argument_is_not_iterable(setup_client_tests):
    """TypeError is raised if the given users argument is not a list."""
    data = setup_client_tests
    data["kwargs"]["users"] = "a user"
    with pytest.raises(TypeError) as cm:
        Client(**data["kwargs"])

    assert str(cm.value) == (
        "ClientUser.user should be an instance of stalker.models.auth.User, not str"
    )


def test_users_attribute_is_not_iterable(setup_client_tests):
    """TypeError is raised if the users attribute is not iterable."""
    data = setup_client_tests
    test_value = "a user"
    with pytest.raises(TypeError) as cm:
        data["test_client"].users = test_value

    assert str(cm.value) == (
        "ClientUser.user should be an instance of stalker.models.auth.User, not str"
    )


def test_users_attribute_defaults_to_empty_list(setup_client_tests):
    """users attribute defaults to an empty list if the users argument is skipped."""
    data = setup_client_tests
    data["kwargs"].pop("users")
    new_client = Client(**data["kwargs"])
    assert new_client.users == []


def test_users_attribute_set_to_none(setup_client_tests):
    """TypeError will be raised if the users attribute is set to None."""
    data = setup_client_tests
    with pytest.raises(TypeError) as cm:
        data["test_client"].users = None
    assert str(cm.value) == "'NoneType' object is not iterable"


def test_projects_argument_accepts_an_empty_list(setup_client_tests):
    """projects argument accepts an empty list."""
    data = setup_client_tests
    # this should work without raising any error
    data["kwargs"]["projects"] = []
    new_dep = Client(**data["kwargs"])
    assert isinstance(new_dep, Client)


def test_projects_attribute_accepts_an_empty_list(setup_client_tests):
    """projects attribute accepts an empty list."""
    data = setup_client_tests
    # this should work without raising any error
    data["test_client"].projects = []


def test_projects_argument_accepts_only_a_list_of_project_objects(setup_client_tests):
    """projects argument accepts only a list of project objects."""
    data = setup_client_tests
    test_value = [1, 2.3, [], {}]
    data["kwargs"]["projects"] = test_value
    # this should raise a TypeError
    with pytest.raises(TypeError) as cm:
        Client(**data["kwargs"])

    assert str(cm.value) == (
        "ProjectClient.project should be a stalker.models.project.Project instance, "
        "not int"
    )


def test_projects_attribute_accepts_only_a_list_of_project_objects(setup_client_tests):
    """users attribute accepts only a list of project objects."""
    data = setup_client_tests
    test_value = [1, 2.3, "a project"]
    # this should raise a TypeError
    with pytest.raises(TypeError) as cm:
        data["test_client"].projects = test_value

    assert str(cm.value) == (
        "ProjectClient.project should be a "
        "stalker.models.project.Project instance, not int"
    )


def test_projects_attribute_elements_accepts_project_only_append(setup_client_tests):
    """TypeError is raised if assigned a non Project instance to the project attr."""
    data = setup_client_tests
    # append
    with pytest.raises(TypeError) as cm:
        data["test_client"].projects.append(0)

    assert str(cm.value) == (
        "ProjectClient.project should be a "
        "stalker.models.project.Project instance, not int"
    )


def test_projects_attribute_elements_accepts_project_only_setitem(setup_client_tests):
    """TypeError is raised if assigned a non Project instance to the projects attr."""
    data = setup_client_tests
    # __setitem__
    with pytest.raises(TypeError) as cm:
        data["test_client"].projects[0] = 0

    assert (
        str(cm.value) == "ProjectClient.project should be a "
        "stalker.models.project.Project instance, not int"
    )


def test_projects_argument_is_not_iterable(setup_client_tests):
    """TypeError is raised if the given projects argument is not a list."""
    data = setup_client_tests
    data["kwargs"]["projects"] = "a project"
    with pytest.raises(TypeError) as cm:
        Client(**data["kwargs"])

    assert str(cm.value) == (
        "ProjectClient.project should be a "
        "stalker.models.project.Project instance, not str"
    )


def test_projects_attribute_is_not_iterable(setup_client_tests):
    """TypeError is raised if the projects attr is set to a non-iterable value."""
    data = setup_client_tests
    test_value = "a project"
    with pytest.raises(TypeError) as cm:
        data["test_client"].projects = test_value

    assert str(cm.value) == (
        "ProjectClient.project should be a "
        "stalker.models.project.Project instance, not str"
    )


def test_projects_attribute_defaults_to_empty_list(setup_client_tests):
    """projects attr defaults to an empty list if the projects argument is skipped."""
    data = setup_client_tests
    data["kwargs"].pop("projects")
    new_client = Client(**data["kwargs"])
    assert new_client.projects == []


def test_projects_attribute_set_to_none(setup_client_tests):
    """TypeError is raised if the projects attribute is set to None."""
    data = setup_client_tests
    with pytest.raises(TypeError) as cm:
        data["test_client"].projects = None

    assert str(cm.value) == "'NoneType' object is not iterable"


def test_user_remove_also_removes_client_from_user(setup_client_tests):
    """Removing user from the users removes the client from the users companies."""
    data = setup_client_tests
    # check if the user is in the company
    assert data["test_client"] in data["test_user1"].companies

    # now remove the user from the company
    data["test_client"].users.remove(data["test_user1"])

    # now check if company is not in users companies anymore
    assert data["test_client"] not in data["test_user1"].companies

    # assign the user back
    data["test_user1"].companies.append(data["test_client"])

    # check if the user is in the companies users list
    assert data["test_user1"] in data["test_client"].users


# def test_project_remove_also_removes_project_from_client(setup_client_tests):
#     """removing user from the users removes the client from the users companies."""
#     data = setup_client_tests
#     # check if the project is registered with the client
#     assert data["test_client"] in data["test_project1"].clients
#
#     # now remove the project from the client
#     # data["test_client"].projects.remove(data["test_project1"])
#     data["test_client"].project_role.remove(data["test_client"].project_role[0])
#
#     # now check if project no longer belongs to client
#     assert data["test_project1"] not in data["test_client"].projects
#
#     # assign the project back
#     data["test_client"].projects.append(data["test_project1"])
#
#     # check if the project is in the companies projects list
#     assert data["test_project1"] in data["test_client"].projects


def test_equality(setup_client_tests):
    """equality of two Client objects."""
    data = setup_client_tests
    client1 = Client(**data["kwargs"])
    client2 = Client(**data["kwargs"])

    entity_kwargs = data["kwargs"].copy()
    entity_kwargs.pop("users")
    entity_kwargs.pop("projects")
    entity1 = Entity(**entity_kwargs)

    data["kwargs"]["name"] = "Company X"
    client3 = Client(**data["kwargs"])

    assert client1 == client2
    assert not client1 == client3
    assert not client1 == entity1


def test_inequality(setup_client_tests):
    """inequality of two Client objects."""
    data = setup_client_tests
    client1 = Client(**data["kwargs"])
    client2 = Client(**data["kwargs"])

    entity_kwargs = data["kwargs"].copy()
    entity_kwargs.pop("users")
    entity_kwargs.pop("projects")
    entity1 = Entity(**entity_kwargs)

    data["kwargs"]["name"] = "Company X"
    client3 = Client(**data["kwargs"])

    assert not client1 != client2
    assert client1 != client3
    assert client1 != entity1


def test_to_tjp_method_is_working_properly(setup_client_tests):
    """to_tjp method is working properly."""
    data = setup_client_tests
    client1 = Client(**data["kwargs"])
    assert client1.to_tjp() == ""


def test_hash_is_correctly_calculated(setup_client_tests):
    """hash value is correctly calculated."""
    data = setup_client_tests
    client1 = Client(**data["kwargs"])
    assert client1.__hash__() == hash(client1.id) + 2 * hash(client1.name) + 3 * hash(
        client1.entity_type
    )


def test_goods_attribute_is_set_to_none(setup_client_tests):
    """TypeError is raised if good is set to None."""
    data = setup_client_tests
    client1 = Client(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        client1.goods = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_goods_attribute_is_set_to_a_list_of_non_good_instances(setup_client_tests):
    """TypeError is raised if the goods attr is set to a list of non Good instances."""
    data = setup_client_tests
    client1 = Client(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        client1.goods = ["not", 1, "list", "of", "goods"]

    assert str(cm.value) == (
        "Client.goods attribute should be all "
        "stalker.models.budget.Good instances, not str"
    )


def test_goods_attribute_is_working_properly(setup_client_tests):
    """goods attribute is working properly."""
    data = setup_client_tests
    client1 = Client(**data["kwargs"])
    good1 = Good(name="Test Good 1")
    good2 = Good(name="Test Good 2")
    good3 = Good(name="Test Good 3")
    client1.goods = [good1, good2, good3]

    assert client1.goods == [good1, good2, good3]
