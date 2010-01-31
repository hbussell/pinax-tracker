from datetime import datetime

class RevisionProperties(object):
    """Metadata for a revision"""
    def __init__(self, revision, p4dict):
        """Initialize a RevisionProperties based on a P4API dict."""
        super(RevisionProperties, self).__init__()
        self._revision = revision
        self._commit_msg = p4dict['desc']
        self._time = datetime.fromtimestamp(float(p4dict['time']))
        self._committer = p4dict['user']
        self._revision_id = p4dict['change']
        
    def get_revision(self):
        """Return the revision to which these properties apply."""
        return self._revision
        
    def get_commit_message(self):
        """Return a unicode string containing the commit message for the Revision."""
        return self._commit_msg
        
    def get_committer(self):
        """Get the User who committed the Revision"""
        return self._committer
        # TODO Return User object here
        
    def get_time(self):
        """Return the (TODO dataformat) of the revision"""
        return self._time
        # TODO Return properly formatted time
        
    def get_revision_id(self):
        """Return the revision identifier for the revision."""
        return self._revision_id
        
    ## See get_revision
    revision = property(get_revision)
    
    ## See get_commit_message
    commit_message = property(get_commit_message)
    
    ## See get_committer
    committer = property(get_committer)
    
    ## See get_time
    time = property(get_time)
    
    ## See get_revision_id
    revision_id = property(get_revision_id)
