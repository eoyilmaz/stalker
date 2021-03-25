# -*- coding: utf-8 -*-

import pytest
from stalker.testing import UnitTestDBBase, PlatformPatcher


class RepositoryTester(UnitTestDBBase):
    """tests the Repository class
    """

    def setUp(self):
        """setup the test
        """
        super(RepositoryTester, self).setUp()
        self.patcher = PlatformPatcher()

        # create a couple of test tags
        from stalker import Tag
        self.test_tag1 = Tag(name="test tag 1")
        self.test_tag2 = Tag(name="test tag 2")

        self.kwargs = {
            "name": "a repository",
            "code": "R1",
            "description": "this is for testing purposes",
            "tags": [self.test_tag1, self.test_tag2],
            "linux_path": "/mnt/M/Projects",
            "osx_path": "/Volumes/M/Projects",
            "windows_path": "M:/Projects"
        }

        from stalker import Repository
        from stalker.db.session import DBSession
        self.test_repo = Repository(**self.kwargs)
        DBSession.add(self.test_repo)
        DBSession.commit()

    def tearDown(self):
        """clean up test
        """
        self.patcher.restore()
        super(RepositoryTester, self).tearDown()

    def test_code_mixin_as_super(self):
        """testing if CodeMixin is one of the supers of the Repository class
        """
        from stalker import Repository, CodeMixin
        repo = Repository(**self.kwargs)
        assert isinstance(repo, CodeMixin)

    def test___auto_name__class_attribute_is_set_to_false(self):
        """testing if the __auto_name__ class attribute is set to False for
        Repository class
        """
        from stalker import Repository
        assert Repository.__auto_name__ is False

    def test_linux_path_argument_accepts_only_strings(self):
        """testing if linux_path argument accepts only string values
        """
        test_values = [123123, 123.1231, [], {}]
        for test_value in test_values:
            self.kwargs["linux_path"] = test_value
            from stalker import Repository

            with pytest.raises(TypeError):
                Repository(**self.kwargs)

    def test_linux_path_attribute_accepts_only_strings(self):
        """testing if linux_path attribute accepts only string values
        """
        test_values = [123123, 123.1231, [], {}]
        for test_value in test_values:
            with pytest.raises(TypeError):
                self.test_repo.linux_path = test_value

    def test_linux_path_attribute_is_working_properly(self):
        """testing if linux_path attribute is working properly
        """
        test_value = "~/newRepoPath/Projects/"
        self.test_repo.linux_path = test_value
        assert self.test_repo.linux_path == test_value

    def test_linux_path_attribute_finishes_with_a_slash(self):
        """testing if the linux_path attribute will be finished with a slash
        even it is not supplied by default
        """
        test_value = '/mnt/T'
        expected_value = '/mnt/T/'
        self.test_repo.linux_path = test_value
        assert self.test_repo.linux_path == expected_value

    def test_windows_path_argument_accepts_only_strings(self):
        """testing if windows_path argument accepts only string values
        """
        from stalker import Repository
        test_values = [123123, 123.1231, [], {}]
        for test_value in test_values:
            self.kwargs["windows_path"] = test_value
            with pytest.raises(TypeError):
                Repository(**self.kwargs)

    def test_windows_path_attribute_accepts_only_strings(self):
        """testing if windows_path attribute accepts only string values
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.windows_path = 123123

        assert str(cm.value) == \
            'Repository.windows_path should be an instance of string not int'

    def test_windows_path_attribute_is_working_properly(self):
        """testing if windows_path attribute is working properly
        """
        test_value = "~/newRepoPath/Projects/"
        self.test_repo.windows_path = test_value
        assert self.test_repo.windows_path == test_value

    def test_windows_path_attribute_finishes_with_a_slash(self):
        """testing if the windows_path attribute will be finished with a slash
        even it is not supplied by default
        """
        test_value = 'T:'
        expected_value = 'T:/'
        self.test_repo.windows_path = test_value
        assert self.test_repo.windows_path == expected_value

    def test_osx_path_argument_accepts_only_strings(self):
        """testing if osx_path argument accepts only string values
        """
        from stalker import Repository
        self.kwargs["osx_path"] = 123123
        with pytest.raises(TypeError) as cm:
            Repository(**self.kwargs)

        assert str(cm.value) == \
            'Repository.osx_path should be an instance of string not int'

    def test_osx_path_attribute_accepts_only_strings(self):
        """testing if osx_path attribute accepts only string values
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.osx_path = 123123

        assert str(cm.value) == \
            'Repository.osx_path should be an instance of string not int'

    def test_osx_path_attribute_is_working_properly(self):
        """testing if osx_path attribute is working properly
        """
        test_value = "~/newRepoPath/Projects/"
        self.test_repo.osx_path = test_value
        assert self.test_repo.osx_path == test_value

    def test_osx_path_attribute_finishes_with_a_slash(self):
        """testing if the osx_path attribute will be finished with a slash
        even it is not supplied by default
        """
        test_value = '/Volumes/T'
        expected_value = '/Volumes/T/'
        self.test_repo.osx_path = test_value
        assert self.test_repo.osx_path == expected_value

    def test_path_returns_properly_for_windows(self):
        """testing if path returns the correct value for the os
        """
        self.patcher.patch('Windows')
        assert self.test_repo.path == self.test_repo.windows_path

    def test_path_returns_properly_for_linux(self):
        """testing if path returns the correct value for the os
        """
        self.patcher.patch('Linux')
        assert self.test_repo.path == self.test_repo.linux_path

    def test_path_returns_properly_for_osx(self):
        """testing if path returns the correct value for the os
        """
        self.patcher.patch('Darwin')
        assert self.test_repo.path == self.test_repo.osx_path

    def test_path_attribute_sets_correct_path_for_windows(self):
        """testing if path property sets the correct attribute in windows
        """
        self.patcher.patch('Windows')
        test_value = 'S:/Projects/'
        assert self.test_repo.path != test_value
        assert self.test_repo.windows_path != test_value
        self.test_repo.path = test_value
        assert self.test_repo.windows_path == test_value
        assert self.test_repo.path == test_value

    def test_path_attribute_sets_correct_path_for_linux(self):
        """testing if path property sets the correct attribute in linux
        """
        self.patcher.patch('Linux')
        test_value = '/mnt/S/Projects/'
        assert self.test_repo.path != test_value
        assert self.test_repo.linux_path != test_value
        self.test_repo.path = test_value
        assert self.test_repo.linux_path == test_value
        assert self.test_repo.path == test_value

    def test_path_attribute_sets_correct_path_for_osx(self):
        """testing if path property sets the correct attribute in osx
        """
        self.patcher.patch('Darwin')
        test_value = '/Volumes/S/Projects/'
        assert self.test_repo.path != test_value
        assert self.test_repo.osx_path != test_value
        self.test_repo.path = test_value
        assert self.test_repo.osx_path == test_value
        assert self.test_repo.path == test_value

    def test_equality(self):
        """testing the equality of two repositories
        """
        from stalker import Repository
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

        assert repo1 == repo2
        assert not repo1 == repo3

    def test_inequality(self):
        """testing the inequality of two repositories
        """
        from stalker import Repository
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

        assert not repo1 != repo2
        assert repo1 != repo3

    def test_plural_class_name(self):
        """testing the plural name of Repository class
        """
        assert self.test_repo.plural_class_name == "Repositories"

    def test_linux_path_argument_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the linux_path argument
        """
        self.kwargs["linux_path"] = r"\mnt\M\Projects"
        from stalker import Repository
        new_repo = Repository(**self.kwargs)

        assert "\\" not in new_repo.linux_path
        assert new_repo.linux_path == "/mnt/M/Projects/"

    def test_linux_path_attribute_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the linux_path attribute
        """
        self.test_repo.linux_path = r"\mnt\M\Projects"
        assert "\\" not in self.test_repo.linux_path
        assert self.test_repo.linux_path == "/mnt/M/Projects/"

    def test_osx_path_argument_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the osx_path argument
        """
        from stalker import Repository
        self.kwargs["osx_path"] = r"\Volumes\M\Projects"
        new_repo = Repository(**self.kwargs)

        assert "\\" not in new_repo.linux_path
        assert new_repo.osx_path == "/Volumes/M/Projects/"

    def test_osx_path_attribute_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the osx_path attribute
        """
        self.test_repo.osx_path = r"\Volumes\M\Projects"
        assert "\\" not in self.test_repo.osx_path
        assert self.test_repo.osx_path == "/Volumes/M/Projects/"

    def test_windows_path_argument_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the windows_path argument
        """
        from stalker import Repository
        self.kwargs["windows_path"] = r"M:\Projects"
        new_repo = Repository(**self.kwargs)

        assert "\\" not in new_repo.linux_path
        assert new_repo.windows_path == "M:/Projects/"

    def test_windows_path_attribute_backward_slashes_are_converted_to_forward_slashes(self):
        """testing if the backward slashes are converted to forward slashes
        in the windows_path attribute
        """
        self.test_repo.windows_path = r"M:\Projects"
        assert "\\" not in self.test_repo.windows_path
        assert self.test_repo.windows_path == "M:/Projects/"

    def test_windows_path_with_more_than_one_slashes_converted_to_single_slash(self):
        """testing if the windows_path is set with more than one slashes is
        converted to single slash
        """
        self.test_repo.windows_path = r'M://'
        assert self.test_repo.windows_path == 'M:/'

        self.test_repo.windows_path = r'M://////////'
        assert self.test_repo.windows_path == 'M:/'

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
        assert \
            self.test_repo.to_linux_path(test_windows_path) == test_linux_path

    def test_to_linux_path_returns_the_linux_version_of_the_given_linux_path(self):
        """testing if the to_linux_path returns the linux version of the given
        linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        assert self.test_repo.to_linux_path(test_linux_path) == test_linux_path

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
        assert self.test_repo.to_linux_path(test_osx_path) == test_linux_path

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
        assert self.test_repo.to_linux_path(test_windows_path_reverse) == \
               test_linux_path

    def test_to_linux_path_returns_the_linux_version_of_the_given_reverse_linux_path(self):
        """testing if the to_linux_path returns the linux version of the given
        reverse linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        assert self.test_repo.to_linux_path(test_linux_path_reverse) == \
            test_linux_path

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
        assert self.test_repo.to_linux_path(test_osx_path_reverse) == \
            test_linux_path

    def test_to_linux_path_returns_the_linux_version_of_the_given_path_with_env_vars(self):
        """testing if the to_linux_path returns the linux version of the given
        path which contains env vars
        """
        import os
        self.test_repo.id = 1
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        os.environ['REPO1'] = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_path_with_env_var = '$REPO1/Sero/Task1/Task2/Some_file.ma'
        assert self.test_repo.to_linux_path(test_path_with_env_var) == \
            test_linux_path

    def test_to_linux_path_raises_TypeError_if_path_is_None(self):
        """testing if to_linux_path raises TypeError if path is None
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.to_linux_path(None)

        assert str(cm.value) == 'Repository.path can not be None'

    def test_to_linux_path_raises_TypeError_if_path_is_not_a_string(self):
        """testing if to_linux_path raises TypeError if path is None
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.to_linux_path(123)

        assert str(cm.value) == 'Repository.path should be a string, not int'

    def test_to_windows_path_returns_the_windows_version_of_the_given_windows_path(self):
        """testing if the to_windows_path returns the windows version of the
        given windows path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        assert self.test_repo.to_windows_path(test_windows_path) == \
            test_windows_path

    def test_to_windows_path_returns_the_windows_version_of_the_given_linux_path(self):
        """testing if the to_windows_path returns the windows version of the
        given linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        assert self.test_repo.to_windows_path(test_linux_path) == \
            test_windows_path

    def test_to_windows_path_returns_the_windows_version_of_the_given_osx_path(self):
        """testing if the to_windows_path returns the windows version of the
        given osx path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        assert self.test_repo.to_windows_path(test_osx_path) == \
            test_windows_path

    def test_to_windows_path_returns_the_windows_version_of_the_given_reverse_windows_path(self):
        """testing if the to_windows_path returns the windows version of the
        given reverse windows path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        test_windows_path_reverse = 'T:\\Stalker_Projects\\Sero\\Task1\\' \
                                    'Task2\\Some_file.ma'
        assert self.test_repo.to_windows_path(test_windows_path_reverse) == \
            test_windows_path

    def test_to_windows_path_returns_the_windows_version_of_the_given_reverse_linux_path(self):
        """testing if the to_windows_path returns the windows version of the
        given reverse linux path
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        assert self.test_repo.to_windows_path(test_linux_path_reverse) == \
            test_windows_path

    def test_to_windows_path_returns_the_windows_version_of_the_given_reverse_osx_path(self):
        """testing if the to_windows_path returns the windows version of the
        given reverse osx path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'
        assert self.test_repo.to_windows_path(test_osx_path_reverse) == \
            test_windows_path

    def test_to_windows_path_returns_the_windows_version_of_the_given_path_with_env_vars(self):
        """testing if the to_windows_path returns the windows version of the
        given path which contains env vars
        """
        import os
        self.test_repo.id = 1
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        os.environ['REPO1'] = self.test_repo.linux_path
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/' \
                            'Some_file.ma'
        test_path_with_env_var = '$REPO1/Sero/Task1/Task2/Some_file.ma'
        assert self.test_repo.to_windows_path(test_path_with_env_var) == \
            test_windows_path

    def test_to_windows_path_raises_TypeError_if_path_is_None(self):
        """testing if to_windows_path raises TypeError if path is None
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.to_windows_path(None)

        assert str(cm.value) == 'Repository.path can not be None'

    def test_to_windows_path_raises_TypeError_if_path_is_not_a_string(self):
        """testing if to_windows_path raises TypeError if path is None
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.to_windows_path(123)

        assert str(cm.value) == 'Repository.path should be a string, not int'

    def test_to_osx_path_returns_the_osx_version_of_the_given_windows_path(self):
        """testing if the to_osx_path returns the osx version of the given
        windows path
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        assert self.test_repo.to_osx_path(test_windows_path) == test_osx_path

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
        assert self.test_repo.to_osx_path(test_linux_path) == test_osx_path

    def test_to_osx_path_returns_the_osx_version_of_the_given_osx_path(self):
        """testing if the to_osx_path returns the osx version of the given
        osx path
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        assert self.test_repo.to_osx_path(test_osx_path) == test_osx_path

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
        assert self.test_repo.to_osx_path(test_windows_path_reverse) == \
            test_osx_path

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
        assert self.test_repo.to_osx_path(test_linux_path_reverse) == \
            test_osx_path

    def test_to_osx_path_returns_the_osx_version_of_the_given_reverse_osx_path(self):
        """testing if the to_osx_path returns the osx version of the given
        reverse osx path
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'
        assert self.test_repo.to_osx_path(test_osx_path_reverse) == \
            test_osx_path

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

        assert self.test_repo.to_osx_path(test_windows_path) == test_osx_path
        assert self.test_repo.to_osx_path(test_linux_path) == test_osx_path
        assert self.test_repo.to_osx_path(test_osx_path) == test_osx_path
        assert self.test_repo.to_osx_path(test_windows_path_reverse) == \
            test_osx_path
        assert self.test_repo.to_osx_path(test_linux_path_reverse) == \
            test_osx_path
        assert self.test_repo.to_osx_path(test_osx_path_reverse) == \
            test_osx_path

    def test_to_osx_path_returns_the_osx_version_of_the_given_path_with_env_vars(self):
        """testing if the to_osx_path returns the osx version of the given path
        which contains env vars
        """
        import os
        self.test_repo.id = 1
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        os.environ['REPO1'] = self.test_repo.windows_path
        test_windows_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                            'Some_file.ma'
        test_path_with_env_var = '$REPO1/Sero/Task1/Task2/Some_file.ma'
        assert self.test_repo.to_osx_path(test_path_with_env_var) == \
            test_windows_path

    def test_to_osx_path_raises_TypeError_if_path_is_None(self):
        """testing if to_osx_path raises TypeError if path is None
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.to_osx_path(None)

        assert str(cm.value) == 'Repository.path can not be None'

    def test_to_osx_path_raises_TypeError_if_path_is_not_a_string(self):
        """testing if to_osx_path raises TypeError if path is None
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.to_osx_path(123)

        assert str(cm.value) == 'Repository.path should be a string, not int'

    def test_to_native_path_returns_the_native_version_of_the_given_linux_path(self):
        """testing if the to_native_path returns the native version of the
        given linux path
        """
        self.patcher.patch('Linux')

        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'

        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'

        assert self.test_repo.to_native_path(test_linux_path) == \
            test_linux_path

    def test_to_native_path_returns_the_native_version_of_the_given_windows_path(self):
        """testing if the to_native_path returns the native version of the
        given windows path
        """
        self.patcher.patch('Linux')

        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'

        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'

        assert self.test_repo.to_native_path(test_windows_path) == \
            '/mnt/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'

    def test_to_native_path_returns_the_native_version_of_the_given_osx_path(self):
        """testing if the to_native_path returns the native version of the
        given osx path
        """
        self.patcher.patch('Linux')

        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        assert self.test_repo.to_native_path(test_osx_path) == test_linux_path

    def test_to_native_path_returns_the_native_version_of_the_given_reverse_windows_path(self):
        """testing if the to_native_path returns the native version of the
        given reverse windows path
        """
        self.patcher.patch('Linux')

        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_windows_path_reverse = 'T:\\Stalker_Projects\\Sero\\Task1\\' \
                                    'Task2\\Some_file.ma'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        assert self.test_repo.to_native_path(test_windows_path_reverse) == \
            test_linux_path

    def test_to_native_path_returns_the_native_version_of_the_given_reverse_linux_path(self):
        """testing if the to_native_path returns the native version of the
        given reverse linux path
        """
        self.patcher.patch('Linux')

        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        assert self.test_repo.to_native_path(test_linux_path_reverse) == \
            test_linux_path

    def test_to_native_path_returns_the_native_version_of_the_given_reverse_osx_path(self):
        """testing if the to_native_path returns the native version of the
        given reverse osx path
        """
        self.patcher.patch('Linux')

        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'
        assert self.test_repo.to_native_path(test_osx_path_reverse) == \
            test_linux_path

    def test_to_native_path_raises_TypeError_if_path_is_None(self):
        """testing if to_native_path raises TypeError if path is None
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.to_native_path(None)

        assert str(cm.value) == 'Repository.path can not be None'

    def test_to_native_path_raises_TypeError_if_path_is_not_a_string(self):
        """testing if to_native_path raises TypeError if path is None
        """
        with pytest.raises(TypeError) as cm:
            self.test_repo.to_native_path(123)

        assert str(cm.value) == 'Repository.path should be a string, not int'

    def test_is_in_repo_returns_True_if_the_given_linux_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given linux path is in
        this repo or False otherwise
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/' \
                          'Some_file.ma'
        assert self.test_repo.is_in_repo(test_linux_path)

    def test_is_in_repo_returns_True_if_the_given_linux_reverse_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given linux reverse path
        is in this repo or False otherwise
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_linux_path_reverse = '\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\' \
                                  'Task2\\Some_file.ma'
        assert self.test_repo.is_in_repo(test_linux_path_reverse)

    def test_is_in_repo_returns_False_if_the_given_linux_path_is_not_in_this_repo(self):
        """testing if is_in_repo returns False if the given linux path is not
        in this repo or False otherwise
        """
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        test_not_in_path_linux_path = '/mnt/T/Other_Projects/Sero/Task1/' \
                                      'Task2/Some_file.ma'
        assert self.test_repo.is_in_repo(test_not_in_path_linux_path) is False

    def test_is_in_repo_returns_True_if_the_given_windows_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given windows path is in
        this repo or False otherwise
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        assert self.test_repo.is_in_repo(test_windows_path)

    def test_is_in_repo_returns_True_if_the_given_windows_reverse_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given windows reverse path
        is in this repo or False otherwise
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path_reverse = 'T:\\Stalker_Projects\\Sero\\Task1\\' \
                                    'Task2\\Some_file.ma'
        assert self.test_repo.is_in_repo(test_windows_path_reverse)

    def test_is_in_repo_is_case_insensitive_under_windows(self):
        """testing if is_in_repo is case-insensitive under windows
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_windows_path_reverse = 't:\\stalKer_ProjectS\\sErO\\task1\\' \
                                    'Task2\\Some_file.ma'
        assert self.test_repo.is_in_repo(test_windows_path_reverse)

    def test_is_in_repo_returns_False_if_the_given_windows_path_is_not_in_this_repo(self):
        """testing if is_in_repo returns False if the given windows path is not
        in this repo or False otherwise
        """
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        test_not_in_path_windows_path = 'T:/Other_Projects/Sero/Task1/Task2/' \
                                        'Some_file.ma'
        assert \
            self.test_repo.is_in_repo(test_not_in_path_windows_path) is False

    def test_is_in_repo_returns_True_if_the_given_osx_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given osx path is in
        this repo or False otherwise
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/' \
                        'Some_file.ma'
        assert self.test_repo.is_in_repo(test_osx_path)

    def test_is_in_repo_returns_True_if_the_given_osx_reverse_path_is_in_this_repo(self):
        """testing if is_in_repo returns True if the given osx reverse path
        is in this repo or False otherwise
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_osx_path_reverse = '\\Volumes\\T\\Stalker_Projects\\Sero\\' \
                                'Task1\\Task2\\Some_file.ma'
        assert self.test_repo.is_in_repo(test_osx_path_reverse)

    def test_is_in_repo_returns_False_if_the_given_osx_path_is_not_in_this_repo(self):
        """testing if is_in_repo returns False if the given osx path is not
        in this repo or False otherwise
        """
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        test_not_in_path_osx_path = '/Volumes/T/Other_Projects/Sero/Task1/' \
                                    'Task2/Some_file.ma'
        assert not self.test_repo.is_in_repo(test_not_in_path_osx_path)

    def test_make_relative_method_converts_the_given_linux_path_to_relative_to_repo_root(self):
        """testing if Repository.make_relative() will convert the given Linux
        path to repository root relative path
        """
        # a Linux Path
        linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        result = self.test_repo.make_relative(linux_path)
        assert result == 'Sero/Task1/Task2/Some_file.ma'

    def test_make_relative_method_converts_the_given_osx_path_to_relative_to_repo_root(self):
        """testing if Repository.make_relative() will convert the given OSX
        path to repository root relative path
        """
        # an OSX Path
        osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        result = self.test_repo.make_relative(osx_path)
        assert result == 'Sero/Task1/Task2/Some_file.ma'

    def test_make_relative_method_converts_the_given_windows_path_to_relative_to_repo_root(self):
        """testing if Repository.make_relative() will convert the given Windows
        path to repository root relative path
        """
        # a Windows Path
        windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.test_repo.osx_path = 'T:/Stalker_Projects'
        result = self.test_repo.make_relative(windows_path)
        assert result == 'Sero/Task1/Task2/Some_file.ma'

    def test_make_relative_method_converts_the_given_path_with_env_variable_to_native_path(self):
        """testing if Repository.make_relative() will convert the given path
        with environment variable to repository root relative path
        """
        # so we should have the env var to be configured
        # now create a path with env var
        path = '$REPO%s/Sero/Task1/Task2/Some_file.ma' % self.test_repo.code
        result = self.test_repo.make_relative(path)
        assert result == 'Sero/Task1/Task2/Some_file.ma'

    def test_make_relative_method_converts_the_given_path_with_old_env_variable_to_native_path(self):
        """testing if Repository.make_relative() will convert the given path
        with old environment variable to repository root relative path
        """
        # so we should have the env var to be configured
        # now create a path with env var
        path = '$REPO%s/Sero/Task1/Task2/Some_file.ma' % self.test_repo.id
        result = self.test_repo.make_relative(path)
        assert result == 'Sero/Task1/Task2/Some_file.ma'

    def test_to_os_independent_path_is_working_properly(self):
        """testing if to_os_independent_path class method is working properly
        """
        from stalker.db.session import DBSession
        DBSession.add(self.test_repo)
        DBSession.commit()

        relative_part = 'some/path/to/a/file.ma'
        test_path = '%s/%s' % (self.test_repo.path, relative_part)
        from stalker import Repository
        assert Repository.to_os_independent_path(test_path) == \
            '$REPO%s/%s' % (self.test_repo.code, relative_part)

    def test_to_os_independent_path_for_old_environment_vars(self):
        """testing if to_os_independent_path class method is working properly
        for paths that contain old env vars
        """
        from stalker.db.session import DBSession
        DBSession.add(self.test_repo)
        DBSession.commit()

        relative_part = 'some/path/to/a/file.ma'
        test_path = '$REPO%s/%s' % (self.test_repo.id, relative_part)
        from stalker import Repository
        assert Repository.to_os_independent_path(test_path) == \
            '$REPO%s/%s' % (self.test_repo.code, relative_part)

    def test_to_os_independent_path_method_converts_the_given_linux_path_to_universal(self):
        """testing if Repository.to_os_independent_path() will convert the
        given Linux path to a os independent path that uses the Repository
        environment variable
        """
        # a Linux Path
        linux_path = '/mnt/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.test_repo.linux_path = '/mnt/T/Stalker_Projects'
        self.test_repo.windows_path = 'T:/Stalker_Projects'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        result = self.test_repo.to_os_independent_path(linux_path)
        assert result == \
               '$REPO%s/Sero/Task1/Task2/Some_file.ma' % self.test_repo.code

    def test_to_os_independent_path_method_converts_the_given_osx_path_to_universal(self):
        """testing if Repository.to_os_independent_path() will convert the
        given OSX path to a os independent path that uses the Repository
        environment variable
        """
        # an OSX Path
        osx_path = '/Volumes/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.test_repo.osx_path = '/Volumes/T/Stalker_Projects'
        result = self.test_repo.to_os_independent_path(osx_path)
        assert result == \
               '$REPO%s/Sero/Task1/Task2/Some_file.ma' % self.test_repo.code

    def test_to_os_independent_path_method_converts_the_given_windows_path_to_universal(self):
        """testing if Repository.to_os_independent_path() will convert the
        given Windows path to a os independent path that uses the Repository
        environment variable
        """
        # a Windows Path
        windows_path = 'T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma'
        self.test_repo.osx_path = 'T:/Stalker_Projects'
        result = self.test_repo.to_os_independent_path(windows_path)
        assert result == \
               '$REPO%s/Sero/Task1/Task2/Some_file.ma' % self.test_repo.code

    def test_to_os_independent_path_method_not_change_the_path_with_env_variable(self):
        """testing if Repository.to_os_independent_path() will not change the
        given path with environment variable
        """
        # so we should have the env var to be configured
        # now create a path with env var
        path = '$REPO%s/Sero/Task1/Task2/Some_file.ma' % self.test_repo.code
        result = self.test_repo.to_os_independent_path(path)
        assert result == \
            '$REPO%s/Sero/Task1/Task2/Some_file.ma' % self.test_repo.code

    def test_to_os_independent_path_method_converts_the_given_path_with_old_env_variable_new_env_variable(self):
        """testing if Repository.to_os_independent_path() will convert the path
        with old environment variable to a path with new environment variable
        """
        # so we should have the env var to be configured
        # now create a path with env var
        path = '$REPO%s/Sero/Task1/Task2/Some_file.ma' % self.test_repo.id
        result = self.test_repo.to_os_independent_path(path)
        assert result == \
            '$REPO%s/Sero/Task1/Task2/Some_file.ma' % self.test_repo.code

    def test_find_repo_is_working_properly(self):
        """testing if the find_repo class method is working properly
        """
        from stalker.db.session import DBSession
        DBSession.add(self.test_repo)
        DBSession.commit()

        # add some other repositories
        from stalker import Repository
        new_repo1 = Repository(
            name='New Repository',
            code='NR',
            linux_path='/mnt/T/Projects',
            osx_path='/Volumes/T/Projects',
            windows_path='T:/Projects'
        )
        DBSession.add(new_repo1)
        DBSession.commit()

        test_path = '%s/some/path/to/a/file.ma' % self.test_repo.path
        assert Repository.find_repo(test_path) == self.test_repo

        test_path = '%s/some/path/to/a/file.ma' % new_repo1.windows_path
        assert Repository.find_repo(test_path) == new_repo1

    def test_find_repo_is_case_insensitive_under_windows(self):
        """testing if the find_repo class method is case-insensitive under
        windows
        """
        import platform
        if platform.platform() != 'Windows':
            pytest.skip("Test under Windows only!")

        from stalker.db.session import DBSession
        DBSession.add(self.test_repo)
        DBSession.commit()

        # add some other repositories
        from stalker import Repository
        new_repo1 = Repository(
            name='New Repository',
            code='NR',
            linux_path='/mnt/T/Projects',
            osx_path='/Volumes/T/Projects',
            windows_path='T:/Projects'
        )
        DBSession.add(new_repo1)
        DBSession.commit()

        test_path = '%s/some/path/to/a/file.ma' % self.test_repo.path.lower()
        assert Repository.find_repo(test_path) == self.test_repo

        test_path = '%s/some/path/to/a/file.ma' % \
                    new_repo1.windows_path.lower()
        assert Repository.find_repo(test_path) == new_repo1

    def test_find_repo_is_working_properly_with_reverse_slashes(self):
        """testing if the find_repo class method will work properly with paths
        that contains reverse slashes
        """
        from stalker.db.session import DBSession
        DBSession.add(self.test_repo)
        DBSession.commit()

        # add some other repositories
        from stalker import Repository
        new_repo1 = Repository(
            name='New Repository',
            code='NR',
            linux_path='/mnt/T/Projects',
            osx_path='/Volumes/T/Projects',
            windows_path='T:/Projects'
        )
        DBSession.add(new_repo1)
        DBSession.commit()

        test_path = '%s\\some\\path\\to\\a\\file.ma' % \
                    self.test_repo.path
        test_path.replace('/', '\\')
        assert Repository.find_repo(test_path) == self.test_repo

        test_path = '%s\\some\\path\\to\\a\\file.ma' % \
                    new_repo1.windows_path.lower()
        test_path.replace('/', '\\')
        assert Repository.find_repo(test_path) == new_repo1

    def test_find_repo_is_working_properly_with_env_vars(self):
        """testing if the find_repo class method is working properly with paths
        containing env vars
        """
        from stalker.db.session import DBSession
        DBSession.add(self.test_repo)
        DBSession.commit()

        # add some other repositories
        from stalker import Repository
        new_repo1 = Repository(
            name='New Repository',
            code='NR',
            linux_path='/mnt/T/Projects',
            osx_path='/Volumes/T/Projects',
            windows_path='T:/Projects'
        )
        DBSession.add(new_repo1)
        DBSession.commit()

        # Test with env var
        test_path = '$REPO%s/some/path/to/a/file.ma' % self.test_repo.code
        assert Repository.find_repo(test_path) == self.test_repo

        test_path = '$REPO%s/some/path/to/a/file.ma' % new_repo1.code
        assert Repository.find_repo(test_path) == new_repo1

        # Test with old env var
        test_path = '$REPO%s/some/path/to/a/file.ma' % self.test_repo.id
        assert Repository.find_repo(test_path) == self.test_repo

        test_path = '$REPO%s/some/path/to/a/file.ma' % new_repo1.id
        assert Repository.find_repo(test_path) == new_repo1

    def test_env_var_property_is_working_properly(self):
        """testing if the env_var property is working properly
        """
        assert self.test_repo.env_var == 'REPOR1'

    def test_creating_and_committing_a_new_repository_instance_will_create_env_var(self):
        """testing if an environment variable will be created when a new
        repository is created
        """
        from stalker import defaults, Repository
        from stalker.db.session import DBSession
        repo = Repository(
            name='Test Repo',
            code='TR',
            linux_path='/mnt/T',
            osx_path='/Volumes/T',
            windows_path='T:/'
        )
        DBSession.add(repo)
        DBSession.commit()

        import os
        assert defaults.repo_env_var_template % {'code': repo.code} in \
            os.environ

        # check the old ID based env var
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == repo.path

    def test_updating_a_repository_will_update_repo_path(self):
        """testing if the environment variable will be updated when the
        repository path is updated
        """
        from stalker import defaults, Repository
        repo = Repository(
            name='Test Repo',
            code='TR',
            linux_path='/mnt/T',
            osx_path='/Volumes/T',
            windows_path='T:/'
        )
        from stalker.db.session import DBSession
        DBSession.add(repo)
        DBSession.commit()

        import os
        assert defaults.repo_env_var_template % {'code': repo.code} \
            in os.environ
        assert defaults.repo_env_var_template_old % {'id': repo.id} \
            in os.environ

        # now update the repository
        test_value = '/mnt/S/'
        repo.path = test_value

        # expect the environment variable is also updated
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == test_value
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == test_value

    def test_updating_windows_path_only_update_repo_path_if_on_windows(self):
        """testing if updating the windows path will only update the path if
        the system is windows
        """
        self.patcher.patch('Linux')
        from stalker import Repository
        repo = Repository(
            name='Test Repo',
            code='TR',
            linux_path='/mnt/T',
            osx_path='/Volumes/T',
            windows_path='T:/'
        )
        from stalker.db.session import DBSession
        DBSession.add(repo)
        DBSession.commit()

        import os
        from stalker import defaults
        assert \
            defaults.repo_env_var_template % {'code': repo.code} in os.environ
        assert \
            defaults.repo_env_var_template_old % {'id': repo.id} in os.environ

        # now update the repository
        test_value = 'S:/'
        repo.windows_path = test_value

        # expect the environment variable not updated
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] != test_value
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == repo.linux_path

        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] != test_value
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == repo.linux_path

        # make it windows
        self.patcher.patch('Windows')

        # now update the repository
        test_value = 'S:/'
        repo.windows_path = test_value

        # expect the environment variable not updated
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == test_value
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == repo.windows_path
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == test_value
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == repo.windows_path

    def test_updating_osx_path_only_update_repo_path_if_on_osx(self):
        """testing if updating the osx path will only update the path if the
        system is osx
        """
        self.patcher.patch('Windows')

        from stalker import defaults, Repository
        repo = Repository(
            name='Test Repo',
            code='TR',
            linux_path='/mnt/T',
            osx_path='/Volumes/T',
            windows_path='T:/'
        )
        from stalker.db.session import DBSession
        DBSession.add(repo)
        DBSession.commit()

        import os
        assert \
            defaults.repo_env_var_template % {'code': repo.code} in os.environ
        assert \
            defaults.repo_env_var_template_old % {'id': repo.id} in os.environ

        # now update the repository
        test_value = '/Volumes/S/'
        repo.osx_path = test_value

        # expect the environment variable not updated
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] != test_value
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == repo.windows_path

        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] != test_value
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == repo.windows_path

        # make it osx
        self.patcher.patch('Darwin')

        # now update the repository
        test_value = '/Volumes/S/'
        repo.osx_path = test_value

        # expect the environment variable not updated
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == test_value
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == repo.osx_path

        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == test_value
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == repo.osx_path

    def test_updating_linux_path_only_update_repo_path_if_on_linux(self):
        """testing if updating the linux path will only update the path if the
        system is linux
        """
        self.patcher.patch('Darwin')

        from stalker import defaults, Repository
        repo = Repository(
            name='Test Repo',
            code='TR',
            linux_path='/mnt/T',
            osx_path='/Volumes/T',
            windows_path='T:/'
        )
        from stalker.db.session import DBSession
        DBSession.add(repo)
        DBSession.commit()

        import os
        assert \
            defaults.repo_env_var_template % {'code': repo.code} in os.environ
        assert \
            defaults.repo_env_var_template_old % {'id': repo.id} in os.environ

        # now update the repository
        test_value = '/mnt/S/'
        repo.linux_path = test_value

        # expect the environment variable not updated
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] != test_value
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == repo.osx_path

        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] != test_value
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == repo.osx_path

        # make it linux
        self.patcher.patch('Linux')

        # now update the repository
        test_value = '/mnt/S/'
        repo.linux_path = test_value

        # expect the environment variable not updated
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == test_value
        assert \
            os.environ[
                defaults.repo_env_var_template % {'code': repo.code}
            ] == repo.linux_path

        # expect the environment variable not updated
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == test_value
        assert \
            os.environ[
                defaults.repo_env_var_template_old % {'id': repo.id}
            ] == repo.linux_path
