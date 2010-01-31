class RevisionDiff(object):
   """The set of changes needed to transform one revision into another."""

   def __init__(self, value):
       super(RevisionDiff, self).__init__()
       self._value = value

   def get_value():
       """Concatenation of Unified Diffs of resources between the revisions."""
       return self._value

   value = property(get_value)
