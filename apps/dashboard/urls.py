from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r"^$", "dashboard.views.dashboard", name="dashboard_index"),
    url(r"^all_tasks/$", "dashboard.views.all_tasks",
        name="dashboard_all_tasks"),
)
