# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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

import unittest2
import datetime
import stalker
from stalker import Type, User

# create a new class deriving from the SimpleEntity
from stalker.models.entity import SimpleEntity


class newClass(SimpleEntity):
    __strictly_typed__ = True


class SimpleEntityTester(unittest2.TestCase):
    """testing the SimpleEntity class
    """

    def setUp(self):
        """setting up some proper values
        """
        # create a user
        self.test_user = User(
            name="Test User",
            login="testuser",
            email="test@user.com",
            password="test"
        )

        self.date_created = datetime.datetime(2010, 10, 21, 3, 8, 0)
        self.date_updated = self.date_created

        self.kwargs = {
            "name": "Test Entity",
            "code": "TstEnt",
            "description": "This is a test entity, and this is a proper \
            description for it",
            "created_by": self.test_user,
            "updated_by": self.test_user,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }

        # create a proper SimpleEntity to use it later in the tests
        self.test_simple_entity = SimpleEntity(**self.kwargs)

        self.test_type = Type(
            name="Test Type",
            code='test',
            target_entity_type=SimpleEntity
        )

        # a couple of test values

        self.name_test_values = [
            ("testName", "testName"),
            ("test-Name", "test-Name"),
            ("1testName", "1testName"),
            ("_testName", "_testName"),
            ("2423$+^^+^'%+%%&_testName", "2423$+^^+^'%+%%&_testName"),
            ("2423$+^^+^'%+%%&_testName_35", "2423$+^^+^'%+%%&_testName_35"),
            ("2423$ +^^+^ '%+%%&_ testName_ 35",
             "2423$ +^^+^ '%+%%&_ testName_ 35"),
            ("SH001", "SH001"),
            ("46-BJ-3A", "46-BJ-3A"),
            ('304-sb-0403-0040', '304-sb-0403-0040'),
            ("Ozgur    Yilmaz\n\n\n", "Ozgur Yilmaz"),
            ("     Ozgur Yilmaz    ", "Ozgur Yilmaz")
        ]

        self.nice_name_test_values = [
            ("testName", "testName"),
            ("1testName", "1testName"),
            ("_testName", "testName"),
            ("2423$+^^+^'%+%%&_testName", "2423_testName"),
            ("2423$+^^+^'%+%%&_testName_35", "2423_testName_35"),
            ("2423$ +^^+^ '%+%%&_ testName_ 35", "2423_testName_35"),
            ("SH001", "SH001"),
            ("My name is Ozgur", "My_name_is_Ozgur"),
            (" this is another name for an asset",
             "this_is_another_name_for_an_asset"),
            ("Ozgur    Yilmaz\n\n\n", "Ozgur_Yilmaz"),
        ]

    def test___auto_name__attribute_is_True(self):
        """testing if the __auto_name__ class attribute is set to True
        """
        self.assertTrue(SimpleEntity.__auto_name__)

    def test_name_argument_is_None(self):
        """testing if the name attribute will be automatically generated if the
        name argument is None
        """
        self.kwargs["name"] = None
        new_simple_entity = SimpleEntity(**self.kwargs)
        self.assertTrue(new_simple_entity.name)

    def test_name_attribute_is_set_to_None(self):
        """testing if the name attribute will be set to an automatic value if
        it is set to None
        """
        self.test_simple_entity.name = ''
        self.assertTrue(self.test_simple_entity.name)

    def test_name_argument_is_empty_string(self):
        """testing if the name attribute will be set to an automatic value if
        the name argument is an empty string
        """
        self.kwargs["name"] = ""
        new_simple_entity = SimpleEntity(**self.kwargs)
        self.assertTrue(new_simple_entity.name)

    def test_name_attribute_is_set_to_empty_string(self):
        """testing if the name attribute will be set to an automatic value if
        it is set to an automatic value
        """
        self.test_simple_entity.name = ''
        self.assertTrue(self.test_simple_entity)

    def test_name_argument_is_not_a_string_or_unicode_instance_or_None(self):
        """testing if a TypeError will be raised when the name argument is not
        a string or unicode or None
        """
        test_values = [
            12132,
            [1, "name"],
            {"a": "name"}
        ]

        for test_value in test_values:
            self.kwargs["name"] = test_value
            self.assertRaises(TypeError, SimpleEntity, **self.kwargs)

    def test_name_attribute_is_not_string_or_unicode_or_None(self):
        """testing if a TypeError will be raised when the name attribute is
        not a string or unicode or None
        """
        test_values = [
            12132, [1, "name"], {"a": "name"}
        ]

        for test_value in test_values:
            self.assertRaises(TypeError, setattr, self.test_simple_entity,
                              "name", test_value)

    def test_name_attribute_is_formatted_correctly(self):
        """testing if name is formatted correctly
        """
        for test_value in self.name_test_values:
            # set the new name
            self.test_simple_entity.name = test_value[0]

            self.assertEqual(
                self.test_simple_entity.name,
                test_value[1],
                "\nfor     : %s\nexpected: %s\ngot     : %s" % \
                (str(test_value[0]), test_value[1],
                 self.test_simple_entity.name)
            )

    def test_nice_name_attribute_is_formatted_correctly(self):
        """testing if nice name attribute is formatted correctly
        """
        for test_value in self.nice_name_test_values:
            self.test_simple_entity.name = test_value[0]

            self.assertEqual(
                self.test_simple_entity.nice_name,
                test_value[1],
                "the nice name attribute is not correctly formatted for, " + \
                test_value[0] + ", " + test_value[1]
            )

    def test_nice_name_attribute_is_read_only(self):
        """testing if nice name attribute is read-only
        """
        self.assertRaises(
            AttributeError,
            setattr,
            self.test_simple_entity,
            "nice_name",
            "a text"
        )

    def test_description_argument_None(self):
        """testing if description proeprty will be convertod to an empty string
        if None is given as the description argument
        """
        self.kwargs["description"] = None
        new_simple_entity = SimpleEntity(**self.kwargs)

        self.assertEqual(new_simple_entity.description, "")

    def test_description_attribute_None(self):
        """testing if description attribute will be converted to an empty
        string if None is given as the description attribute
        """

        self.test_simple_entity.description = None
        self.assertEqual(self.test_simple_entity.description, "")

    def test_description_argument_is_not_a_string_or_unicode(self):
        """testing if a TypeError will be raised when the description argument
        value is not a string or unicode
        """
        self.kwargs['description'] = {'a': 'description'}
        self.assertRaises(TypeError, SimpleEntity, **self.kwargs)

    def test_description_attribute_is_not_a_string_or_unicode(self):
        """testing if a TypeError will be raised when the description attribute
        value is set to a value other than a string or unicide
        """
        self.assertRaises(TypeError, setattr, self.test_simple_entity,
                          'description', ["a description"])

    def test_equality(self):
        """testing the equality of two simple entities
        """
        # create two simple entities with same parameters and check for
        # equality
        simpleEntity1 = SimpleEntity(**self.kwargs)
        simpleEntity2 = SimpleEntity(**self.kwargs)

        self.kwargs["name"] = "a different simple entity"
        self.kwargs["description"] = "no description"
        simpleEntity3 = SimpleEntity(**self.kwargs)
        self.assertTrue(simpleEntity1 == simpleEntity2)
        self.assertFalse(simpleEntity1 == simpleEntity3)

    def test_inequality(self):
        """testing the inequality of two simple entites
        """
        # create two simple entities with same parameters and check for
        # equality
        simpleEntity1 = SimpleEntity(**self.kwargs)
        simpleEntity2 = SimpleEntity(**self.kwargs)

        self.kwargs["name"] = "a different simple entity"
        self.kwargs["description"] = "no description"
        simpleEntity3 = SimpleEntity(**self.kwargs)

        self.assertFalse(simpleEntity1 != simpleEntity2)
        self.assertTrue(simpleEntity1 != simpleEntity3)

    def test_created_by_argument_is_not_a_User_instance(self):
        """testing if TypeError is raised when assigned anything other than a
        stalker.models.user.User object to created_by argument
        """
        # the created_by argument should be an instance of User class, in any
        # other case it should raise a TypeError
        test_value = "A User Name"

        # be sure that the test value is not an instance of User
        self.assertFalse(isinstance(test_value, User))

        # check the value
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "created_by",
            test_value
        )

    def test_created_by_attribute_instance_of_User(self):
        """testing if TypeError is raised when assigned anything other than a
        stalker.models.User object to created_by attribute
        """
        # the created_by attribute should be an instance of User class, in any
        # other case it should raise a TypeError
        test_value = "A User Name"

        # be sure that the test value is not an instance of User
        self.assertFalse(isinstance(test_value, User))

        # check the value
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "created_by",
            test_value
        )

    def test_updated_by_argument_instance_of_User(self):
        """testing if TypeError is raised when assigned anything other than a
        stalker.models.User object to updated_by argument
        """
        # the updated_by argument should be an instance of User class, in any
        # other case it should raise a TypeError
        test_value = "A User Name"

        # be sure that the test value is not an instance of User
        self.assertFalse(isinstance(test_value, User))

        # check the value
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "updated_by",
            test_value
        )

    def test_updated_by_attribute_instance_of_User(self):
        """testing if TypeError is raised when assigned anything other than a
        stalker.models.User object to update_by attribute
        """
        # the updated_by attribute should be an instance of User class, in any
        # other case it should raise a TypeError
        test_value = "A User Name"

        # be sure that the test value is not an instance of User
        self.assertFalse(isinstance(test_value, User))

        # check the value
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "updated_by",
            test_value
        )

    def test_updated_by_argument_empty(self):
        """testing if initializing updated_by with None causes it to be set to
        the same value with created_by argument
        """
        self.kwargs["updated_by"] = None

        aNewSimpleEntity = SimpleEntity(**self.kwargs)

        # now check if they are same
        self.assertEqual(aNewSimpleEntity.created_by,
                         aNewSimpleEntity.updated_by)

    def test_date_created_argument_accepts_datetime_only(self):
        """testing if TypeError raises when the date_created argument is set
        to something else than a datetime.datetime object
        """
        # the date_created argument should be an instance of datetime.datetime
        # try to set something else and expect a TypeError
        test_value = "a string date time 2010-10-26 etc."

        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse(isinstance(test_value, datetime.datetime))

        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_created",
            test_value
        )

    def test_date_created_attribute_accepts_datetime_only(self):
        """testing if TypeError raises when the date_created attribute is set
        to something else than a datetime.datetime object
        """
        # the date_created attribute should be an instance of datetime.datetime
        # try to set something else and expect a TypeError
        test_value = "a string date time 2010-10-26 etc."
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse(isinstance(test_value, datetime.datetime))
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_created",
            test_value
        )

    def test_date_created_attribute_being_empty(self):
        """testing if TypeError is raised when the date_created attribute is
        set to None
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_created",
            None
        )

    def test_date_updated_argument_accepts_datetime_only(self):
        """testing if TypeError raises when the date_updated argument is set
        to something else than a datetime.datetime object
        """
        # try to set it to something else and expect a TypeError
        test_value = "a string date time 2010-10-26 etc."

        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse(isinstance(test_value, datetime.datetime))

        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_updated",
            test_value
        )

    def test_date_updated_attribute_being_datetime(self):
        """testing if TypeError raises when the date_updated attribute is set
        to something else than a datetime.datetime object
        """
        # try to set something else and expect a TypeError
        test_value = "a string date time 2010-10-26 etc."

        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse(isinstance(test_value, datetime.datetime))

        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_updated",
            test_value
        )

    def test_date_updated_attribute_is_set_to_None(self):
        """testing if TypeError is raised when the date_updated attribute is
        set to None
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_updated",
            None
        )

    def test_date_updated_attribute_is_working_properly(self):
        """testing if the date_updated attribute is working properly
        """
        test_value = datetime.datetime.now()
        self.test_simple_entity.date_updated = test_value
        self.assertEqual(self.test_simple_entity.date_updated, test_value)

    def test_date_created_is_before_date_updated(self):
        """testing if a ValueError is going to be raised when trying to set the
        date_updated to a time before date_created
        """
        self.kwargs["date_created"] = datetime.datetime(2000, 1, 1, 1, 1, 1)
        self.kwargs["date_updated"] = datetime.datetime(1990, 1, 1, 1, 1, 1)

        # create a new entity with these dates
        # and expect a ValueError
        self.assertRaises(ValueError, SimpleEntity, **self.kwargs)

    def test___repr__(self):
        """testing the __repr__ works properly
        """
        self.assertEqual(
            self.test_simple_entity.__repr__(),
            "<%s (%s)>" % (
                self.test_simple_entity.name,
                self.test_simple_entity.entity_type,
            )
        )

    def test_type_argument_is_None(self):
        """testing if nothing will happen the type argument is None
        """
        self.kwargs["type"] = None
        new_simple_entity = SimpleEntity(**self.kwargs)

    def test_type_attribute_is_set_to_None(self):
        """testing if nothing will be happened when the type attribute is set to
        None.
        """
        self.test_simple_entity.type = None

    def test_type_argument_accepts_only_Type_instances(self):
        """testing if a TypeError will be raised when the given type attribute
        is not instance of stalker.models.type.Type class
        """
        test_values = [1, 1.2, "a type"]
        for test_value in test_values:
            self.kwargs["type"] = test_value
            self.assertRaises(TypeError, SimpleEntity, **self.kwargs)

    def test_type_argument_accepts_Type_instances(self):
        """testing if no error will be raised when the type argument is given
        as a stalker.models.type.Type instance
        """
        # test with a proper Type
        self.kwargs["type"] = self.test_type
        # no error is expected
        new_simple_entity = SimpleEntity(**self.kwargs)

    def test_type_attribute_accepts_only_Type_instances(self):
        """testing if a TypeError will be raised when the given type attribute
        is not instance of stalker.models.type.Type class
        """
        test_values = [1, 1.2, "a type"]
        for test_value in test_values:
            self.assertRaises(TypeError, setattr, self.test_simple_entity,
                              "type", test_value)

    def test_type_attribute_accepts_Type_instances(self):
        """testing if no error will be raised when the type attribute is given
        as a stalker.models.type.Type instance
        """
        # test with a proper Type
        self.test_simple_entity.type = self.test_type

    def test___strictly_typed___class_attribute_is_init_as_False(self):
        """testing if the __strictly_typed__ class attribute is initialized as
        False
        """
        self.assertEqual(self.test_simple_entity.__strictly_typed__, False)

    def test___strictly_typed___attribute_set_to_True_and_no_type_argument(self):
        """testing if a TypeError will be raised the __strictly_typed__
        attribute is set to true in a derived class but there is no type
        argument defined
        """
        ## create a new class deriving from the SimpleEntity
        #class newClass(SimpleEntity):
        #__strictly_typed__ = True
        self.assertEqual(newClass.__strictly_typed__, True)

        # create a new instance and skip the Type attribute and expect a
        # TypeError
        if self.kwargs.has_key("type"):
            self.kwargs.pop("type")

        self.assertRaises(TypeError, newClass, **self.kwargs)

    def test___strictly_typed___attribute_set_to_True_and_type_argument_is_None(self):
        """testing if a TypeError will be raised the __strictly_typed__
        attribute is set to true in a derived class but the given type argument
        is None
        """
        ## create a new class deriving from the SimpleEntity
        #class newClass(SimpleEntity):
        #__strictly_typed__ = True

        # set it to None and expect a TypeError
        self.kwargs["type"] = None
        self.assertRaises(TypeError, newClass, **self.kwargs)

    def test___strictly_typed___attribute_set_to_True_and_type_argument_is_not_Type(self):
        """testing if a TypeError will be raised the __strictly_typed__
        attribute is set to true in a derived class but the given type argument
        is not a string
        """
        ## create a new class deriving from the SimpleEntity
        #class newClass(SimpleEntity):
        #__strictly_typed__ = True

        test_values = [1, 1.2, ["a", "list"], {"a": "dict"}]

        for test_value in test_values:
            # set it and expect a TypeError
            self.kwargs["type"] = test_value
            self.assertRaises(TypeError, newClass, **self.kwargs)

    def test___stalker_version__attribute_is_automatically_set_to_the_current_task_Stalker(self):
        """testing if the __stalker_version__ is automatically set to the
        current version for the newly created SimpleEntities
        """
        new_simpleEntity = SimpleEntity(**self.kwargs)
        self.assertEqual(new_simpleEntity.__stalker_version__,
                         stalker.__version__)

        # update stalker.__version__ to a test value
        current_version = stalker.__version__

        test_version = "test_version"
        stalker.__version__ = test_version

        # test if it is updated
        self.assertEqual(stalker.__version__, test_version)

        # create a new SimpleEntity and check if it is following the version
        new_simpleEntity2 = SimpleEntity(**self.kwargs)
        self.assertEqual(new_simpleEntity2.__stalker_version__, test_version)

        # restore the stalker.__version__
        stalker.__version__ = current_version

    def test_generic_data_attribute_can_hold_a_wide_variety_of_object_types(self):
        """testing if the generic_data attribute can hold any kind of object as
        a list
        """

        from stalker.db.session import DBSession

        DBSession.remove()
        DBSession.configure(extension=None)
        from stalker import db

        db.setup()

        new_simpleEntity = SimpleEntity(**self.kwargs)
        test_user = User(
            name='email',
            login='email',
            email='email@email.com',
            password='email',
        )

        from stalker import Department

        test_department = Department(
            name='department1'
        )

        from stalker import Repository

        test_repo = Repository(
            name='Test Repository'
        )

        from stalker import Structure

        test_struct = Structure(
            name='Test Project Structure'
        )

        from stalker import Status, StatusList

        test_project_status_list = StatusList(
            name='Project Status List',
            target_entity_type='Project',
            statuses=[
                Status(name='Active', code='ACT')
            ]
        )

        from stalker import Project

        test_proj = Project(
            name='Test Project 1',
            code='tp1',
            repository=test_repo,
            structure=test_struct,
            status_list=test_project_status_list
        )

        new_simpleEntity.generic_data.extend(
            [test_proj, test_project_status_list, test_struct, test_repo,
             test_department, test_user]
        )

        DBSession.add(new_simpleEntity)
        DBSession.commit()

        # now check if it is added to the database correctly
        del new_simpleEntity

        new_simpleEntity_DB = SimpleEntity.query \
            .filter_by(name=self.kwargs['name']) \
            .first()

        self.assertTrue(test_proj in new_simpleEntity_DB.generic_data)
        self.assertTrue(
            test_project_status_list in new_simpleEntity_DB.generic_data)
        self.assertTrue(test_struct in new_simpleEntity_DB.generic_data)
        self.assertTrue(test_repo in new_simpleEntity_DB.generic_data)
        self.assertTrue(test_department in new_simpleEntity_DB.generic_data)
        self.assertTrue(test_user in new_simpleEntity_DB.generic_data)

        DBSession.remove()
        DBSession.configure(extension=None)

    def test_thumbnail_argument_is_skipped(self):
        """testing if the thumbnail attribute will be None when the thumbnail
        argument is skipped
        """
        try:
            self.kwargs.pop('thumbnail')
        except KeyError:
            pass

        new_simple_entity = SimpleEntity(**self.kwargs)
        self.assertIsNone(new_simple_entity.thumbnail)

    def test_thumbnail_argument_is_None(self):
        """testing if the thumbnail argument can be None
        """
        self.kwargs['thumbnail'] = None
        new_simple_entity = SimpleEntity(**self.kwargs)
        self.assertIsNone(new_simple_entity.thumbnail)

    def test_thumbnail_attribute_is_None(self):
        """testing if the thumbnail attribute can be set to None
        """
        self.test_simple_entity.thumbnail = None
        self.assertEqual(self.test_simple_entity.thumbnail, None)

    def test_thumbnail_argument_is_not_a_Link_instance(self):
        """testing if a TypeError will be raised when the thumbnail argument is
        not a Link instance
        """
        self.kwargs['thumbnail'] = 'not a Link'
        self.assertRaises(TypeError, SimpleEntity, **self.kwargs)

    def test_thumbnail_attribute_is_not_a_Link_instance(self):
        """testing if a TypeError will be raised when the thumbnail attribute
        is set to something other than a Link instance (and None)
        """
        self.assertRaises(TypeError, setattr, self.test_simple_entity,
                          'thumbnail', 'not a Link')

    def test_thumbnail_argument_is_working_properly(self):
        """testing if the thumbnail argument value is passed to the thumbnail
        attribute correctly
        """
        from stalker import Link

        thumb = Link(full_path='some path')
        self.kwargs['thumbnail'] = thumb
        new_simple_entity = SimpleEntity(**self.kwargs)
        self.assertEqual(new_simple_entity.thumbnail, thumb)

    def test_thumbnail_attribute_is_working_properly(self):
        """testing if the thumbnail attribute is working properly
        """
        from stalker import Link

        thumb = Link(full_path='some path')
        self.assertNotEqual(self.test_simple_entity.thumbnail, thumb)
        self.test_simple_entity.thumbnail = thumb
        self.assertEqual(self.test_simple_entity.thumbnail, thumb)
