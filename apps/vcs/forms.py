from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app
from django.utils.translation import ugettext

from django.contrib.auth.models import User
from vcs.models import Repository

from django.forms.util import ErrorList

class RepositoryForm(forms.ModelForm):
    """
    Form for editing repository details
    """
    
#    def __init__(self, project, *args, **kwargs):
    def __init__(self, project, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        self.project = project
        super(RepositoryForm, self).__init__(data, files, auto_id, prefix,
                                             initial, error_class,
                                             label_suffix, empty_permitted,
                                             instance)
        
        if instance:
            self.fields['path'].initial = instance.path
            self.fields['type'].initial = instance.type
    
    class Meta:
        model = Repository
        fields = ["path", "type"]
    

