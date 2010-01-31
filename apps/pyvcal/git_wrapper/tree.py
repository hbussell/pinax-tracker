from pyvcal.resource import Resource
from .path import Path
import git

class Tree(Resource):
    """A versioned container of Files"""

    def __init__(self, tree_id, repo):
        # all we need is the hash and repo; we let gitpython do the rest
        super(Tree, self).__init__()
#        import pdb;pdb.set_trace()
        if isinstance(tree_id, git.Tree):
            tree_id = tree_id.id
        self.tree_id = tree_id
        self.repo = repo
        self.path = Path(self.repo)
        
        self._contents = {}
        gitTree = self.repo.tree(self.tree_id)
        for i in gitTree.items():
            self._contents[i[0]] = i[1]

    def get_path(self):
        """Return the path to this tree in its container Repository"""
        return self._path
        
    def get_contents(self, recursive=True):
        """Return the immediate contents of a tree as a list of Resources."""
        return get_data(recursive)
    
    def get_data(self, recursive=True):
        return self._contents 
    
    def get(self, key):
        return self._contents.get(key)
    
    def items(self):
        return self._contents.items()
        
    def keys(self):
        return self._contents.keys()
    
    def values(self):
        return self._contents.values()
 
    def get_path_tree(self, path):
        if path =='':
            return self
        path = path.lstrip('/').rstrip('/')
        dirs = path.split('/')
        if len(dirs)==0:
            return self

        def get_child(dirs, tree):
            if len(dirs)==0:
                return tree
            name = dirs.pop(0)
            child = tree.get(name)
            if not child:
                return tree
            return get_child(dirs, child)

        child = get_child(dirs, self)
        #if isinstance(child, git.Tree):
        #    return child
        return child
    
   
#    path = property(get_path, set_path)
#    contents = property(get_contents)
    
