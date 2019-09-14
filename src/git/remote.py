import sys
import subprocess as sp
from urllib.parse import urlparse

from ..issues import warning, execute, exit
from ..qs import confirm

def url_valid(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def getRemoteList():
    remotelst = sp.getoutput(f'git remote -v').split('\n')
    remotelst = [r.split('\t')[0]
                 for idx, r in enumerate(remotelst) if idx % 2]
    return remotelst


def Remote(remote):
    remotelst = getRemoteList()
    if remote in remotelst:
        pass
    else:
        warning(f'Remote branch `{remote}` not found')
        if confirm(f'Add?'):
            while(1):
                remote_url = prompt("URL")
                if url_valid(remote_url):
                    execute([f'git remote add {remote} {remote_url}'])
                    break
                else:
                    warning('Not valid URL')
        else:
            exit()
