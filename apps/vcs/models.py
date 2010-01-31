from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from projects.models import Project


class Repository(models.Model):
    # VCS Types
    SVN = 'svn'
    GIT = 'git'

    # Limits
    # The max vcs path length is an arbitrary restriction.
    MAX_PATH_LENGTH = 256
    MAX_TYPE_LENGTH = 5

    project = models.ForeignKey(Project,
                                unique=True,
                                verbose_name=_("project"))
    path = models.CharField(_("path"), max_length=MAX_PATH_LENGTH)
    type = models.CharField(
                _("version control type"),
                max_length=MAX_TYPE_LENGTH,
                choices=((SVN, _("Subversion")),
                         (GIT, _("Git"))),
                default=SVN)

    class Meta:
        verbose_name = _("repository")
        verbose_name_plural = _("repositories")

    def __unicode__(self):
        return self.path

class Commit(models.Model):

    revision = models.IntegerField(_("revision"))
    repo = models.ForeignKey(Repository, verbose_name=_("repository"))
    project = models.ForeignKey(Project, verbose_name=_("project"))
    author = models.ForeignKey(User, verbose_name=_("author"), null=True,
                               blank=True)

    class Meta:
        verbose_name = _("commit")
        verbose_name_plural = _("commits")

    def __unicode__(self):
        return 'Commit #%s' % self.revision

    def get_absolute_url(self):
        kwargs={
            'project_slug': self.project.slug,
            'format': "browse",
            'rev': self.revision,
            'path': ".",
        }
        return reverse('commit_detail', kwargs=kwargs)


