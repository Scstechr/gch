import sys, subprocess as sp
from os import path, chdir, getcwd
from pathlib import Path
from urllib.parse import urlparse

from . import issues
from .qs import getAnswer, isExist, confirm, prompt, echo
from . import diff

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
    commit_message = prompt("Commit Message [v:vim mode]")
    if commit_message in ['v', 'vi', 'vim']:
        issues.execute([f'git commit'])
    else:
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
            echo(f'Commiting branch set to {b(current_branch)}')
            branch = current_branch
    else:
        echo(f'Currently on branch `{b(current_branch)}` but tried to commit to branch `{b(branch)}`.')
        qs =     [f'Merge branch `{b(current_branch)}` => branch `{b(branch)}`']
        qs.append(f'Stay on branch `{b(current_branch)}`                   ')
        qs.append(f'Checkout to branch `{b(branch)}`                       ')
        answer = getAnswer(qs)
        if answer == 2:
            echo(f'Commiting branch is now set to `{b(current_branch)}`')
            branch = current_branch
        else:
            if not isExist(f'git status --short'):
                issues.execute([f'git checkout {branch}'])
            else:
                echo(f'\nTheres some changes in branch `{b(current_branch)}`.')
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
    echo("** Configureation of global settings **")
    issues.execute(['git config --global credential.helper osxkeychain',\
                    'git config --global core.excludesfile ~/.gitignore_global'])
    name, email = prompt("name"), prompt("email")
    issues.execute([f'git config --global user.name "{name}"',\
                    f'git config --global user.email {email}'])

    if confirm('Do you want to use emacs instead of vim as an editor?'):
        issues.execute([f'git config --global core.editor emacs'])
    else:
        issues.execute([f'git config --global core.editor vim'])
        
    if confirm('Do you want to use ediff instead of vimdiff?'):
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
    # git config
    gitconfigpath = path.join(path.expanduser('~'), '.gitconfig')
    if not path.exists(gitconfigpath):
        echo("~/.gitconfig file does not exist. => Start Initialization!")
        globalsetting()

    issues.execute(['git init'])

    # README.md
    readmepath = path.join(getcwd(), 'README.md')
    title = prompt('Title of this repository(project)')
    if path.exists(readmepath):
        if confirm('Do you want to remove the existing README.md?'):
            issues.execute([f'rm README.md'])
            issues.execute([f'echo "# {title}" >> README.md'])
    else:
        issues.execute(['touch README.md'])
        issues.execute([f'echo "# {title}" >> README.md'])

    # .gitignore
    ignorepath = path.join(getcwd(), '.gitignore')
    if not path.exists(readmepath):
        issues.execute(['touch .gitignore'])
        issues.execute([f'echo ".*" >> .gitignore'])
        issues.execute([f'echo ".default.txt" >> .gitignore'])
    issues.execute(['git add -f .gitignore'])

def Reset():
    if confirm("Are you sure you want to reset?"):
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
            if confirm('Do you want to name specific author?'):
                flag = True
            dhash = diff.diffhash(verbose=True, head=True, author=flag)
            while(1):
                if confirm("Is this the correct hash you want to go back?"):
                    break
                dhash = diff.diffhash(verbose=True, head=True, author=flag)
            if confirm(f"Go back (reset) to {dhash}?"):
                if not isExist(f'git status --short'):
                    issues.execute([f'git reset --hard {dhash}'])
                else:
                    echo(f'\nTheres some changes not commited..')
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

def Remote(remote):
    remotelst = sp.getoutput(f'git remote -v').split('\n')
    remotelst = [r.split('\t')[0] for idx, r in enumerate(remotelst) if idx%2]
    if remote in remotelst:
        pass
    else:
        issues.warning(f'Remote branch `{remote}` not found')
        if confirm(f'Add?'):
            while(1):
                remote_url = prompt("URL")
                if url_valid(remote_url):
                    issues.execute([f'git remote add {remote} {remote_url}'])
                    break
                else:
                    issues.warning('Not valid URL')
        else:
            sys.exit()

def Push(remote, branch):
    Remote(remote)
    issues.execute([f'git push -u {remote} {branch}'])

def Checkout():
    current_branch, branch_list = getCurrentBranch(lst=True)
    branch_list.append('[MAKE NEW BRANCH]')
    echo(f'\n\033[1mCURRENTLY ON: \033[3m{current_branch}')
    echo(f'\n\033[0m\033[1mWhich branch do you want to checkout?\033[0m')
    branch = [b for b in branch_list if b != current_branch]
    answer = getAnswer(branch)
    if answer == len(branch):
        while 1:
            new_branch = prompt('Enter new branch name')
            if new_branch in branch_list:
                issues.warning(f'Branch {new_branch} already exists!')
            else:
                if confirm(f'Checkout to {new_branch}'):
                    issues.execute([f'git checkout -b {new_branch}'])
                else:
                    issues.execute([f'git branch {new_branch}'])
                break

    else:
        issues.execute([f'git checkout {branch[answer-1]}'])
        issues.execute([f'git diff {current_branch}..{branch[answer-1]}'])
