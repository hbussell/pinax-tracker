from user import User

class RevisionProperties(object):
    """ Metadata for a revision """
	
    def __init__(self, revision, revnum, author, log, datetime):
        """ Constructor for the svn revision properties """

        super(RevisionProperties, self).__init__()
		
        self._rev = revision
        self._revnum = revnum
        self._author = User(author)
        self._log = log
        self._date = datetime
    
    def get_revision(self):
        """ Return the revision to which these properties apply """
        return self._rev
        
    def get_commit_message(self):
        """ Return a unicode string containing the commit message for the Revision """
        return self._log
        
    def get_committer(self):
        """ Get the User who committed the Revision """
        return self._author.author
        
    def get_time(self):
        """ Return the (TODO dataformat) of the revision """
        return self._date
    
    def get_revision_id(self):
        """ Return the revision identifier of the revision """
        return self._revnum
    
    revision = property(get_revision)
    commit_message = property(get_commit_message)
    committer = property(get_committer)
    time = property(get_time)
    revision_id = property(get_revision_id)
