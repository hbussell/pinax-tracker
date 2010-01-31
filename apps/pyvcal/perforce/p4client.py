import P4

class P4Client(object):
    """
    with P4Client(user, password, host, port , client, cwd) as p4c:
        p4c.do_stuff()
    """
    
    def __init__(self, user, password, host, port, client, cwd):
        """Initializes a P4 object"""
        self._p4c = P4.P4()
        
        if user:
            self._p4c.user = user
        if host:
            self._p4c.host = host
        if port:
            self._p4c.port = port
        if client:
            self._p4c.client = client
        if cwd:
           self._p4c.cwd = cwd
        self._password = password
        
    def __enter__(self):
        """Connects a P4 object"""
        self._p4c.connect()
        if self._password:
            self._p4c.login(self._password)
        return self._p4c
    
    def __exit__(self, type, value, traceback):
        """Tear down the P4 object"""
        self._p4c.disconnect()

    @property
    def host(self):
        """Return the server host"""
        return self._p4c.host
        
    @property
    def port(self):
        """Return the server port"""
        return self._p4c.port

