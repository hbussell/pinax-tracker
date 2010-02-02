from django import forms

import django_filters as filters

from tasks.models import Task
from projects.models import Project
from django.contrib.auth.models import User
from milestones.models import Milestone
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import SafeString

class TaskFilter(filters.FilterSet):
    
    state = filters.MultipleChoiceFilter(
        choices = Task.STATE_CHOICES,
        widget = forms.CheckboxSelectMultiple,
    )
    
    class Meta:
        model = Task
        fields = ["state"]

class TaskMilestoneFilter(filters.FilterSet):
    state = filters.MultipleChoiceFilter(
        choices = Task.STATE_CHOICES,
        widget = forms.CheckboxSelectMultiple,
    )
    
    def __init__(self, project, data=None, queryset=None, prefix=None):
        super(TaskMilestoneFilter, self).__init__(data, queryset, prefix)

        content_type = ContentType.objects.get_for_model(Project)
        self.filters['milestone'] = filters.MultipleChoiceFilter('milestone',
            choices = tuple([(m.id, m.title) for m in
                             Milestone.objects.filter(content_type=content_type,
                                 object_id=project.id)]),
            #widget = forms.CheckboxSelectMultiple,
            widget = forms.SelectMultiple,
        )
    
    class Meta:
        model = Task
        fields = ["state", "milestone"]


class TaskProjectFilter(filters.FilterSet):
    
    state = filters.MultipleChoiceFilter(
        choices = Task.STATE_CHOICES,
        widget = forms.CheckboxSelectMultiple,
    )

    milestones = []
    projects = Project.objects.all()
    for project in projects:
        project_milestones = Milestone.objects.filter(object_id=project.id)
        if len(project_milestones) >0:
            milestones.append(('', project.name))
            for milestone in project_milestones:
                milestones.append((milestone.id, SafeString('&nbsp;&nbsp;&nbsp;' +
                                   milestone.title)))
        
    milestone = filters.MultipleChoiceFilter(
        name = 'milestone',
        choices = tuple(milestones),
        widget = forms.SelectMultiple,
    )
   
    def __init__(self, user, data=None, queryset=None, prefix=None):
        super(TaskProjectFilter, self).__init__(data, queryset, prefix)

        projects = []
        assignee = []
        if user.is_authenticated():

            assignee.append((user.id, 'Assigned to You'))
            for u in User.objects.exclude(id=user.id):
                assignee.append((u.id, str(u)))

            my_projects = Project.objects.filter(member_users=user).order_by("name")

            projects.append(('','Your Projects'))
            for project in my_projects:
                projects.append((project.id,
                                 SafeString('&nbsp;&nbsp;&nbsp;' + project.name)))

            projects.append(('','Other Projects'))
            for project in Project.objects.exclude(id__in=my_projects):
                projects.append((project.id,
                                 SafeString('&nbsp;&nbsp;&nbsp;' + project.name)))
        else:
            projects.append(('','All Projects'))
            for project in Project.objects.all():
                projects.append((project.id,
                                 SafeString('&nbsp;&nbsp;&nbsp;' + project.name)))

            for u in User.objects.all():
                assignee.append((u.id, str(u)))


        object_id = filters.MultipleChoiceFilter(
#            choices = tuple([(p.id, p.name) for p in Project.objects.all()]),
            name='object_id',
            choices = tuple(projects),
            widget = forms.SelectMultiple,
            label='Project'
        )
        self.filters['object_id'] = object_id

        assignee = filters.MultipleChoiceFilter(
#            choices = tuple([(p.id, p.name) for p in Project.objects.all()]),
            name='assignee',
            choices = tuple(assignee),
            widget = forms.SelectMultiple,
            label='Assignee'
        )
        self.filters['assignee'] = assignee
 

    class Meta:
        model = Task
        fields = ["state", "milestone", "object_id", "assignee"]
