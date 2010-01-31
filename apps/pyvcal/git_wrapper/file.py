from pyvcal.resource import Resource

class File(Resource):
    """A snapshot of a versioned file."""
    
    def __init__(self, identity, repo):
        # just need hash and repo
        super(File, self).__init__()
        self._id = identity # hash of this object
        self._repo = repo # repository this file belongs to
        self._blob = self._repo.blob(identity) # corresponding git.Blob object

    def _get_size(self):
        """Size of file in bytes"""
        return self._blob.size()

    def get_data(self):
        """Return a str representing binary blob of the file contents"""
        return self._blob.data()

    data = property(get_data)
    size = property(_get_size)

