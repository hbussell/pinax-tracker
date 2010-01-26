
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def dashboard(request, template_name="dashboard/dashboard.html"):
    return render_to_response(template_name, {

    }, context_instance=RequestContext(request))

def all_tasks(request, template_name="dashboard/all_tasks.html"):

    from tasks.models import Task 
    from tasks import workflow
    from tasks.filters import TaskProjectFilter

   
    if not request.user.is_authenticated():
        is_member = False
    else:
        is_member = True
    
    group_by = request.GET.get("group_by")

    tasks = Task.objects.all()
    tasks = tasks.select_related("assignee")
    
    # default filtering
    state_keys = dict(workflow.STATE_CHOICES).keys()
    default_states = set(state_keys).difference(
        # don"t show these states
        set(["2", "3"])
    )
#    milestones = [(m.id, m.title) for m in Milestone.objects.all()]

    filter_data = {"state": list(default_states)}
                   #"milestone":
                   #milestones}
    filter_data.update(request.GET)
    
    task_filter = TaskProjectFilter(filter_data, queryset=tasks)
    










#    task_filter.filter('milestone', milestone.id)
    
    group_by_querydict = request.GET.copy()
    group_by_querydict.pop("group_by", None)
    group_by_querystring = group_by_querydict.urlencode()

    del task_filter.filters['milestone']

    return render_to_response(template_name, {

        "group_by": group_by,
        "gbqs": group_by_querystring,
        "task_filter": task_filter,
        "tasks": task_filter.qs,
        "querystring": request.GET.urlencode(),

    }, context_instance=RequestContext(request))


