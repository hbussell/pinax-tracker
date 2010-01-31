from unittest import TestCase

from git_wrapper import *

class TestResource(ModuleSpecificTestCase):
    def __init__(self):
        super(TestRepository, self).__init__()

    # setup, runtest, takedown
    def setup(self):
        repo = Repository("/Users/jwl/Documents/univ")
        rev = repo.get_latest_revision()
        prop = rev.get_properties()
    
    def testCreation(self):
        p = self.setup()
        
    def testGetRevision(self):
        p = self.setup()
        p.get_commit_message()
        
    def testGetCommitter(self):
        p = self.setup()
        p.get_committer()
        p.get_committer().author
    
    def testCommitTime(self):
        p = self.setup()
        p.get_time()
    
    def testGetRevisionID(self):
        p = self.setup()
        p.get_revision_id()


if __name__=='__main__':
    unittest.main()


