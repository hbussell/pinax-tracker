from mock import Mock

## \brief  A coherent set of data that evolve together
class Branch(object):
    """A coherent set of data that evolves together"""
    
    def __init__(self, head, name):
        self.mock = Mock({"get_head": head,
                          "get_name": name})
    
    def get_head(self):
        """Return the latest Revision in the branch"""
        return self.mock.get_head()
        
    def get_name(self):
        """Return the user-defined name of the branch"""
        return self.mock.get_name()

    def get_mock(self):
        """Return the Mock object that is used in Repository. This could
        be used for adding expectations or performing other checks on Mock.
        Refer to http://python-mock.sourceforge.net/ for more details"""
        return self.mock

    ## The latest revision in the branch.
    head = property(get_head)
    
    ## The user-specified name of the branch.
    name = property(get_name)
