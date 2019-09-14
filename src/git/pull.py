from ..issues import execute

def Pull(remote, branch):
    execute([f'git pull {remote} {branch}'])