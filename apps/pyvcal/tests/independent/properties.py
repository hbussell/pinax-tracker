import modulespecific
import unittest

class TestProperties(modulespecific.ModuleSpecificTestCase):
    """Test the Properties interface."""        
    def setUp(self):
        """Create and connect to a repository."""
        self.basic_repo = self.test_module.BasicRepository()
        self.repo = self.basic_repo.repo()
                
        """Get the latest revision from that repository."""
        self.revisions = self.repo.revisions
        self.head = self.repo.branches[""].head
#        self.resource = self.head.get_resource()
        
    def tearDown(self):
        """Destroy the created repository."""
        self.basic_repo.teardown()

class TestPropertiesResourceProperties(TestProperties):
    """Test resource.properties"""
    def runTest(self):
        """Test that the get_properties() returns the properties associated 
           with the Resource in question."""
#        props = self.resource.properties
#        self.assertTrue(props)
        self.fail("Not implemented yet.")
