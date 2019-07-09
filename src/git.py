import click
import sys, subprocess as sp
from os import path, chdir, getcwd
from pathlib import Path
from urllib.parse import urlparse

from . import issues
from . import qs
from . import diff

getAnswer = qs.getAnswer
isExist = qs.isExist

def b(string):
    ''' String Format for Branch Name '''
    return f'\033[3m\033[33m{string}\033[0m'

def CheckState():
    if isExist(f'git status --short'):
        return True
    else:
        issues.ok('Clean State')
        return False

def Commit():
    ''' Commit '''
    commit_message = click.prompt("Commit Message", type=str)
    issues.execute([f'git commit -m "{commit_message}"'])

def getCurrentBranch(lst=False):
    ''' Returns current branch name w or w/o branch list '''
    l = sp.getoutput('git branch').split('\n')
    current_branch = ''.join(branch[2:] for branch in l if branch[0]=='*')
    branch_list = [branch[2:] for branch in l]
    if lst:
        return current_branch, branch_list
    else:
        return current_branch

def setBranch(branch, filepath):
    current_branch, branch_list = getCurrentBranch(lst=True)
    if branch not in branch_list:
        issues.warning(f'Branch `{b(branch)}` not found.')
        qs =     [f'Make new branch `{b(branch)}`               ']
        qs.append(f'Stay on current branch `{b(current_branch)}`')
        answer = getAnswer(qs)
        if answer == 1:
            issues.execute([f'git checkout -b {branch}'])
        else:
            click.echo(f'Commiting branch set to {b(current_branch)}')
            branch = current_branch
    else:
        click.echo(f'Currently on branch `{b(current_branch)}` but tried to commit to branch `{b(branch)}`.')
        qs =     [f'Merge branch `{b(current_branch)}` => branch `{b(branch)}`']
        qs.append(f'Stay on branch `{b(current_branch)}`                   ')
        qs.append(f'Checkout to branch `{b(branch)}`                       ')
        answer = getAnswer(qs)
        if answer == 2:
            click.echo(f'Commiting branch is now set to `{b(current_branch)}`')
            branch = current_branch
        else:
            if not isExist(f'git status --short'):
                issues.execute([f'git checkout {branch}'])
            else:
                click.echo(f'\nTheres some changes in branch `{b(current_branch)}`.')
                issues.execute([f'git diff --stat'])
                qs =     [f'Commit changes of branch `{b(current_branch)}`']
                qs.append(f'Stash changes of branch `{b(current_branch)}` ')
                qs.append(f'Force Checkout to branch `{b(branch)}`        ')
                answer_2 = getAnswer(qs)
                if answer_2 == 1:
                    issues.execute([f'git add .',f'git diff --stat'])
                    Commit()
                    issues.execute([f'git checkout {branch}'])
                elif answer_2 == 2:
                    issues.execute([f'git stash',f'git checkout {branch}'])
                else:
                    issues.execute([f'git checkout -f {branch}'])
            if answer == 1:
                issues.execute([f'git format-patch {branch}..{current_branch} --stdout | git apply --check'])
                if isExist('git format-patch {branch}..{current_branch} --stdout | git apply --check'):
                    issues.execute([f'git merge {current_branch}'])
                else:
                    issues.warning("Aborting Merge because conflict is likely to occur.")
                    issues.abort()
    return branch

def globalsetting():
    click.echo("** Configureation of global settings **")
    issues.execute(['git config --global credential.helper osxkeychain',\
                    'git config --global core.excludesfile ~/.gitignore_global'])
    name, email = click.prompt("name", type=str), click.prompt("email", type=str)
    issues.execute([f'git config --global user.name "{name}"',\
                    f'git config --global user.email {email}'])

    if click.confirm('Do you want to use emacs instead of vim as an editor?'):
        issues.execute([f'git config --global core.editor emacs'])
    else:
        issues.execute([f'git config --global core.editor vim'])
        
    if click.confirm('Do you want to use ediff instead of vimdiff?'):
        issues.execute([f'git config --global {x}.tool ediff' for x in ['diff', 'merge']])
    else:
        issues.execute([f'git config --global {x}.tool vimdff' for x in ['diff', 'merge']])
    format_string ="'%h %Cred%d %Cgreen%ad %Cblue%cn %Creset%s'" 
    string = f'"log --graph --date-order --all --pretty=format:{format_string} --date=short"'
    issues.execute([f"git config --global alias.graph {string}"])
    issues.execute([f'cat ~/.gitconfig'])

def initialize(flag=False):
    if flag:
        issues.execute([f'cat ~/.gitconfig'])
        globalsetting()
        sys.exit()
    else:
        # git confi
        gitconfigpath = path.join(path.expanduser('~'), '.gitconfig')
        if not path.exists(gitconfigpath):
            click.echo("~/.gitconfig file does not exist. => Start Initialization!")
            globalsetting()
        readmepath = path.join(getcwd(), 'README.md')
        if not path.exists(readmepath):
            title = click.prompt('Title of this repository(project)').upper()
            issues.execute(['git init', 'touch .gitignore', 'touch README.md',\
                            'echo ".*" >> .gitignore', \
                            'echo ".default.txt" >> .gitignore', \
                            f'echo "# {title}" >> README.md'])
            issues.execute(['git add -f .gitignore'])

def Update():
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

def Reset():
    if click.confirm("Are you sure you want to reset?"):
        issues.warning('Options with `--hard` must be done with caution')
        opt=[]
        opt.append('\033[3mgit commit --amend\033[0m          > Change message of last commit')
        opt.append('\033[3mgit reset --soft HEAD^\033[0m      > Undo last commit (soft)')
        opt.append('\033[3mgit reset \033[91m--hard\033[0m\033[3m HEAD^\033[0m      > Undo last commit')
        opt.append('\033[3mgit reset \033[91m--hard\033[0m\033[3m HEAD\033[0m       > Undo changes from last commit')
        opt.append('\033[3mgit reset \033[91m--hard\033[0m\033[3m <hash>\033[0m     > Undo changes from past commit')
        opt.append('\033[3mgit reset \033[91m--hard\033[0m\033[3m ORIG_HEAD\033[0m  > Undo most recent reset')
        ans = getAnswer(opt)
        if ans == 1:
            issues.execute(['git commit --amend'])
        elif ans == 2:
            issues.execute(['git reset --soft HEAD^'])
        elif ans == 3:
            issues.execute(['git reset --hard HEAD^'])
        elif ans == 4:
            issues.execute(['git reset --hard HEAD'])
        elif ans == 5:
            issues.warning('Select hash from diff tool...')
            flag = False
            if click.confirm('Do you want to name specific author?'):
                flag = True
            dhash = diff.diffhash(verbose=True, head=True, author=flag)
            while(1):
                if click.confirm("Is this the correct hash you want to go back?"):
                    break
                dhash = diff.diffhash(verbose=True, head=True, author=flag)
            if click.confirm(f"Go back (reset) to {dhash}?"):
                if not isExist(f'git status --short'):
                    issues.execute([f'git reset --hard {dhash}'])
                else:
                    click.echo(f'\nTheres some changes not commited..')
                    issues.execute([f'git diff --stat'])
                    qs =     [f'Commit changes before reset']
                    qs.append(f'Stash changes before reset')
                    qs.append(f'Force Checkout before reset')
                    ans = getAnswer(qs)
                    if ans == 1:
                        issues.execute([f'git add .',f'git diff --stat'])
                        Commit()
                        issues.execute([f'git reset --hard {dhash}'])
                    elif ans == 2:
                        issues.execute([f'git stash',f'git reset --hard {dhash}'])
                    else:
                        issues.execute([f'git reset --hard {dhash}'])
        elif ans == 5:
            issues.execute([f'git reset --hard ORIG_HEAD'])


def url_valid(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

def Push(remote, branch):
    remotelst = sp.getoutput(f'git remote -v').split('\n')
    remotelst = [r.split('\t')[0] for idx, r in enumerate(remotelst) if idx%2]
    if remote in remotelst:
        issues.execute([f'git push -u {remote} {branch}'])
    else:
        issues.warning(f'Remote repository `{remote}` not found')
        if click.confirm(f'Add?'):
            while(1):
                remote_url = click.prompt("URL", type=str)
                if url_valid(remote_url):
                    issues.execute([f'git remote add {remote} {remote_url}'])
                    issues.execute([f'git push -u {remote} {branch}'])
                    break
                else:
                    issues.warning('Not valid URL')




