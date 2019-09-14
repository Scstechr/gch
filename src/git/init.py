import sys
import subprocess as sp
from os import path, getcwd

from .. import issues
from .. import qs

def Init(flag=False):
    if flag:
        issues.execute([f'cat ~/.gitconfig'])
        globalsetting()
        sys.exit()
    # git config
    gitconfigpath = path.join(path.expanduser('~'), '.gitconfig')
    if not path.exists(gitconfigpath):
        print("~/.gitconfig file does not exist. => Start Initialization!")
        globalsetting()

    issues.execute(['git init'])

    # README.md
    readmepath = path.join(getcwd(), 'README.md')
    title = qs.prompt('Title of this repository(project)')
    if path.exists(readmepath):
        if qs.confirm('Do you want to remove the existing README.md?'):
            issues.execute([f'rm README.md'])
            issues.execute([f'echo "# {title}" >> README.md'])
    else:
        issues.execute(['touch README.md'])
        issues.execute([f'echo "# {title}" >> README.md'])

    # .gitignore
    ignorepath = path.join(getcwd(), '.gitignore')
    if not path.exists(ignorepath):
        issues.execute(['touch .gitignore'])
        issues.execute([f'echo ".*" >> .gitignore'])
        issues.execute([f'echo ".default.txt" >> .gitignore'])
    issues.execute(['git add -f .gitignore'])


def GlobalSetting():
    print("** Configuration of global settings **")
    issues.execute(['git config --global credential.helper osxkeychain',
                    'git config --global core.excludesfile ~/.gitignore_global'])
    name, email = prompt("name"), prompt("email")
    issues.execute([f'git config --global user.name "{name}"',
                    f'git config --global user.email {email}'])

    if qs.confirm('Do you want to use emacs instead of vim as an editor?'):
        issues.execute([f'git config --global core.editor emacs'])
    else:
        issues.execute([f'git config --global core.editor vim'])

    if qs.confirm('Do you want to use ediff instead of vimdiff?'):
        issues.execute(
            [f'git config --global {x}.tool ediff' for x in ['diff', 'merge']])
    else:
        issues.execute(
            [f'git config --global {x}.tool vimdff' for x in ['diff', 'merge']])
    format_string = "'%h %Cred%d %Cgreen%ad %Cblue%cn %Creset%s'"
    string = f'"log --graph --date-order --all --pretty=format:{format_string} --date=short"'
    issues.execute([f"git config --global alias.graph {string}"])
    issues.execute([f'cat ~/.gitconfig'])

