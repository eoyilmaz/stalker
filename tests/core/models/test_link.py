#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import types, link






########################################################################
class LinkTester(mocker.MockerTestCase):
    """tests the :class:`~stalker.core.models.link.Link` class
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test 
        """
        
        assert(isinstance(self.mocker, mocker.Mocker))
        
        # create a mock LinkType object
        self.mock_link_type1 = self.mocker.mock(types.LinkType)
        self.mock_link_type2 = self.mocker.mock(types.LinkType)
        
        # for __eq__
        self.mock_link_type1.__eq__(self.mock_link_type2)
        self.mocker.result(False)
        self.mocker.count(0, None)
        
        
        self.mock_link_type1.__eq__(self.mock_link_type1)
        self.mocker.result(True)
        self.mocker.count(0, None)
        
        # for __ne__
        self.mock_link_type1.__ne__(self.mock_link_type2)
        self.mocker.result(True)
        self.mocker.count(0, None)
        
        self.mocker.replay()
        
        self.kwargs= {
            "name": "An Image Link",
            "path": "C:/A_NEW_PROJECT/",
            "filename": "this_is_an_image.jpg",
            "type": self.mock_link_type1
        }
        
        self.mock_link = link.Link(**self.kwargs)
    
    
    #----------------------------------------------------------------------
    def test_path_argument_accepts_string_or_unicode_only(self):
        """testing if path argument accepts string or unicode only and raises
        ValueError otherwise
        """
        
        test_values = [1, 1.1, ["a path"], {"a": "path"}]
        
        for test_value in test_values:
            self.kwargs["path"] = test_value
            self.assertRaises(ValueError, link.Link, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_path_attribute_accpets_string_or_unicode_only(self):
        """testing if path attribute accepts string or unicode only and raises
        ValueError otherwise
        """
        
        test_values = [1, 1.1, ["a path"], {"a": "path"}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_link,
                "path",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_path_argument_being_empty(self):
        """testing if setting the path argument to an empty string raises a
        ValueError
        """
        
        self.kwargs["path"] = ""
        self.assertRaises(ValueError, link.Link, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_path_attribute_being_empty(self):
        """testing if setting the path attribute to an empty string raises a
        ValueError
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_link,
            "path",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_path_argument_being_None(self):
        """testing if setting the path argument to None raises a ValueError
        """
        
        self.kwargs["path"] = None
        self.assertRaises(ValueError, link.Link, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_path_attribute_being_None(self):
        """testing if setting the path attribute to None raises a ValueError
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_link,
            "path",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_path_windows_to_other_conversion(self):
        """testing if the path is stored in internal format
        """
        
        windows_path = "M:\\path\\to\\object"
        expected_result = "M:/path/to/object"
        
        self.mock_link.path = windows_path
        
        self.assertEquals(self.mock_link.path, expected_result)
    
    
    
    #----------------------------------------------------------------------
    def test_filename_argument_accepts_string_or_unicode_only(self):
        """testing if filename argument accepts string or unicode only and
        raises ValueError otherwise
        """
        
        test_values = [1, 1.1, ["a filename"], {"a": "filename"}]
        
        for test_value in test_values:
            self.kwargs["filename"] = test_value
            self.assertRaises(ValueError, link.Link, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_filename_attribute_accpets_string_or_unicode_only(self):
        """testing if filename attribute accepts string or unicode only and
        raises ValueError otherwise
        """
        
        test_values = [1, 1.1, ["a filename"], {"a": "filename"}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_link,
                "filename",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_filename_argument_being_empty(self):
        """testing if setting the filename argument to an empty string raises a
        ValueError
        """
        
        self.kwargs["filename"] = ""
        self.assertRaises(ValueError, link.Link, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_filename_attribute_being_empty(self):
        """testing if setting the filename attribute to an empty string raises
        a ValueError
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_link,
            "filename",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_filename_argument_being_None(self):
        """testing if setting the filename argument to None raises a ValueError
        """
        
        self.kwargs["filename"] = None
        self.assertRaises(ValueError, link.Link, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_filename_attribute_being_None(self):
        """testing if setting the filename attribute to None raises a
        ValueError
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_link,
            "filename",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_being_None(self):
        """testing if a ValueError will be raised when type argument is set to
        None
        """
        
        self.kwargs["type"] = None
        self.assertRaises(ValueError, link.Link, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_being_None(self):
        """testing if a ValueError will be raised when type attribute is set to
        None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_link,
            "type",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_accepts_only_LinkType_objects(self):
        """testing if a ValueError will be raised when type argument is
        something other than a LinkType object
        """
        
        test_values = [1, 1.2, "A link Type", ["Another link type"],
                       {"another":"link type"}]
        
        for test_value in test_values:
            self.kwargs["type"] = test_value
            self.assertRaises(ValueError, link.Link, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_accepts_only_LinkType_objects(self):
        """testing if a ValueError will be raised when type attribute is
        somehting other than a LinkType object
        """
        
        test_values = [1, 1.2, "A link Type", ["Another link type"],
                       {"another":"link type"}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_link,
                "type",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_equality_of_two_links(self):
        """testing the equality operator
        """
        
        # with same parameters
        mock_link1 = link.Link(**self.kwargs)
        self.assertTrue(self.mock_link==mock_link1)
        
        # with different parameters
        self.kwargs["type"] = self.mock_link_type2
        mock_link2 = link.Link(**self.kwargs)
        
        self.assertFalse(self.mock_link==mock_link2)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality_of_two_links(self):
        """testing the inequality operator
        """
        # with same parameters
        mock_link1 = link.Link(**self.kwargs)
        self.assertTrue(self.mock_link==mock_link1)
        
        # with different parameters
        self.kwargs["type"] = self.mock_link_type2
        mock_link2 = link.Link(**self.kwargs)
        
        self.assertFalse(self.mock_link!=mock_link1)
        self.assertTrue(self.mock_link!=mock_link2)
    
    
    