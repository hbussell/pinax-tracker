class Properties(object):
    """ Properties of a versioned object """

    def __init__(self, resource=None, revnum=None, path=None):
        super(Properties, self).__init__()
		
        self._resource = resource
        self._revnum = revnum
        self._path = path       
    
	
class ResourceProperties(Properties):
    """ Properties of a versioned object """

    def __init__(self, resource, revnum, path):
        super(Properties, self).__init__()
        
        self._resource = resource
        self._revnum = revnum
        self._path = path       

    def _get_revision_number(self):
        """ Return the revision number of the Resource to which these properties apply """
        return self._revnum
        
    def _get_path(self):
        """ Return the path of this Resource in the Repository """
        return self._path
        
    def _get_resource(self):
        """ Get the Resource """
        return self._resource
            
    resource = property(_get_resource)
    path = property(_get_path)
    revision_number = property(_get_revision_number)


class FileProperties(ResourceProperties):
    """ The properties of a File """

    def __init__(self, resource=None, revnum=None, path=None):
        super(FileProperties, self).__init__()
         
        self._resource = resource
        self._revnum = revnum
        self._path = path       

    def _get_type(self):
        """ Return the type of this Resource """
        return 'file'

		
class TreeProperties(ResourceProperties):
    """ The properties of a Tree """
    def __init__(self, resource=None, revnum=None, path=None):
        super(TreeProperties, self).__init__()
        
        self._resource = resource
        self._revnum = revnum
        self._path = path       
        
    def _get_type(self):
        """ Return the type of this Resource """
        return 'directory'
