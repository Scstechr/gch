from .. import issues
from .. import qs

def Status():
    if qs.isExist(f'git status --short'):
        return True
    else:
        issues.ok('Clean!')
        return False
