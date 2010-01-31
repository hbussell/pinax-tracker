class Resource(object):
    """Abstract class representing a versioned object"""
    
    def __init__(self, identity, revision, repo, isTree):
        super(Resource, self).__init__()
        self._id = identity # hash of this object
        self._revision = revision # revision this object belongs to
        self._repo = repo # repository this object belongs to
    
    def get_latest_revision(self):
        """Return the last revision this was modified"""
        raise NotImplementedError
        
    def get_properties(self):
        """Return the properties of a resource"""
        raise NotImplementedError 
    
    latest_revision = property(get_latest_revision)
    properties = property(get_properties)
