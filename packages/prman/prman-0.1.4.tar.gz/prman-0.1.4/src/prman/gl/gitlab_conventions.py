import re


def get_pr_name(mappings, branch_name):
  def try_map(mapping):
    match = re.search(mapping['regex'], branch_name)
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
      return re.sub('(\\${.+?})', sub, mapping['template'])
  for mapping in mappings:
    res = try_map(mapping)
    if not res is None:
      return res
  return None
