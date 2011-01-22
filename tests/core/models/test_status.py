#-*- coding: utf-8 -*-



import unittest
from stalker.core.models import status



########################################################################
class StatusTest(unittest.TestCase):
    """tests the status class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.kwargs = {
            "name": "Complete",
            "description": "use this when the object is complete",
            "code": "CMPLT",
        }
        
        # create an entity object with same kwargs for __eq__ and __ne__ tests
        # (it should return False for __eq__ and True for __ne__ for same
        # kwargs)
        from stalker.core.models import entity
        self.entity1 = entity.Entity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality of two statuses
        """
        
        status1 = status.Status(**self.kwargs)
        status2 = status.Status(**self.kwargs)
        
        self.kwargs["name"] = "Work In Progress"
        self.kwargs["description"] = "use this when the object is still in \
        progress"
        self.kwargs["code"] = "WIP"
        
        status3 = status.Status(**self.kwargs)
        
        self.assertTrue(status1==status2)
        self.assertFalse(status1==status3)
        self.assertFalse(status1==self.entity1)
    
    
    
    def test_inequality(self):
        """testing inequality of two statuses
        """
        
        status1 = status.Status(**self.kwargs)
        status2 = status.Status(**self.kwargs)
        
        self.kwargs["name"] = "Work In Progress"
        self.kwargs["description"] = "use this when the object is still in \
        progress"
        self.kwargs["code"] = "WIP"
        
        status3 = status.Status(**self.kwargs)
        
        self.assertFalse(status1!=status2)
        self.assertTrue(status1!=status3)
        self.assertTrue(status1!=self.entity1)






########################################################################
class StatusListTest(unittest.TestCase):
    """testing the StatusList class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """let's create proper values for the tests
        """
        
        from stalker.core.models import project
        
        self.kwargs = {
            "name": "a status list",
            "description": "this is a status list for testing purposes",
            "statuses": [
                status.Status(name="Not Available", code="N/A"),
                status.Status(name="Waiting To Start", code="WSTRT"),
                status.Status(name="Started", code="STRT"),
                status.Status(name="Waiting For Approve", code="WAPPR"),
                status.Status(name="Approved", code="APPR"),
                status.Status(name="Finished", code="FNSH"),
                status.Status(name="On Hold", code="OH"),
                ],
            "target_entity_type": project.Project.entity_type,
        }
        
        self.mock_status_list = status.StatusList(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_accepts_statuses_only(self):
        """testing if statuses list argument accepts list of statuses only
        """
        
        # the statuses argument should be a list of statuses
        # can be empty?
        #
        
        test_values = ["a str", {}, 1, 1.0]
        
        for test_value in test_values:
            #----------------------------------------------------------------------
            # it should only accept lists of statuses
            
            self.kwargs["statuses"] = test_value
            
            self.assertRaises(ValueError, status.StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_property_accepting_only_statuses(self):
        """testing the status_list property as a property and accepting
        Status objects only
        """
        
        test_values = ["1", ["1"], 1, [1, "w"]]
        
        # check the property
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_status_list,
                "statuses",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_being_empty(self):
        """testing status_list against being empty
        """
        
        #----------------------------------------------------------------------
        # the list couldn't be empty
        self.kwargs["statuses"] = []
        
        self.assertRaises(ValueError, status.StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_statusList_list_elements_being_status_objects(self):
        """testing status_list elements against not being derived from Status
        class
        """
        
        #----------------------------------------------------------------------
        # every element should be an object derived from Status
        a_fake_status_list = [1, 2, "a string", u"a unicode", 4.5]
        
        self.kwargs["statuses"] = a_fake_status_list
        
        self.assertRaises(ValueError, status.StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_statusList_property(self):
        """testing status_list as being property
        """
        
        #----------------------------------------------------------------------
        # it should be a property so check if it sets property correctly
        
        new_list_of_statutes = [
            status.Status(name="New Status", code="NSTS")
        ]
        
        self.mock_status_list.statuses = new_list_of_statutes
        self.assertEquals( self.mock_status_list.statuses,
                           new_list_of_statutes)
    
    
    
    #----------------------------------------------------------------------
    def test_equality_operator(self):
        """testing equality of two status list object
        """
        
        status_list1 = status.StatusList(**self.kwargs)
        status_list2 = status.StatusList(**self.kwargs)
        
        
        self.kwargs["target_entity_type"] = "SomeOtherClass"
        
        status_list3 = status.StatusList(**self.kwargs)
        
        self.kwargs["statuses"] = [
            status.Status(name="Started", code="STRT"),
            status.Status(name="Waiting For Approve", code="WAPPR"),
            status.Status(name="Approved", code="APPR"),
            status.Status(name="Finished", code="FNSH"),
        ]
        
        status_list4 = status.StatusList(**self.kwargs)
        
        
        
        self.assertTrue(status_list1==status_list2)
        self.assertFalse(status_list1==status_list3)
        self.assertFalse(status_list1==status_list4)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality_operator(self):
        """testing equality of two status list object
        """
        
        status_list1 = status.StatusList(**self.kwargs)
        status_list2 = status.StatusList(**self.kwargs)
        
        self.kwargs["target_entity_type"] = "SomeOtherClass"
        
        status_list3 = status.StatusList(**self.kwargs)
        
        self.kwargs["statuses"] = [
            status.Status(name="Started", code="STRT"),
            status.Status(name="Waiting For Approve", code="WAPPR"),
            status.Status(name="Approved", code="APPR"),
            status.Status(name="Finished", code="FNSH"),
        ]
        
        status_list4 = status.StatusList(**self.kwargs)
        
        self.assertFalse(status_list1!=status_list2)
        self.assertTrue(status_list1!=status_list3)
        self.assertTrue(status_list1!=status_list4)
    
    
    
    #----------------------------------------------------------------------
    def test_indexing_get(self):
        """testing indexing of statuses in the statusList, get
        """
        # first try indexing
        
        # this shouldn't raise a TypeError
        status1 = self.mock_status_list[0]
        
        # check the equality
        self.assertEquals(self.mock_status_list.statuses[0], status1)
    
    
    
    #----------------------------------------------------------------------
    def test_indexing_set(self):
        """testing indexing of statuses in the statusList, set
        """
        # first try indexing
        
        # this shouldn't raise a TypeError
        status1 = self.mock_status_list[0]
        
        self.mock_status_list[-1] = status1
        
        # check the equality
        self.assertEquals(self.mock_status_list.statuses[-1], status1)
    
    
    
    #----------------------------------------------------------------------
    def test_indexing_del(self):
        """testing indexing of statuses in the statusList, del
        """
        
        # first get the lenght
        len_statuses = len(self.mock_status_list.statuses)
        
        
        del self.mock_status_list[-1]
        
        self.assertEquals(len(self.mock_status_list.statuses),
                          len_statuses-1)
    
    
    
    #----------------------------------------------------------------------
    def test_indexing_len(self):
        """testing indexing of statuses in the statusList, len
        """
        
        # get the len and compare it wiht len(statuses)
        self.assertEquals(len(self.mock_status_list.statuses),
                          len(self.mock_status_list))
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_argument_being_empty_string(self):
        """testing if a ValueError will be raised when the target_entity_type
        argument is given as None
        """
        
        self.kwargs["target_entity_type"] = ""
        self.assertRaises(ValueError, status.StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_argument_being_None(self):
        """testing if a ValueError will be raised when the target_entity_type
        argument is given as None
        """
        
        self.kwargs["target_entity_type"] = None
        self.assertRaises(ValueError, status.StatusList, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_target_entity_type_property_read_only(self):
        """testing if a ValueError will be raised when the target_entity_type
        argment is tried to be set
        """
        
        # try to set the target_entity_type attribute and expect AttributeError
        self.assertRaises(
            AttributeError,
            setattr,
            self.mock_status_list,
            "target_entity_type",
            "Sequence"
        )
    
    
    
    
    
    