from mock.repository import Repository

import mock.mock_constructor as mc
import unittest

# This file features a very simple example of using mock to test methods that
# relies on a repository

# get_branch is the method to be tested
def get_branch(repo_path, branch):
    """Helper to get Branch for project's repo."""
    repo = Repository(repo_path)
    branches = repo.get_branches()
    if branch not in branches:
        raise StandardError
    return branches[branch]


class Demo(unittest.TestCase):
    
    def test_get_branch1(self):
        # Here we have constructed a repo with the path: http://www.somesvnpath.com/svn
        repo = mc.construct_repository('demo.yaml')
        
        # we are going to get branch1 from the mock repo we just created
        branches = get_branch('http://www.somesvnpath.com/svn', 'branch1')
        
        # assertions, for more complicated methods, additional assertions
        # in mock can be made, such as argument checking.
        mock = repo.get_mock()
        
        # we'll assert the number of calls we've made to get_branches in our repo class in once
        self.assertEquals(len(mock.mockGetNamedCalls('get_branches')), 2)

        # assertion on the branch object we got back matches the one we created
        self.assertEquals(branches.get_name(), 'branch1')
        self.assertEquals(branches.get_head(), 'revision52')

    def test_get_branch2(self):
        repo = mc.construct_repository('demo.yaml')
        
        # assertions using mock
        mock = repo.get_mock()
        self.assertEquals(len(mock.mockGetNamedCalls('get_branches')), 1)
        
        # assert that an error has been raised
        self.assertRaises(StandardError, get_branch, 'http://www.somesvnpath.com/svn', 'branch2')
    
if __name__ == '__main__':
    unittest.main()