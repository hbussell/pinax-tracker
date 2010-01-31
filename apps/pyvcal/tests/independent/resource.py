import modulespecific
import unittest

class TestResource(modulespecific.ModuleSpecificTestCase):
    """Test the Resource interface."""        
    def setUp(self):
        """Create and connect to a repository."""
        self.basic_repo = self.test_module.BasicRepository()
        self.repo = self.basic_repo.repo()
                
        """Get the latest revision from that repository."""
        self.revisions = self.repo.revisions
        self.head = self.repo.branches[""].head

        #TODO How do we get to a resource from a repo?
        
    def tearDown(self):
        """Destroy the created repository."""
        self.basic_repo.teardown()

class TestResourceProperties(TestResource):
    """Test resource.properties"""
    def runTest(self):
        """Test that the get_properties() returns the properties associated 
           with the Resource in question."""
        #props = self.resource.properties
        #self.assert_(props)
        #self.assert_(props.path)
        #self.assert_(props.resource)
        #self.assert_(props.revision_number)        
        self.fail("not implemented yet")

class TestResourceLatestRevision(TestResource):
    """Test resource.latest_revision"""
    def runTest(self):
        """Test that the get_latest_revision() returns the latest Revision this
           Resource was modified"""
        #latest_rev = props = self.resource.latest_revision
        #self.assertEquals(latest_rev, self.head)
        self.fail("Not implemented yet")
