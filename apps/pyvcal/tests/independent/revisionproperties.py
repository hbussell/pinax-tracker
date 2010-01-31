import modulespecific
import unittest

class TestRevisionProperties(modulespecific.ModuleSpecificTestCase):
    """Test the RevisionProperties interface."""        
    def setUp(self):
        """Create and connect to a repository."""
        self.basic_repo = self.test_module.BasicRepository()
        self.repo = self.basic_repo.repo()
                
        # Get the latest revision from that repository.
        self.revisions = self.repo.revisions
        self.head = self.repo.branches[""].head
        self.properties = self.head.properties
        
    def tearDown(self):
        """Destroy the created repository."""
        self.basic_repo.teardown()

class TestRevisionPropertiesRevision(TestRevisionProperties):
    """Test RevisionProperties.revision"""
    def runTest(self):
        """Test that the latest revision matches containing this properties is 
           the same object."""
        latest_rev = self.properties.revision
        self.assertEquals(latest_rev, self.head)

class TestRevisionPropertiesCommitMessage(TestRevisionProperties):
    """Test RevisionProperties.commit_message"""
    def runTest(self):
        """Test that the 'basic' test RevisionProperties reports the correct commit message."""
        commit_msg = self.properties.commit_message
        self.assertEquals(commit_msg, "Delete README")
        
class TestRevisionPropertiesCommitter(TestRevisionProperties):
    """Test RevisionProperties.committer"""
    def runTest(self):
        """Test that the 'basic' test RevisionProperties reports committer as not null."""
        committer = self.properties.committer
        self.assert_(committer)
        
class TestRevisionPropertiesTime(TestRevisionProperties):
    """Test RevisionProperties.time"""
    def runTest(self):
        """Test that the 'basic' test RevisionProperties reports time as not null."""
        rtime = self.properties.time
        self.assert_(rtime)    

class TestRevisionPropertiesRevisionID(TestRevisionProperties):
    """Test RevisionProperties.revision_id"""
    def runTest(self):
        """Test that the 'basic' test RevisionProperties reports revision_id as not null."""
        r_id = self.properties.revision_id
        self.assert_(r_id)
