# pylint: disable=unused-wildcard-import
from .cli.argparsing import *
from .config import *
from .cli.interaction import *
from .git.git_interop import *
from .git.git_conventions import *
from .gl.gitlab_interop import *
from .gl.gitlab_conventions import *
from toolz.curried import *
import logging
import os


__version__ = "0.1.3"


def main():
  args = read_args()
  if args['config']:
    key = args['<key>']
    value = args.get('<value>', None)
    if value is None:
      config = read_config()
      value = config.get(key, '')
      print(value)
    else:
      add_config_kvp(key, value)
    return

  config = read_config()

  repo = get_repo(os.getcwd())
  repo_name = get_repo_name(repo)
  print_repo_name(repo_name)

  remote_url = get_first_remote_url(repo)
  project_id = extract_gitlab_project_id(remote_url)
  print_project_id(project_id)

  current_branch = get_current_branch(repo)
  print_current_branch(current_branch)

  mr_name = get_mr_name(
    config['conventions.pr.branch_regex'],
    config['conventions.pr.template'],
    current_branch
  )
  if mr_name is None:
    print_current_branch_has_bad_format()
    return
  print_mr_name(mr_name)

  print_fetching_project()
  gl_client = init_gitlab_client(config['gitlab.url'], config['gitlab.token'])
  project = get_project(gl_client, project_id)

  print_fetching_prs()
  mrs = get_mrs_list(project)

  mrs_for_current_branch = pipe(mrs, filter(lambda x: x.source_branch == current_branch), list)
  mr_for_current_branch = None if len(mrs_for_current_branch) == 0 else mrs_for_current_branch[0]
  if not mr_for_current_branch is None:
    print_mr_is_already_created(current_branch, mr_for_current_branch.web_url)
    return

  print_fetching_users()
  users = get_project_users_except_me_and_ci(gl_client, project)
  approvers = select_approvers(users)
  approver_ids = pipe(approvers, map(lambda x: x.id), list)

  print_pushing_to_origin()
  push_origin(repo)

  print_creating_mr()
  maximum_required_approvers_count = int(config['conventions.maximum_required_approvers_count'])
  mr = create_mr(
    maximum_required_approvers_count,
    gl_client,
    project,
    current_branch,
    'master',
    mr_name,
    approver_ids
  )

  mr_web_url = mr.web_url
  print_mr_is_created(mr_web_url)


if __name__ == '__main__':
  main()
