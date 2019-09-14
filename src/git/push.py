from .remote import Remote
from ..issues import execute

def Push(remote, branch):
    Remote(remote)
    execute([f'git push -u {remote} {branch}'])
