from revision import Revision

from datetime import datetime

from subvertpy import repos, ra, NODE_NONE, NODE_DIR, NODE_FILE

class Branch(object):
    """ A coherent set of data that evolves together """

    def __init__(self, branch_path, ra_api):
        super(Branch, self).__init__()

        self._branch_path = branch_path
        self._ra_api = ra_api
    
    def get_head(self):
        """ Return the latest Revision in the branch """
        _head = self._ra_api.get_latest_revnum()
        return self._log(path=self._branch_path, rev=_head)[0]
        
    def get_name(self):
        """ Return the user-defined name of the branch i.e. the directory name """
        return self._branch_path

    def _log(self, path='', rev=None):
        """ Return a Revision object scoped to path with revision id as rev """
        self.rev_list = []

        def cb(paths, revnum, props, has_children=False):
            paths = paths or {}
            self.rev_list.append(Revision(revnum,
                            props.get('svn:author', ''),
                            props.get('svn:log', ''),
                            datetime.strptime(
                            props['svn:date'].split('.')[0],
                                 "%Y-%m-%dT%H:%M:%S"),
                            paths.keys(),
                            self._ra_api,
                            path))

        self._ra_api.get_log(callback=cb, paths=[path],
                           start=1, end=rev,
                           discover_changed_paths=True,
                           revprops=["svn:date", "svn:author", "svn:log"])

        self.rev_list.reverse()

        return self.rev_list
        
    head = property(get_head)
    name = property(get_name)


