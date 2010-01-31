from mock import Mock

class Resource(object):
    """A versioned object"""
    
    def __init__(self, revision, properties):
        self.mock = Mock({"get_latest_revision": revision,
                          "get_properties": properties})
    
    def get_latest_revision(self):
        """Return the last revision this was modified"""
        return self.mock.get_latest_revision()
        
    def get_properties(self):
        """Return the properties of a resource"""
        return self.mock.get_properties()
    
    def get_mock(self):
        """Return the Mock object that is used in Repository. This could
        be used for adding expectations or performing other checks on Mock.
        Refer to http://python-mock.sourceforge.net/ for more details"""
        return self.mock
    
    latest_revision = property(get_latest_revision)
    properties = property(get_properties)
