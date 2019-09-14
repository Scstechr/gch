from .remote import Remote

def Push(remote, branch):
    Remote(remote)
    issues.execute([f'git push -u {remote} {branch}'])
