from unittest import TestCase

from git_wrapper import *

class TestResource(ModuleSpecificTestCase):
    def __init__(self):
        super(TestRepository, self).__init__()

    # setup, runtest, takedown
    def setup(self):
        repo = Repository("/Users/jwl/Documents/univ")
        self.fail()
        
        
        


if __name__=='__main__':
    unittest.main()


