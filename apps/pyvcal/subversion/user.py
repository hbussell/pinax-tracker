
class User(object):
    """ A user in the version control system. """

    def __init__(self, name):
        super(User, self).__init__()
	
	self._name = name

    def _get_author(self):
	""" Returns the name of the User """
	return self._name
    
    author = property(_get_author)
	
        
