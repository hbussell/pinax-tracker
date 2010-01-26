from datetime import datetime
from sys import stderr

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app
from django.utils.translation import ugettext

from django.contrib.auth.models import User

from tasks.models import Task, TaskHistory, workflow
from tasks.widgets import ReadOnlyWidget

from django.contrib.admin import widgets

from tagging_utils.widgets import TagAutoCompleteInput
from tagging.forms import TagField
from .models import Milestone

class MilestoneForm(forms.ModelForm):
    """
    Form for creating milestones
    """
    
    due = forms.DateTimeField(widget=widgets.AdminDateWidget())

    def __init__(self, user, group, *args, **kwargs):
        self.user = user
        self.group = group
        
        super(MilestoneForm, self).__init__(*args, **kwargs)
        
    
    class Meta:
        model = Milestone
        fields = ["title", "detail", "due", "markup"]
    
    def clean(self):
        self.check_group_membership()
        return self.cleaned_data
    
    def check_group_membership(self):
        group = self.group
        if group and not self.group.user_is_member(self.user):
            raise forms.ValidationError("You must be a member to create tasks")


class EditMilestoneForm(forms.ModelForm):
    """
    Form for creating milestones
    """
    
    due = forms.DateTimeField(widget=widgets.AdminDateWidget())

    def __init__(self, user, group, *args, **kwargs):
        self.user = user
        self.group = group
        
        super(EditMilestoneForm, self).__init__(*args, **kwargs)
        
    
    class Meta:
        model = Milestone
        fields = ["title", "detail", "due", 'state', "markup"]
    
    def clean(self):
        self.check_group_membership()
        return self.cleaned_data
    
    def check_group_membership(self):
        group = self.group
        if group and not self.group.user_is_member(self.user):
            raise forms.ValidationError("You must be a member to create tasks")


