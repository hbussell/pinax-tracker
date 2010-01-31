from revisionproperties import RevisionProperties
from resource import Resource
from revisiondiff import RevisionDiff

from subvertpy import repos, ra, NODE_NONE, NODE_DIR, NODE_FILE
from datetime import datetime
import os

class Revision(object):
    """ The complete state of a branch at a given time """
	
    def __init__(self, revnum=None, author=None, log=None, date=None, paths=None, ra_api=None, branch_path=None):
        super(Revision, self).__init__()
		
        self.revnum = revnum
        self.author = author
        self.log = log
        self.date = date
        self.paths = paths
        self.ra_api = ra_api
        self.branch_path = branch_path
		
        self._proplist = RevisionProperties(self, revnum, author, log, date)
        self._resource = Resource(self.ra_api, self.branch_path, self.paths, self.revnum)
 
    def get_predecessors(self):
        """ Return a list of Revision(s) that flow into this Revision """
        self.r_predecessors = []
        log_path = self.branch_path
        rpaths = self.paths[0]
        rid = self.revnum

        def cb(paths, rev_id, props, has_children=False):
            paths = paths or {}
            if rpaths in paths:
                self.r_predecessors.append(Revision(rev_id,
                                            props.get('svn:author', ''),
                                            props.get('svn:log', ''),
                                            datetime.strptime(props['svn:date'].split('.')[0],
                                                 "%Y-%m-%dT%H:%M:%S"),
                                            paths.keys(),
                                            self.ra_api,
                                            rpaths))
        
        self.ra_api.get_log(callback=cb, paths=[log_path],
                           start=1, end=(rid-1), 
                           discover_changed_paths=True,
                           revprops=["svn:date", "svn:author", "svn:log"])

        self.r_predecessors.reverse()
        return self.r_predecessors

    def get_ra_api(self):
        """ Returns the self.ra_api variable associated with this Revision object"""
        return self.ra_api

    def get_resource(self):
        """ Return the Resource that belongs to this Revision """
        return self._resource
        
    def get_properties(self):
        """ Get the RevisionProperties for this revision """
        return self._proplist

    def get_diff_with_parent(self, paths=None):
        """ Return the RevisionDiff from this revision to its parent, optionally
        restricted to the given file(s) on paths
       
        If there is more than one parent, this method may return a fake RevisionDiff
        with no content to represent a merge.
        """
        parents = self.get_predecessors()
        return self.diff(self, parents[0])
        
    @classmethod
    def diff(cls, src, dst, paths=None):
        """ Return the RevisionDiff from Revision src to Revision dst, optionally 
	    restricted to the given file(s) on paths """
        return RevisionDiff(src, dst)

    def _get_node_path(self, path):
        """Return the node path of a given path which is everything
           after self.branch_path."""

        branch_path = os.path.join(self.branch_path, '')
        # The path should always be prefixed by the branch path, 
        #assert path.startswith(branch_path)
        
        return path[len(branch_path):]

    def _get_revision_number(self):
        """ Return the revision number that belongs to this Revision """
	return self.revnum

    predecessors = property(get_predecessors)
    properties = property(get_properties)
    diff_with_parent = property(get_diff_with_parent)

