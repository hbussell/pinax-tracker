from mock import Mock, PerpetualReturnValues

class Repository(object):
    """A container for codelines"""
    
    # This code is necessary to mimic the ability to reconnect to the same
    # repository. Each repository must have a unique path
    repository = {}
    
    def __init__(self, path, branches={}, revisions={}, new_repo=False):
        if new_repo or path not in self.__class__.repository:
            super(Repository, self).__init__()
            mock = Mock({"get_uri": path,
                         "get_branches": PerpetualReturnValues(branches),
                         "get_revisions": PerpetualReturnValues(revisions)})
            self.__class__.repository[path] = mock
        
        self.mock = self.__class__.repository[path]
    
    def get_uri(self):
        """Return the URI of the repository"""
        return self.mock.get_uri()
        
    def get_branches(self):
        """Return the branches available in the repository"""
        return self.mock.get_branches()
        
    def get_revisions(self):
        """Return the Revision objects available in this repository"""
        return self.mock.get_revisions()
    
    def get_mock(self):
        """Return the Mock object that is used in Repository. This could
        be used for adding expectations or performing other checks on Mock.
        Refer to http://python-mock.sourceforge.net/ for more details"""
        return self.mock
    
    uri = property(get_uri)
    branches = property(get_branches)
    revisions = property(get_revisions)
    
    @classmethod
    def create(cls,**kwargs):
        """Create a new Repository and return it."""
        raise NotImplementedError
