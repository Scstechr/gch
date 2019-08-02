#!/usr/bin/env python
'''
==================
Git Commit Handler
==================
'''

import sys, subprocess as sp
from os import path, chdir, getcwd
import os
import click

from src import issues
from src.qs import getAnswer, isExist 
from src.git import *
from src.diff import diffhash, logviewer
from src.parse import Parser, Help

from src import VERSION
GCH_VERSION = VERSION
issues.version(3)

# git commands 
diffcmd = 'git diff --cached --ignore-all-space --ignore-blank-lines'
logcmd =  'git log --stat --oneline --graph --decorate'

def main():
    d = Parser()

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

    if d['help']:
        Help()

    if version:
        print(" gch version :", GCH_VERSION)
        sys.exit(0)

    gitfolder = path.join(gitpath, '.git')
    if not path.exists(gitfolder):
        issues.warning(f'It seems path:`{gitpath}` does not have `.git` folder.')
        if click.confirm(f'Initialize?'):
            initialize(flag=False)
        else:
            issues.abort()
    if init:
        initialize(flag=True)

    if diff:
        if click.confirm('Do you want to use diff-column viewer?'):
            flag = False
            if click.confirm('Do you want to name specific author?'):
                flag = True
            diffhash(verbose=verbose, head=False, author=flag)
        else:
            logviewer(verbose=verbose, head=False)

    if reset:
        Reset()

    if len(branch) == 0:
        issues.execute(['git branch'])

    if isExist('git branch'):
        current_branch = getCurrentBranch()
        if len(branch):
            if current_branch != branch:
                issues.branch()
                branch = setBranch(branch, filepath)
        
    issues.execute(['git status --short'])

    if save:
        issues.execute([f'rm {defaultspath}'])
        for k, v in defaults.items():
            issues.execute([f'echo "{str(k)}:{str(v)}" >> {defaultspath}'])

    #conversion to absolute path
    gitpath = path.abspath(gitpath)
    filepath = path.abspath(filepath)

    if log:
        issues.execute([logcmd])

    if CheckState():
        issues.execute([f'git diff --stat'])
        if verbose:
            issues.execute([f'git add .', diffcmd, f'git reset'])
        if commit:
            issues.execute([f'git add {filepath}'])
            Commit()


    if pull:
        issues.execute([f'git fetch {remote} {branch}',
                        f'git merge {remote} {branch}'])

    # Push or not
    if push:
        Push(remote, branch)
    else:
        issues.ok('No push')

if __name__ == "__main__":
    main()
