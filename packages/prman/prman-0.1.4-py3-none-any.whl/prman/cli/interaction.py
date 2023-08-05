# pylint: disable=unused-wildcard-import
from toolz.curried import *
from .colorized_print import *
import sys


strJoin = lambda sep: lambda strs: sep.join(strs)


def choose_items(items, text_provider):
  s = input()
  def parse_pair(s):
    spl = s.strip().split('..')
    assert len(spl) <= 2
    if len(spl) == 1:
      s = spl[0]
      try:
        return [int(s) - 1]
      except ValueError:
        indexes = pipe(
          items,
          map(text_provider),
          enumerate,
          filter(lambda t: s.lower() in t[1].lower()),
          map(lambda t: t[0]),
          list
        )
        if len(indexes) != 1:
          print_red(f'Can not find an unique item with \'{s}\' substring. Found {len(indexes)} items.')
          sys.exit()
        return indexes
    else:
      return list(range(int(spl[0]) - 1, int(spl[1])))

  return pipe(
    s.split(';'),
    mapcat(parse_pair),
    set,
    map(lambda idx: items[idx]),
    list
  )


def print_commits(commits):
  print(pipe(
    commits,
    enumerate,
    map(lambda t: f"{t[0] + 1}. {t[1].message}"),
    strJoin('\n')
  ))


def select_commits_to_make_prs(commits):
  print('Select commits to make PR\'s:')
  print_commits(commits)
  return choose_items(commits, lambda x: x.message)


def get_user_str(user):
  return f'{user.username} ({user.name})'


def print_users(users):
  print(pipe(
    users,
    enumerate,
    map(lambda t: f"{t[0] + 1}. {get_user_str(t[1])}"),
    strJoin('\n')
  ))


def select_approvers(users):
  print('Select approvers:')
  print_users(users)
  return choose_items(users, get_user_str)


def print_dir_is_not_repo(path):
  print_red(f'Directory \'{path}\' is not a git repository.')


def print_repo_name(name):
  print(f'The repository name: {name}')


def print_repo_gitlab_project_id_can_not_be_extracted(remote_url):
  print_red(f'Can not extract GitLab project id from remote \'{remote_url}\'.')


def print_project_id(project_id):
  print(f'The project id: {project_id}')


def print_current_branch(name):
  print(f'The current branch: {name}')


def print_can_not_create_pr_from_master():
  print_red('Can not create a PR from master branch.')


def print_pr_name(name):
  print(f'The PR name: {name}')


def print_fetching_project():
  print('Fetching the project...')


def print_fetching_prs():
  print('Fetching PR\'s...')


def print_pr_is_already_created(branch_name, web_url):
  print_red(f'PR for \'{branch_name}\' is already created:')
  print(web_url)


def print_fetching_users():
  print('Fetching approvers...')


def print_pushing_to_origin():
  print('Pushing to the origin...')


def print_creating_pr():
  print('Creating the PR...')


def print_current_branch_can_not_be_mapped_to_pr_name():
  print_red(f'The current branch name is incompatible with \'conventions.branch_to_pr_mappings\'.')


def print_pr_is_created(pr_web_url):
  print_green('The PR is created:')
  print(pr_web_url)
