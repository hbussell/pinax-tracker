from django.conf.urls.defaults import *

#from milestoness.feeds import AllMilestoneFeed



#milestone_feed_dict = {"feed_dict": {
#    "all": AllMilestoneFeed,
#}}



urlpatterns = patterns("",
    url(r"^$", "milestones.views.milestones", name="milestone_list"),
    
    url(r"^add/$", "milestones.views.add_milestone", name="milestone_add"),
    #url(r"^$", "milestones.views.milestones", name="milestone_new"),
#    url(r"^add/$", "milestones.views.add_milestone", name="milestone_add"),
    url(r"^milestone/edit/(?P<id>\d+)/$", "milestones.views.milestone_edit",
        name="milestone_edit"),
    url(r"^milestone/(?P<id>\d+)/$", "milestones.views.milestone_detail", name="milestone_detail"),
        
    # feeds
    #(r"^feeds/(.*)/$", "django.contrib.syndication.views.feed", tasks_feed_dict),
)
