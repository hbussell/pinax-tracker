from mock import Mock
from resource import Resource

class File(Resource):
    """A snapshot of a versioned file."""
    
    def __init__(self, data=None):
        super(File, self).__init__()
        self.mock = Mock({"get_data": data})
    
    def get_data(self):
        """Return a binary blob of the file contents"""
        return self.mock.get_data()
    
    def get_mock(self):
        """Return the Mock object that is used in Repository. This could
        be used for adding expectations or performing other checks on Mock.
        Refer to http://python-mock.sourceforge.net/ for more details"""
        return self.mock

    data = property(get_data)
