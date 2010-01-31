from revision import Revision
from branch import Branch

import os
from datetime import datetime
from subvertpy import repos, ra, NODE_NONE, NODE_DIR, NODE_FILE

class Repository(object):

    def __init__(self, path):
        """ Constructor for the SVN Repository object """
        super(Repository, self).__init__()
        self.path = path
        self.connect()

    def get_uri(self):
        """ Return the URI of the repository """
        return self.ra_api.get_repos_root()
	
    def connect(self):
        """ Given a path, then connect to that path """
	
	# Check if the path contains a 'file://' indicator
	#if self.path.find() == -1:
	#	self.abs_path = "file://" + self.path
	#else:
	#	self.abs_path = self.path
	
        self.ra_api = ra.RemoteAccess(self.path)

    def get_revisions(self):
        """ Return a dictionary of Revision objects where the key is the revision_id 
        and the value is the actual Revision object """

        rev_id = self.ra_api.get_latest_revnum()
        return self._log(rev=rev_id)
	
    def get_branches(self):
        """ Return the branches available in the repository """
        # assume: /trunk, /branches
        branch_dict = {}

        # The first element in the top level info is the list of files
        f_list = self._file_list('', self.ra_api)

        if 'trunk' in f_list:
            branch_dict['trunk'] = Branch('trunk', self.ra_api)

        if 'branches' in f_list:
            branch_list = self._file_list('branches', self.ra_api)
            for branch in branch_list:
                branch_dict[branch] = Branch(('branches/' + branch), self.ra_api)

        # If repo doesnt have the /trunk, /branches, /tags structure, then the
        # repository will only report a single branch 
        if not branch_dict:
            branch_dict[''] = Branch('', self.ra_api)

    	return branch_dict
	
	""" Helper methods for this class """
    def _log(self, path='', rev=None):
        """ Return a Revision object scoped to path with revision id as rev """
        rev = rev or self.ra_api.get_latest_revnum()
        log_path = path # may need to join it with the current branch's path?
			
    	# dictionary containing the revisions of the repository as key-value pairs, where the key is the revision_id 
    	# and the value would be a Revision object.
        revision_dict = {}

        def cb(paths, revnum, props, has_children=False):
            paths = paths or {}
            revision_dict[revnum] = Revision(revnum,
                                    props.get('svn:author', ''),
                                    props.get('svn:log', ''),
                                    datetime.strptime(
                                    props['svn:date'].split('.')[0],
                                             "%Y-%m-%dT%H:%M:%S"),
                                    paths.keys(),
                                    self.ra_api,
                                    log_path)

        self.ra_api.get_log(callback=cb, paths=[log_path],
                           start=1, end=rev,
                           discover_changed_paths=True,
                           revprops=["svn:date", "svn:author", "svn:log"])

        return revision_dict

    def _file_list(self, path, ra_api):
        """ Return a list of strings representing the contents of a given path """
        revnum = ra_api.get_latest_revnum()
        path_level_info = ra_api.get_dir(path, revnum)

        return path_level_info[0].keys()

    @classmethod
    def create(cls, path):
        """ Create a new Repository and return it. """
        return repos.create(path)

    uri = property(get_uri)
    branches = property(get_branches)
    revisions = property(get_revisions)
