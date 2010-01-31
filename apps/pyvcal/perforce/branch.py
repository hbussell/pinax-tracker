from __future__ import with_statement

from .revision import Revision

## \brief  A coherent set of data that evolve together
class Branch(object):
    """A coherent set of data that evolves together.
    
    A PyVCAL branch maps to a Perforce codeline.
    
    We assume that each branch gets a folder under the depot root.
    """
    
    def get_head(self):
        """Return the latest Revision in the branch"""
        with self._repo._init_client() as p4c:
            raw_change_list = p4c.run("changes", "-m", "1", "//%(depot)s/%(branch_path)s..." % 
                {'depot' : self._repo._depot, 
                 'branch_path' : self._branch_path()})
                 
            latest_change = raw_change_list[0]
            return Revision(self._repo, latest_change)
            
        
    def get_name(self):
        """Return the user-defined name of the branch"""
        return self._name

    def __init__(self, repo=None, name=None):
        super(Branch, self).__init__()
        self._name = name
        self._repo = repo
        
    def _branch_path(self):
        if self.name is not "":
            return self.name + "/"
        else:
            return self.name

    ## The latest revision in the branch.
    head = property(get_head)
    
    ## The user-specified name of the branch.
    name = property(get_name)
