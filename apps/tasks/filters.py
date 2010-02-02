from django import forms

import django_filters as filters

from tasks.models import Task
from projects.models import Project

from milestones.models import Milestone
from django.contrib.contenttypes.models import ContentType

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
            widget = forms.CheckboxSelectMultiple,
        )
    
    class Meta:
        model = Task
        fields = ["state", "milestone"]


class TaskProjectFilter(filters.FilterSet):
    
    state = filters.MultipleChoiceFilter(
        choices = Task.STATE_CHOICES,
        widget = forms.CheckboxSelectMultiple,
    )
    milestone = filters.MultipleChoiceFilter(
        choices = tuple([(m.id, str(m)) for m in Milestone.objects.all()]),
        widget = forms.CheckboxSelectMultiple,
    )
    
    object_id = filters.MultipleChoiceFilter(
        choices = tuple([(p.id, p.name) for p in Project.objects.all()]),
        widget = forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = ["state", "milestone", "object_id"]
