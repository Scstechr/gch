import sys
import subprocess as sp
from os import path, getcwd

from ..issues import warning, execute, abort
from ..qs import prompt, confirm

def Init(flag=False):
    if flag:
        execute([f'cat ~/.gitconfig'])
        GlobalSetting()
        sys.exit()
    # git config
    gitconfigpath = path.join(path.expanduser('~'), '.gitconfig')
    if not path.exists(gitconfigpath):
        print("~/.gitconfig file does not exist. => Start Initialization!")
        GlobalSetting()

    execute(['git init'])

    # README.md
    readmepath = path.join(getcwd(), 'README.md')
    title = prompt('Title of this repository(project)')
    if path.exists(readmepath):
        if confirm('Do you want to remove the existing README.md?'):
            execute([f'rm README.md'])
            execute([f'echo "# {title}" >> README.md'])
    else:
        execute(['touch README.md'])
        execute([f'echo "# {title}" >> README.md'])

    # .gitignore
    ignorepath = path.join(getcwd(), '.gitignore')
    if not path.exists(ignorepath):
        execute(['touch .gitignore'])
        execute([f'echo ".*" >> .gitignore'])
        execute([f'echo ".default.txt" >> .gitignore'])
    execute(['git add -f .gitignore'])


def GlobalSetting():
    print("** Configuration of global settings **")
    execute(['git config --global credential.helper osxkeychain',
                    'git config --global core.excludesfile ~/.gitignore_global'])
    name, email = prompt("name"), prompt("email")
    execute([f'git config --global user.name "{name}"',
                    f'git config --global user.email {email}'])

    if confirm('Do you want to use emacs instead of vim as an editor?'):
        execute([f'git config --global core.editor emacs'])
    else:
        execute([f'git config --global core.editor vim'])

    if confirm('Do you want to use ediff instead of vimdiff?'):
        execute(
            [f'git config --global {x}.tool ediff' for x in ['diff', 'merge']])
    else:
        execute(
            [f'git config --global {x}.tool vimdff' for x in ['diff', 'merge']])
    format_string = "'%h %Cred%d %Cgreen%ad %Cblue%cn %Creset%s'"
    string = f'"log --graph --date-order --all --pretty=format:{format_string} --date=short"'
    execute([f"git config --global alias.graph {string}"])
    execute([f'cat ~/.gitconfig'])

