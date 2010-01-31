from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r"^$", "changesets.views.changesets", name="changeset_index"),
)
