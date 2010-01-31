from subvertpy import repos, ra, NODE_DIR, NODE_FILE

class Path(object):
    """ A path to a versioned resource """
    def __init__(self, ra_api=None, revision=None, branch_path=None, node_path=None):
        super(Path, self).__init__()

        self._ra_api = ra_api
        self._branch_path = branch_path
        self._node_path = node_path
        self._revnum = revision
    
    def get_resource(self, revision, branch_path=None, node_path=None):
        """ Return the versioned resource at this path at the given revision or None """

        kind = self._ra_api.check_path(os.path.join(self._branch_path, self._node_path), self._revnum)
        kinds = {NODE_FILE: File, NODE_DIR: Tree}

        if kind in kinds:
            return kinds[kind](self._branch_path, self._node_path, self._ra_api, self._revnum)
        else:
            return None

    resource = property(get_resource)


