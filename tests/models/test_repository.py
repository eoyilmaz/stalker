# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import platform
import unittest
from stalker import Repository, Tag

class RepositoryTester(unittest.TestCase):
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

    def test_linux_path_attribute_works_properly(self):
        """testing if linux_path attribute works properly
        """
        test_value = "~/newRepoPath/Projects"
        self.test_repo.linux_path = test_value
        self.assertEqual(self.test_repo.linux_path, test_value)

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

    def test_windows_path_attribute_works_properly(self):
        """testing if windows_path attribute works properly
        """
        test_value = "~/newRepoPath/Projects"
        self.test_repo.windows_path = test_value
        self.assertEqual(self.test_repo.windows_path, test_value)

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

    def test_osx_path_attribute_works_properly(self):
        """testing if osx_path attribute works properly
        """
        test_value = "~/newRepoPath/Projects"
        self.test_repo.osx_path = test_value
        self.assertEqual(self.test_repo.osx_path, test_value)

    @unittest.skipUnless(platform.system() == "Windows", "requires Windows")
    def test_path_returns_properly_for_windows(self):
        """testing if path returns the correct value for the os
        """
        self.assertEqual(self.test_repo.path, self.test_repo.windows_path)

    @unittest.skipUnless(platform.system() == "Linux", "requires Linux")
    def test_path_returns_properly_for_linux(self):
        """testing if path returns the correct value for the os
        """
        self.assertEqual(self.test_repo.path, self.test_repo.linux_path)

    @unittest.skipUnless(platform.system() == "Darwin", "requires OSX")
    def test_path_returns_properly_for_osx(self):
        """testing if path returns the correct value for the os
        """
        self.assertEqual(self.test_repo.path, self.test_repo.osx_path)

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

        #def test_plural_name(self):
        #"""testing the plural name of Repository class
        #"""
        #self.assertTrue(Repository.plural_name, "Repositories")

    def test_linux_path_argument_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the linux_path argument
        """
        self.kwargs["linux_path"] = r"\mnt\M\Projects"
        new_repo = Repository(**self.kwargs)

        self.assertNotIn("\\", new_repo.linux_path)
        self.assertEqual(new_repo.linux_path, "/mnt/M/Projects")

    def test_linux_path_attribute_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the linux_path attribute
        """
        self.test_repo.linux_path = r"\mnt\M\Projects"
        self.assertNotIn("\\", self.test_repo.linux_path)
        self.assertEqual(self.test_repo.linux_path, "/mnt/M/Projects")

    def test_osx_path_argument_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the osx_path argument
        """
        self.kwargs["osx_path"] = r"\Volumes\M\Projects"
        new_repo = Repository(**self.kwargs)

        self.assertNotIn("\\", new_repo.linux_path)
        self.assertEqual(new_repo.osx_path, "/Volumes/M/Projects")

    def test_osx_path_attribute_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the osx_path attribute
        """
        self.test_repo.osx_path = r"\Volumes\M\Projects"
        self.assertNotIn("\\", self.test_repo.osx_path)
        self.assertEqual(self.test_repo.osx_path, "/Volumes/M/Projects")

    def test_windows_path_argument_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the windows_path argument
        """
        self.kwargs["windows_path"] = r"M:\Projects"
        new_repo = Repository(**self.kwargs)

        self.assertNotIn("\\", new_repo.linux_path)
        self.assertEqual(new_repo.windows_path, "M:/Projects")

    def test_windows_path_attribute_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the windows_path attribute
        """
        self.test_repo.windows_path = r"M:\Projects"
        self.assertNotIn("\\", self.test_repo.windows_path)
        self.assertEqual(self.test_repo.windows_path, "M:/Projects")
