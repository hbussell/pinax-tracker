## \brief  A coherent set of data that evolve together
class Branch(object):
    """A coherent set of data that evolves together"""
    
    def get_head(self):
        """Return the latest Revision in the branch"""
        raise NotImplementedError 
        
    def get_name(self):
        """Return the user-defined name of the branch"""
        raise NotImplementedError 

    ## The latest revision in the branch.
    head = property(get_head)
    
    ## The user-specified name of the branch.
    name = property(get_name)
