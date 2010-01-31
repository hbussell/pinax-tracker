import modulespecific
import unittest

class TestBasic(modulespecific.ModuleSpecificTestCase):
    """Basic sanity test for each VCS."""        

    def setUp(self):
        """Initialize a repository to use"""
        self.basic_repo = self.test_module.BasicRepository()
        self.repo = self.basic_repo.repo()

    def runTest(self):
        """Check that the api responds."""
        self.assertTrue(self.repo)
        revisions = self.repo.revisions
        self.assertEquals(len(revisions), 4)
        
    def tearDown(self):
        """Destroy the created repository."""
        self.basic_repo.teardown()
        
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    