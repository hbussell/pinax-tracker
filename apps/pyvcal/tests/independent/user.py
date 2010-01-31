import modulespecific
import unittest

class TestUser(modulespecific.ModuleSpecificTestCase):
    """Test the Repository interface."""        
    def setUp(self):
        """Create and connect to a repository."""
        self.basic_repo = self.test_module.BasicRepository()
        self.repo = self.basic_repo.repo()
        
        self.revisions = self.repo.revisions
        self.head = self.repo.branches[""].head
        self.properties = self.head.properties

    def tearDown(self):
        """Destroy the created repository."""
        self.basic_repo.teardown()

class TestUserAuthor(TestUser):
    """Test Repository.revisions"""
    def runTest(self):
        """Test that the 'basic' test repository get_user returns a non - null author."""
        author = self.properties.committer
        self.assert_(author)
