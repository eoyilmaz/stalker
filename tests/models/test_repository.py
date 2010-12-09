#-*- coding: utf-8 -*-



import mocker
from stalker.models import repository, tag






########################################################################
class RepositoryTester(mocker.MockerTestCase):
    """tests the repository.Repository class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.name = 'a repository'
        self.description =  'this is for testing purposes'
        
        self.linux_path = '~/M/Projects'
        self.osx_path = '~/M/Projects'
        self.windows_path = 'M:\\Projects'
        
        # create a couple of mock tags
        self.mock_tag1 = self.mocker.mock(tag.Tag)
        self.mock_tag2 = self.mocker.mock(tag.Tag)
        
        # ------------
        # replace platform
        # weirdly I need to do it here...
        # then call it for a second time inside the test method
        tmp = self.mocker.replace("platform.system")
        tmp()
        # ------------
        
        self.mocker.replay()
        
        self.mock_repo = repository.Repository(
            name=self.name,
            description=self.description,
            tags=[self.mock_tag1, self.mock_tag2],
            linux_path=self.linux_path,
            osx_path=self.osx_path,
            windows_path=self.windows_path
        )
    
    
    
    #----------------------------------------------------------------------
    def test_linux_path_attribute_accepts_only_strings(self):
        """testing if linux_path attribute accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                repository.Repository,
                name=self.name,
                description=self.description,
                tags=[self.mock_tag1, self.mock_tag2],
                linux_path=test_value,
                osx_path=self.osx_path,
                windows_path=self.windows_path
            )
    
    
    
    #----------------------------------------------------------------------
    def test_linux_path_property_accepts_only_strings(self):
        """testing if linux_path property accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_repo,
                'linux_path',
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_linux_path_property_works_properly(self):
        """testing if the linux_path property works properly
        """
        
        test_value = '~/newRepoPath/Projects'
        
        self.mock_repo.linux_path = test_value
        
        self.assertEquals(self.mock_repo.linux_path, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_windows_path_attribute_accepts_only_strings(self):
        """testing if windows_path attribute accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                repository.Repository,
                name=self.name,
                description=self.description,
                tags=[self.mock_tag1, self.mock_tag2],
                linux_path=self.linux_path,
                osx_path=self.osx_path,
                windows_path=test_values
            )
    
    
    
    #----------------------------------------------------------------------
    def test_windows_path_property_accepts_only_strings(self):
        """testing if windows_path property accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_repo,
                'windows_path',
            test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_windows_path_property_works_properly(self):
        """testing if the windows_path property works properly
        """
        
        test_value = '~/newRepoPath/Projects'
        
        self.mock_repo.windows_path = test_value
        
        self.assertEquals(self.mock_repo.windows_path, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_osx_path_attribute_accepts_only_strings(self):
        """testing if osx_path attribute accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                repository.Repository,
                name=self.name,
                description=self.description,
                tags=[self.mock_tag1, self.mock_tag2],
                linux_path=self.linux_path,
                osx_path=test_values,
                windows_path=self.windows_path
            )
    
    
    
    #----------------------------------------------------------------------
    def test_osx_path_property_accepts_only_strings(self):
        """testing if osx_path property accepts only string or unicode
        values
        """
        
        test_values = [123123, 123.1231, [], {}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_repo,
                'osx_path',
            test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_osx_path_property_works_properly(self):
        """testing if the osx_path property works properly
        """
        
        test_value = '~/newRepoPath/Projects'
        
        self.mock_repo.osx_path = test_value
        
        self.assertEquals(self.mock_repo.osx_path, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_path_returns_properly_for_windows(self):
        """testing if the path returns the correct value for the os
        """
        
        assert(isinstance(self.mocker, mocker.Mocker))
        
        # test for windows
        tmp = self.mocker.replace("platform.system")
        tmp()
        
        self.mocker.result("Windows")
        self.mocker.count(0, 1000)
        self.mocker.replay()
        
        self.assertEquals(self.mock_repo.path, self.mock_repo.windows_path)
    
    
    
    #----------------------------------------------------------------------
    def test_path_returns_properly_for_linux(self):
        """testing if the path returns the correct value for the os
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
        """testing if the path returns the correct value for the os
        """
        
        assert(isinstance(self.mocker, mocker.Mocker))
        
        tmp = self.mocker.replace("platform.system")
        tmp()
        
        # test for osx
        self.mocker.result("Darwin")
        self.mocker.count(0, 1000)
        self.mocker.replay()
        
        self.assertEquals(self.mock_repo.path, self.mock_repo.osx_path)
    
    
    
    