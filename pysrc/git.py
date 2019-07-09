import click
import sys, subprocess as sp
from os import path, chdir, getcwd

from . import issues
from . import qs

getAnswer = qs.getAnswer
isExist = qs.isExist

def b(string):
    ''' String Format for Branch Name '''
    return f'\033[3m\033[33m{string}\033[0m'

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
                            'echo ".*" >> .gitignore', f'echo ".*" >> ~/.gitignore_global',\
                            f'echo "# {title}" >> README.md'])
            issues.execute(['git add -f .gitignore'])

def update():
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
