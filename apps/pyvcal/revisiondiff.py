 class RevisionDiff(object):
    """The set of changes needed to transform one revision into another."""

    def get_value():
        """Concatenation of Unified Diffs of resources between the revisions."""
        raise NotImplementedError 

    value = property(get_value)