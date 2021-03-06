from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from account.openid_consumer import PinaxConsumer



handler500 = "pinax.views.server_error"


if settings.ACCOUNT_OPEN_SIGNUP:
    signup_view = "account.views.signup"
else:
    signup_view = "signup_codes.views.signup"


urlpatterns = patterns("",
    #url(r"^$", direct_to_template, {
    #    "template": "homepage.html",
    #}, name="home"),
    
    url(r'^$', 'dashboard.views.dashboard', name='home'),
    (r'^dashboard/', include('dashboard.urls')),
    #url(r'^$', 'squaretracker_results.views.view_runs', name='home'),
    url(r"^admin/invite_user/$", "signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^account/signup/$", signup_view, name="acct_signup"),
    
    (r"^about/", include("about.urls")),
    (r"^account/", include("account.urls")),
    (r"^openid/(.*)", PinaxConsumer()),
    (r"^profiles/", include("basic_profiles.urls")),
    (r"^notices/", include("notification.urls")),
    (r"^avatar/", include("avatar.urls")),
    (r"^comments/", include("threadedcomments.urls")),
    (r"^announcements/", include("announcements.urls")),
    (r"^tagging_utils/", include("tagging_utils.urls")),
    (r"^attachments/", include("attachments.urls")),
    (r"^projects/", include("projects.urls")),
    (r"^changesets/", include("changesets.urls")),
    (r"^vcs/", include("vcs.urls")),
    
#    (r'^tracker/results/', include('squaretracker_results.urls')),
#    (r'^tracker/api/', include('squaretracker.urls')),

    (r"^admin/", include(admin.site.urls)),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        (r"", include("staticfiles.urls")),
    )
