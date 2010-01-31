class Branch(object):
    """A coherent set of data that evolves together"""
    
    def __init__(self, name, head, repo):
        super(Branch, self).__init__()
        self._name = name # string
        self._head = head # Revision object at head of this branch
        self._repo = repo # repo this belongs to
    
    def get_head(self):
        """Return the latest Revision in the branch (head)"""
        return self._head
        
    def get_name(self):
        """Return the user-defined name of the branch as a string"""
        return self._name

    def set_name(self, name):
        self._name = name
    
    head = property(get_head)
    name = property(get_name, set_name)
