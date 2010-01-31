from .revisionproperties import RevisionProperties
from mock import Mock

class Revision(object):
    """The complete state of a branch at a given time"""

    def __init__(self, predecessors=[], properties=None, diffWithParent=None):
        super(Revision, self).__init__()
        self.mock = Mock({"get_predecessors": predecessors,
                          "get_properties": properties,
                          "get_diff_with_parent": diffWithParent})

    def get_predecessors(self):
        """Return a list of Revisions that flow into this Revision"""
        return self.mock.get_predecessors()
        
    def get_properties(self):
        """Get the RevisionProperties for this revision."""
        return self.mock.get_properties()
        
    def get_diff_with_parent(self, paths=None):
        """Return the RevisionDiff from this revision to its parent, optionally restricted to the given file(s) on paths
        
        If there is more than one parent, this method may return a fake RevisionDiff with no content to represent a merge.
        """
        return self.mock.get_diff_with_parent()
    
    def get_mock(self):
        """Return the Mock object that is used in Repository. This could
        be used for adding expectations or performing other checks on Mock.
        Refer to http://python-mock.sourceforge.net/ for more details"""
        return self.mock
    
    @classmethod
    def diff(cls, src, dst, paths=None):
        """Return the RevisionDiff from Revision src to Revision dst, optionally restricted to the given file(s) on paths"""
        raise NotImplementedError 

    predecessors = property(get_predecessors)
    properties = property(get_properties)
    diff_with_parent = property(get_diff_with_parent)
