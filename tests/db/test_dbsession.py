from stalker import User
from stalker.db.session import DBSession, ExtendedScopedSession


def test_dbsession_save_method_is_correctly_created(setup_postgresql_db):
    """DBSession is correctly created from ExtendedScopedSession class."""
    assert isinstance(DBSession, ExtendedScopedSession)


def test_dbsession_save_method_is_working_as_expected_for_single_entity(
    setup_postgresql_db,
):
    """DBSession.save() method is working as expected for single entity."""
    test_user = User(
        name="Test User", login="tuser", email="tuser@gmail.com", password="12345"
    )
    DBSession.save(test_user)

    del test_user
    test_user_db = User.query.filter(User.name == "Test User").first()
    assert test_user_db is not None


def test_dbsession_save_method_is_working_as_expected_for_multiple_entity(
    setup_postgresql_db,
):
    """DBSession.save() method is working as expected for single entity."""
    test_user1 = User(
        name="Test User 1",
        login="tuser1",
        email="tuser1@gmail.com",
        password="12345",
    )
    test_user2 = User(
        name="Test User 2",
        login="tuser2",
        email="tuser2@gmail.com",
        password="12345",
    )

    DBSession.save([test_user1, test_user2])

    del test_user1
    del test_user2
    test_user1_db = User.query.filter(User.name == "Test User 1").first()
    test_user2_db = User.query.filter(User.name == "Test User 2").first()
    assert test_user1_db is not None
    assert test_user2_db is not None


def test_dbsession_save_method_is_working_as_expected_for_no_entry(setup_postgresql_db):
    """DBSession.save() method is working as expected with no parameters."""
    test_user = User(
        name="Test User", login="tuser", email="tuser@gmail.com", password="12345"
    )
    DBSession.add(test_user)
    DBSession.save()

    del test_user
    test_user_db = User.query.filter(User.name == "Test User").first()
    assert test_user_db is not None
