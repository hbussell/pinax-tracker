import modulespecific
import unittest

class TestFile(modulespecific.ModuleSpecificTestCase):
    """Test the File interface."""        
    def setUp(self):
        """Create and connect to a repository."""
        self.basic_repo = self.test_module.BasicRepository()
        self.repo = self.basic_repo.repo()
                
        """Get the latest revision from that repository."""
        self.revisions = self.repo.revisions
        self.head = self.repo.branches[""].head
        #self.resource = self.head.get_resource()
        
    def tearDown(self):
        """Destroy the created repository."""
        self.basic_repo.teardown()

class TestFileData(TestFile):
    """Test File.data"""
    def runTest(self):
        """Test that the get_data() returns the contents of the Resource in
           question."""
        #self.assertTrue(self.resource)
        #contents = self.resource.data
        #self.assert_(contents)
        self.fail("Not implemented yet")
        
