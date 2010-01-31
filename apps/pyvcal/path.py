class Path(object):
    """A path to a versioned resource."""
    
    def get_resource(self, revision):
        """Return the versioned resource at this path at the given revision or None"""
        raise NotImplementedError 
        
    resource = property(get_resource)
