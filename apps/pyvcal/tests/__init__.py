from unittest import TestSuite
import os
import subprocess

import git_wrapper as git
import subversion
import perforce

import pyvcal

test_all = TestSuite([  git.test_git, 
                        perforce.test_perforce, 
                        subversion.test_subversion
                    ])

import independent

for test_module in [git, subversion, perforce]:
    test_all.addTest(independent.tests(test_module))
    
    
