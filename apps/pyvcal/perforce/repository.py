from __future__ import with_statement

from .revision import Revision
from .branch import Branch
from .p4client import P4Client

import os # For repository creation :(
import subprocess

import re
class Repository(object):
    """A Perforce repository. """    
    def __init__(self, user=None, password=None, host=None, port=str(1666), client=None, cwd=None, depot="depot"):
        """Initialize a Perforce repository. Perforce has defaults for everything.
        
        A PyVCAL repository maps to a Perforce depot. Thus a single p4d
        instance may require multiple Repository instances."""
        super(Repository, self).__init__()
        
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._client = client
        self._cwd = cwd
        self._depot = depot

    def _init_client(self):
        return P4Client(self._user, self._password, self._host, self._port, self._client, self._cwd)

    def get_uri(self):
        """Return the URI of the repository"""
        with self._init_client() as p4c:
            return p4c.host + ":" + p4c.port
        
    def get_branches(self):
        """Return the branches available in the repository.
        
        A PyVCAL branch maps to a Perforce codeline, assumed to be a folder
        in the root of the depot.
        """
        
        with self._init_client() as p4c:
            raw_change_list = p4c.run("files", self._depot_path())
        
        r = re.compile(r"//%(depot)s/([^/]+)/.*" % {'depot' : self._depot})
        
        branches = {}
        for change in raw_change_list:
            m = r.match(change['depotFile'])
            # File in folder
            if m:
                name = m.group(1)
                branches.setdefault(name, Branch(repo=self, name=name))
            # File in depot root, treat depot root as a branch
            else:
                branches.setdefault("", Branch(repo=self, name=""))

        return branches
        
    def _depot_path(self):
        return "//%(depot)s/..." % {'depot' : self._depot}
        
    def get_revisions(self):
        """Return the Revision objects available in this repository"""
        with self._init_client() as p4c:
            raw_changes = p4c.run("changes")
            raw_revisions = [Revision(self, c) for c in raw_changes]
            result = {}
            for r in raw_revisions:
                result[r.properties.revision_id] = r   
            return result

    ## Meaningless URI for the perforce repository
    uri = property(get_uri)
    
    ## Logical branches in the perforce repository
    branches = property(get_branches) 
    
    ## Global revisions in the perforce repository
    revisions = property(get_revisions)

    @classmethod
    def create(cls,**kwargs):
        """Create a new Repository and return it."""
        p4d = subprocess.Popen(['p4d'], stdout=subprocess.PIPE)
        
        repo = Repository()
        
        repo.p4d = p4d
        
        return repo
        
