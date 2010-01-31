from unittest import TestCase

from git_wrapper import *

class TestUser(ModuleSpecificTestCase):
    def __init__(self):
        super(TestRepository, self).__init__()

    # setup, runtest, takedown
    def setup(self):
        repo = Repository("/Users/jwl/Documents/univ")
        rev = repo.get_latest_revision()
        revprop = rev.get_properties()
        user = revprop.get_committer()
        return user
    
    def testGetName(self):
        r = self.setup()
        r.author
    
        


if __name__=='__main__':
    unittest.main()


