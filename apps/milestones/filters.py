from django import forms

import django_filters as filters

from .models import Milestone



class MilestoneFilter(filters.FilterSet):
    
    state = filters.MultipleChoiceFilter(
        choices = Milestone.STATE_CHOICES,
        widget = forms.CheckboxSelectMultiple,
    )
    
    class Meta:
        model = Milestone
        fields = ["state"]
