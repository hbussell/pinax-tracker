from unittest import TestCase

# from git_wrapper import *
from pyvcal import git_wrapper

path = os.path.join(os.path.dirname(__file__), '..', 'repositories', 'git')

class TestRepository(ModuleSpecificTestCase):
    def __init__(self):
        super(TestRepository, self).__init__()

    # setup, runtest, takedown
    def setup(self):
        vcs_api = pyvcal.get_api('git')
        repo = vcs_api.Repository(os.path.join(path, 'testrepo01'))
        return repo

    # DEPRECATED by git_wrapper.test_create()
    # def testCreation(self):
    #     r = self.setup()
        
    def testGetURI(self):
        r = self.setup()
        self.assertEqual(r.get_uri(), os.path.join(path, 'testrepo01'))
    

    def testGetLatestRevision(self):
        r = self.setup()
        r.get_latest_revision()
    
    def testGetRevisions(self):
        r = self.setup()
        r.get_revisions()
    
    def testGetBranches(self):
        r = self.setup()
        r.get_branches()
        
    def teardown(self):
        rmrf(os.path.join(path, 'testrepo01'))
        


if __name__=='__main__':
    unittest.main()


