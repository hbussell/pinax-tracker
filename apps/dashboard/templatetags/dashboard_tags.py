from projects.models import Project
from tasks.models import Task
from django import template

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional, Model
register = template.Library()

@tag(register, [Optional([Constant("as"), Name()])])
def get_projects(context, asvar=None):
    val = Project.objects.all()
    if asvar:
        context[asvar] = val
        return ""
    else:
        return val

@tag(register, [Optional([Constant("as"), Name()])])
def get_tasks(context, asvar=None):
    val = Task.get_all()
    if asvar:
        context[asvar] = val
        return ""
    else:
        return val

@tag(register, [Variable(), Optional([Constant("as"), Name()])])
def get_usertasks(context, user, asvar=None):
    val = Task.get_all().filter(assignee=user)
    if asvar:
        context[asvar] = val
        return ""
    else:
        return val

@tag(register, [Variable(), Optional([Constant("as"), Name()])])
def get_notices(context, user, asvar=None):
    from notification.models import *
    notice_types = NoticeType.objects.all()
    val = Notice.objects.notices_for(user, on_site=True)
    if asvar:
        context[asvar] = val
        return ""
    else:
        return val



@tag(register, [Variable(), Optional([Constant("as"), Name()])])
def project_task_count(context, project, asvar=None):
    val = Task.get_project_count(project) 
    if asvar:
        context[asvar] = val
        return ""
    else:
        return val

