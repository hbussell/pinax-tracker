from mock import Mock

class User(object):
    """A user in the version control system."""
        
    def __init__(self):
        self.mock = Mock()
        
    def get_mock(self):
        """Return the Mock object that is used in Repository. This could
        be used for adding expectations or performing other checks on Mock.
        Refer to http://python-mock.sourceforge.net/ for more details"""
        return self.mock