#!/usr/bin/env python
'''
==================
Git Commit Handler
==================
'''

import sys, subprocess as sp
from os import path, chdir, getcwd
import click

from pysrc import issues
from pysrc.qs import getAnswer, isExist 
from pysrc.git import *

issues.version(3)

defaults = {}
defaultspath = path.join(".", ".defaults.txt")
if path.exists(defaultspath):
    with open(defaultspath, 'r') as readfile:
        for line in readfile:
            k, v = line.replace('\n','').split(":")
            defaults[str(k)] = str(v)
else:
    defaults['init'] = 'False'
    defaults['gitpath'] = '.'
    defaults['filepath'] = '.'
    defaults['branch'] = 'master'
    defaults['detail'] = 'False'
    defaults['log'] = 'False'
    defaults['commit'] = 'False'
    defaults['reset'] = 'False'
    defaults['push'] = 'False'
    defaults['remote'] = 'origin'
    defaults['pull'] = 'False'

# Explanation of the options showed in --help flag
exp_i=f'run initializer or not.'.ljust(38)+f'>Default:{defaults["init"]}'
exp_g=f'Path of dir that contains `.git`.'.ljust(38)+f'>Default:{defaults["gitpath"]}'
exp_f=f'Path/Regex of staging file/dir.'.ljust(38)+f'>Default:{defaults["filepath"]}'
exp_b=f'Commiting branch.'.ljust(38)+f'>Default:{defaults["branch"]}'
exp_d=f'Detailed diff.'.ljust(38)+f'>Default:{defaults["detail"]}'
exp_l=f'Git log with option.'.ljust(38)+f'>Default:{defaults["log"]}'
exp_c=f'Commit or not.'.ljust(38)+f'>Default:{defaults["commit"]}'
exp_r=f'Reset all changes since last commit.'.ljust(38)+f'>Default:{defaults["reset"]}'
exp_p=f'Push or not.'.ljust(38)+f'>Default:{defaults["push"]}'
exp_e=f'Choose which remote repo.to push.'.ljust(38)+f'>Default:{defaults["remote"]}'
exp_p2=f'git pull {defaults["remote"]} {defaults["branch"]}'.ljust(38)+f'>Default:False'
exp_s=f'Save settings'.ljust(38)+f'>Default:False'

@click.command()
@click.option('-i', '--init',     is_flag=defaults['init'],     help=exp_i)
@click.option('-d', '--detail',   is_flag=defaults['detail'],   help=exp_d)
@click.option('-l', '--log',      is_flag=defaults['log'],      help=exp_l)
@click.option('-c', '--commit',   is_flag=defaults['commit'],   help=exp_c)
@click.option('-r', '--remote',   default=defaults['remote'],    help=exp_e)
@click.option('-p', '--push',     is_flag=defaults['push'],     help=exp_p)
@click.option('-g', '--gitpath',  default=defaults['gitpath'],  type=click.Path(exists=True), help=exp_g)
@click.option('-f', '--filepath', default=defaults['filepath'], type=str, help=exp_f)
@click.option('-b', '--branch',   default=defaults['branch'],   type=str, help=exp_b)
@click.option('-s', '--save',     is_flag='False',              help=exp_s)
@click.option('--reset',          is_flag=defaults['reset'],   type=str, help=exp_r)
@click.option('--pull',           is_flag=defaults['pull'],   type=str, help=exp_p2)
def main(init, detail, log, commit, remote, push, gitpath, filepath, branch, save, reset, pull):
#def main(init, detail, log, commit, reset, push, save, gitpath, filepath, branch, remote, pull):

    defaults['init'] = init
    defaults['gitpath'] = path.abspath(gitpath)
    defaults['filepath'] = filepath
    defaults['branch'] = branch
    defaults['detail'] = detail 
    defaults['log'] = log
    defaults['commit'] = commit
    defaults['reset'] = reset
    defaults['push'] = push
    defaults['remote'] = remote
    defaults['pull'] = pull

    if save:
        issues.execute([f'rm {defaultspath}'])
        for k, v in defaults.items():
            issues.execute([f'echo "{str(k)}:{str(v)}" >> {defaultspath}'])

    if init:
        initialize(flag=True)
    #conversion to absolute path
    gitpath = path.abspath(gitpath)
    filepath = path.abspath(filepath)

    chdir(gitpath)

    gitfolder = path.join(gitpath, '.git')
    if not path.exists(gitfolder):
        issues.warning(f'It seems path:`{gitpath}` does not have `.git` folder.')
        if click.confirm(f'Initialize?'):
            initialize()
        else:
            issues.abort()

    if reset:
        if click.confirm("Are you sure you want to reset?"):
            issues.execute(['git reset --hard'])
    issues.execute(['git status --short'])

    if log:
        issues.execute(['git log --stat --oneline --graph --decorate'])
    # Commit or not

    if isExist(f'git status --short'):
        issues.execute([f'git diff --stat'])
        if detail:
            issues.execute([f'git add .',\
                            f'git diff --cached --ignore-all-space --ignore-blank-lines',\
                            f'git reset'])
        if commit:
            issues.execute([f'git add {filepath}'])
            Commit()
    else:
        click.echo('Clean State')

    if pull:
        issues.execute([f'git pull {remote} {branch}'])

    if isExist('git branch'):
        current_branch = getCurrentBranch()
        if current_branch != branch:
            issues.branch()
            branch = setBranch(branch, filepath)
        

    # Push or not
    if not push:
        pass
        click.echo('** no push **')
    elif not isExist(f'git remote -v'):
        click.echo('** no remote repository **')
    else:
        issues.execute([f'git push -u {remote} {branch}'])

if __name__ == "__main__":
    main()
