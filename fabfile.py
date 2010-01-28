from __future__ import with_statement
from manage import *
from djangofab.vcs.git import update_remote, update_local, push, commit, add, update_app
from djangofab.api import *
env.capture_default = False


# apply the settings from fab.cfg default section
# sets the DJANGO_SETTINGS which allows access to settings values
apply_settings()

#use the default section of fab.cfg
@user_settings()
def prod():
    "Production settings"
    env.hosts = ['server1']
    env.wsgi = '%(prod_wsgi)s'
    env.path = '%(prod_path)s'
    env.giturl = '%(giturl)s'
    env.site_user = '%(site_user)s'
    env.site_group = '%(site_group)s'
    env.virtualenv = '%(prod_virtualenv)s'

@user_settings()
def dev():
    "Development settings"
    env.hosts = ['server1']
    env.wsgi = '%(dev_wsgi)s'
    env.path = '%(dev_path)s'
    env.giturl = '%(giturl)s'
    env.site_user = '%(site_user)s'
    env.site_group = '%(site_group)s'
    env.virtualenv = '%(dev_virtualenv)s'

#use the local section
@user_settings('fab.cfg','local')
def localhost():
    "Local settings"
    env.path = '%(dev_path)s'
    env.giturl = '%(giturl)s'

def deploy():
    "Push local changes and update checkout on the remote host"
    push()
    update_remote() # reset and pull on the remote server
    #remote_export() 
    change_ownership()
    touch_wsgi()

def test():
    print env.giturl
    print env.path
    from django.conf import settings
    print "website using database %s " % (settings.DATABASE_NAME,)
