# pylint: disable=unused-wildcard-import
from toolz.curried import *
from .git_interop import *
import re


WIP_BRANCH_NAME_SUFFIX = '-wip'


def extract_gitlab_project_id(remote):
  match = re.search(r'git@gitlab.com:(?P<project_id>.+?)\.git', remote)
  assert not match is None
  return match.group('project_id')


def is_wip_branch(branch_name):
  return branch_name.endswith(WIP_BRANCH_NAME_SUFFIX)


def get_wip_branch_prefix(branch_name):
  assert is_wip_branch(branch_name)
  return branch_name[:len(branch_name) - len(WIP_BRANCH_NAME_SUFFIX)]


def commit_to_branch_name(commit_message):
  return commit_message.replace(' ', '-')


def get_wip_branch_mr_branch(wip_branch_prefix, commit_message):
  commit_branch_name = commit_to_branch_name(commit_message)
  return f'{wip_branch_prefix}-{commit_branch_name}'


def filter_wip_commits(repo, wip_branch_prefix, commits):
  return pipe(
    commits,
    filter(lambda x: not is_branch_exists(repo,
      get_wip_branch_mr_branch(wip_branch_prefix, x.message)
    )),
    list
  )
