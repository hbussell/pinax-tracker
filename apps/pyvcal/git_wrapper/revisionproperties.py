# from .revision import Revision
# from pyvcal.git_wrapper.revision import Revision

from .user import User
import datetime
import time

class RevisionProperties(object):
    """Metadata for a revision"""
    def __init__(self, id_hash, repo, rev):
        """Initialize a RevisionProperties based on provided Git commit ID hash"""
        super(RevisionProperties, self).__init__()
        self._id = id_hash # should be a 40char git commit hash id
        self._repo = repo # repo this belongs to, git.Repo obj
        self._rev = rev
        self._path = self._repo.path
    
    def get_revision(self):
        """Return the Revision obj to which these properties apply."""
        return self._rev
        
    def get_commit_message(self):
        """Return a unicode string containing the commit message for the Revision."""
        # return self._log
        return self._repo.commit(self._id).message

        
    def get_committer(self):
        """Get the User who committed the Revision"""
        return User(self._repo.commit(self._id).committer.name)
        
    def get_time(self):
        """Return the python timedate obj of the revision"""
        # relies on Revision to pass along the python timedate obj
        repotime = self._repo.commit(self._id).committed_date # time.time_struct
        return datetime.datetime.fromtimestamp(time.mktime(repotime))
    
    def get_revision_id(self):
        """Return the revision identifier of the revision."""
        return self._id
    
    revision = property(get_revision)
    commit_message = property(get_commit_message)
    committer = property(get_committer)
    time = property(get_time)
    revision_id = property(get_revision_id)

class ResourceProperties(object):
    pass

class FileProperties(ResourceProperties):
    """ The properties of a File """

    def __init__(self, id_hash=None, repo=None, rev=None, path=None):
        super(FileProperties, self).__init__()
        self._id = id_hash # should be a 40char git commit hash id
        self._repo = repo # repo this belongs to
        self._rev = rev
        self._path = path    

    def _get_type(self):
        """ Return the type of this Resource """
        return 'file'


class TreeProperties(ResourceProperties):
    """ The properties of a Tree """
    def __init__(self, id_hash=None, repo=None, rev=None, path=None):
        super(TreeProperties, self).__init__()
        self._id = id_hash # should be a 40char git commit hash id
        self._repo = repo # repo this belongs to
        self._rev = rev
        self._path = path   

    def _get_type(self):
        """ Return the type of this Resource """
        return 'directory'
