import sys
import subprocess as sp
from os import path, getcwd
from . import issues
from .qs import getAnswer, isExist, confirm, prompt
from . import diff
from .util import CursorOff, wait_key, B
from .git.branch import getBranch, setBranch, newBranch, renameBranch


def DeleteBranch():
    current_branch, branch_list = getBranch(lst=True)
    print(f'\nCurrently on branch: {B(current_branch)}...\033[m\n')

    branch_list = [branch for branch in branch_list]
    print("Which branch do you want to delete?:\n")
    answer = getAnswer(branch_list, exit=False) - 1
    branch = branch_list[answer]
    if branch == 'master':
        issues.warning('You cannot delete master branch via gch.')
    elif branch == current_branch:
        msg = f"You tried to delete branch you are currently on"
        issues.warning(msg)
        next_list = [b for b in branch_list if b != current_branch]
        print(
            f"Please choose the branch to checkout before deleting {B(branch)}:\n")
        answer = getAnswer(next_list, exit=False) - 1
    else:
        if confirm(f"Delete branch {B(branch)}?"):
            issues.execute([f'git branch --delete {branch}'])
            issues.ok('You deleted branch!')


def Branch():
    if isExist('git branch'):
        issues.execute([f'git branch'])
        current_branch, branch_list = getBranch(lst=True)
        with CursorOff():
            options = ['(c) checkout']
            options.append('(r) rename')
            options.append('(n) new branch')
            options.append('(d) delete')
            print(f"\n\033[1mOptions:\033[m\n {' '.join(options)} (e) exit")
            answer = wait_key()
            while 1:
                if answer in ['c', 'r', 'n', 'd', 'e']:
                    break
                answer = wait_key()
        if answer == 'c':
            issues.ok('Checking out branch!')
            Checkout(current_branch, branch)
        elif answer == 'r':
            issues.ok('Renaming current branch!')
            renameBranch()
        elif answer == 'n':
            issues.ok('Making new branch!')
            newBranch(branch_list)
        elif answer == 'd':
            DeleteBranch()
    else:
        issues.warning('branch not found!')
        branch = 'master'
    branch = getBranch()
    issues.ok(f'Branch set to {B(branch)}...')
    return branch
