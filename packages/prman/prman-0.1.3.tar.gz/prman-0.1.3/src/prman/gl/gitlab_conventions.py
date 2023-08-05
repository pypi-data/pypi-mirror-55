import re


def get_mr_name(branch_regex, template, branch_name):
  match = re.search(branch_regex, branch_name)
  if match is None:
    return None
  else:
    def sub(m):
      x = m.group(1)
      x = x[2:len(x) - 1]
      s = match.group(x)
      s = "" if s is None else s
      s = s.replace('-', ' ')
      return s
    return re.sub('(\\${.+?})', sub, template)
