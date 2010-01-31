from __future__ import with_statement

from .revisionproperties import RevisionProperties

class Revision(object):
    """The complete state of a branch at a given time"""
    def __init__(self, repo, p4dict):
        """Initialize a complete Perforce changeset."""
        super(Revision, self).__init__()
        self._properties = RevisionProperties(self, p4dict)
        self._repo = repo
        
        self._cached_files = None
        
    def get_predecessors(self):
        """Return a list of Revisions that flow into this Revision"""
        raise NotImplementedError 
        
    def get_properties(self):
        """Get the RevisionProperties for this revision."""
        return self._properties
        
    def get_diff_with_parent(self, paths=None):
        """Return the RevisionDiff from this revision to its parent, optionally restricted to the given file(s) on paths
        
        If there is more than one parent, this method may return a fake RevisionDiff with no content to represent a merge.
        """
        raise NotImplementedError
        
    def _files(self):
        if not self._cached_files:
            with self._repo._init_client() as p4c:
                self._cached_files = p4c.run("files", self._repo._depot_path() + "@" + self.properties.revision_id)
                
        return self._cached_files
        
    @classmethod
    def diff(cls, src, dst, paths=None):
        """Return the RevisionDiff from Revision src to Revision dst, optionally restricted to the given file(s) on paths"""
        path = self._repo._depot_path()
        # TODO paths format
            
        with self._repo._init_client() as p4c:
            oldtaggedvalue = p4c.tagged
            diff = '\n'.join(p4c.run("diff2", 
                                       "-u", 
                                       path + "@" + src.properties.revision_id,
                                       path + "@" + dst.properties.revision_id))
            p4c.tagged = oldtaggedvalue
        
            return RevisionDiff(diff)


    ## Predecessor revisions of a revision
    predecessors = property(get_predecessors)
    
    ## Properties of a revision
    properties = property(get_properties)
    
    ## Diff between this revision and its parent. Will be a fake for revisions with multiple parents.
    diff_with_parent = property(get_diff_with_parent)


   ########################
   # Perforce file actions:
   #    add
   #    edit
   #    branch
   #    delete
   #    integrate
   
