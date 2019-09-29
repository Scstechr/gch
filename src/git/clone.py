import subprocess as sp

from ..issues import warning, execute, exit, ok
from ..qs import confirm, prompt
from ..util import validateRef, validateURL


def Clone():
    ok("Cloning remote repository")
    remote_url = ''
    while 1:
        remote_url = prompt("URL")
        if validateURL(remote_url):
            break
    name = remote_url.split('/').pop()
    if confirm(f'Clone it in the directory `./{name}`?'):
        directory = name
    else:
        directory = prompt("Specify directory")
    if confirm(f'Is it master branch?'):
        branch = 'master'
    else:
        while 1:
            branch = prompt("Branch name")
            if validateRef(branch):
                break

    execute([f'git clone -b {branch} {remote_url} {directory}'])
    exit()

