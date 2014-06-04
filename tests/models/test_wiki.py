# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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

import unittest
from stalker import Type, Repository, Status, StatusList, Project
from stalker.models.wiki import Page


class PageTester(unittest.TestCase):
    """Tests stalker.wiki.Page class
    """

    def setUp(self):
        """setting up the test
        """
        # create a repository
        self.repository_type = Type(
            name="Test Repository Type",
            code='test_repo',
            target_entity_type=Repository
        )

        self.test_repository = Repository(
            name="Test Repository",
            type=self.repository_type,
        )

        # statuses
        self.status1 = Status(name="Status1", code="STS1")
        self.status2 = Status(name="Status2", code="STS2")
        self.status3 = Status(name="Status3", code="STS3")

        # project status list
        self.project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.status1,
                self.status2,
                self.status3,
            ],
            target_entity_type=Project
        )

        # project type
        self.test_project_type = Type(
            name="Test Project Type",
            code='testproj',
            target_entity_type=Project,
        )

        # create projects
        self.test_project1 = Project(
            name="Test Project 1",
            code='tp1',
            type=self.test_project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )

        self.kwargs = {
            'title': 'Test Page Title',
            'content': 'Test content',
            'project': self.test_project1
        }

        self.test_page = Page(**self.kwargs)

    def test_title_argument_is_skipped(self):
        """testing if a ValueError will be raised when the title argument is
        skipped
        """
        self.kwargs.pop('title')
        with self.assertRaises(ValueError) as cm:
            Page(**self.kwargs)

        self.assertEqual(
            'Page.title can not be empty',
            str(cm.exception)
        )

    def test_title_argument_is_None(self):
        """testing if a TypeError will be raised when the title argument is
        None
        """
        self.kwargs['title'] = None
        with self.assertRaises(TypeError) as cm:
            Page(**self.kwargs)

        self.assertEqual(
            'Page.title should be a string, not NoneType',
            str(cm.exception)
        )

    def test_title_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the title attribute is
        set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_page.title = None

        self.assertEqual(
            'Page.title should be a string, not NoneType',
            str(cm.exception)
        )

    def test_title_argument_is_an_empty_string(self):
        """testing if a ValueError will be raised when the title argument is
        an empty string
        """
        self.kwargs['title'] = ''
        with self.assertRaises(ValueError) as cm:
            Page(**self.kwargs)

        self.assertEqual(
            'Page.title can not be empty',
            str(cm.exception)
        )

    def test_title_attribute_is_set_to_empty_string(self):
        """testing if a ValueError will be raised when the title attribute is
        set to empty string
        """
        with self.assertRaises(ValueError) as cm:
            self.test_page.title = ''

        self.assertEqual(
            'Page.title can not be empty',
            str(cm.exception)
        )

    def test_title_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the title argument is not
        a string
        """
        self.kwargs['title'] = 2165
        with self.assertRaises(TypeError) as cm:
            Page(**self.kwargs)

        self.assertEqual(
            'Page.title should be a string, not int',
            str(cm.exception)
        )

    def test_title_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the title is set to a
        value other than a string
        """
        with self.assertRaises(TypeError) as cm:
            self.test_page.title = 2135

        self.assertEqual(
            'Page.title should be a string, not int',
            str(cm.exception)
        )

    def test_title_argument_is_working_properly(self):
        """testing if the title argument value is correctly passed to title
        attribute
        """
        self.assertEqual(
            self.kwargs['title'],
            self.test_page.title
        )

    def test_title_attribute_is_working_properly(self):
        """testing if the title attribute is working properly
        """
        test_value = 'Test Title 2'
        self.test_page.title = test_value
        self.assertEqual(
            test_value,
            self.test_page.title
        )

    def test_content_argument_skipped(self):
        """testing if the content attribute value will be an empty string if
        the content argument is skipped
        """
        self.kwargs.pop('content')
        new_page = Page(**self.kwargs)
        self.assertEqual(new_page.content, '')

    def test_content_argument_is_None(self):
        """testing if the content attribute value will be an empty string if
        the content argument is None
        """
        self.kwargs['content'] = None
        new_page = Page(**self.kwargs)
        self.assertEqual(new_page.content, '')

    def test_content_attribute_is_set_to_None(self):
        """testing if the content attribute value will be an empty string if
        the content attribute is set to None
        """
        self.assertNotEqual('', self.test_page.content)
        self.test_page.content = None
        self.assertEqual('', self.test_page.content)

    def test_content_argument_is_empty_string(self):
        """testing if the content attribute value will be an empty string if
        the content argument is an empty string
        """
        self.kwargs['content'] = ''
        new_page = Page(**self.kwargs)
        self.assertEqual(new_page.content, '')

    def test_content_attribute_is_set_to_an_empty_string(self):
        """testing if the content attribute can be set to an empty string
        """
        self.test_page.content = ''
        self.assertEqual('', self.test_page.content)

    def test_content_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the content argument is
        not a string
        """
        self.kwargs['content'] = 1234
        with self.assertRaises(TypeError) as cm:
            Page(**self.kwargs)

        self.assertEqual(
            'Page.content should be a string, not int',
            str(cm.exception)
        )

    def test_content_attribute_is_set_to_a_value_other_than_a_string(self):
        """testing if a TypeError will be raised when the content attribute is
        set to a value other than a string
        """
        with self.assertRaises(TypeError) as cm:
            self.test_page.content = ['not', 'a', 'string']
        self.assertEqual(
            'Page.content should be a string, not list',
            str(cm.exception)
        )

    def test_content_argument_is_working_properly(self):
        """testing if content argument value is correctly passed to the content
        attribute
        """
        self.assertEqual(
            self.kwargs['content'],
            self.test_page.content
        )

    def test_content_attribute_is_working_properly(self):
        """testing if the content attribute value can be correctly set
        """
        test_value = 'This is a test content'
        self.assertNotEqual(
            test_value,
            self.test_page.content
        )
        self.test_page.content = test_value
        self.assertEqual(
            test_value,
            self.test_page.content
        )
