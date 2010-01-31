import modulespecific
import unittest

class TestRevision(modulespecific.ModuleSpecificTestCase):
    """Test the Revision interface."""        
    def setUp(self):
        """Create and connect to a repository."""
        self.basic_repo = self.test_module.BasicRepository()
        self.repo = self.basic_repo.repo()
                
        """Get the latest revision from that repository."""
        self.revisions = self.repo.revisions
        self.head = self.repo.branches[""].head
        
    def tearDown(self):
        """Destroy the created repository."""
        self.basic_repo.teardown()

class TestRevisionPredecessors(TestRevision):
    """Test Revision.predecessors"""
    def runTest(self):
        """Test that the latest revision returns the expected predecessor i.e: Revision(rev_num - 1)."""
        # PROBLEM: This test fails (at least on git) because there is only ONE
        # revision in the test repo, therefore self.head.properties.time is equal
        # to predecessors[0].properties.time
        predecessors = self.head.predecessors
        self.assertEquals(1, len(predecessors))
        self.assert_(self.head.properties.time > predecessors[0].properties.time)
        self.assertEquals(predecessors[0].properties.commit_message, "Rename README.txt to README")

class TestRevisionGetProperties(TestRevision):
    """Test Revision.properties"""
    def runTest(self):
        """Test that the 'basic' test Revision.properties returns a non-null properties object."""
        props = self.head.properties
        self.assert_(props)
        self.assert_(props.committer)
        self.assert_(props.time)
        self.assert_(props.commit_message)        
        
class TestRevisionDiffWithParents(TestRevision):
    """Test Revision.diff_with_parents"""
    def runTest(self):
        """Test the get diff with parents returns a valid RevisionDiff object."""
        diff = self.head.diff_with_parent
        diff_value = diff.value
        self.assertEquals("", diff_value)
        
        #TODO need a better test... base on branch_and_merge test repo

