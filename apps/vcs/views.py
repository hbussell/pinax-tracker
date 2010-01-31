import os
import difflib
import itertools
import re

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import Context
from django.template.context import RequestContext
from django.template.loader import get_template
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse

from .models import Repository
import pyvcal
from projects.models import Project
import git
import datetime
from .forms import RepositoryForm
from django.core.cache import cache

from django.contrib import messages
highlightable_extensions = ('.py', '.cs', '.sh', '.php', '.sql', '.java',
                            '.cpp', '.css', '.rb', '.vb', '.xml', '.html',
                            '.htm')

def get_repo(project):
    """Returns the active repository for the given project name.
    It is assumed that the given project exists in the database."""

    repo = Repository.objects.get(project=project)
    vcs_api = pyvcal.get_api(repo.type)
    vcs_repo = vcs_api.Repository(repo.path)
    return vcs_repo

def repository_edit(request, project_slug,
                    template='vcs/edit_repository.html'):
    project = Project.objects.get(slug=project_slug)
    try:
        repo = Repository.objects.get(project=project)
    except:
        repo=None

    if request.method=='POST':
        form = RepositoryForm(project, data=request.POST, instance=repo)
        repo = form.save(commit=False)
        repo.project = project
        repo.save()
        messages.add_message(request, messages.SUCCESS,
            ugettext("repository updated")
        )
    else:
        form = RepositoryForm(project, instance=repo)

    template_data = {
        'form':form,
        'project': project
    }
    return render_to_response(template, template_data, RequestContext(request))
 

def repository_detail(request, project_slug, branch=None, partial=''):
    return path_detail(request, project_slug, branch, '')

def get_path_commit(tree, path, repo, ref='master'):
    "get the commit affecting a file path"
    path = path.lstrip('/').rstrip('/')
    path_key = '%s:%s' % (tree.tree_id, path)
    cached = cache.get(path_key)
    if cached:
        return cached
    commits = repo.commits(path=path, max_count=1)
    if len(commits)>0:
        commit = commits[0]
    else:
        commits = repo.commits(max_count=1)
        commit = commits[0]
    cache.set(path_key, commit)
    return commit

def path_detail(request, project_slug, branch='master', path=''):

    # If the rev /was/ specified, then we want it to be cast to an int
    if 'r' in request.GET:
        rev = int(request.GET['r'])
    else:
        rev = None
    path = path.lstrip('/')
    project = Project.objects.get(slug=project_slug)
    repo = get_repo(project)
    git_repo = repo.get_git_repo()
    nodes = []
    if not branch:
        branch = 'master'
    if branch !='master':
        if not repo.revisions.has_key('branch'):
            raise Http404
        revision = repo.revisions[branch]
        tree = revision.tree
    else:    
        tree = repo.tree

    root = tree.get_path_tree(path)
    template = 'vcs/repository_detail.html'
    if isinstance(root, git.Blob):
        tree_values = [root]
        template = 'vcs/file_detail.html'
    else:
        tree_values = root.values()

#    commits = repo.get_git_repo().commits()
#    git.Commit.find_all(repo.get_git_repo(), 
    for node in tree_values:
        node_type = 'file'
        if isinstance(node, git.Tree):
            node_type = 'tree'
        commit = node
        details = {'name':node.name,
                   'type':node_type}
        commit = get_path_commit(tree, '%s/%s' % (path, node.name), git_repo )
        details['commit_id'] = commit.id
        details['committer'] = commit.committer.name
        tup = commit.committed_date
        date = datetime.datetime(*(tup[0:6]))
        details['committed_date'] = date
        details['message'] = commit.message

        url = reverse('vcs_path_detail',
                      kwargs={'project_slug':project_slug,
                              'branch':branch, 'path':'%s/%s' % (path,
                                                                 node.name)})
        details['url'] = url
        nodes.append(details)

    crumbs = []
    if path !='':
        dirs = path.split('/')
        if len(dirs)==0:
            crumbs.append((path, None))
        else:
            for i in range(0, len(dirs)):
                p = '/'.join(dirs)
                name = dirs.pop()
                url = reverse('vcs_path_detail',
                              kwargs={'project_slug':project_slug,
                                      'branch':branch, 'path':p})
                crumbs.append((name, url))
    crumbs.reverse()
    url = reverse('vcs_path_detail',
                              kwargs={'project_slug':project_slug,
                                      'branch':branch, 'path':''})
    crumbs.insert(0, (project.name, url))

    template_data = {
        'tree': nodes,
        'root': root,
        'crumbs': crumbs,
        'tree_id': tree.tree_id,
        'project': project
    }

    return render_to_response(template, template_data, RequestContext(request))


def commit_detail(request, project_slug, commit_id):
    project = Project.objects.get(slug=project_slug)
    project = project
    repo = get_repo(project)
    nodes = []
    commit = repo.get_git_repo().commit(commit_id)
    files = {}
    for name, stats in commit.stats.files.items():
        if stats['deletions'] ==0:
            file_type = 'added'
        else:
            file_type = 'modified'
        changes = int(stats['deletions']) + int(stats['insertions'])
        url = reverse('vcs_path_detail',
                              kwargs={'project_slug':project_slug,
                                      'branch':commit.id, 'path':name})

        files[name] = {'stats':stats,'status':file_type, 'changes':changes,
                       'url':url,
                       'insertions': stats['insertions'], 'deletions':
                       stats['deletions']}
    for diff in commit.diffs:
        name = diff.b_path
        chunks = get_diff_chunks(diff.diff.split("\n"))
        files[name]['stats'] = stats
        files[name]['line_diffs'] = chunks

    tup = commit.committed_date
    date = datetime.datetime(*(tup[0:6]))
    parent = None
    if len(commit.parents) > 0:
        parent = commit.parents[0]

    template_data = {
        'tree': commit.tree.values(),
        'tree_id': commit.tree.id,
        'commit': commit,
        'commit_date': date,
        'parent': parent,
        'files':files

    }
    template = 'vcs/commit_detail.html'

    return render_to_response(template, template_data, RequestContext(request))

def get_diff_lines(diff):
    lines = []
    # We can ignore the first two lines in the unified diff.
    for diffline in itertools.islice(diff, 2, None):
        # The beginning of a context section begins with "@@". It gives line
        # number information.
        if diffline.startswith("@"):
            pass
        elif diffline.startswith(" "):
            pass
            # Are there any REMOVED, ADDED, or MODIFIED lines to add?
        # Beginning of a removed line. We don't know if it's a line that was
        # taken out, or if it was modified. Save it and we'll handle it later.
        elif diffline.startswith("-"):
            lines.append(('removed', diffline))
        elif diffline.startswith("+"):
            lines.append(('added', diffline))

    return lines





def get_diff_chunks(diff):
    """
    Chunk formatting

    left_markup: the text on the left side of the diff view (side by side diff)
    right_markup: the text on the right side of the diff view (side by side diff)
    left_counter: the current line number on the left text
    right_counter: the current line number on the right text
    type: The type of line being shown in the diff.  One of {ADDED, UNMODIFIED, REMOVED}
    """

    chunks = []
    lines = None
    lines = []
    modified_old = []
    modified_new = []
    left_counter = 0
    right_counter = 0
    # We can ignore the first two lines in the unified diff.
    for diffline in itertools.islice(diff, 2, None):
        # The beginning of a context section begins with "@@". It gives line
        # number information.
        if diffline.startswith("@"):
            match = re.search(r"@@ -(\d+),\d+ \+(\d+),\d+ @@\n", diffline)
            if match:
                left_counter = int(match.group(1))
                right_counter = int(match.group(2))

                if lines is not None:
                    chunks.append(lines)

                lines = []
            # Beginning of an unmodified line.
        elif diffline.startswith(" "):
            # Are there any REMOVED, ADDED, or MODIFIED lines to add?
            add_modified_section(lines, modified_old, modified_new)
            modified_old = []
            modified_new = []

            # Common line, add to both
            lines.append({
                    "type": "UNMODIFIED",
                    "left_markup": escape(diffline[1:]),
                    "right_markup": escape(diffline[1:]),
                    "left_counter": left_counter,
                    "right_counter": right_counter,
            })
            left_counter += 1
            right_counter += 1
        # Beginning of a removed line. We don't know if it's a line that was
        # taken out, or if it was modified. Save it and we'll handle it later.
        elif diffline.startswith("-"):
            modified_old.append({
                    "text": diffline[1:],
                    "counter": left_counter,
            })
            left_counter += 1
        # Beginning of an added line. We don't know if it's a line that was
        # inserted, or if it was modified. Save it and we'll handle it later.
        elif diffline.startswith("+"):
            modified_new.append({
                    "text": diffline[1:],
                    "counter": right_counter,
            })
            right_counter += 1

    # What if the very end of the file is modified? Need to check that too.
    # (Ideally, everyone should newline-terminate a file, but hey.)
    add_modified_section(lines, modified_old, modified_new)
    if lines is not None:
        chunks.append(lines)
    return chunks

def add_modified_section(lines, modified_old, modified_new):
    old_lines = len(modified_old)
    new_lines = len(modified_new)

    # Are there adjacent REMOVED and ADDED sections? (Is there a MODIFIED
    # section?) This loop only has an effect when both modified_old and
    # modified_new have entries.
    for i in range(min(old_lines, new_lines)):
        lines.append({
                "type": "MODIFIED",
                "left_markup": escape(modified_old[i]["text"]),
                "right_markup": escape(modified_new[i]["text"]),
                "left_counter": modified_old[i]["counter"],
                "right_counter": modified_new[i]["counter"],
        })

    # Append any extra REMOVED lines.
    # (only has an effect when old_lines > new_lines)
    append_modified_old(lines, modified_old[new_lines:])
    # Append any extra ADDED lines.
    # (only has an effect when new_lines > old_lines)
    append_modified_new(lines, modified_new[old_lines:])

def append_modified_old(lines, modified_old):
    for removed in modified_old:
        lines.append({
                "type": "REMOVED",
                "left_markup": escape(removed["text"]),
                "right_markup": "",
                "left_counter": removed["counter"],
                "right_counter": "",
        })

def append_modified_new(lines, modified_new):
    for added in modified_new:
        lines.append({
                "type": "ADDED",
                "left_markup": "",
                "right_markup": escape(added["text"]),
                "left_counter": "",
                "right_counter": added["counter"],
        })




