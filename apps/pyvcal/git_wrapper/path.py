class Path(object):
    """A path to a versioned resource."""
    
    def __init__(self, repo=None, branch=None, node_path=None):
        # self._rev = rev # Revision object
        self.repo = repo
        # self._id = self._rev.identity
        # self._branch = branch
        # self._node_path = node_path
    
    def get_resource(self, revision):
        """Return the versioned resource at this path at the given revision or None"""
        
        
    resource = property(get_resource)
