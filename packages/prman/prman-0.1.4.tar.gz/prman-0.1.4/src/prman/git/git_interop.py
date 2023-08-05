# pylint: disable=unused-wildcard-import
import brigit
from toolz.curried import *
import os
from pyrecord import Record


def get_repo(path):
  try:
    repo = brigit.Git(path)
    repo.status()
    return repo
  except brigit.GitException:
    return None


def get_first_remote_url(repo):
  return repo.remote('-v').rstrip().split('\n')[0].replace('\t', ' ').split(' ')[1]


def get_repo_name(repo):
  path = repo.__call__('rev-parse', '--show-toplevel').strip()
  return os.path.basename(path)


Commit = Record.create_type('Commit', 'hash', 'message')


def get_commits(repo):
  try:
    log = list(repo.pretty_log('origin/master..HEAD'))
  except IndexError: # brigit bug if the log is empty
    log = []
  return pipe(
    log,
    filter(lambda x: not x['message'].startswith('Merge')),
    map(lambda x: Commit(x['hash'], x['message'])),
    list
  )


def get_current_branch(repo):
  return repo.__call__('rev-parse', '--abbrev-ref', 'HEAD').strip()


def is_branch_exists(repo, branch_name):
  try:
    repo.__call__('rev-parse', '--verify', branch_name)
    return True
  except brigit.GitException:
    return False


def is_git_cache_empty(repo):
  output = repo.status()
  return 'working tree clean' in output


def cherry_pick(repo, commit_hash):
  repo.__call__('cherry-pick', commit_hash)


def checkout(repo, branch_name):
  repo.checkout(branch_name)


def checkout_new_branch(repo, branch_name):
  repo.checkout('-b', branch_name)


def push_origin(repo):
  repo.push('-u', 'origin', 'HEAD')
