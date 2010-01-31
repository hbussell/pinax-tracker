import difflib
 
class RevisionDiff(object):
    """The set of changes needed to transform one revision into another."""

    def get_value(self, data1, data2):
        """Concatenation of Unified Diffs of resources between the revisions."""
        # this will need to be changed as we figure out how this will be used
        # result is a Generator class - i.e. you can do the following:
        # for line in result:
        #     print line
        result = difflib.unified_diff(data1, data2)
        
        # if you don't like the below, you can instead write:
        # string.join(result, '')
        return ''.join(result)
        
    value = property(get_value)