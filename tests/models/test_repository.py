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

import platform
import mocker
import unittest2
from stalker import Repository, Tag


class RepositoryTester(unittest2.TestCase):
    """tests the Repository class
    """

    def setUp(self):
        """setup the test
        """
        # create a couple of test tags
        self.test_tag1 = Tag(name="test tag 1")
        self.test_tag2 = Tag(name="test tag 2")

        self.kwargs = {
            "name": "a repository",
            "description": "this is for testing purposes",
            "tags": [self.test_tag1, self.test_tag2],
            "linux_path": "/mnt/M/Projects",
            "osx_path": "/Volumes/M/Projects",
            "windows_path": "M:/Projects"
        }

        self.test_repo = Repository(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Repository class
        """
        self.assertFalse(Repository.__auto_name__)

    def test_linux_path_argument_accepts_only_strings(self):
        """testing if linux_path argument accepts only string or unicode
        values
        """
        test_values = [123123, 123.1231, [], {}]
        for test_value in test_values:
            self.kwargs["linux_path"] = test_value
            self.assertRaises(TypeError, Repository, **self.kwargs)

    def test_linux_path_attribute_accepts_only_strings(self):
        """testing if linux_path attribute accepts only string or unicode
        values
        """
        test_values = [123123, 123.1231, [], {}]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_repo,
                "linux_path",
                test_value
            )

    def test_linux_path_attribute_is_working_properly(self):
        """testing if linux_path attribute is working properly
        """
        test_value = "~/newRepoPath/Projects/"
        self.test_repo.linux_path = test_value
        self.assertEqual(self.test_repo.linux_path, test_value)

    def test_linux_path_attribute_finishes_with_a_slash(self):
        """testing if the linux_path attribute will be finished with a slash
        even it is not supplied by default
        """
        test_value = '/mnt/T'
        expected_value = '/mnt/T/'
        self.test_repo.linux_path = test_value
        self.assertEqual(self.test_repo.linux_path, expected_value)

    def test_windows_path_argument_accepts_only_strings(self):
        """testing if windows_path argument accepts only string or unicode
        values
        """
        test_values = [123123, 123.1231, [], {}]
        for test_value in test_values:
            self.kwargs["windows_path"] = test_value
            self.assertRaises(TypeError, Repository, **self.kwargs)

    def test_windows_path_attribute_accepts_only_strings(self):
        """testing if windows_path attribute accepts only string or unicode
        values
        """
        test_values = [123123, 123.1231, [], {}]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_repo,
                "windows_path",
                test_value
            )

    def test_windows_path_attribute_is_working_properly(self):
        """testing if windows_path attribute is working properly
        """
        test_value = "~/newRepoPath/Projects/"
        self.test_repo.windows_path = test_value
        self.assertEqual(self.test_repo.windows_path, test_value)

    def test_windows_path_attribute_finishes_with_a_slash(self):
        """testing if the windows_path attribute will be finished with a slash
        even it is not supplied by default
        """
        test_value = 'T:'
        expected_value = 'T:/'
        self.test_repo.windows_path = test_value
        self.assertEqual(self.test_repo.windows_path, expected_value)

    def test_osx_path_argument_accepts_only_strings(self):
        """testing if osx_path argument accepts only string or unicode
        values
        """
        test_values = [123123, 123.1231, [], {}]
        for test_value in test_values:
            self.kwargs["osx_path"] = test_value
            self.assertRaises(TypeError, Repository, **self.kwargs)

    def test_osx_path_attribute_accepts_only_strings(self):
        """testing if osx_path attribute accepts only string or unicode
        values
        """
        test_values = [123123, 123.1231, [], {}]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_repo,
                "osx_path",
                test_value
            )

    def test_osx_path_attribute_is_working_properly(self):
        """testing if osx_path attribute is working properly
        """
        test_value = "~/newRepoPath/Projects/"
        self.test_repo.osx_path = test_value
        self.assertEqual(self.test_repo.osx_path, test_value)

    def test_osx_path_attribute_finishes_with_a_slash(self):
        """testing if the osx_path attribute will be finished with a slash
        even it is not supplied by default
        """
        test_value = '/Volumes/T'
        expected_value = '/Volumes/T/'
        self.test_repo.osx_path = test_value
        self.assertEqual(self.test_repo.osx_path, expected_value)

    def test_path_returns_properly_for_windows(self):
        """testing if path returns the correct value for the os
        """
        m1 = mocker.Mocker()
        o = m1.replace(platform.system)
        o()
        m1.result("Windows")
        m1.replay()
        self.assertEqual(self.test_repo.path, self.test_repo.windows_path)
        m1.restore()

    def test_path_returns_properly_for_linux(self):
        """testing if path returns the correct value for the os
        """
        m1 = mocker.Mocker()
        o = m1.replace(platform.system)
        o()
        m1.result("Linux")
        m1.replay()
        self.assertEqual(self.test_repo.path, self.test_repo.linux_path)
        m1.restore()

    def test_path_returns_properly_for_osx(self):
        """testing if path returns the correct value for the os
        """
        m1 = mocker.Mocker()
        o = m1.replace(platform.system)
        o()
        m1.result("Darwin")
        m1.replay()
        self.assertEqual(self.test_repo.path, self.test_repo.osx_path)
        m1.restore()

    def test_equality(self):
        """testing the equality of two repositories
        """
        repo1 = Repository(**self.kwargs)
        repo2 = Repository(**self.kwargs)

        self.kwargs.update({
            "name": "a repository",
            "description": "this is the commercial repository",
            "linux_path": "/mnt/commercialServer/Projects",
            "osx_path": "/Volumes/commercialServer/Projects",
            "windows_path": "Z:\\Projects"
        })

        repo3 = Repository(**self.kwargs)

        self.assertTrue(repo1 == repo2)
        self.assertFalse(repo1 == repo3)

    def test_inequality(self):
        """testing the inequality of two repositories
        """
        repo1 = Repository(**self.kwargs)
        repo2 = Repository(**self.kwargs)

        self.kwargs.update({
            "name": "a repository",
            "description": "this is the commercial repository",
            "linux_path": "/mnt/commercialServer/Projects",
            "osx_path": "/Volumes/commercialServer/Projects",
            "windows_path": "Z:\\Projects"
        })

        repo3 = Repository(**self.kwargs)

        self.assertFalse(repo1 != repo2)
        self.assertTrue(repo1 != repo3)

    def test_plural_class_name(self):
        """testing the plural name of Repository class
        """
        self.assertTrue(self.test_repo.plural_class_name, "Repositories")

    def test_linux_path_argument_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the linux_path argument
        """
        self.kwargs["linux_path"] = r"\mnt\M\Projects"
        new_repo = Repository(**self.kwargs)

        self.assertNotIn("\\", new_repo.linux_path)
        self.assertEqual(new_repo.linux_path, "/mnt/M/Projects/")

    def test_linux_path_attribute_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the linux_path attribute
        """
        self.test_repo.linux_path = r"\mnt\M\Projects"
        self.assertNotIn("\\", self.test_repo.linux_path)
        self.assertEqual(self.test_repo.linux_path, "/mnt/M/Projects/")

    def test_osx_path_argument_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the osx_path argument
        """
        self.kwargs["osx_path"] = r"\Volumes\M\Projects"
        new_repo = Repository(**self.kwargs)

        self.assertNotIn("\\", new_repo.linux_path)
        self.assertEqual(new_repo.osx_path, "/Volumes/M/Projects/")

    def test_osx_path_attribute_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the osx_path attribute
        """
        self.test_repo.osx_path = r"\Volumes\M\Projects"
        self.assertNotIn("\\", self.test_repo.osx_path)
        self.assertEqual(self.test_repo.osx_path, "/Volumes/M/Projects/")

    def test_windows_path_argument_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the windows_path argument
        """
        self.kwargs["windows_path"] = r"M:\Projects"
        new_repo = Repository(**self.kwargs)

        self.assertNotIn("\\", new_repo.linux_path)
        self.assertEqual(new_repo.windows_path, "M:/Projects/")

    def test_windows_path_attribute_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the windows_path attribute
        """
        self.test_repo.windows_path = r"M:\Projects"
        self.assertNotIn("\\", self.test_repo.windows_path)
        self.assertEqual(self.test_repo.windows_path, "M:/Projects/")

    def test_to_linux_path_returns_the_linux_version_of_the_given_windows_path(self):
        """testing if the to_linux_path returns the linux version of the given
        windows path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/' \
                            'Some_file.ma'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        self.assertEqual(
            self.test_repo.to_linux_path(test_windows_path),
            test_linux_path
        )

    def test_to_linux_path_returns_the_linux_version_of_the_given_linux_path(self):
        """testing if the to_linux_path returns the linux version of the given
        linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        self.assertEqual(
            self.test_repo.to_linux_path(test_linux_path),
            test_linux_path
        )

    def test_to_linux_path_returns_the_linux_version_of_the_given_osx_path(self):
        """testing if the to_linux_path returns the linux version of the given
        osx path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        self.assertEqual(
            self.test_repo.to_linux_path(test_osx_path),
            test_linux_path
        )

    def test_to_linux_path_returns_the_linux_version_of_the_given_reverse_windows_path(self):
        """testing if the to_linux_path returns the linux version of the given
        reverse windows path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_windows_path_reverse = 'T:\\Stalker_Projects\\Sero\\Task1\\' \
                                    'Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_linux_path(test_windows_path_reverse),
            test_linux_path
        )

    def test_to_linux_path_returns_the_linux_version_of_the_given_reverse_linux_path(self):
        """testing if the to_linux_path returns the linux version of the given
        reverse linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_linux_path(test_linux_path_reverse),
            test_linux_path
        )

    def test_to_linux_path_returns_the_linux_version_of_the_given_reverse_osx_path(self):
        """testing if the to_linux_path returns the linux version of the given
        reverse osx path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_linux_path(test_osx_path_reverse),
            test_linux_path
        )

    def test_to_linux_path_raises_TypeError_if_path_is_None(self):
        """testing if to_linux_path raises TypeError if path is None
        """
        self.assertRaises(TypeError, self.test_repo.to_linux_path, None)

    def test_to_linux_path_raises_TypeError_if_path_is_not_a_string(self):
        """testing if to_linux_path raises TypeError if path is None
        """
        self.assertRaises(TypeError, self.test_repo.to_linux_path, 123)

    def test_to_windows_path_returns_the_windows_version_of_the_given_windows_path(self):
        """testing if the to_windows_path returns the windows version of the
        given windows path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.assertEqual(
            self.test_repo.to_windows_path(test_windows_path),
            test_windows_path
        )

    def test_to_windows_path_returns_the_windows_version_of_the_given_linux_path(self):
        """testing if the to_windows_path returns the windows version of the
        given linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.assertEqual(
            self.test_repo.to_windows_path(test_linux_path),
            test_windows_path
        )

    def test_to_windows_path_returns_the_windows_version_of_the_given_osx_path(self):
        """testing if the to_windows_path returns the windows version of the
        given osx path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.assertEqual(
            self.test_repo.to_windows_path(test_osx_path),
            test_windows_path
        )

    def test_to_windows_path_returns_the_windows_version_of_the_given_reverse_windows_path(self):
        """testing if the to_windows_path returns the windows version of the
        given reverse windows path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        test_windows_path_reverse = 'T:\\Stalker_Projects\\Sero\\Task1\\' \
                                    'Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_windows_path(test_windows_path_reverse),
            test_windows_path
        )

    def test_to_windows_path_returns_the_windows_version_of_the_given_reverse_linux_path(self):
        """testing if the to_windows_path returns the windows version of the
        given reverse linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_windows_path(test_linux_path_reverse),
            test_windows_path
        )

    def test_to_windows_path_returns_the_windows_version_of_the_given_reverse_osx_path(self):
        """testing if the to_windows_path returns the windows version of the
        given reverse osx path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_windows_path(test_osx_path_reverse),
            test_windows_path
        )

    def test_to_windows_path_raises_TypeError_if_path_is_None(self):
        """testing if to_windows_path raises TypeError if path is None
        """
        self.assertRaises(TypeError, self.test_repo.to_windows_path, None)

    def test_to_windows_path_raises_TypeError_if_path_is_not_a_string(self):
        """testing if to_windows_path raises TypeError if path is None
        """
        self.assertRaises(TypeError, self.test_repo.to_windows_path, 123)

    def test_to_osx_path_returns_the_osx_version_of_the_given_windows_path(self):
        """testing if the to_osx_path returns the osx version of the given
        windows path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        self.assertEqual(
            self.test_repo.to_osx_path(test_windows_path),
            test_osx_path
        )

    def test_to_osx_path_returns_the_osx_version_of_the_given_linux_path(self):
        """testing if the to_osx_path returns the osx version of the given
        linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        self.assertEqual(
            self.test_repo.to_osx_path(test_linux_path),
            test_osx_path
        )

    def test_to_osx_path_returns_the_osx_version_of_the_given_osx_path(self):
        """testing if the to_osx_path returns the osx version of the given
        osx path
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        self.assertEqual(
            self.test_repo.to_osx_path(test_osx_path),
            test_osx_path
        )

    def test_to_osx_path_returns_the_osx_version_of_the_given_reverse_windows_path(self):
        """testing if the to_osx_path returns the osx version of the given
        reverse windows path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        test_windows_path_reverse = 'T:\\Stalker_Projects\\Sero\\Task1\\' \
                                    'Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_osx_path(test_windows_path_reverse),
            test_osx_path
        )

    def test_to_osx_path_returns_the_osx_version_of_the_given_reverse_linux_path(self):
        """testing if the to_osx_path returns the osx version of the given
        reverse linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_osx_path(test_linux_path_reverse),
            test_osx_path
        )

    def test_to_osx_path_returns_the_osx_version_of_the_given_reverse_osx_path(self):
        """testing if the to_osx_path returns the osx version of the given
        reverse osx path
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_osx_path(test_osx_path_reverse),
            test_osx_path
        )

    def test_to_osx_path_returns_the_osx_version_of_the_given_path(self):
        """testing if the to_osx_path returns the osx version of the
        given path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'

        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/' \
                            'Some_file.ma'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'

        test_windows_path_reverse = 'T:\\Stalker_Projects\\Sero\\Task1\\' \
                                    'Task2\\Some_file.ma'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'

        self.assertEqual(
            self.test_repo.to_osx_path(test_windows_path),
            test_osx_path
        )

        self.assertEqual(
            self.test_repo.to_osx_path(test_linux_path),
            test_osx_path
        )

        self.assertEqual(
            self.test_repo.to_osx_path(test_osx_path),
            test_osx_path
        )

        self.assertEqual(
            self.test_repo.to_osx_path(test_windows_path_reverse),
            test_osx_path
        )

        self.assertEqual(
            self.test_repo.to_osx_path(test_linux_path_reverse),
            test_osx_path
        )

        self.assertEqual(
            self.test_repo.to_osx_path(test_osx_path_reverse),
            test_osx_path
        )

    def test_to_osx_path_raises_TypeError_if_path_is_None(self):
        """testing if to_osx_path raises TypeError if path is None
        """
        self.assertRaises(TypeError, self.test_repo.to_osx_path, None)

    def test_to_osx_path_raises_TypeError_if_path_is_not_a_string(self):
        """testing if to_osx_path raises TypeError if path is None
        """
        self.assertRaises(TypeError, self.test_repo.to_osx_path, 123)

    def test_to_native_path_returns_the_native_version_of_the_given_linux_path(self):
        """testing if the to_native_path returns the native version of the
        given linux path
        """
        m1 = mocker.Mocker()
        o = m1.replace(platform.system)
        o()
        m1.result("Linux")
        m1.replay()

        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'

        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'

        self.assertEqual(
            self.test_repo.to_native_path(test_linux_path),
            test_linux_path
        )
        m1.restore()

    def test_to_native_path_returns_the_native_version_of_the_given_windows_path(self):
        """testing if the to_native_path returns the native version of the
        given windows path
        """
        m1 = mocker.Mocker()
        o = m1.replace(platform.system)
        o()
        m1.result("Linux")
        m1.replay()

        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'

        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'

        self.assertEqual(
            self.test_repo.to_native_path(test_windows_path),
            '/mnt/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        )
        m1.restore()

    def test_to_native_path_returns_the_native_version_of_the_given_osx_path(self):
        """testing if the to_native_path returns the native version of the
        given osx path
        """
        m1 = mocker.Mocker()
        o = m1.replace(platform.system)
        o()
        m1.result("Linux")
        m1.replay()

        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        self.assertEqual(
            self.test_repo.to_native_path(test_osx_path),
            test_linux_path
        )
        m1.restore()

    def test_to_native_path_returns_the_native_version_of_the_given_reverse_windows_path(self):
        """testing if the to_native_path returns the native version of the
        given reverse windows path
        """
        m1 = mocker.Mocker()
        o = m1.replace(platform.system)
        o()
        m1.result("Linux")
        m1.replay()

        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_windows_path_reverse = 'T:\\Stalker_Projects\\Sero\\Task1\\' \
                                    'Task2\\Some_file.ma'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        self.assertEqual(
            self.test_repo.to_native_path(test_windows_path_reverse),
            test_linux_path
        )
        m1.restore()

    def test_to_native_path_returns_the_native_version_of_the_given_reverse_linux_path(self):
        """testing if the to_native_path returns the native version of the
        given reverse linux path
        """
        m1 = mocker.Mocker()
        o = m1.replace(platform.system)
        o()
        m1.result("Linux")
        m1.replay()

        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_native_path(test_linux_path_reverse),
            test_linux_path
        )
        m1.restore()

    def test_to_native_path_returns_the_native_version_of_the_given_reverse_osx_path(self):
        """testing if the to_native_path returns the native version of the
        given reverse osx path
        """
        m1 = mocker.Mocker()
        o = m1.replace(platform.system)
        o()
        m1.result("Linux")
        m1.replay()

        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'
        self.assertEqual(
            self.test_repo.to_native_path(test_osx_path_reverse),
            test_linux_path
        )
        m1.restore()

    def test_to_native_path_raises_TypeError_if_path_is_None(self):
        """testing if to_native_path raises TypeError if path is None
        """
        self.assertRaises(TypeError, self.test_repo.to_native_path, None)

    def test_to_native_path_raises_TypeError_if_path_is_not_a_string(self):
        """testing if to_native_path raises TypeError if path is None
        """
        self.assertRaises(TypeError, self.test_repo.to_native_path, 123)

    def test_is_in_repo_returns_True_if_the_given_linux_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given linux path is in
        this repo or False otherwise
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        self.assertTrue(self.test_repo.is_in_repo(test_linux_path))

    def test_is_in_repo_returns_True_if_the_given_linux_reverse_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given linux reverse path
        is in this repo or False otherwise
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        self.assertTrue(self.test_repo.is_in_repo(test_linux_path_reverse))

    def test_is_in_repo_returns_False_if_the_given_linux_path_is_not_in_this_repo(self):
        """testing if is_in_repo returns False if the given linux path is not
        in this repo or False otherwise
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_not_in_path_linux_path = '/mnt/T/Other_Projects/Sero/Task1/' \
                                      'Task2/Some_file.ma'
        self.assertFalse(
            self.test_repo.is_in_repo(test_not_in_path_linux_path))

    def test_is_in_repo_returns_True_if_the_given_windows_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given windows path is in
        this repo or False otherwise
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.assertTrue(self.test_repo.is_in_repo(test_windows_path))

    def test_is_in_repo_returns_True_if_the_given_windows_reverse_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given windows reverse path
        is in this repo or False otherwise
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path_reverse = 'T:\\Stalker_Projects\\Sero\\Task1\\' \
                                    'Task2\\Some_file.ma'
        self.assertTrue(self.test_repo.is_in_repo(test_windows_path_reverse))

    def test_is_in_repo_returns_False_if_the_given_windows_path_is_not_in_this_repo(self):
        """testing if is_in_repo returns False if the given windows path is not
        in this repo or False otherwise
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_not_in_path_windows_path = 'T:/Other_Projects/Sero/Task1/Task2/' \
                                        'Some_file.ma'
        self.assertFalse(
            self.test_repo.is_in_repo(test_not_in_path_windows_path))

    def test_is_in_repo_returns_True_if_the_given_osx_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given osx path is in
        this repo or False otherwise
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        self.assertTrue(self.test_repo.is_in_repo(test_osx_path))

    def test_is_in_repo_returns_True_if_the_given_osx_reverse_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given osx reverse path
        is in this repo or False otherwise
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'
        self.assertTrue(self.test_repo.is_in_repo(test_osx_path_reverse))

    def test_is_in_repo_returns_False_if_the_given_osx_path_is_not_in_this_repo(self):
        """testing if is_in_repo returns False if the given osx path is not
        in this repo or False otherwise
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_not_in_path_osx_path = '/Volumes/T/Other_Projects/Sero/Task1/' \
                                    'Task2/Some_file.ma'
        self.assertFalse(self.test_repo.is_in_repo(test_not_in_path_osx_path))







