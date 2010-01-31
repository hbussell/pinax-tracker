import os

from difflib import Differ
from pprint import pprint

from subvertpy import repos, ra, NODE_DIR, NODE_FILE

class RevisionDiff(object):
    """ The set of changes needed to transform one revision into another """

    def __init__(self, revision1=None, revision2=None):
        super(RevisionDiff, self).__init__()
        
        self._rev1 = revision1
        self._rev2 = revision2
        self.ra_api = self._rev2.get_ra_api()
        
    def get_value(self):
        """Concatenation of Unified Diffs of resources between the revisions."""

        # getting the revision id of the element to be diffed.
        self.rev1_num = self._rev1.properties.revision_id
        self.rev2_num = self._rev2.properties.revision_id
        
        resource1 = str(self._rev1.get_resource().data)
        resource2 = str(self._rev2.get_resource().data)
        
        differ = Differ()
        result = list(differ.compare(resource1, resource2))

        return ''.join(result)
        
    value = property(get_value)


