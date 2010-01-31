import modulespecific
import unittest

class TestTree(modulespecific.ModuleSpecificTestCase):
    """Test the File interface."""        
    def setUp(self):
        """Create and connect to a repository."""
        self.basic_repo = self.test_module.BasicRepository()
        self.repo = self.basic_repo.repo()
                
        #Get the latest revision from that repository.
        self.revisions = self.repo.revisions
        #self.first = self.revisions[1]
        #self.resource = self.first.get_resource()
        
    def tearDown(self):
        """Destroy the created repository."""
        self.basic_repo.teardown()

class TestTreeContents(TestTree):
    """Test Tree.contents"""
    def runTest(self):
        """Test that the get_contents() returns the contents of the Resource in
           question as a list."""
        #dir_paths = self.resource.contents
        #self.assertNotEqual(len(dir_paths), 0)
        #self.assertTrue(self.resource)
        self.fail("Not implemented yet.")

class TestTreePath(TestTree):
    """Test Tree.path"""
    def runTest(self):
        """Test that the get_path() returns the path of the Resource in 
           question."""
        #self.assertTrue(self.resource)
        #rprop_path = self.resource.properties.path
        #self.assertTrue(rprop_path)        
        self.fail("Not implemented yet.")
