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
import pysrc.git as git
from pysrc.diff import diffhash

issues.version(3)
from pathlib import Path

defaults = {}
defaults['init'] = 'False'
defaults['gitpath'] = '.'
defaults['filepath'] = '.'
defaults['branch'] = 'master'
defaults['verbose'] = 'False'
defaults['log'] = 'False'
defaults['commit'] = 'False'
defaults['reset'] = 'False'
defaults['push'] = 'False'
defaults['remote'] = 'origin'
defaults['pull'] = 'False'
defaults['update'] = 'False'
defaults['diff'] = 'False'
defaultspath = path.join(".", ".defaults.txt")
if path.exists(defaultspath):
    with open(defaultspath, 'r') as readfile:
        for line in readfile:
            k, v = line.replace('\n','').split(":")
            defaults[str(k)] = str(v)

# git commands 
diffcmd = 'git diff --cached --ignore-all-space --ignore-blank-lines'
logcmd =  'git log --stat --oneline --graph --decorate'

# Explanation of the options showed in --help flag
exp_i=f'Run initializer or not.'.ljust(38)+f'>Default:{defaults["init"]}'
exp_g=f'Path of dir that contains `.git`.'.ljust(38)+f'>Default:{defaults["gitpath"]}'
exp_f=f'Path/Regex of staging file/dir.'.ljust(38)+f'>Default:{defaults["filepath"]}'
exp_b=f'Commiting branch.'.ljust(38)+f'>Default:{defaults["branch"]}'
exp_d=f'Detailed diff.'.ljust(38)+f'>Default:{defaults["verbose"]}'
exp_l=f'Git log with option.'.ljust(38)+f'>Default:{defaults["log"]}'
exp_c=f'Commit or not.'.ljust(38)+f'>Default:{defaults["commit"]}'
exp_r=f'Reset all changes since last commit.'.ljust(38)+f'>Default:{defaults["reset"]}'
exp_p=f'Push or not.'.ljust(38)+f'>Default:{defaults["push"]}'
exp_e=f'Choose which remote repo.to push.'.ljust(38)+f'>Default:{defaults["remote"]}'
exp_p2=f'Pull from <{defaults["remote"]}> <{defaults["branch"]}>.'.ljust(38)+f'>Default:False'
exp_s=f'Save settings'.ljust(38)+f'>Default:False'
exp_u=f'Update gch'.ljust(38)+f'>Default:False'
exp_d2=f'Open diff tool'.ljust(38)+f'>Default:False'

@click.command()
@click.option('-i', '--init',     is_flag=defaults['init'],     help=exp_i)
@click.option('-v', '--verbose',   is_flag=defaults['verbose'],   help=exp_d)
@click.option('-l', '--log',      is_flag=defaults['log'],      help=exp_l)
@click.option('-c', '--commit',   is_flag=defaults['commit'],   help=exp_c)
@click.option('-r', '--remote',   default=defaults['remote'],    help=exp_e)
@click.option('-p', '--push',     is_flag=defaults['push'],     help=exp_p)
@click.option('-g', '--gitpath',  default=defaults['gitpath'],  type=click.Path(exists=True), help=exp_g)
@click.option('-f', '--filepath', default=defaults['filepath'], type=str, help=exp_f)
@click.option('-b', '--branch',   default=defaults['branch'],   type=str, help=exp_b)
@click.option('-s', '--save',     is_flag='False',              help=exp_s)
@click.option('--reset',          is_flag=defaults['reset'],    type=str, help=exp_r)
@click.option('--pull',           is_flag=defaults['pull'],     type=str, help=exp_p2)
@click.option('-u', '--update',   is_flag=defaults['update'],   type=str, help=exp_u)
@click.option('-d', '--diff',     is_flag=defaults['diff'],     type=str, help=exp_d2)
def main(init,
         verbose,
         log,
         commit,
         remote,
         push,
         gitpath,
         filepath,
         branch,
         save,
         reset,
         pull,
         update,
         diff
         ):
#def main(init, verbose, log, commit, reset, push, save, gitpath, filepath, branch, remote, pull):

    defaults['init'] = init
    defaults['gitpath'] = path.abspath(gitpath)
    defaults['filepath'] = filepath
    defaults['branch'] = branch
    defaults['verbose'] = verbose 
    defaults['log'] = log
    defaults['commit'] = commit
    defaults['reset'] = reset
    defaults['push'] = push
    defaults['remote'] = remote
    defaults['pull'] = pull
    defaults['update'] = update
    defaults['diff'] = diff

    if diff:
        diffhash(detail=verbose, head=False)
        exit(1)

    if reset:
        git.reset()

    issues.execute(['git status --short'])

    if update:
        if click.confirm(f'Update? (will execute pull from origin repository of gch)'):
            exepath = Path(__file__).parent
            current = Path('.')
            chdir(exepath)
            issues.execute(['pwd',
                            f'git checkout master',
                            f'git pull origin master',
                            ])
            #issues.execute(#['cd ~/.gch'])
            chdir(current)
        else:
            issues.abort()


    if len(branch) == 0:
        issues.execute(['git branch'])

    if save:
        issues.execute([f'rm {defaultspath}'])
        for k, v in defaults.items():
            issues.execute([f'echo "{str(k)}:{str(v)}" >> {defaultspath}'])

    if init:
        git.initialize(flag=True)
    #conversion to absolute path
    gitpath = path.abspath(gitpath)
    filepath = path.abspath(filepath)

    chdir(gitpath)

    gitfolder = path.join(gitpath, '.git')
    if not path.exists(gitfolder):
        issues.warning(f'It seems path:`{gitpath}` does not have `.git` folder.')
        if click.confirm(f'Initialize?'):
            git.initialize()
        else:
            issues.abort()


    if log:
        issues.execute([logcmd])
    # Commit or not

    if git.CheckState():
        issues.execute([f'git diff --stat'])
        if verbose:
            issues.execute([f'git add .', diffcmd, f'git reset'])
        if commit:
            issues.execute([f'git add {filepath}'])
            git.Commit()

    if pull:
        issues.execute([f'git pull {remote} {branch}'])

    if isExist('git branch'):
        current_branch = git.getCurrentBranch()
        if len(branch):
            if current_branch != branch:
                issues.branch()
                branch = git.setBranch(branch, filepath)
        

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
