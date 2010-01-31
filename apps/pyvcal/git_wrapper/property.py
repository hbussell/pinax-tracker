class Properties(object):
    """ Properties of a versioned object """

    def __init__(self, resource=None, id_hash, rev, path=None):
        super(Properties, self).__init__()
        self._resource = resource
        self._id = id_hash
        self._repo = repo
        self._path = path       
    
