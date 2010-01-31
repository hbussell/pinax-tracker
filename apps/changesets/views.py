from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import re
#from git import *
import pyvcal

def changesets(request, template_name="changesets/changesets.html"):
    import pdb;pdb.set_trace()
    vcs_api = pyvcal.get_api('git')
    repo = vcs_api.Repository('/home/harley/projects/pinax-tracker-website/website')

    #git = Git('/home/harley/projects/pinax-tracker/website')
#    repo = Repo('/home/harley/projects/pinax-tracker/website')
#    tree = self.repo.tree('master')

    return render_to_response(template_name, {

    }, context_instance=RequestContext(request))


