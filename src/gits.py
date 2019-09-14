import sys
import subprocess as sp
from os import path, getcwd
from . import issues
from .qs import getAnswer, isExist, confirm, prompt
from . import diff
from .util import CursorOff, wait_key


def b(string):
    ''' String Format for Branch Name '''
    return f'`\033[3m{string}\033[m`'



def getCurrentBranch(lst=False):
    ''' Returns current branch name w or w/o branch list '''
    output = sp.getoutput('git branch').split('\n')
    current_branch = ''.join(branch[2:]
                             for branch in output if branch[0] == '*')
    branch_list = [branch[2:] for branch in output]
    if lst:
        return current_branch, branch_list
    else:
        return current_branch


def checkoutBranch(branch):
    current_branch, branch_list = getCurrentBranch(lst=True)
    if not isExist(f'git status --short'):
        issues.execute([f'git checkout {b(branch)}'])
    else:
        print(
            f'\nTheres some changes in branch {b(current_branch)}.')
        issues.execute([f'git diff --stat'])
        qs = [f'Commit changes of branch {b(current_branch)}']
        qs.append(f'Stash changes of branch {b(current_branch)} ')
        qs.append(f'Force Checkout to branch {b(branch)}        ')
        answer = getAnswer(qs)
        if answer == 1:
            issues.execute([f'git add .', f'git diff --stat'])
            Commit()
            issues.execute([f'git checkout {branch}'])
        elif answer == 2:
            issues.execute([f'git stash', f'git checkout {branch}'])
        else:
            issues.execute([f'git checkout -f {branch}'])


def setBranch(branch, filepath):
    current_branch, branch_list = getCurrentBranch(lst=True)
    if branch not in branch_list:
        issues.warning(f'Branch {b(branch)} not found.')
        qs = [f'Make new branch {b(branch)}               ']
        qs.append(f'Stay on current branch {b(current_branch)}')
        answer = getAnswer(qs)
        if answer == 1:
            issues.execute([f'git checkout -b {branch}'])
        else:
            print(f'Commiting branch set to {b(current_branch)}')
            branch = current_branch
    else:
        print(
            f'Currently on branch {b(current_branch)} but tried to commit to branch {b(branch)}.')
        qs = [f'Merge branch {b(current_branch)} => branch {b(branch)}']
        qs.append(f'Stay on branch {b(current_branch)}                   ')
        qs.append(f'Checkout to branch {b(branch)}                       ')
        answer = getAnswer(qs)
        if answer == 2:
            print(f'Committing branch is now set to {b(current_branch)}')
            branch = current_branch
        else:
            checkoutBranch(branch)
            if answer == 1:
                issues.execute(
                    [f'git format-patch {branch}..{current_branch} --stdout | git apply --check'])
                if isExist('git format-patch {branch}..{current_branch} --stdout | git apply --check'):
                    issues.execute([f'git merge {current_branch}'])
                else:
                    issues.warning(
                        "Aborting Merge because conflict is likely to occur.")
                    issues.abort()

    return branch









def MakeNewBranch(branch_list):
    while 1:
        new_branch = prompt(
            '\nEnter new branch name (spaces will be replaced with `-`)').replace(' ', '-')
        if new_branch in branch_list:
            issues.warning(f'Branch `{new_branch}` already exists!')
        else:
            issues.ok(f'\bBranch `{new_branch}` successfully created!')
            if confirm(f'Checkout to `{new_branch}`'):
                issues.execute([f'git checkout -b {new_branch}'])
            else:
                issues.execute([f'git branch {new_branch}'])
            break


def Checkout():
    current_branch, branch_list = getCurrentBranch(lst=True)
    branch_list.append('Make new branch')
    branch = [b for b in branch_list if b != current_branch]
    if len(branch) == 1:
        if confirm(f"Make new branch?"):
            MakeNewBranch(branch_list)
    else:
        print(f'\n\033[m\033[1mWhich branch do you want to checkout?\033[m')
        answer = getAnswer(branch)
        if answer == len(branch):
            MakeNewBranch(branch_list)
        else:
            issues.execute([f'git checkout {branch[answer-1]}'])
            issues.execute([f'git diff {current_branch}..{branch[answer-1]}'])



def RenameBranch():
    current_branch, branch_list = getCurrentBranch(lst=True)
    while 1:
        new_branch = prompt(
            '\n\033[2KEnter new branch name (spaces will be replaced with `-`)').replace(' ', '-')

        if new_branch in branch_list:
            issues.warning(f'Branch `{new_branch}` already exists!')
        else:
            issues.execute([f'git branch -m {new_branch}'])
            issues.ok(f'Branch `{current_branch}` is now `{new_branch}`')
            break


def DeleteBranch():
    current_branch, branch_list = getCurrentBranch(lst=True)
    print(f'\nCurrently on branch: {b(current_branch)}...\033[m\n')

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
            f"Please choose the branch to checkout before deleting {b(branch)}:\n")
        answer = getAnswer(next_list, exit=False) - 1
    else:
        if confirm(f"Delete branch {b(branch)}?"):
            issues.execute([f'git branch --delete {branch}'])
            issues.ok('You deleted branch!')


def Branch():
    if isExist('git branch'):
        issues.execute([f'git branch'])
        current_branch, branch_list = getCurrentBranch(lst=True)
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
            Checkout()
        elif answer == 'r':
            issues.ok('Renaming current branch!')
            RenameBranch()
        elif answer == 'n':
            issues.ok('Making new branch!')
            MakeNewBranch(branch_list)
        elif answer == 'd':
            DeleteBranch()
    else:
        issues.warning('branch not found!')
        branch = 'master'
        issues.ok('Branch set to {b(master)}...')
    branch = getCurrentBranch()
    issues.ok(f'Branch set to {b(branch)}...')
    return branch