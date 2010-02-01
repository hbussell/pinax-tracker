
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from tasks.models import Task
from projects.models import Project

from django.contrib import messages
from django.utils.translation import ugettext
from django.template.defaultfilters import slugify


def dashboard(request, template_name="dashboard/dashboard.html"):

    if _handle_taskbar(request):
        return HttpResponseRedirect('/')
    if _handle_projects(request):
        return HttpResponseRedirect('/')

    return render_to_response(template_name, {
        'projects':Project.objects.all()
    }, context_instance=RequestContext(request))

def _handle_taskbar(request):
    if not request.user.is_authenticated():
        return
    if request.method == 'POST':
        if request.POST.get('add_task'):
            name = request.POST.get('task_name')
            project_id = request.POST.get('task_project', None)
            if project_id:
                try:
                    project = Project.objects.get(pk=project_id)
                except Project.DoesNotExist:
                    #project = None
                    return
            task = Task(summary=name, group=project, creator=request.user)
            task.save()
            messages.add_message(request, messages.SUCCESS,
                ugettext("added task '%s'") % task.summary
            )
            return True


def _handle_projects(request):
    if not request.user.is_authenticated():
        return
    if request.method == 'POST':
        if request.POST.get('add_project'):
            name = request.POST.get('project_name')
            try:
                Project.objects.get(name=name)
            except Project.DoesNotExist:
                project = Project(name=name, slug=slugify(name), creator=request.user)
                project.save()
                messages.add_message(request, messages.SUCCESS,
                    ugettext("added project '%s'") % project.name
                )
                return True



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


