class FileDiff(object):
    """The set of changes needed to transform one revision of a file to another."""

    def __init__(self, file1=None, file2=None):
        super(FileDiff, self).__init__()
        
        self._file1 = file1
        self._file2 = file2
    
#    def apply_to(self, file):
#        """Apply this FileDiff to a File and return the transformed file."""
#        raise NotImplementedError 
