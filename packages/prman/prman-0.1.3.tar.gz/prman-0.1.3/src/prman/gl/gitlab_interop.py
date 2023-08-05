# pylint: disable=unused-wildcard-import
import gitlab
from toolz.curried import *


def init_gitlab_client(gitlab_url, token):
  client = gitlab.Gitlab(gitlab_url, private_token=token)
  client.auth()
  return client


def get_current_user(client):
  return client.user


def get_project(client, project_id):
  return client.projects.get(project_id)


def get_project_users_except_me_and_ci(client, project):
  user_id = client.user.id
  return pipe(
    project.users.list(),
    map(lambda x: x.id),
    filter(lambda x: x != user_id and x != 3696277),
    map(lambda x: client.users.get(x)),
    list
  )


def get_mrs_list(project):
  return pipe(
    project.mergerequests.list(state='opened'),
    map(lambda x: x.iid),
    map(project.mergerequests.get),
    list
  )


def create_mr(maximum_required_approvers_count, client, project, source_branch, target_branch, title, approver_ids):
  user = get_current_user(client)
  mr_create_req = {
    'source_branch': source_branch,
    'target_branch': target_branch,
    'title': title,
    'remove_source_branch': True,
    'squash': True,
    'assignee_ids': [user.id] + approver_ids,
  }
  if maximum_required_approvers_count != -1:
    approvals_before_merge = min(maximum_required_approvers_count, len(approver_ids))
    mr_create_req['approvals_before_merge'] = approvals_before_merge
  mr = project.mergerequests.create(mr_create_req)

  mr.approvals.set_approvers() # set_approvers does not work without it
  mr.approvals.set_approvers(approver_ids)
  return mr
