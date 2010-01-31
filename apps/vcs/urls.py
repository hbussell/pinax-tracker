from django.conf.urls.defaults import patterns, url

## Regex fragments we interpolate into URL matchers, for readabilty.

# We support 4 formats for viewing the repo:
# * browse: pretty markup, coloring
# * raw: no markup, plain text
# * download: force the browser download mechanism
# * json: json markup of subfolders for a given path
format = '(?P<format>raw|download|json|browse|partial)'
format = '(?P<format>[^/]+)'

# branch names match any string up to the next slash.
branch = '(?P<branch>[^/]+)'

# path resolves to a filepath in the repo, so it matches everything
# it can (including slashes); can also be the empty string.
path = '(?P<path>.*)'

# rev is an arbitrary string (up to the next slash) because we match
# hashes for git, numbers for svn, etc.
rev = '(?P<rev>[^/]+)'

urlpatterns = patterns('vcs.views',

 
    url(r'^commit/(?P<project_slug>[\w\._-]+)/(?P<commit_id>[^/]+)/$', 'commit_detail',
        name='vcs_commit_details'),

    url(r'^tree/(?P<project_slug>[\w\._-]+)/%s/%s/$' % (branch, path),
        'path_detail', name='vcs_path_detail'),
    url(r'edit/(?P<project_slug>[^/]+)/$', 'repository_edit',
        name='vcs_repository_edit'),


    #url(r'path/(?P<project_slug>[^/]+)/$', 'path_detail', name='vcs_path_detail'),
#    url(r'^(?P<project_slug>[^/]+/)%s/%s/?$' % (format, path), 'path_detail',
#        name='vcs_path_detail'),
    

    url(r'(?P<project_slug>[^/]+)/$', 'repository_detail', name='vcs_root'),
 

#    url(r'^commits/%s$' % path, 'commit_list', name='commit-list'),

)
