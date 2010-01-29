# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from pinax.utils.importlib import import_module


if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

from tagging.fields import TagField
from tagging.models import Tag
from threadedcomments.models import ThreadedComment
from django.db.models import Q

from tasks.fields import MarkupField


workflow = import_module(getattr(settings, "TASKS_WORKFLOW_MODULE", "tasks.workflow"))



class Milestone(models.Model):
    """
    a project goal with a planed date.
    """
    
    STATE_CHOICES = (('1', 'open'), ('2', 'closed'))

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    group = generic.GenericForeignKey("content_type", "object_id")
    
    title = models.CharField(_("title"), max_length=100)
    detail = models.TextField(_("detail"), blank=True)
    markup = MarkupField(_(u"Detail Markup"))
    creator = models.ForeignKey(User,
        related_name = "created_milestones",
        verbose_name = _("creator")
    )
    created = models.DateTimeField(_("created"), default=datetime.now)
    due = models.DateField(_("due"), null=True, blank=True)
    modified = models.DateTimeField(_("modified"), default=datetime.now) # task modified when commented on or when various fields changed
    
    # status is a short message the assignee can give on their current status
    
    state = models.CharField(_("state"),
        max_length = 1,
        choices = STATE_CHOICES,
        default = 1
    )
   
    # fields for review and saves
    fields = [
        "title"
        "detail",
        "creator",
        "due"
        "created",
        "markup",
        "state",
    ]
    
    def __unicode__(self):
        return self.title
    
    def save(self, **kwargs):
        self.modified = datetime.now()
        super(Milestone, self).save(**kwargs)
    
    def get_absolute_url(self, group=None):
        kwargs = {"id": self.pk}
        if group:
            return group.content_bridge.reverse("milestone_detail", group, kwargs)
        return reverse("milestone_detail", kwargs=kwargs)
   
    def get_due_display(self):
        from django.utils.timesince import timesince
        import datetime
        now = datetime.datetime.now()
        if not self.due:
            return u''
        if self.due <= now:
            #d = timesince(self.due, now)
            return u'%s ago' % timesince(self.due, now)
        else:
            return u'in %s' % timesince(now, self.due)

    @property
    def progress_complete(self):
        from tasks.models import Task
        closed_tasks = Task.objects.filter(Q(milestone=self)).filter(Q(state='2') | Q(state='3'))
        todo_tasks = Task.objects.filter(Q(milestone=self) & ~Q(state='2') & ~Q(state='3'))
        return todo_tasks.count() == 0 and closed_tasks.count() > 0

    @property
    def closed_count(self):
        from tasks.models import Task
        return float(Task.objects.filter(Q(milestone=self)).filter(Q(state='2') |
                                           Q(state='3')).count())
        
    @property
    def todo_count(self):
        from tasks.models import Task
        return float(Task.objects.filter(Q(milestone=self)).filter(~Q(state='2') &
                                           ~Q(state='3')).count())

    @property
    def closed_pct(self):
        from tasks.models import Task
        tasks = Task.objects.filter(milestone=self).count()
        closed_tasks = self.closed_count
        if closed_tasks > 0:
            return closed_tasks / tasks * 100
        return 0

    @property
    def todo_pct(self):
        from tasks.models import Task
        tasks = Task.objects.filter(milestone=self).count()
        todo_tasks = self.todo_count
        if todo_tasks > 0:
            return todo_tasks / tasks * 100
        return 0

    @property
    def closed(self):
        return self.state != '1'

    @classmethod
    def get_project_milestones(cls, project):
        ct = ContentType.objects.get_for_model(project)
        return cls.objects.filter(content_type=ct, object_id=project.id)

    def allowable_states(self, user):
        """
        return state choices allowed given current state and user
        """
        
        # I"m the relevant state choices.
        choices = []
        
        # I"m the states already allowed for the users
        existing_states = []
        
        for transition in workflow.STATE_TRANSITIONS:
            
            if self.state != str(transition[0]):
                # if the current state does not match a first element in the
                # state transitions we skip to the next transition
                continue
            
            # Fire the validation function.
            if transition[2](self, user):
                
                # grab the new state and state description
                new_state = str(transition[1])
                description = transition[3]
                
                # build new element
                element = (new_state, description)
                
                # append new element to choices
                choices.append(element)
        
        return choices
