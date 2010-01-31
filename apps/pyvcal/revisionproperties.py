class RevisionProperties(object):
    """Metadata for a revision"""
    
    def get_revision(self):
        """Return the revision to which these properties apply."""
        pass
        
    def get_commit_message(self):
        """Return a unicode string containing the commit message for the Revision."""
        pass
        
    def get_committer(self):
        """Get the User who committed the Revision"""
        pass
        
    def get_time(self):
        """Return the datetime of the revision"""
        pass
    
    def get_revision_id(self):
        """Return the revision identifier of the revision."""
        pass
    
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
