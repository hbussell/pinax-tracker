from property import ResourceProperties

import os 

from subvertpy import repos, ra, NODE_DIR, NODE_FILE

class Resource(object):
    """ A versioned object """

    def __init__(self, ra_api=None, branch_path=None, path=None, revnum=None):
        super(Resource, self).__init__()
        
        self._ra_api = ra_api
        self._branch_path = branch_path
    	self._path = path
    	self._revnum = revnum

    	self._resource_proplist = ResourceProperties(self, revnum, path)
    
    def get_latest_revision(self):
        """ Return the last revision this was modified """
        #self.rev = Revision(self._revnum, "", "", "", self._path, self._ra_api, self._branch_path)
                
        #return self.rev.predecessors[0]
        raise NotImplementedError 

    def get_properties(self):
        """ Return the properties of a resource """
        return self._resource_proplist
    
    def _get_ra_api(self):
        return self._ra_api

    def full_path(self):
        """ Returns the full path of this Resource """
        return str(os.path.join(self._branch_path, self._path[0]))

    def basename(self):
        """ Returns the Resource path """
        return os.path.basename(self.self._path)

    """ Some methods to see if this Resource is a File or a Tree """
    def is_file(self):
        """ To be overriden in File """
        return False

    def is_tree(self):
        """ To be overriden in Tree """
        return False

    def is_text(self):
        """ To be overriden in File """
        return False

    def get_data(self):
        """ To be overriden in File/Tree """
        return ''

    latest_revision = property(get_latest_revision)
    properties = property(get_properties)
    data = property(get_data)


