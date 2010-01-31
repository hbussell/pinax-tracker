"""
This module represents an interface to a version control system.
Except get_api, the code is not intended to be run---it is documentation in 
Python syntax.

For usage information for get_api(), see USAGE_STRING.

Version control system api implementors should copy the following import 
statements which allow a user of get_api() to use e.g. 

get_api(...).Repository

"""

## @package pyvcal The PyVCAL API for version control system abstraction.

from repository import Repository

#import perforce, subversion, git_wrapper as git
import git_wrapper as git

USAGE_STRING = """
Usage: vcs_api = pyvcal.get_api('<vcs>')
         where <vcs> can be:
         - git
         - subversion
         - perforce

"""

def get_api(system):
    try:
        vcs = {
            'git' : git,
            #'subversion' : subversion,
            #'perforce' : perforce
        }[system]
    except KeyError, e:
        raise ValueError(USAGE_STRING)

    return vcs

