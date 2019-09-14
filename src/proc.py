import sys
from os import path, chdir

from . import issues
from .qs import isExist, confirm
from .arg import Help, defaultspath, status_bar, IGNORE as ignore
from .version import Version
from .diff import diffhash, logviewer
from .gits import Branch
from .git.commit import Commit
from .git.status import Status
from .git.init import Init
from .git.ls_files import Ls
from .git.pull import Pull
from .git.push import Push
from .git.reset import Reset
from .git.log import Log
from .git.remote import Remote
from .git.branch import getBranch, setBranch, checkoutBranch
from .util import B

# git commands
diffcmd = 'git diff --cached --ignore-all-space --ignore-blank-lines'


def proc(d, MODE=0):
    init = d['init']
    gitpath = d['gitpath']
    filepath = d['filepath']
    branch = d['branch']
    verbose = d['verbose']
    log = d['log']
    commit = d['commit']
    reset = d['reset']
    push = d['push']
    remote = d['remote']
    pull = d['pull']
    diff = d['diff']
    version = d['version']
    save = d['save']
    checkout = d['checkout']
    ls = d['ls']

    if d['help']:
        Help(MODE)

    if version:
        Version('GCH - Git Commit Handler')

    status_bar(d)

    if type(branch) == bool:
        branch = Branch()

    if save:
        if path.exists(defaultspath):
            issues.execute([f'rm {defaultspath}'], verbose=False)
        for k, v in d.items():
            if k not in ignore:
                cmd = f'echo "{str(k)}:{str(v)}" >> {defaultspath}'
                issues.execute([cmd], verbose=False)
        issues.ok('Saved!')

    # conversion to absolute path
    gitpath = path.abspath(gitpath)
    filepath = path.abspath(filepath)
    chdir(gitpath)

    gitfolder = path.join(gitpath, '.git')
    if not path.exists(gitfolder):
        issues.warning(
            f'It seems path:`{gitpath}` does not have `.git` folder.')
        if confirm(f'Initialize?'):
            Init(flag=False)
        else:
            issues.abort()
    if init:
        Init(flag=True)

    current_branch, _ = getBranch(lst=True)
    if diff:
        if confirm('Do you want to use diff-column viewer?'):
            flag = False
            if confirm('Do you want to name specific author?'):
                flag = True
            diffhash(verbose=verbose, head=False, author=flag)
        else:
            logviewer(verbose=verbose, head=False)

    if checkout:
        print(f'\n\033[1mCurrently on branch {B(current_branch)}')
        checkoutBranch()

    if reset:
        Reset()

    if len(branch) == 0:
        issues.execute(['git branch'])
        sys.exit()

    if ls:
        Ls()

    if isExist('git branch'):
        if len(branch):
            if current_branch != branch:
                issues.branch()
                branch = setBranch(branch, filepath)

    if log:
        Log()

    if Status():
        issues.execute([f'git diff --stat'])
        if verbose:
            issues.execute([f'git add .', diffcmd, f'git reset'])
        if commit:
            issues.execute([f'git add {filepath}'])
            Commit()

    if pull:
        Pull(remote, branch)

    if push:
        Push(remote, branch)

