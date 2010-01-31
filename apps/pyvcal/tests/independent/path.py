import modulespecific
import unittest

class TestPath(modulespecific.ModuleSpecificTestCase):
    """Test the Path interface."""        
    def setUp(self):
        """Create and connect to a repository."""
        self.basic_repo = self.test_module.BasicRepository()
        self.repo = self.basic_repo.repo()

# TODO : How do we get to resources and paths from a repository??        
        
        
    def tearDown(self):
        """Destroy the created repository."""
        self.basic_repo.teardown()

class TestPathResource(TestPath):
    """Test Path.resource"""
    def runTest(self):
        """Test that the get_resource() returns the Resource associated with
           this path."""
        self.fail("Not implemented yet.")
        #r_path = self.resource.path
        #self.assertEquals(r_path.resource, self.resource)
        
