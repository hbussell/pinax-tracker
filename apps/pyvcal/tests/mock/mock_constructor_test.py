import mock.mock_constructor as mc
import mock.repository as repository

import unittest
import yaml


def load_yaml(path):
    """ Convenience method for writing test cases. This will convert a string 
    in YAML syntax into a python object """
    fsock = open(path)
    
    try:
        yaml_string = fsock.read()
        yaml_obj = yaml.load(yaml_string)
        
    finally:
        fsock.close()

    return yaml_obj


class Mock_Constructor_Test(unittest.TestCase):
    
    def setUp(self):
        self.fixture = load_yaml('test_fixtures.yaml')
    
    def test_process_repository_basic(self):
        repo_dict = self.fixture['testrepo1']
        repo = mc.process_repository(repo_dict[mc.REPOSITORY_KEY])
        
        self.assertEquals({}, repo.get_branches())
        self.assertEquals({}, repo.get_revisions())
        self.assertEquals('http://www.somesvnpath.com/svn', repo.get_uri())
        
        
    def test_process_repository(self):
        repo_dict = self.fixture['testrepo2']
        repo = mc.process_repository(repo_dict[mc.REPOSITORY_KEY])
        
        self.assertEquals({'branch1': None, 'branch2': None}, repo.get_branches())
        self.assertEquals({}, repo.get_revisions())
        self.assertEquals('http://www.somesvnpath.com/svn2', repo.get_uri())
        
        
    def test_process_repository_with_revisions(self):
        repo_dict = self.fixture['testrepo3']
        repo = mc.process_repository(repo_dict[mc.REPOSITORY_KEY])
        
        self.assertEquals({'branch1': None, 'branch2': None}, repo.get_branches())
        self.assertEquals({'revision1': None, 'revision2': None}, repo.get_revisions())
        self.assertEquals('http://www.somesvnpath.com/svn3', repo.get_uri())
        
        
    def test_process_branch_simple(self):
        branch_dict = self.fixture['testbranch1']
        empty_repo = repository.Repository('some_svn_path')
        
        mc.process_branch(branch_dict[mc.BRANCH_KEY], empty_repo)
        
        branch1 = empty_repo.get_branches()['branch1']
        self.assertEquals('branch1', branch1.get_name())
        self.assertEquals('revision5', branch1.get_head())
        
        
    def test_process_branch_multiple(self):
        branch_dict = self.fixture['testbranch2']
        empty_repo = repository.Repository('some_svn_path')
        
        mc.process_branch(branch_dict[mc.BRANCH_KEY], empty_repo)
        
        branch1 = empty_repo.get_branches()['branch1']
        branch3 = empty_repo.get_branches()['branch3']
        branch6 = empty_repo.get_branches()['branch6']
        
        self.assertEquals('branch1', branch1.get_name())
        self.assertEquals('revision5', branch1.get_head())
        
        self.assertEquals('branch3', branch3.get_name())
        self.assertEquals('revision35', branch3.get_head())
        
        self.assertEquals('branch6', branch6.get_name())
        self.assertEquals('revision1', branch6.get_head())
    
    def test_process_branch_with_repo(self):
        branch_dict = self.fixture['testbranch2']
        repo_dict = self.fixture['testrepo3']
        
        repo = mc.process_repository(repo_dict[mc.REPOSITORY_KEY])
        mc.process_branch(branch_dict[mc.BRANCH_KEY], repo)
        
        branch1 = repo.get_branches()['branch1']
        branch2 = repo.get_branches()['branch2']
        branch3 = repo.get_branches()['branch3']
        
        self.assertEquals('branch1', branch1.get_name())
        self.assertEquals('revision5', branch1.get_head())
        
        self.assertEquals(None, branch2)
        
        self.assertEquals('branch3', branch3.get_name())
        self.assertEquals('revision35', branch3.get_head())
        
    def test_process_revision_simple(self):
        revision_dict = self.fixture['testrevision1']
        empty_repo = repository.Repository('some_svn_path')
        
        mc.process_revision(revision_dict, empty_repo)
        
        revision1 = empty_repo.get_revisions()['revision1']
        
        self.assertEquals([], revision1.get_predecessors())
        self.assertEquals(['ignore'], revision1.get_properties())
        self.assertEquals(None, revision1.get_diff_with_parent())
        
    def test_process_revision(self):
        revision_dict = self.fixture['testrevision2']
        empty_repo = repository.Repository('some_svn_path')
        
        mc.process_revision(revision_dict, empty_repo)
        
        revision6 = empty_repo.get_revisions()['revision6']
        
        self.assertEquals(['revision5', 'revision4'], revision6.get_predecessors())
        self.assertEquals(None, revision6.get_properties())
        self.assertEquals(['diffobject'], revision6.get_diff_with_parent())