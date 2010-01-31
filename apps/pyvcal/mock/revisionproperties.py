from mock import Mock

class RevisionProperties(object):
    """Metadata for a revision"""
    
    def __init__(self, revision=None, commitMsg='', committer='', time=None, 
                 revId=0):
        self.mock = Mock({"get_revision": revision,
                          "get_commit_message": commitMsg,
                          "get_committer": committer,
                          "get_time": time,
                          "get_revision_id": revId})
    
    def get_revision(self):
        """Return the revision to which these properties apply."""
        return self.mock.get_revision()
        
    def get_commit_message(self):
        """Return a unicode string containing the commit message for the Revision."""
        return self.mock.get_commit_message()
        
    def get_committer(self):
        """Get the User who committed the Revision"""
        return self.mock.get_committer()
        
    def get_time(self):
        """Return the (TODO dataformat) of the revision"""
        return self.mock.get_time()
    
    def get_revision_id(self):
        """Return the revision identifier of the revision."""
        return self.mock.get_revision_id()
    
    def get_mock(self):
        """Return the Mock object that is used in Repository. This could
        be used for adding expectations or performing other checks on Mock.
        Refer to http://python-mock.sourceforge.net/ for more details"""
        return self.mock
    
    revision = property(get_revision)
    commit_message = property(get_commit_message)
    committer = property(get_committer)
    time = property(get_time)
    revision_id = property(get_revision_id)
