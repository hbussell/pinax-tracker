from django import template
from django.conf import settings

from django.template.defaultfilters import stringfilter

register = template.Library()
#import vcs
from vcs.forms import RepositoryForm 
from vcs.models import Repository

@register.filter
@stringfilter
def line_id(value, side):
    if value == '':
        return ''
    else:
        return 'id=%s-%s' % (side, value)

@register.filter
@stringfilter
def diff_class(value):
    if value == 'MODIFIED':
        return 'modified-line'
    elif value == 'REMOVED':
        return 'removed-line'
    elif value == 'ADDED':
        return 'added-line'
    else:
        return '';

@register.inclusion_tag("vcs/_edit_repository_form.html", takes_context=True)
def vcs_edit_repository_form(context, project):
    try:
        repo = Repository.objects.get(project=project)
    except:
        repo=None

    form = RepositoryForm(project, instance=repo)
    return {
        "project": project,
        "form": form,
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
    }


