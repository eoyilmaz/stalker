# -*- coding: utf-8 -*-

import unittest

import pytest

from stalker import Page


class PageTester(unittest.TestCase):
    """Tests stalker.wiki.Page class
    """

    def setUp(self):
        """setting up the test
        """
        super(PageTester, self).setUp()

        # create a repository
        from stalker import Type
        self.repository_type = Type(
            name="Test Repository Type",
            code='test_repo',
            target_entity_type='Repository'
        )

        from stalker import Repository
        self.test_repository = Repository(
            name="Test Repository",
            code="TR",
            type=self.repository_type,
        )

        # statuses
        from stalker import Status
        self.status1 = Status(name="Status1", code="STS1")
        self.status2 = Status(name="Status2", code="STS2")
        self.status3 = Status(name="Status3", code="STS3")

        # project status list
        from stalker import StatusList
        self.project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.status1,
                self.status2,
                self.status3,
            ],
            target_entity_type='Project'
        )

        # project type
        self.test_project_type = Type(
            name="Test Project Type",
            code='testproj',
            target_entity_type='Project',
        )

        # create projects
        from stalker import Project
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
        with pytest.raises(ValueError) as cm:
            Page(**self.kwargs)

        assert str(cm.value) == 'Page.title can not be empty'

    def test_title_argument_is_None(self):
        """testing if a TypeError will be raised when the title argument is
        None
        """
        self.kwargs['title'] = None
        with pytest.raises(TypeError) as cm:
            Page(**self.kwargs)

        assert str(cm.value) == 'Page.title should be a string, not NoneType'

    def test_title_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the title attribute is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_page.title = None

        assert str(cm.value) == 'Page.title should be a string, not NoneType'

    def test_title_argument_is_an_empty_string(self):
        """testing if a ValueError will be raised when the title argument is
        an empty string
        """
        self.kwargs['title'] = ''
        with pytest.raises(ValueError) as cm:
            Page(**self.kwargs)

        assert str(cm.value) == 'Page.title can not be empty'

    def test_title_attribute_is_set_to_empty_string(self):
        """testing if a ValueError will be raised when the title attribute is
        set to empty string
        """
        with pytest.raises(ValueError) as cm:
            self.test_page.title = ''

        assert str(cm.value) == 'Page.title can not be empty'

    def test_title_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the title argument is not
        a string
        """
        self.kwargs['title'] = 2165
        with pytest.raises(TypeError) as cm:
            Page(**self.kwargs)

        assert str(cm.value) == 'Page.title should be a string, not int'

    def test_title_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the title is set to a
        value other than a string
        """
        with pytest.raises(TypeError) as cm:
            self.test_page.title = 2135

        assert str(cm.value) == 'Page.title should be a string, not int'

    def test_title_argument_is_working_properly(self):
        """testing if the title argument value is correctly passed to title
        attribute
        """
        assert self.test_page.title == self.kwargs['title']

    def test_title_attribute_is_working_properly(self):
        """testing if the title attribute is working properly
        """
        test_value = 'Test Title 2'
        self.test_page.title = test_value
        assert self.test_page.title == test_value

    def test_content_argument_skipped(self):
        """testing if the content attribute value will be an empty string if
        the content argument is skipped
        """
        self.kwargs.pop('content')
        new_page = Page(**self.kwargs)
        assert new_page.content == ''

    def test_content_argument_is_None(self):
        """testing if the content attribute value will be an empty string if
        the content argument is None
        """
        self.kwargs['content'] = None
        new_page = Page(**self.kwargs)
        assert new_page.content == ''

    def test_content_attribute_is_set_to_None(self):
        """testing if the content attribute value will be an empty string if
        the content attribute is set to None
        """
        assert self.test_page.content != ''
        self.test_page.content = None
        assert self.test_page.content == ''

    def test_content_argument_is_empty_string(self):
        """testing if the content attribute value will be an empty string if
        the content argument is an empty string
        """
        self.kwargs['content'] = ''
        new_page = Page(**self.kwargs)
        assert new_page.content == ''

    def test_content_attribute_is_set_to_an_empty_string(self):
        """testing if the content attribute can be set to an empty string
        """
        self.test_page.content = ''
        assert self.test_page.content == ''

    def test_content_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the content argument is
        not a string
        """
        self.kwargs['content'] = 1234
        with pytest.raises(TypeError) as cm:
            Page(**self.kwargs)

        assert str(cm.value) == 'Page.content should be a string, not int'

    def test_content_attribute_is_set_to_a_value_other_than_a_string(self):
        """testing if a TypeError will be raised when the content attribute is
        set to a value other than a string
        """
        with pytest.raises(TypeError) as cm:
            self.test_page.content = ['not', 'a', 'string']
        assert str(cm.value) == 'Page.content should be a string, not list'

    def test_content_argument_is_working_properly(self):
        """testing if content argument value is correctly passed to the content
        attribute
        """
        assert self.test_page.content == self.kwargs['content']

    def test_content_attribute_is_working_properly(self):
        """testing if the content attribute value can be correctly set
        """
        test_value = 'This is a test content'
        assert self.test_page.content != test_value
        self.test_page.content = test_value
        assert self.test_page.content == test_value
