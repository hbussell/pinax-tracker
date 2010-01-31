from .revisionproperties import RevisionProperties
from .tree import Tree
from .file import File
from .revisiondiff import RevisionDiff

class Revision(object):
    """The complete state of a branch at a given time"""
    
    def __init__(self, rev_id, repo):
        # all we need is the hash and repo; we let gitpython do the rest
        """Initialize a complete Git delta (analogous to a SVN revision or Perforce changeset)"""
        super(Revision, self).__init__()
        self._rev_id = rev_id
        self._repo = repo
        self._git_commit = self._repo.commit(self._rev_id)

    def get_predecessors(self):
        """Return a list of immediate Revisions that flow into this Revision"""
        parent_list = self._git_commit.parents # analogous to git.Commit[]
        predecessor_list = list(Revision(p.id, p.repo) for p in parent_list)
        return predecessor_list
        
    def get_properties(self):
        """Get the RevisionProperties for this revision."""
        return RevisionProperties(self._rev_id, self._repo, self)
        
    def get_diff_with_parent(self, paths=None):
        """Return the RevisionDiff from this revision to its parent, optionally restricted to the given file(s) on paths
        
        If there is more than one parent, this method may return a fake RevisionDiff with no content to represent a merge.
        """
        # Will return git.diff object until pyvcal.diff is formalized
        return self.diff(self, self.get_predecessors()[0])
        
    def _get_tree(self):
        """Return Tree object representing top-level contents"""
        return Tree(self._git_commit.tree, self._repo)
        
    def _get_identity(self):
        """Return revision ID of this revision; will be a 40-char hash"""
        return self._rev_id
   
    def get_repo(self):
        """Return associated repository"""
        return self._repo

    def get_git_commit(self):
        """Return associated git.Commit obj"""
        return self._git_commit

        
    @classmethod
    def diff(cls, a, b, paths=None):
        """Return the RevisionDiff from Revision src to Revision dst, optionally restricted to the given file(s) on paths"""
        return RevisionDiff(a, b, a.get_repo())
    
    predecessors = property(get_predecessors)
    properties = property(get_properties)
    diff_with_parent = property(get_diff_with_parent)
    tree = property(_get_tree)
    identity = property(_get_identity)
