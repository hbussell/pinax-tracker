###########################################
# APICoverage.py #
#################
# This script will indicate what parts of
#  the api don't exist yet.
########################################

import pyvcal
import inspect

# Build a list of the api we want to be used
api_list = [ ('branch', ['Branch']),
             ('file', ['File']),
             ('filediff', ['FileDiff']),
             ('path', ['Path']),
             ('property', ['Properties', 'ResourceProperties', 'FileProperties', 'TreeProperties']),
             ('repository', ['Repository']),
             ('resource', ['Resource']),
             ('revision', ['Revision']),
             ('revisiondiff', ['RevisionDiff', 'NullRevisionDiff', 'MultipleParentNullRevisionDiff']),
             ('revisionproperties', ['RevisionProperties']),
             ('tree', ['Tree']),
             ('user', ['User'])
           ]

vcs_list = ['git_wrapper', 'perforce', 'subversion']


for vcs in vcs_list:
    print "\n-{ ", vcs, " }-"
    for (module_name, classes) in api_list:
        full_general = 'pyvcal.' + module_name
        full_vcs = 'pyvcal.' + vcs + '.' + module_name
        
        vcs_module = None
        try:
            vcs_module = __import__(full_vcs, globals(), locals(), classes, -1)
        except ImportError:
            print "Must add ", full_vcs, " module."
        
        if vcs_module:
            for class_name in classes:
                members_general = __import__(full_general, globals(), locals(), classes, -1).__dict__[class_name].__dict__
                members_vcs = vcs_module.__dict__[class_name].__dict__
                
                for member_general in members_general.keys():
                    if inspect.isroutine(members_general[member_general]):
                        if not member_general in members_vcs.keys():
                            print "Must implement ", full_vcs, ".", class_name, "::", member_general, " function."
                        else:
                            if inspect.isfunction(members_general[member_general]):
                                args_general = inspect.getargspec(members_general[member_general])[0]
                                args_vcs = inspect.getargspec(members_vcs[member_general])[0]
                            
                                for arg in args_general:
                                    if not arg in args_vcs:
                                        print "Method signature of ", full_vcs, ".", class_name, "::", member_general, " function appears to be wrong: Doesn't have the ", arg, " argument."
                                
                                args = []
                                for i in range(len(inspect.getargspec(members_vcs[member_general])[0])):
                                    args.append('narf')
                                
                                try:
                                    members_vcs[member_general](*args)
                                except NotImplementedError:
                                    print "Method ", full_vcs, ".", class_name, "::", member_general, " isn't implemented yet."
                                except:
                                    pass

