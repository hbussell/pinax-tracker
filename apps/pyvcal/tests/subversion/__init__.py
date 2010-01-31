from unittest import TestSuite

import os
import subprocess

import pyvcal
from ...util import rmrf


api = pyvcal.get_api('subversion')

path = os.path.join(os.path.dirname(__file__), '..', 'repositories', 'subversion')

class BasicRepository(object):
    """Represents our 'basic' test repository"""
    def __init__(self):
        super(BasicRepository, self).__init__()
        os.chdir(path)
        subprocess.Popen(['bash', 'create_basic_repository.sh'], 
                         stdout=subprocess.PIPE).wait()
        
    def repo(self):
        """Return the PyVCAL Repository"""
        return api.Repository(path="file://" + os.path.join(path, 'svn-basic'))

    def teardown(self):
        rmrf(os.path.join(path, 'svn-basic'))
        rmrf(os.path.join(path, 'repo01'))

test_subversion = TestSuite()

def test_create(testinstance):
    repo = api.Repository.create(os.path.join(path, 'repo01'))
    testinstance.assert_(repo)
