class Revision(object):
    """The complete state of a branch at a given time"""

    def get_predecessors(self):
        """Return a list of Revisions that flow into this Revision"""
        raise NotImplementedError 
        
    def get_properties(self):
        """Get the RevisionProperties for this revision."""
        raise NotImplementedError
        
    def get_diff_with_parent(self, paths=None):
        """Return the RevisionDiff from this revision to its parent, optionally restricted to the given file(s) on paths
        
        If there is more than one parent, this method may return a fake RevisionDiff with no content to represent a merge.
        """
        raise NotImplementedError
        
    @classmethod
    def diff(cls, src, dst, paths=None):
        """Return the RevisionDiff from Revision src to Revision dst, optionally restricted to the given file(s) on paths"""
        raise NotImplementedError 

    predecessors = property(get_predecessors)
    properties = property(get_properties)
    diff_with_parent = property(get_diff_with_parent)
