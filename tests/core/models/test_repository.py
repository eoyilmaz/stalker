#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import repository, tag






########################################################################
class RepositoryTester(mocker.MockerTestCase):
    """tests the repository.Repository class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create a couple of mock tags
        self.mock_tag1 = self.mocker.mock(tag.Tag)
        self.mock_tag2 = self.mocker.mock(tag.Tag)
        
        # ------------
        # replace platform
        # weirdly I need to do it here...
        # then call it for a second time inside the test method
        tmp = self.mocker.replace("platform.system")
        tmp()
        self.mocker.count(0,1000)
        # ------------
        
        self.mocker.replay()
        
        self.kwargs = {
            "name": "a repository",
            "description": "this is for testing purposes",
            "tags": [self.mock_tag1, self.mock_tag2],
            "linux_path": "~/M/Projects",
            "osx_path": "/Volumes/M/Projects",
            "windows_path": "M:\\Projects"
        }
        
        self.mock_repo = repository.Repository(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_linux_path_argument_accepts_only_strings(self):
        """testing if linux_path argument accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.kwargs["linux_path"] = test_value
            self.assertRaises(ValueError, repository.Repository, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_linux_path_attribute_accepts_only_strings(self):
        """testing if linux_path attribute accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_repo,
                "linux_path",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_linux_path_attribute_works_properly(self):
        """testing if linux_path attribute works properly
        """
        
        test_value = "~/newRepoPath/Projects"
        self.mock_repo.linux_path = test_value
        self.assertEquals(self.mock_repo.linux_path, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_windows_path_argument_accepts_only_strings(self):
        """testing if windows_path argument accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.kwargs["windows_path"] = test_value
            self.assertRaises(ValueError, repository.Repository, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_windows_path_attribute_accepts_only_strings(self):
        """testing if windows_path attribute accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_repo,
                "windows_path",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_windows_path_attribute_works_properly(self):
        """testing if windows_path attribute works properly
        """
        
        test_value = "~/newRepoPath/Projects"
        self.mock_repo.windows_path = test_value
        self.assertEquals(self.mock_repo.windows_path, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_osx_path_argument_accepts_only_strings(self):
        """testing if osx_path argument accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.kwargs["osx_path"] = test_value
            self.assertRaises(ValueError, repository.Repository, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_osx_path_attribute_accepts_only_strings(self):
        """testing if osx_path attribute accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_repo,
                "osx_path",
            test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_osx_path_attribute_works_properly(self):
        """testing if osx_path attribute works properly
        """
        
        test_value = "~/newRepoPath/Projects"
        self.mock_repo.osx_path = test_value
        self.assertEquals(self.mock_repo.osx_path, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_path_returns_properly_for_windows(self):
        """testing if path returns the correct value for the os
        """
        
        assert(isinstance(self.mocker, mocker.Mocker))
        
        # test for windows
        tmp = self.mocker.replace("platform.system")
        tmp()
        
        self.mocker.result("Windows")
        self.mocker.count(0, 1000)
        self.mocker.replay()
        
        #import platform
        #self.assertEquals(platform.system(), "Windows")
        
        new_mock_repo = repository.Repository(**self.kwargs)
        
        self.assertEquals(new_mock_repo.path, new_mock_repo.windows_path)
    
    
    
    #----------------------------------------------------------------------
    def test_path_returns_properly_for_linux(self):
        """testing if path returns the correct value for the os
        """
        
        assert(isinstance(self.mocker, mocker.Mocker))
        
        tmp = self.mocker.replace("platform.system")
        tmp()
        
        # test for linux
        self.mocker.result("Linux")
        self.mocker.count(0, 1000)
        self.mocker.replay()
        
        self.assertEquals(self.mock_repo.path, self.mock_repo.linux_path)
    
    
    
    #----------------------------------------------------------------------
    def test_path_returns_properly_for_osx(self):
        """testing if path returns the correct value for the os
        """
        
        assert(isinstance(self.mocker, mocker.Mocker))
        
        tmp = self.mocker.replace("platform.system")
        tmp()
        
        # test for osx
        self.mocker.result("Darwin")
        self.mocker.count(0, 1000)
        self.mocker.replay()
        
        self.assertEquals(self.mock_repo.path, self.mock_repo.osx_path)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality of two repositories
        """
        
        repo1 = repository.Repository(**self.kwargs)
        repo2 = repository.Repository(**self.kwargs)
        
        self.kwargs.update({
            "name": "a repository",
            "description": "this is the commercial repository",
            "linux_path": "/mnt/commercialServer/Projects",
            "osx_path": "/Volumes/commercialServer/Projects",
            "windows_path": "Z:\\Projects"
        })
        
        repo3 = repository.Repository(**self.kwargs)
        
        self.assertTrue(repo1==repo2)
        self.assertFalse(repo1==repo3)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality of two repositories
        """
        
        repo1 = repository.Repository(**self.kwargs)
        repo2 = repository.Repository(**self.kwargs)
        
        self.kwargs.update({
            "name": "a repository",
            "description": "this is the commercial repository",
            "linux_path": "/mnt/commercialServer/Projects",
            "osx_path": "/Volumes/commercialServer/Projects",
            "windows_path": "Z:\\Projects"
        })
        
        repo3 = repository.Repository(**self.kwargs)
        
        self.assertFalse(repo1!=repo2)
        self.assertTrue(repo1!=repo3)
    
    
    
    