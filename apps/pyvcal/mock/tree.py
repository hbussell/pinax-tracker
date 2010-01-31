from mock import Mock
from pyvcal.resource import Resource

class Tree(Resource):
    """A versioned container of Files"""

    def __init__(self, path, contents):
        self.mock = Mock({"get_path": path,
                          "get_contents": contents})

    def get_path(self):
        """Return the path to this tree in its container Repository"""
        return self.mock.get_path()
        
    def get_contents(self, recursive=True):
        """Return the contents of a tree as a list of Resources."""
        return self.mock.get_contents()
    
    def get_mock(self):
        """Return the Mock object that is used in Repository. This could
        be used for adding expectations or performing other checks on Mock.
        Refer to http://python-mock.sourceforge.net/ for more details"""
        return self.mock
        
    path = property(get_path)
    contents = property(get_contents)
