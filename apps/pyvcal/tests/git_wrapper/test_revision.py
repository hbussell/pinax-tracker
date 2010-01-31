from unittest import TestCase

from git_wrapper import *

class TestResource(ModuleSpecificTestCase):
    def __init__(self):
        super(TestRepository, self).__init__()

    # setup, runtest, takedown
    def setup(self):
        repo = Repository("/Users/jwl/Documents/univ")
        rev = repo.get_latest_revision()
        return rev
    
    def testCreation(self):
        r = self.setup()
        
    def testGetPredecessors(self):
        r = self.setup()
        
    def testGetParentDiff(self):
        r = self.setup()
        self.fail()
    
    def testGetDiff(self):
        r = self.setup()
        self.fail()
    
    def testGetTree(self):
        r = self.setup()
        r.tree()
        self.fail()
        
        
        


if __name__=='__main__':
    unittest.main()


