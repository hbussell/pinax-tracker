class Resource(object):
    """A versioned object"""
    
    def get_latest_revision(self):
        """Return the last revision this was modified"""
        raise NotImplementedError
        
    def get_properties(self):
        """Return the properties of a resource"""
        raise NotImplementedError 
    
    latest_revision = property(get_latest_revision)
    properties = property(get_properties)
