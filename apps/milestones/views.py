from datetime import date, datetime, timedelta
from itertools import chain
from operator import attrgetter

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db.models import Q, get_app
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from pinax.utils.importlib import import_module

# Only import dpaste Snippet Model if it's activated
if "dpaste" in getattr(settings, "INSTALLED_APPS"):
    from dpaste.models import Snippet
else:
    Snippet = False
if "notification" in getattr(settings, "INSTALLED_APPS"):
    from notification import models as notification
else:
    notification = None

from tagging.models import Tag

from .models import Milestone
from .filters import MilestoneFilter
from .forms import MilestoneForm, EditMilestoneForm

def milestones(request, group_slug=None, template_name="milestones/milestone_list.html", bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    if not request.user.is_authenticated():
        is_member = False
    else:
        if group:
            is_member = group.user_is_member(request.user)
        else:
            is_member = True
    
    group_by = request.GET.get("group_by")
    
    if group:
        milestones = group.content_objects(Milestone)
        group_base = bridge.group_base_template()
    else:
        milestones = Milestone.objects.filter(object_id=None)
        group_base = None
    
    # default filtering
    state_keys = dict(Milestone.STATE_CHOICES).keys()
    default_states = set(state_keys).difference(
        # don"t show these states
        set(["2"])
    )
    
    filter_data = {"state": list(default_states)}
    filter_data.update(request.GET)
    
    milestone_filter = MilestoneFilter(filter_data, queryset=milestones)
    
    group_by_querydict = request.GET.copy()
    group_by_querydict.pop("group_by", None)
    group_by_querystring = group_by_querydict.urlencode()
    
    return render_to_response(template_name, {
        "group": group,
        "group_by": group_by,
        "gbqs": group_by_querystring,
        "is_member": is_member,
        "group_base": group_base,
        "milestone_filter": milestone_filter,
        "milestones": milestone_filter.qs,
        "querystring": request.GET.urlencode(),
    }, context_instance=RequestContext(request))


def add_milestone(request, group_slug=None, secret_id=None,
             form_class=MilestoneForm,
             template_name="milestones/add.html", bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    if group:
        group_base = bridge.group_base_template()
    else:
        group_base = None
    
    if not request.user.is_authenticated():
        is_member = False
    else:
        if group:
            is_member = group.user_is_member(request.user)
        else:
            is_member = True
    
    initial = {}
    if request.method == "POST":
        if request.user.is_authenticated():
            milestone_form = form_class(request.user, group, request.POST)
            if milestone_form.is_valid():
                milestone = milestone_form.save(commit=False)
                milestone.creator = request.user
                milestone.group = group
                #if hasattr(workflow, "initial_state"):
                #    milestone.state = workflow.initial_state(milestone, user)
                milestone.save()
                #milestone.save_history()
                messages.add_message(request, messages.SUCCESS,
                    ugettext("added milestone '%s'") % milestone.title
                )
                if notification:
                    if group:
                        notify_list = group.member_queryset()
                    else:
                        notify_list = User.objects.all() # @@@
                    notify_list = notify_list.exclude(id__exact=request.user.id)
                    notification.send(notify_list, "milestones_new",
                                      {"creator": request.user,
                                       "milestone": milestone, "group": group})
                if request.POST.has_key("add-another-milestone"):
                    if group:
                        redirect_to = bridge.reverse("milestone_add", group)
                    else:
                        redirect_to = reverse("milestone_add")
                    return HttpResponseRedirect(redirect_to)
                if group:
                    redirect_to = bridge.reverse("milestone_list", group)
                else:
                    redirect_to = reverse("milestone_list")
                return HttpResponseRedirect(redirect_to)
    else:
        milestone_form = form_class(request.user, group, initial=initial)
    
    return render_to_response(template_name, {
        "group": group,
        "is_member": is_member,
        "milestone_form": milestone_form,
        "group_base": group_base,
    }, context_instance=RequestContext(request))


def milestone_detail(request, id, group_slug=None,
              template_name="milestones/milestone.html", bridge=None):
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    if group:
        milestones = group.content_objects(Milestone)
        group_base = bridge.group_base_template()
    else:
        milestones = Milestone.objects.filter(object_id=None)
        group_base = None
    milestone = get_object_or_404(milestones, id=id)
    if group:
        notify_list = group.member_queryset()
    else:
        notify_list = User.objects.all()
    notify_list = notify_list.exclude(id__exact=request.user.id)
    if not request.user.is_authenticated():
        is_member = False
    else:
        if group:
            is_member = group.user_is_member(request.user)
        else:
            is_member = True
    ## milestone tasks
    from tasks.models import Task
    from tasks import workflow
    from tasks.filters import TaskFilter

    group_by = request.GET.get("group_by")

    if group:
        tasks = group.content_objects(Task)
        group_base = bridge.group_base_template()
    else:
        tasks = Task.objects.filter(object_id=None)
        group_base = None
    tasks = tasks.select_related("assignee")

    # default filtering
    state_keys = dict(workflow.STATE_CHOICES).keys()
    default_states = set(state_keys)
    filter_data = {"state": list(default_states)}
    filter_data.update(request.GET)
    task_filter = TaskFilter(filter_data, queryset=tasks)
    group_by_querydict = request.GET.copy()
    group_by_querydict.pop("group_by", None)
    group_by_querystring = group_by_querydict.urlencode()

    return render_to_response(template_name, {
        "group": group,
        "milestone": milestone,
        "is_member": is_member,
        "group_base": group_base,
        "group_by": group_by,
        "gbqs": group_by_querystring,
        "is_member": is_member,
        "task_filter": task_filter,
        "tasks": task_filter.qs.filter(milestone=milestone),
        "querystring": request.GET.urlencode(),

    }, context_instance=RequestContext(request))

@login_required
def milestone_edit(request, id, group_slug=None,
              template_name="milestones/edit.html", bridge=None):

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    if group:
        milestones = group.content_objects(Milestone)
        group_base = bridge.group_base_template()
    else:
        milestones = Milestone.objects.filter(object_id=None)
        group_base = None
    milestone = get_object_or_404(milestones, id=id)
    if group:
        notify_list = group.member_queryset()
    else:
        notify_list = User.objects.all()
    notify_list = notify_list.exclude(id__exact=request.user.id)
    if group:
        is_member = group.user_is_member(request.user)
    else:
        is_member = True
    if not is_member:
        messages.add_message(request, messages.ERROR,
            ugettext("You can't edit milestones unless you are a project member")
        )
        return HttpResponseRedirect(reverse("project_list"))

    if is_member and request.method == "POST":
        form = EditMilestoneForm(request.user, group, request.POST, instance=milestone)
        if form.is_valid():
            milestone = form.save()
            if "state" in form.changed_data:
                messages.add_message(request, messages.SUCCESS,
                    ugettext("milestone marked %(state)s") % {
                        "state": milestone.get_state_display()
                    }
                )
                if notification:
                    notification.send(notify_list, "milestones_change", {"user": request.user, "milestone": milestone, "group": group, "new_state": milestone.get_state_display()})
            form = EditMilestoneForm(request.user, group, instance=milestone)
    else:
        form = EditMilestoneForm(request.user, group, instance=milestone)
    return render_to_response(template_name, {
        "group": group,
        "milestone": milestone,
        "is_member": is_member,
        "form": form,
        "group_base": group_base
    }, context_instance=RequestContext(request))



